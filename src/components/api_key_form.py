"""
API key input form component for the Healthcare Database Request Assistant.
This component is displayed when the API key is not found in the environment variables.
"""

import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv, set_key
from src.utils.api_validator import validate_api_key


def render_api_key_form():
    """
    Render a form to collect the Google API key from the user.

    Returns:
        bool: True if the API key is now available, False otherwise
    """
    st.markdown("<h1 class='main-header'>Healthcare Database Request Assistant 🏥</h1>", unsafe_allow_html=True)

    st.warning("⚠️ Google API Key Not Found")

    st.markdown("""
    ### API Key Required

    This application requires a Google API key to function. The key is used to access the Gemini AI model
    for processing your database requests.

    You can obtain a Google API key by:
    1. Going to the [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. Creating or signing in to your Google account
    3. Creating a new API key
    """)

    # Create a form for the API key
    with st.form("api_key_form"):
        api_key = st.text_input("Enter your Google API Key:", type="password")
        remember = st.checkbox("Save this API key in .env file for future use", value=True)

        submitted = st.form_submit_button("Submit", use_container_width=True)

        if submitted and api_key:
            # Validate the API key
            with st.spinner("Validating API key..."):
                is_valid, error_message = validate_api_key(api_key)

            if is_valid:
                # Set the API key in the environment
                os.environ["GOOGLE_API_KEY"] = api_key

                # Save to .env file if requested
                if remember:
                    try:
                        # Find the .env file path
                        dotenv_path = find_dotenv()
                        if not dotenv_path:
                            # Create .env file in the current directory if it doesn't exist
                            with open(".env", "w") as f:
                                f.write(f"GOOGLE_API_KEY = \"{api_key}\"")
                            st.success("API key saved to new .env file!")
                        else:
                            # Update existing .env file
                            set_key(dotenv_path, "GOOGLE_API_KEY", api_key)
                            st.success("API key saved to existing .env file!")
                    except Exception as e:
                        st.error(f"Error saving API key to .env file: {str(e)}")
                        st.info("The application will still work for this session, but you'll need to enter the API key again next time.")

                # Indicate that the API key is now available
                return True
            else:
                # Show error message if validation failed
                st.error(f"Invalid API key: {error_message}")
                st.info("Please check your API key and try again.")
                return False

    # If we get here, the API key is not yet available
    return False
