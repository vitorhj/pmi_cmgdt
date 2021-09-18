
#______________________________________________________________________________________________________________________

## IMPORTA BIBLIOTECAS PARA O PYTHON

import pandas as pd
import os
#import folium
import re
#import geopandas as gpd
import streamlit as st


#_____________________________________________________________________________________________________________________

##ESTRUTURA PAGINA

st.text('teste 1234')
import pandas as pd
tabela_deliberacoes = pd.read_excel(os.path.join(folder,'Deliberações CMGDT.xlsx'))
#tabela_deliberacoes.head()
#import pandas as pd
#latlong =pd.read_csv(os.path.join(folder,'plantacadastral','viewplantacadastral_pontos.csv'))
#latlong.head()
#tabela_deliberacoes['inscricao_lotes']=tabela_deliberacoes['INSCRIÇÃO'].str[:15]
#tabela_deliberacoes.head()
#nova_tabela=tabela_deliberacoes.merge(latlong,how='left',left_on='inscricao_lotes', right_on='inscricao')
#nova_tabela.to_csv('/content/drive/MyDrive/dados_itajai/CMGDT/nova_tabela.csv}')
#ultima_linha=len(nova_tabela)

##Limpa valores de latitude e longitude em branco do mapa (estava dando erro!)
#nova_tabela=nova_tabela[~nova_tabela['latitude'].isna()].reset_index().copy()
#nova_tabela

#_____________________________________________________________________________________________________________________

##MAPA CMGDT

#from shapely import wkt
#df=nova_tabela.copy()
#df2=latlong.copy()

#df['geometry'] = df['geometry'].apply(wkt.loads)
#df2['geometry'] = df2['geometry'].apply(wkt.loads)

#gdf = gpd.GeoDataFrame(df, geometry='geometry', crs=4326)
#gdf2 = gpd.GeoDataFrame(df2, geometry='geometry', crs=4326)
#gdf2.head()

#lotes_cmgdt = gdf['geometry']
#todos_lotes = gdf2['geometry']

#m = folium.Map(location=[-26.9038,-48.6821], zoom_start=14, tiles="cartodbpositron")

##Insere a geometria dos lotes da localização das empresas aprovadas pelo conselho

#folium.Choropleth(
    #geo_data=lotes_cmgdt,
    #columnns=rsocial,
    #tooltip = prot,
    #fill_color='black',
    #fill_opacity=0.3,
    #line_opacity=0.5,
#).add_to(m)

##Insere a geometria de todos os lotes da cidade

#folium.Choropleth(
    #geo_data=todos_lotes.head(10000),
    #name="choropleth",
    #fill_color='black',
    #fill_opacity=0.0,
    #line_opacity=0.1,
#).add_to(m)

## Insere markers com as informções das empresas que foram para conselho

#ultima_linha = len(nova_tabela)

#for i in range(ultima_linha):
  #lat = nova_tabela.iloc[i]['latitude']
  #lon = nova_tabela.iloc[i]['longitude']
  #rsocial = nova_tabela.loc[i]['RAZÃO SOCIAL']
  #prot = nova_tabela.loc[i]['PROTOCOLO']
  #data = nova_tabela.loc[i]['DATA']
  #ndeliberacao = nova_tabela.loc[i]['Nº DELIBERAÇÃO']
  #cadastro = nova_tabela.loc[i]['CADASTRO']
  #endereco = nova_tabela.loc[i]['ENDEREÇO COMPLETO']
  #deliberacao = nova_tabela.loc[i]['DELIBERAÇÃO']

  #folium.Marker(
      #location=[lon,lat],
      #popup = 'Protocolo: '+prot+' , Nº Deliberação: '+str(ndeliberacao)+' , Data deliberação: '+str(data)+' , Razão Social: '+rsocial+' , Nº cadastro: '+str(cadastro)+ ', Endereço: '+str(endereco),
      #tooltip = 'Protocolo: '+prot+', Razão Social: '+rsocial,
      #icon=folium.Icon(color="black")
  #).add_to(m)

#m.add_child(folium.LayerControl())
#m.save(outfile=os.path.join(folder,'map.html'))

#m
