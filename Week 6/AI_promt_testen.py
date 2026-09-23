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
    # SHOP HEADER
    # ========================================================

    col_logo, col_title, col_logout = st.columns(
        [1, 4, 1]
    )


    with col_logo:

        # Check if Elmo image exists before displaying it
        if ELMO_IMAGE.exists():

            st.image(
                str(ELMO_IMAGE),
                width=110
            )

        else:

            st.warning(
                "elmo.png was not found."
            )


    with col_title:

        st.markdown(
            '<div class="shop-title">'
            "🍦 Elmo's Ice Cream Shop"
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="shop-subtitle">'
            'The coolest ice cream in town!'
            '</div>',
            unsafe_allow_html=True
        )


    with col_logout:

        if st.button(
            "Log out",
            use_container_width=True
        ):

            st.session_state.logged_in = False

            st.rerun()


    st.divider()


    # ========================================================
    # WELCOME MESSAGE
    # ========================================================

    st.markdown(
        '<div class="welcome-shop">'
        '<div class="welcome-shop-title">'
        "👋 Welcome to Elmo's!"
        '</div>'
        '<div class="welcome-shop-text">'
        'You are logged in as '
        + st.session_state.saved_email +
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # ICE CREAM TITLE
    # ========================================================

    st.markdown(
        '<h2 style="'
        'color:#102a56;'
        'text-align:center;'
        'margin-bottom:5px;'
        '">'
        '🍨 Our Ice Cream'
        '</h2>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p style="'
        'text-align:center;'
        'color:#405d83;'
        'margin-bottom:30px;'
        '">'
        'Pick your favorite flavor!'
        '</p>',
        unsafe_allow_html=True
    )


    # ========================================================
    # PRODUCTS
    # ========================================================

    ice1, ice2, ice3, ice4 = st.columns(4)


    # ========================================================
    # STRAWBERRY
    # ========================================================

    with ice1:

        st.markdown(
            '<div class="product-card">'
            '<div class="product-emoji">🍓</div>'
            '<div class="product-name">Strawberry</div>'
            '<div class="product-description">'
            'Sweet strawberry ice cream'
            '</div>'
            '<div class="product-price">€2.95</div>'
            '</div>',
            unsafe_allow_html=True
        )

        if st.button(
            "Add to cart 🛒",
            key="strawberry",
            use_container_width=True
        ):

            st.toast(
                "🍓 Strawberry added to your cart!"
            )


    # ========================================================
    # CHOCOLATE
    # ========================================================

    with ice2:

        st.markdown(
            '<div class="product-card">'
            '<div class="product-emoji">🍫</div>'
            '<div class="product-name">Chocolate</div>'
            '<div class="product-description">'
            'Rich chocolate ice cream'
            '</div>'
            '<div class="product-price">€3.25</div>'
            '</div>',
            unsafe_allow_html=True
        )

        if st.button(
            "Add to cart 🛒",
            key="chocolate",
            use_container_width=True
        ):

            st.toast(
                "🍫 Chocolate added to your cart!"
            )


    # ========================================================
    # COOKIE CRUNCH
    # ========================================================

    with ice3:

        st.markdown(
            '<div class="product-card">'
            '<div class="product-emoji">🍪</div>'
            '<div class="product-name">Cookie Crunch</div>'
            '<div class="product-description">'
            'Vanilla with cookie pieces'
            '</div>'
            '<div class="product-price">€3.50</div>'
            '</div>',
            unsafe_allow_html=True
        )

        if st.button(
            "Add to cart 🛒",
            key="cookie",
            use_container_width=True
        ):

            st.toast(
                "🍪 Cookie Crunch added to your cart!"
            )


    # ========================================================
    # RAINBOW
    # ========================================================

    with ice4:

        st.markdown(
            '<div class="product-card">'
            '<div class="product-emoji">🌈</div>'
            '<div class="product-name">Rainbow</div>'
            '<div class="product-description">'
            "Elmo's colorful special"
            '</div>'
            '<div class="product-price">€3.75</div>'
            '</div>',
            unsafe_allow_html=True
        )

        if st.button(
            "Add to cart 🛒",
            key="rainbow",
            use_container_width=True
        ):

            st.toast(
                "🌈 Rainbow added to your cart!"
            )


    # ========================================================
    # ELMO'S FAVORITE
    # ========================================================

    st.write("")
    st.write("")

    elmo_image, elmo_message = st.columns(
        [1, 4]
    )


    with elmo_image:

        # Again check if the file exists
        if ELMO_IMAGE.exists():

            st.image(
                str(ELMO_IMAGE),
                width=140
            )

        else:

            st.info(
                "Add elmo.png to the Week 6 folder."
            )


    with elmo_message:

        st.markdown(
            '<div class="elmo-message">'
            '<div class="elmo-message-title">'
            "❤️ Elmo's favorite"
            '</div>'
            '<div class="elmo-message-text">'
            'Elmo loves the Strawberry Special! '
            'Try one today for only €2.95.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


    # ========================================================
    # DISCLAIMER
    # ========================================================

    st.write("")

    st.caption(
        "This is a fictional demonstration shop. "
        "All products and prices are fake."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer-text">'
    'SecureLogin &nbsp; | &nbsp; '
    'Built for a safer digital world'
    '</div>',
    unsafe_allow_html=True
)