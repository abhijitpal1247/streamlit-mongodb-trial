import streamlit as st
from abc import ABC, abstractmethod


class Page(ABC):
    def __init__(self):
        self.placeholder = st.empty()

    @abstractmethod
    def run_page(self):
        pass
