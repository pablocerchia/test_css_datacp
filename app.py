import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

#st.header('')

st.set_page_config(page_title='Control Cuotas', layout='wide')
conn = st.connection("gsheets", type=GSheetsConnection)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1Y0yQPfLo4XgTd3BXPFlAJpJs2WC-2TZ9lr0usZxdUZs/edit#gid=1573688581"
df = conn.read(spreadsheet=spreadsheet_url,ttl='30m')

spreadsheet_url2 = "https://docs.google.com/spreadsheets/d/1Y0yQPfLo4XgTd3BXPFlAJpJs2WC-2TZ9lr0usZxdUZs/edit?usp=sharing"
df2 = conn.read(spreadsheet=spreadsheet_url2,ttl='30m')
# Count duplicates in the 'ipAddress' column
num_duplicates = df2.duplicated(subset=['ipAddress']).sum()

# Find unique cases of duplicates
unique_duplicates = df2[df2.duplicated(subset=['ipAddress'], keep=False)].drop_duplicates(subset=['ipAddress'], keep='last')
num_unique_duplicates = unique_duplicates.shape[0]
total_rows = df2.shape[0]

# Percentage of cases that are duplicates
percentage_duplicates = (num_duplicates / total_rows) * 100

# Percentage of unique cases of duplicates out of the total
percentage_unique_duplicates = (num_unique_duplicates / total_rows) * 100
rounded_percentage_duplicates = round(percentage_duplicates, 2)
rounded_percentage_unique_duplicates = round(percentage_unique_duplicates, 2)



df = df.drop_duplicates(subset=['ipAddress'], keep='first')




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

st.write(f"Cantidad casos duplicados: {num_duplicates} ({rounded_percentage_duplicates}%)")
st.write(f"Cantidad casos duplicados unicos: {num_unique_duplicates} ({rounded_percentage_unique_duplicates}%)")
