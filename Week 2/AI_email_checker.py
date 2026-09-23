def valideer_email(email):
    if " " in email:
        return False
    
    if email.count("@") != 1:
        return False
    
    gebruikersnaam, domein = email.split("@")
    
    if gebruikersnaam == "":
        return False
    
    if "." not in domein:
        return False
    
    if domein.startswith(".") or domein.endswith("."):
        return False
    
    return True

import re
import socket
import ipaddress
import unicodedata
from dataclasses import dataclass
from typing import Optional


# ============================================================
# CONFIGURATIE
# ============================================================

MAX_EMAIL_LENGTH = 254
MAX_LOCAL_LENGTH = 25
MAX_DOMAIN_LENGTH = 255
MAX_DOMAIN_LABEL_LENGTH = 63

# RFC-achtige atom characters voor het local-part.
ATEXT_CHARS = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789"
    "!#$%&'*+-/=?^_`{|}~."
)

# Controle op control characters.
CONTROL_CHAR_PATTERN = re.compile(r"[\x00-\x1F\x7F]")

# Geldige standaard domein-labels.
DOMAIN_LABEL_PATTERN = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?$"
)

# TLD moet uit letters bestaan.
TLD_PATTERN = re.compile(r"^[A-Za-z]{2,63}$")


# ============================================================
# RESULTAATOBJECT
# ============================================================

@dataclass
class EmailValidationResult:
    geldig: bool
    foutcode: Optional[str] = None
    melding: Optional[str] = None
    genormaliseerd: Optional[str] = None
    local_part: Optional[str] = None
    domein: Optional[str] = None


# ============================================================
# BASISCONTROLES
# ============================================================

def _is_string(email):
    """Controleert of de invoer een string is."""
    return isinstance(email, str)


def _heeft_control_characters(tekst):
    """Controleert op ASCII control characters."""
    return CONTROL_CHAR_PATTERN.search(tekst) is not None


def _heeft_whitespace(tekst):
    """Controleert op alle soorten whitespace."""
    return any(char.isspace() for char in tekst)


def _normaliseer_email(email):
    """
    Normaliseert Unicode naar NFC.
    Hierdoor worden equivalent weergegeven Unicode-tekens
    zoveel mogelijk gelijk behandeld.
    """
    return unicodedata.normalize("NFC", email)


# ============================================================
# LOCAL-PART
# ============================================================

def _is_valid_atext_character(char):
    """Controleert of een teken in een atom mag voorkomen."""
    return char in ATEXT_CHARS


def _validate_unquoted_local(local):
    """
    Controleert het normale local-part.

    Voorbeeld:
        john.doe
        john123
        john-doe
        john+test
    """

    if not local:
        return False, "LOCAL_EMPTY", "Het lokale gedeelte is leeg."

    # Lengte in bytes.
    if len(local.encode("utf-8")) > MAX_LOCAL_LENGTH:
        return False, "LOCAL_TOO_LONG", (
            "Het lokale gedeelte is langer dan 64 bytes."
        )

    # Begin/einde mag geen punt zijn.
    if local.startswith("."):
        return False, "LOCAL_START_DOT", (
            "Het lokale gedeelte mag niet met een punt beginnen."
        )

    if local.endswith("."):
        return False, "LOCAL_END_DOT", (
            "Het lokale gedeelte mag niet met een punt eindigen."
        )

    # Twee punten achter elkaar zijn ongeldig.
    if ".." in local:
        return False, "LOCAL_DOUBLE_DOT", (
            "Het lokale gedeelte bevat twee punten achter elkaar."
        )

    # Controleer ieder teken.
    for char in local:

        # Unicode letters kunnen in SMTPUTF8 toegestaan zijn.
        if ord(char) > 127:
            if char.isalnum():
                continue

        if not _is_valid_atext_character(char):
            return False, "LOCAL_INVALID_CHARACTER", (
                f"Ongeldig teken in local-part: {char!r}"
            )

    return True, None, None


