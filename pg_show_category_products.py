import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode, DataReturnMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from Src.utils import *
import pg_show_product_detail
import time

image_jscode = JsCode("""
function(params) {
    var image_url = params.value;
    return {
        'background-image': 'url("'+image_url+'")',
        'background-repeat': 'no-repeat',
        'background-position': 'center',
        'color': 'transparent'
    };
}
""")
def app(xCategory = ""):
    if (xCategory != ""):
        st.subheader(f"Products in {xCategory} Category")
        df = get_category_product_list(xCategory)
        show_product_list(df)
    else:
        st.error("No defined Category")

def get_category_product_list(xCategory):
    df = read_food_data()
    cols = ["code", "product_name_en", "brands", "off:nova_groups", "off:nutriscore_grade", "url","allergens"]
    df = df.loc[df["Category_new"] == xCategory, cols]
    return df

def go_product_detail():
    if ("id_row" in st.session_state):
        if (st.session_state.id_row != None):
            product_code = st.session_state.id_row['selectedRows'][0]['code']
            pg_show_product_detail.app(product_code)
        else:
            app()

def show_product_list(df):
        df["img_small_url"] = df.apply(lambda x: x["url"].replace(".400.jpg", ".100.jpg"), axis=1)
        grd = GridOptionsBuilder()
        grd.configure_default_column(
            resizable=True,
            filterable=True,
            sortable=True,
            editable=False,
        )
        grd.configure_grid_options(rowHeight=100)
        grd.configure_pagination(enabled=True, paginationPageSize=10)
        grd.configure_selection()
        grd.configure_column(field="code", header_name="Code", width=80)
        grd.configure_column(field="product_name_en", header_name="Name", width=100)
        grd.configure_column(field="brands", header_name="Brand", width=80)
        grd.configure_column(field="off:nutriscore_grade", header_name="Nutrition Score", width=70)
        grd.configure_column(field="off:nova_groups", header_name="NOVA Score", width=70)
        grd.configure_column(field="allergens", header_name="Allergens", width=80, cellStyle={'color': 'red'})
        grd.configure_column(field="img_small_url", header_name="Image", cellStyle=image_jscode, width = 80)
        gridOptions = grd.build()
        with st.form(key="grid_frm"):
            st.form_submit_button(label="GO",on_click=go_product_detail)
            grd_Table = AgGrid(data=df,
                               gridOptions=gridOptions,
                               fit_columns_on_grid_load=True,
                               height=500,
                               width="100%",
                               allow_unsafe_jscode=True,
                               custom_css={
                                   "#gridToolBar": {
                                       "padding-bottom": "0px !important"
                                   },
                                   ".ag-header-cell-text, .ag-cell": {
                                       "font-size": "18px !important",
                                   }},
                               key="id_row",
                               theme="streamlit",
                               reload_data=True,
                               update_mode=GridUpdateMode.SELECTION_CHANGED,
                               )


