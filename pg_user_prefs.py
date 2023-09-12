import streamlit as st


def local_css(file_name):
    """
    render parameter css file.
    """
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def save_pref_values():
    """
    Function saves form widget values into session state variables
    """
    st.session_state.pref_nutritional_quality = st.session_state.nutritional_quality
    st.session_state.pref_nova_quality = st.session_state.nova_quality
    st.session_state.pref_Allergen_Gluten = int(st.session_state.chk_Allergen_Gluten)
    st.session_state.pref_Allergen_Milk = int(st.session_state.chk_Allergen_Milk)
    st.session_state.pref_Allergen_Egg = int(st.session_state.chk_Allergen_Egg)
    st.session_state.pref_Allergen_Nut = int(st.session_state.chk_Allergen_Nut)
    st.session_state.pref_Allergen_Peanut = int(st.session_state.chk_Allergen_Peanut)
    st.session_state.pref_Allergen_Soybeans = int(st.session_state.chk_Allergen_Soybeans)


def app():
    with st.form(key="user_pref_form"):
        st.subheader("User Preferences")
        #####################################################################
        # Nutritional Quality
        #####################################################################
        if ("pref_nutritional_quality" in st.session_state):
            if (str(st.session_state.pref_nutritional_quality) == "Important"):
                st.radio("Nutritional Quality", ["Important", "Not Important"], index=0, horizontal=True,
                         key="nutritional_quality")
            else:
                st.radio("Nutritional Quality", ["Important", "Not Important"], index=1, horizontal=True,
                         key="nutritional_quality")
        else:
            st.radio("Nutritional Quality", ["Important", "Not Important"], index=1, horizontal=True,
                     key="nutritional_quality")
        #####################################################################
        # Nova Quality
        #####################################################################
        if ("pref_nova_quality" in st.session_state):
            if (str(st.session_state.pref_nova_quality) == "Important"):
                st.radio("Nova Quality", ["Important", "Not Important"], index=0, horizontal=True, key="nova_quality")
            else:
                st.radio("Nova Quality", ["Important", "Not Important"], index=1, horizontal=True, key="nova_quality")
        else:
            st.radio("Nova Quality", ["Important", "Not Important"], index=1, horizontal=True, key="nova_quality")

        #####################################################################
        st.write("Choose Your Allergens")
        col1, col2, col3 = st.columns(3)
        #####################################################################
        # Milk
        #####################################################################
        if ("pref_Allergen_Milk" in st.session_state):
            if (str(st.session_state.pref_Allergen_Milk) == "1"):
                col1.checkbox("Milk", key="chk_Allergen_Milk", value=True)
            else:
                col1.checkbox("Milk", key="chk_Allergen_Milk", value=False)
        else:
            col1.checkbox("Milk", key="chk_Allergen_Milk", value=False)
        #####################################################################
        # Gluten
        #####################################################################
        if ("pref_Allergen_Gluten" in st.session_state):
            if (str(st.session_state.pref_Allergen_Gluten) == "1"):
                col2.checkbox("Gluten", key="chk_Allergen_Gluten", value=True)
            else:
                col2.checkbox("Gluten", key="chk_Allergen_Gluten", value=False)
        else:
            col2.checkbox("Gluten", key="chk_Allergen_Gluten", value=False)
        #####################################################################
        # Egg
        #####################################################################
        if ("pref_Allergen_Egg" in st.session_state):
            if (str(st.session_state.pref_Allergen_Egg) == "1"):
                col3.checkbox("Egg", key="chk_Allergen_Egg", value=True)
            else:
                col3.checkbox("Egg", key="chk_Allergen_Egg", value=False)
        else:
            col3.checkbox("Egg", key="chk_Allergen_Egg", value=False)
        #####################################################################
        # PeaNut
        #####################################################################
        if ("pref_Allergen_Peanut" in st.session_state):
            if (str(st.session_state.pref_Allergen_Peanut) == "1"):
                col1.checkbox("Peanut", key="chk_Allergen_Peanut", value=True)
            else:
                col1.checkbox("Peanut", key="chk_Allergen_Peanut", value=False)
        else:
            col1.checkbox("Peanut", key="chk_Allergen_Peanut", value=False)
        #####################################################################
        # Nut
        #####################################################################
        if ("pref_Allergen_Nut" in st.session_state):
            if (str(st.session_state.pref_Allergen_Nut) == "1"):
                col2.checkbox("Nut", key="chk_Allergen_Nut", value=True)
            else:
                col2.checkbox("Nut", key="chk_Allergen_Nut", value=False)
        else:
            col2.checkbox("Nut", key="chk_Allergen_Nut", value=False)
        #####################################################################
        # Soybeans
        #####################################################################
        if ("pref_Allergen_Soybeans" in st.session_state):
            if (str(st.session_state.pref_Allergen_Soybeans) == "1"):
                col3.checkbox("Soybeans", key="chk_Allergen_Soybeans", value=True)
            else:
                col3.checkbox("Soybeans", key="chk_Allergen_Soybeans", value=False)
        else:
            col3.checkbox("Soybeans", key="chk_Allergen_Soybeans", value=False)
        #####################################################################
        st.form_submit_button("Save", on_click=save_pref_values, use_container_width=True, type="primary")
