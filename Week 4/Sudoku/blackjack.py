import streamlit as st
import random

# ============================================================
# PAGINA-INSTELLINGEN
# ============================================================

st.set_page_config(
    page_title="Blackjack Casino",
    page_icon="♠️",
    layout="centered"
)

# ============================================================
# CSS - CASINO LOOK
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at center, #146b3a 0%, #0b4d2b 45%, #062e1c 100%);
    color: white;
}

.block-container {
    max-width: 950px;
    padding-top: 2rem;
}

/* Titel */
.casino-title {
    text-align: center;
    font-size: 52px;
    font-weight: 900;
    color: #f5c542;
    letter-spacing: 4px;
    text-shadow: 2px 2px 5px black;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #eeeeee;
    margin-bottom: 30px;
}

/* Dealer / speler gebied */
.table-section {
    background: rgba(0, 0, 0, 0.18);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 20px;
}

/* Kaarten */
.card {
    display: inline-flex;
    flex-direction: column;
    justify-content: space-between;

    width: 95px;
    height: 135px;

    background: white;
    border-radius: 10px;

    margin-right: 10px;
    margin-bottom: 10px;

    padding: 8px;

    font-size: 27px;
    font-weight: bold;

    box-shadow: 4px 5px 10px rgba(0,0,0,0.45);
    border: 2px solid #dddddd;
}

.red-card {
    color: #d71920;
}

.black-card {
    color: #111111;
}

.card-bottom {
    text-align: right;
    transform: rotate(180deg);
}

.hidden-card {
    display: inline-flex;
    justify-content: center;
    align-items: center;

    width: 95px;
    height: 135px;

    border-radius: 10px;
    margin-right: 10px;
    margin-bottom: 10px;

    background:
        repeating-linear-gradient(
            45deg,
            #172554,
            #172554 8px,
            #1e3a8a 8px,
            #1e3a8a 16px
        );

    border: 5px solid white;
    box-shadow: 4px 5px 10px rgba(0,0,0,0.45);

    font-size: 35px;
}

/* Chip informatie */
.chip-box {
    background: rgba(0,0,0,0.35);
    border-radius: 14px;
    padding: 15px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.15);
}

.result-win {
    background: rgba(25, 150, 70, 0.85);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    font-size: 23px;
    font-weight: bold;
}

.result-loss {
    background: rgba(180, 30, 30, 0.85);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    font-size: 23px;
    font-weight: bold;
}

.result-push {
    background: rgba(220, 160, 20, 0.85);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    font-size: 23px;
    font-weight: bold;
}