def _validate_quoted_local(local):
    """
    Controleert een quoted local-part.

    Voorbeeld:
        "john doe"
        "john\\doe"
    """

    if len(local) < 2:
        return False, "QUOTED_INVALID", (
            "Quoted local-part is ongeldig."
        )

    if not (local.startswith('"') and local.endswith('"')):
        return False, "QUOTED_INVALID", (
            "Quoted local-part moet beginnen en eindigen met dubbele quotes."
        )

    inhoud = local[1:-1]

    if not inhoud:
        return False, "QUOTED_EMPTY", (
            "Quoted local-part mag niet leeg zijn."
        )

    # Controleer escaped characters.
    i = 0

    while i < len(inhoud):

        char = inhoud[i]

        if char == "\\":

            # Escape moet gevolgd worden door een teken.
            if i + 1 >= len(inhoud):
                return False, "QUOTED_ESCAPE", (
                    "Backslash aan het einde van quoted local-part."
                )

            i += 2
            continue

        # Ongeëscapete quote mag niet voorkomen.
        if char == '"':
            return False, "QUOTED_QUOTE", (
                "Ongeëscapete dubbele quote gevonden."
            )

        # CR/LF en control characters zijn niet toegestaan.
        if char in "\r\n":
            return False, "QUOTED_NEWLINE", (
                "Quoted local-part mag geen newline bevatten."
            )

        if ord(char) < 32 or ord(char) == 127:
            return False, "QUOTED_CONTROL", (
                "Quoted local-part bevat een control character."
            )

        i += 1

    return True, None, None


def _validate_local(local, allow_quoted=True):
    """Complete controle van het local-part."""

    if not local:
        return False, "LOCAL_EMPTY", "Local-part is leeg."

    if local.startswith('"') or local.endswith('"'):

        if not allow_quoted:
            return False, "QUOTED_NOT_ALLOWED", (
                "Quoted local-parts zijn uitgeschakeld."
            )

        return _validate_quoted_local(local)

    return _validate_unquoted_local(local)


# ============================================================
# DOMAIN
# ============================================================

def _is_ipv4(domain):
    """Controleert of het domein een IPv4-adres is."""
    try:
        ipaddress.IPv4Address(domain)
        return True
    except ValueError:
        return False


def _is_ipv6(domain):
    """Controleert of het domein een IPv6-adres is."""
    try:
        ipaddress.IPv6Address(domain)
        return True
    except ValueError:
        return False


def _validate_domain_literal(domain):
    """
    Controleert domeinen zoals:

        [192.168.1.10]
        [IPv6:2001:db8::1]
    """

    if not (domain.startswith("[") and domain.endswith("]")):
        return False, "NOT_LITERAL", None

    inhoud = domain[1:-1]

    if inhoud.startswith("IPv6:"):
        adres = inhoud[5:]

        if not _is_ipv6(adres):
            return False, "INVALID_IPV6", (
                "De IPv6 domein-literal is ongeldig."
            )

        return True, None, None

    if _is_ipv4(inhoud):
        return True, None, None

    return False, "INVALID_DOMAIN_LITERAL", (
        "De domein-literal is geen geldig IPv4- of IPv6-adres."
    )


def _convert_domain_to_idna(domain):
    """
    Zet een Unicode-domein om naar IDNA/ASCII.

    Bijvoorbeeld:

        münchen.de
            ->
        xn--mnchen-3ya.de
    """

    try:
        return domain.encode("idna").decode("ascii")
    except UnicodeError:
        return None


