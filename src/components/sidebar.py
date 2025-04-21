"""
Sidebar components for the Healthcare Database Request Assistant.
"""

import streamlit as st


def render_sidebar():
    """
    Render the sidebar with sample requests and information.
    """
    with st.sidebar:
        st.title("Request Guide")
        
        # Tabs in sidebar for better organization
        tab1, tab2 = st.tabs(["Sample Requests", "About"])
        
        with tab1:
            st.subheader("Sample Service Requests")
            with st.expander("📝 Update Requests", expanded=False):
                st.markdown("""
                - Update the phone number for patient ID 1042 to +91-8885544332
                - Change the email address for doctor with ID 210 to dr.ravi@hospital.com
                - Set the expiry_date for license ID 502 to 2027-05-31
                """)
            
            with st.expander("🔄 Correction Requests", expanded=False):
                st.markdown("""
                - Correct the date of birth for patient ID 1090 to 1992-10-05
                - The gender field for doctor ID 255 is incorrect; please set it to 'Female'
                - The name of the department with ID 15 should be 'Cardiology'
                """)
                
            with st.expander("🔗 Assignment Requests", expanded=False):
                st.markdown("""
                - Assign doctor ID 212 to hospital ID 4, department ID 3, starting from 2024-05-01
                - End the hospital assignment for doctor ID 208 in department ID 7
                """)
                
            with st.expander("📊 Report Requests", expanded=False):
                st.markdown("""
                - Generate a report of all appointments for patient ID 1089 in April 2024
                - List all doctors specialized in Neurology currently assigned to hospital ID 3
                - Show all expired licenses for doctors as of today
                - Get the number of patients registered in hospital ID 5 last month
                """)
                
            with st.expander("🔍 Data Integrity", expanded=False):
                st.markdown("""
                - Update all phone numbers starting with 99999 to 88888 in the Patients table
                - List all departments on the 3rd floor in hospital ID 2
                - Show all appointments scheduled for next week across all hospitals
                """)
        
        with tab2:
            st.markdown("""
            ### About HDBRA
            
            This assistant helps healthcare professionals process database-level service requests that cannot be handled through the UI.
            
            *Features:*
            - SQL query generation
            - Data correction assistance
            - Report generation
            - Assignment management
            
            Built with LangChain and Gemini AI
            """)
        
        # Vector index management
        st.divider()
        st.subheader("Vector Index Management")
        reset_index = st.button("Reset Vector Index", use_container_width=True)
        
        st.divider()
        st.caption("© 2025 Healthcare IT Services")
        
        return reset_index
