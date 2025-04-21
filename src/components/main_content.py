"""
Main content components for the Healthcare Database Request Assistant.
"""

import streamlit as st


def render_input_section():
    """
    Render the input section for service requests.
    
    Returns:
        tuple: (input_text, submit_button, clear_button)
    """
    st.markdown("<div class='query-box'>", unsafe_allow_html=True)
    
    # Input text area
    input_text = st.text_area(
        "Enter your service request:", 
        height=100,
        placeholder="Example: Update the phone number for patient ID 1042 to +91-8885544332"
    )
    
    # Action buttons
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    with col_btn1:
        submit_button = st.button("Process Request", use_container_width=True)
    with col_btn2:
        clear_button = st.button("Clear", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    return input_text, submit_button, clear_button


def display_response(response):
    """
    Display the response from the LLM with appropriate styling.
    
    Args:
        response (dict): The response from the LLM
    """
    # Check if the response contains an error message
    is_error = "ERROR:" in response['answer']
    
    # Use appropriate styling based on whether it's an error
    style_class = "error-response" if is_error else "success-response"
    
    # Display the response with styling
    st.markdown(f"<div class='{style_class}'>", unsafe_allow_html=True)
    st.markdown("### Response:")
    st.markdown(response['answer'])
    st.markdown("</div>", unsafe_allow_html=True)


def display_history(history):
    """
    Display the request history in an expander.
    
    Args:
        history (list): List of (request, action_type) tuples
    """
    if history:
        with st.expander("Request History", expanded=False):
            for i, (req, act) in enumerate(history):
                st.markdown(f"*Request {i+1}:* {req} (Action: {act})")
                st.divider()
