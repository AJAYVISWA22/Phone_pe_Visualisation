import streamlit as st
from PIL import Image
import os
import requests
import json
from streamlit_option_menu import option_menu
import pandas as pd
import sqlite3
import plotly.express as px
import humanize


# Reading the data from csv files
df_aggregated_transaction=pd.read_csv('agg_trans.csv')
df_aggregated_user=pd.read_csv('agg_user.csv')
df_aggregated_insurance=pd.read_csv('agg_insr.csv')

df_map_transaction=pd.read_csv('map_trans.csv')
df_map_user=pd.read_csv('map_user.csv')
df_map_insurance=pd.read_csv('map_insr.csv')

df_top_transaction=pd.read_csv('top_trans.csv')
df_top_user=pd.read_csv('top_user.csv')
df_top_insurance=pd.read_csv('top_insr.csv')


# CREATING CONNECTION WITH SQL SERVER
def df_to_sql():
    conn = sqlite3.connect("phonepe_pulse.db")
    cursor = conn.cursor()

    # Inserting each Data frame into sql server
    df_aggregated_transaction.to_sql('aggregated_transaction', conn, if_exists='replace',index=False)
    df_aggregated_user.to_sql('aggregated_user', conn, if_exists='replace',index=False)
    df_aggregated_insurance.to_sql('aggregated_insurance', conn, if_exists='replace',index=False)

    df_map_transaction.to_sql('map_transaction', conn, if_exists='replace',index=False)
    df_map_user.to_sql('map_user', conn, if_exists='replace',index=False)
    df_map_insurance.to_sql('map_insurance', conn, if_exists='replace',index=False)

    df_top_transaction.to_sql('top_transaction', conn, if_exists='replace',index=False)
    df_top_user.to_sql('top_user', conn, if_exists='replace',index=False)
    df_top_insurance.to_sql('top_insurance', conn, if_exists='replace',index=False)
    conn.close()


df_to_sql()




#Retriving Data from Sql

conn = sqlite3.connect("phonepe_pulse.db")
cursor = conn.cursor()

# Fetch data and convert to DataFrame
cursor.execute("select * from aggregated_insurance;")
table7 = cursor.fetchall()
Aggre_insurance = pd.DataFrame(table7, columns=["States", "Years", "Quarter", "Insurance_type", "Insurance_count", "Insurance_amount"])

cursor.execute("select * from aggregated_transaction;")
table1 = cursor.fetchall()
Aggre_transaction = pd.DataFrame(table1, columns=["States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"])

cursor.execute("select * from aggregated_user;")
table2 = cursor.fetchall()
Aggre_user = pd.DataFrame(table2, columns=["States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"])




cursor.execute("select * from map_insurance;")
table3 = cursor.fetchall()
Map_insurance = pd.DataFrame(table3, columns=["States", "Years", "Quarter", "Districts", "Insurance_count", "Insurance_amount"])

cursor.execute("select * from map_transaction;")
table3 = cursor.fetchall()
Map_transaction = pd.DataFrame(table3, columns=["States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"])

cursor.execute("select * from map_user;")
table4 = cursor.fetchall()
Map_user = pd.DataFrame(table4, columns=["States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"])




cursor.execute("select * from top_insurance;")
table5 = cursor.fetchall()
Top_insurance = pd.DataFrame(table5, columns=["States", "Years", "Quarter", "Pincodes", "Insurance_count", "Insurance_amount"])

cursor.execute("select * from top_transaction;")
table5 = cursor.fetchall()
Top_transaction = pd.DataFrame(table5, columns=["States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"])

cursor.execute("select * from top_user;")
table6 = cursor.fetchall()
Top_user = pd.DataFrame(table6, columns=["States", "Years", "Quarter", "Pincodes", "RegisteredUser"])





phn=Image.open('images/phonepe-logo-icon.png')
phn1=Image.open('images/phonepe.png')
video_file = open('vedios/Phonepe.mp4', 'rb')
video2= video_file.read()




def Aggre_transaction_Y(df,year):
    aiy= df[df["Years"] == year]
    aiy.reset_index(drop= True, inplace= True)

    aiyg=aiy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    aiyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(aiyg, x="States", y= "Transaction_amount",title= f"{year} TRANSACTION AMOUNT",
                        width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        fig_amount.update_layout(xaxis_tickangle=-45)
        
        st.plotly_chart(fig_amount)
    with col2:

        fig_count= px.bar(aiyg, x="States", y= "Transaction_count",title= f"{year} TRANSACTION COUNT",
                        width=600, height= 650, color_discrete_sequence=px.colors.sequential.Bluered_r)
        fig_count.update_layout(xaxis_tickangle=-45)
        
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()
        

        fig_india_1= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                range_color= (aiyg["Transaction_amount"].min(),aiyg["Transaction_amount"].max()),
                                hover_name= "States",title = f"{year} TRANSACTION AMOUNT",
                                fitbounds= "locations",width =600, height= 600)
        
        fig_india_1.update_geos(
        projection=dict(
            type="mercator",  # You can try other types like 'orthographic', 'natural earth', etc.
            rotation=dict(
                lon=30,  
                lat=30, 
                roll=40  # Adjust the roll for additional slant
            )
        ),
        fitbounds="locations",
        visible=False
        )

        # Update the layout to make the figure wider and set the background to black
        fig_india_1.update_layout(
            width=800,                     # Adjust the width to a larger size
            height=800,                    # Adjust the height to a larger size
            paper_bgcolor='black',         # Set the paper background color to black
            plot_bgcolor='black',          # Set the plot background color to black
            font=dict(color='violet')      # Set the font color to white for better visibility
            )
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                range_color= (aiyg["Transaction_count"].min(),aiyg["Transaction_count"].max()),
                                hover_name= "States",title = f"{year} TRANSACTION COUNT",
                                fitbounds= "locations",width =600, height= 600)
        
        fig_india_2.update_geos(
        projection=dict(
            type="mercator",  # You can try other types like 'orthographic', 'natural earth', etc.
            rotation=dict(
                lon=30,  
                lat=30, 
                roll=40  # Adjust the roll for additional slant
            )
        ),
        fitbounds="locations",
        visible=False
        )

        # Update the layout to make the figure wider and set the background to black
        fig_india_2.update_layout(
            width=800,  # Adjust the width to a larger size
            height=800,  # Adjust the height to a larger size
            paper_bgcolor='black',  # Set the paper background color to black
            plot_bgcolor='black',   # Set the plot background color to black
            font=dict(color='violet')  # Set the font color to white for better visibility
            )
        
        st.plotly_chart(fig_india_2)

    return aiy


