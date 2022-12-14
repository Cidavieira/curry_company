import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    layout='wide'
)

#image_path=
image = Image.open('image.png')
st.sidebar.image(image,width=120)


st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")
st.write(" Curry Company Growth Dashboard")

st.markdown(
    """
    Growth Dashboard foi construído pra acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dasboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas Gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurante
        - Indicadores semanais de crescimento dos Restaurantes
    ### Ask for Help
    - Time de Data Science no Discord
        - @Cida.vieira#8158
    """
)