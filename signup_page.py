import streamlit as st
from utils import email_exists, create_account
from page import Page
import time


class SignUpPage(Page):

    def signup_form(self):
        with self.placeholder.form("signup_page"):
            email = st.text_input('Email', '', autocomplete="email")
            password = st.text_input('Password', '', type="password", autocomplete="password")
            confirm_password = st.text_input('Confirm Password', '', type="password", autocomplete="password")
            confirm_button = st.form_submit_button('Confirm')
            cancel_button = st.form_submit_button('Cancel')
            if cancel_button:
                st.experimental_rerun()
            if confirm_button and password == confirm_password:
                if not email_exists(email):
                    create_account(email, password)
                    st.success('Account Created!', icon="✅")
                    time.sleep(1)
                    self.placeholder.empty()
                    st.session_state['signup'] = False
                    st.experimental_rerun()
                else:
                    st.error('Email Exists', icon="🚨")
                    time.sleep(1)
                    st.experimental_rerun()

    def run_page(self):
        self.signup_form()
