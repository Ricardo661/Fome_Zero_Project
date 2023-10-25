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

df2 =df1.copy()
df3 = df1.copy()
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

restaurants = st.sidebar.slider(
    'Escolha os Paises que Deseja visualizar as Informações', 1, 20, 10)


cuisines = st.sidebar.multiselect(
    "Escolha os Tipos de Culinária",
    df1.loc[:, "cuisines_number"].unique().tolist(),
    default=["Home-made", "BBQ", "Japanese", "Brazilian", "Arabian", "American","Italian"])



#filtro de paises
linhas_selecionadas = df1['country'].isin(countries)
df1 = df1.loc[linhas_selecionadas,:]


#filtro de culinaria
linhas_selecionadas = df1['cuisines_number'].isin(cuisines)
df1 = df1.loc[linhas_selecionadas,:]

#filtro de qtd
linhas_selecionadas = df1.head(restaurants)
df1 = linhas_selecionadas

#=========================================================
# Layout no Streamlit
#=========================================================
    
st.title('🍽️ Visão Tipos de Cusinhas')


with st.container():
    st.subheader('Melhores Restaurantes')
    col1,col2,col3,col4,col5 = st.columns(5)
    
    with col1:
        line = df2['cuisines_number']=='Brazilian'
        cols = ['country','city','restaurant_name','cuisines_number','average_cost_for_two','currency','aggregate_rating','restaurant_id']
        aux = df2.loc[line, cols].sort_values(['aggregate_rating','restaurant_id'], ascending = [False,True])
        aux['restaurant'] = aux['restaurant_name'] + ' - ' + aux['cuisines_number']
        aux['Cust'] = aux['average_cost_for_two'].map(str) + '(' + aux['currency'] + ')'
        aux['nota'] = aux['aggregate_rating'].map(str) + '/' + '5'
        aux1 = aux.reset_index()
        aux2 = aux1.iloc[0,9]
        aux3 = aux1.iloc[0,11]
        help_aux = f'País: {aux1.iloc[0,1]}\n\nCidade: {aux1.iloc[0,2]}\n\nMédia Prato para dois: {aux1.iloc[0,10]}' 
        col1.metric(aux2, aux3 , help= help_aux)

    with col2:
        line = df2['cuisines_number']=='Japanese'
        cols = ['country','city','restaurant_name','cuisines_number','average_cost_for_two','currency','aggregate_rating','restaurant_id']
        aux = df2.loc[:, cols].sort_values(['aggregate_rating','restaurant_id'], ascending = [False,True])
        aux['restaurant'] = aux['restaurant_name'] + ' - ' + aux['cuisines_number']
        aux['Cust'] = aux['average_cost_for_two'].map(str) + '(' + aux['currency'] + ')'
        aux['nota'] = aux['aggregate_rating'].map(str) + '/' + '5'
        aux1 = aux.reset_index()
        aux2 = aux1.iloc[0,9]
        aux3 = aux1.iloc[0,11]
        help_aux = f'País: {aux1.iloc[0,1]}\n\nCidade: {aux1.iloc[0,2]}\n\nMédia Prato para dois: {aux1.iloc[0,10]}' 
        col2.metric(aux2, aux3 , help= help_aux)    
    with col3:
        line = df2['cuisines_number']=='Arabian'
        cols = ['country','city','restaurant_name','cuisines_number','average_cost_for_two','currency','aggregate_rating','restaurant_id']
        aux = df2.loc[:, cols].sort_values(['aggregate_rating','restaurant_id'], ascending = [False,True])
        aux['restaurant'] = aux['restaurant_name'] + ' - ' + aux['cuisines_number']
        aux['Cust'] = aux['average_cost_for_two'].map(str) + '(' + aux['currency'] + ')'
        aux['nota'] = aux['aggregate_rating'].map(str) + '/' + '5'
        aux1 = aux.reset_index()
        aux2 = aux1.iloc[0,9]
        aux3 = aux1.iloc[0,11]
        help_aux = f'País: {aux1.iloc[0,1]}\n\nCidade: {aux1.iloc[0,2]}\n\nMédia Prato para dois: {aux1.iloc[0,10]}' 
        col3.metric(aux2, aux3 , help= help_aux)
    
    with col4:
        line = df2['cuisines_number']=='American'
        cols = ['country','city','restaurant_name','cuisines_number','average_cost_for_two','currency','aggregate_rating','restaurant_id']
        aux = df2.loc[:, cols].sort_values(['aggregate_rating','restaurant_id'], ascending = [False,True])
        aux['restaurant'] = aux['restaurant_name'] + ' - ' + aux['cuisines_number']
        aux['Cust'] = aux['average_cost_for_two'].map(str) + '(' + aux['currency'] + ')'
        aux['nota'] = aux['aggregate_rating'].map(str) + '/' + '5'
        aux1 = aux.reset_index()
        aux2 = aux1.iloc[0,9]
        aux3 = aux1.iloc[0,11]
        help_aux = f'País: {aux1.iloc[0,1]}\n\nCidade: {aux1.iloc[0,2]}\n\nMédia Prato para dois: {aux1.iloc[0,10]}' 
        col4.metric(aux2, aux3 , help= help_aux)
    
    with col5:
        line = df2['cuisines_number']=='Italian'
        cols = ['country','city','restaurant_name','cuisines_number','average_cost_for_two','currency','aggregate_rating','restaurant_id']
        aux = df2.loc[:, cols].sort_values(['aggregate_rating','restaurant_id'], ascending = [False,True])
        aux['restaurant'] = aux['restaurant_name'] + ' - ' + aux['cuisines_number']
        aux['Cust'] = aux['average_cost_for_two'].map(str) + '(' + aux['currency'] + ')'
        aux['nota'] = aux['aggregate_rating'].map(str) + '/' + '5'
        aux1 = aux.reset_index()
        aux2 = aux1.iloc[0,9]
        aux3 = aux1.iloc[0,11]
        help_aux = f'País: {aux1.iloc[0,1]}\n\nCidade: {aux1.iloc[4,2]}\n\nMédia Prato para dois: {aux1.iloc[0,10]}' 
        col5.metric(aux2, aux3 , help= help_aux)

