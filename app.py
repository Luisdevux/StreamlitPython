import streamlit as st
import pandas as pd
import seaborn as sns
import altair as alt

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
selecionadas = st.sidebar.multiselect("Espécies", especies, default=list(especies))

df_filtrado = df[df["species"].isin(selecionadas)]

st.write(df_filtrado)

st.subheader("Gráfico Scatter plot")

x_axis = st.sidebar.selectbox("Eixo X", ['sepal_length', 'sepal_width', 'petal_length', 'petal_width'], index=0)
y_axis = st.sidebar.selectbox("Eixo Y", ['sepal_length', 'sepal_width', 'petal_length', 'petal_width'], index=1)

chart = alt.Chart(df_filtrado).mark_circle(size=60).encode(
    x=x_axis,
    y=y_axis,
    color='species',
    tooltip=['sepal_length','sepal_width','petal_length','petal_width','species']
).interactive()

st.altair_chart(chart, use_container_width=True)