def _validate_domain_labels(domain):
    """
    Controleert alle labels van een normaal domein.
    """

    labels = domain.split(".")

    # Domein moet uit minimaal twee labels bestaan.
    if len(labels) < 2:
        return False, "DOMAIN_NO_TLD", (
            "Het domein moet minimaal één punt en een TLD hebben."
        )

    for label in labels:

        # Lege labels.
        if not label:
            return False, "DOMAIN_EMPTY_LABEL", (
                "Het domein bevat een leeg label."
            )

        # Maximale lengte per label.
        if len(label.encode("ascii")) > MAX_DOMAIN_LABEL_LENGTH:
            return False, "DOMAIN_LABEL_TOO_LONG", (
                f"Domeinlabel {label!r} is langer dan 63 bytes."
            )

        # Een label mag niet beginnen met een koppelteken.
        if label.startswith("-"):
            return False, "DOMAIN_LABEL_START_HYPHEN", (
                f"Domeinlabel {label!r} begint met '-'."
            )

        # Een label mag niet eindigen met een koppelteken.
        if label.endswith("-"):
            return False, "DOMAIN_LABEL_END_HYPHEN", (
                f"Domeinlabel {label!r} eindigt met '-'."
            )

        # Controle standaard domein-karakters.
        if not DOMAIN_LABEL_PATTERN.fullmatch(label):
            return False, "DOMAIN_INVALID_CHARACTER", (
                f"Ongeldig teken in domeinlabel {label!r}."
            )

    # Controle TLD.
    tld = labels[-1]

    if not TLD_PATTERN.fullmatch(tld):
        return False, "DOMAIN_INVALID_TLD", (
            "De TLD moet uit 2 tot 63 letters bestaan."
        )

    return True, None, None


def _validate_domain(domain, allow_unicode=True):
    """
    Complete domeincontrole.
    """

    if not domain:
        return False, "DOMAIN_EMPTY", "Domein is leeg.", None

    # Maximale lengte vóór IDNA.
    if len(domain.encode("utf-8")) > MAX_DOMAIN_LENGTH:
        return False, "DOMAIN_TOO_LONG", (
            "Het domein is langer dan 255 bytes."
        ), None

    # Domein-literal.
    if domain.startswith("[") or domain.endswith("]"):

        result = _validate_domain_literal(domain)

        if result[0]:
            return True, None, None, domain

        return result[0], result[1], result[2], None

    # Domein mag geen whitespace bevatten.
    if _heeft_whitespace(domain):
        return False, "DOMAIN_WHITESPACE", (
            "Het domein bevat whitespace."
        ), None

    # Unicode-domain verwerken.
    if any(ord(c) > 127 for c in domain):

        if not allow_unicode:
            return False, "UNICODE_NOT_ALLOWED", (
                "Unicode in het domein is niet toegestaan."
            ), None

        ascii_domain = _convert_domain_to_idna(domain)

        if ascii_domain is None:
            return False, "IDNA_INVALID", (
                "Het domein kan niet worden geconverteerd naar IDNA."
            ), None

    else:
        ascii_domain = domain

    # ASCII-domein opnieuw controleren.
    if len(ascii_domain.encode("ascii")) > MAX_DOMAIN_LENGTH:
        return False, "DOMAIN_IDNA_TOO_LONG", (
            "Het IDNA-domein is langer dan 255 bytes."
        ), None

    # lowercase voor consistente DNS-verwerking.
    ascii_domain = ascii_domain.lower()

    # Begin/einde met punt voorkomen.
    if ascii_domain.startswith("."):
        return False, "DOMAIN_START_DOT", (
            "Domein mag niet met een punt beginnen."
        ), None

    if ascii_domain.endswith("."):
        return False, "DOMAIN_END_DOT", (
            "Domein mag niet met een punt eindigen."
        ), None

    # Dubbele punten/dots.
    if ".." in ascii_domain:
        return False, "DOMAIN_DOUBLE_DOT", (
            "Domein bevat twee punten achter elkaar."
        ), None

    valid, code, message = _validate_domain_labels(ascii_domain)

    if not valid:
        return False, code, message, None

    return True, None, None, ascii_domain


# ============================================================
# DNS
# ============================================================