def Aggre_transaction_Y_Q(df,quarter):
    aiyq= df[df["Quarter"] == quarter]
    aiyq.reset_index(drop= True, inplace= True)

    aiyqg= aiyq.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    aiyqg.reset_index(inplace= True)

    col1,col2= st.columns(2)

    with col1:
        fig_q_amount= px.bar(aiyqg, x= "States", y= "Transaction_amount", 
                            title= f"{aiyq['Years'].min()} AND {quarter} TRANSACTION AMOUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Burg_r)
        fig_q_amount.update_layout(xaxis_tickangle=-45)
        
        
        st.plotly_chart(fig_q_amount)

    with col2:
        fig_q_count= px.bar(aiyqg, x= "States", y= "Transaction_count", 
                            title= f"{aiyq['Years'].min()} AND {quarter} TRANSACTION COUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Cividis_r)
        fig_q_count.update_layout(xaxis_tickangle=-45)
       
        st.plotly_chart(fig_q_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()

        fig_india_1= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                range_color= (aiyqg["Transaction_amount"].min(),aiyqg["Transaction_amount"].max()),
                                hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} TRANSACTION AMOUNT",
                                fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(
        projection=dict(
            type="mercator",  # You can try other types like 'orthographic', 'natural earth', etc.
            rotation=dict(
                lon=30,  
                lat=30, 
                roll=40  # Adjust the roll for additional slant
            )
        ),
        fitbounds="locations",
        visible=False
        )

        # Update the layout to make the figure wider and set the background to black
        fig_india_1.update_layout(
            width=800,  # Adjust the width to a larger size
            height=800,  # Adjust the height to a larger size
            paper_bgcolor='black',  # Set the paper background color to black
            plot_bgcolor='black',   # Set the plot background color to black
            font=dict(color='violet')  # Set the font color to white for better visibility
            )
        
        st.plotly_chart(fig_india_1)
    with col2:

        fig_india_2= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                range_color= (aiyqg["Transaction_count"].min(),aiyqg["Transaction_count"].max()),
                                hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} TRANSACTION COUNT",
                                fitbounds= "locations",width =600, height= 600)
        
        fig_india_2.update_geos(
        projection=dict(
            type="mercator",  # You can try other types like 'orthographic', 'natural earth', etc.
            rotation=dict(
                lon=30,  
                lat=30, 
                roll=40  # Adjust the roll for additional slant
            )
        ),
        fitbounds="locations",
        visible=False
        )

        # Update the layout to make the figure wider and set the background to black
        fig_india_2.update_layout(
            width=800,  # Adjust the width to a larger size
            height=800,  # Adjust the height to a larger size
            paper_bgcolor='black',  # Set the paper background color to black
            plot_bgcolor='black',   # Set the plot background color to black
            font=dict(color='violet')  # Set the font color to white for better visibility
            )
        
        st.plotly_chart(fig_india_2)
    
    return aiyq