/* Streamlit buttons */
.stButton > button {
    width: 100%;
    height: 52px;
    font-size: 18px;
    font-weight: bold;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# CONSTANTEN
# ============================================================

START_BALANCE = 1000

SUITS = ["♠", "♥", "♦", "♣"]

RANKS = [
    "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "J", "Q", "K", "A"
]


# ============================================================
# BLACKJACK FUNCTIES
# ============================================================

def create_deck():
    """
    Maakt een standaard deck van 52 kaarten
    en schudt deze.
    """

    deck = []

    for suit in SUITS:
        for rank in RANKS:
            deck.append({
                "rank": rank,
                "suit": suit
            })

    random.shuffle(deck)

    return deck


def card_value(rank):
    """
    Geeft de standaardwaarde van een kaart.
    Een aas begint als 11.
    """

    if rank in ["J", "Q", "K"]:
        return 10

    if rank == "A":
        return 11

    return int(rank)


def hand_value(hand):
    """
    Berekent de waarde van een blackjack-hand.

    Azen tellen eerst als 11.
    Als de score boven 21 komt,
    wordt een aas veranderd van 11 naar 1.
    """

    total = 0
    aces = 0

    for card in hand:

        total += card_value(card["rank"])

        if card["rank"] == "A":
            aces += 1

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total


def is_blackjack(hand):
    """
    Blackjack betekent:
    precies twee kaarten met totale waarde 21.
    """

    return len(hand) == 2 and hand_value(hand) == 21


def draw_card():
    """
    Pakt de bovenste kaart uit het deck.
    """

    return st.session_state.deck.pop()


def card_html(card):
    """Maakt één speelkaart."""

    rank = card["rank"]
    suit = card["suit"]

    if suit in ["♥", "♦"]:
        color = "#d32f2f"
    else:
        color = "#111111"

    return f"""
    <span style="
        display:inline-block;
        width:95px;
        height:135px;
        background:white;
        color:{color};
        border-radius:10px;
        border:2px solid #d0d0d0;
        box-shadow:4px 5px 10px rgba(0,0,0,0.4);
        margin-right:12px;
        padding:10px;
        box-sizing:border-box;
        font-size:27px;
        font-weight:bold;
        vertical-align:top;
        line-height:1.2;
    ">{rank}{suit}<br><br><span style="font-size:40px;">{suit}</span></span>
    """


def hidden_card_html():
    """Maakt de gesloten kaart van de dealer."""

    return """
    <span style="
        display:inline-block;
        width:95px;
        height:135px;
        background:#172554;
        color:white;
        border-radius:10px;
        border:5px solid white;
        box-shadow:4px 5px 10px rgba(0,0,0,0.4);
        margin-right:12px;
        padding:35px 10px;
        box-sizing:border-box;
        font-size:38px;
        font-weight:bold;
        text-align:center;
        vertical-align:top;
    ">♠</span>
    """


def show_hand(hand, hide_second=False):
    """Laat alle kaarten naast elkaar zien."""

    html = ""

    for i, card in enumerate(hand):

        if hide_second and i == 1:
            html += hidden_card_html()
        else:
            html += card_html(card)

    # BELANGRIJK:
    # Alles in één markdown-call renderen
    st.markdown(
        html.replace("\n", ""),
        unsafe_allow_html=True
    )

# ============================================================
# SESSION STATE
# ============================================================

if "balance" not in st.session_state:
    st.session_state.balance = START_BALANCE

if "bet" not in st.session_state:
    st.session_state.bet = 50

if "deck" not in st.session_state:
    st.session_state.deck = []

if "player_hand" not in st.session_state:
    st.session_state.player_hand = []

if "dealer_hand" not in st.session_state:
    st.session_state.dealer_hand = []

if "game_active" not in st.session_state:
    st.session_state.game_active = False

if "game_finished" not in st.session_state:
    st.session_state.game_finished = False

if "result" not in st.session_state:
    st.session_state.result = ""

if "result_type" not in st.session_state:
    st.session_state.result_type = ""

if "payout_done" not in st.session_state:
    st.session_state.payout_done = False


# ============================================================
# SPELLOGICA
# ============================================================

def finish_game(result, result_type, payout):
    """
    Beëindigt het spel en verwerkt de winst/verlies.
    """

    st.session_state.game_active = False
    st.session_state.game_finished = True

    st.session_state.result = result
    st.session_state.result_type = result_type

    if not st.session_state.payout_done:
        st.session_state.balance += payout
        st.session_state.payout_done = True


def start_game():

    bet = st.session_state.bet

    if bet > st.session_state.balance:
        return

    # Inzet afschrijven
    st.session_state.balance -= bet

    st.session_state.deck = create_deck()

    st.session_state.player_hand = [
        draw_card(),
        draw_card()
    ]

    st.session_state.dealer_hand = [
        draw_card(),
        draw_card()
    ]

    st.session_state.game_active = True
    st.session_state.game_finished = False
    st.session_state.result = ""
    st.session_state.result_type = ""
    st.session_state.payout_done = False

    player_blackjack = is_blackjack(
        st.session_state.player_hand
    )

    dealer_blackjack = is_blackjack(
        st.session_state.dealer_hand
    )

    # Direct controleren op blackjack
    if player_blackjack and dealer_blackjack:

        finish_game(
            "🤝 Beide Blackjack — Push!",
            "push",
            bet
        )

    elif player_blackjack:

        # Blackjack betaalt 3:2
        payout = bet * 2.5

        finish_game(
            "🃏 BLACKJACK! Je wint!",
            "win",
            payout
        )

    elif dealer_blackjack:

        finish_game(
            "Dealer heeft Blackjack.",
            "loss",
            0
        )


def hit():

    if not st.session_state.game_active:
        return

    st.session_state.player_hand.append(
        draw_card()
    )

    value = hand_value(
        st.session_state.player_hand
    )

    if value > 21:

        finish_game(
            f"💥 Bust! Je hebt {value}.",
            "loss",
            0
        )

    elif value == 21:

        stand()


def stand():

    if not st.session_state.game_active:
        return

    # Dealer trekt tot minimaal 17
    while hand_value(st.session_state.dealer_hand) < 17:

        st.session_state.dealer_hand.append(
            draw_card()
        )

    player = hand_value(
        st.session_state.player_hand
    )

    dealer = hand_value(
        st.session_state.dealer_hand
    )

    bet = st.session_state.bet

    if dealer > 21:

        finish_game(
            f"🎉 Dealer bust met {dealer}. Je wint!",
            "win",
            bet * 2
        )

    elif player > dealer:

        finish_game(
            f"🏆 Je wint! {player} tegen {dealer}.",
            "win",
            bet * 2
        )

    elif dealer > player:

        finish_game(
            f"Dealer wint: {dealer} tegen {player}.",
            "loss",
            0
        )

    else:

        finish_game(
            f"🤝 Push! Jullie hebben allebei {player}.",
            "push",
            bet
        )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="casino-title">♠ BLACKJACK ♥</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Beat the dealer • Get as close to 21 as possible</div>',
    unsafe_allow_html=True
)


