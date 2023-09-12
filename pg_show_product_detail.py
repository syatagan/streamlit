import streamlit as st
import pandas as pd
from Src.utils import *


def show_Product_Detail(xproduct_code):
    df = get_product_detail_df(xproduct_code)
    if (df.shape[0] != 1):
        st.error("An error occured with the product code :" + str(xproduct_code))
    else:
        col1, col2 = st.columns((1, 2))
        col1.image(df["url"].values[0], caption='', use_column_width=True)
        col2.header(df["product_name_en"].values[0])
        col2.markdown("**CODE** : " + str(df["code"].values[0]))
        # split correction  ':'
        ingredients_text = df["ingredients_text_en"].values[0]
        if ":" in ingredients_text:
            ingredient_parts = ingredients_text.split(':')
            if len(ingredient_parts) > 1:
                ingredient_value = ingredient_parts[1].strip()
                col2.markdown("**INGREDIENTS** : " + ingredient_value + "**")
            else:
                col2.markdown("**INGREDIENTS** : ...")
        else:
            col2.markdown("**INGREDIENTS : ...**")

        col2.markdown("**BRAND** : " + df["brands"].values[0].upper())
        if (str(df["stores"].values[0]) != ""):
            col2.markdown("**STORES** : " + df["stores"].values[0].upper())
        else:
            col2.markdown("**STORES** : ...")
        col2.markdown("**ALLERGENS** : " + df["allergens"].values[0])
        ########################################################################
        # SCORES
        ########################################################################
        with st.container():
            col1, col2 = st.columns(2)
            if pd.isna(df["off:nutriscore_grade"].values[0]):
                col1.success("**NUTRITION SCORE** : No Information")
            elif df["off:nutriscore_grade"].values[0] == "E":
                col1.error("**NUTRITION SCORE** : E", icon="🚨")
            else:
                col1.success(f"**NUTRITION SCORE** : " + df["off:nutriscore_grade"].values[0])
            df["off:nova_groups"] = df["off:nova_groups"].astype(str)
            if pd.isna(df["off:nova_groups"].values[0]):
                col2.error("**NOVA SCORE** : No Information")
            elif df["off:nova_groups"].values[0] == "4":
                col2.error("**NOVA SCORE** : 4", icon="🚨")
            else:
                nova_score = df["off:nova_groups"].values[0]
                nova_score = nova_score.replace(',', '.')
                nova_score = int(float(nova_score))
                col2.success(f"**NOVA SCORE** : {nova_score}")
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
                allergen_expression = allergen_expressions.get(allergen_key, "Unknown allergen")
                col_object.error(f"{allergen_icon} {allergen_expression}")

            # Allerjen seçimi yapıldı ama allergens alanı boş
        if Allergen_Count == 0 and df["Allergen_Milk"].values[0] == "2":
            st.info("NO ALLERGEN INFORMATION")

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
        allergens = df_product["allergens"].values[0].split(", ")
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
        df_product["Allergen_Egg"] = "0"
        if ("pref_Allergen_Egg" in st.session_state):
            if (st.session_state.pref_Allergen_Egg == 0):
                chk = False
        if (chk) & ("Egg" in allergens):
            df_product["Allergen_Egg"] = "1"
        if (chk) & ("Eggs" in allergens):
            df_product["Allergen_Egg"] = "1"
        df_product["Allergen_Nut"] = "0"
        if ("pref_Allergen_Nut" in st.session_state):
            if (st.session_state.pref_Allergen_Nut == 0):
                chk = False
        if (chk) & ("Nut" in allergens):
            df_product["Allergen_Nut"] = "1"
        if (chk) & ("Nuts" in allergens):
            df_product["Allergen_Nut"] = "1"
        df_product["Allergen_Peanut"] = "0"
        if ("pref_Allergen_Peanut" in st.session_state):
            if (st.session_state.pref_Allergen_Peanut == 0):
                chk = False
        if (chk) & ("Peanut" in allergens):
            df_product["Allergen_Peanut"] = "1"
        if (chk) & ("Peanuts" in allergens):
            df_product["Allergen_Peanut"] = "1"
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
