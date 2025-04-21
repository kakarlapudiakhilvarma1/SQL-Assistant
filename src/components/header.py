"""
Header components for the Healthcare Database Request Assistant.
"""

import streamlit as st


def render_header():
    """
    Render the application header with title and subtitle.
    """
    st.markdown("<h1 class='main-header'>Healthcare Database Request Assistant 🏥</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>Process database service requests for healthcare professionals</p>", unsafe_allow_html=True)
