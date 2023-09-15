import streamlit as st
import pandas as pd
from Src.utils import *
from PIL import Image
import pg_show_category_products

def oneri_bul(product_code):
    df = read_food_data()
    secilen_urun = df[df["code"] == product_code]
    if not secilen_urun.empty:
        secilen_urun = secilen_urun.iloc[0]
        selected_allergens = secilen_urun["allergens"].split(", ")
        oneriler = df[(df["off:nova_groups"] < secilen_urun["off:nova_groups"]) &
                      (df["Category_new"] == secilen_urun["Category_new"]) &
                      (df["off:nutriscore_grade"] < secilen_urun["off:nutriscore_grade"])]
        if selected_allergens:
            oneriler = oneriler[
                ~oneriler["allergens"].apply(lambda x: any(allergen in x for allergen in selected_allergens))]

        if not oneriler.empty:
            st.markdown('## Products you might be interested in :mag:')
            recommendations_df = oneriler[["code", "product_name_en", "off:nova_groups", "off:nutriscore_grade", "allergens", "url"]]
            pg_show_category_products.show_product_list(recommendations_df)
        else:
            st.warning('No suitable recommendation found.😔')
def show_Product_Detail(xproduct_code):
    df = get_product_detail_df(xproduct_code)
    if (df.shape[0] != 1):
        st.error("An error occured with the product code :" + str(xproduct_code))
    else:
        col1, col2 = st.columns((1, 2))
        col1.image(df["url"].values[0], caption='', use_column_width=True)
        col2.header(df["product_name_en"].values[0])
        col2.markdown("**CODE** : " + str(df["code"].values[0]))
        ingredients_text = df["ingredients_text_en"].values[0]
        if ":" in ingredients_text:
            ingredient_parts = ingredients_text.split(':')
            if len(ingredient_parts) > 1:
                ingredient_value = ingredient_parts[1].strip()
                col2.markdown("**INGREDIENTS** : " + ingredient_value)
            else:
                col2.markdown("**INGREDIENTS** : " + ingredients_text)
        else:
            col2.markdown("**INGREDIENTS** : " + ingredients_text)
        col2.markdown("**BRAND** : " + df["brands"].values[0])
        if (str(df["stores"].values[0]) != ""):
            col2.markdown("**STORES** : " + df["stores"].values[0])
        else:
            col2.markdown("**STORES** : Carrefour")
        col2.markdown("**ALLERGENS** : " + df["allergens"].values[0])
        ########################################################################
        # SCORES
        ########################################################################
        nutriscore_expressions = {
            "A": "Very good nutritional quality",
            "B": "Good nutritional quality",
            "C": "Average nutritional quality",
            "D": "Poor nutritional quality",
            "E": "Bad nutritional quality"
        }
        novascore_expressions = {
            "1" : "Unprocessed or minimally processed foods",
            "2" : "Processed culinary ingredients",
            "3" : "Processed foods",
            "4" : "Ultra processed foods"
        }
        with st.container():
            col1, col2 = st.columns(2)
            show_nutritional_quality = True
            if ("pref_nutritional_quality" in st.session_state):
                if (st.session_state.pref_nutritional_quality == "Not Important"):
                    show_nutritional_quality = False
            if (show_nutritional_quality):
                if (pd.isna(df["off:nutriscore_grade"].values[0]) | (df["off:nutriscore_grade"].values[0] == "")):
                    col1.success("**NUTRITION SCORE** : No Information")
                elif df["off:nutriscore_grade"].values[0] == "E":
                    xStr = "**NUTRITION SCORE : E** (" + nutriscore_expressions["E"] + ")"
                    col1.error(xStr, icon="🚨")
                else:
                    xScore = df["off:nutriscore_grade"].values[0]
                    xStr = "**NUTRITION SCORE : " + xScore + "** (" + nutriscore_expressions[xScore] + ")"
                    col1.success(xStr)
        show_nova_quality = True
        if ("pref_nova_quality" in st.session_state):
            if (st.session_state.pref_nova_quality == "Not Important"):
                show_nova_quality = False
        if (show_nova_quality):
            if (show_nutritional_quality):
                colnova = col2
            else:
                colnova = col1
            df["off:nova_groups"] = df["off:nova_groups"].astype(str)
            if (pd.isna(df["off:nova_groups"].values[0]) | (df["off:nova_groups"].values[0] == "")):
                colnova.error("**NOVA SCORE** : No Information")
            elif df["off:nova_groups"].values[0] == "4":
                xstr = "**NOVA SCORE : 4** (" +novascore_expressions["4"] + ")"
                colnova.error(xstr, icon="🚨")
            else:
                nova_score = df["off:nova_groups"].values[0]
                nova_score = nova_score.replace(',', '.')
                nova_score = int(float(nova_score))
                xstr = "**NOVA SCORE : " + str(nova_score) + "** (" +novascore_expressions[str(nova_score)] + ")"
                colnova.success(xstr)
        #######################################################################
        # ALLERGENS
        ########################################################################
        # Allergen icons and expressions
        allergen_icons = {
            "Allergen_Milk": "🥛",
            "Allergen_Egg": "🥚",
            "Allergen_Nut": "🌰",
            "Allergen_Peanut": "🥜",
            "Allergen_Gluten": "🌾",
            "Allergen_Soybeans": "🌱"
        }
        allergen_expressions = {
            "Allergen_Milk": "Contains Milk",
            "Allergen_Egg": "Contains Egg",
            "Allergen_Nut": "Contains Nuts",
            "Allergen_Peanut": "Contains Peanuts",
            "Allergen_Gluten": "Contains Gluten",
            "Allergen_Soybeans": "Contains Soybeans"
        }
        Allergen_Count = 0
        Allergen_Pozitives_list = []
        Allergen_col_list = [col for col in df.columns if "Allergen" in col]
        for col in Allergen_col_list:
            if str(df[col].values[0]) == "1":
                Allergen_Pozitives_list.append(col)
        Allergen_Count = len(Allergen_Pozitives_list)
        if Allergen_Count > 0:
            col_obj_list = st.columns(Allergen_Count)
            for i, col_object in enumerate(col_obj_list):
                allergen_key = Allergen_Pozitives_list[i]
                allergen_icon = allergen_icons.get(allergen_key, "❓")
                allergen_expression = allergen_expressions.get(allergen_key, "*Unknown Allergen*")
                col_object.error(f"{allergen_icon} **{allergen_expression}**")

            # Allerjen seçimi yapıldı ama allergens alanı boş
        if Allergen_Count == 0 and df["Allergen_Milk"].values[0] == "2":
            st.info("NO ALLERGEN INFORMATION")
        ############################################################
        # Recommendation
        ############################################################
        oneri_bul(xproduct_code)