def _check_dns_records(domain):
    """
    Controleert of het domein daadwerkelijk DNS-informatie heeft.

    Eerst proberen we MX-records via dnspython.
    Als dat niet beschikbaar is, gebruiken we socket.getaddrinfo()
    als beperkte fallback.
    """

    # IP-literals hoeven geen DNS.
    if domain.startswith("[") and domain.endswith("]"):
        return True, "DOMAIN_LITERAL"

    # --------------------------------------------------------
    # MX via dnspython
    # --------------------------------------------------------

    try:
        import dns.resolver

        try:
            antwoorden = dns.resolver.resolve(domain, "MX")

            if antwoorden:
                return True, "MX"

        except Exception:
            pass

    except ImportError:
        pass

    # --------------------------------------------------------
    # A / AAAA fallback
    # --------------------------------------------------------

    try:

        resultaten = socket.getaddrinfo(
            domain,
            None,
            type=socket.SOCK_STREAM
        )

        if resultaten:
            return True, "A_OR_AAAA"

    except socket.gaierror:
        pass

    return False, "NO_DNS"


# ============================================================
# HOOFDFUNCTIE
# ============================================================

def valideer_email(
    email,
    check_dns=False,
    allow_unicode=True,
    allow_quoted=True
):
    """
    Zeer uitgebreide e-mailvalidatie.

    Parameters
    ----------
    email : str
        Het te controleren e-mailadres.

    check_dns : bool
        Controleert of het domein DNS-informatie heeft.

    allow_unicode : bool
        Laat Unicode-domeinen toe.

    allow_quoted : bool
        Laat quoted local-parts toe.

    Returns
    -------
    EmailValidationResult
        Object met geldig/ongeldig en foutinformatie.
    """

    # ========================================================
    # 1. TYPE
    # ========================================================

    if not _is_string(email):
        return EmailValidationResult(
            False,
            "INVALID_TYPE",
            "E-mailadres moet een string zijn."
        )

    # ========================================================
    # 2. NORMALISATIE
    # ========================================================

    email = _normaliseer_email(email)

    # Spaties aan begin/einde verwijderen.
    email = email.strip()

    if not email:
        return EmailValidationResult(
            False,
            "EMPTY",
            "E-mailadres is leeg."
        )

    # ========================================================
    # 3. ALGEMENE TEKENS
    # ========================================================

    if _heeft_control_characters(email):
        return EmailValidationResult(
            False,
            "CONTROL_CHARACTER",
            "E-mailadres bevat control characters."
        )

    if _heeft_whitespace(email):
        return EmailValidationResult(
            False,
            "WHITESPACE",
            "E-mailadres bevat whitespace."
        )

    # ========================================================
    # 4. TOTALE LENGTE
    # ========================================================

    if len(email.encode("utf-8")) > MAX_EMAIL_LENGTH:
        return EmailValidationResult(
            False,
            "EMAIL_TOO_LONG",
            "E-mailadres is langer dan 254 bytes."
        )

    # ========================================================
    # 5. @
    # ========================================================

    if email.count("@") != 1:
        return EmailValidationResult(
            False,
            "AT_COUNT",
            "E-mailadres moet precies één @ bevatten."
        )

    local_part, domain = email.rsplit("@", 1)

    # ========================================================
    # 6. LOCAL-PART LENGTE
    # ========================================================

    if len(local_part.encode("utf-8")) > MAX_LOCAL_LENGTH:
        return EmailValidationResult(
            False,
            "LOCAL_TOO_LONG",
            "Local-part is langer dan 64 bytes."
        )

    # ========================================================
    # 7. LOCAL-PART
    # ========================================================

    local_valid, local_code, local_message = _validate_local(
        local_part,
        allow_quoted=allow_quoted
    )

    if not local_valid:
        return EmailValidationResult(
            False,
            local_code,
            local_message,
            email,
            local_part,
            domain
        )

    # ========================================================
    # 8. DOMAIN
    # ========================================================

    (
        domain_valid,
        domain_code,
        domain_message,
        normalized_domain
    ) = _validate_domain(
        domain,
        allow_unicode=allow_unicode
    )

    if not domain_valid:
        return EmailValidationResult(
            False,
            domain_code,
            domain_message,
            email,
            local_part,
            domain
        )

    # ========================================================
    # 9. NIEUW GENORMALISEERD ADRES
    # ========================================================

    normalized_email = f"{local_part}@{normalized_domain}"

    # ========================================================
    # 10. DNS
    # ========================================================

    if check_dns:

        dns_valid, dns_type = _check_dns_records(
            normalized_domain
        )

        if not dns_valid:
            return EmailValidationResult(
                False,
                "DNS_NOT_FOUND",
                (
                    "Het domein heeft geen bruikbare DNS-"
                    "informatie voor deze controle."
                ),
                normalized_email,
                local_part,
                normalized_domain
            )

    # ========================================================
    # 11. EINDE
    # ========================================================

    return EmailValidationResult(
        True,
        None,
        None,
        normalized_email,
        local_part,
        normalized_domain
    )


