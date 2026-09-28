import random


# -------------------------
# Invoer controleren
# -------------------------

def geldige_invoer(waarde):

    if waarde == "":
        return True

    if waarde in "123456789":
        return True

    return False


# -------------------------
# Geldig cijfer controleren
# -------------------------

def geldig(bord, rij, kolom, cijfer):

    # Rij controleren
    for andere_kolom in range(9):

        if bord[rij][andere_kolom] == cijfer:
            return False

    # Kolom controleren
    for andere_rij in range(9):

        if bord[andere_rij][kolom] == cijfer:
            return False

    # 3 × 3 blok controleren
    begin_rij = (rij // 3) * 3
    begin_kolom = (kolom // 3) * 3

    for andere_rij in range(begin_rij, begin_rij + 3):

        for andere_kolom in range(begin_kolom, begin_kolom + 3):

            if bord[andere_rij][andere_kolom] == cijfer:
                return False

    return True


# -------------------------
# Volledige Sudoku genereren
# -------------------------

def genereer_sudoku():

    bord = [
        [0 for kolom in range(9)]
        for rij in range(9)
    ]

    def oplossen():

        for rij in range(9):

            for kolom in range(9):

                if bord[rij][kolom] == 0:

                    cijfers = list(range(1, 10))

                    random.shuffle(cijfers)

                    for cijfer in cijfers:

                        if geldig(
                            bord,
                            rij,
                            kolom,
                            cijfer
                        ):

                            bord[rij][kolom] = cijfer

                            if oplossen():
                                return True

                            bord[rij][kolom] = 0

                    return False

        return True

    oplossen()

    return bord


# -------------------------
# Puzzel maken
# -------------------------

def maak_puzzel(oplossing, aantal_lege_vakjes):

    puzzel = []

    for rij in oplossing:
        puzzel.append(rij.copy())

    # Alle posities verzamelen
    posities = []

    for rij in range(9):

        for kolom in range(9):

            posities.append(
                (rij, kolom)
            )

    # Posities willekeurig maken
    random.shuffle(posities)

    # Cijfers verwijderen
    for i in range(aantal_lege_vakjes):

        rij, kolom = posities[i]

        puzzel[rij][kolom] = 0

    return puzzel


# -------------------------
# Willekeurige puzzel kiezen
# -------------------------

def kies_puzzel(moeilijkheid):

    # Nieuwe volledige Sudoku maken
    oplossing = genereer_sudoku()

    if moeilijkheid == "makkelijk":

        aantal_lege_vakjes = 35

    elif moeilijkheid == "normaal":

        aantal_lege_vakjes = 45

    elif moeilijkheid == "moeilijk":

        aantal_lege_vakjes = 52

    else:

        aantal_lege_vakjes = 35

    # Cijfers verwijderen
    puzzel = maak_puzzel(
        oplossing,
        aantal_lege_vakjes
    )

    return puzzel


# -------------------------
# Rij controleren
# -------------------------

def controleer_rij(vakjes, rij, kolom, cijfer):

    for andere_kolom in range(9):

        if andere_kolom == kolom:
            continue

        waarde = vakjes[rij][andere_kolom].get()

        if waarde == str(cijfer):
            return False

    return True


# -------------------------
# Kolom controleren
# -------------------------

def controleer_kolom(vakjes, rij, kolom, cijfer):

    for andere_rij in range(9):

        if andere_rij == rij:
            continue

        waarde = vakjes[andere_rij][kolom].get()

        if waarde == str(cijfer):
            return False

    return True


# -------------------------
# 3 × 3 blok controleren
# -------------------------

def controleer_blok(vakjes, rij, kolom, cijfer):

    begin_rij = (rij // 3) * 3
    begin_kolom = (kolom // 3) * 3

    for andere_rij in range(begin_rij, begin_rij + 3):

        for andere_kolom in range(begin_kolom, begin_kolom + 3):

            if andere_rij == rij and andere_kolom == kolom:
                continue

            waarde = vakjes[andere_rij][andere_kolom].get()

            if waarde == str(cijfer):
                return False

    return True


# -------------------------
# Zet controleren
# -------------------------

def controleer_zet(vakjes, rij, kolom, cijfer):

    if not controleer_rij(
        vakjes,
        rij,
        kolom,
        cijfer
    ):
        return False

    if not controleer_kolom(
        vakjes,
        rij,
        kolom,
        cijfer
    ):
        return False

    if not controleer_blok(
        vakjes,
        rij,
        kolom,
        cijfer
    ):
        return False

    return True


# -------------------------
# Sudoku oplossen
# -------------------------

def los_sudoku_op(puzzel):

    bord = []

    for rij in puzzel:
        bord.append(rij.copy())

    def oplossen():

        for rij in range(9):

            for kolom in range(9):

                if bord[rij][kolom] == 0:

                    for cijfer in range(1, 10):

                        if geldig(
                            bord,
                            rij,
                            kolom,
                            cijfer
                        ):

                            bord[rij][kolom] = cijfer

                            if oplossen():
                                return True

                            bord[rij][kolom] = 0

                    return False

        return True

    if oplossen():
        return bord

    return None


# -------------------------
# Hele bord controleren
# -------------------------

def bord_is_opgelost(vakjes, oplossing):

    for rij in range(9):

        for kolom in range(9):

            waarde = vakjes[rij][kolom].get()

            if waarde == "":
                return False

            if waarde != str(oplossing[rij][kolom]):
                return False

    return True