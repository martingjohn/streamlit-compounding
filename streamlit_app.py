import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import datetime as dt

"""
# Impact of high fees on pension pot

"""

current_year = dt.datetime.now().year

starting_amount=st.number_input("Starting amount",1,1000000,100000)
interest_rate=st.number_input("Stock market growth %",0,100,10)
vanguard_fees=st.number_input("Vanguard fees %age",0.0,100.0,0.14)
active_fees=st.number_input("Active management fees %age",0.0,100.0,1.0)
number_of_years=st.number_input("Number of years",0,100,40)

delta_rate1=1+((interest_rate-vanguard_fees)/100)
delta_rate2=1+((interest_rate-active_fees)/100)

year_series=\
    (
        pd
        .date_range
        (
            start=str(current_year),
            periods=number_of_years,
            freq="1YS"
        )
    )

df=\
    (
        pd
        .DataFrame
        (
            {
                "year":year_series
            }
        )   
    )

df["Year"]=df["year"].dt.strftime("%Y").astype("int64")
df["year"]=df["Year"]-current_year
df["Vanguard"]=round((starting_amount*(delta_rate1**df["year"])),2)
df["Active Management"]=round((starting_amount*(delta_rate2**df["year"])),2)
df["diff"]=df["Vanguard"]-df["Active Management"]
df["diff_percent"]=(df["diff"]/df["Active Management"])*100

max=df["year"].max()
year=int(df.query('year==@max')["Year"].to_string(index=False))
v_amount=float(df.query('year==@max')["Vanguard"].to_string(index=False))
a_amount=float(df.query('year==@max')["Active Management"].to_string(index=False))
diff=float(df.query('year==@max')["diff"].to_string(index=False))
diff_percent=float(df.query('year==@max')["diff_percent"].to_string(index=False))

comment="After {} years, using an active fund lost you £{:,}, returning only £{:,}, rather than Vanguard's £{:,}, a difference of {:.2f}%".format(max+1,diff,a_amount,v_amount,diff_percent)

st.write(comment)

st.line_chart\
    (
        data=df,
        x="year",
        y=["Vanguard","Active Management"]
    )

st.dataframe\
    (
        data=df,
        hide_index=True,
        column_order=["Year","year","Vanguard","Active Management","diff","diff_percent"],
        column_config=\
            {
                "Year":st.column_config.NumberColumn(label="Year",format="%d"),
                "year":st.column_config.NumberColumn(label="Delta Year",format="%d"),
                "Vanguard":st.column_config.NumberColumn(label="Vanguard",format="£%.2f"),
                "Active Management":st.column_config.NumberColumn(label="Active Management",format="£%.2f"),
                "diff":st.column_config.NumberColumn(label="Diff",format="£%.2f"),
                "diff_percent":st.column_config.NumberColumn(label="Diff %age",format="%.2f%%"),
            }
    )
