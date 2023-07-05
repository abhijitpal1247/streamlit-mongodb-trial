import io
import streamlit as st
from page import Page
from zipfile import ZipFile
from utils import save_image, query_datasets, get_preview_images


class MainPage(Page):

    def run_page(self):
        with self.placeholder.container():
            col1, col2, col3 = st.columns(spec=[4, 4, 2], gap="large")
            with col1:
                st.write(f"Logged in as {st.session_state['email']}")
            with col3:
                logout_button = st.button('Log Out')
                if logout_button:
                    st.session_state["logged_in"] = False
                    st.experimental_rerun()
            st.divider()
        uploaded_file = st.file_uploader("Upload Dataset", type="zip")

        if uploaded_file is not None:
            z = ZipFile(io.BytesIO(uploaded_file.getvalue()))
            st.write('Preview Data')
            file_list = z.infolist()
            max_columns = 5 if len(file_list) > 5 else len(file_list)
            column_list = list(st.columns(max_columns))
            for i in range(max_columns):
                with column_list[i]:
                    im = z.read(file_list[i])
                    st.image(im)
            save_button = st.button('Save Data')
            if save_button:
                progress_text = "Operation in progress. Please wait."
                my_bar = st.progress(0, text=progress_text)
                for idx, i in enumerate(file_list):
                    save_image(z.read(i), uploaded_file.name[:-4], st.session_state['email'])
                    my_bar.progress(float(idx + 1)/len(file_list), text=progress_text)
                my_bar.progress(float(idx + 1) / len(file_list), text='Saved')

        dataset_list = query_datasets(st.session_state["email"])
        dataset_select = st.selectbox('Select Dataset to preview', options=['-']+dataset_list)
        if dataset_select != '-':
            image_list = get_preview_images(dataset_select, st.session_state['email'], 5)
            max_columns = 5 if len(image_list) >= 5 else len(image_list)
            column_list = list(st.columns(max_columns))
            for i in range(max_columns):
                with column_list[i]:
                    st.image(image_list[i])
