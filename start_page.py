import streamlit as st
from utils import check_password
from app_page import MainPage
from signup_page import SignUpPage
from page import Page


class LoginPage(Page):

    def login_form(self):
        with self.placeholder.form("login_page"):
            email = st.text_input('Email', '', autocomplete="email")
            password = st.text_input('Password', '', type="password", autocomplete="password")
            login_button = st.form_submit_button('Login')
            signup_button = st.form_submit_button('Sign Up')
            if signup_button:
                st.session_state['signup'] = True
            if login_button:
                check_password(email, password)
                if st.session_state["logged_in"]:
                    self.placeholder.empty()
                    st.session_state["email"] = email
                    st.experimental_rerun()
                else:
                    st.error('Wrong email or password', icon="🚨")

    def run_page(self):
        st.session_state["logged_in"] = False if "logged_in" not in st.session_state.keys() else st.session_state["logged_in"]
        st.session_state['signup'] = False if "signup" not in st.session_state.keys() else st.session_state["signup"]
        if not st.session_state["logged_in"]:
            self.login_form()
            if st.session_state['signup']:
                self.placeholder.empty()
                signup_page = SignUpPage()
                signup_page.run_page()
        else:
            main_page = MainPage()
            main_page.run_page()


login_page = LoginPage()
login_page.run_page()
