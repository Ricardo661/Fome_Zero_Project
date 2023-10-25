# Importando as Bibliotecas
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from streamlit_folium import folium_static
from PIL import Image
import folium
from folium.plugins import MarkerCluster
import locale


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

df2 = df1.copy()


st.set_page_config(
    page_title="Main Page",
    page_icon="📊",
    layout="wide"
)


#=========================================================
# Barra Lateral
#=========================================================

image= Image.open('logo.png')
#st.sidebar.image (image, width=160, use_column_width="auto")
col1, col2 = st.sidebar.columns([2, 5], gap="small")
col1.image(image, width=35, use_column_width="auto")
col2.markdown("# Fome Zero")


st.sidebar.markdown('## Filtros')

countries = st.sidebar.multiselect(
    "Escolha os Paises que Deseja visualizar os Restaurantes",
    df1.loc[:, "country"].unique().tolist(),
    default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"])


countries = df1['country'].isin(countries)
df1 = df1.loc[countries,:]

st.sidebar.markdown("""---""")
st.sidebar.markdown("### Base de Dados")

processed_data = pd.read_csv('dataset/zomato.csv')
st.sidebar.download_button(
        label="Download",
        data=processed_data.to_csv(index=False, sep=";"),
        file_name="data.csv",
        mime="text/csv",
    )

#=========================================================
# Funções
#=========================================================

st.title('Fome Zero!')

st.header('O Melhor lugar para encontrar seu mais novo restaurante favorito!')
st.subheader('Temos as seguintes marcas dentro da nossa plataforma:')

with st.container():
    col1,col2,col3,col4,col5 = st.columns(5)
    
    with col1:
        aux = df2.loc[:, 'restaurant_id'].nunique()
        col1.metric('Restaurantes Cadastrados', aux)

    with col2:
        aux = df2.loc[:, 'country'].nunique()
        col2.metric('Países Cadastrados', aux)
        
    with col3:
        aux = df2.loc[:, 'city'].nunique()
        col3.metric('Cidades Cadastrados', aux)
    with col4:
        aux = df2.loc[:, 'votes'].sum()
        formatted_aux = "{:,.2f}".format(aux).replace(",", ".")
        col4.metric('Avaliações feitas na Plataforma', formatted_aux)
    with col5:
        aux = df2.loc[:, 'cuisines_number'].nunique()
        col5.metric('Restaurantes Cadastrados', aux)

with st.container():
    st.markdown('# Country Maps') 
    df1['cust'] = df1['average_cost_for_two'].map(str) + '(' + df1['currency'] + ')' + 'Para dois'
    df1['nota'] = df1['aggregate_rating'].map(str) + '/' + '5'
    df1 = df1.reset_index()
    # Desenhar o mapa
    map = folium.Map( zoom_start=11 )
    marker_cluster = MarkerCluster().add_to(map)   
    
    for index, location in df1.iterrows():
        popup_info = f'{location["restaurant_name"]}<br> Price: {location["cust"]}<br> Type: {location["cuisines_number"]}<br> Aggragate Rating: {location["nota"]}'
        color = f'{location["color_name"]}'
        folium.Marker([location['latitude'],
                        location['longitude']],
                        popup = folium.Popup(popup_info,parse_html=False, max_width=300),
                        icon=folium.Icon(color=color, icon="home", prefix="fa")).add_to(marker_cluster)     
    folium_static(map, width=1024, height=768)


        
    