# ============================================================
# EENVOUDIGE BOOLEAN-FUNCTIE
# ============================================================

def email_is_geldig(email):
    """
    Alleen True/False nodig?
    Dan gebruik je deze functie.
    """

    resultaat = valideer_email(
        email,
        check_dns=False
    )

    return resultaat.geldig


# ============================================================
# TESTS
# ============================================================

test_emails = [

    # Geldig
    "test@gmail.com",
    "matt@fontys.nl",
    "voornaam.achternaam@gmail.com",
    "test123@gmail.com",
    "test+project@gmail.com",
    "test-name@gmail.com",
    "test_name@gmail.com",

    # Ongeldig
    "",
    "test",
    "test@gmail",
    "@gmail.com",
    "test@",
    "@",
    "test@@gmail.com",
    "test@gmail..com",
    ".test@gmail.com",
    "test.@gmail.com",
    "test..test@gmail.com",
    "test @gmail.com",
    "test@ gmail.com",
    "test@gm ail.com",
    "test!gmail.com",
    "test@gmail",
    "test@.com",
    "test@com.",
    "test@-gmail.com",
    "test@gmail-.com",

    # Quoted local parts
    '"john doe"@example.com',
    '"john\\\\doe"@example.com',

    # IP domein
    "test@[192.168.1.1]",
    "test@[IPv6:2001:db8::1]",

    # Unicode domein
    "test@münchen.de",
]


# ============================================================
# TEST UITVOEREN
# ============================================================

for email in test_emails:

    resultaat = valideer_email(
        email,
        check_dns=False
    )

    if resultaat.geldig:

        print(
            f"[GELDIG]   {email}"
        )

        print(
            f"           -> {resultaat.genormaliseerd}"
        )

    else:

        print(
            f"[ONGELDIG] {email}"
        )

        print(
            f"           -> {resultaat.foutcode}: "
            f"{resultaat.melding}"
        )

resultaat = valideer_email("test@gmail.com")
print(resultaat)

from rich import print
from rich.console import Console
import re
import socket
import ipaddress
import unicodedata


# ============================================================
# KLEUREN
# ============================================================

RESET = "\033[0m"
ROOD = "\033[91m"
GROEN = "\033[92m"
GEEL = "\033[93m"
BLAUW = "\033[94m"
CYAN = "\033[96m"
PAARS = "\033[95m"
VET = "\033[1m"


# ============================================================
# CONFIGURATIE
# ============================================================

MAX_EMAIL_LENGTH = 254
MAX_LOCAL_LENGTH = 64
MAX_DOMAIN_LENGTH = 255
MAX_DOMAIN_LABEL_LENGTH = 63

ATEXT_CHARS = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789"
    "!#$%&'*+-/=?^_`{|}~."
)

CONTROL_CHAR_PATTERN = re.compile(
    r"[\x00-\x1F\x7F]"
)

DOMAIN_LABEL_PATTERN = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?$"
)

TLD_PATTERN = re.compile(
    r"^[A-Za-z]{2,63}$"
)


# ============================================================
# HULPFUNCTIES
# ============================================================

def lijn(lengte=65):
    print(CYAN + "═" * lengte + RESET)


