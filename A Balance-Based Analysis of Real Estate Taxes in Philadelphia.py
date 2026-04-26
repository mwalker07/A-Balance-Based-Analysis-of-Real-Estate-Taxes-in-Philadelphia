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

dataFile["delinquencyPeriod"]=dataFile["max_period"]-dataFile["min_period"]
plt.figure(figsize=(5,3)) #create a scatter plot
plt.scatter(dataFile["delinquencyPeriod"], dataFile["avg_balance"], s=dataFile["num_props"]*2, alpha=0.5) #size of points based on number of properties

plt.xlabel("Delinquency Period (years)") #labels and title
plt.ylabel("Average Balance")
plt.title("Why do some ZIP codes have higher average balances than others? (severity and time)")
plt.grid(True)
st.pyplot(plt) #display the plot in Streamlit

st.subheader("Conclusion") #conclusion based on the analysis
st.write("As a way to sort of visualize/summarize the entire data file I created two visuals that display key trends, and when viewed together, reveal how different aspects of the data are interconnected.")
st.write("  -The bar chart (x-axis: zip code, y-axis: total balances) works to show exactly where real estate tax delinquency is an issue and to what extent, allowing you to compare the scale across neighborhoods.")
st.write("  -The scatter plot answers why there may be a high balance in certain areas. Considering the possibility of long-term unpaid taxes or is it many properties vs a few extreme ones?")
st.write("From this, it can be concluded that most ZIP codes have relatively low or average tax delinquency levels, while a small number of them stand out with disproportionately high balances. However, some of the high-balance areas do not have especially long delinquency periods, suggesting that debts may have accumulated quickly and are not solely determined by how long taxes go unpaid.")

st.divider()

st.write("**An actionable insight is that it would be best to prioritize intervention in a few ZIP codes with unusually high balances, even if delinquency is recent, to prevent large debts from accumulating quickly. Here is a predictive model that is meant to help identify and act early on high-risk ZIP codes (0=low risk, 1=high risk):**")

dataFile["scalePeriod"]=dataFile["delinquencyPeriod"]/dataFile["delinquencyPeriod"].max() #scale delinquency period to a 0-1 range
dataFile["scaleBalance"]=dataFile["avg_balance"]/dataFile["avg_balance"].max()
dataFile["scaleProperties"]=dataFile["num_props"]/dataFile["num_props"].max()

dataFile["riskScore"]=(0.4*dataFile["scaleBalance"]+0.3*dataFile["scalePeriod"]+0.3*dataFile["scaleProperties"]) #risk score based on a weighted average of the three scaled factors

dataSorted=dataFile.sort_values("riskScore", ascending=False) #sort by risk score
fig, ax=plt.subplots(figsize=(13,3))
ax.bar(dataSorted["zip_code"].astype(str), dataSorted["riskScore"])
ax.set_xlabel("ZIP Code")
ax.set_ylabel("Risk Score")
ax.set_title("Predicted Risk of High Real Estate Tax Delinquency")
ax.tick_params(axis="x", rotation=45)
st.pyplot(fig)

#for col in sumColumns:
#    dataFile[col]=pd.to_numeric(dataFile[col], errors="coerce") #----
#dataFile=dataFile.dropna() #drop rows with missing values
#st.subheader("Summary Statistics")
#dataFile["avg_balance"]=dataFile["balance"]/dataFile["num_props"]"""