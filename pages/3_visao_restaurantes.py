# Libraries

import plotly.express as px
import folium
from haversine import haversine

# Bibliotecas necessárias

import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title = 'Visão Restaurantes', page_icon = ':spaghetti:', layout = 'wide')


# ==========================================================================
# Funcoes
# ==========================================================================

def mean_std_city_type(df1):

    st.title('Distribuição da Distância')

    city_type_avg_std = df1.loc[:, ['Time_taken(min)', 'City', 'Type_of_order']].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)': ['mean', 'std']})
    city_type_avg_std.columns = ['Time_taken_mean', 'Time_taken_std']
    city_type_avg_std = city_type_avg_std.reset_index()

    return city_type_avg_std





def mean_std_city_traffic_graph(df1):

    city_traffic_avg_std = df1.loc[df1['Road_traffic_density'] != 'NaN', ['Time_taken(min)', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']})
    city_traffic_avg_std.columns = ['Time_taken_mean', 'Time_taken_std']
    city_traffic_avg_std = city_traffic_avg_std.reset_index()

    fig = px.sunburst(city_traffic_avg_std, path = ['City', 'Road_traffic_density'], values = 'Time_taken_mean', color = 'Time_taken_std', color_continuous_scale = 'RdBu', color_continuous_midpoint = np.average(city_traffic_avg_std['Time_taken_std']))

    return fig






def avg_distance(df1):

    df1['Distance'] = df1.loc[: , ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']].apply(lambda x: haversine((x['Delivery_location_latitude'], x['Delivery_location_longitude']), (x['Restaurant_latitude'], x['Restaurant_longitude'])), axis = 1)

    df1['Distance'] = df1.loc[:, ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']].apply(lambda x: haversine((x['Delivery_location_latitude'], x['Delivery_location_longitude']), (x['Restaurant_latitude'], x['Restaurant_longitude'])), axis = 1)

    avg_distance = df1.loc[:, ['City', 'Distance']].groupby('City').mean().reset_index()

    fig =go.Figure(data = [go.Pie(labels = avg_distance['City'], values = avg_distance['Distance'], pull = [0, 0.05, 0])])

    return fig






def avg_std_time_graph(df1):

    city_avg_std = df1.loc[:, ['City', 'Time_taken(min)']].groupby(['City']).agg({'Time_taken(min)': ['mean', 'std']})
    city_avg_std.columns = ['Time_taken_mean', 'Time_taken_std']
    city_avg_std = city_avg_std.reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar( name = 'Control', x = city_avg_std['City'], y = city_avg_std['Time_taken_mean'], error_y = dict(type = 'data', array = city_avg_std['Time_taken_std'])))

    fig.update_layout(barmode = 'group')

    return fig






def std_festival(df1, festival):
    
    """
        Esta funcao calcula o desvio padrao do tempo de entrega.
        Parâmetros:
            Input:
                - df: Dataframe com os dados necessarios para o calculo
                - festival: Operaçao com ou sem festival
                    'Yes': Durante festival
                    'No': Fora de período de festival
            Output:
                - Dataframe com 2 colunas e 1 linha.
    """

    tempo_festivais = df1.loc[df1['Festival'] == festival, ['Festival', 'Time_taken(min)']].groupby('Festival').std().reset_index()
    tempo_festivais = np.round(tempo_festivais.loc[:, 'Time_taken(min)'], 2)

    return tempo_festivais





def mean_festival(df1, festival):
    """
        Esta funcao calcula o tempo medio das entregas.
        Parâmetros:
            Input:
                - df: Dataframe com os dados necessarios para o calculo
                - festival: Operaçao com ou sem festival
                    'Yes': Durante festival
                    'No': Fora de período de festival
            Output:
                - Dataframe com 2 colunas e 1 linha.
    """

    tempo_festivais = df1.loc[df1['Festival'] == festival, ['Festival', 'Time_taken(min)']].groupby('Festival').mean().reset_index()
    tempo_festivais = np.round(tempo_festivais.loc[:, 'Time_taken(min)'], 2)
    
    return tempo_festivais





def distance(df1):

    df1['Distance'] = df1.loc[: , ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']].apply(lambda x: haversine((x['Delivery_location_latitude'], x['Delivery_location_longitude']), (x['Restaurant_latitude'], x['Restaurant_longitude'])), axis = 1)

    media_distancias = np.round(df1['Distance'].mean(), 2)

    return media_distancias





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

#===========================================
# Importante dataset
#===========================================

df = pd.read_csv('dataset/train.csv')



#===========================================
# Limpando os dados
#===========================================


df1 = clean_code(df)


#===========================================
# Barra Lateral
#===========================================


st.header('Marketplace - Visão Restaurantes')

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

weatherconditions_options = st.sidebar.multiselect('Qual a condição climática?', ['conditions Sunny', 'conditions Stormy', 'conditions Sandstorms', 'conditions Cloudy', 'conditions Fog', 'conditions Windy'], default = ['conditions Sunny', 'conditions Stormy', 'conditions Sandstorms', 'conditions Cloudy', 'conditions Fog', 'conditions Windy'])

# Filtro de data

data_selecionada = df1['Order_Date'] < date_slider
df1 = df1.loc[data_selecionada, :]


# Filtro de transito

linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de clima

clima_selecionado = df1['Weatherconditions'].isin(weatherconditions_options)
df1 = df1.loc[clima_selecionado, :]

#==========================================
# Layout no Streamlit
#==========================================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '', ''])

with tab1:
    with st.container():
        st.title('Overall Metrics')
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            
            entregadores_unicos = len(df1['Delivery_person_ID'].unique())

            col1.metric('Entregadores', entregadores_unicos)
            
        with col2:
            
            media_distancias = distance(df1)
            col2.metric('Média KM', media_distancias)
            
            


        with col3: 
            
            
            tempo_festivais = mean_festival(df1, festival = 'Yes')
            col3.metric('Tempo Festivais', tempo_festivais)
            
            
        with col4:
            

            tempo_festivais = std_festival(df1, festival = 'Yes')
            col4.metric('STD Festivais', tempo_festivais)
  
        with col5:
            
            tempo_festivais = mean_festival(df1, festival = 'No')
            col5.metric('Tempo Entregas', tempo_festivais)
            
        with col6:
            
            tempo_festivais = std_festival(df1, 'No')
            col6.metric('STD Entregas', tempo_festivais)
            
    with st.container():
        
        st.markdown("""---""")
        fig = avg_std_time_graph(df1)
        st.plotly_chart(fig)
        
    with st.container():
        
        st.markdown("""---""")
        st.title('Distribuição do Tempo')
        
        col1, col2 = st.columns(2)
        
        with col1:
            
            fig = avg_distance(df1)
            st.plotly_chart(fig)
                                    
            
        with col2:

            fig = mean_std_city_traffic_graph(df1)
            st.plotly_chart(fig)
            
    with st.container():
        
        st.markdown("""---""")
        city_type_avg_std = mean_std_city_type(df1)
        st.dataframe(city_type_avg_std)