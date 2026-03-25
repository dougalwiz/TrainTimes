import streamlit as st
import national_rail_api
import pandas as pd

# Page Config for Mobile
st.set_page_config(
    page_title="Train Times",
    page_icon="🚆",
    layout="centered"
)

# Custom CSS to make it feel more like an app
st.markdown("""
    <style>
    .stApp { max-width: 600px; margin: 0 auto; }
    .main-header { font-size: 24px; font-weight: bold; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚆 Train Times")

def display_train_table(title, data):
    st.subheader(title)
    if data == "NO_API_KEY":
        st.error("API key not found. Check config.py.")
    elif data == "INVALID_API_KEY":
        st.error("API key is invalid.")
    elif not data:
        st.info("No train data available.")
    else:
        # Convert list of dicts to a clean DataFrame for the web
        df = pd.DataFrame(data)
        df.columns = ["Departs", "Expected (Dep)", "Arrives", "Expected (Arr)", "Platform"]
        st.dataframe(df, use_container_width=True, hide_index=True)

# Manual Refresh Button
if st.button('🔄 Refresh Data', use_container_width=True):
    st.rerun()

# Get Data
gld_to_wat = national_rail_api.get_departures("Guildford", "London Waterloo")
wat_to_gld = national_rail_api.get_departures("London Waterloo", "Guildford")

# Display Tables
display_train_table("📍 Guildford → Waterloo", gld_to_wat)
st.divider()
display_train_table("📍 Waterloo → Guildford", wat_to_gld)
