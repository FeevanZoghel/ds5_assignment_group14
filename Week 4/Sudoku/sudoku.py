import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from controle import geldige_invoer
from controle import controleer_zet
from controle import kies_puzzel
from controle import los_sudoku_op
from controle import bord_is_opgelost


# -------------------------
# Venster
# -------------------------

window = tk.Tk()
window.title("Sudoku")


# -------------------------
# Moeilijkheid
# -------------------------

moeilijkheid = tk.StringVar()
moeilijkheid.set("Makkelijk")


label_moeilijkheid = tk.Label(
    window,
    text="Moeilijkheid:"
)

label_moeilijkheid.grid(
    row=0,
    column=0,
    columnspan=3,
    pady=5
)


keuzelijst = ttk.Combobox(
    window,
    textvariable=moeilijkheid,
    values=[
        "Makkelijk",
        "Normaal",
        "Moeilijk"
    ],
    state="readonly"
)

keuzelijst.grid(
    row=1,
    column=0,
    columnspan=3,
    pady=5
)


# -------------------------
# Sudoku-vakjes
# -------------------------

vakjes = []

for rij in range(9):
    vakjes.append([])


# -------------------------
# Geselecteerd vakje
# -------------------------

geselecteerde_rij = None
geselecteerde_kolom = None


# -------------------------
# Huidige puzzel
# -------------------------

huidige_oplossing = None


# -------------------------
# Vakje selecteren
# -------------------------

def selecteer_vakje(rij, kolom):

    global geselecteerde_rij
    global geselecteerde_kolom

    geselecteerde_rij = rij
    geselecteerde_kolom = kolom


# -------------------------
# Invoer controleren
# -------------------------

def controleer_invoer(event):

    vakje = event.widget
    waarde = vakje.get()

    if geldige_invoer(waarde):

        vakje.config(bg="white")

    else:

        vakje.delete(0, tk.END)
        vakje.config(bg="white")


# -------------------------
# Geselecteerd vakje controleren
# -------------------------

def controleer_geselecteerd_vakje():

    if geselecteerde_rij is None:

        messagebox.showinfo(
            "Geen vakje geselecteerd",
            "Selecteer eerst een vakje."
        )

        return

    vakje = vakjes[
        geselecteerde_rij
    ][
        geselecteerde_kolom
    ]

    cijfer = vakje.get()

    if cijfer == "":

        messagebox.showinfo(
            "Leeg vakje",
            "Vul eerst een cijfer in."
        )

        return

    if controleer_zet(
        vakjes,
        geselecteerde_rij,
        geselecteerde_kolom,
        cijfer
    ):

        vakje.config(
            bg="lightgreen"
        )

        # Correct cijfer vastzetten
        vakje.config(
            state="disabled"
        )

    else:

        vakje.config(
            bg="lightcoral"
        )

        messagebox.showinfo(
            "Ongeldige zet",
            "Dit cijfer komt al voor in de rij, kolom of het 3×3-blok."
        )

        # Fout cijfer verwijderen
        vakje.delete(
            0,
            tk.END
        )

        # Achtergrond terug naar normaal
        vakje.config(
            bg="white"
        )

        return

    # -------------------------
    # Hele bord controleren
    # -------------------------

    if bord_is_opgelost(
        vakjes,
        huidige_oplossing
    ):

        messagebox.showinfo(
            "Gefeliciteerd!",
            "Je hebt de Sudoku opgelost!"
        )


# -------------------------
# 3 × 3 blokken maken
# -------------------------

for blok_rij in range(3):

    for blok_kolom in range(3):

        blok = tk.Frame(
            window,
            bd=3,
            relief="solid"
        )

        blok.grid(
            row=blok_rij + 2,
            column=blok_kolom
        )

        for rij in range(3):

            for kolom in range(3):

                vakje = tk.Entry(
                    blok,
                    width=3,
                    justify="center"
                )

                vakje.grid(
                    row=rij,
                    column=kolom
                )

                # Positie op het volledige bord
                echte_rij = blok_rij * 3 + rij
                echte_kolom = blok_kolom * 3 + kolom

                # Vakje opslaan
                vakjes[echte_rij].append(vakje)

                # Vakje selecteren
                vakje.bind(
                    "<FocusIn>",
                    lambda event,
                    r=echte_rij,
                    k=echte_kolom:
                    selecteer_vakje(r, k)
                )

                # Invoer controleren
                vakje.bind(
                    "<KeyRelease>",
                    controleer_invoer
                )


# -------------------------
# Puzzel laden
# -------------------------

def laad_puzzel():

    global huidige_oplossing
    global geselecteerde_rij
    global geselecteerde_kolom

    # Selectie resetten
    geselecteerde_rij = None
    geselecteerde_kolom = None

    # Hoofdletters omzetten naar kleine letters
    moeilijkheid_voor_controle = (
        moeilijkheid.get().lower()
    )

    # Nieuwe puzzel kiezen
    puzzel = kies_puzzel(
        moeilijkheid_voor_controle
    )

    # Oplossing berekenen
    huidige_oplossing = los_sudoku_op(
        puzzel
    )

    # Bord leegmaken
    for rij in range(9):

        for kolom in range(9):

            vakje = vakjes[rij][kolom]

            vakje.config(
                state="normal"
            )

            vakje.delete(
                0,
                tk.END
            )

            vakje.config(
                bg="white"
            )

    # Puzzel invullen
    for rij in range(9):

        for kolom in range(9):

            cijfer = puzzel[rij][kolom]

            vakje = vakjes[rij][kolom]

            if cijfer != 0:

                vakje.insert(
                    0,
                    str(cijfer)
                )

                # Voorgegeven cijfer vastzetten
                vakje.config(
                    state="disabled"
                )


# -------------------------
# Moeilijkheid gewijzigd
# -------------------------

def moeilijkheid_gewijzigd(event):

    laad_puzzel()


keuzelijst.bind(
    "<<ComboboxSelected>>",
    moeilijkheid_gewijzigd
)


# -------------------------
# Eerste puzzel laden
# -------------------------

laad_puzzel()


# -------------------------
# Controle-knop
# -------------------------

knop_controleer = tk.Button(
    window,
    text="Controleer",
    command=controleer_geselecteerd_vakje
)

knop_controleer.grid(
    row=5,
    column=1,
    pady=10
)


# -------------------------
# Nieuw spel-knop
# -------------------------

knop_nieuw_spel = tk.Button(
    window,
    text="Nieuw spel",
    command=laad_puzzel
)

knop_nieuw_spel.grid(
    row=5,
    column=2,
    pady=10
)


# -------------------------
# Programma starten
# -------------------------

window.mainloop()