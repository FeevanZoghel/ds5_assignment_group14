import streamlit as st
import re
from pathlib import Path


# ============================================================
# PAGINA-INSTELLINGEN
# ============================================================

st.set_page_config(
    page_title="VeiligInloggen",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# BESTANDEN
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
ELMO_IMAGE = BASE_DIR / "elmo.png"


# ============================================================
# OPMAAK
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 15% 15%,
            rgba(255,255,255,0.30) 0%,
            transparent 32%
        ),
        radial-gradient(
            circle at 85% 10%,
            rgba(255,255,255,0.20) 0%,
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #b8d8ff 0%,
            #91c2fa 50%,
            #6fa9ed 100%
        );

    min-height: 100vh;
}


.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}


header[data-testid="stHeader"] {
    background: transparent;
}


/* LOGO */

.brand {
    font-size: 22px;
    font-weight: 700;
    color: #102a56;
    margin-bottom: 25px;
}

.brand-light {
    font-weight: 400;
}


/* ACCOUNT AANMAKEN */

.hero-title {
    font-family: Georgia, serif;
    font-size: 54px;
    line-height: 1.02;
    color: #102a56;
    margin-top: 100px;
    margin-bottom: 25px;
}

.hero-line {
    width: 45px;
    height: 3px;
    background: #2563eb;
    border-radius: 10px;
    margin-bottom: 28px;
}

.hero-text {
    color: #405d83;
    font-size: 17px;
    line-height: 1.6;
    max-width: 270px;
}


/* TITELS */

.lock-icon {
    width: 65px;
    height: 65px;
    margin: 5px auto 15px auto;
    border-radius: 50%;
    background: rgba(255,255,255,0.55);

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 29px;
}

.main-title {
    text-align: center;
    color: #10234b;
    font-size: 31px;
    font-weight: 750;
    margin-bottom: 5px;
}

.main-subtitle {
    text-align: center;
    color: #536d92;
    font-size: 15px;
    margin-bottom: 25px;
}


/* INVOERVELDEN */