def titel(tekst):
    print()
    lijn()
    print(VET + CYAN + f"{tekst:^65}" + RESET)
    lijn()


def fout(tekst):
    print(ROOD + "✗ " + tekst + RESET)


def goed(tekst):
    print(GROEN + "✓ " + tekst + RESET)


def waarschuwing(tekst):
    print(GEEL + "⚠ " + tekst + RESET)


def info(tekst):
    print(BLAUW + "ℹ " + tekst + RESET)


# ============================================================
# CONTROL CHARACTERS
# ============================================================

def heeft_control_characters(tekst):

    return CONTROL_CHAR_PATTERN.search(tekst) is not None


# ============================================================
# WHITESPACE
# ============================================================

def heeft_whitespace(tekst):

    return any(
        char.isspace()
        for char in tekst
    )


# ============================================================
# UNICODE NORMALISATIE
# ============================================================

def normaliseer_email(email):

    return unicodedata.normalize(
        "NFC",
        email
    )


# ============================================================
# LOCAL PART
# ============================================================

def valideer_local_part(local):

    if not local:

        return False, "Local-part is leeg."

    if len(local.encode("utf-8")) > MAX_LOCAL_LENGTH:

        return False, (
            "Local-part is langer dan 64 bytes."
        )

    if local.startswith("."):

        return False, (
            "Local-part mag niet met een punt beginnen."
        )

    if local.endswith("."):

        return False, (
            "Local-part mag niet met een punt eindigen."
        )

    if ".." in local:

        return False, (
            "Local-part bevat twee punten achter elkaar."
        )

    for char in local:

        if ord(char) > 127 and char.isalnum():
            continue

        if char not in ATEXT_CHARS:

            return False, (
                f"Ongeldig teken gevonden: {char!r}"
            )

    return True, None


# ============================================================
# DOMAIN
# ============================================================

def valideer_domain(domain):

    if not domain:

        return False, "Domein is leeg."

    if len(domain.encode("utf-8")) > MAX_DOMAIN_LENGTH:

        return False, (
            "Domein is langer dan 255 bytes."
        )

    if domain.startswith("."):

        return False, (
            "Domein mag niet met een punt beginnen."
        )

    if domain.endswith("."):

        return False, (
            "Domein mag niet met een punt eindigen."
        )

    if ".." in domain:

        return False, (
            "Domein bevat twee punten achter elkaar."
        )

    if "-" == domain[0]:

        return False, (
            "Domein mag niet met '-' beginnen."
        )

    if _is_ip_address(domain):

        return True, None

    # Unicode domein omzetten naar IDNA
    try:
        ascii_domain = (
            domain.encode("idna")
            .decode("ascii")
        )

    except UnicodeError:

        return False, (
            "Domein kan niet naar IDNA worden omgezet."
        )

    labels = ascii_domain.split(".")

    if len(labels) < 2:

        return False, (
            "Domein moet minimaal één punt bevatten."
        )

    for label in labels:

        if not label:

            return False, (
                "Domein bevat een leeg gedeelte."
            )

        if len(label) > MAX_DOMAIN_LABEL_LENGTH:

            return False, (
                f"Domeinlabel '{label}' is te lang."
            )

        if label.startswith("-"):

            return False, (
                f"Domeinlabel '{label}' begint met '-'."
            )

        if label.endswith("-"):

            return False, (
                f"Domeinlabel '{label}' eindigt met '-'."
            )

        if not DOMAIN_LABEL_PATTERN.fullmatch(label):

            return False, (
                f"Ongeldige tekens in domeinlabel '{label}'."
            )

    tld = labels[-1]

    if not TLD_PATTERN.fullmatch(tld):

        return False, (
            "TLD moet minimaal 2 letters bevatten."
        )

    return True, None


# ============================================================
# IP ADRES
# ============================================================

def _is_ip_address(domain):

    # IPv4
    try:

        ipaddress.IPv4Address(domain)

        return True

    except ValueError:
        pass

    # IPv6
    try:

        ipaddress.IPv6Address(domain)

        return True

    except ValueError:
        pass

    return False


