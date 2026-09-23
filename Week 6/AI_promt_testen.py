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

BASE_DIR = Path(__file__).resolve().parent
ELMO_IMAGE = BASE_DIR / "elmo.png"


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

/* BACKGROUND */

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


/* PAGE */

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}


/* BRAND */

.brand {
    font-size: 22px;
    font-weight: 700;
    color: #102a56;
    margin-bottom: 25px;
}

.brand-light {
    font-weight: 400;
}


/* CREATE ACCOUNT LEFT SIDE */

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


/* TITLES */

.lock-icon {
    width: 65px;
    height: 65px;

    margin:
        5px auto
        15px auto;

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


/* INPUT */

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


/* PASSWORD REQUIREMENTS */

.requirements {
    background: rgba(255,255,255,0.70);

    border:
        1px solid
        rgba(255,255,255,0.60);

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


/* BUTTONS */

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

    transition: all 0.2s ease;
}

.stButton > button:hover {

    transform: translateY(-1px);

    box-shadow:
        0 10px 24px
        rgba(36,99,212,0.30);
}


/* ALERT */

div[data-testid="stAlert"] p {
    color: #14532d !important;
    font-weight: 700 !important;
}


/* RIGHT SIDE */

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


/* SHOP */

.shop-title {
    color: #102a56;
    font-size: 42px;
    font-weight: 800;
}

.shop-subtitle {
    color: #405d83;
    font-size: 17px;
}


/* FOOTER */

.footer-text {
    text-align: center;
    color: #657b9c;
    font-size: 12px;
    margin-top: 30px;
    letter-spacing: 0.5px;
}


/* PROGRESS */

.stProgress > div > div > div > div {
    background-color: #2563eb;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCTIONS
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


def validate_password(password):

    if password == "":
        return False, "Please enter a password."

    checks = password_checks(password)

    for requirement, passed in checks.items():

        if not passed:
            return False, "Missing requirement: " + requirement

    return True, "Valid password."


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

# IMPORTANT:
# This remembers which shop page the user is on
if "shop_page" not in st.session_state:
    st.session_state.shop_page = "Home"

if "order_total" not in st.session_state:
    st.session_state.order_total = 0

if "order_items" not in st.session_state:
    st.session_state.order_items = []


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


    # LEFT
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


    # CENTER
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


        email = st.text_input(
            "Email address",
            placeholder="name@example.com",
            key="register_email"
        )


        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a strong password",
            key="register_password"
        )


        repeat_password = st.text_input(
            "Confirm password",
            type="password",
            placeholder="Enter your password again",
            key="repeat_password"
        )


        # PASSWORD REQUIREMENTS
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
            'Password requirements'
            '</div>'
            + requirement_html +
            '</div>',
            unsafe_allow_html=True
        )


        # PASSWORD STRENGTH
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


        # CREATE ACCOUNT
        if st.button(
            "Create Account →",
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
                    "The passwords do not match."
                )

            else:

                st.session_state.saved_email = email.strip()
                st.session_state.saved_password = password
                st.session_state.account_created = True

                st.rerun()


    # RIGHT
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

        # BACK TO CREATE ACCOUNT
        if st.button(
            "← Back to create account",
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


        login_email = st.text_input(
            "Email address",
            placeholder="name@example.com",
            key="login_email"
        )


        login_password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )


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

                # Start on Home
                st.session_state.shop_page = "Home"

                st.rerun()

            else:

                st.error(
                    "Incorrect email address or password."
                )


# ============================================================
# SHOP
# ============================================================

