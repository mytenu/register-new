import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

SCOPE=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]


@st.cache_resource
def init_connection():
	credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPE)
	clients=gspread.authorize(credentials)
	return clients


connect=init_connection()

client=connect.open("register_users").sheet1

st.title("Talisoft Unisex Boutique")


tab1, tab2 = st.tabs(["Login", "Registration"])

with tab1:
	with st.form("Login"):
		username100=st.text_input("Enter Username").strip().lower()
		password100=st.text_input("Enter password", type="password").strip()
		users= client.get_all_records()
		found = False
		if st.form_submit_button("Login"):
			if username100 == "admin" and password100=="123456":
				df=pd.DataFrame(users)
				st.dataframe(df)
			else:
				for user in users: 
					if str(user["username"])== username100 and str(user["password"]) == password100:
						found = True
						st.success(f"welcome {username100}")
						break
				if not found:
					st.success("wrong username or password")
with tab2:
	with st.form("Registration"):
		users=client.get_all_records()
		name=st.text_input("Enter your name").strip()
		code = st.selectbox("Country Code", ["+233", "+234", "+44", "+1"])
		contact1= st.text_input("Enter your contact").strip()
		contact= code+contact1
		email= st.text_input("Enter Email").strip()
		gender=st.radio("Select Gender:", ("Male", "Female", "Prefer not say"))
		dob=st.text_input("Enter your date of birth").strip()
		username=st.text_input("Enter your username").strip().lower()
		password=st.text_input("Enter Password", type="password").strip()
		password2=st.text_input("Repeat Password", type="password").strip()
		if st.form_submit_button("Submit"):
			if password != password2:
				st.success("Your Passwords do not match")
			else:
				client.append_row([name, contact, email, gender, dob, username, password])
				st.success("Registration Successful")
