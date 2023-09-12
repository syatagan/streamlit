import pandas as pd
import streamlit as st
from streamlit_card import card

def main():
    """
    Heart of the streamlit App
    """
    st.set_page_config(
        page_title="Safety Food For Everyone",
        page_icon="path_of_your_favicon",
        layout="wide",
        initial_sidebar_state="auto",
    )
    local_css("style.css")
    st.title("Safety Food For Everyone")
    st.markdown("Welcome to the Safe Food World.")
    st.sidebar.subheader("Categories")
    category_list = pd.read_csv("categories.csv")
    buttons = []
    category_list = ["Chocolate","Yoghurt","Chips","Snacks","Frozen","Biscuits"]
    for col in category_list:
        buttons.append((col,st.sidebar.button(col, type="primary")))

    for x, button in buttons:
        if button:
            st.experimental_rerun()
            st.write( x + " caegory button")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if __name__ ==  "__main__":
     main()