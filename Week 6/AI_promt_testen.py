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
# STREAMLIT PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Data Validator",
    page_icon="🔍",
    layout="centered"
)


# ============================================================
# TITLE
# ============================================================

st.title("🔍 Data Validator")

st.write(
    "This application can validate an email address "
    "or check the strength of a password."
)

st.divider()


# ============================================================
# MENU
# ============================================================

option = st.radio(
    "Choose what you want to validate:",
    ["📧 Email address", "🔐 Password"],
    horizontal=True
)

st.divider()


# ============================================================
# EMAIL VALIDATOR
# ============================================================

if option == "📧 Email address":

    st.header("📧 Email Validator")

    st.write(
        "Enter an email address below. The program will check "
        "whether the email address has a valid format."
    )

    email = st.text_input(
        "Email address",
        placeholder="example@gmail.com"
    )

    if st.button(
        "Validate email",
        type="primary",
        use_container_width=True
    ):

        valid, message = validate_email(email)

        if valid:

            st.success("✅ Valid email address!")

            st.write("The entered email address is:")

            st.code(email)

            st.balloons()

        else:

            st.error("❌ Invalid email address")

            st.warning(message)

            st.write(
                "Please correct the email address and try again."
            )

    # Explanation
    with st.expander("What does the email validator check?"):

        st.write("""
        The validator checks whether:

        - The email contains exactly one @ symbol
        - The username is valid
        - The domain is valid
        - The domain contains a dot
        - There are no spaces
        - There are no consecutive dots
        - The domain extension contains at least 2 characters
        - Only valid characters are used
        """)


# ============================================================
# PASSWORD VALIDATOR
# ============================================================

elif option == "🔐 Password":

    st.header("🔐 Password Validator")

    st.write(
        "Enter a password below. The program will check "
        "whether the password meets all requirements."
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )

    if st.button(
        "Validate password",
        type="primary",
        use_container_width=True
    ):

        valid, message = validate_password(password)

        if valid:

            st.success("✅ Strong password!")

            st.write(
                "Your password meets all the requirements."
            )

            st.balloons()

        else:

            st.error("❌ Invalid password")

            st.warning(message)

            st.write(
                "Please change your password and try again."
            )

    # Explanation
    with st.expander("What does the password validator check?"):

        st.write("""
        Your password must:

        - Contain at least 8 characters
        - Contain at least one uppercase letter
        - Contain at least one lowercase letter
        - Contain at least one number
        - Contain at least one special character
        - Not contain spaces
        """)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption("Data Science 5 - Validation Application")