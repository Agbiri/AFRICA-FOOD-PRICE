import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt


@st.cache_data
def load_data():
    df= pd.read_csv('africa_food_prices.csv', low_memory=False)
    df.drop("mp_commoditysource",  axis = 1, inplace = True) # mp_commoditysource was remove because it is an empty column
    df.drop("Unnamed: 0", axis = 1, inplace = True)# removed the Unnamed: 0 column because it is not needed
    df.drop('currency_id', axis = 1, inplace= True)# removed currency id because it contains only zero
    df.loc[df['market']=='Ghat', 'state']=df.loc[df['market']=='Ghat', 'state'].fillna(value='Ghat')#working on NAN values
    df.loc[df['market']=='National Average', 'state']=df.loc[df['market']=='National Average', 'state'].fillna(value='National')
    df.loc[df['market']=='Nalut', 'state']=df.loc[df['market']=='Nalut', 'state'].fillna(value='Nalut') 
    df.loc[df['market']=='Azzintan', 'state']=df.loc[df['market']=='Azzintan', 'state'].fillna(value='Azzintan') 
    df.loc[df['market']=='AlMarj', 'state']=df.loc[df['market']=='AlMarj', 'state'].fillna(value='AlMarj') 
    df.loc[df['market']=='Ghat', 'state']=df.loc[df['market']=='Ghat', 'state'].fillna(value='Ghat')  
    df.loc[df['country']=='Mozambique', 'state']=df.loc[df['country']=='Mozambique', 'state'].fillna(value='Maputo') 
    df.loc[df['country']=='Libya', 'state']=df.loc[df['country']=='Libya', 'state'].fillna(value='Tripoli')
    df.loc[df['country']=='South Sudan', 'state']=df.loc[df['country']=='South Sudan', 'state'].fillna(value='Juba')
    df.loc[df['country']=='Chad', 'state']=df.loc[df['country']=='Chad','state'].fillna(value='N\'Djamena')
    df.loc[df['country']=='Swaziland','state']=df.loc[df['country']=='Swaziland'].fillna(value='Mbabane')
    df['country_id'] = df['country_id'].astype(int) #changed datatype from flaat to int
    df.rename(columns={'pt_id':'market type id', 'um_unit_id':'measurement id'}, inplace=True)#renamed colum
                    
    return df
    return df.set_index("year")
        
                    
st.title('AFRICA FOOD PRICES')

try:
    df=load_data()
    countries=df.country.unique()
    countries_selected= st.multiselect(
        "Choose countries", countries, [countries[0],countries[1]]
    )
    countries_selected= df[df['country'].isin(countries_selected)]
    st.write(countries_selected.head())
 
        
    #chart
    
    #Q1 what are the overall trends in Afriac food price over the period
    
    st.write("""### AFRICA FOOD PRICE TRENDS OVER TIME""")
    fig, ax= plt.subplots(figsize=(10,6))
    plt.plot(df['year'], df['price'], marker='o', linestyle='-', color='b')
    plt.xlabel('year')
    plt.ylabel('price')
    plt.grid(True)
    st.pyplot(fig)
    
   #Q2- Are there any noticeable seasonal patterns in the price fluctuations of specific produce
    
    st.write("""### Seasonal Pattern in the Price Fluctuations of a Specific Produce""")
    produce=df['produce'].value_counts()
    x=list(dict(produce).keys())[:10]
    y=list(dict(produce).values())[:10]
    fig2,ax=plt.subplots (figsize=(7,7))
    ax.bar(x, y)
    plt.xticks(rotation='vertical')
    ax.set_label("commoodity")
    ax.set_label("price")
    st.pyplot(fig2)
            
        
     #Q3 How does food  price vary with produce
    
    st.write("""### Top 10 Average Prices of Different Products""")
    avg_prices = df.groupby('produce')['price'].mean().reset_index()
    avg_prices = avg_prices.sort_values(by='price', ascending=False)
    top_10_products = avg_prices.head(10)
    fig3,ax=plt.subplots(figsize=(10, 6))
    plt.plot(top_10_products['produce'], top_10_products['price'], marker='o', linestyle='-', color='b')
    plt.xlabel('Product')
    plt.ylabel('Average Price')
    plt.xticks(rotation=45)
    st.pyplot(fig3)
    
    
    #Q4 which market type recorded more sale
    
    st.write("""### Percentage purchases per market""")
    fig4, ax1=plt.subplots()
    pie_data=df['market_type'].value_counts()
    ax1.pie(pie_data, labels=pie_data.index, autopct='%1.2f%%', explode=[0,0,1])
    st.pyplot(fig4)
    
    #Q5  are there certain locality that consistently experienxe higher food price inflation than others
    
    st.write("""### Top 10 Countries: Mean Price of Products per Country""")
    cunty_prc_yr = df[['country','year','price']]
    first_year_per_country = cunty_prc_yr.groupby('country')['year'].min()
    selected_years = cunty_prc_yr.set_index('country')['year'].to_dict()
    selected_rows = cunty_prc_yr[cunty_prc_yr.apply(lambda row: row['year'] == selected_years.get(row['country']), axis=1)]
    top_10_countries = selected_rows.groupby('country')['price'].mean().nlargest(10)
    mean_price_line_graph = cunty_prc_yr.groupby('country')['price'].mean()
    mean_price_line_graph_top_10 = mean_price_line_graph.loc[top_10_countries.index]
    fig5, ax =plt.subplots()
    plt.plot(mean_price_line_graph_top_10.index, mean_price_line_graph_top_10.values, label='Mean Price (1990-2021)', marker='o')
    plt.bar(top_10_countries.index, top_10_countries.values, label='Mean Price (First Trading Year)', alpha=0.5)
    plt.xlabel('Country')
    plt.ylabel('Mean Price')
    plt.xticks(rotation='vertical')
    plt.legend()
    st.pyplot(fig5)
except ValueError as e:
        st.error("""
                Error:
            """ % e.reason)