# Documentação — Aula 03: Análise Exploratória com Streamlit + Dataset Tips

## O que é o Dataset Tips?

O dataset **tips** é um conjunto de dados clássico que registra informações sobre gorjetas em um restaurante americano.
Ele está disponível diretamente pela biblioteca **Seaborn** e contém **244 linhas** e **7 colunas**:

| Coluna       | Tipo    | Descrição                                    |
|--------------|---------|----------------------------------------------|
| `total_bill` | float   | Valor total da conta em dólares (US$)        |
| `tip`        | float   | Valor da gorjeta em dólares (US$)            |
| `sex`        | categórico | Sexo do pagador (Male / Female)           |
| `smoker`     | categórico | Se havia fumantes na mesa (Yes / No)      |
| `day`        | categórico | Dia da semana (Thur, Fri, Sat, Sun)       |
| `time`       | categórico | Turno da refeição (Lunch / Dinner)        |
| `size`       | int     | Número de pessoas na mesa                    |

---

## Como carregar o dataset

```python
import seaborn as sns

df = sns.load_dataset("tips")
```

Isso cria um **DataFrame do pandas** — uma tabela em memória com linhas e colunas, como uma planilha Excel.

---

## Estrutura do App (app2.py)

O app foi criado com **Streamlit**, um framework Python que transforma scripts em páginas web interativas.

### Estrutura básica de um app Streamlit

```python
import streamlit as st

st.title("Título da Página")
st.header("Seção")
st.subheader("Subseção")
st.write("Texto qualquer ou objeto Python")
st.dataframe(df)          # exibe uma tabela interativa
st.altair_chart(chart)    # exibe um gráfico Altair
st.info("Texto informativo em azul")
st.success("Texto de sucesso em verde")
st.metric("Rótulo", "Valor")
```

Para rodar o app:
```bash
streamlit run app2.py
```

---

## Conceitos de Análise Utilizados

### 1. Correlação de Pearson

Mede a força e direção da relação linear entre duas variáveis numéricas.

```python
correlacao = df["total_bill"].corr(df["tip"])
```

- Valor entre **-1 e 1**
- **> 0.7** → correlação forte
- **0.4–0.7** → moderada
- **< 0.4** → fraca
- **Negativo** → relação inversa

No dataset tips, a correlação é de ~**0.68** (moderada a forte positiva).

---

### 2. Agrupamento com groupby

Permite calcular estatísticas por grupo (média, soma, etc.):

```python
# Média de gorjeta por dia da semana
media_dia = df.groupby("day")["tip"].mean().reset_index()

# Soma do faturamento por dia
fat_dia = df.groupby("day")["total_bill"].sum().reset_index()
```

`reset_index()` transforma o índice de volta em coluna comum — boa prática antes de usar em gráficos.

---

### 3. Criação de novas colunas

```python
# Gasto por pessoa
df["gasto_por_pessoa"] = df["total_bill"] / df["size"]

# Percentual de gorjeta
df["pct_gorjeta"] = (df["tip"] / df["total_bill"]) * 100
```

---

### 4. Segmentação de dados em faixas (pd.cut)

Transforma valores contínuos em categorias:

```python
df["faixa_conta"] = pd.cut(
    df["total_bill"],
    bins=[0, 10, 20, 30, 50],
    labels=["0-10", "10-20", "20-30", "30-50"]
)
```

---

### 5. Identificação de Outliers pelo método IQR

O **IQR (Interquartile Range)** é a diferença entre o 3º e o 1º quartil.
Valores além de `Q3 + 1.5 * IQR` são considerados outliers.

```python
q1, q3 = df["total_bill"].quantile([0.25, 0.75])
iqr = q3 - q1
outliers = df[df["total_bill"] > q3 + 1.5 * iqr]
```

---

## Tipos de Gráficos Utilizados (Altair)

### Scatter Plot (Dispersão)

