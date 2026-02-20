import streamlit as st
import pandas as pd
import seaborn as sns

st.title("Aula 01 - Streamlit + Dataset Iris!")

st.write("Adquirindo Sabamento Pesado!")

df = sns.load_dataset("iris")

st.subheader("Prévia do Dataset")
st.dataframe(df.tail())

st.subheader("Dimensões")
st.write(f"Dimensões: {df.shape}")
st.write(f"Linhas: {df.shape[0]}, Colunas: {df.shape[1]}")

st.subheader("Tipos de Dados:")
st.write(df.dtypes)

st.subheader("Resumo do DF")
st.write(df.describe())

st.sidebar.header("Filtros")
especies = df['species'].unique()
escolha = st.sidebar.selectbox("Espécie: ", especies)

df_filtrado = df[df["species"] == escolha]

st.write(df_filtrado)