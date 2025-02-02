import streamlit as st 
import pandas as pd 
import preprocessor 

# load data
df=pd.read_csv("data.csv")
# load the fetch time function 
df=preprocessor.fetch_time_data(df)
st.title("Sales Analytics Dashboard")
st.sidebar.title("Filters")

selected_year=preprocessor.MultiSelectFilter('Select Year',df['Financial_Year'].unique())
selected_month=preprocessor.MultiSelectFilter("Select Month",df['Financial_Month'].unique())
selected_Retailer=preprocessor.MultiSelectFilter("select Retailer",df['Retailer'].unique())
selected_Company=preprocessor.MultiSelectFilter("Select Company",df['Company'].unique())

filtered_df=df[(df['Financial_Year']).isin(selected_year) & (df['Financial_Month'].isin(selected_month)) & (df['Retailer'].isin(selected_Retailer)) & (df['Company'].isin(selected_Company))]



#key performance indicators
# key Metrics 
st.title("Key Metrics (KPIs)")

col1,col2,col3,col4=st.columns(4)

with col1:
    # total profits
    total_sales=int(filtered_df['Amount'].sum())
    if total_sales>1000000:
        formatted_values=f"₹{total_sales/1000000:.2f}M"
    elif total_sales>1000:
        formatted_values=f"₹{total_sales/1000:.2f}K"
    else:
        formatted_values=f"₹{total_sales}"
    st.metric(label="Total Sales",value=formatted_values,delta="11.2 M")

# total margin 
with col2:
    total_margin=int(filtered_df['Margin'].sum())
    if total_margin>1000000:
        formatted_margin=f"₹{total_margin/1000000:.2f}M"
    elif total_margin>1000:
        formatted_margin=f"₹{total_margin/1000:.2f}K"
    else:
        formatted_margin=f"₹{total_margin}"
    st.metric(label="Total Margin",value=formatted_margin,delta="1.8K")
with col3:
    # total_tranasactions 
    st.metric(label="Total Tranasactions",value=len(filtered_df))
with col4:
    # margin percentage 
    st.metric(label="Margin Percentage",value=f"{df['Margin'].sum()/df['Amount'].sum()*100:.2f}%",delta="6.4%")
    
    
# Sales Analysis on Monthly basis 
st.title("Monthly Sales Analysis")
yearly=filtered_df[['Financial_Year','Amount','Financial_Month']].groupby(['Financial_Year','Financial_Month']).sum().reset_index().pivot(index='Financial_Month',
                                                                                                                                          columns='Financial_Year',values='Amount')
st.line_chart(data=yearly,x_label="Month",y_label="Amount")
st.balloons()


col5,col6 = st.columns(2)

with col5:
    st.write("Top Retailers by Revenue")
    retailers_count=preprocessor.top_revenue_retailers(filtered_df)
    retailers_count.set_index('percentage_revenue',inplace=True)
    st.bar_chart(retailers_count,x_label='percentage_revenue',y_label='retailers_count')
    
    
with col6:
    st.write("Top Company By Revenue")
    companies_count=preprocessor.top_revenue_company(filtered_df)
    companies_count.set_index('percentage_revenue',inplace=True)
    st.bar_chart(companies_count,x_label='percentage_revenue',y_label='companies_count')
   
    
