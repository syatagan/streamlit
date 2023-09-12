import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode, DataReturnMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from Src.utils import *
import pg_show_product_detail

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

def get_category_product_list(xCategory):
    df = read_food_data()
    cols = ["code", "product_name_en", "brands", "off:nova_groups", "off:nutriscore_grade", "url","allergens"]
    df = df.loc[df["Category_new"] == xCategory, cols]
    return df

def show_product_list(df):
    try:
        #df = df.sort_values(by="product_name_en", ascending=True)
        df["img_small_url"] = df.apply(lambda x: x["url"].replace(".400.jpg", ".100.jpg"), axis=1)
        grd = GridOptionsBuilder.from_dataframe(df)
        grd.configure_grid_options(rowHeight=100)
        grd.configure_pagination(enabled=True, paginationPageSize=10)
        grd.configure_selection()
        grd.configure_column(field="code", header_name="Code", width=80)
        grd.configure_column(field="url", header_name="", width=0)
        grd.configure_column(field="product_name_en", header_name="Name", width=100)
        grd.configure_column(field="brands", header_name="Brand", width=80)
        grd.configure_column(field="off:nova_groups", header_name="NOVA", width=50)
        grd.configure_column(field="off:nutriscore_grade", header_name="Nutrition", width=60)
        grd.configure_column(field="allergens", header_name="Allergens", width=80, cellStyle={'color': 'red'})
        grd.configure_column(field="img_small_url", header_name="Image", cellStyle=image_jscode)
        gridOptions = grd.build()

        grd_Table = AgGrid(data=df,
                           gridOptions=gridOptions,
                           fit_columns_on_grid_load=True,
                           height=500,
                           width="100%",
                           allow_unsafe_jscode=True,
                           custom_css={"#gridToolBar": {"padding-bottom": "0px !important"}},
                           theme="streamlit",
                           key="id_row"
                           )
        if grd_Table['selected_rows']:
            st.write("1")
            product_code = grd_Table['selected_rows'][0]['code']
            if (str(product_code) != ""):
                st.write("2")
                pg_show_product_detail.app(product_code)
        else:
            st.write("No row selected")
    except:
        st.error("Something went wrong when getting products")

def app(xCategory = ""):
    if (xCategory != ""):
        df = get_category_product_list(xCategory)
        show_product_list(df)
    else:
        st.error("No defined Category")