# ============================================================
# DNS
# ============================================================

def controleer_dns(domain):

    try:

        resultaten = socket.getaddrinfo(
            domain,
            None
        )

        if resultaten:

            return True

    except socket.gaierror:
        pass

    return False


# ============================================================
# HOOFDFUNCTIE
# ============================================================

def valideer_email(email, controleer_dns=False):

    titel("EMAIL VALIDATION ENGINE")

    print(
        f"{PAARS}Invoer:{RESET} {email}"
    )

    print()

    # --------------------------------------------------------
    # TYPE
    # --------------------------------------------------------

    if not isinstance(email, str):

        fout(
            "Invoer is geen string."
        )

        return False

    goed("Datatype: string")

    # --------------------------------------------------------
    # NORMALISEREN
    # --------------------------------------------------------

    email = normaliseer_email(
        email.strip()
    )

    goed("Unicode genormaliseerd")

    # --------------------------------------------------------
    # LEEG
    # --------------------------------------------------------

    if not email:

        fout(
            "E-mailadres is leeg."
        )

        return False

    goed("E-mailadres is niet leeg")

    # --------------------------------------------------------
    # CONTROL CHARACTERS
    # --------------------------------------------------------

    if heeft_control_characters(email):

        fout(
            "E-mailadres bevat control characters."
        )

        return False

    goed("Geen control characters")

    # --------------------------------------------------------
    # WHITESPACE
    # --------------------------------------------------------

    if heeft_whitespace(email):

        fout(
            "E-mailadres bevat whitespace."
        )

        return False

    goed("Geen whitespace")

    # --------------------------------------------------------
    # LENGTE
    # --------------------------------------------------------

    if len(email.encode("utf-8")) > MAX_EMAIL_LENGTH:

        fout(
            "E-mailadres is langer dan 254 bytes."
        )

        return False

    goed(
        f"Totale lengte: "
        f"{len(email.encode('utf-8'))} bytes"
    )

    # --------------------------------------------------------
    # @
    # --------------------------------------------------------

    if email.count("@") != 1:

        fout(
            "E-mailadres moet precies één @ bevatten."
        )

        return False

    goed("Precies één @ gevonden")

    # --------------------------------------------------------
    # OPSPLITSEN
    # --------------------------------------------------------

    local_part, domain = email.split("@")

    print()
    info(
        f"Local-part : {local_part}"
    )

    info(
        f"Domein     : {domain}"
    )

    # --------------------------------------------------------
    # LOCAL
    # --------------------------------------------------------

    geldig, melding = valideer_local_part(
        local_part
    )

    if not geldig:

        fout(melding)

        return False

    goed("Local-part is geldig")

    # --------------------------------------------------------
    # DOMAIN
    # --------------------------------------------------------

    geldig, melding = valideer_domain(
        domain
    )

    if not geldig:

        fout(melding)

        return False

    goed("Domeinstructuur is geldig")

    # --------------------------------------------------------
    # DNS
    # --------------------------------------------------------

    if controleer_dns:

        print()

        info(
            "DNS-controle wordt uitgevoerd..."
        )

        if controleer_dns(domain):

            goed(
                "Domein is via DNS bereikbaar"
            )

        else:

            waarschuwing(
                "Geen DNS-record gevonden"
            )

    # --------------------------------------------------------
    # EINDE
    # --------------------------------------------------------

    print()

    lijn()

    print(
        VET + GROEN +
        "                 ✓ EMAIL IS GELDIG"
        + RESET
    )

    lijn()

    return True


# ============================================================
# PROGRAMMA
# ============================================================

while True:

    print()

    email = input(
        CYAN +
        "✉ Geef een e-mailadres "
        "(of 'stop'): " +
        RESET
    )

    if email.lower() == "stop":

        print()
        print(
            GEEL +
            "Validator afgesloten." +
            RESET
        )

        break

    valideer_email(
        email,
        controleer_dns=True
    )