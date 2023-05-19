#Libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import re
import folium 
from PIL import Image 
from haversine import haversine
from streamlit_folium import folium_static
from datetime import datetime


st.set_page_config(page_title='Visão Empresa',layout='wide')


#===========================================
# Funções
#===========================================

def country_maps(df1):
    localizacao= df1.loc[:,['City','Road_traffic_density','Delivery_location_latitude','Delivery_location_longitude']].groupby(['City','Road_traffic_density']).mean().reset_index()
    map=folium.Map()
    for index,location_info in localizacao.iterrows():
            folium.Marker([location_info['Delivery_location_latitude'],
                           location_info['Delivery_location_longitude']],
                           popup=location_info[['City','Road_traffic_density']]).add_to(map)

    folium_static(map,width=1024,height=600)
    return None
         
def order_share_by_week(df1):
    pedido_entregador_semana=df1.loc[:,['ID','week_of_year']].groupby('week_of_year').count().reset_index()
    pedido_entregador_semana1=df1.loc[:,['Delivery_person_ID','week_of_year']].groupby('week_of_year').nunique().reset_index()
    pedido_entregador_semana=pd.merge(pedido_entregador_semana,pedido_entregador_semana1,how='inner',on='week_of_year')
    pedido_entregador_semana['order_by_delivery']=(pedido_entregador_semana['ID']/pedido_entregador_semana['Delivery_person_ID'])
    fig=px.line(pedido_entregador_semana,x='week_of_year',y='order_by_delivery')
    return fig


def order_by_week(df1):
    pedidos_semana=df1.loc[:,['ID','week_of_year']].groupby('week_of_year').count().reset_index()
    fig=px.line(pedidos_semana,x='week_of_year',y='ID')
    return fig #aquiiiiiiiiiiiiiiiiiiiii df1

def traffic_order_city(df1):
    volume=df1.loc[:,['ID','City','Road_traffic_density']].groupby(['City','Road_traffic_density']).count().reset_index()
    fig=px.scatter(volume,x='City',y='Road_traffic_density',size='ID',color='City')
    return fig

def traffic_order_share(df1):
    pedidos_tipo_trafego=df1.loc[:,['ID','Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    fig=px.pie(pedidos_tipo_trafego,values='ID',names='Road_traffic_density')
    return fig

def order_metric(df1):
    pedidos_dia=df1.loc[:,['ID','Order_Date']].groupby('Order_Date').count().reset_index()
    fig=px.bar(pedidos_dia,x='Order_Date',y='ID')
    return fig   

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
#-----------------------Inicio da Estrutura lógica do código --------------------------------------
#===========================================
# #Import dataset
#===========================================

df=pd.read_csv('dataset/train.csv')
#C:\Users\Cida\repos\dataset
#df=pd.read_csv('repos\FTC/train.csv')

#===========================================
# Limpando os dadosl
#===========================================

df1=clean_code(df)

#===========================================
# Barra Lateral
#===========================================

st.header('Marketplace - Visão Cliente')


#image=Image.open('image.png')
#st.sidebar.image(image,width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

#st.sidebar.markdown('## Selecione uma data limite')

#date_slider=st.sidebar.slider(
                 # 'Até qual valor?',
                  # value=pd.datetime(2022,4,13),
                  # min_value=pd.datetime(2022,2,11),
                   #max_value=pd.datetime(2022,4,6),
                   #format='DD-MM-YYYY')

#st.sidebar.markdown("""---""")

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
st.dataframe( df1 )


#===========================================
# Layout no streamlit
#===========================================

tab1,tab2,tab3 = st.tabs( ['Visão Gerencial','Visão Tática','Visão Geográfica'] )

with tab1:
    with st.container():
        fig= order_metric(df1)
        st.markdown( '# Orders by Day' )
        st.plotly_chart(fig,use_container_width=True)
            
    with st.container():
        col1, col2 = st.columns( 2 )
        
        with col1:
            fig=traffic_order_share( df1)
            st.header(" Traffic Order Share")
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.header(" Traffic Order City")
            fig=traffic_order_city(df1)
            st.plotly_chart(fig,use_container_width=True)   
    
with tab2:
    with st.container():
        st.markdown("# Order by Week")
        fig=order_by_week(df1)
        st.plotly_chart(fig,use_container_width=True)   
    
    with st.container():
        st.markdown("# Order Share by Week")
        fig=order_share_by_week(df1)
        st.plotly_chart(fig,use_container_width=True)
           
with tab3:
    st.markdown("# Country Map")
    country_maps(df1)
   

    
   