else:

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
            "description": "Vanilla ice cream with cookie pieces",
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

        if ELMO_IMAGE.exists():

            st.image(
                str(ELMO_IMAGE),
                width=120
            )


        st.markdown("## 🍦 Elmo's")
        st.caption("Ice Cream Shop")

        st.divider()

        st.markdown("### Navigation")


        # ----------------------------------------------------
        # HOME
        # ----------------------------------------------------

        if st.button(
            "🏠 Home",
            use_container_width=True
        ):

            st.session_state.shop_page = "Home"
            st.rerun()


        # ----------------------------------------------------
        # MENU
        # ----------------------------------------------------

        if st.button(
            "🍦 Menu + Prices",
            use_container_width=True
        ):

            st.session_state.shop_page = "Menu"
            st.rerun()


        # ----------------------------------------------------
        # CART
        # ----------------------------------------------------

        if st.button(
            f"🛒 Shopping Cart ({len(st.session_state.cart)})",
            use_container_width=True
        ):

            st.session_state.shop_page = "Cart"
            st.rerun()


        st.divider()

        st.caption("Logged in as:")

        st.write(
            st.session_state.saved_email
        )

        st.write("")


        # ----------------------------------------------------
        # LOG OUT
        # ----------------------------------------------------

        if st.button(
            "🚪 Log out",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.shop_page = "Home"

            st.rerun()


    # ========================================================
    # HEADER
    # ========================================================

    header1, header2 = st.columns(
        [5, 1]
    )


    with header1:

        st.markdown(
            "# 🍦 Elmo's Ice Cream Shop"
        )

        st.write(
            "The coolest ice cream in town!"
        )


    with header2:

        st.metric(
            "🛒 Cart",
            len(st.session_state.cart)
        )


    st.divider()


    # ========================================================
    # HOME
    # ========================================================

    if st.session_state.shop_page == "Home":

        # BACK BUTTON
        if st.button(
            "← Back to login",
            key="home_back"
        ):

            st.session_state.logged_in = False

            st.rerun()


        st.success(
            "👋 Welcome to Elmo's Ice Cream Shop!"
        )

        st.caption(
            "You are logged in as "
            + st.session_state.saved_email
        )


        st.write("")


        # ELMO + TEXT
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

                st.error(
                    "Elmo image could not be found."
                )


        with text_col:

            st.markdown("## ❤️ Welcome!")

            st.write(
                "Welcome to **Elmo's Ice Cream Shop!**"
            )

            st.write(
                "Here you can discover our delicious "
                "collection of fictional ice creams."
            )

            st.write(
                "Visit **Menu + Prices** to see all our "
                "flavors and add your favorites to your "
                "shopping cart."
            )

            st.write(
                "When you're finished, open your "
                "**Shopping Cart** to see your order "
                "and total price."
            )

            st.info(
                "🍓 Elmo's favorite is the Strawberry Special!"
            )


        st.write("")
        st.divider()


        # TODAY'S SPECIAL
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
                "Today's Special"
                "</h2>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<p style='text-align:center; font-size:18px;'>"
                "Strawberry Special — only €2.95"
                "</p>",
                unsafe_allow_html=True
            )


        # NEXT BUTTON
        st.write("")

        if st.button(
            "View Menu →",
            type="primary",
            use_container_width=True
        ):

            st.session_state.shop_page = "Menu"

            st.rerun()


    # ========================================================
    # MENU + PRICES
    # ========================================================

    elif st.session_state.shop_page == "Menu":

        # BACK BUTTON
        if st.button(
            "← Back to Home",
            key="menu_back"
        ):

            st.session_state.shop_page = "Home"

            st.rerun()


        st.markdown("# 🍦 Menu + Prices")

        st.write(
            "Choose your favorite ice cream and "
            "add it to your shopping cart."
        )

        st.write("")


        # ====================================================
        # PRODUCT DISPLAY FUNCTION
        # ====================================================

        def show_product(
            name,
            button_key
        ):

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


            if st.button(
                "Add to cart 🛒",
                key=button_key,
                use_container_width=True
            ):

                st.session_state.cart.append(
                    name
                )

                # IMPORTANT:
                # Stay on menu after rerun
                st.session_state.shop_page = "Menu"

                st.toast(
                    product["emoji"]
                    + " "
                    + name
                    + " added!"
                )

                st.rerun()


        # FIRST ROW
        col1, col2, col3 = st.columns(
            3,
            gap="medium"
        )

        with col1:
            show_product(
                "Strawberry",
                "add_strawberry"
            )

        with col2:
            show_product(
                "Chocolate",
                "add_chocolate"
            )

        with col3:
            show_product(
                "Cookie Crunch",
                "add_cookie"
            )


        st.write("")
        st.write("")


        # SECOND ROW
        col4, col5, col6 = st.columns(
            3,
            gap="medium"
        )

        with col4:
            show_product(
                "Rainbow",
                "add_rainbow"
            )

        with col5:
            show_product(
                "Vanilla Dream",
                "add_vanilla"
            )

        with col6:
            show_product(
                "Cherry Sundae",
                "add_cherry"
            )


        st.write("")


        # GO TO CART
        if st.button(
            f"Go to Shopping Cart ({len(st.session_state.cart)}) →",
            type="primary",
            use_container_width=True
        ):

            st.session_state.shop_page = "Cart"

            st.rerun()


    # ========================================================
    # SHOPPING CART
    # ========================================================

    elif st.session_state.shop_page == "Cart":

        # BACK BUTTON
        if st.button(
            "← Back to Menu + Prices",
            key="cart_back"
        ):

            st.session_state.shop_page = "Menu"

            st.rerun()


        st.markdown("# 🛒 Shopping Cart")

        st.write("")


        # ====================================================
        # EMPTY CART
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
                    "Your cart is empty"
                    "</h2>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    "<p style='"
                    "text-align:center;"
                    "font-size:17px;"
                    "'>"
                    "Visit Menu + Prices to add "
                    "some delicious ice cream!"
                    "</p>",
                    unsafe_allow_html=True
                )


        # ====================================================
        # CART WITH ITEMS
        # ====================================================

        else:

            cart_counts = {}


            for item in st.session_state.cart:

                if item in cart_counts:

                    cart_counts[item] += 1

                else:

                    cart_counts[item] = 1


            total_price = 0


            # PRODUCT ROWS
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
                        "Amount",
                        quantity
                    )


                with price_col:

                    st.metric(
                        "Subtotal",
                        f"€{subtotal:.2f}"
                    )


                with remove_col:

                    st.write("")

                    if st.button(
                        "➖",
                        key="remove_" + product_name,
                        help="Remove one"
                    ):

                        st.session_state.cart.remove(
                            product_name
                        )

                        # Stay in cart
                        st.session_state.shop_page = "Cart"

                        st.rerun()


                st.divider()


            # =================================================
            # TOTAL
            # =================================================

            total_left, total_right = st.columns(
                [4, 1.5]
            )


            with total_right:

                st.markdown("### Total")

                st.markdown(
                    f"# €{total_price:.2f}"
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

                    st.session_state.shop_page = "Cart"

                    st.rerun()


            with order_col:

                if st.button(
                    "🍦 Place fake order",
                    type="primary",
                    use_container_width=True
                ):

                    # Save order before clearing cart
                    st.session_state.order_total = total_price

                    st.session_state.order_items = (
                        st.session_state.cart.copy()
                    )

                    # Empty cart
                    st.session_state.cart = []

                    # Go to confirmation page
                    st.session_state.shop_page = "Confirmation"

                    st.rerun()


    # ========================================================
    # ORDER CONFIRMATION
    # ========================================================

    elif st.session_state.shop_page == "Confirmation":

        # Balloons when arriving here
        st.balloons()


        # BACK BUTTON
        if st.button(
            "← Back to Shopping Cart",
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
                "Order received!"
                "</h1>",
                unsafe_allow_html=True
            )


            st.markdown(
                "<p style='"
                "text-align:center;"
                "font-size:19px;"
                "'>"
                "Thank you for your order!"
                "</p>",
                unsafe_allow_html=True
            )


            st.success(
                "🍦 Your fake order was successfully received!"
            )


            # ================================================
            # ORDER SUMMARY
            # ================================================

            st.markdown("### 🧾 Order summary")


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
                "## Total: €"
                + f"{st.session_state.order_total:.2f}"
            )


            st.info(
                "This is a demonstration order. "
                "No real purchase or payment has been made."
            )


            # ================================================
            # NEW ORDER
            # ================================================

            if st.button(
                "🍦 Start a new order",
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
    'SecureLogin &nbsp; | &nbsp; '
    'Built for a safer digital world'
    '</div>',
    unsafe_allow_html=True
)