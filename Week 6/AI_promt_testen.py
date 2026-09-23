import streamlit as st
import re


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="SecureLogin",
    page_icon="🔐",
    layout="centered"
)


# ============================================================
# CSS - DESIGN
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: linear-gradient(
            135deg,
            #f5f7fa 0%,
            #e8edf5 100%
        );
    }

    /* Main content width */
    .block-container {
        max-width: 650px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    /* Titles */
    h1 {
        text-align: center;
        color: #1f2937;
        font-weight: 700;
    }

    h3 {
        color: #374151;
    }

    /* Input fields */
    div[data-baseweb="input"] {
        border-radius: 10px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        height: 48px;
        font-weight: 600;
        font-size: 16px;
        transition: 0.3s;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
    }

    /* Login logo */
    .logo {
        text-align: center;
        font-size: 55px;
        margin-bottom: -10px;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 17px;
        margin-bottom: 25px;
    }

    /* Requirement text */
    .requirement {
        font-size: 14px;
        margin: 3px 0;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 12px;
        margin-top: 40px;
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

    checks = {
        "8 characters": len(password) >= 8,

        "Uppercase letter":
            any(character.isupper() for character in password),

        "Lowercase letter":
            any(character.islower() for character in password),

        "Number":
            any(character.isdigit() for character in password),

        "Special character":
            any(character in special_characters for character in password),

        "No spaces":
            " " not in password
    }

    return checks


# ============================================================
# PASSWORD VALIDATION
# ============================================================

def validate_password(password):

    if password == "":
        return False, "Please enter a password."

    checks = password_checks(password)

    if not checks["8 characters"]:
        return False, "Password must contain at least 8 characters."

    if not checks["Uppercase letter"]:
        return False, "Password must contain at least one uppercase letter."

    if not checks["Lowercase letter"]:
        return False, "Password must contain at least one lowercase letter."

    if not checks["Number"]:
        return False, "Password must contain at least one number."

    if not checks["Special character"]:
        return False, "Password must contain at least one special character."

    if not checks["No spaces"]:
        return False, "Password cannot contain spaces."

    return True, "Strong password."


# ============================================================
# PASSWORD STRENGTH
# ============================================================

def password_strength(password):

    if password == "":
        return 0, "No password entered"

    checks = password_checks(password)

    score = sum(checks.values())

    if score <= 2:
        return 0.25, "Weak"

    elif score <= 4:
        return 0.50, "Medium"

    elif score == 5:
        return 0.75, "Good"

    else:
        return 1.0, "Strong"


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
# CREATE ACCOUNT
# ============================================================

if not st.session_state.account_created:

    st.markdown(
        '<div class="logo">🔐</div>',
        unsafe_allow_html=True
    )

    st.title("Create your account")

    st.markdown(
        '<div class="subtitle">'
        'Create a secure account to continue'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("### Account details")

    # --------------------------------------------------------
    # EMAIL
    # --------------------------------------------------------

    email = st.text_input(
        "Email address",
        placeholder="name@example.com",
        key="register_email"
    )

    # Live email validation
    if email:

        email_valid, email_message = validate_email(email)

        if email_valid:
            st.success("✓ Email address looks good")

        else:
            st.warning(email_message)

    # --------------------------------------------------------
    # PASSWORD
    # --------------------------------------------------------

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Create a strong password",
        key="register_password"
    )

    # --------------------------------------------------------
    # LIVE PASSWORD CHECK
    # --------------------------------------------------------

    if password:

        strength_value, strength_text = password_strength(password)

        st.write(f"**Password strength: {strength_text}**")

        st.progress(strength_value)

        checks = password_checks(password)

        col1, col2 = st.columns(2)

        requirements = list(checks.items())

        with col1:

            for requirement, passed in requirements[:3]:

                if passed:
                    st.markdown(f"🟢 {requirement}")
                else:
                    st.markdown(f"⚪ {requirement}")

        with col2:

            for requirement, passed in requirements[3:]:

                if passed:
                    st.markdown(f"🟢 {requirement}")
                else:
                    st.markdown(f"⚪ {requirement}")

    # --------------------------------------------------------
    # CONFIRM PASSWORD
    # --------------------------------------------------------

    repeat_password = st.text_input(
        "Confirm password",
        type="password",
        placeholder="Enter your password again",
        key="repeat_password"
    )

    # Live password match
    if repeat_password:

        if password == repeat_password:
            st.success("✓ Passwords match")

        else:
            st.warning("Passwords do not match yet.")

    st.write("")

    # --------------------------------------------------------
    # CREATE BUTTON
    # --------------------------------------------------------

    if st.button(
        "Create Account",
        type="primary",
        use_container_width=True
    ):

        email_valid, email_message = validate_email(email)

        password_valid, password_message = validate_password(password)

        if not email_valid:

            st.error("❌ Invalid email address")
            st.warning(email_message)

        elif not password_valid:

            st.error("❌ Password does not meet the requirements")
            st.warning(password_message)

        elif password != repeat_password:

            st.error("❌ The passwords do not match.")

        else:

            st.session_state.saved_email = email.strip()
            st.session_state.saved_password = password
            st.session_state.account_created = True

            st.rerun()

    st.markdown(
        '<div class="footer">'
        'SecureLogin • Data Science 5'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# LOGIN
# ============================================================

elif not st.session_state.logged_in:

    st.markdown(
        '<div class="logo">🔐</div>',
        unsafe_allow_html=True
    )

    st.title("Welcome back")

    st.markdown(
        '<div class="subtitle">'
        'Sign in to your account'
        '</div>',
        unsafe_allow_html=True
    )

    # Account created message
    st.success(
        "✓ Your account has been created successfully. "
        "You can now log in."
    )

    st.write("### Login")

    # --------------------------------------------------------
    # LOGIN EMAIL
    # --------------------------------------------------------

    login_email = st.text_input(
        "Email address",
        placeholder="name@example.com",
        key="login_email"
    )

    # --------------------------------------------------------
    # LOGIN PASSWORD
    # --------------------------------------------------------

    login_password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password",
        key="login_password"
    )

    st.write("")

    # --------------------------------------------------------
    # LOGIN BUTTON
    # --------------------------------------------------------

    if st.button(
        "Login",
        type="primary",
        use_container_width=True
    ):

        if (
            login_email.strip() == st.session_state.saved_email
            and
            login_password == st.session_state.saved_password
        ):

            st.session_state.logged_in = True

            st.rerun()

        else:

            st.error(
                "❌ Incorrect email address or password. "
                "Please try again."
            )

    # --------------------------------------------------------
    # NEW ACCOUNT
    # --------------------------------------------------------

    st.divider()

    st.markdown(
        "<p style='text-align:center;'>"
        "Want to create a different account?"
        "</p>",
        unsafe_allow_html=True
    )

    if st.button(
        "Create new account",
        use_container_width=True
    ):

        st.session_state.account_created = False
        st.session_state.saved_email = ""
        st.session_state.saved_password = ""

        st.rerun()

    st.markdown(
        '<div class="footer">'
        '🔒 Your login information is protected'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# DASHBOARD
# ============================================================

else:

    st.markdown(
        '<div class="logo">🎉</div>',
        unsafe_allow_html=True
    )

    st.title("You're logged in!")

    st.markdown(
        '<div class="subtitle">'
        'Welcome to your account'
        '</div>',
        unsafe_allow_html=True
    )

    st.success("✓ Authentication successful")

    st.write("### 👤 Account")

    st.info(
        f"**Email address:**  \n"
        f"{st.session_state.saved_email}"
    )

    st.write("### 🔐 Security status")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Email",
            value="Valid"
        )

    with col2:
        st.metric(
            label="Password",
            value="Strong"
        )

    st.divider()

    st.write(
        "Your email address and password have successfully "
        "passed all validation checks."
    )

    st.write("")

    # --------------------------------------------------------
    # LOGOUT
    # --------------------------------------------------------

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.rerun()

    st.markdown(
        '<div class="footer">'
        'SecureLogin • Data Science 5'
        '</div>',
        unsafe_allow_html=True
    )