#______________________________________________________________________________________________________________________________________________________
##IMPORTAÇÃO DOS PACOTES

import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
import geopandas as gpd
from shapely import wkt

#______________________________________________________________________________________________________________________________________________________
##DADOS DO REPOSITÓRIO

#Tabelas de deliberações e dados geoespaciais
deliberacoes_cmgdt = pd.read_csv('./dados/CMGDT.csv', sep=';')
latlong = pd.read_csv('./dados/viewplantacadastral_pontos.csv')

#Trata o número da inscrição para o padrão da tabela viewplantacadastral
deliberacoes_cmgdt['inscricao_lotes']=deliberacoes_cmgdt['INSCRIÇÃO'].str[:15]

#Junta as duas tabelas pelo número da inscrição
nova_tabela=deliberacoes_cmgdt.merge(latlong,how='left',left_on='inscricao_lotes', right_on='inscricao')
nova_tabela=nova_tabela[~nova_tabela['latitude'].isna()].reset_index().copy()

#Filtra por valores únicos para o filtro da sidebar
lista_del=deliberacoes_cmgdt['Nº DELIBERAÇÃO'].unique().tolist()
lista_del.insert(0,' ')
lista_prot=deliberacoes_cmgdt['PROTOCOLO'].unique().tolist()
lista_prot.insert(0,' ')
lista_razaosocial=deliberacoes_cmgdt['RAZÃO SOCIAL'].unique().tolist()
lista_razaosocial.insert(0,' ')
lista_logradouro=nova_tabela['nomevia'].unique().tolist()
lista_logradouro.insert(0,' ')

#______________________________________________________________________________________________________________________________________________________
##CÓDIGO

##Limpa valores de latitude e longitude em branco do mapa (estava dando erro!)
nova_tabela=nova_tabela[~nova_tabela['latitude'].isna()].reset_index().copy()

ultima_linha = len(nova_tabela)

df=nova_tabela.copy()
df2=latlong.copy()

df['geometry'] = df['geometry'].apply(wkt.loads)
df2['geometry'] = df2['geometry'].apply(wkt.loads)

gdf = gpd.GeoDataFrame(df, geometry='geometry', crs=4326)
gdf2 = gpd.GeoDataFrame(df2, geometry='geometry', crs=4326)
#gdf2.head()

lotes_cmgdt = gdf['geometry']
todos_lotes = gdf2['geometry']

m = folium.Map(location=[-26.9038,-48.6821], zoom_start=14, tiles="cartodbpositron")

##Insere a geometria dos lotes da localização das empresas aprovadas pelo conselho


#Insere a geometria de todos os lotes da cidade

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

##Padrão de visualização da página
st.set_page_config(layout="wide")

##Título acima do mapa
st.title('Mapa de deliberações do CMGDT')

##Mapa com as deliberações CMGDT
folium_static(m, width=1150, height=400)

#Tabela com deliberações

st.dataframe(deliberacoes_cmgdt)

##Sidebar e filtros
st.sidebar.subheader('Filtros:')
prot = st.sidebar.selectbox('Nº do Protocolo:',lista_prot)
razaosocial = st.sidebar.selectbox('Razão Social:',lista_razaosocial)
logradouro = st.sidebar.selectbox('Logradouro:',lista_logradouro)
ano = st.sidebar.slider('Ano da deliberação:', min_value=2000, max_value=2030, value=2021, step=1)
cadastro=st.sidebar.input('Cadastro: ', cadastro_inputbox)
st.text('___________________________________________________________________________________________________________________')
st.text('Prefeitura Municipal de Itajaí - Secretaria de Desenvolvimento Urbano e Habitação')
