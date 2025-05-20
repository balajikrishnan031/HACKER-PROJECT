import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

# Load color data
@st.cache_data
def load_colors():
    return pd.read_csv("Colors.csv.csv")  # Ensure this file is in the same folder

color_data = load_colors()

# Function to find closest color
def get_color_name(R, G, B, color_data):
    min_dist = float('inf')
    closest_color = None
    for _, row in color_data.iterrows():
        try:
            d = ((R - int(row['R']))**2 + (G - int(row['G']))**2 + (B - int(row['B']))**2) ** 0.5
            if d < min_dist:
                min_dist = d
                closest_color = row
        except:
            continue
    return closest_color if closest_color is not None else {
        'color_name': 'Unknown',
        'hex': '#000000'
    }

# App UI
st.title("Color Detection App (Click on Image)")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.write("Click anywhere on the image to detect the color")
    coords = streamlit_image_coordinates(image, key="click_image")

    if coords is not None:
        x, y = int(coords['x']), int(coords['y'])
        st.write(f"Coordinates: ({x}, {y})")

        image_np = np.array(image)
        if y < image_np.shape[0] and x < image_np.shape[1]:
            r, g, b = image_np[y, x]
            color_info = get_color_name(r, g, b, color_data)

            st.markdown(f"### Detected Color: {color_info['color_name']}")
            st.markdown(f"RGB: ({r}, {g}, {b})  |  HEX: {color_info['hex']}")
            st.markdown(f"""
                <div style="width:120px;height:50px;background-color:{color_info['hex']};border:1px solid #000;"></div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Click was outside image bounds.")