.stTextInput label {
    color: #172b4d !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

div[data-baseweb="input"] {
    background-color: #24252d !important;
    border: 1px solid #30333e !important;
    border-radius: 10px !important;
    min-height: 47px;
}

div[data-baseweb="input"] input {
    color: white !important;
}

div[data-baseweb="input"] input::placeholder {
    color: #b8bdca !important;
}


/* WACHTWOORDVEREISTEN */

.requirements {
    background: rgba(255,255,255,0.70);
    border: 1px solid rgba(255,255,255,0.60);
    border-radius: 14px;

    padding: 16px 20px;

    margin-top: 10px;
    margin-bottom: 15px;
}

.requirements-title {
    color: #14294f;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 10px;
}

.req {
    font-size: 13px;
    margin: 5px 0;
    color: #657999;
}

.req-ok {
    color: #17603b;
    font-weight: 600;
}


/* KNOPPEN */

.stButton > button {

    width: 100%;
    min-height: 47px;

    border: none !important;
    border-radius: 10px !important;

    background:
        linear-gradient(
            90deg,
            #2463d4,
            #3478ea
        ) !important;

    color: white !important;

    font-weight: 650 !important;
    font-size: 15px !important;

    box-shadow:
        0 8px 18px
        rgba(36,99,212,0.20);

    transition: all 0.15s ease;
}

.stButton > button:hover {

    transform: translateY(-1px);

    box-shadow:
        0 10px 24px
        rgba(36,99,212,0.30);
}


/* MELDINGEN */

div[data-testid="stAlert"] p {
    font-weight: 650 !important;
}


/* RECHTERKANT ACCOUNT */

.right-title {
    color: #102a56;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 2px;
}

.right-text {
    color: #405d83;
    font-size: 14px;
    line-height: 1.4;
}

.feature {
    margin-top: 70px;
    margin-bottom: 45px;
}


/* FOOTER */

.footer-text {
    text-align: center;
    color: #657b9c;
    font-size: 12px;
    margin-top: 30px;
    letter-spacing: 0.5px;
}


/* VOORTGANGSBALK */

.stProgress > div > div > div > div {
    background-color: #2563eb;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCTIES
# ============================================================

def validate_email(email):

    email = email.strip()

    if email == "":
        return False, "Vul een e-mailadres in."

    if len(email) > 254:
        return False, "Het e-mailadres is te lang."

    if " " in email:
        return False, "Een e-mailadres mag geen spaties bevatten."

    if email.count("@") != 1:
        return False, "Een e-mailadres moet precies één @ bevatten."

    username, domain = email.split("@")

    if username == "":
        return False, "De gebruikersnaam mag niet leeg zijn."

    if domain == "":
        return False, "Het domein mag niet leeg zijn."

    if len(username) > 64:
        return False, "De gebruikersnaam is te lang."

    if username.startswith(".") or username.endswith("."):
        return False, "De gebruikersnaam mag niet met een punt beginnen of eindigen."

    if domain.startswith(".") or domain.endswith("."):
        return False, "Het domein mag niet met een punt beginnen of eindigen."

    if ".." in email:
        return False, "Het e-mailadres mag geen twee punten achter elkaar bevatten."

    if "." not in domain:
        return False, "Het domein moet een punt bevatten."

    domain_name, extension = domain.rsplit(".", 1)

    if domain_name == "":
        return False, "De domeinnaam mag niet leeg zijn."

    if len(extension) < 2:
        return False, "De domeinextensie moet minimaal 2 tekens bevatten."

    username_pattern = r"^[A-Za-z0-9._%+-]+$"

    if not re.match(username_pattern, username):
        return False, "De gebruikersnaam bevat ongeldige tekens."

    domain_pattern = r"^[A-Za-z0-9.-]+$"

    if not re.match(domain_pattern, domain):
        return False, "Het domein bevat ongeldige tekens."

    return True, "Geldig e-mailadres."


def password_checks(password):

    special_characters = "!@#$%^&*()_+-=[]{};:,.?"

    return {
        "Minimaal 8 tekens":
            len(password) >= 8,

        "Minimaal één hoofdletter (A-Z)":
            any(c.isupper() for c in password),

        "Minimaal één kleine letter (a-z)":
            any(c.islower() for c in password),

        "Minimaal één cijfer (0-9)":
            any(c.isdigit() for c in password),

        "Minimaal één speciaal teken":
            any(c in special_characters for c in password),

        "Geen spaties":
            " " not in password
    }


def validate_password(password):

    if password == "":
        return False, "Vul een wachtwoord in."

    checks = password_checks(password)

    for requirement, passed in checks.items():

        if not passed:
            return False, "Ontbrekende vereiste: " + requirement

    return True, "Geldig wachtwoord."


def password_strength(password):

    if password == "":
        return 0

    checks = password_checks(password)

    return sum(checks.values()) / len(checks)


# ============================================================
# SESSION STATE
# ============================================================

if "account_created" not in st.session_state:
    st.session_state.account_created = False

if "saved_email" not in st.session_state:
    st.session_state.saved_email = ""

if "saved_password" not in st.session_state:
    st.session_state.saved_password = ""

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

if "cart" not in st.session_state:
    st.session_state.cart = []

if "shop_page" not in st.session_state:
    st.session_state.shop_page = "Home"

if "order_total" not in st.session_state:
    st.session_state.order_total = 0

if "order_items" not in st.session_state:
    st.session_state.order_items = []


# ============================================================
# LOGO
# ============================================================

st.markdown(
    '<div class="brand">'
    '🔒 Veilig'
    '<span class="brand-light">Inloggen</span>'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# ACCOUNT AANMAKEN
# ============================================================

if not st.session_state.account_created:

    left, center, right = st.columns(
        [1, 1.55, 1],
        gap="large"
    )


    # LINKERKANT
    with left:

        st.markdown(
            '<div class="hero-title">'
            'Een veiligere<br>'
            'digitale<br>'
            'toekomst'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="hero-line"></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="hero-text">'
            'Maak een account aan en zet de eerste stap '
            'naar een veilige digitale ervaring.'
            '</div>',
            unsafe_allow_html=True
        )


    # MIDDEN
    with center:

        st.markdown(
            '<div class="lock-icon">🔐</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="main-title">'
            'Maak je account aan'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="main-subtitle">'
            'Maak een veilig account aan om verder te gaan'
            '</div>',
            unsafe_allow_html=True
        )


        email = st.text_input(
            "E-mailadres",
            placeholder="naam@voorbeeld.nl",
            key="register_email"
        )


        password = st.text_input(
            "Wachtwoord",
            type="password",
            placeholder="Maak een sterk wachtwoord",
            key="register_password"
        )


        repeat_password = st.text_input(
            "Bevestig wachtwoord",
            type="password",
            placeholder="Vul je wachtwoord opnieuw in",
            key="repeat_password"
        )


        # ====================================================
        # WACHTWOORDVEREISTEN
        # ====================================================

        checks = password_checks(password)

        requirement_html = ""

        for name, passed in checks.items():

            if passed:

                requirement_html += (
                    '<div class="req req-ok">'
                    '✓ ' + name +
                    '</div>'
                )

            else:

                requirement_html += (
                    '<div class="req">'
                    '○ ' + name +
                    '</div>'
                )


        st.markdown(
            '<div class="requirements">'
            '<div class="requirements-title">'
            'Wachtwoordvereisten'
            '</div>'
            + requirement_html +
            '</div>',
            unsafe_allow_html=True
        )


        # ====================================================
        # WACHTWOORDSTERKTE
        # ====================================================

        if password:

            strength = password_strength(password)

            if strength <= 0.35:
                strength_text = "Zwak"

            elif strength <= 0.65:
                strength_text = "Gemiddeld"

            elif strength < 1:
                strength_text = "Goed"

            else:
                strength_text = "Sterk"

            st.caption(
                "Wachtwoordsterkte: " + strength_text
            )

            st.progress(strength)


        # ====================================================
        # ACCOUNT AANMAKEN
        # ====================================================

        if st.button(
            "Account aanmaken →",
            type="primary",
            use_container_width=True
        ):

            email_valid, email_message = validate_email(email)

            password_valid, password_message = validate_password(
                password
            )

            if not email_valid:

                st.error(email_message)

            elif not password_valid:

                st.error(password_message)

            elif password != repeat_password:

                st.error(
                    "De wachtwoorden komen niet overeen."
                )

            else:

                st.session_state.saved_email = email.strip()
                st.session_state.saved_password = password
                st.session_state.account_created = True

                st.rerun()


    # RECHTERKANT
    with right:

        st.markdown(
            '<div class="feature">'
            '<div class="right-title">'
            '🛡️ &nbsp; Veilig'
            '</div>'
            '<div class="right-text">'
            'Je gegevens worden beschermd.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="feature">'
            '<div class="right-title">'
            '👤 &nbsp; Privé'
            '</div>'
            '<div class="right-text">'
            'We delen je gegevens niet.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="feature">'
            '<div class="right-title">'
            '⚡ &nbsp; Eenvoudig'
            '</div>'
            '<div class="right-text">'
            'Snel en gemakkelijk te gebruiken.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


# ============================================================
# INLOGPAGINA
# ============================================================

elif not st.session_state.logged_in:

    left_space, login, right_space = st.columns(
        [1, 1.2, 1]
    )

    with login:

        if st.button(
            "← Terug naar account aanmaken",
            use_container_width=True
        ):

            st.session_state.account_created = False
            st.session_state.saved_email = ""
            st.session_state.saved_password = ""

            st.rerun()


        st.markdown(
            '<div class="lock-icon">🔐</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="main-title">'
            'Welkom terug'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="main-subtitle">'
            'Log in op je account'
            '</div>',
            unsafe_allow_html=True
        )

        st.success(
            "✓ Account succesvol aangemaakt!"
        )


        login_email = st.text_input(
            "E-mailadres",
            placeholder="naam@voorbeeld.nl",
            key="login_email"
        )


        login_password = st.text_input(
            "Wachtwoord",
            type="password",
            placeholder="Vul je wachtwoord in",
            key="login_password"
        )


        if st.button(
            "Inloggen →",
            type="primary",
            use_container_width=True
        ):

            if (
                login_email.strip()
                == st.session_state.saved_email
                and
                login_password
                == st.session_state.saved_password
            ):

                st.session_state.logged_in = True
                st.session_state.show_balloons = True
                st.session_state.shop_page = "Home"

                st.rerun()

            else:

                st.error(
                    "Onjuist e-mailadres of wachtwoord."
                )


# ============================================================
# ELMO'S IJSSALON
# ============================================================

else:

    if st.session_state.show_balloons:

        st.balloons()
        st.session_state.show_balloons = False


    # ========================================================
    # PRODUCTEN
    # ========================================================

    products = {

        "Aardbei": {
            "emoji": "🍓",
            "description": "Romig aardbeienijs",
            "price": 2.95
        },

        "Chocolade": {
            "emoji": "🍫",
            "description": "Vol en romig chocolade-ijs",
            "price": 3.25
        },

        "Cookie Crunch": {
            "emoji": "🍪",
            "description": "Vanille-ijs met stukjes koek",
            "price": 3.50
        },

        "Regenboog": {
            "emoji": "🌈",
            "description": "Elmo's kleurrijke specialiteit",
            "price": 3.75
        },

        "Vanilledroom": {
            "emoji": "🍦",
            "description": "Klassiek romig vanille-ijs",
            "price": 2.75
        },

        "Kersen Sundae": {
            "emoji": "🍒",
            "description": "IJssundae met kersen",
            "price": 4.25
        }
    }


    # ========================================================
    # ZIJBALK
    # ========================================================

    with st.sidebar:

        if ELMO_IMAGE.exists():

            st.image(
                str(ELMO_IMAGE),
                width=120
            )


        st.markdown("## 🍦 Elmo's")
        st.caption("IJssalon")

        st.divider()

        st.markdown("### Hoofdmenu")


        if st.button(
            "🏠 Startpagina",
            use_container_width=True
        ):

            st.session_state.shop_page = "Home"
            st.rerun()


        if st.button(
            "🍦 Menu + prijzen",
            use_container_width=True
        ):

            st.session_state.shop_page = "Menu"
            st.rerun()


        if st.button(
            f"🛒 Winkelwagen ({len(st.session_state.cart)})",
            use_container_width=True
        ):

            st.session_state.shop_page = "Cart"
            st.rerun()


        st.divider()

        st.caption("Ingelogd als:")

        st.write(
            st.session_state.saved_email
        )


        if st.button(
            "🚪 Uitloggen",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.shop_page = "Home"

            st.rerun()


    # ========================================================
    # BOVENKANT WINKEL
    # ========================================================

    header1, header2 = st.columns(
        [5, 1]
    )


    with header1:

        st.markdown(
            "# 🍦 Elmo's IJssalon"
        )

        st.write(
            "Het lekkerste ijs van de stad!"
        )


    with header2:

        st.metric(
            "🛒 Winkelwagen",
            len(st.session_state.cart)
        )


    st.divider()


    # ========================================================
    # STARTPAGINA
    # ========================================================

    if st.session_state.shop_page == "Home":

        if st.button(
            "← Terug naar inloggen",
            key="home_back"
        ):

            st.session_state.logged_in = False
            st.rerun()


        st.success(
            "👋 Welkom bij Elmo's IJssalon!"
        )

        st.caption(
            "Je bent ingelogd als "
            + st.session_state.saved_email
        )


        st.write("")


        elmo_col, text_col = st.columns(
            [1, 2],
            gap="large"
        )


        with elmo_col:

            if ELMO_IMAGE.exists():

                st.image(
                    str(ELMO_IMAGE),
                    width=300
                )

            else:

                st.warning(
                    "De afbeelding van Elmo kon niet worden gevonden."
                )

                st.caption(
                    "Zorg ervoor dat elmo.png in dezelfde map "
                    "staat als dit Python-bestand."
                )


        with text_col:

            st.markdown(
                "## ❤️ Welkom!"
            )

            st.write(
                "Welkom bij **Elmo's IJssalon!**"
            )

            st.write(
                "Hier vind je onze heerlijke collectie "
                "van verschillende soorten ijs."
            )

            st.write(
                "Ga naar **Menu + prijzen** om alle smaken "
                "te bekijken en je favoriete ijsjes aan je "
                "winkelwagen toe te voegen."
            )

            st.write(
                "Ben je klaar? Open dan je **Winkelwagen** "
                "om je bestelling en het totaalbedrag te bekijken."
            )

            st.info(
                "🍓 Elmo's favoriet is het aardbeienijs!"
            )


        st.write("")
        st.divider()


        center1, center2, center3 = st.columns(
            [1, 2, 1]
        )


        with center2:

            st.markdown(
                "<p style='text-align:center; font-size:60px;'>"
                "🍓 🍦 🍫"
                "</p>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<h2 style='text-align:center;'>"
                "Specialiteit van vandaag"
                "</h2>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<p style='text-align:center; font-size:18px;'>"
                "Aardbeienspecial — slechts €2,95"
                "</p>",
                unsafe_allow_html=True
            )


        st.write("")


        if st.button(
            "Bekijk het menu →",
            type="primary",
            use_container_width=True
        ):

            st.session_state.shop_page = "Menu"
            st.rerun()


    # ========================================================
    # MENU + PRIJZEN
    # ========================================================

    elif st.session_state.shop_page == "Menu":

        if st.button(
            "← Terug naar startpagina",
            key="menu_back"
        ):

            st.session_state.shop_page = "Home"
            st.rerun()


        st.markdown(
            "# 🍦 Menu + prijzen"
        )

        st.write(
            "Kies je favoriete ijs en voeg het toe "
            "aan je winkelwagen."
        )

        st.write("")


        # ====================================================
        # FUNCTIE VOOR PRODUCTEN
        # ====================================================

        def show_product(name, button_key):

            product = products[name]


            st.markdown(
                f"<div style='"
                f"text-align:center;"
                f"font-size:75px;"
                f"'>"
                f"{product['emoji']}"
                f"</div>",
                unsafe_allow_html=True
            )


            st.markdown(
                f"<h3 style='text-align:center;'>"
                f"{name}"
                f"</h3>",
                unsafe_allow_html=True
            )


            st.markdown(
                f"<p style='text-align:center;'>"
                f"{product['description']}"
                f"</p>",
                unsafe_allow_html=True
            )


            st.markdown(
                f"<h2 style='text-align:center;'>"
                f"€{product['price']:.2f}"
                f"</h2>",
                unsafe_allow_html=True
            )


            # GEEN EXTRA ST.RERUN HIER
            # Hierdoor kun je sneller meerdere ijsjes toevoegen.

            if st.button(
                "Toevoegen 🛒",
                key=button_key,
                use_container_width=True
            ):

                st.session_state.cart.append(name)

                st.session_state.shop_page = "Menu"

                st.toast(
                    product["emoji"]
                    + " "
                    + name
                    + " toegevoegd aan je winkelwagen!"
                )


        # ====================================================
        # EERSTE RIJ
        # ====================================================

        col1, col2, col3 = st.columns(
            3,
            gap="medium"
        )


        with col1:

            show_product(
                "Aardbei",
                "add_strawberry"
            )


        with col2:

            show_product(
                "Chocolade",
                "add_chocolate"
            )


        with col3:

            show_product(
                "Cookie Crunch",
                "add_cookie"
            )


        st.write("")
        st.write("")


        # ====================================================
        # TWEEDE RIJ
        # ====================================================

        col4, col5, col6 = st.columns(
            3,
            gap="medium"
        )


        with col4:

            show_product(
                "Regenboog",
                "add_rainbow"
            )


        with col5:

            show_product(
                "Vanilledroom",
                "add_vanilla"
            )


        with col6:

            show_product(
                "Kersen Sundae",
                "add_cherry"
            )


        st.write("")
        st.divider()


        # ====================================================
        # SNEL OVERZICHT WINKELWAGEN
        # ====================================================

        if len(st.session_state.cart) == 0:

            st.info(
                "🛒 Je winkelwagen is nog leeg."
            )

        else:

            st.success(
                f"🛒 Je hebt nu "
                f"{len(st.session_state.cart)} "
                f"ijsje(s) in je winkelwagen."
            )


        # ====================================================
        # NAAR WINKELWAGEN
        # ====================================================

        if st.button(
            f"Bekijk winkelwagen "
            f"({len(st.session_state.cart)}) →",
            type="primary",
            use_container_width=True
        ):

            st.session_state.shop_page = "Cart"
            st.rerun()


    # ========================================================
    # WINKELWAGEN
    # ========================================================

    elif st.session_state.shop_page == "Cart":

        if st.button(
            "← Terug naar menu + prijzen",
            key="cart_back"
        ):

            st.session_state.shop_page = "Menu"
            st.rerun()


        st.markdown(
            "# 🛒 Winkelwagen"
        )

        st.write("")


        # ====================================================
        # LEGE WINKELWAGEN
        # ====================================================

        if len(st.session_state.cart) == 0:

            empty_left, empty_center, empty_right = st.columns(
                [1, 2, 1]
            )


            with empty_center:

                st.markdown(
                    "<p style='"
                    "text-align:center;"
                    "font-size:80px;"
                    "'>"
                    "🛒"
                    "</p>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    "<h2 style='text-align:center;'>"
                    "Je winkelwagen is leeg"
                    "</h2>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    "<p style='"
                    "text-align:center;"
                    "font-size:17px;"
                    "'>"
                    "Ga naar Menu + prijzen om lekker ijs "
                    "aan je winkelwagen toe te voegen!"
                    "</p>",
                    unsafe_allow_html=True
                )


            st.write("")


            if st.button(
                "🍦 Naar het menu",
                type="primary",
                use_container_width=True
            ):

                st.session_state.shop_page = "Menu"
                st.rerun()


        # ====================================================
        # WINKELWAGEN MET PRODUCTEN
        # ====================================================

        else:

            cart_counts = {}


            for item in st.session_state.cart:

                if item in cart_counts:

                    cart_counts[item] += 1

                else:

                    cart_counts[item] = 1


            total_price = 0


            for product_name, quantity in cart_counts.items():

                product = products[product_name]

                subtotal = (
                    product["price"]
                    * quantity
                )

                total_price += subtotal


                emoji_col, item_col, quantity_col, price_col, remove_col = (
                    st.columns(
                        [0.7, 3.3, 1, 1.4, 0.7]
                    )
                )


                with emoji_col:

                    st.markdown(
                        f"<div style='"
                        f"font-size:45px;"
                        f"text-align:center;"
                        f"'>"
                        f"{product['emoji']}"
                        f"</div>",
                        unsafe_allow_html=True
                    )


                with item_col:

                    st.markdown(
                        f"### {product_name}"
                    )

                    st.caption(
                        product["description"]
                    )


                with quantity_col:

                    st.metric(
                        "Aantal",
                        quantity
                    )


                with price_col:

                    st.metric(
                        "Subtotaal",
                        f"€{subtotal:.2f}"
                    )


                with remove_col:

                    st.write("")

                    if st.button(
                        "➖",
                        key="remove_" + product_name,
                        help="Verwijder één ijsje"
                    ):

                        st.session_state.cart.remove(
                            product_name
                        )

                        st.session_state.shop_page = "Cart"

                        st.rerun()


                st.divider()


            # =================================================
            # TOTAAL
            # =================================================

            total_left, total_right = st.columns(
                [4, 1.5]
            )


            with total_right:

                st.markdown(
                    "### Totaal"
                )

                st.markdown(
                    f"# €{total_price:.2f}"
                )


            st.write("")


            # =================================================
            # KNOPPEN
            # =================================================

            clear_col, order_col = st.columns(
                [1, 2]
            )


            with clear_col:

                if st.button(
                    "🗑️ Winkelwagen legen",
                    use_container_width=True
                ):

                    st.session_state.cart = []
                    st.session_state.shop_page = "Cart"

                    st.rerun()


            with order_col:

                if st.button(
                    "🍦 Nepbestelling plaatsen",
                    type="primary",
                    use_container_width=True
                ):

                    st.session_state.order_total = total_price

                    st.session_state.order_items = (
                        st.session_state.cart.copy()
                    )

                    st.session_state.cart = []

                    st.session_state.shop_page = "Confirmation"

                    st.rerun()


    # ========================================================
    # BESTELLING ONTVANGEN
    # ========================================================

    elif st.session_state.shop_page == "Confirmation":

        st.balloons()


        if st.button(
            "← Terug naar winkelwagen",
            key="confirmation_back"
        ):

            st.session_state.shop_page = "Cart"
            st.rerun()


        st.write("")
        st.write("")


        confirmation_left, confirmation_center, confirmation_right = (
            st.columns(
                [1, 2, 1]
            )
        )


        with confirmation_center:

            st.markdown(
                "<p style='"
                "text-align:center;"
                "font-size:90px;"
                "'>"
                "✅"
                "</p>",
                unsafe_allow_html=True
            )


            st.markdown(
                "<h1 style='text-align:center;'>"
                "Bestelling ontvangen!"
                "</h1>",
                unsafe_allow_html=True
            )


            st.markdown(
                "<p style='"
                "text-align:center;"
                "font-size:19px;"
                "'>"
                "Bedankt voor je bestelling!"
                "</p>",
                unsafe_allow_html=True
            )


            st.success(
                "🍦 Je nepbestelling is succesvol binnengekomen!"
            )


            # =================================================
            # BESTELOVERZICHT
            # =================================================

            st.markdown(
                "### 🧾 Besteloverzicht"
            )


            order_counts = {}


            for item in st.session_state.order_items:

                if item in order_counts:

                    order_counts[item] += 1

                else:

                    order_counts[item] = 1


            for product_name, quantity in order_counts.items():

                product = products[product_name]

                subtotal = (
                    product["price"]
                    * quantity
                )


                st.write(
                    product["emoji"]
                    + " **"
                    + product_name
                    + "** × "
                    + str(quantity)
                    + " — €"
                    + f"{subtotal:.2f}"
                )


            st.divider()


            st.markdown(
                "## Totaal: €"
                + f"{st.session_state.order_total:.2f}"
            )


            st.info(
                "Dit is een demonstratiebestelling. "
                "Er is geen echte aankoop of betaling gedaan."
            )


            # =================================================
            # NIEUWE BESTELLING
            # =================================================

            if st.button(
                "🍦 Nieuwe bestelling plaatsen",
                type="primary",
                use_container_width=True
            ):

                st.session_state.order_items = []
                st.session_state.order_total = 0

                st.session_state.shop_page = "Menu"

                st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer-text">'
    'VeiligInloggen &nbsp; | &nbsp; '
    'Gebouwd voor een veiligere digitale wereld'
    '</div>',
    unsafe_allow_html=True
)