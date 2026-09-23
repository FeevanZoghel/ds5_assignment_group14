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

/* ----------------------------------------------------------
   GENERAL PAGE
---------------------------------------------------------- */

.stApp {
    background:
        radial-gradient(circle at 15% 20%,
            rgba(255,255,255,0.95) 0%,
            rgba(255,255,255,0.15) 25%,
            transparent 45%),

        radial-gradient(circle at 85% 15%,
            rgba(255,255,255,0.8) 0%,
            transparent 35%),

        linear-gradient(
            135deg,
            #f8fbff 0%,
            #e9f2ff 35%,
            #dcecff 65%,
            #c5ddfb 100%
        );

    min-height: 100vh;
}


/* Hide Streamlit menu/footer */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* Main page width */
.block-container {
    max-width: 1450px;
    padding-top: 25px;
    padding-bottom: 30px;
}


/* ----------------------------------------------------------
   HEADER
---------------------------------------------------------- */

.logo-header {
    font-size: 25px;
    font-weight: 700;
    color: #102a56;
    margin-bottom: 25px;
}

.logo-light {
    font-weight: 400;
}


/* ----------------------------------------------------------
   LEFT SIDE
---------------------------------------------------------- */

.left-container {
    padding-top: 90px;
    padding-right: 40px;
}

.big-text {
    font-family: Georgia, serif;
    font-size: 58px;
    line-height: 1.03;
    color: #102a56;
    margin-bottom: 25px;
}

.blue-line {
    width: 45px;
    height: 3px;
    background: #4d8cff;
    margin-top: 25px;
    margin-bottom: 30px;
}

.left-description {
    color: #526b91;
    font-size: 18px;
    line-height: 1.6;
    max-width: 260px;
}


/* ----------------------------------------------------------
   CENTER CARD
---------------------------------------------------------- */

.login-card {
    background: rgba(255,255,255,0.94);

    border-radius: 24px;

    padding:
        28px
        36px
        32px
        36px;

    box-shadow:
        0px 20px 60px rgba(39, 73, 125, 0.15);

    border:
        1px solid rgba(255,255,255,0.9);

    backdrop-filter: blur(15px);

    margin-top: 10px;
}


/* Lock circle */
.lock-circle {
    width: 68px;
    height: 68px;

    margin:
        0 auto
        10px auto;

    border-radius: 50%;

    background:
        #e8f1ff;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 31px;
}


/* Titles */
.card-title {
    text-align: center;

    font-size: 30px;

    font-weight: 750;

    color: #10234b;

    margin-bottom: 3px;
}

.card-subtitle {
    text-align: center;

    color: #6e82a3;

    font-size: 15px;

    margin-bottom: 20px;
}


/* ----------------------------------------------------------
   STREAMLIT INPUTS
---------------------------------------------------------- */

.stTextInput label {
    font-weight: 600 !important;
    color: #15294e !important;
}


/* Input box */
div[data-baseweb="input"] {

    background: #ffffff;

    border-radius: 11px;

    border:
        1px solid #d6dfec;

    min-height: 48px;
}


/* Input text */
div[data-baseweb="input"] input {

    color: #172b4d;

    font-size: 15px;
}


/* ----------------------------------------------------------
   BUTTON
---------------------------------------------------------- */

.stButton > button {

    width: 100%;

    min-height: 50px;

    border: none;

    border-radius: 12px;

    background:
        linear-gradient(
            90deg,
            #2864d7,
            #3478e9
        );

    color: white;

    font-size: 16px;

    font-weight: 650;

    box-shadow:
        0 8px 20px rgba(41, 101, 215, 0.18);

    transition:
        transform 0.15s ease,
        box-shadow 0.15s ease;
}


.stButton > button:hover {

    transform: translateY(-1px);

    color: white;

    border: none;

    box-shadow:
        0 10px 25px rgba(41, 101, 215, 0.28);
}


/* ----------------------------------------------------------
   PASSWORD REQUIREMENTS
---------------------------------------------------------- */

.password-box {

    background: #f4f7fc;

    border-radius: 14px;

    padding:
        15px
        18px;

    margin:
        10px 0
        18px 0;

    border:
        1px solid #e5ebf4;
}


.requirement-title {

    font-weight: 700;

    color: #14294f;

    margin-bottom: 8px;
}


.requirement {

    color: #657999;

    font-size: 13px;

    margin: 4px 0;
}


.good {
    color: #24794c;
}


.bad {
    color: #8290a7;
}


/* ----------------------------------------------------------
   RIGHT SIDE
---------------------------------------------------------- */

.right-container {

    padding-top: 115px;

    padding-left: 40px;
}


.security-item {

    display: flex;

    align-items: center;

    margin-bottom: 38px;
}


.security-icon {

    width: 58px;

    height: 58px;

    min-width: 58px;

    border-radius: 50%;

    background: rgba(220,233,252,0.9);

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 25px;

    margin-right: 18px;
}


.security-title {

    color: #102a56;

    font-size: 17px;

    font-weight: 700;
}


.security-description {

    color: #62799d;

    font-size: 14px;

    line-height: 1.35;

    margin-top: 3px;
}


/* ----------------------------------------------------------
   FOOTER
---------------------------------------------------------- */

.page-footer {

    text-align: center;

    color: #7c8fac;

    font-size: 12px;

    margin-top: 30px;

    letter-spacing: 1px;
}


/* ----------------------------------------------------------
   RESPONSIVE
---------------------------------------------------------- */

