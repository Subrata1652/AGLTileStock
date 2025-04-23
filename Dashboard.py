import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')
st.set_page_config(page_title="AGL Stock Report",page_icon=":bar_chart",layout="wide")
st.title(" :bar_chart: AGL Dealer Stock")
st.markdown('<style>div.block-container{padding-top:3rem;}</style>',unsafe_allow_html=True)
fl=st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
df=pd.DataFrame()
col1,col2 = st.columns(2)
st.sidebar.header("CHOOSE YOUR FILTER:")
if fl is not None:
      if fl.name.endswith('csv'): 
            df=pd.read_csv(fl.name,encoding="ISO-8859-1") 
            st.write(df)             
      elif fl.name.endswith('xlsx'):
            df=pd.read_excel(fl,sheet_name='Sheet1',index_col=None,usecols=['Customer State Code','Customer Name','Size','Description','Posting Date','Quantity','Net Sales'],engine='openpyxl')
            #df=pd.read_excel("sales_reg.xlsx",sheet_name='Sheet1',index_col=None,usecols=['Customer State Code','Customer Name','Size','Description','Posting Date','Quantity','Net Sales'],engine='openpyxl')
            df["Posting Date"]=pd.to_datetime(df["Posting Date"])   
            with col1:
                  date1=pd.to_datetime(st.date_input("Start Date",pd.to_datetime(df["Posting Date"]).min()))
            with col2:
                  date2=pd.to_datetime(st.date_input("End Date",pd.to_datetime(df["Posting Date"]).max())) 
            df=df[(df["Posting Date"] >= date1) & (df["Posting Date"] <= date2)].copy()   
            cst=st.sidebar.multiselect("Pick State:",df['Customer State Code'].unique())
            if not cst:
                  df2=df.copy()
            else:
                  df2=df[df['Customer State Code'].isin(cst)]
            dnm =st.sidebar.multiselect("Pick Dealer:",df2['Customer Name'].unique())
            if not dnm:
                  df3=df2.copy()
            else:
                  df3=df2[df2['Customer Name'].isin(dnm)]
            sz=st.sidebar.multiselect("pick Size",df3['Size'].unique())
            if not sz:
                  df4=df3.copy()
            else:
                  df4=df3[df3['Size'].isin(sz)]
            des=st.sidebar.multiselect("Pick Item Name",df4['Description'].unique())
            if not des:
                  df5=df4.copy()
            else:
                  df5=df4[df4['Description'].isin(des)]

            if not cst and not dnm and not sz and not des:
                  filtered_df=df
            elif cst and dnm and sz and des:
                  filtered_df=df5[df5['Customer State Code'].isin(cst) & df5['Customer Name'].isin(dnm) & df5['Size'].isin(sz) & df5['Description'].isin(des)] 
            elif cst and dnm and sz:
                  filtered_df=df4[df4['Customer State Code'].isin(cst) & df4['Customer Name'].isin(dnm) & df4['Size'].isin(sz)] 
            elif cst and dnm and des:
                  filtered_df=df5[df5['Customer State Code'].isin(cst) & df5['Customer Name'].isin(dnm) & df5['Size'].isin(sz)] 
            elif cst and sz and des:
                  filtered_df=df5[df5['Customer State Code'].isin(cst) & df5['Size'].isin(sz) & df5['Description'].isin(des)]  
            elif dnm and sz and des:
                  filtered_df=df5[df5['Customer Name'].isin(dnm) & df5['Size'].isin(sz) & df5['Description'].isin(des)]  
            elif cst and dnm:
                  filtered_df=df3[df3['Customer Name'].isin(dnm) & df3['Customer State Code'].isin(cst)]  
            elif cst and sz:
                  filtered_df=df4[df4['Customer State Code'].isin(cst) & df4['Size'].isin(sz)]  
            elif cst and des:
                  filtered_df=df5[df5['Customer State Code'].isin(cst) & df5['Description'].isin(des)] 
            elif dnm and sz:
                  filtered_df=df3[df3['Customer Name'].isin(dnm) & df3['Size'].isin(sz)] 
            elif dnm and des:
                  filtered_df=df5[df5['Customer Name'].isin(dnm) & df5['Description'].isin(des)] 
            elif sz and des:
                  filtered_df=df5[df5['Size'].isin(sz) & df5['Description'].isin(des)] 
            elif not dnm and not sz and not des:
                  filtered_df=df2
            elif not cst and not sz and not des:
                  filtered_df=df3
            elif not cst and not dnm and not des:
                  filtered_df=df4
            elif not cst and not dnm and not sz:
                  filtered_df=df5
            with col1:
                  #if not sz and not des:
                        if not dnm:
                              bar_data=pd.pivot_table(filtered_df,values='Net Sales',index=[filtered_df['Posting Date'].dt.month_name()],columns=['Customer State Code'],aggfunc="sum",sort=False)
                              st.subheader("State Wise Sales")
                              st.write(bar_data)
                              fig=px.bar(bar_data,x=bar_data.index, y=bar_data.columns, barmode='group')
                              st.plotly_chart(fig,use_container_width=True, height=300)  
                        elif  dnm:
                              bar_data=pd.pivot_table(filtered_df,values='Net Sales',index=[filtered_df['Posting Date'].dt.month_name()],columns=['Customer Name'],aggfunc="sum",sort=False)
                              st.subheader("Dealer Wise Sales")
                              st.write(bar_data)
                              fig=px.bar(bar_data,x=bar_data.index, y=bar_data.columns, barmode='group')
                              st.plotly_chart(fig,use_container_width=True, height=300)   
            with col2:
                  #if sz and not des:
                        bar_data=pd.pivot_table(filtered_df,values='Quantity',index=[filtered_df['Posting Date'].dt.month_name()],columns=['Size'],aggfunc="sum",sort=False)
                        st.subheader("Size Wise Sales")
                        st.write(bar_data)
                        fig=px.bar(bar_data,x=bar_data.index,y=bar_data.columns,barmode='group')
                        st.plotly_chart(fig,use_container_width=True, height=300) 
      else:       
            st.write("Sorry")

  