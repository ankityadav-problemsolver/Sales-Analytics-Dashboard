import pandas as pd
import streamlit as st 

# create fucntion to filter data 
def MultiSelectFilter(title,option_list):
    selected=st.sidebar.multiselect(title,option_list)
    select_all=st.sidebar.checkbox('Select All',value=True,key=title)
    if select_all:
        selected_options=option_list
    else:
        selected_options=selected 
    return selected_options

# fetch the date and time from the data 
def fetch_time_data(df):
    df['Date']=pd.to_datetime(df['Date'])
    df['Year']=df['Date'].dt.year
    df['Day']=df['Date'].dt.day
    df['Month']=df['Date'].dt.month
    
    month_dict={4:1, 5:2, 6:3,7:4, 8:5, 9:6, 10:7, 11:8, 12:9, 1:10, 2:11,3:12}
    df['Financial_Month']=df['Month'].map(month_dict)
    df['Financial_Year']= df.apply(lambda x: f"{x['Year']} - {x['Year']+1}" if x['Month'] >= 4 else f"{x['Year']-1} - {x['Year']}",axis=1)
    
    return df


# find the top retailers 
def top_revenue_retailers(df):
    Revenue=df.groupby('Retailer')['Amount'].sum().reset_index().sort_values(by='Amount',ascending=False)
    Total_Revenue=Revenue['Amount'].sum()
    percentages=[100,90,80,70,60,50,40,30,20,10]
    retailers_count=[]
    for i in percentages:
        target_revenue= Total_Revenue * i * 0.01
        loop=1
        while( loop <= len(Revenue) and Revenue.iloc[:loop,1].sum() <=target_revenue):
            loop +=1
        retailers_count.append(loop)
    
    retailers=pd.DataFrame({'percentage_revenue':percentages,'retailers_count':retailers_count})
    return retailers

# find the top companies
def top_revenue_company(df):
    Revenue=df.groupby('Company')['Amount'].sum().reset_index().sort_values(by='Amount',ascending=False)
    Total_Revenue=Revenue['Amount'].sum()
    percentages=[100,90,80,70,60,50,40,30,20,10]
    companies_count=[]
    for i in percentages:
        target_revenue= Total_Revenue * i * 0.01
        loop=1
        while( loop <= len(Revenue) and Revenue.iloc[:loop,1].sum() <=target_revenue):
            loop +=1
        companies_count.append(loop)
    
    companies=pd.DataFrame({'percentage_revenue':percentages,'retailers_count':companies_count})
    return companies
        
        