@media (max-width: 900px) {

    .big-text {
        font-size: 40px;
    }

    .left-container {
        padding-top: 20px;
    }

    .right-container {
        padding-top: 20px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# VALIDATE EMAIL
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
            any(char.isupper() for char in password),

        "One lowercase letter (a-z)":
            any(char.islower() for char in password),

        "One number (0-9)":
            any(char.isdigit() for char in password),

        "One special character":
            any(char in special_characters for char in password),

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
            return False, f"Password requirement not met: {requirement}"

    return True, "Valid password."


# ============================================================
# PASSWORD STRENGTH
# ============================================================

def password_strength(password):

    if password == "":
        return 0

    checks = password_checks(password)

    passed = sum(checks.values())

    return passed / len(checks)


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
# HEADER
# ============================================================

st.markdown(
    """
    <div class="logo-header">
        🔒 Secure<span class="logo-light">Login</span>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CREATE ACCOUNT PAGE
# ============================================================

if not st.session_state.account_created:

    left, center, right = st.columns(
        [1.0, 1.7, 1.0],
        gap="large"
    )


    # ========================================================
    # LEFT
    # ========================================================

    with left:

        st.markdown("""
        <div class="left-container">

            <div class="big-text">
                A safer<br>
                brighter<br>
                tomorrow
            </div>

            <div class="blue-line"></div>

            <div class="left-description">

                Create your account
                and take the first step
                towards a more secure
                digital experience.

            </div>

        </div>
        """, unsafe_allow_html=True)


    # ========================================================
    # CENTER
    # ========================================================

    with center:

        st.markdown(
            '<div class="lock-circle">🔒</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="card-title">'
            'Create your account'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="card-subtitle">'
            'Create a secure account to continue'
            '</div>',
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # EMAIL
        # ----------------------------------------------------

        email = st.text_input(
            "Email address",
            placeholder="name@example.com",
            key="register_email"
        )


        # ----------------------------------------------------
        # PASSWORD
        # ----------------------------------------------------

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a strong password",
            key="register_password"
        )


        # ----------------------------------------------------
        # CONFIRM PASSWORD
        # ----------------------------------------------------

        repeat_password = st.text_input(
            "Confirm password",
            type="password",
            placeholder="Enter your password again",
            key="repeat_password"
        )


        # ----------------------------------------------------
        # REQUIREMENTS
        # ----------------------------------------------------

        checks = password_checks(password)

        requirements = ""

        for requirement, passed in checks.items():

            if passed:

                requirements += (
                    f'<div class="requirement good">'
                    f'✓ {requirement}'
                    f'</div>'
                )

            else:

                requirements += (
                    f'<div class="requirement bad">'
                    f'○ {requirement}'
                    f'</div>'
                )


        st.markdown(
            f"""
            <div class="password-box">

                <div class="requirement-title">
                    Password requirements
                </div>

                {requirements}

            </div>
            """,
            unsafe_allow_html=True
        )


        # Password strength
        if password:

            strength = password_strength(password)

            st.caption("Password strength")

            st.progress(strength)


        # ----------------------------------------------------
        # CREATE ACCOUNT
        # ----------------------------------------------------

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
    # RIGHT
    # ========================================================

    with right:

        st.markdown("""
        <div class="right-container">

            <div class="security-item">

                <div class="security-icon">
                    🛡️
                </div>

                <div>

                    <div class="security-title">
                        Secure
                    </div>

                    <div class="security-description">
                        Your information<br>
                        is protected
                    </div>

                </div>

            </div>


            <div class="security-item">

                <div class="security-icon">
                    👥
                </div>

                <div>

                    <div class="security-title">
                        Private
                    </div>

                    <div class="security-description">
                        We never share<br>
                        your data
                    </div>

                </div>

            </div>


            <div class="security-item">

                <div class="security-icon">
                    ⚡
                </div>

                <div>

                    <div class="security-title">
                        Simple
                    </div>

                    <div class="security-description">
                        Fast and easy<br>
                        to use
                    </div>

                </div>

            </div>

        </div>
        """, unsafe_allow_html=True)


# ============================================================
# LOGIN PAGE
# ============================================================

elif not st.session_state.logged_in:

    empty_left, login_column, empty_right = st.columns(
        [1, 1.3, 1]
    )

    with login_column:

        st.markdown(
            '<div class="lock-circle">🔒</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="card-title">'
            'Welcome back'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="card-subtitle">'
            'Sign in to your SecureLogin account'
            '</div>',
            unsafe_allow_html=True
        )

        st.success(
            "✓ Your account was created successfully."
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

        st.write("")

        if st.button(
            "Create a different account",
            use_container_width=True
        ):

            st.session_state.account_created = False
            st.session_state.saved_email = ""
            st.session_state.saved_password = ""

            st.rerun()


# ============================================================
# LOGGED IN PAGE
# ============================================================

else:

    empty_left, dashboard, empty_right = st.columns(
        [1, 1.3, 1]
    )

    with dashboard:

        st.markdown(
            '<div class="lock-circle">✓</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="card-title">'
            'Welcome!'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="card-subtitle">'
            'You are securely logged in'
            '</div>',
            unsafe_allow_html=True
        )

        st.success(
            "✓ Authentication successful"
        )

        st.info(
            f"Logged in as: "
            f"**{st.session_state.saved_email}**"
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

        st.write("")

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
    """
    <div class="page-footer">
        SecureLogin &nbsp; | &nbsp;
        Built for a safer digital world
    </div>
    """,
    unsafe_allow_html=True
)