def Aggre_Transaction_type(df, state):
    df_state= df[df["States"] == state]
    df_state.reset_index(drop= True, inplace= True)

    agttg= df_state.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    agttg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_hbar_1= px.bar(agttg, x= "Transaction_count", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width= 600, 
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION COUNT",height= 500)
        #fig_hbar_1.update_layout(xaxis_tickangle=-45)
        
        st.plotly_chart(fig_hbar_1)

    with col2:

        fig_hbar_2= px.bar(agttg, x= "Transaction_amount", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 600,
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION AMOUNT", height= 500)
        #fig_hbar_2.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_hbar_2)
        
def Aggre_user_plot_1(df,year):
    aguy= df[df["Years"] == year]
    aguy.reset_index(drop= True, inplace= True)
    
    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_line_1= px.bar(aguyg, x="Brands",y= "Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(fig_line_1)

    return aguy

def Aggre_user_plot_2(df,quarter):
    auqs= df[df["Quarter"] == quarter]
    auqs.reset_index(drop= True, inplace= True)

    fig_pie_1= px.pie(data_frame=auqs, names= "Brands", values="Transaction_count", hover_data= "Percentage",
                    width=1000,title=f"{quarter} QUARTER TRANSACTION COUNT PERCENTAGE",hole=0.5, color_discrete_sequence= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)

    return auqs

def Aggre_user_plot_3(df,state):
    aguqy= df[df["States"] == state]
    aguqy.reset_index(drop= True, inplace= True)

    aguqyg= pd.DataFrame(aguqy.groupby("Brands")["Transaction_count"].sum())
    aguqyg.reset_index(inplace= True)

    fig_scatter_1= px.line(aguqyg, x= "Brands", y= "Transaction_count",title=f"{state}\'s  BRANDS AND  TRANSACTION COUNT ", markers= True,width=1000)
    st.plotly_chart(fig_scatter_1)



def Aggre_insurance_Y(df, year):
    aiy = df[df["Years"] == year]
    aiy.reset_index(drop=True, inplace=True)

    aiyg = aiy.groupby("States")[["Insurance_count", "Insurance_amount"]].sum()
    aiyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(aiyg, x="States", y="Insurance_amount", title=f"{year} INSURANCE AMOUNT",
                            width=600, height=650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        fig_amount.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count = px.bar(aiyg, x="States", y="Insurance_count", title=f"{year} INSURANCE COUNT",
                           width=600, height=650, color_discrete_sequence=px.colors.sequential.Bluered_r)
        fig_count.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_count)

    col1, col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states_name_tra = [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()

        fig_india_1 = px.choropleth(aiyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color="Insurance_amount", color_continuous_scale="Sunsetdark",
                                    range_color=(aiyg["Insurance_amount"].min(), aiyg["Insurance_amount"].max()),
                                    hover_name="States", title=f"{year} INSURANCE AMOUNT",
                                    fitbounds="locations", width=600, height=600)

        fig_india_1.update_geos(
            projection=dict(
                type="mercator",
                rotation=dict(lon=30, lat=30, roll=40)
            ),
            fitbounds="locations",
            visible=False
        )

        fig_india_1.update_layout(
            width=800,
            height=800,
            paper_bgcolor='black',
            plot_bgcolor='black',
            font=dict(color='violet')
        )
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth(aiyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color="Insurance_count", color_continuous_scale="Sunsetdark",
                                    range_color=(aiyg["Insurance_count"].min(), aiyg["Insurance_count"].max()),
                                    hover_name="States", title=f"{year} INSURANCE COUNT",
                                    fitbounds="locations", width=600, height=600)

        fig_india_2.update_geos(
            projection=dict(
                type="mercator",
                rotation=dict(lon=30, lat=30, roll=40)
            ),
            fitbounds="locations",
            visible=False
        )

        fig_india_2.update_layout(
            width=800,
            height=800,
            paper_bgcolor='black',
            plot_bgcolor='black',
            font=dict(color='violet')
        )
        st.plotly_chart(fig_india_2)

    return aiy


def Aggre_insurance_Y_Q(df, quarter):
    aiyq = df[df["Quarter"] == quarter]
    aiyq.reset_index(drop=True, inplace=True)

    aiyqg = aiyq.groupby("States")[["Insurance_count", "Insurance_amount"]].sum()
    aiyqg.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_q_amount = px.bar(aiyqg, x="States", y="Insurance_amount",
                              title=f"{aiyq['Years'].min()} AND {quarter} INSURANCE AMOUNT", width=600, height=650,
                              color_discrete_sequence=px.colors.sequential.Burg_r)
        fig_q_amount.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_q_amount)

    with col2:
        fig_q_count = px.bar(aiyqg, x="States", y="Insurance_count",
                             title=f"{aiyq['Years'].min()} AND {quarter} INSURANCE COUNT", width=600, height=650,
                             color_discrete_sequence=px.colors.sequential.Cividis_r)
        fig_q_count.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_q_count)

    col1, col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states_name_tra = [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()

        fig_india_1 = px.choropleth(aiyqg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color="Insurance_amount", color_continuous_scale="Sunsetdark",
                                    range_color=(aiyqg["Insurance_amount"].min(), aiyqg["Insurance_amount"].max()),
                                    hover_name="States", title=f"{aiyq['Years'].min()} AND {quarter} INSURANCE AMOUNT",
                                    fitbounds="locations", width=600, height=600)
        fig_india_1.update_geos(
            projection=dict(
                type="mercator",
                rotation=dict(lon=30, lat=30, roll=40)
            ),
            fitbounds="locations",
            visible=False
        )

        fig_india_1.update_layout(
            width=800,
            height=800,
            paper_bgcolor='black',
            plot_bgcolor='black',
            font=dict(color='violet')
        )
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2 = px.choropleth(aiyqg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color="Insurance_count", color_continuous_scale="Sunsetdark",
                                    range_color=(aiyqg["Insurance_count"].min(), aiyqg["Insurance_count"].max()),
                                    hover_name="States", title=f"{aiyq['Years'].min()} AND {quarter} INSURANCE COUNT",
                                    fitbounds="locations", width=600, height=600)

        fig_india_2.update_geos(
            projection=dict(
                type="mercator",
                rotation=dict(lon=30, lat=30, roll=40)
            ),
            fitbounds="locations",
            visible=False
        )

        fig_india_2.update_layout(
            width=800,
            height=800,
            paper_bgcolor='black',
            plot_bgcolor='black',
            font=dict(color='violet')
        )
        st.plotly_chart(fig_india_2)

    return aiyq








def map_trans_plot_1(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(miysg, x= "Districts", y= "Transaction_amount",
                            width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                            color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_1= px.bar(miysg, x= "Districts", y= "Transaction_count",
                            width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                            color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_bar_1)



def map_trans_plot_2(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_pie_1= px.pie(miysg, names= "Districts", values= "Transaction_amount",
                            width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                            hole=0.5,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_1)

    with col2:
        fig_map_pie_1= px.pie(miysg, names= "Districts", values= "Transaction_count",
                            width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                            hole=0.5,  color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_pie_1)


def map_insure_plot_1(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("Districts")[["Insurance_count","Insurance_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(miysg, x= "Districts", y= "Insurance_amount",
                            width=600, height=500, title= f"{state.upper()} DISTRICTS INSURANCE AMOUNT",
                            color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_1= px.bar(miysg, x= "Districts", y= "Insurance_count",
                            width=600, height= 500, title= f"{state.upper()} DISTRICTS INSURANCE COUNT",
                            color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_bar_1)

def map_insure_plot_2(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("Districts")[["Insurance_count","Insurance_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_pie_1= px.pie(miysg, names= "Districts", values= "Insurance_amount",
                            width=600, height=500, title= f"{state.upper()} DISTRICTS INSURANCE AMOUNT",
                            hole=0.5,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_1)

    with col2:
        fig_map_pie_1= px.pie(miysg, names= "Districts", values= "Insurance_count",
                            width=600, height= 500, title= f"{state.upper()} DISTRICTS Insurance COUNT",
                            hole=0.5,  color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_pie_1)

def map_user_plot_1(df, year):
    muy= df[df["Years"] == year]
    muy.reset_index(drop= True, inplace= True)
    muyg= muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyg, x= "States", y= ["RegisteredUser","AppOpens"], markers= True,
                                width=2000,title= f"{year} REGISTERED USER AND APPOPENS", color_discrete_sequence= px.colors.sequential.Viridis_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muy

def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"] == quarter]
    muyq.reset_index(drop= True, inplace= True)
    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyqg, x= "States", y= ["RegisteredUser","AppOpens"], markers= True,
                                title= f"{df['Years'].min()}, {quarter} QUARTER REGISTERED USER AND APPOPENS",
                                width= 2000,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muyq

def map_user_plot_3(df, state):
    muyqs= df[df["States"] == state]
    muyqs.reset_index(drop= True, inplace= True)
    muyqsg= muyqs.groupby("Districts")[["RegisteredUser", "AppOpens"]].sum()
    muyqsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_plot_1= px.bar(muyqsg, x= "RegisteredUser",y= "Districts",orientation="h",
                                    title= f"{state.upper()} REGISTERED USER",
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_plot_1)

    with col2:
        fig_map_user_plot_2= px.bar(muyqsg, x= "AppOpens", y= "Districts",orientation="h",
                                    title= f"{state.upper()} APPOPENS",
                                    color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_plot_2)

def top_user_plot_1(df,year):
    tuy= df[df["Years"] == year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUser"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUser", barmode= "group", color= "Quarter",
                            title= f"REGISTERED USERS FOR THE YEAR {year} ",width=1000, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_plot_1)

    return tuy

def top_user_plot_2(df,state):
    tuys= df[df["States"] == state]
    tuys.reset_index(drop= True, inplace= True)

    tuysg= pd.DataFrame(tuys.groupby("Quarter")["RegisteredUser"].sum())
    tuysg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuys, x= "Quarter", y= "RegisteredUser",barmode= "group",
                        width=1000, height= 600,color= "RegisteredUser",
                        title= f"{state.upper()} REGISTERED USER",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_1)


def store_feedback(feedback_text):
    conn = sqlite3.connect('phonepe_pulse.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO FEEDBACK (feedback) VALUES (?)", (feedback_text,))
    conn.commit()
    conn.close()

def menu_Home():
    st.title("Welcome to PhonePe Pulse")
    st.subheader("The Indian digital payments story has truly captured the world's imagination.")
    
    st.write("""
    From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet, and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government.
    Founded in December 2015, PhonePe has been a strong beneficiary of the API-driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India.
    PhonePe Pulse is our way of giving back to the digital payments ecosystem.
    """)

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Phonepe Now Everywhere..!")
        st.image(phn1)
        st.markdown("[DOWNLOAD THE APP NOW](https://www.phonepe.com/app-download/)", unsafe_allow_html=True)

    with col2:
        st.subheader("Solution for Everything")
        st.video(video2)

    # Add interactive elements
    st.write("## How PhonePe Pulse Data Visualization works")
    st.write("""
    PhonePe Pulse Data Visualization brings you all the insights about digital payments in India. Explore the data and discover trends in transactions, registered users, and more.
    """)

    st.write("### Select Your Interest Area")
    interest = st.selectbox("Choose an area to explore:", ["Transactions", "Registered Users", "Top States"])

    if interest == "Transactions":
        st.write("## Transaction Insights")
        st.write("Explore detailed insights on transactions across different states and years.")
        # Add more interactive elements like charts, tables, etc.
    
    elif interest == "Registered Users":
        st.write("## Registered User Insights")
        st.write("Discover the trends and insights about registered users across India.")
        # Add more interactive elements like charts, tables, etc.

    elif interest == "Top States":
        st.write("## Top States in Digital Payments")
        st.write("Find out which states are leading in digital payments.")
        # Add more interactive elements like charts, tables, etc.

    st.write("## Feedback")
    feedback = st.text_area("We would love to hear your thoughts or feedback!", "")
    if st.button("Submit Feedback"):
        store_feedback(feedback)
        st.write("Thank you for your feedback!")




def menu_Data_Exploration():

    Tabs = option_menu(
    menu_title=None,
    options=["Aggregated Analysis","Map Analysis", "Top Analysis"],
    icons=["graph-up", "globe", "bar-chart"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "white", "size": "cover"},
        "icon": {"color": "black", "font-size": "18px"},
        "nav-link": {"font-size": "18px", "text-align": "center", "margin": "-2px", 
                    "--hover-color": "#6F36AD", "color": "#6F36AD","font-weight": "bold"},
        "nav-link-selected": {"background-color": "#6F36AD", "color": "white"}
    } )


    if Tabs=="Aggregated Analysis":
        left_col, center_col1, midle, center_col2, right_col = st.columns([1, 2, 1, 2, 1])

        with center_col1:
            method = st.radio("**Select the Analysis Method**", ["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":
            with center_col2:
                # Convert the years column to a set to get unique values
                unique_years = Aggre_insurance["Years"].unique()

                # Create radio buttons for year selection
                years = st.radio("**Select the Year**", unique_years)

            df_agg_insur_Y = Aggre_insurance_Y(Aggre_insurance, years)

            col4, center_col, col5 = st.columns([1, 2, 1])
            with center_col:
                unique_quarters = df_agg_insur_Y["Quarter"].unique()
                quarters = st.selectbox("**Select the Quarter**", unique_quarters)

            Aggre_insurance_Y_Q(df_agg_insur_Y, quarters)

        elif method == "Transaction Analysis":
            with center_col2:
                unique_years_at = Aggre_transaction["Years"].unique()
                years_at = st.radio("**Select the Year**", unique_years_at)

            df_agg_tran_Y = Aggre_transaction_Y(Aggre_transaction, years_at)

            col4, center_col, col5 = st.columns([1, 2, 1])
            with center_col:
                unique_quarters_at = df_agg_tran_Y["Quarter"].unique()
                quarters_at = st.selectbox("**Select the Quarter**", unique_quarters_at)

            df_agg_tran_Y_Q = Aggre_transaction_Y_Q(df_agg_tran_Y, quarters_at)

            state_Y_Q = st.selectbox("**Select the State**", df_agg_tran_Y_Q["States"].unique())

            Aggre_Transaction_type(df_agg_tran_Y_Q, state_Y_Q)

        elif method == "User Analysis":
            year_au = st.selectbox("Select the Year", Aggre_user["Years"].unique())
            col4, center_col, col5 = st.columns([1, 2, 1])
            with center_col:
                agg_user_Y = Aggre_user_plot_1(Aggre_user, year_au)

            quarter_au = st.selectbox("Select the Quarter", agg_user_Y["Quarter"].unique())
            col4, center_col, col5 = st.columns([1, 2, 1])
            with center_col:
                agg_user_Y_Q = Aggre_user_plot_2(agg_user_Y, quarter_au)

            state_au = st.selectbox("**Select the State**", agg_user_Y["States"].unique())
            col4, center_col, col5 = st.columns([1, 2, 1])
            with center_col:
                Aggre_user_plot_3(agg_user_Y_Q, state_au)

    if Tabs=="Map Analysis":
        left_col, center_col1, midle, center_col2, right_col = st.columns([1, 2, 1, 2, 1])

        with center_col1:
            method_map = st.radio("**Select the Analysis Method(MAP)**", ["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])

        if method_map == "Map Insurance Analysis":
            with center_col2:
                years_m1 = st.radio("**Select the Year**", Map_insurance["Years"].unique())

            df_map_insur_Y = Aggre_insurance_Y(Map_insurance, years_m1)

            col4, center_col, col5 = st.columns([1, 2, 1])
            with center_col:
                quarters_m1 = st.selectbox("**Select the Quarter**", df_map_insur_Y["Quarter"].unique())

            df_map_insur_Y_Q = Aggre_insurance_Y_Q(df_map_insur_Y, quarters_m1)

            col6, center_col, col7 = st.columns([1, 2, 1])
            with center_col:
                state = st.selectbox("Select the State", df_map_insur_Y_Q["States"].unique())
            map_insure_plot_1(df_map_insur_Y, state)

            
            map_insure_plot_2(df_map_insur_Y_Q, state)

        elif method_map == "Map Transaction Analysis":
            with center_col2:
                years_m2 = st.radio("**Select the Year**", Map_transaction["Years"].unique())

            df_map_tran_Y = Aggre_transaction_Y(Map_transaction, years_m2)

            col4, center_col, col5 = st.columns([1, 2, 1])
            with center_col:
                quarters_m2 = st.selectbox("**Select the Quarter**", df_map_tran_Y["Quarter"].unique())

            df_map_tran_Y_Q = Aggre_transaction_Y_Q(df_map_tran_Y, quarters_m2)

            col6, center_col, col7 = st.columns([1, 2, 1])
            with center_col:
                state = st.selectbox("Select the State", df_map_tran_Y_Q["States"].unique())

            map_trans_plot_1(df_map_tran_Y, state)

    
            map_trans_plot_2(df_map_tran_Y_Q, state)

        elif method_map == "Map User Analysis":

            year_mu1 = st.selectbox("**Select the Year**", Map_user["Years"].unique())

            col4, center_col, col5 = st.columns([1, 2, 1])
            with col4 and col5:
                st.write("")
            with center_col:
                map_user_Y = map_user_plot_1(Map_user, year_mu1)

            quarter_mu1 = st.selectbox("**Select the Quarter**", map_user_Y["Quarter"].unique())
            col4, center_col, col5 = st.columns([1, 2, 1])
            with col4 and col5:
                st.write("")
            with center_col:
                map_user_Y_Q = map_user_plot_2(map_user_Y, quarter_mu1)

            state_mu1 = st.selectbox("**Select the State**", map_user_Y_Q["States"].unique())
            map_user_plot_3(map_user_Y_Q, state_mu1)


    if Tabs=="Top Analysis":
        left_col, center_col1, midle, center_col2, right_col = st.columns([1, 2, 1, 2, 1])

        with center_col1:
            method_top = st.radio("**Select the Analysis Method(TOP)**", ["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])

        if method_top == "Top Insurance Analysis":
            with center_col2:
                years_t1 = st.radio("**Select the Year**", Top_insurance["Years"].unique())

            df_top_insur_Y = Aggre_insurance_Y(Top_insurance, years_t1)

            col4, center_col, col5 = st.columns([1, 2, 1])
            with center_col:
                quarters_t1 = st.selectbox("**Select the Quarter**", df_top_insur_Y["Quarter"].unique())

            df_top_insur_Y_Q = Aggre_insurance_Y_Q(df_top_insur_Y, quarters_t1)

        elif method_top == "Top Transaction Analysis":
            with center_col2:
                years_t2 = st.radio("**Select the Year**", Top_transaction["Years"].unique())

            df_top_tran_Y = Aggre_transaction_Y(Top_transaction, years_t2)

            col4, center_col, col5 = st.columns([1, 2, 1])
            with center_col:
                quarters_t2 = st.selectbox("**Select the Quarter**", df_top_tran_Y["Quarter"].unique())

            df_top_tran_Y_Q = Aggre_transaction_Y_Q(df_top_tran_Y, quarters_t2)

        elif method_top == "Top User Analysis":
            
            years_t3 = st.selectbox("**Select the Year**", Top_user["Years"].unique())

            df_top_user_Y = top_user_plot_1(Top_user, years_t3)

            col4, center_col, col5 = st.columns([1, 2, 1])
            with center_col:
                state_t3 = st.selectbox("**Select the State**", df_top_user_Y["States"].unique())

            df_top_user_Y_S = top_user_plot_2(df_top_user_Y, state_t3)


def menu_Search():
    Topic = ["","Brand","District","Registered-users","Top-Transactions","Transaction-Type"]
    choice_topic = st.selectbox("Search by",Topic)
    

    #creating functions for query search in sqlite to get the data
    def type_(type):
        cursor.execute(f"SELECT DISTINCT States,Quarter,Years,Transaction_type,Transaction_amount FROM aggregated_transaction WHERE Transaction_type = '{type}' ORDER BY States,Quarter,Years")
        df = pd.DataFrame(cursor.fetchall(), columns=['States','Quarter', 'Years', 'Transaction_type', 'Transaction_amount'])
        return df

    def type_year(year, type):
        cursor.execute(f"SELECT DISTINCT States,Years,Quarter,Transaction_type,Transaction_amount FROM aggregated_transaction WHERE Years = '{year}' AND Transaction_type = '{type}' ORDER BY States,Quarter,Years")
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Years',"Quarter", 'Transaction_type', 'Transaction_amount'])
        return df

    def type_state(state, year, type):
        cursor.execute(f"SELECT DISTINCT States,Years,Quarter,Transaction_type,Transaction_amount FROM aggregated_transaction WHERE States = '{state}' AND Transaction_type = '{type}' And Years = '{year}' ORDER BY States,Quarter,Years")
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Years',"Quarter", 'Transaction_type', 'Transaction_amount'])
        return df

    def district_choice_state(_state):
        cursor.execute(f"SELECT DISTINCT States,Years,Quarter,Districts,Transaction_amount FROM map_transaction WHERE States = '{_state}' ORDER BY States,Years,Quarter,Districts")
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Years',"Quarter", 'Districts', 'Transaction_amount'])
        return df

    def dist_year_state(year, _state):
        cursor.execute(f"SELECT DISTINCT States,Years,Quarter,Districts,Transaction_amount FROM map_transaction WHERE Years = '{year}' AND States = '{_state}' ORDER BY States,Years,Quarter,Districts")
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Years',"Quarter", 'Districts', 'Transaction_amount'])
        return df

    def district_year_state(_dist, year, _state):
        cursor.execute(f"SELECT DISTINCT States,Years,Quarter,Districts,Transaction_amount FROM map_transaction WHERE Districts = '{_dist}' AND States = '{_state}' AND Years = '{year}' ORDER BY States,Years,Quarter,Districts")
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Years',"Quarter", 'Districts', 'Transaction_amount'])
        return df

    def brand_(brand_type):
        cursor.execute(f"SELECT States,Years,Quarter,brands,Transaction_count FROM aggregated_user WHERE brands='{brand_type}' ORDER BY States,Years,Quarter,brands,Transaction_count DESC")
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Years',"Quarter", 'brands', 'Transaction_count'])
        return df

    def brand_year(brand_type, year):
        cursor.execute(f"SELECT States,Years,Quarter,brands,Transaction_count FROM aggregated_user WHERE Years = '{year}' AND brands='{brand_type}' ORDER BY States,Years,Quarter,brands,Transaction_count DESC")
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Years',"Quarter", 'brands', 'Transaction_count'])
        return df

    def brand_state(state, brand_type, year):
        cursor.execute(f"SELECT States,Years,Quarter,brands,Transaction_count FROM aggregated_user WHERE States = '{state}' AND brands='{brand_type}' AND Years = '{year}' ORDER BY States,Years,Quarter,brands,Transaction_count DESC")
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Years',"Quarter", 'brands', 'Transaction_count'])
        return df

    def transaction_state(_state):
        cursor.execute(f"SELECT States,Years,Quarter,Transaction_count,Transaction_amount FROM top_transaction WHERE States = '{_state}' GROUP BY States,Years,Quarter")
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Years',"Quarter", 'Transaction_count', 'Transaction_amount'])
        return df

    def transaction_year(_state, _year):
        cursor.execute(f"SELECT States,Years,Quarter,Transaction_count,Transaction_amount FROM top_transaction WHERE Years = '{_year}' AND States = '{_state}' GROUP BY States,Years,Quarter")
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Years',"Quarter", 'Transaction_count', 'Transaction_amount'])
        return df

    def transaction_quarter(_state, _year, _quarter):
        cursor.execute(f"SELECT States,Years,Quarter,Transaction_count,Transaction_amount FROM top_transaction WHERE Years = '{_year}' AND Quarter = '{_quarter}' AND States = '{_state}' GROUP BY States,Years,Quarter")
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Years',"Quarter", 'Transaction_count', 'Transaction_amount'])
        return df

    def registered_user_state(_state):
        cursor.execute(f"SELECT States,Years,Quarter,Districts,RegisteredUser FROM map_user WHERE States = '{_state}' ORDER BY States,Years,Quarter,Districts")
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Years',"Quarter", 'Districts', 'RegisteredUser'])
        return df

    def registered_user_year(_state, _year):
        cursor.execute(f"SELECT States,Years,Quarter,Districts,RegisteredUser FROM map_user WHERE Years = '{_year}' AND States = '{_state}' ORDER BY States,Years,Quarter,Districts")
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Years',"Quarter", 'Districts', 'RegisteredUser'])
        return df

    def registered_user_district(_state, _year, _dist):
        cursor.execute(f"SELECT States,Years,Quarter,Districts,RegisteredUser FROM map_user WHERE Years = '{_year}' AND States = '{_state}' AND Districts = '{_dist}' ORDER BY States,Years,Quarter,Districts")
        df = pd.DataFrame(cursor.fetchall(), columns=['States', 'Years',"Quarter", 'Districts', 'RegisteredUser'])
        return df

    def format_df_tx_type(df):
        df['Years'] = df['Years'].apply(lambda x: f"{int(x):04d}")
        df['Transaction_amount'] = df['Transaction_amount'].apply(humanize.intword)
        return df
    
    def format_df_top_tx(df):
        df['Years'] = df['Years'].apply(lambda x: f"{int(x):04d}")
        df['Transaction_count'] = df['Transaction_count'].apply(humanize.intword)
        df['Transaction_amount'] = df['Transaction_amount'].apply(humanize.intword)
        return df
    
    def reg_users(df):
        df['Years'] = df['Years'].apply(lambda x: f"{int(x):04d}")
        df['RegisteredUser'] = df['RegisteredUser'].apply(humanize.intword)
        return df

    def format_brand(df):
        df['Years'] = df['Years'].apply(lambda x: f"{int(x):04d}")
        df['Transaction_count'] = df['Transaction_count'].apply(humanize.intword)
        return df







    
    if choice_topic == "Transaction-Type":
        select = st.selectbox('SELECT VIEW', ['Tabular view', 'Plotly View'], 0)
        if select=='Tabular view':
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader(" SELECT TYPE OF TRANSACTION ")
                trx_tpe=Aggre_transaction["Transaction_type"].unique()
                transaction_type = st.selectbox("search by", trx_tpe, 0)
            with col2:
                st.subheader("SELECT YEAR ")      
                unique_years = Aggre_transaction["Years"].unique()
                choice_year = st.selectbox("**Select the Year**", unique_years,0)

            with col3:
                st.subheader(" SELECT STATES ")
                menu_state = Aggre_transaction["States"].unique()
                choice_state = st.selectbox("States", menu_state, 0)

            if transaction_type:
                col1, col2, col3, = st.columns(3)
                with col1:
                    st.subheader(f'Table view of {transaction_type}')
                    df = type_(transaction_type)
                    df = format_df_tx_type(df)
                    st.write(df)

            if transaction_type and choice_year:
                with col2:
                    st.subheader(f' in {choice_year}')
                    df = type_year(choice_year, transaction_type)
                    df = format_df_tx_type(df)
                    st.write(df)
                    
            if transaction_type and choice_state and choice_year:
                with col3:
                    st.subheader(f' in {choice_state}')
                    df = type_state(choice_state, choice_year, transaction_type)
                    df = format_df_tx_type(df)
                    st.write(df)
                    
        else:
            col1, col2,col3 = st.columns(3)
            with col1:
                st.subheader(" SELECT TYPE OF TRANSACTION ")
                trx_tpe=Aggre_transaction["Transaction_type"].unique()
                transaction_type = st.selectbox("search by", trx_tpe, 0)

                if transaction_type:
                    df = type_(transaction_type)
                    fig = px.bar(df, x="States", y="Transaction_amount", title=f'Plotly view of {transaction_type}',color='Years')
                    st.plotly_chart(fig, theme=None, use_container_width=True)
            with col2:
                st.subheader(" SELECT YEAR ")
                unique_years = Aggre_transaction["Years"].unique()
                # Create radio buttons for year selection
                choice_year = st.selectbox("**Select the Year**", unique_years,0)

                if transaction_type and choice_year:
                    df = type_year(choice_year, transaction_type)
                    fig = px.bar(df, x="States", y="Transaction_amount",title=f"Plotly view of {transaction_type} in {choice_year}",color='Quarter')
                    st.plotly_chart(fig, theme=None, use_container_width=True)
            with col3:
                st.subheader(" SELECT STATE ")
                menu_state = Aggre_transaction["States"].unique()
                choice_state = st.selectbox("States", menu_state, 0)
                if transaction_type and choice_state and choice_year:
                    df = type_state(choice_state, choice_year, transaction_type)
                    fig = px.bar(df, x="Quarter", y="Transaction_amount",title=f" {transaction_type} in {choice_year} at {choice_state}",color="Quarter")
                    st.plotly_chart(fig, theme=None, use_container_width=True)

    
    if choice_topic == "District":
        select = st.selectbox('View', ['Tabular view', 'Plotly View'], 0)
        if select == 'Tabular view':

            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader(" SELECT STATE ")
                menu_state = Map_transaction["States"].unique()
                choice_state = st.selectbox("State", menu_state, 0)
            with col2:
                st.subheader(" SELECT YEAR ")
                unique_years = Map_transaction["Years"].unique()
                choice_year = st.selectbox("**Select the Year**", unique_years,0)
            with col3:
                st.subheader(" SELECT DISTRICT ")
                dist=df_map_transaction["Districts"].unique().tolist()
                dist.sort()
                district = st.selectbox("search by", dist)
            if choice_state:
                with col1:
                    st.subheader(f'{choice_state}')
                    df = district_choice_state(choice_state)
                    df = format_df_tx_type(df)
                    st.write(df)
                    
            if choice_year and choice_state:
                with col2:
                    st.subheader(f'in {choice_year} ')
                    df = dist_year_state(choice_year, choice_state)
                    df = format_df_tx_type(df)
                    st.write(df)
                  
            if district and choice_state and choice_year:
                with col3:
                    st.subheader(f'in {district} ')
                    df = district_year_state(district, choice_year, choice_state)
                    df = format_df_tx_type(df)
                    st.write(df)
                    
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader(" SELECT STATE ")
                menu_state = Map_transaction["States"].unique()
                choice_state = st.selectbox("State", menu_state, 0)
                if choice_state:
                    df=district_choice_state(choice_state)
                    fig = px.bar(df, x="Districts", y="Transaction_amount", title=f'Transaction in {choice_state}',color='Years')
                    st.plotly_chart(fig, theme=None, use_container_width=True)

            with col2:
                st.subheader(" SELECT YEAR ") 
                unique_years = Map_transaction["Years"].unique()
                choice_year = st.selectbox("**Select the Year**", unique_years,0)
                df=dist_year_state(choice_year, choice_state)
                fig = px.bar(df, x="Districts", y="Transaction_amount", title=f'Transaction in  {choice_state} in {choice_year}',color='Quarter')
                st.plotly_chart(fig, theme=None, use_container_width=True)
            with col3:
                st.subheader(" SELECT DISTRICT ")
                dist=Map_transaction["Districts"].unique().tolist()
                dist.sort()
                district = st.selectbox("search by",dist )
                df=district_year_state(district, choice_year, choice_state)
                fig = px.bar(df, x="Quarter", y="Transaction_amount",title=f"Transaction {district} in {choice_year} at {choice_state}",color='Quarter')
                st.plotly_chart(fig, theme=None, use_container_width=True)
    
    
    if choice_topic == "Brand":
        select = st.selectbox('View', ['Tabular view', 'Plotly View'], 0)
        if select == 'Tabular view':
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader(" SELECT BRAND ")
                mobiles = Aggre_user["Brands"].unique()
                brand_type = st.selectbox("search by", mobiles, 0)
            with col2:
                st.subheader(" SELECT YEAR")
                br_yr = Aggre_user ["Years"].unique()
                choice_year = st.selectbox("Year", br_yr , 0)
            with col3:
                st.subheader(" SELECT STATE ")
                br_st=Aggre_user["States"].unique()
                choice_state = st.selectbox("State", br_st, 0)

            if brand_type:
                col1, col2, col3, = st.columns(3)
                with col1:
                    st.subheader(f'{brand_type}')
                    br=brand_(brand_type)
                    df = format_brand(br)
                    st.write(df)
                    
            if brand_type and choice_year:
                with col2:
                    st.subheader(f' in {choice_year}')
                    br1_yr=brand_year(brand_type, choice_year)
                    df = format_brand(br1_yr)
                    st.write(df)
                    
            if brand_type and choice_state and choice_year:
                with col3:
                    st.subheader(f' in {choice_state}')
                    df = brand_state(choice_state, brand_type, choice_year)
                    df = format_brand(df)
                    st.write(df)
                   
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader(" SELECT BRAND ")
                mobiles = Aggre_user["Brands"].unique()
                brand_type = st.selectbox("search by", mobiles, 0)
                if brand_type:
                    df=brand_(brand_type)
                    fig = px.bar(df, x="States", y="Transaction_count",title=f" {brand_type} Users ",color='Years')
                    st.plotly_chart(fig, theme=None, use_container_width=True)

            with col2:
                st.subheader(" SELECT YEAR")
                br_yr = Aggre_user ["Years"].unique()
                choice_year = st.selectbox("Year", br_yr , 0)
                if brand_type and choice_year:
                    df=brand_year(brand_type, choice_year)
                    fig = px.bar(df, x="States", y="Transaction_count",title=f"{brand_type} Users in {choice_year}",color='Quarter')
                    st.plotly_chart(fig, theme=None, use_container_width=True)
            with col3:
                st.subheader(" SELECT STATE ")
                br_st=Aggre_user["States"].unique()
                choice_state = st.selectbox("State", br_st, 0)
                if brand_type and choice_state and choice_year:
                    df=brand_state(choice_state, brand_type, choice_year)
                    fig = px.bar(df, x="Quarter", y="Transaction_count",title=f"{brand_type} Users in {choice_year} at {choice_state}",color='Quarter')
                    st.plotly_chart(fig, theme=None, use_container_width=True)

    if choice_topic == "Top-Transactions":
        select = st.selectbox('View', ['Tabular view', 'Plotly View'], 0)
        if select == 'Tabular view':
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader(" SELECT STATE ")
                menu_state = Top_transaction["States"].unique()
                choice_state = st.selectbox("State", menu_state, 0)
            with col2:
                st.subheader(" SELECT  YEAR ")
                tr_Year= Top_transaction["Years"].unique()
                choice_year = st.selectbox("Year", tr_Year , 0)
            with col3:
                st.subheader(" SELECT Quarter ")
                menu_quater = Top_transaction["Quarter"].unique()
                choice_quater = st.selectbox("Quater", menu_quater, 0)

            if choice_state:
                with col1:
                    st.subheader(f'{choice_state}')
                    df = transaction_state(choice_state)
                    df = format_df_top_tx(df)
                    st.write(df)
                    
            if choice_state and choice_year:
                with col2:
                    st.subheader(f'{choice_year}')
                    df = transaction_year(choice_state, choice_year)
                    df = format_df_top_tx(df)
                    st.write(df)
                    
            if choice_state and choice_quater:
                with col3:
                    st.subheader(f'{choice_quater}')
                    df = transaction_quarter(choice_state, choice_year, choice_quater)
                    df = format_df_top_tx(df)
                    st.write(df)
                    
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader(" SELECT STATE ")
                menu_state = Top_transaction["States"].unique()
                choice_state = st.selectbox("State", menu_state, 0)
                if choice_state:
                    df=transaction_state(choice_state)
                    fig = px.bar(df, x="Years", y="Transaction_count",title=f"Transactions in {choice_state}", color='Quarter')
                    st.plotly_chart(fig, theme=None, use_container_width=True)

            with col2:
                st.subheader(" SELECT  YEAR ")
                tr_Year= Top_transaction["Years"].unique()
                choice_year = st.selectbox("Year", tr_Year , 0)
                if choice_state and choice_year:
                    df=transaction_year(choice_state, choice_year)
                    fig = px.bar(df, x="Years", y="Transaction_count",title=f"Transactions{choice_year} at {choice_state}", color='Quarter')
                    st.plotly_chart(fig, theme=None, use_container_width=True)

            with col3:
                st.subheader(" SELECT Quarter ")
                menu_quater = Top_transaction["Quarter"].unique()
                choice_quater = st.selectbox("Quater", menu_quater, 0)
                if choice_state and choice_quater:
                    df=transaction_quarter(choice_state, choice_year, choice_quater)
                    fig = px.bar(df, x="Quarter", y="Transaction_count",title=f"Transactions in {choice_year} at {choice_state} in Quarter {choice_quater}", color='Quarter')
                    st.plotly_chart(fig, theme=None, use_container_width=True)

    if choice_topic == "Registered-users":
        select = st.selectbox('View', ['Tabular view', 'Plotly View'], 0)
        if select == 'Tabular view':
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader(" SELECT STATE ")
                menu_state = Map_user["States"].unique()
                choice_state = st.selectbox("State", menu_state, 0)
            with col2:
                st.subheader(" SELECT YEAR ")
                ru_years=Map_user["Years"].unique()
                choice_year = st.selectbox("Year", ru_years , 0)
    
            with col3:
                st.subheader(" SELECT DISTRICT ")
                dist=Map_user["Districts"].unique().tolist()
                dist.sort()
                district = st.selectbox("search by",dist )

            if choice_state:
                with col1:
                    st.subheader(f'{choice_state}')
                    df = registered_user_state(choice_state)
                    df = reg_users(df)
                    st.write(df)
                    
            if choice_state and choice_year:
                with col2:
                    st.subheader(f'{choice_year}')
                    df = registered_user_year(choice_state, choice_year)
                    df = reg_users(df)
                    st.write(df)
                   

            if choice_state and choice_year and district:
                with col3:
                    st.subheader(f'{district}')
                    df = registered_user_district(choice_state, choice_year, district)
                    df = reg_users(df)
                    st.write(df)
                    
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader(" SELECT STATE ")
                menu_state = Map_user["States"].unique()
                choice_state = st.selectbox("State", menu_state, 0)
                if choice_state:
                    df=registered_user_state(choice_state)
                    fig = px.bar(df, x="Districts", y="RegisteredUser",title=f"Registered users at {choice_state} ",color='Years')
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, theme=None, use_container_width=True)
            with col2:
                st.subheader(" SELECT YEAR ")
                ru_years=Map_user["Years"].unique()
                choice_year = st.selectbox("Year", ru_years , 0)
                if choice_state and choice_year:
                    df=registered_user_year(choice_state, choice_year)
                    fig = px.bar(df, x="Districts", y="RegisteredUser",title=f"Registered users in {choice_state} in {choice_year}",color='Quarter')
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, theme=None, use_container_width=True)
            with col3:
                st.subheader("SELECT DISTRICT ")
                dist=Map_user["Districts"].unique().tolist()
                dist.sort()
                district = st.selectbox("search by",dist)
                if choice_state and choice_year and district:
                    df=registered_user_district(choice_state, choice_year, district)
                    fig = px.bar(df, x="Quarter", y="RegisteredUser",title=f"Registered users at {choice_state} in {choice_year} in {district}",color='Quarter')
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, theme=None, use_container_width=True)


def menu_Basic_insights():
    st.title("BASIC INSIGHTS")
    #st.write("----")
    st.subheader("Let's know some basic insights about the data")


        
    def ques1():
        brand= Aggre_user[["Brands","Transaction_count"]]
        brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
        brand2= pd.DataFrame(brand1).reset_index()

        fig_brands= px.pie(brand2, values= "Transaction_count", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                        title= "Top Mobile Brands of Transaction_count")
        return st.plotly_chart(fig_brands)

    def ques2():
        lt= Aggre_transaction[["States", "Transaction_amount"]]
        lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
        lt2= pd.DataFrame(lt1).reset_index().head(10)

        fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                        color_discrete_sequence= px.colors.sequential.Oranges_r)
        return st.plotly_chart(fig_lts)

    def ques3():
        htd= Map_transaction[["Districts", "Transaction_amount"]]
        htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
        htd2= pd.DataFrame(htd1).head(10).reset_index()

        fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Emrld_r)
        return st.plotly_chart(fig_htd)

    def ques4():
        htd= Map_transaction[["Districts", "Transaction_amount"]]
        htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
        htd2= pd.DataFrame(htd1).head(10).reset_index()

        fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Greens_r)
        return st.plotly_chart(fig_htd)


    def ques5():
        sa= Map_user[["States", "AppOpens"]]
        sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
        sa2= pd.DataFrame(sa1).reset_index().head(10)

        fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="Top 10 States With AppOpens",
                    color_discrete_sequence= px.colors.sequential.deep_r)
        return st.plotly_chart(fig_sa)

    def ques6():
        sa= Map_user[["States", "AppOpens"]]
        sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
        sa2= pd.DataFrame(sa1).reset_index().head(10)

        fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="lowest 10 States With AppOpens",
                    color_discrete_sequence= px.colors.sequential.dense_r)
        return st.plotly_chart(fig_sa)

    def ques7():
        stc= Aggre_transaction[["States", "Transaction_count"]]
        stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
        stc2= pd.DataFrame(stc1).reset_index()

        fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                        color_discrete_sequence= px.colors.sequential.Jet_r)
        return st.plotly_chart(fig_stc)

    def ques8():
        stc= Aggre_transaction[["States", "Transaction_count"]]
        stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
        stc2= pd.DataFrame(stc1).reset_index()

        fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                        color_discrete_sequence= px.colors.sequential.Magenta_r)
        return st.plotly_chart(fig_stc)

    def ques9():
        ht= Aggre_transaction[["States", "Transaction_amount"]]
        ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
        ht2= pd.DataFrame(ht1).reset_index().head(10)

        fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                        color_discrete_sequence= px.colors.sequential.Oranges_r)
        return st.plotly_chart(fig_lts)

    def ques10():
        dt= Map_transaction[["Districts", "Transaction_amount"]]
        dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
        dt2= pd.DataFrame(dt1).reset_index().head(50)

        fig_dt= px.bar(dt2, x= "Districts", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence= px.colors.sequential.Mint_r)
        return st.plotly_chart(fig_dt)
    
    def ques11():
        States_in= Aggre_insurance[["States","Years","Insurance_count"]]
        df_States_in=States_in.groupby("States")["Insurance_count"].sum()
        df_States_in=pd.DataFrame(df_States_in).reset_index()
        #df_States_in.columns=['States','Insurance_count']

        fig_ststes_in= px.bar(df_States_in, y= "Insurance_count", x= "States", color_discrete_sequence=px.colors.sequential.Tealgrn ,
                    title= "States And Its Insurance Count")
        return st.plotly_chart(fig_ststes_in)
        

    def ques12():
        States_in= Aggre_insurance[["States","Insurance_amount"]]
        df_States_in=States_in.groupby("States")["Insurance_amount"].sum()
        df_States_in=pd.DataFrame(df_States_in).reset_index()
        #df_States_in.columns=['States','Insurance_amount']

        fig_ststes_in= px.bar(df_States_in, y= "Insurance_amount", x= "States", color_discrete_sequence=px.colors.sequential.Tealgrn ,
                    title= "States And Its Insurance Count")
        return st.plotly_chart(fig_ststes_in)






    ques= st.selectbox("**Select the Question**",('States With Lowest Trasaction Amount',
                                                'Districts With Highest Transaction Amount',
                                                'Districts With Lowest Transaction Amount',
                                                'Top 10 States With AppOpens',
                                                'Least 10 States With AppOpens',
                                                'States With Lowest Trasaction Count',
                                                'States With Highest Trasaction Count',
                                                'States With Highest Trasaction Amount',
                                                'Top 50 Districts With Lowest Transaction Amount',
                                                'Top Brands Of Mobiles Used',
                                                'States And Its Insurance Amount',
                                                'States And Its Insurance Count'))
    
    if ques=="Top Brands Of Mobiles Used":
        ques1()

    elif ques=="States With Lowest Trasaction Amount":
        ques2()

    elif ques=="Districts With Highest Transaction Amount":
        ques3()

    elif ques=="Districts With Lowest Transaction Amount":
        ques4()

    elif ques=="Top 10 States With AppOpens":
        ques5()

    elif ques=="Least 10 States With AppOpens":
        ques6()

    elif ques=="States With Lowest Trasaction Count":
        ques7()

    elif ques=="States With Highest Trasaction Count":
        ques8()

    elif ques=="States With Highest Trasaction Amount":
        ques9()

    elif ques=="Top 50 Districts With Lowest Transaction Amount":
        ques10()

    elif ques=="States And Its Insurance Count":
        ques11()

    elif ques=="States And Its Insurance Amount":
        ques12()

    






def menu_select(SELECT):
    if SELECT == "Home":
        menu_Home()
    elif SELECT=="Data Exploration":
        menu_Data_Exploration()
    elif SELECT == "Search":
        menu_Search()
    elif SELECT == "Basic insights":
        menu_Basic_insights()



#
def streamlit_app():
    st.set_page_config(page_title='PhonePe Pulse',page_icon=phn,layout='wide')
    st.title(':violet[ PhonePe Pulse Data Visualization ]')


    SELECT = option_menu(
    menu_title=None,
    options=["Home","Data Exploration","Search", "Basic insights"],
    icons=["house","bar-chart", "search",  "toggles"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "white", "size": "cover"},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", 
                    "--hover-color": "#6F36AD", "color": "#6F36AD","font-weight": "bold"},
        "nav-link-selected": {"background-color": "#6F36AD", "color": "white"}
    } 
    )
    menu_select(SELECT)


streamlit_app()