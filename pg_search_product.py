import streamlit as st
import pandas as pd
import pg_show_category_products
import pg_show_product_detail
from Src.utils import *

def search_product():
    search_text = st.session_state.txt_search
    df = read_food_data()
    cols = ["code", "product_name_en", "brands", "off:nova_groups", "off:nutriscore_grade", "url"]
    result_df = df.loc[(df["product_name_en"].str.contains(search_text)) |
                       (df["code"].astype(str).str.contains(search_text)), cols]
    ## if the result set contains only one product
    if (result_df.shape[0] == 0):
        st.session_state.notfound = "There is not any food product with " + search_text
        app()
    elif (result_df.shape[0] == 1):
        product_code = result_df["code"].values[0]
        pg_show_product_detail.app(product_code)
        oneri_bul(product_code)
    else:
        pg_show_category_products.show_product_list(result_df)

def show_Product_Search_Form():
    with st.form(key="product_search_form"):
        st.text_input(label="Product", key="txt_search")
        st.form_submit_button(label="Search",on_click=search_product)
    if ("notfound" in st.session_state):
        if (st.session_state.notfound != ""):
            st.info(st.session_state.notfound)
            st.session_state.notfound = ""
def oneri_bul(product_code):
    df = read_food_data()
    secilen_urun = df[df["code"] == product_code]
    if not secilen_urun.empty:
        secilen_urun = secilen_urun.iloc[0]
        selected_allergens = secilen_urun["allergens"].split(", ")
        oneriler = df[(df["off:nova_groups"] < secilen_urun["off:nova_groups"]) &
                      (df["Category_new"] == secilen_urun["Category_new"])&
                      (df["off:nutriscore_grade"] < secilen_urun["off:nutriscore_grade"])]
        if selected_allergens:
            oneriler = oneriler[
                ~oneriler["allergens"].apply(lambda x: any(allergen in x for allergen in selected_allergens))]

        if not oneriler.empty:
            st.markdown('## Products you might be interested in :mag:')
            cols = ["code", "product_name_en", "brands", "off:nova_groups", "off:nutriscore_grade", "url", "allergens"]
            recommendations_df = oneriler[cols]
            pg_show_category_products.show_product_list(recommendations_df)
        else:
            st.warning('No suitable recommendation found.😔')
    #else:
        #st.error('Ürün bulunamadı.')

def app():
    show_Product_Search_Form()

if __name__ == "__main__":
    st.session_state.selected_product = st.text_input('ürün numarası:', type='default')
    app()

