import pandas as pd
import streamlit as st
import pg_show_category_products
import pg_search_product
import pg_about
import pg_user_prefs
import pg_homepage
from Src.utils import *


# Session state değişkenini tanımlayın
def init_session_state():
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "pg_homepage"

# Her sayfada bu fonksiyonu çağırarak session state'i başlatın
def main():
    init_session_state()

    st.set_page_config(
        page_title="Safe Food For Everyone",
        page_icon="path_of_your_favicon",
        layout="wide",
        initial_sidebar_state="auto",
    )

    local_css("style.css")
    st.header("Safe Food for Everyone")

    if (st.sidebar.button("User Preferences", type="secondary")):
        st.session_state.current_page = "pg_user_prefs"
        pg_user_prefs.app()
    if (st.sidebar.button("Search Product", type="secondary")):
        st.session_state.current_page = "pg_search_product"
        pg_search_product.app()

    category_df = read_categories_data()
    buttons = []
    category_list = category_df["Name"].values
    for col in category_list:
        buttons.append((col, st.sidebar.button(col, type="primary")))
    for cat, button in buttons:
        if button:
            st.session_state.current_page = "pg_show_category_products"
            pg_show_category_products.app(cat)
    if (st.sidebar.button("About", type="secondary")):
        st.session_state.current_page = "pg_about"
        pg_about.app()
    # Hangi sayfa görüntüleniyor ise ona göre "Wellcome to the homepage" metnini görüntüle
    if st.session_state.current_page == "pg_homepage":
        pg_homepage.app()


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()