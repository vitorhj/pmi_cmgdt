#______________________________________________________________________________________________________________________________________________________
##IMPORTAÇÃO DOS PACOTES

import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
import geopandas as gpd
from shapely import wkt
from PIL import Image

#______________________________________________________________________________________________________________________________________________________
##DADOS

#Logo Itajai
logo_image = ('./dados/logo.png')

#Tabelas de deliberações e dados geoespaciais
deliberacoes_cmgdt = pd.read_csv('./dados/CMGDT.csv', sep=';')
latlong = pd.read_csv('./dados/viewplantacadastral_pontos.csv')

#Trata o número da inscrição para o padrão da tabela viewplantacadastral
deliberacoes_cmgdt['inscricao_lotes']=deliberacoes_cmgdt['INSCRIÇÃO'].str[:15]

#Trata o ano das deliberações
deliberacoes_cmgdt['ano']=deliberacoes_cmgdt['DATA'].str[6:11]

#Junta as duas tabelas pelo número da inscrição
nova_tabela=deliberacoes_cmgdt.merge(latlong,how='left',left_on='inscricao_lotes', right_on='inscricao')
nova_tabela=nova_tabela[~nova_tabela['latitude'].isna()].reset_index().copy()

#Filtra por valores únicos para o filtro da sidebar
lista_del=deliberacoes_cmgdt['Nº DELIBERAÇÃO'].unique().tolist()
lista_del.insert(0,'')
lista_prot=deliberacoes_cmgdt['PROTOCOLO'].unique().tolist()
lista_prot.insert(0,'')
lista_razaosocial=deliberacoes_cmgdt['RAZÃO SOCIAL'].unique().tolist()
lista_razaosocial.insert(0,'')
lista_logradouro=nova_tabela['nomevia'].unique().tolist()
lista_logradouro.insert(0,'')

#______________________________________________________________________________________________________________________________________________________
##INPUTS DA PÁGINA DO STREAMLIT

##Padrão de visualização da página
st.set_page_config(layout="wide")
st.sidebar.image(logo_image, width=200)

##Sidebar e filtros
st.sidebar.subheader('Filtros:')
cadastro_sidebar=st.sidebar.text_input('Cadastro: ', '')
delib_sidebar = st.sidebar.selectbox('Nº da Deliberação:',lista_del)
prot_sidebar = st.sidebar.selectbox('Nº do Protocolo:',lista_prot)
razaosocial_sidebar = st.sidebar.selectbox('Razão Social:',lista_razaosocial)
logradouro_sidebar = st.sidebar.selectbox('Logradouro:',lista_logradouro)
ano_sidebar = st.sidebar.slider('Ano da deliberação:', min_value=2000, max_value=2030, value=2021, step=1)
#st.download_button(label='Download', data = deliberacoes_cmgdt, filename='deliberacoes_cmgdt.csv',mime='csv')

#______________________________________________________________________________________________________________________________________________________
##FILTRO DOS DADOS A PARTIR DA SIDEBAR

#Colunas da nova tabela
cadastro = nova_tabela['CADASTRO']
delib = nova_tabela['Nº DELIBERAÇÃO']
ano = nova_tabela['DATA']
protocolo = nova_tabela['PROTOCOLO']
rsocial = nova_tabela['RAZÃO SOCIAL']
logradouro = nova_tabela['nomevia']

#Filtro cadastro
if cadastro_sidebar != '':
    nova_tabela=nova_tabela[nova_tabela['CADASTRO']==int(cadastro_sidebar)]
    
#Filtro deliberação
if delib_sidebar != '':
    nova_tabela=nova_tabela[nova_tabela['Nº DELIBERAÇÃO']==delib_sidebar]
    
#Filtro protocolo   
if prot_sidebar != '':
    nova_tabela=nova_tabela[nova_tabela['PROTOCOLO']==prot_sidebar]

#Filtro razão social
if razaosocial_sidebar != '':
    nova_tabela=nova_tabela[nova_tabela['RAZÃO SOCIAL']==razaosocial_sidebar]

#Filtro pelo ano
#if logradouro_sidebar != '':
    #st.dataframe(nova_tabela[nova_tabela['RAZÃO SOCIAL']==razaosocial_sidebar])

#______________________________________________________________________________________________________________________________________________________
##TRATAMENTO DOS DADOS PARA GEOPANDAS

#Converte os dados da tabela em dados geoespaciais
nova_tabela=nova_tabela[~nova_tabela['latitude'].isna()].reset_index().copy()

ultima_linha = len(nova_tabela)

#Nova variável para cada tabela
df=nova_tabela.copy()
df2=latlong.copy()

df['geometry'] = df['geometry'].apply(wkt.loads)
df2['geometry'] = df2['geometry'].apply(wkt.loads)

gdf = gpd.GeoDataFrame(df, geometry='geometry', crs=4326)
gdf2 = gpd.GeoDataFrame(df2, geometry='geometry', crs=4326)
#gdf2.head()

lotes_cmgdt = gdf['geometry']
todos_lotes = gdf2['geometry']

#______________________________________________________________________________________________________________________________________________________
##PLOTAGEM DO MAPA

m = folium.Map(location=[-26.9038,-48.6821], zoom_start=14, tiles="cartodbpositron")

##Insere a geometria dos lotes das empresas aprovadas pelo conselho:

folium.Choropleth(
    geo_data=lotes_cmgdt,
    fill_color='black',
    fill_opacity=0.3,
    line_opacity=1,
).add_to(m)

## Insere markers com as informções das empresas que foram para conselho

ultima_linha = len(nova_tabela)

for i in range(ultima_linha):
  lat = nova_tabela.iloc[i]['latitude']
  lon = nova_tabela.iloc[i]['longitude']
  rsocial = nova_tabela.loc[i]['RAZÃO SOCIAL']
  prot = nova_tabela.loc[i]['PROTOCOLO']
  data = nova_tabela.loc[i]['DATA']
  ndeliberacao = nova_tabela.loc[i]['Nº DELIBERAÇÃO']
  cadastro = nova_tabela.loc[i]['CADASTRO']
  endereco = nova_tabela.loc[i]['ENDEREÇO COMPLETO']
  deliberacao = nova_tabela.loc[i]['DELIBERAÇÃO']

  folium.Marker(
      location=[lon,lat],
      popup = 'Protocolo: '+prot+' , Nº Deliberação: '+str(ndeliberacao)+' , Data deliberação: '+str(data)+' , Razão Social: '+rsocial+' , Nº cadastro: '+str(cadastro)+ ', Endereço: '+str(endereco),
      tooltip = 'Protocolo: '+prot+', Razão Social: '+rsocial,
      icon=folium.Icon(color="black")
  ).add_to(m)

m.add_child(folium.LayerControl())
#m.save(outfile=os.path.join(folder,'map.html'))

#______________________________________________________________________________________________________________________________________________________
##ESTRUTURA DA PÁGINA 

##Título acima do mapa
st.title('Mapa de deliberações do CMGDT')

##Mapa com as deliberações CMGDT
folium_static(m, width=1420, height=400)

#Tabela com deliberações
st.dataframe(nova_tabela)

 
st.text('_________________________________________________________________________________')

#Rodapé da página
st.text('Prefeitura Municipal de Itajaí - Secretaria de Desenvolvimento Urbano e Habitação')
st.text('Última atualização dos dados: 22/09/2021')
