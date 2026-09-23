import streamlit as st
import re


# --------------------------------------------------
# EMAIL VALIDATION FUNCTION
# --------------------------------------------------

def validate_email(email):
    """
    Checks if an email address is valid.

    Returns:
        True, message  -> if email is valid
        False, message -> if email is invalid
    """

    # Remove spaces at beginning and end
    email = email.strip()

    # Check if email is empty
    if email == "":
        return False, "Please enter an email address."

    # Check maximum length
    if len(email) > 254:
        return False, "Email address is too long."

    # Check for spaces
    if " " in email:
        return False, "Email cannot contain spaces."

    # Check if there is exactly one @
    if email.count("@") != 1:
        return False, "Email must contain exactly one @ symbol."

    # Split email into username and domain
    username, domain = email.split("@")

    # Check username
    if username == "":
        return False, "Username cannot be empty."

    # Check domain
    if domain == "":
        return False, "Domain cannot be empty."

    # Check username length
    if len(username) > 64:
        return False, "Username is too long."

    # Username cannot start or end with a dot
    if username.startswith(".") or username.endswith("."):
        return False, "Username cannot start or end with a dot."

    # Domain cannot start or end with a dot
    if domain.startswith(".") or domain.endswith("."):
        return False, "Domain cannot start or end with a dot."

    # No consecutive dots
    if ".." in email:
        return False, "Email cannot contain consecutive dots."

    # Domain must contain a dot
    if "." not in domain:
        return False, "Domain must contain a dot."

    # Split domain extension
    domain_name, extension = domain.rsplit(".", 1)

    if domain_name == "":
        return False, "Domain name cannot be empty."

    # Extension must have at least 2 characters
    if len(extension) < 2:
        return False, "Domain extension must contain at least 2 characters."

    # Check username characters
    username_pattern = r"^[A-Za-z0-9._%+-]+$"

    if not re.match(username_pattern, username):
        return False, "Username contains invalid characters."

    # Check domain characters
    domain_pattern = r"^[A-Za-z0-9.-]+$"

    if not re.match(domain_pattern, domain):
        return False, "Domain contains invalid characters."

    # Everything passed
    return True, "This is a valid email address."


# --------------------------------------------------
# STREAMLIT PAGE
# --------------------------------------------------

st.set_page_config(
    page_title="Email Validator",
    page_icon="📧",
    layout="centered"
)


# Title
st.title("📧 Email Validator")

st.write(
    "Enter an email address below and the program will check "
    "whether the email address has a valid format."
)

st.divider()


# --------------------------------------------------
# EMAIL INPUT
# --------------------------------------------------

email = st.text_input(
    "Email address",
    placeholder="example@gmail.com"
)


# --------------------------------------------------
# VALIDATE BUTTON
# --------------------------------------------------

if st.button("Validate email", type="primary", use_container_width=True):

    valid, message = validate_email(email)

    if valid:

        st.success("✅ Valid email address!")

        st.write("The entered email address is:")

        st.code(email)

        st.balloons()

    else:

        st.error("❌ Invalid email address")

        st.warning(message)

        st.write("Please correct the email address and try again.")


# --------------------------------------------------
# INFORMATION
# --------------------------------------------------

st.divider()

with st.expander("What does the validator check?"):

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


st.caption("Data Science 5 - Email Validation")