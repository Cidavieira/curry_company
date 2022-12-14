#Libraries
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import re
import folium 
import streamlit as st
from PIL import Image 
from haversine import haversine
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Entregadores',layout='wide')

#===========================================
# Funções
#===========================================

def top_delivers(df1, top_asc):
    dez_entregadores=df1.loc[:,['City','Delivery_person_ID','Time_taken(min)']].groupby(['City','Delivery_person_ID']).max().sort_values(['City','Time_taken(min)'],ascending= top_asc).reset_index()
    df_aux1=dez_entregadores.loc[dez_entregadores['City']=='Metropolitian',:].head(10)
    df_aux2=dez_entregadores.loc[dez_entregadores['City']=='Urban',:].head(10)
    df_aux3=dez_entregadores.loc[dez_entregadores['City']=='Semi-Urban',:].head(10)
    df4=pd.concat([df_aux1,df_aux2,df_aux3]).reset_index(drop=True)
    st.dataframe(df4)
    return df4

def clean_code(df1):
    """ Esta função tem a responsabilidade de limpar o dataframe 
    
        Tipos de limpeza:
        1.Remoção dos dados NaN
        2.Mudança do tipo da coluna de dados
        3.Remoção dos espaços das variavéis de texto
        4.Formatação da coluna de datas
        5.Limpeza da coluna de tempo ( remoção do texto da variável numérica
        Input: Dataframe
        Output: Dataframe
    """
    #Tranformacao
    linhas_selecionadas=(df1['Delivery_person_Age']!='NaN ')
    df1=df1.loc[linhas_selecionadas,:].copy()
    df1['Delivery_person_Age']=df1['Delivery_person_Age'].astype(int)

    df1['Delivery_person_Ratings']=df1['Delivery_person_Ratings'].astype(float)

    df1['Order_Date']=pd.to_datetime(df1['Order_Date'],format='%d-%m-%Y')

    linhas_selecionadas=(df1['multiple_deliveries']!='NaN ')
    df1=df1.loc[linhas_selecionadas,:].copy()
    df1['multiple_deliveries']=df1['multiple_deliveries'].astype(int)

    linhas_selecionadas=(df1['City']!='NaN ')
    df1=df1.loc[linhas_selecionadas,:].copy()

    linhas_selecionadas=(df1['Delivery_person_Age']!='NaN ')
    df1=df1.loc[linhas_selecionadas,:].copy()

    linhas_selecionadas=(df1['Weatherconditions']!='conditions NaN ')
    df1=df1.loc[linhas_selecionadas,:].copy()

    linhas_selecionadas=(df1['Road_traffic_density']!='NaN ')
    df1=df1.loc[linhas_selecionadas,:].copy()

    linhas_selecionadas=(df1['Festival']!='NaN ')
    df1=df1.loc[linhas_selecionadas,:].copy()

    df1.loc[:,'ID']=df1.loc[:,'ID'].str.strip()
    df1.loc[:,'Road_traffic_density']=df1.loc[:,'Road_traffic_density'].str.strip()
    df1.loc[:,'Type_of_order']=df1.loc[:,'Type_of_order'].str.strip()
    df1.loc[:,'Type_of_vehicle']=df1.loc[:,'Type_of_vehicle'].str.strip()
    df1.loc[:,'City']=df1.loc[:,'City'].str.strip()
    df1.loc[:,'Festival']=df1.loc[:,'Festival'].str.strip()

    df1['week_of_year']=df1['Order_Date'].dt.strftime('%U')

    df1['Time_taken(min)']=df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)']=df1['Time_taken(min)'].astype(int)

    #selecao de linhas
    pedidos_dia=df1.loc[:,['ID','Order_Date']].groupby('Order_Date').count().reset_index()

    #desenhar o grafico de linhas
    #plotly
    px.bar(pedidos_dia,x='Order_Date',y='ID')

    return df1

#Import Dataset
df=pd.read_csv('repos\dataset/train.csv')
#df=pd.read_csv('dataset/train.csv')
#df=pd.read_csv('repos\FTC/train.csv')
df1= clean_code(df)

#===========================================
# Barra Lateral
#===========================================
st.header('Marketplace - Visão Entregadores')


image=Image.open('image.png')
st.sidebar.image(image,width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')

date_slider=st.sidebar.slider(
                  'Até qual valor?',
                   value=pd.datetime(2022,4,13),
                   min_value=pd.datetime(2022,2,11),
                   max_value=pd.datetime(2022,4,6),
                    format='DD-MM-YYYY')

st.sidebar.markdown("""---""")

traffic_options= st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low','Medium','High','Jam'],
    default=['Jam','Medium','High','Jam'])

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Aparecida Vieira')

#Filtro de data
linhas_selecionadas=df1['Order_Date']< date_slider
df1 = df1.loc[linhas_selecionadas,:]

#Filto de transito
linhas_selecionadas=df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas,:]
#st.dataframe( df1 )


#===========================================
# Layout no streamlit
#===========================================

tab1,tab2,tab3 = st.tabs( ['Visão Gerencial',' -' ,' - '] )
with tab1:
    with st.container():
        st.title( 'Overall Metrics' )
        
        col1,col2,col3,col4 = st.columns(4, gap='large')
        with col1:
            idade_entregadores_max=df1['Delivery_person_Age'].max()
            col1.metric('Maior idade',idade_entregadores_max)
        with col2:
            idade_entregadores_min=df1['Delivery_person_Age'].min()
            col2.metric('Menor idade',idade_entregadores_min)
        with col3:
            melhor_condicao=df1['Vehicle_condition'].max()
            col3.metric('Melhor Condição de veículos',melhor_condicao)
        with col4:
            pior_condicao=df1['Vehicle_condition'].min()
            col4.metric('Pior Condição de veículos', pior_condicao)
            
            
    with st.container():
        st.markdown ("""---""")
        st.title('Avaliações')
        
        col1,col2 = st.columns (2)
        with col1:
            st.markdown('##### Avaliação Média por entregador')
            media_entregador=df1.loc[:,['Delivery_person_ID','Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index()
            st.dataframe(media_entregador)
        with col2:
            st.markdown('##### Avaliação Média por trânsito')
            media_std=df1.loc[:,['Delivery_person_Ratings','Road_traffic_density']].groupby('Road_traffic_density').agg({'Delivery_person_Ratings':['mean','std']})

            media_std.columns=['delivery_mean','delivery_std']

            media_std.reset_index()
            st.dataframe(media_std)
            
            st.markdown('##### Avaliação Média por clima')
            media_std1=df1.loc[:,['Delivery_person_Ratings','Weatherconditions']].groupby('Weatherconditions').agg({'Delivery_person_Ratings':['mean','std']})
            media_std1.columns=['delivery_mean','delivery_std']
            media_std1.reset_index()
            st.dataframe(media_std1)
            
    with st.container():
        st.markdown ("""---""")
        st.title('Velocidade de Entrega')
        
        col1,col2=st.columns(2)
        
        with col1:
            st.markdown('##### Top entregadores mais rápidos')
            df3=top_delivers(df1, top_asc=True)
            st.dataframe(df3)
            
        with col2:
            st.markdown('##### Top entregadores mais lentos')
            df3=top_delivers(df1, top_asc=False)
            st.dataframe(df3)
                