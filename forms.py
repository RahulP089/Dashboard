import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime
import io

# --- Background Image Function ---
def get_base64_of_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- Image Path ---
image_path = "background.jpg"
base64_image = get_base64_of_image(image_path)

# --- Inject Custom CSS ---
# span heading size
#
custom_css = f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{base64_image}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    font-family: 'Segoe UI', sans-serif;
}}
.css-pxxe24 {{ visibility: hidden; }}
h1 {{ font-size: 32px !important; color: #222 !important; }}
h2 {{ font-size: 35px !important; color: #333 !important; }}
h3 {{ font-size: 24px !important; color: #444 !important; }}
h4, h5, h6 {{ font-size: 20px !important; color: #555 !important; }}
label {{ font-size: 12px !important; color: black !important; }}
p, div, span {{ font-size: 17px !important; color: black !important; font-weight:bold !important }}
input, textarea {{
    font-size: 15px !important;
    color: black !important;
    background-color: #f5f5f5 !important;
    height: 40px !important;
    padding: 8px;
    border-radius: 5px;
}}
textarea {{ height: 100px !important; }}
button {{
    font-size: 14px !important;
    padding: 10px 20px;
    background-color: #4CAF50 !important;
    color: black !important;
    border-radius: 10px;
    border: none !important;
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- User Credentials ---
USER_CREDENTIALS = {
    "Rahul": {"password": "rahul@123", "role": "admin"},
    "User": {"password": "user@123", "role": "user"},
}

# --- Session State ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None

# --- Login Function ---
def login():
    st.title("🔐 Login to Dashboard")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

        if login_button:
            user_info = USER_CREDENTIALS.get(username)
            if user_info and user_info["password"] == password:
                st.session_state.authenticated = True
                st.session_state.role = user_info["role"]
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

# --- Observation Form Function ---
def observation_form():
    st.title("📋 Daily HSE Observation")
    excel_file = r"C:\\Users\\rahul_\\Desktop\\New Microsoft Excel Worksheet.xlsx"

    with st.form("observation_form"):
        date = st.date_input("Date", value=datetime.today())

        well_options = ["WELL-101", "WELL-102", "WELL-103", "WELL-104", "WELL-105"]
        well_no = st.selectbox("Well No", well_options)

        area_options = ["Well head","Flow Line","OHPL",]
        area = st.selectbox("Area", area_options)

        observer_options = [
            "JOSEPH", "MUHAMMAD SOOMER", "PRADEEP", "VARGHEESE", "MUHAMMAD ILYAS", "SHIVA KANNAN", "VAISHAK",
            "ARUN SOMAN", "SUDISH", "MUNSIF KHAN", "M.UMAIR", "QAMAR", "SURESH BABU", "AJISH JOSEPH",
            "MD ILYAS", "ARFAN", "JAMALI"
        ]
        observer_name = st.selectbox("Observer Name", observer_options)

        observation_details = st.text_area("Observation Details")
        recommended_action = st.text_area("Recommended Solution / Action Taken")
        supervisor_name = st.text_input("Supervisor Name")
        discipline = st.text_input("Discipline")
        category = st.text_input("Category")
        classification = st.text_input("Classification")
        status = st.selectbox("Status", ["Open", "Closed", "In Progress", "Pending"])
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            headers = ["SL NO", "DATE", "WELL NO", "AREA", "OBSERVER NAME", "OBSERVATION DETAILS",
                       "RECOMMENDED SOLUTION/ ACTION TAKEN", "SUPERVISOR NAME", "DISCIPLINE",
                       "CATEGORY", "CLASSIFICATION", "STATUS"]

            if not os.path.exists(excel_file):
                pd.DataFrame(columns=headers).to_excel(excel_file, index=False)

            existing_df = pd.read_excel(excel_file)
            next_sl_no = len(existing_df) + 1

            new_row = pd.DataFrame([[
                next_sl_no, date, well_no, area, observer_name, observation_details,
                recommended_action, supervisor_name, discipline, category,
                classification, status
            ]], columns=headers)

            updated_df = pd.concat([existing_df, new_row], ignore_index=True)

            with pd.ExcelWriter(excel_file, engine="openpyxl", mode="w") as writer:
                updated_df.to_excel(writer, index=False, sheet_name="Sheet1")

            st.success(f"✅ Observation saved with SL NO: {next_sl_no}")

# --- Permit Form Function ---
def permit_form():
    st.title("📖 Daily Internal Permit Log")
    excel_file = r"C:\\Users\\rahul_\\Desktop\\Daily_Internal_Permit_Log.xlsx"

    with st.form("permit_form"):
        date = st.date_input("Date", value=datetime.today())
        permit_number = st.text_input("Permit Number")
        location = st.text_input("Location")
        work_description = st.text_area("Work Description")
        issued_by = st.text_input("Issued By")
        received_by = st.text_input("Received By")
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            headers = ["SL NO", "DATE", "PERMIT NUMBER", "LOCATION", "WORK DESCRIPTION", "ISSUED BY", "RECEIVED BY"]

            if not os.path.exists(excel_file):
                pd.DataFrame(columns=headers).to_excel(excel_file, index=False)

            existing_df = pd.read_excel(excel_file)
            next_sl_no = len(existing_df) + 1

            new_row = pd.DataFrame([[
                next_sl_no, date, permit_number, location, work_description, issued_by, received_by
            ]], columns=headers)

            updated_df = pd.concat([existing_df, new_row], ignore_index=True)

            with pd.ExcelWriter(excel_file, engine="openpyxl", mode="w") as writer:
                updated_df.to_excel(writer, index=False, sheet_name="Sheet1")

            st.success(f"✅ Permit log saved with SL NO: {next_sl_no}")

# --- Dashboard Function ---
def dashboard():
    if st.session_state.role != "admin":
        st.error("🚫 You do not have permission to view the dashboard.")
        return

    st.title("📊 Dashboard")

    form_type = st.radio("Select form to view data:", ["📋 Daily HSE OBS", "📖 Daily Internal Permit Log"])

    if form_type == "📋 Daily HSE OBS":
        file_path = r"C:\\Users\\rahul_\\Desktop\\New Microsoft Excel Worksheet.xlsx"
    else:
        file_path = r"C:\\Users\\rahul_\\Desktop\\Daily_Internal_Permit_Log.xlsx"

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        search_term = st.text_input("🔍 Search:")
        if search_term:
            df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

        st.dataframe(df, use_container_width=True)

        buffer = io.BytesIO()
        df.to_excel(buffer, index=False, engine="openpyxl")
        buffer.seek(0)

        st.download_button(
            label="📥 Download Excel",
            data=buffer,
            file_name=os.path.basename(file_path),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("No data file found.")

# --- Main App ---
if not st.session_state.authenticated:
    login()
else:
    st.sidebar.title("📂 Navigation")
    page = st.sidebar.radio("Choose a page:", ["🏠 Home", "📋 Daily HSE OBS", "📖 Daily Internal Permit Log", "📊 View Dashboard", "🔓 Logout"])

    if page == "🏠 Home":
        st.title("🏠 Welcome")
        st.write("Select a form or dashboard using the sidebar.")
    elif page == "📋 Daily HSE OBS":
        observation_form()
    elif page == "📖 Daily Internal Permit Log":
        permit_form()
    elif page == "📊 View Dashboard":
        dashboard()
    elif page == "🔓 Logout":
        st.session_state.authenticated = False
        st.session_state.role = None
        st.success("✅ Logged out successfully")
        st.rerun()