# ============================================================
# SALDO EN INZET
# ============================================================

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        f"""
        <div class="chip-box">
            <div style="font-size:15px;">BALANCE</div>
            <div style="font-size:28px;font-weight:bold;">
                🪙 {st.session_state.balance:g}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f"""
        <div class="chip-box">
            <div style="font-size:15px;">CURRENT BET</div>
            <div style="font-size:28px;font-weight:bold;">
                🎰 {st.session_state.bet:g}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")


# ============================================================
# INZET KIEZEN
# ============================================================

if not st.session_state.game_active:

    max_bet = int(st.session_state.balance)

    if max_bet > 0:

        possible_bets = [
            amount
            for amount in [10, 25, 50, 100, 250, 500]
            if amount <= max_bet
        ]

        # Zorg dat er altijd een geldige inzet bestaat
        if not possible_bets:
            possible_bets = [max_bet]

        if st.session_state.bet not in possible_bets:
            st.session_state.bet = possible_bets[0]

        selected_bet = st.select_slider(
            "Choose your bet",
            options=possible_bets,
            value=st.session_state.bet
        )

        st.session_state.bet = selected_bet


# ============================================================
# DEALER
# ============================================================

if st.session_state.player_hand:

    st.markdown('<div class="table-section">', unsafe_allow_html=True)

    st.subheader("🎩 Dealer")

    if st.session_state.game_active:

        show_hand(
            st.session_state.dealer_hand,
            hide_second=True
        )

        first_card_value = hand_value(
            [st.session_state.dealer_hand[0]]
        )

        st.write(
            f"Visible value: **{first_card_value}**"
        )

    else:

        show_hand(
            st.session_state.dealer_hand
        )

        st.write(
            f"Dealer value: **{hand_value(st.session_state.dealer_hand)}**"
        )

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# PLAYER
# ============================================================

if st.session_state.player_hand:

    st.markdown('<div class="table-section">', unsafe_allow_html=True)

    st.subheader("👤 Your hand")

    show_hand(
        st.session_state.player_hand
    )

    player_value = hand_value(
        st.session_state.player_hand
    )

    st.write(
        f"Your value: **{player_value}**"
    )

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# RESULTAAT
# ============================================================

if st.session_state.game_finished:

    if st.session_state.result_type == "win":

        css_class = "result-win"

    elif st.session_state.result_type == "loss":

        css_class = "result-loss"

    else:

        css_class = "result-push"

    st.markdown(
        f"""
        <div class="{css_class}">
            {st.session_state.result}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")


# ============================================================
# BUTTONS
# ============================================================

if not st.session_state.game_active:

    if st.session_state.balance > 0:

        if st.button(
            "🃏 DEAL CARDS",
            use_container_width=True,
            type="primary"
        ):
            start_game()
            st.rerun()

    else:

        st.error("You are out of chips!")

        if st.button(
            "🔄 Start again with 1000 chips",
            use_container_width=True
        ):

            st.session_state.balance = START_BALANCE
            st.session_state.bet = 50

            st.session_state.player_hand = []
            st.session_state.dealer_hand = []

            st.session_state.game_active = False
            st.session_state.game_finished = False

            st.rerun()


else:

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "➕ HIT",
            use_container_width=True,
            type="primary"
        ):
            hit()
            st.rerun()

    with col2:

        if st.button(
            "✋ STAND",
            use_container_width=True
        ):
            stand()
            st.rerun()


# ============================================================
# SPELREGELS
# ============================================================

with st.expander("📖 Blackjack rules"):

    st.markdown("""
    **Goal**

    Get closer to **21** than the dealer without going over 21.

    **Card values**

    - 2–10 = face value
    - J, Q and K = 10
    - Ace = 1 or 11
    - Blackjack = Ace + 10-value card in your first two cards

    **Actions**

    **Hit** → take another card  
    **Stand** → keep your current hand

    **Dealer**

    The dealer must draw cards until reaching at least **17**.

    **Payout**

    Normal win: **1:1**  
    Blackjack: **3:2**  
    Push: your bet is returned
    """)