Usado para ver a relação entre duas variáveis numéricas.

```python
import altair as alt

chart = (
    alt.Chart(df)
    .mark_circle(opacity=0.6, size=60)     # pontos semi-transparentes
    .encode(
        x="total_bill",                     # eixo X
        y="tip",                            # eixo Y
        color="sex",                        # cor por grupo
        tooltip=["total_bill", "tip"],      # info ao passar o mouse
    )
    .interactive()                          # zoom e pan com mouse
)
```

Para adicionar uma linha de regressão:
```python
linha = chart.transform_regression("total_bill", "tip").mark_line(color="red")
st.altair_chart(chart + linha, use_container_width=True)
```

---

### Bar Chart (Gráfico de Barras)

Usado para comparar categorias.

```python
bar = (
    alt.Chart(media_dia)
    .mark_bar()
    .encode(
        x=alt.X("Dia", sort=["Thur", "Fri", "Sat", "Sun"]),  # ordem manual
        y="Gorjeta Média (US$)",
        color="Dia",
    )
)

# Adicionar rótulos nas barras
texto = bar.mark_text(dy=-10).encode(
    text=alt.Text("Gorjeta Média (US$):Q", format=".2f")  # 2 casas decimais
)

st.altair_chart(bar + texto, use_container_width=True)
```

---

### Boxplot

Visualiza a distribuição e os outliers de uma variável.

```python
box = (
    alt.Chart(df)
    .mark_boxplot(extent=1.5)   # extent=1.5 usa regra do IQR para bigodes
    .encode(
        x="sex",
        y="tip",
        color="sex",
    )
)
```

O boxplot mostra:
- **Linha central** → mediana
- **Caixa** → IQR (25% a 75% dos dados)
- **Bigodes** → 1.5 × IQR
- **Pontos fora** → outliers

---

### Histograma

Mostra a distribuição de frequência de uma variável numérica.

```python
hist = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("total_bill:Q", bin=alt.Bin(maxbins=20)),  # divide em até 20 faixas
        y="count()",
    )
)
```

---

## Layout com Colunas

```python
col1, col2 = st.columns(2)   # divide a tela em 2 colunas iguais

with col1:
    st.altair_chart(grafico1)

with col2:
    st.altair_chart(grafico2)
```

---

## Widget Interativo: selectbox

Permite ao usuário escolher uma opção:

```python
grupo_sel = st.selectbox("Analisar por:", ["sex", "smoker", "day", "time"])
media_pct = df.groupby(grupo_sel)["pct_gorjeta"].mean().reset_index()
```

O gráfico é reprocessado automaticamente toda vez que o usuário muda a seleção.

---

## Resumo: Fluxo do App

```
1. Carregar dados         → sns.load_dataset("tips")
2. Calcular métricas      → groupby, corr, quantile, pd.cut
3. Criar gráfico Altair   → alt.Chart(df).mark_*().encode(...)
4. Exibir no Streamlit    → st.altair_chart(chart, use_container_width=True)
5. Adicionar explicação   → st.info("...") / st.write("...")
```

---

## Comandos Úteis

| Ação                             | Código                                      |
|----------------------------------|---------------------------------------------|
| Rodar o app                      | `streamlit run app2.py`                     |
| Ver primeiras linhas             | `df.head()`                                 |
| Ver últimas linhas               | `df.tail()`                                 |
| Dimensões                        | `df.shape`                                  |
| Tipos de dados                   | `df.dtypes`                                 |
| Estatísticas básicas             | `df.describe()`                             |
| Média por grupo                  | `df.groupby("col")["outra"].mean()`         |
| Correlação                       | `df["a"].corr(df["b"])`                     |
| Criar coluna                     | `df["nova"] = df["a"] / df["b"]`            |
| Filtrar linhas                   | `df[df["coluna"] > valor]`                  |
| Percentil                        | `df["col"].quantile(0.75)`                  |
