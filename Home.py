import streamlit as st

st.set_page_config(page_title="Home", page_icon=":game_die:")


st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write('# Cury Company Growth Dashboard')

st.markdown(
    """
    Growth Dashboard foi contruido para acompanhar as metricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar o Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Metricas gerais de comportamento.
        - Visão Tatica: Indicadores semanais de crescimento.
        - Visão Geografica: Insights de geolocalizacao.
    - Visao Entregador:
        - Acompanhamento dos indicadores semanais de crescimento.
    - Visao Restaurantes:
        - Indicadores semanais de crescimento dos restaurantes
    ### Ask For Help
    - Time de Data Science """)