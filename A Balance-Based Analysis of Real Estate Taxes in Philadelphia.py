import matplotlib.pyplot as plt
import pandas as pd
#from rich import print

import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("A Balance-Based Analysis of Real Estate Taxes in Philadelphia")

st.write(...) # Add a description/introduction to the dashboard

my_map = folium.Map(location=[39.9526, -75.1652], zoom_start=12)
folium.Marker([39.9526, -75.1652], popup="Philadelphia").add_to(my_map)
st_folium(my_map)

dataFile=pd.read_csv("real_estate_tax_balances_zip_code.csv")
st.subheader("File Contents")
st.dataframe(dataFile)