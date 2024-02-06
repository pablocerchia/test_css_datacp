import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

#st.header('')

st.set_page_config(page_title='Control Cuotas', layout='wide')
conn = st.connection("gsheets", type=GSheetsConnection)
spreadsheet_url = st.secrets["spreadsheet"]
df = conn.read(spreadsheet=spreadsheet_url)


cuotas = pd.read_excel('Cuotas.xlsx', sheet_name='Hoja1')
cuotas= cuotas[['municipio', 'Cuota']]

localidades_pablo = ['Barros Blancos', 'Naranjal', 'Tandil', 'Ibarra']
localidades_maga = ["Trenque Lauquen", "Granadero Baigorria", "Salto", "Montevideo"]
localidades_fausti = ["Pando", "Naranjito", "Mendoza", "Milagro"]

# Pablo
filtered_df_pablo = df[df['municipio'].isin(localidades_pablo)]
municipio_counts_df_pablo = filtered_df_pablo['municipio'].value_counts().reset_index()
municipio_counts_df_pablo.columns = ['municipio', 'Count']
df_final_pablo = pd.merge(municipio_counts_df_pablo, cuotas, on='municipio', how='inner')
df_final_pablo['% completado'] = ((df_final_pablo['Count'] / df_final_pablo['Cuota'])*100).round(2)
df_final_pablo = df_final_pablo[['municipio', 'Count', 'Cuota', '% completado']]

# Maga
filtered_df_maga = df[df['municipio'].isin(localidades_maga)]
municipio_counts_df_maga = filtered_df_maga['municipio'].value_counts().reset_index()
municipio_counts_df_maga.columns = ['municipio', 'Count']
df_final_maga = pd.merge(municipio_counts_df_maga, cuotas, on='municipio', how='inner')
df_final_maga['% completado'] = ((df_final_maga['Count'] / df_final_maga['Cuota'])*100).round(2)
df_final_maga = df_final_maga[['municipio', 'Count', 'Cuota', '% completado']]

# Fausti
filtered_df_fausti = df[df['municipio'].isin(localidades_fausti)]
municipio_counts_df_fausti = filtered_df_fausti['municipio'].value_counts().reset_index()
municipio_counts_df_fausti.columns = ['municipio', 'Count']
df_final_fausti = pd.merge(municipio_counts_df_fausti, cuotas, on='municipio', how='inner')
df_final_fausti['% completado'] = ((df_final_fausti['Count'] / df_final_fausti['Cuota'])*100).round(2)
df_final_fausti = df_final_fausti[['municipio', 'Count', 'Cuota', '% completado']]

col1, col2, col3 = st.columns(3)

with col1:
    st.write('Pablo')
    st.dataframe(df_final_pablo, use_container_width=True, hide_index=True)

with col2:
    st.write('Maga')
    st.dataframe(df_final_maga, use_container_width=True, hide_index=True)

with col3:
    st.write('Fausti')
    st.dataframe(df_final_fausti, use_container_width=True, hide_index=True)
