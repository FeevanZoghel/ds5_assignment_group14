import streamlit as st
import re
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SecureLogin",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# FILE PATHS
# ============================================================

# Folder where this Python file is located
BASE_DIR = Path(__file__).resolve().parent

# Elmo image in the same folder as this Python file
ELMO_IMAGE = BASE_DIR / "elmo.png"


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

/* ==========================================================
   BACKGROUND
========================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 15% 15%,
            rgba(255, 255, 255, 0.30) 0%,
            transparent 32%
        ),
        radial-gradient(
            circle at 85% 10%,
            rgba(255, 255, 255, 0.20) 0%,
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


/* ==========================================================
   PAGE
========================================================== */

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}


/* ==========================================================
   BRAND
========================================================== */

.brand {
    font-size: 22px;
    font-weight: 700;
    color: #102a56;
    margin-bottom: 25px;
}

.brand-light {
    font-weight: 400;
}


/* ==========================================================
   LEFT SIDE
========================================================== */

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
    max-width: 260px;
}


/* ==========================================================
   CENTER
========================================================== */

.lock-icon {
    width: 65px;
    height: 65px;

    margin:
        5px auto
        15px auto;

    border-radius: 50%;

    background: rgba(255, 255, 255, 0.55);

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


/* ==========================================================
   INPUT FIELDS
========================================================== */

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


/* ==========================================================
   PASSWORD REQUIREMENTS
========================================================== */

.requirements {
    background: rgba(255, 255, 255, 0.70);

    border:
        1px solid
        rgba(255, 255, 255, 0.60);

    border-radius: 14px;

    padding:
        16px
        20px;

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


/* ==========================================================
   BUTTONS
========================================================== */

.stButton > button {

    width: 100%;
    height: 49px;

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
        rgba(36, 99, 212, 0.20);

    transition: all 0.2s ease;
}

.stButton > button:hover {

    transform: translateY(-1px);

    box-shadow:
        0 10px 24px
        rgba(36, 99, 212, 0.30);
}


/* ==========================================================
   ALERT MESSAGES
========================================================== */

/* Darker text so the success message is easier to read */
div[data-testid="stAlert"] p {
    color: #14532d !important;
    font-weight: 700 !important;
}


/* ==========================================================
   RIGHT SIDE
========================================================== */

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


/* ==========================================================
   FOOTER
========================================================== */

.footer-text {
    text-align: center;
    color: #657b9c;
    font-size: 12px;
    margin-top: 30px;
    letter-spacing: 0.5px;
}


/* ==========================================================
   ICE CREAM SHOP
========================================================== */

.shop-title {
    font-size: 42px;
    font-weight: 800;
    color: #102a56;
    padding-top: 10px;
}

.shop-subtitle {
    color: #405d83;
    font-size: 17px;
}

.welcome-shop {
    background: rgba(255, 255, 255, 0.60);
    padding: 18px 25px;
    border-radius: 15px;
    margin-bottom: 25px;
}

.welcome-shop-title {
    font-size: 21px;
    font-weight: 700;
    color: #102a56;
}

.welcome-shop-text {
    color: #405d83;
    margin-top: 5px;
}

.product-card {
    text-align: center;
    background: rgba(255, 255, 255, 0.72);
    padding: 25px 15px;
    border-radius: 18px;
    min-height: 230px;
    border: 1px solid rgba(255,255,255,0.55);
    box-shadow: 0 8px 20px rgba(16,42,86,0.08);
}

.product-emoji {
    font-size: 65px;
}

.product-name {
    color: #102a56;
    font-size: 22px;
    font-weight: 700;
    margin-top: 10px;
}

.product-description {
    color: #526b91;
    font-size: 14px;
    min-height: 45px;
}

.product-price {
    color: #102a56;
    font-size: 25px;
    font-weight: 800;
    margin-top: 12px;
}

.elmo-message {
    background: rgba(255,255,255,0.72);
    padding: 25px;
    border-radius: 18px;
    margin-top: 10px;
}

.elmo-message-title {
    font-size: 21px;
    font-weight: 700;
    color: #102a56;
}

.elmo-message-text {
    color: #405d83;
    margin-top: 8px;
    font-size: 16px;
}


/* ==========================================================
   PROGRESS BAR
========================================================== */

.stProgress > div > div > div > div {
    background-color: #2563eb;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# EMAIL VALIDATION
# ============================================================

def validate_email(email):

    email = email.strip()

    if email == "":
        return False, "Please enter an email address."

    if len(email) > 254:
        return False, "Email address is too long."

    if " " in email:
        return False, "Email cannot contain spaces."

    if email.count("@") != 1:
        return False, "Email must contain exactly one @ symbol."

    username, domain = email.split("@")

    if username == "":
        return False, "Username cannot be empty."

    if domain == "":
        return False, "Domain cannot be empty."

    if len(username) > 64:
        return False, "Username is too long."

    if username.startswith(".") or username.endswith("."):
        return False, "Username cannot start or end with a dot."

    if domain.startswith(".") or domain.endswith("."):
        return False, "Domain cannot start or end with a dot."

    if ".." in email:
        return False, "Email cannot contain consecutive dots."

    if "." not in domain:
        return False, "Domain must contain a dot."

    domain_name, extension = domain.rsplit(".", 1)

    if domain_name == "":
        return False, "Domain name cannot be empty."

    if len(extension) < 2:
        return False, "Domain extension must contain at least 2 characters."

    username_pattern = r"^[A-Za-z0-9._%+-]+$"

    if not re.match(username_pattern, username):
        return False, "Username contains invalid characters."

    domain_pattern = r"^[A-Za-z0-9.-]+$"

    if not re.match(domain_pattern, domain):
        return False, "Domain contains invalid characters."

    return True, "Valid email address."


# ============================================================
# PASSWORD CHECKS
# ============================================================

def password_checks(password):

    special_characters = "!@#$%^&*()_+-=[]{};:,.?"

    return {
        "At least 8 characters":
            len(password) >= 8,

        "One uppercase letter (A-Z)":
            any(c.isupper() for c in password),

        "One lowercase letter (a-z)":
            any(c.islower() for c in password),

        "One number (0-9)":
            any(c.isdigit() for c in password),

        "One special character":
            any(c in special_characters for c in password),

        "No spaces":
            " " not in password
    }


# ============================================================
# PASSWORD VALIDATION
# ============================================================

def validate_password(password):

    if password == "":
        return False, "Please enter a password."

    checks = password_checks(password)

    for requirement, passed in checks.items():

        if not passed:
            return False, "Missing requirement: " + requirement

    return True, "Valid password."


# ============================================================
# PASSWORD STRENGTH
# ============================================================

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


# ============================================================
# BRAND
# ============================================================

st.markdown(
    '<div class="brand">'
    '🔒 Secure'
    '<span class="brand-light">Login</span>'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# CREATE ACCOUNT PAGE
# ============================================================

if not st.session_state.account_created:

    left, center, right = st.columns(
        [1, 1.55, 1],
        gap="large"
    )


    # ========================================================
    # LEFT SIDE
    # ========================================================

    with left:

        st.markdown(
            '<div class="hero-title">'
            'A safer<br>'
            'brighter<br>'
            'tomorrow'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="hero-line"></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="hero-text">'
            'Create your account and take the first step '
            'towards a more secure digital experience.'
            '</div>',
            unsafe_allow_html=True
        )


    # ========================================================
    # CENTER
    # ========================================================

    with center:

        st.markdown(
            '<div class="lock-icon">🔐</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="main-title">'
            'Create your account'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="main-subtitle">'
            'Create a secure account to continue'
            '</div>',
            unsafe_allow_html=True
        )


        # EMAIL
        email = st.text_input(
            "Email address",
            placeholder="name@example.com",
            key="register_email"
        )


        # PASSWORD
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a strong password",
            key="register_password"
        )


        # CONFIRM PASSWORD
        repeat_password = st.text_input(
            "Confirm password",
            type="password",
            placeholder="Enter your password again",
            key="repeat_password"
        )


        # ====================================================
        # PASSWORD REQUIREMENTS
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


        requirements_box = (
            '<div class="requirements">'
            '<div class="requirements-title">'
            'Password requirements'
            '</div>'
            + requirement_html +
            '</div>'
        )

        st.markdown(
            requirements_box,
            unsafe_allow_html=True
        )


        # ====================================================
        # PASSWORD STRENGTH
        # ====================================================

        if password:

            strength = password_strength(password)

            if strength <= 0.35:
                strength_text = "Weak"

            elif strength <= 0.65:
                strength_text = "Medium"

            elif strength < 1:
                strength_text = "Good"

            else:
                strength_text = "Strong"

            st.caption(
                "Password strength: " + strength_text
            )

            st.progress(strength)


        # ====================================================
        # CREATE ACCOUNT BUTTON
        # ====================================================

        if st.button(
            "Create Account  →",
            type="primary",
            use_container_width=True
        ):

            email_valid, email_message = validate_email(email)

            password_valid, password_message = validate_password(password)

            if not email_valid:

                st.error(email_message)

            elif not password_valid:

                st.error(password_message)

            elif password != repeat_password:

                st.error(
                    "The passwords do not match."
                )

            else:

                st.session_state.saved_email = email.strip()

                st.session_state.saved_password = password

                st.session_state.account_created = True

                st.rerun()


    # ========================================================
    # RIGHT SIDE
    # ========================================================

    with right:

        st.markdown(
            '<div class="feature">'
            '<div class="right-title">'
            '🛡️ &nbsp; Secure'
            '</div>'
            '<div class="right-text">'
            'Your information is protected.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="feature">'
            '<div class="right-title">'
            '👤 &nbsp; Private'
            '</div>'
            '<div class="right-text">'
            'We never share your data.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="feature">'
            '<div class="right-title">'
            '⚡ &nbsp; Simple'
            '</div>'
            '<div class="right-text">'
            'Fast and easy to use.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


# ============================================================
# LOGIN PAGE
# ============================================================

elif not st.session_state.logged_in:

    left_space, login, right_space = st.columns(
        [1, 1.2, 1]
    )

    with login:

        st.markdown(
            '<div class="lock-icon">🔐</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="main-title">'
            'Welcome back'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="main-subtitle">'
            'Sign in to your account'
            '</div>',
            unsafe_allow_html=True
        )

        st.success(
            "✓ Account successfully created!"
        )


        # LOGIN EMAIL
        login_email = st.text_input(
            "Email address",
            placeholder="name@example.com",
            key="login_email"
        )


        # LOGIN PASSWORD
        login_password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )


        # LOGIN BUTTON
        if st.button(
            "Log in →",
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

                st.rerun()

            else:

                st.error(
                    "Incorrect email address or password."
                )


# ============================================================
# ELMO'S ICE CREAM SHOP
# ============================================================

else:

    # ========================================================
    # BALLOONS AFTER LOGIN
    # ========================================================

    if st.session_state.show_balloons:
        st.balloons()
        st.session_state.show_balloons = False


    # ========================================================
    # PRODUCTS
    # ========================================================

    products = {
        "Strawberry": {
            "emoji": "🍓",
            "description": "Sweet strawberry ice cream",
            "price": 2.95
        },

        "Chocolate": {
            "emoji": "🍫",
            "description": "Rich chocolate ice cream",
            "price": 3.25
        },

        "Cookie Crunch": {
            "emoji": "🍪",
            "description": "Vanilla with cookie pieces",
            "price": 3.50
        },

        "Rainbow": {
            "emoji": "🌈",
            "description": "Elmo's colorful special",
            "price": 3.75
        },

        "Vanilla Dream": {
            "emoji": "🍦",
            "description": "Classic creamy vanilla",
            "price": 2.75
        },

        "Cherry Sundae": {
            "emoji": "🍒",
            "description": "Ice cream sundae with cherry",
            "price": 4.25
        }
    }


    # ========================================================
    # SIDEBAR
    # ========================================================

    with st.sidebar:

        # Elmo image
        if ELMO_IMAGE.exists():
            st.image(
                str(ELMO_IMAGE),
                width=120
            )

        st.markdown(
            """
            <h2 style="
                color: #102a56;
                margin-bottom: 0px;
            ">
                🍦 Elmo's
            </h2>

            <p style="
                color: #526b91;
                margin-top: 0px;
            ">
                Ice Cream Shop
            </p>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        st.markdown("### Navigation")

        # Count products in cart
        cart_amount = len(st.session_state.cart)

        page = st.radio(
            "Choose a page",
            [
                "🏠 Home",
                "🍦 Menu + Prices",
                f"🛒 Shopping Cart ({cart_amount})"
            ],
            label_visibility="collapsed"
        )

        st.divider()

        st.caption(
            "Logged in as:"
        )

        st.write(
            st.session_state.saved_email
        )

        st.write("")

        if st.button(
            "🚪 Log out",
            use_container_width=True
        ):

            st.session_state.logged_in = False

            st.session_state.cart = []

            st.rerun()


    # ========================================================
    # HEADER
    # ========================================================

    header1, header2 = st.columns(
        [5, 1]
    )

    with header1:

        st.markdown(
            """
            <div class="shop-title">
                🍦 Elmo's Ice Cream Shop
            </div>

            <div class="shop-subtitle">
                The coolest ice cream in town!
            </div>
            """,
            unsafe_allow_html=True
        )

    with header2:

        st.metric(
            "🛒 Cart",
            len(st.session_state.cart)
        )


    st.divider()


    # ========================================================
    # PAGE 1
    # HOME
    # ========================================================

    if page == "🏠 Home":

        st.markdown(
            f"""
            <div class="welcome-shop">

                <div class="welcome-shop-title">
                    👋 Welcome to Elmo's Ice Cream Shop!
                </div>

                <div class="welcome-shop-text">
                    You are logged in as
                    {st.session_state.saved_email}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # HOME COLUMNS
        # ----------------------------------------------------

        elmo_col, text_col = st.columns(
            [1, 2]
        )


        with elmo_col:

            if ELMO_IMAGE.exists():

                st.image(
                    str(ELMO_IMAGE),
                    width=300
                )

            else:

                st.warning(
                    "elmo.png was not found."
                )


        with text_col:

            st.markdown(
                """
                ## ❤️ Welcome!

                Welcome to **Elmo's Ice Cream Shop!**

                Here you can discover our delicious
                collection of fictional ice creams.

                Visit **Menu + Prices** to see all our
                flavors and add your favorites to your
                shopping cart.

                When you're finished, open your
                **Shopping Cart** to see your order and
                total price.
                """
            )

            st.info(
                "🍓 Elmo's favorite is the Strawberry Special!"
            )


        st.write("")
        st.write("")


        # ----------------------------------------------------
        # SPECIAL OFFER
        # ----------------------------------------------------

        st.markdown(
            """
            <div style="
                background: rgba(255,255,255,0.70);
                border-radius: 18px;
                padding: 30px;
                text-align: center;
            ">

                <div style="
                    font-size: 35px;
                ">
                    🍓 🍦 🍫
                </div>

                <div style="
                    color: #102a56;
                    font-size: 25px;
                    font-weight: 800;
                    margin-top: 10px;
                ">
                    Today's Special
                </div>

                <div style="
                    color: #405d83;
                    font-size: 17px;
                    margin-top: 8px;
                ">
                    Strawberry Special — only €2.95
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


       # ========================================================
    # PAGE 2
    # MENU + PRICES
    # ========================================================

    elif page == "🍦 Menu + Prices":

        st.markdown(
            """
            <h1 style="color:#102a56;">
                🍦 Menu + Prices
            </h1>

            <p style="
                color:#405d83;
                font-size:17px;
                margin-bottom:30px;
            ">
                Choose your favorite ice cream and add it to your shopping cart.
            </p>
            """,
            unsafe_allow_html=True
        )


        # ====================================================
        # FIRST ROW
        # ====================================================

        col1, col2, col3 = st.columns(3, gap="medium")


        # ----------------------------------------------------
        # STRAWBERRY
        # ----------------------------------------------------

        with col1:

            st.markdown(
                "<div style='text-align:center; font-size:75px;'>🍓</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<h3 style='text-align:center; color:#102a56;'>Strawberry</h3>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<p style='text-align:center; color:#405d83;'>"
                "Sweet strawberry ice cream"
                "</p>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<h2 style='text-align:center; color:#102a56;'>€2.95</h2>",
                unsafe_allow_html=True
            )

            if st.button(
                "Add Strawberry 🛒",
                key="add_strawberry",
                use_container_width=True
            ):

                st.session_state.cart.append("Strawberry")

                st.toast("🍓 Strawberry added!")

                st.rerun()


        # ----------------------------------------------------
        # CHOCOLATE
        # ----------------------------------------------------

        with col2:

            st.markdown(
                "<div style='text-align:center; font-size:75px;'>🍫</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<h3 style='text-align:center; color:#102a56;'>Chocolate</h3>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<p style='text-align:center; color:#405d83;'>"
                "Rich chocolate ice cream"
                "</p>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<h2 style='text-align:center; color:#102a56;'>€3.25</h2>",
                unsafe_allow_html=True
            )

            if st.button(
                "Add Chocolate 🛒",
                key="add_chocolate",
                use_container_width=True
            ):

                st.session_state.cart.append("Chocolate")

                st.toast("🍫 Chocolate added!")

                st.rerun()


        # ----------------------------------------------------
        # COOKIE CRUNCH
        # ----------------------------------------------------

        with col3:

            st.markdown(
                "<div style='text-align:center; font-size:75px;'>🍪</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<h3 style='text-align:center; color:#102a56;'>Cookie Crunch</h3>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<p style='text-align:center; color:#405d83;'>"
                "Vanilla ice cream with cookie pieces"
                "</p>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<h2 style='text-align:center; color:#102a56;'>€3.50</h2>",
                unsafe_allow_html=True
            )

            if st.button(
                "Add Cookie Crunch 🛒",
                key="add_cookie",
                use_container_width=True
            ):

                st.session_state.cart.append("Cookie Crunch")

                st.toast("🍪 Cookie Crunch added!")

                st.rerun()


        st.write("")
        st.write("")


        # ====================================================
        # SECOND ROW
        # ====================================================

        col4, col5, col6 = st.columns(3, gap="medium")


        # ----------------------------------------------------
        # RAINBOW
        # ----------------------------------------------------

        with col4:

            st.markdown(
                "<div style='text-align:center; font-size:75px;'>🌈</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<h3 style='text-align:center; color:#102a56;'>Rainbow</h3>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<p style='text-align:center; color:#405d83;'>"
                "Elmo's colorful special"
                "</p>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<h2 style='text-align:center; color:#102a56;'>€3.75</h2>",
                unsafe_allow_html=True
            )

            if st.button(
                "Add Rainbow 🛒",
                key="add_rainbow",
                use_container_width=True
            ):

                st.session_state.cart.append("Rainbow")

                st.toast("🌈 Rainbow added!")

                st.rerun()


        # ----------------------------------------------------
        # VANILLA DREAM
        # ----------------------------------------------------

        with col5:

            st.markdown(
                "<div style='text-align:center; font-size:75px;'>🍦</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<h3 style='text-align:center; color:#102a56;'>Vanilla Dream</h3>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<p style='text-align:center; color:#405d83;'>"
                "Classic creamy vanilla"
                "</p>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<h2 style='text-align:center; color:#102a56;'>€2.75</h2>",
                unsafe_allow_html=True
            )

            if st.button(
                "Add Vanilla Dream 🛒",
                key="add_vanilla",
                use_container_width=True
            ):

                st.session_state.cart.append("Vanilla Dream")

                st.toast("🍦 Vanilla Dream added!")

                st.rerun()


        # ----------------------------------------------------
        # CHERRY SUNDAE
        # ----------------------------------------------------

        with col6:

            st.markdown(
                "<div style='text-align:center; font-size:75px;'>🍒</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<h3 style='text-align:center; color:#102a56;'>Cherry Sundae</h3>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<p style='text-align:center; color:#405d83;'>"
                "Ice cream sundae with cherry"
                "</p>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<h2 style='text-align:center; color:#102a56;'>€4.25</h2>",
                unsafe_allow_html=True
            )

            if st.button(
                "Add Cherry Sundae 🛒",
                key="add_cherry",
                use_container_width=True
            ):

                st.session_state.cart.append("Cherry Sundae")

                st.toast("🍒 Cherry Sundae added!")

                st.rerun()
    # ========================================================
    # PAGE 3
    # SHOPPING CART
    # ========================================================

    else:

        st.markdown(
            """
            <h1 style="
                color:#102a56;
            ">
                🛒 Shopping Cart
            </h1>
            """,
            unsafe_allow_html=True
        )


        # ====================================================
        # EMPTY CART
        # ====================================================

        if len(st.session_state.cart) == 0:

            st.markdown(
                """
                <div style="
                    background:rgba(255,255,255,0.65);
                    border-radius:18px;
                    padding:50px;
                    text-align:center;
                    margin-top:25px;
                ">

                    <div style="
                        font-size:70px;
                    ">
                        🛒
                    </div>

                    <div style="
                        color:#102a56;
                        font-size:25px;
                        font-weight:700;
                    ">
                        Your cart is empty
                    </div>

                    <div style="
                        color:#526b91;
                        margin-top:10px;
                    ">
                        Visit Menu + Prices to add
                        some delicious ice cream!
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        # ====================================================
        # CART HAS PRODUCTS
        # ====================================================

        else:

            # Count how many of each product
            cart_counts = {}

            for item in st.session_state.cart:

                if item in cart_counts:
                    cart_counts[item] += 1

                else:
                    cart_counts[item] = 1


            # =================================================
            # CART ITEMS
            # =================================================

            total_price = 0


            for product_name, quantity in cart_counts.items():

                product = products[product_name]

                subtotal = (
                    product["price"]
                    * quantity
                )

                total_price += subtotal


                item_col, quantity_col, price_col, remove_col = st.columns(
                    [4, 1, 1.5, 1]
                )


                with item_col:

                    st.markdown(
                        f"""
                        ### {product["emoji"]} {product_name}

                        {product["description"]}
                        """
                    )


                with quantity_col:

                    st.metric(
                        "Amount",
                        quantity
                    )


                with price_col:

                    st.metric(
                        "Subtotal",
                        f"€{subtotal:.2f}"
                    )


                with remove_col:

                    if st.button(
                        "➖",
                        key=f"remove_{product_name}"
                    ):

                        st.session_state.cart.remove(
                            product_name
                        )

                        st.rerun()


                st.divider()


            # =================================================
            # TOTAL
            # =================================================

            st.markdown(
                f"""
                <div style="
                    background:rgba(255,255,255,0.75);
                    border-radius:18px;
                    padding:25px;
                    margin-top:20px;
                    text-align:right;
                ">

                    <div style="
                        color:#526b91;
                        font-size:15px;
                    ">
                        Total
                    </div>

                    <div style="
                        color:#102a56;
                        font-size:35px;
                        font-weight:800;
                    ">
                        €{total_price:.2f}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            st.write("")


            # =================================================
            # CART BUTTONS
            # =================================================

            clear_col, order_col = st.columns(
                [1, 2]
            )


            with clear_col:

                if st.button(
                    "🗑️ Empty cart",
                    use_container_width=True
                ):

                    st.session_state.cart = []

                    st.rerun()


            with order_col:

                if st.button(
                    "🍦 Place fake order",
                    type="primary",
                    use_container_width=True
                ):

                    st.success(
                        "🎉 Your fake ice cream order has been placed!"
                    )

                    st.balloons()

                    st.session_state.cart = []


    # ========================================================
    # DISCLAIMER
    # ========================================================

    st.write("")
    st.write("")

    st.caption(
        "This is a fictional demonstration shop. "
        "All products and prices are fake."
    )