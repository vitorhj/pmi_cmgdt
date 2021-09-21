#______________________________________________________________________________________________________________________________________________________
##IMPORTAÇÃO DOS PACOTES

import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
import geopandas as gpd

#______________________________________________________________________________________________________________________________________________________
##ESTRUTURA DA PÁGINA

st.set_page_config(layout="wide")

# # center on Liberty Bell
# m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)

# # add marker for Liberty Bell
# tooltip = "Liberty Bell"
# folium.Marker(
    # [39.949610, -75.150282], popup="Liberty Bell", tooltip=tooltip
# ).add_to(m)

# # call to render Folium map in Streamlit
# folium_static(m)


nova_tabela=pd.read_csv('nova_tabela.csv')
latlong =pd.read_csv('viewplantacadastral_pontos.csv')

ultima_linha=len(nova_tabela)
##Limpa valores de latitude e longitude em branco do mapa (estava dando erro!)
nova_tabela=nova_tabela[~nova_tabela['latitude'].isna()].reset_index().copy()


ultima_linha = len(nova_tabela)

from shapely import wkt
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

# folium.Choropleth(
    # geo_data=todos_lotes.head(10000),
    # name="choropleth",
    # fill_color='black',
    # fill_opacity=0.0,
    # line_opacity=0.1,
# ).add_to(m)

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

folium_static(m)
