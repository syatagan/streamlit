import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode, DataReturnMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from Src.utils import *
import pg_show_product_detail

image_nation = JsCode("""function (params) {
            var element = document.createElement("span");
            var imageElement = document.createElement("img");

            if (params.data.url) {
                imageElement.src = params.data.url;
                imageElement.width="20";
            } else {
                imageElement.src = "";
            }
            element.appendChild(imageElement);
            element.appendChild(document.createTextNode(params.value));
            return element;
            }""")


render_image = JsCode('''
    function renderImage(params) {
    // Create a new image element
    var img = new Image();

    // Set the src property to the value of the cell (should be a URL pointing to an image)
    img.src = params.value;

    // Set the width and height of the image to 50 pixels
    img.width = 50;
    img.height = 50;

    // Return the image element
    return img;
    }
'''
)

link_jscode = JsCode("""
function(params) {
	var element = document.createElement("span");
	var linkElement = document.createElement("a");
	var linkText = document.createTextNode(params.value);
	link_url = params.value;
	linkElement.appendChild(linkText);
	linkText.title = params.value;
	linkElement.href = link_url;
	linkElement.target = "_blank";
	element.appendChild(linkElement);
	return element;
};
""")
## var image_url = "https://images.openfoodfacts.org/images/products/931/001/524/1932/1.100.jpg";
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

def app():
    df = read_food_data()
    cols = ["code", "product_name_en", "brands", "off:nova_groups", "off:nutriscore_grade","allergens", "url"]
    df = df.loc[df["Category_new"] == "Chocolates", cols]
    df = df.sort_values(by="product_name_en",ascending=True)
    df["img_small_url"] = df.apply(lambda x : x["url"].replace(".400.jpg",".100.jpg"),axis=1)
    grd = GridOptionsBuilder.from_dataframe(df)
    grd.configure_grid_options(rowHeight=100)
    grd.configure_pagination(enabled=True, paginationPageSize = 10)
    grd.configure_selection()
    grd.configure_column(field="code", header_name="Code", width=70)
    grd.configure_column(field="product_name_en", header_name="Name", width=80)
    grd.configure_column(field="brands", header_name="Brand", width=80)
    grd.configure_column(field="off:nova_groups", header_name="Nova Score", width=50)
    grd.configure_column(field="off:nutriscore_grade", header_name="Nutrition Score", width=60)
    grd.configure_column(field="allergens", header_name="Allergens", width=80, cellStyle={'color': 'red'})
    #grd.configure_column(field="url", header_name="url", cellRenderer=link_jscode)
    grd.configure_column(field="img_small_url", header_name="Image", cellStyle = image_jscode)
    grd.configure_column(field="sm_url", header_name="Image2")
    gridOptions = grd.build()

    grd_Table = AgGrid(data = df,
                       gridOptions=gridOptions,
                       fit_columns_on_grid_load=True,
                       height=500,
                       width="80%",
                       allow_unsafe_jscode=True,
                       custom_css={"#gridToolBar": {"padding-bottom": "0px !important"}},
                       theme = "streamlit",
                       key="id_row"
                       )
    if grd_Table['selected_rows']:
        product_code = grd_Table['selected_rows'][0]['code']
        if (str(product_code) != ""):
            pg_show_product_detail.app(product_code)
    else:
        st.write("No row selected")
