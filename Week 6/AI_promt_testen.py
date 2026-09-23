import streamlit as st
import re


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
# CSS
# ============================================================

st.markdown("""
<style>

/* Complete page */
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
/* Remove Streamlit default header spacing */
.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Main Streamlit header */
header[data-testid="stHeader"] {
    background: transparent;
}

/* --------------------------------------------------
   BRAND
-------------------------------------------------- */

.brand {
    font-size: 22px;
    font-weight: 700;
    color: #102a56;
    margin-bottom: 25px;
}

.brand-light {
    font-weight: 400;
}


/* --------------------------------------------------
   LEFT SIDE
-------------------------------------------------- */

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
    background: #3b82f6;
    border-radius: 10px;
    margin-bottom: 28px;
}

.hero-text {
    color: #60789c;
    font-size: 17px;
    line-height: 1.6;
    max-width: 260px;
}


/* --------------------------------------------------
   CENTER
-------------------------------------------------- */

.lock-icon {
    width: 65px;
    height: 65px;
    margin: 5px auto 15px auto;
    border-radius: 50%;
    background: #e7f0ff;
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
    color: #7185a5;
    font-size: 15px;
    margin-bottom: 25px;
}


/* --------------------------------------------------
   INPUT FIELDS
-------------------------------------------------- */

.stTextInput label {
    color: #172b4d !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

div[data-baseweb="input"] {
    background-color: white !important;
    border: 1px solid #d9e2ef !important;
    border-radius: 10px !important;
    min-height: 47px;
}

div[data-baseweb="input"] input {
    color: #172b4d !important;
}


/* --------------------------------------------------
   PASSWORD REQUIREMENTS
-------------------------------------------------- */

.requirements {
    background: rgba(255, 255, 255, 0.65);
    border: 1px solid #e1e8f2;
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
    color: #71819a;
}

.req-ok {
    color: #26835a;
    font-weight: 500;
}


/* --------------------------------------------------
   BUTTON
-------------------------------------------------- */

.stButton > button {
    width: 100%;
    height: 49px;
    border: none !important;
    border-radius: 10px !important;

    background: linear-gradient(
        90deg,
        #2463d4,
        #3478ea
    ) !important;

    color: white !important;
    font-weight: 650 !important;
    font-size: 15px !important;

    box-shadow: 0 8px 18px rgba(36, 99, 212, 0.15);

    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 24px rgba(36, 99, 212, 0.25);
}


/* --------------------------------------------------
   RIGHT SIDE
-------------------------------------------------- */

.right-title {
    color: #102a56;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 2px;
}

.right-text {
    color: #7185a5;
    font-size: 14px;
    line-height: 1.4;
}

.feature {
    margin-top: 70px;
    margin-bottom: 45px;
}


/* --------------------------------------------------
   FOOTER
-------------------------------------------------- */

.footer-text {
    text-align: center;
    color: #8b9bb5;
    font-size: 12px;
    margin-top: 30px;
    letter-spacing: 0.5px;
}


/* Progress bar */
.stProgress > div > div > div > div {
    background-color: #3478ea;
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


# ============================================================
# BRAND
# ============================================================

st.markdown(
    '<div class="brand">🔒 Secure<span class="brand-light">Login</span></div>',
    unsafe_allow_html=True
)


# ============================================================
# CREATE ACCOUNT
# ============================================================

if not st.session_state.account_created:

    left, center, right = st.columns(
        [1, 1.55, 1],
        gap="large"
    )


    # ========================================================
    # LEFT COLUMN
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
    # CENTER COLUMN
    # ========================================================

    with center:

        st.markdown(
            '<div class="lock-icon">🔐</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="main-title">Create your account</div>',
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
            placeholder="name@example.com"
        )


        # PASSWORD
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a strong password"
        )


        # CONFIRM PASSWORD
        repeat_password = st.text_input(
            "Confirm password",
            type="password",
            placeholder="Enter your password again"
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


        # IMPORTANT:
        # HTML IS ALL ON ONE LINE TO PREVENT STREAMLIT
        # FROM TURNING IT INTO A CODE BLOCK

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

                st.error("The passwords do not match.")

            else:

                st.session_state.saved_email = email.strip()

                st.session_state.saved_password = password

                st.session_state.account_created = True

                st.rerun()


    # ========================================================
    # RIGHT COLUMN
    # ========================================================

    with right:

        st.markdown(
            '<div class="feature">'
            '<div class="right-title">🛡️ &nbsp; Secure</div>'
            '<div class="right-text">'
            'Your information is protected.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="feature">'
            '<div class="right-title">👤 &nbsp; Private</div>'
            '<div class="right-text">'
            'We never share your data.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="feature">'
            '<div class="right-title">⚡ &nbsp; Simple</div>'
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
            '<div class="main-title">Welcome back</div>',
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
            "Log in  →",
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

                st.rerun()

            else:

                st.error(
                    "Incorrect email address or password."
                )


# ============================================================
# LOGGED IN
# ============================================================

else:

    left_space, dashboard, right_space = st.columns(
        [1, 1.2, 1]
    )

    with dashboard:

        st.markdown(
            '<div class="lock-icon">✓</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="main-title">'
            'Welcome!'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="main-subtitle">'
            'You are securely logged in'
            '</div>',
            unsafe_allow_html=True
        )

        st.success(
            "✓ Authentication successful"
        )

        st.info(
            "Logged in as: "
            + st.session_state.saved_email
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Email status",
                "Valid"
            )

        with col2:

            st.metric(
                "Password",
                "Strong"
            )

        if st.button(
            "Log out",
            use_container_width=True
        ):

            st.session_state.logged_in = False

            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer-text">'
    'SecureLogin &nbsp; | &nbsp; Built for a safer digital world'
    '</div>',
    unsafe_allow_html=True
)