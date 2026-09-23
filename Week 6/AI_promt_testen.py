import streamlit as st
import re


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
# PASSWORD VALIDATION
# ============================================================

def validate_password(password):

    if password == "":
        return False, "Please enter a password."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if not any(character.isupper() for character in password):
        return False, "Password must contain at least one uppercase letter."

    if not any(character.islower() for character in password):
        return False, "Password must contain at least one lowercase letter."

    if not any(character.isdigit() for character in password):
        return False, "Password must contain at least one number."

    special_characters = "!@#$%^&*()_+-=[]{};:,.?"

    if not any(character in special_characters for character in password):
        return False, "Password must contain at least one special character."

    if " " in password:
        return False, "Password cannot contain spaces."

    return True, "Valid password."


# ============================================================
# STREAMLIT SETTINGS
# ============================================================

st.set_page_config(
    page_title="Login System",
    page_icon="🔐",
    layout="centered"
)


# ============================================================
# SESSION STATE
# ============================================================

# Stores the created account
if "account_created" not in st.session_state:
    st.session_state.account_created = False

if "saved_email" not in st.session_state:
    st.session_state.saved_email = ""

if "saved_password" not in st.session_state:
    st.session_state.saved_password = ""

# Keeps track of login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ============================================================
# CREATE ACCOUNT PAGE
# ============================================================

if not st.session_state.account_created:

    st.title("👤 Create Account")

    st.write(
        "Create an account by entering a valid email address "
        "and a strong password."
    )

    st.divider()

    # Email input
    email = st.text_input(
        "Email address",
        placeholder="example@gmail.com"
    )

    # Password input
    password = st.text_input(
        "Password",
        type="password",
        placeholder="Create a password"
    )

    # Repeat password
    repeat_password = st.text_input(
        "Repeat password",
        type="password",
        placeholder="Repeat your password"
    )

    # --------------------------------------------------------
    # PASSWORD REQUIREMENTS
    # --------------------------------------------------------

    with st.expander("🔐 Password requirements"):

        st.write("""
        Your password must:

        - Contain at least 8 characters
        - Contain at least one uppercase letter
        - Contain at least one lowercase letter
        - Contain at least one number
        - Contain at least one special character
        - Not contain spaces
        """)

    # --------------------------------------------------------
    # CREATE ACCOUNT BUTTON
    # --------------------------------------------------------

    if st.button(
        "Create account",
        type="primary",
        use_container_width=True
    ):

        email_valid, email_message = validate_email(email)

        password_valid, password_message = validate_password(password)

        # Check email
        if not email_valid:

            st.error("❌ Invalid email address")
            st.warning(email_message)

        # Check password
        elif not password_valid:

            st.error("❌ Invalid password")
            st.warning(password_message)

        # Check if passwords match
        elif password != repeat_password:

            st.error("❌ Passwords do not match.")

        # Everything is correct
        else:

            st.session_state.saved_email = email.strip()
            st.session_state.saved_password = password
            st.session_state.account_created = True

            st.success("✅ Account successfully created!")

            st.rerun()


# ============================================================
# LOGIN PAGE
# ============================================================

elif not st.session_state.logged_in:

    st.title("🔐 Login")

    st.write("Enter your email address and password to continue.")

    st.divider()

    # Login email
    login_email = st.text_input(
        "Email address",
        placeholder="example@gmail.com"
    )

    # Login password
    login_password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )

    # --------------------------------------------------------
    # LOGIN BUTTON
    # --------------------------------------------------------

    if st.button(
        "Login",
        type="primary",
        use_container_width=True
    ):

        # Check both email and password
        if (
            login_email.strip() == st.session_state.saved_email
            and
            login_password == st.session_state.saved_password
        ):

            st.session_state.logged_in = True

            st.success("✅ Login successful!")

            st.rerun()

        else:

            st.error("❌ Incorrect email address or password.")

    st.divider()

    # Option to create a new account
    if st.button("Create a new account"):

        st.session_state.account_created = False
        st.session_state.saved_email = ""
        st.session_state.saved_password = ""

        st.rerun()


# ============================================================
# LOGGED IN PAGE
# ============================================================

else:

    st.title("🎉 Welcome!")

    st.success("You are successfully logged in.")

    st.write("Logged in as:")

    st.info(st.session_state.saved_email)

    st.divider()

    st.write(
        "You have successfully created an account "
        "and logged into the application."
    )

    # --------------------------------------------------------
    # LOGOUT BUTTON
    # --------------------------------------------------------

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.rerun()