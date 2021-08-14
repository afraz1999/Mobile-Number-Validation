import streamlit as st

import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

from phonenumbers import geocoder
from phonenumbers import carrier
import phonenumbers


def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()
def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

	


def main():

	menu = ["SignUp","Login"]
	choice = st.sidebar.radio("Menu",menu)

	if choice == "Login":
		st.subheader("Login Section:")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			create_usertable()
			result = login_user(username,password)
			if result:


				if len(username) and len(password) != 0: 
					st.success("Logged In as {}".format(username))
					st.title("Mobile Number Location Tracker & Also Service Operator")
					mobile_number=st.text_input("Enter Your Number:")

					if st.button("Track"):
						ch_number=phonenumbers.parse(mobile_number, 'CH')
						st.success("Location: {}".format(geocoder.description_for_number(ch_number,"en")))
						services_operator=phonenumbers.parse(mobile_number,'RO')
						st.success("Service Operator: {}".format(carrier.name_for_number(services_operator,"en")))

				else:
					st.warning("Incorrect Username, Password")		
					st.info("Go to SignUp Menu to Create New Account")		

				
			else:
				st.warning("Incorrect Username, Password")		
				st.info("Go to SignUp Menu to Create New Account")
			

	elif choice == "SignUp":
		st.title("Mobile Number Validation")
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("SignUp"):
			create_usertable()
			add_userdata(new_user,new_password)

			
			if len(new_user) and len(new_password) != 0:
				st.info("Go to Login Menu to login")
				st.success("you have successfully created a New Account")
				

			else:
				st.warning("Please Enter Valid Username\Password")
				
			
				



if __name__ == '__main__':
	main()