def check_allergens(df_product):
    if (df_product["allergens"].values[0] == ""):
        allergens = []
        df_product["Allergen_Milk"] = "2"
        df_product["Allergen_Egg"] = "2"
        df_product["Allergen_Nut"] = "2"
        df_product["Allergen_Peanut"] = "2"
        df_product["Allergen_Gluten"] = "2"
        df_product["Allergen_Soybeans"] = "2"
        return df_product
    else:
        allergens = df_product["allergens"].values[0].replace(" ","").split(",")
        chk = True
        df_product["Allergen_Milk"] = "0"
        if ("pref_Allergen_Milk" in st.session_state):
            if (st.session_state.pref_Allergen_Milk == 0):
                chk = False
        if (chk) & ("Milk" in allergens):
            df_product["Allergen_Milk"] = "1"
        chk = True
        df_product["Allergen_Gluten"] = "0"
        if ("pref_Allergen_Gluten" in st.session_state):
            if (st.session_state.pref_Allergen_Gluten == 0):
                chk = False
        if (chk) & ("Gluten" in allergens):
            df_product["Allergen_Gluten"] = "1"
        chk = True
        df_product["Allergen_Egg"] = "0"
        if ("pref_Allergen_Egg" in st.session_state):
            if (st.session_state.pref_Allergen_Egg == 0):
                chk = False
        if (chk) & ("Egg" in allergens):
            df_product["Allergen_Egg"] = "1"
        if (chk) & ("Eggs" in allergens):
            df_product["Allergen_Egg"] = "1"
        chk = True
        df_product["Allergen_Nut"] = "0"
        if ("pref_Allergen_Nut" in st.session_state):
            if (st.session_state.pref_Allergen_Nut == 0):
                chk = False
        if (chk) & ("Nut" in allergens):
            df_product["Allergen_Nut"] = "1"
        if (chk) & ("Nuts" in allergens):
            df_product["Allergen_Nut"] = "1"
        chk = True
        df_product["Allergen_Peanut"] = "0"
        if ("pref_Allergen_Peanut" in st.session_state):
            if (st.session_state.pref_Allergen_Peanut == 0):
                chk = False
        if (chk) & ("Peanut" in allergens):
            df_product["Allergen_Peanut"] = "1"
        if (chk) & ("Peanuts" in allergens):
            df_product["Allergen_Peanut"] = "1"
        chk = True
        df_product["Allergen_Soybeans"] = "0"
        if ("pref_Allergen_Soybeans" in st.session_state):
            if (st.session_state.pref_Allergen_Soybeans == 0):
                chk = False
        if (chk) & ("Soybeans" in allergens):
            df_product["Allergen_Soybeans"] = "1"
        if (chk) & ("Soybean" in allergens):
            df_product["Allergen_Soybeans"] = "1"
        return df_product

def get_product_detail_df(xproduct_code):
    df = read_food_data2()
    df.loc[df["allergens"].isnull(), "allergens"] = ""
    df.loc[df["stores"].isnull(), "stores"] = ""
    # df["GI_category"] = 1

    cols = ["code", "product_name_en", "brands", "off:nova_groups", "off:nutriscore_grade", "allergens",
            "ingredients_text_en", "stores", "url"]
    df_product = df.loc[df["code"].astype(str) == str(xproduct_code), cols]
    df_product_detail = check_allergens(df_product)
    return df_product_detail


def app(xproduct_code):
    show_Product_Detail(xproduct_code)
