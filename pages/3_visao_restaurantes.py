#Libraries
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import re
import folium 
import streamlit as st
import numpy as np
from PIL import Image 
from haversine import haversine
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Restaurantes',layout='wide')
#===========================================
# Funções
#===========================================

def avg_std_time_on_traffic(df1):
    medio_std=df1.loc[:,['Time_taken(min)','City','Road_traffic_density']].groupby(['City','Road_traffic_density']).agg({'Time_taken(min)':['mean','std']})
    medio_std.columns=['entrega_media','entrega_std']
    medio_std=medio_std.reset_index()
    fig=px.sunburst(medio_std,path=['City','Road_traffic_density'],values='entrega_media',color='entrega_std',color_continuous_scale='RdBu',color_continuous_midpoint=np.average(medio_std['entrega_std']))
    return fig


def avg_std_time_graph(df1):
    medio_std=df1.loc[:,['City','Time_taken(min)']].groupby('City').agg({'Time_taken(min)':['mean','std']})
    medio_std.columns=['entrega_media','entrega_std']
    medio_std=medio_std.reset_index()
    fig=go.Figure()
    fig.add_trace(go.Bar(name='Control',x=medio_std['City'],y=medio_std['entrega_media'],
                         error_y=dict(type='data',array=medio_std['entrega_std'])))
    return fig


def avg_std_time_delivery(df1,festival,op):

    """
        Esta função calcula o tempo médio ao desvio padrão do tempo de entrega.
        Parâmetros:
            Imput:
                - df: Dataframe com os dados necessários para o cálculo
                - op: Tipo de operação que precisa ser calculado
                    'avg_time': Calcula o tempo medio
                    'std_time': Calcula o desvio padrão do tempo
            Output:
                - df: Dataframe com 2 colunas e 1 linha                
     """
               
    festivais=df1.loc[:,['Festival','Time_taken(min)']].groupby('Festival').agg({'Time_taken(min)':['mean','std']})
    festivais.columns=['avg_time','std_time']
    festivais=festivais.reset_index()
    festivais=np.round(festivais.loc[festivais['Festival']==festival,op],2)
    return festivais

def distance(df1,fig):
    if fig == False:
        df1['distance']=df1.loc[:,['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']].apply( lambda x: 
                                                                                                                                                   haversine((x['Restaurant_latitude'],x['Restaurant_longitude']),
                                                                                                                                                             (x['Delivery_location_latitude'],x['Delivery_location_longitude'])),axis=1)
        avg_distance=np.round(df1['distance'].mean(),2)
        return avg_distance
    else:
        df1['distance']=df1.loc[:,['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']].apply( lambda x: 
                                                                                                                                                   haversine((x['Restaurant_latitude'],x['Restaurant_longitude']),
                                                                                                                                                             (x['Delivery_location_latitude'],x['Delivery_location_longitude'])),axis=1)
        avg_distance=df1.loc[:,['City','distance']].groupby('City').mean().reset_index()
        fig=go.Figure(data=[go.Pie(labels=df1['City'],values=df1['distance'],pull=[0.1,0,0])])
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


#===========================================
#Import Dataset
#===========================================
df=pd.read_csv('repos\dataset/train.csv')
#df=pd.read_csv('dataset/train.csv')
#df=pd.read_csv('repos\FTC/train.csv')
df1=clean_code(df)

#===========================================
# Barra Lateral
#===========================================
st.header('Marketplace - Visão Restaurantes')

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
        st.title ( "Overal Metrics" )
        
        col1,col2,col3,col4,col5,col6= st.columns(6)
        with col1:
            entregadores_unicos=df['Delivery_person_ID'].nunique()
            col1.metric('Entregadores',entregadores_unicos)
        with col2:
            avg_distance = distance (df1,fig=False)
            col2.metric('A dist média entregas',avg_distance)
                          
        with col3:
            festivais=avg_std_time_delivery (df1,'Yes','avg_time')
            col3.metric('Tempo médio c/ fest',festivais)
        with col4:
            festivais=avg_std_time_delivery (df1,'Yes','std_time')
            col4.metric('Std entrega c/ fest',festivais)
        with col5:
            festivais=avg_std_time_delivery (df1,'No','avg_time')
            col5.metric('Tempo médio s/ fest',festivais)
        with col6:
            festivais=avg_std_time_delivery (df1,'No','std_time')
            col6.metric('Std entrega s/ fest',festivais)       
            
            
    with st.container():
        st.markdown( """---""" )
        st.title("Tempo Médio de entrega por cidade")

        fig=avg_std_time_graph(df1)
        st.plotly_chart(fig)        
            
        
    with st.container():
        st.markdown( """---""" )
        st.title("Distribuição do Tempo 1")
        fig=distance(df1,fig=True)
        st.plotly_chart(fig)


    with st.container():
        st.markdown( """---""" )
        st.title("Distribuição do Tempo 2")
        fig=avg_std_time_on_traffic(df1)
        st.plotly_chart(fig)
            
    with st.container():
        st.markdown( """---""" )
        st.title("Distribuição da Distância")
        medio_std=df1.loc[:,['Time_taken(min)','City','Type_of_order']].groupby(['City','Type_of_order']).agg({'Time_taken(min)':['mean','std']})
        medio_std.columns=['entrega_media','entrega_std']
        medio_std.reset_index()
        st.dataframe( medio_std )