with st.container():
    st.header (f'Top {restaurants} Restaurantes')
    cols = ['restaurant_id', 'restaurant_name', 'country', 'city', 'cuisines_number','average_cost_for_two','aggregate_rating','votes']

    aux = df1.loc[:, cols].sort_values(['aggregate_rating','restaurant_id'], ascending=[False, True]).reset_index()
    st.dataframe(aux, hide_index = False,column_config={'restaurant_id' : st.column_config.NumberColumn('ID RESTAURANTE', format="%d"),
                                                        'restaurant_name':'RESTAURANTE',
                                                        'country':'PAÍS',
                                                        'city':'CIDADE',
                                                        'cuisines_number':'TIPO DE CULINÁRIA',
                                                        'average_cost_for_two':st.column_config.NumberColumn('VALOR MÉDIO PARA DUAS PESSOAS', format="%d"),
                                                        'aggregate_rating':'NOTA MÉDIA',
                                                        'votes':st.column_config.NumberColumn('QTD DE AVALIÇÕES FEITAS', format="%d")},
                 column_order=('restaurant_id','restaurant_name','country','city','cuisines_number','average_cost_for_two','aggregate_rating','votes'))
    
with st.container():
    col1,col2 = st.columns(2)
    with col1:
        lines = df3["country"].isin(countries)
        cols =['aggregate_rating','cuisines_number']
        aux = round((df3.loc[lines,cols].groupby(['cuisines_number'])
               .mean()
               .sort_values(['aggregate_rating'],ascending=False)
               .reset_index().head(restaurants)),2)

        fig= (px.bar(aux, x = 'cuisines_number', 
                    y = 'aggregate_rating',
                    text='aggregate_rating',
                    title=(f'Top {restaurants} Melhores Restaurantes'),
                    labels={'aggregate_rating':'MÉDIA DE AVALIAÇÃO MÉDIA','cuisines_number':'TIPO DE CULINÁRIA'},
                    color_discrete_sequence=px.colors.qualitative.Light24,
                    color = 'cuisines_number'))
        st.plotly_chart(fig, use_container_width = True)
    
    with col2:
        lines = df3["country"].isin(countries)
        cols =['aggregate_rating','cuisines_number']
        aux = round((df3.loc[lines,cols].groupby(['cuisines_number'])
               .mean()
               .sort_values(['aggregate_rating'],ascending=True)
              .reset_index().head(restaurants)),2)

        fig= (px.bar(aux, x = 'cuisines_number', 
                    y = 'aggregate_rating',
                    text='aggregate_rating',
                    title=(f'Top {restaurants} Piores Restaurantes'),
                    labels={'aggregate_rating':'MÉDIA DE AVALIAÇÃO MÉDIA','cuisines_number':'TIPO DE CULINÁRIA'},
                    color_discrete_sequence=px.colors.qualitative.Light24,
                    color = 'cuisines_number'))
        st.plotly_chart(fig, use_container_width = True)                
