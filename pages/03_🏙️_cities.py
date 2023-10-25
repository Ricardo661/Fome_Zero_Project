# Importando as Bibliotecas
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from streamlit_folium import folium_static
from PIL import Image

#importando o arquivo para o computador
df = pd.read_csv('dataset/zomato.csv')
#criando copia do dataframe
df1 = df.copy()

# Limpeza dos dados

# Renomeando o nome das colunas
df1.columns = [
    "restaurant_id",
    "restaurant_name",
    "country",
    "city",
    "address",
    "locality",
    "locality_verbose",
    "longitude",
    "latitude",
    "cuisines",
    "average_cost_for_two",
    "currency",
    "has_table_booking",
    "has_online_delivery",
    "is_delivering_now",
    "switch_to_order_menu",
    "price_range",
    "aggregate_rating",
    "rating_color",
    "rating_text",
    "votes"
    ]

# Removendo as linhas vazias do data frame
df1 = df1.dropna(axis = 0)

# Remover as linhas duplicadas do dataframe
df1 = df1.drop_duplicates()

# Remover a colunas sem variação de valor do data frame
df1 = df1.drop('switch_to_order_menu', axis = 1)

# ALteração das colunas

COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}

# Nome dos codigos

COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}

# Nomeando as faixas de preço

def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

def country_name(country):
    return COUNTRIES[country]

def color_name(rating_color):
    return COLORS[rating_color]

# Função para colocar o nome dos Paises
df1["country"] = df1.loc[:, "country"].apply(lambda x: country_name(x))

# Função para colocar o nome das Cores
df1["color_name"] = df1.loc[:, "rating_color"].apply(lambda x: color_name(x))

# Função para colocar o nome das faixas de cores
df1["price_type"] = df1.loc[:, "price_range"].apply(lambda x: create_price_tye(x))

# Função para Colocar todos os tipos de cosinhas como número 1
df1["cuisines_number"] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])


#=========================================================
# Barra página
#=========================================================

st.set_page_config(
    layout="wide")

#=========================================================
# Barra Lateral
#=========================================================
st.sidebar.markdown("""---""")
st.sidebar.markdown('## Filtros')

countries = st.sidebar.multiselect(
    "Escolha os Paises que Deseja visualizar os Restaurantes",
    df1.loc[:, "country"].unique().tolist(),
    default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"])


cities = st.sidebar.multiselect(
    "Escolha as Cidades que Deseja visualizar os Restaurantes",
    df1.loc[:, "city"].unique().tolist(),
    default= df1.loc[:, "city"].unique().tolist() )

#filtro de paises
linhas_selecionadas = df1['country'].isin(countries)
df1 = df1.loc[linhas_selecionadas,:]

#filtro de cidades
linhas_selecionadas = df1['city'].isin(cities)
df1 = df1.loc[linhas_selecionadas,:]

#=========================================================
# Layout no Streamlit
#=========================================================
    
st.title('🏙️ Visão Cidades')

with st.container():
    aux = df1.loc[:, ['city','restaurant_id']].groupby(['city']).nunique().sort_values(by='restaurant_id', ascending=False).reset_index()
    fig= (px.bar(aux, x = 'city',
                 y = 'restaurant_id',
                 text='restaurant_id',
                 title=('Quantidade de restaurantes registradas por cidade'),
                 labels={'restaurant_id':'QTD RESTAURANTES','city':'CIDADES'},
                 color_discrete_sequence=px.colors.qualitative.Light24,
                 color = 'city'))
    st.plotly_chart(fig, use_container_width = True)
    
with st.container():
    col1,col2 = st.columns(2)
    
    with col1:
        aux = (df1.loc[df1['aggregate_rating']>4,['city','restaurant_id']]
            .groupby(['city'])
            .nunique()
            .sort_values(by='restaurant_id', ascending=False).reset_index())
        fig = (px.bar(aux, x = 'city',
                      y = 'restaurant_id', 
                      text = 'restaurant_id',
                      title= ('Cidades com Restaurantes com nota média acima de 4'),
                      labels={'restaurant_id':'QTD RESTAURANTES','city':'CIDADES'},
                      color_discrete_sequence=px.colors.qualitative.Light24,
                      color = 'city'))
        st.plotly_chart(fig, use_container_width = True)
        
    with col2:
        aux = (df1.loc[df1['aggregate_rating']<2.5,['city','restaurant_id']]
               .groupby(['city'])
               .nunique()
               .sort_values(by='restaurant_id', ascending=False)
               .reset_index())
        fig = (px.bar(aux, x = 'city',
                      y = 'restaurant_id', 
                      text = 'restaurant_id',
                      title= ('Cidades com Restaurantes com nota média abaixo de 2,5'),
                      labels={'restaurant_id':'QTD RESTAURANTES','city':'CIDADES'},
                      color_discrete_sequence=px.colors.qualitative.Light24,
                      color = 'city'))
        st.plotly_chart(fig, use_container_width = True)
        
with st.container():
    aux = (df1.loc[:, ['city','cuisines_number']]
           .groupby(['city'])
           .nunique()
           .sort_values(by='cuisines_number', ascending=False)
           .reset_index())
    fig = (px.bar(aux, x = 'city',
                      y = 'cuisines_number', 
                      text = 'cuisines_number',
                      title= ('Cidades com Restaurantes com nota média abaixo de 2,5'),
                      labels={'cuisines_number':'QTD DE TIPO CULINÁRIOS ÚNICOS','city':'CIDADES'},
                      color_discrete_sequence=px.colors.qualitative.Light24,
                      color = 'city'))
    st.plotly_chart(fig, use_container_width = True)
        
