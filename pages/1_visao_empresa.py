# Libraries

import plotly.express as px
import folium
from haversine import haversine

# Bibliotecas necessárias

import pandas as pd
import streamlit as st
from streamlit_folium import folium_static


st.set_page_config(page_title="Visão Empresa", page_icon=":chart_with_upwards_trend:", layout="wide")
# ---------------------------------------------------------------------
# Funções
# ---------------------------------------------------------------------

def country_maps(df1):

    cidade_e_trafego = (df1['City'] != 'NaN') & (df1['Road_traffic_density'] != 'NaN')
    df1 = df1.loc[cidade_e_trafego, :]

    df_aux = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()

    map = folium.Map()

    for i in range(len(df_aux)):
      folium.Marker([df_aux.loc[i, 'Delivery_location_latitude'], df_aux.loc[i, 'Delivery_location_longitude']], popup = df_aux.loc[i,'City'] ).add_to(map)

    folium_static (map, width = 1024, height = 600)

    return None






def order_share_by_week(df1):

    df_aux_1 = df1.loc[:, ['ID', 'Week_of_year']].groupby(['Week_of_year']).count().reset_index()
    df_aux_2 = df1.loc[:, ['Delivery_person_ID', 'Week_of_year']].groupby(['Week_of_year']).nunique().reset_index()

    df_aux = pd.merge(df_aux_1, df_aux_2, how = 'inner')
    df_aux['Order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']

    fig = px.line(df_aux, x = 'Week_of_year', y = 'Order_by_deliver')

    return fig






def order_by_week(df1):


    df1['Week_of_year'] = df1['Order_Date'].dt.strftime('%U')

    graf_2 = df1.loc[:, ['ID', 'Week_of_year']].groupby(['Week_of_year']).count().reset_index()
    fig = px.line(graf_2, x = 'Week_of_year', y = 'ID')

    return fig





def traffic_order_city(df1):

    cidade_e_trafego = (df1['City'] != 'NaN') & (df1['Road_traffic_density'] != 'NaN')

    graf_4 = df1.loc[cidade_e_trafego, ['ID', 'Road_traffic_density', 'City']].groupby(['City', 'Road_traffic_density']).count().reset_index()
    fig = px.scatter(graf_4, x = 'City', y = 'Road_traffic_density', size = 'ID', color = 'City')
    return fig





def traffic_order_share(df1):



    trafego_sem_nan = df1['Road_traffic_density'] != 'NaN'

    graf_3 = df1.loc[trafego_sem_nan, ['ID', 'Road_traffic_density']].groupby(['Road_traffic_density']).count().reset_index()
    graf_3['entregas_perc'] = graf_3['ID'] / graf_3['ID'].sum()

    fig = px.pie(graf_3, values = 'entregas_perc', names = 'Road_traffic_density')
    return fig





def order_metric(df1):

    graf_1 = df1.loc[:, ['ID', 'Order_Date']].groupby(['Order_Date']).count().reset_index()
    fig = px.bar(graf_1, x='Order_Date', y='ID')
    return fig




def clean_code(df1):
    """ Esta funcao tem a responsabilidade de limpar o dataframe
        
        Tipos de Limpeza:
        1- Remocao dos dados NaN
        2- Conversao de Delivery_person_Age para int
        3- Conversao de Delivery_person_Ratings para float
        4- Mudanca do formato de Order_Date para datetime d m Y
        5- Conversao de multiple_deliveries para int
        6- Conversao de Time_taken(min) para int e remocao de strings
        7- Remocao de espacos de colunas
        
        Input: Dataframe
        Output: Dataframe
        
    """
    # 1 Removendo 'NaN'
    linhas_sem_nan = (df1['Delivery_person_Age'] != 'NaN ') & (df1['City'] != 'NaN ') & (df1['multiple_deliveries'] != 'NaN ')

    df1 = df1.loc[linhas_sem_nan, :]

    # 2 Convertendo a coluna Age para int

    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    # 3 Convertendo a coluna Delivery_person_Ratings para float

    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    # 4 Convertendo a coluna Order_Date para formato data

    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y')

    # 5 Convertendo multiple_deliveries para int

    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    # 6 Removendo strings e convertendo Time_taken(min) para int

    df1['Time_taken(min)'] = df1['Time_taken(min)'].str.extract(pat = '(\d+)', expand = False).astype(int)

    # 7 Removendo espaços dentro de strings/texto/object

    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    return df1

# =========================================== Inicio da estrutura logica do codigo ===========================================

# ==========================================
# Import Dataset
# ==========================================

df = pd.read_csv('dataset/train.csv')


# ==========================================
# Limpando os dados
# ==========================================

df1 = clean_code(df)




#===========================================
# Barra Lateral
#===========================================

st.header('Marketplace - Visão Empresa')

#image_path = 
#image = Image.open(image_path)
#st.sidebar.image(image, width = 120)


st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider('Até qual valor?', value = pd.datetime(2022, 4, 13), min_value = pd.datetime(2022, 2, 11), max_value = pd.datetime(2022, 4, 6), format = 'DD-MM-YYYY')

st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect('Quais as condições do trânsito?', ['Low', 'Medium', 'High', 'Jam'], default = ['Low', 'Medium', 'High', 'Jam'])


# Filtro de data

linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]


# Filtro de transito

linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

st.dataframe(df1)

#==========================================
# Layout no Streamlit
#==========================================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])


with tab1:
    with st.container():
        # Order Metric
        fig = order_metric(df1)
        st.markdown('# Orders by Day')
        st.plotly_chart(fig, use_container_width = True)
        
        
    
    with st.container():
    
        col1, col2 = st.columns(2)
    
        with col1:
            
            fig = traffic_order_share(df1)
            st.header('Traffic Order Share')
            st.plotly_chart(fig, use_container_width = True)
            

            
        with col2:
            
            fig = traffic_order_city(df1)
            st.header('Traffic Order City')
            st.plotly_chart(fig, use_container_width = True)
            

            
with tab2:
    with st.container():
        
        fig = order_by_week(df1)
        st.markdown('Orders by week')
        st.plotly_chart(fig, use_container_width = True)
        

    with st.container():
        
        fig = order_share_by_week(df1)
        st.markdown("# Order Share by Week")
        st.plotly_chart(fig, use_container_width = True)
        

with tab3:
    
    st.markdown('# Country Map')
    country_maps(df1)
