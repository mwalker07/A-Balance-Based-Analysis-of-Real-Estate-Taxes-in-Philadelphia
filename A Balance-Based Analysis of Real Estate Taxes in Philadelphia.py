import matplotlib.pyplot as plt
import pandas as pd
#from rich import print

import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("A Balance-Based Analysis of Real Estate Taxes in Philadelphia")

st.write("This project analyzes a dataset published on OpenDataPhilly, which summarizes delinquent real estate taxes in the city of Philadelphia (categorized by ZIP code). Each column is a piece of a larger picture, and together they show how tax debt varies across different areas.") #introduction

my_map = folium.Map(location=[39.9526, -75.1652], zoom_start=12, width=300, height=200)
#location=[39.9526, -75.1652], zoom_start=12) #map centered on Philadelphia
#folium.Marker([39.9526, -75.1652], popup="Philadelphia").add_to(my_map)
st_folium(my_map)

dataFile=pd.read_csv("real_estate_tax_balances_zip_code.csv") #load the data file
st.subheader("File Contents") #display the contents of the data file, working as a summary
st.dataframe(dataFile)

dataFile.columns=dataFile.columns.str.strip().str.lower().str.replace(" ", "_")
sumColumns=["num_props", "principal", "interest", "panalty", "other", "balance"]

byZIPCode=dataFile.groupby("zip_code").agg({"balance":"sum", "num_props":"sum", "avg_balance":"mean"}).reset_index()

st.divider()

st.bar_chart(byZIPCode.set_index("zip_code")["balance"])

#for col in sumColumns:
#    dataFile[col]=pd.to_numeric(dataFile[col], errors="coerce") #----
#dataFile=dataFile.dropna() #drop rows with missing values
#st.subheader("Summary Statistics")
#dataFile["avg_balance"]=dataFile["balance"]/dataFile["num_props"]"""