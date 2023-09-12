import streamlit as st
from PIL import Image
def app():
    st.markdown("- 🍽️ Provides consumers with information about food safety, such as product ingredients and allergens.")
    st.markdown("- :dart: Aims to promote food safety practices and increase consumer awareness.")
    st.markdown("- 🥗 Encourages healthy eating habits and helps consumers make informed decisions about food products.")
    st.markdown("- 💪 Empowers you to make safer choices in your product selection journey.")
    #image_url = "https://www.foodsafetynews.com/files/2020/06/Food-Safety-Hero-963x546.png"
    image_url = Image.open("Datasets/resim2.png")
    st.image(image_url, width=450)


if __name__ == "__main__":
    app()
