import streamlit as st
import pandas as pd
import seaborn as sns
import altair as alt
import numpy as np

st.set_page_config(page_title="Análise Dataset Tips", layout="wide")
st.title("Aula 03 - Análise Exploratória: Dataset Tips")
st.write("Respondendo às perguntas da atividade com base nos dados reais do restaurante.")

df = sns.load_dataset("tips")

# ─── Visão Geral ─────────────────────────────────────────────────────────────
with st.expander("Visão Geral do Dataset", expanded=False):
    st.dataframe(df.head())
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Linhas:** {df.shape[0]}  |  **Colunas:** {df.shape[1]}")
        st.write(df.dtypes)
    with col2:
        st.write("**Estatísticas Descritivas:**")
        st.dataframe(df.describe())

st.markdown("---")

# ─── Questão 1 ───────────────────────────────────────────────────────────────
st.header("1. Existe correlação entre total_bill e tip?")
correlacao = df["total_bill"].corr(df["tip"])
st.write(f"**Correlação de Pearson:** `{correlacao:.4f}`")

scatter1 = (
    alt.Chart(df)
    .mark_circle(opacity=0.6, size=60)
    .encode(
        x=alt.X("total_bill", title="Valor Total da Conta (US$)"),
        y=alt.Y("tip", title="Gorjeta (US$)"),
        color=alt.Color("sex", legend=alt.Legend(title="Sexo")),
        tooltip=["total_bill", "tip", "sex", "day"],
    )
    .properties(title="Correlação: Valor da Conta × Gorjeta")
    .interactive()
)
linha1 = scatter1.transform_regression("total_bill", "tip").mark_line(color="red", strokeDash=[6, 3])
st.altair_chart(scatter1 + linha1, use_container_width=True)
st.info(
    f"A correlação de **{correlacao:.2f}** indica uma **relação positiva moderada a forte**. "
    "A linha de tendência vermelha confirma que contas maiores tendem a gerar gorjetas maiores."
)

st.markdown("---")

# ─── Questão 2 ───────────────────────────────────────────────────────────────
st.header("2. Quanto maior a conta, maior tende a ser a gorjeta?")
st.write(
    "Sim, há uma tendência clara. A correlação (~0.68) é considerada **moderada a forte**. "
    "Isso significa que existe uma relação linear consistente, embora não perfeita — "
    "há variação individual (algumas mesas altas deixam gorjetas proporcionalmente pequenas)."
)
df_bin = df.copy()
df_bin["faixa_conta"] = pd.cut(df["total_bill"], bins=[0, 10, 20, 30, 50], labels=["0-10", "10-20", "20-30", "30-50"])
media_faixa = df_bin.groupby("faixa_conta", observed=True)["tip"].mean().reset_index()
media_faixa.columns = ["Faixa da Conta (US$)", "Gorjeta Média (US$)"]
bar_faixa = (
    alt.Chart(media_faixa)
    .mark_bar(color="#4C78A8")
    .encode(
        x=alt.X("Faixa da Conta (US$)", sort=None),
        y=alt.Y("Gorjeta Média (US$)"),
        tooltip=["Faixa da Conta (US$)", "Gorjeta Média (US$)"],
    )
    .properties(title="Gorjeta Média por Faixa de Valor da Conta")
)
st.altair_chart(bar_faixa, use_container_width=True)

st.markdown("---")

# ─── Questão 3 ───────────────────────────────────────────────────────────────
st.header("3. Qual dia da semana apresenta a maior média de gorjeta?")
media_dia = df.groupby("day")["tip"].mean().reset_index()
media_dia.columns = ["Dia", "Gorjeta Média (US$)"]
ordem_dias = ["Thur", "Fri", "Sat", "Sun"]
bar_dia = (
    alt.Chart(media_dia)
    .mark_bar()
    .encode(
        x=alt.X("Dia", sort=ordem_dias, title="Dia da Semana"),
        y=alt.Y("Gorjeta Média (US$)"),
        color=alt.Color("Dia", sort=ordem_dias, legend=None),
        tooltip=["Dia", "Gorjeta Média (US$)"],
    )
    .properties(title="Gorjeta Média por Dia da Semana")
)
texto_dia = bar_dia.mark_text(dy=-10, fontSize=13).encode(
    text=alt.Text("Gorjeta Média (US$):Q", format=".2f")
)
st.altair_chart(bar_dia + texto_dia, use_container_width=True)
melhor_dia = media_dia.loc[media_dia["Gorjeta Média (US$)"].idxmax(), "Dia"]
st.info(f"**{melhor_dia}** é o dia com a maior média de gorjeta. Domingos e sábados tendem a ter clientes mais generosos, possivelmente por ser fim de semana e ambiente mais descontraído.")

st.markdown("---")

# ─── Questão 4 ───────────────────────────────────────────────────────────────
st.header("4. Qual dia da semana possui o maior faturamento total?")
fat_dia = df.groupby("day")["total_bill"].sum().reset_index()
fat_dia.columns = ["Dia", "Faturamento Total (US$)"]
bar_fat = (
    alt.Chart(fat_dia)
    .mark_bar(color="#F58518")
    .encode(
        x=alt.X("Dia", sort=ordem_dias, title="Dia da Semana"),
        y=alt.Y("Faturamento Total (US$)"),
        tooltip=["Dia", "Faturamento Total (US$)"],
    )
    .properties(title="Faturamento Total por Dia da Semana")
)
texto_fat = bar_fat.mark_text(dy=-10, fontSize=13).encode(
    text=alt.Text("Faturamento Total (US$):Q", format=".0f")
)
st.altair_chart(bar_fat + texto_fat, use_container_width=True)
melhor_fat = fat_dia.loc[fat_dia["Faturamento Total (US$)"].idxmax(), "Dia"]
st.info(f"**{melhor_fat}** é o dia com maior faturamento total. Sábado concentra o maior volume de atendimentos, tornando-o o dia mais lucrativo do restaurante.")

st.markdown("---")

# ─── Questão 5 ───────────────────────────────────────────────────────────────
st.header("5. Existe relação entre o número de pessoas (size) e a gorjeta (tip)?")
corr_size_tip = df["size"].corr(df["tip"])
scatter5 = (
    alt.Chart(df)
    .mark_circle(opacity=0.5, size=80)
    .encode(
        x=alt.X("size:O", title="Número de Pessoas na Mesa"),
        y=alt.Y("tip", title="Gorjeta (US$)"),
        color=alt.Color("day", legend=alt.Legend(title="Dia")),
        tooltip=["size", "tip", "day", "total_bill"],
    )
    .properties(title="Número de Pessoas × Gorjeta")
    .interactive()
)
st.altair_chart(scatter5, use_container_width=True)
st.info(f"Correlação size × tip: **{corr_size_tip:.2f}**. Mesas maiores tendem a deixar gorjetas maiores em valor absoluto, mas proporcionalmente a gorjeta por pessoa pode ser menor.")

st.markdown("---")

# ─── Questão 6 ───────────────────────────────────────────────────────────────
st.header("6. Existe relação entre o número de pessoas (size) e o valor total da conta (total_bill)?")
corr_size_bill = df["size"].corr(df["total_bill"])
scatter6 = (
    alt.Chart(df)
    .mark_circle(opacity=0.5, size=80)
    .encode(
        x=alt.X("size:O", title="Número de Pessoas na Mesa"),
        y=alt.Y("total_bill", title="Valor Total da Conta (US$)"),
        color=alt.Color("time", legend=alt.Legend(title="Turno")),
        tooltip=["size", "total_bill", "day", "time"],
    )
    .properties(title="Número de Pessoas × Valor Total da Conta")
    .interactive()
)
st.altair_chart(scatter6, use_container_width=True)
st.info(f"Correlação size × total_bill: **{corr_size_bill:.2f}**. A relação é positiva e esperada: mais pessoas na mesa geram contas mais altas.")

st.markdown("---")

# ─── Questão 7 ───────────────────────────────────────────────────────────────
st.header("7. Qual é o valor médio gasto por pessoa em cada dia da semana?")
df["gasto_por_pessoa"] = df["total_bill"] / df["size"]
media_pessoa = df.groupby("day")["gasto_por_pessoa"].mean().reset_index()
media_pessoa.columns = ["Dia", "Gasto Médio por Pessoa (US$)"]
bar7 = (
    alt.Chart(media_pessoa)
    .mark_bar(color="#72B7B2")
    .encode(
        x=alt.X("Dia", sort=ordem_dias, title="Dia da Semana"),
        y=alt.Y("Gasto Médio por Pessoa (US$)"),
        tooltip=["Dia", "Gasto Médio por Pessoa (US$)"],
    )
    .properties(title="Gasto Médio por Pessoa (total_bill / size)")
)
texto7 = bar7.mark_text(dy=-10, fontSize=13).encode(
    text=alt.Text("Gasto Médio por Pessoa (US$):Q", format=".2f")
)
st.altair_chart(bar7 + texto7, use_container_width=True)
st.info("Sexta-feira costuma apresentar o maior gasto médio por pessoa, sugerindo grupos menores com maior poder aquisitivo ou cardápio mais caro.")

st.markdown("---")

# ─── Questão 8 ───────────────────────────────────────────────────────────────
st.header("8. Homens e mulheres deixam gorjetas diferentes, em média?")
media_sexo = df.groupby("sex")["tip"].mean().reset_index()
media_sexo.columns = ["Sexo", "Gorjeta Média (US$)"]
col_a, col_b = st.columns(2)
with col_a:
    bar8 = (
        alt.Chart(media_sexo)
        .mark_bar()
        .encode(
            x=alt.X("Sexo"),
            y=alt.Y("Gorjeta Média (US$)"),
            color=alt.Color("Sexo", legend=None),
            tooltip=["Sexo", "Gorjeta Média (US$)"],
        )
        .properties(title="Gorjeta Média por Sexo")
    )
    texto8 = bar8.mark_text(dy=-10, fontSize=13).encode(
        text=alt.Text("Gorjeta Média (US$):Q", format=".2f")
    )
    st.altair_chart(bar8 + texto8, use_container_width=True)
with col_b:
    box8 = (
        alt.Chart(df)
        .mark_boxplot(extent="min-max")
        .encode(
            x=alt.X("sex", title="Sexo"),
            y=alt.Y("tip", title="Gorjeta (US$)"),
            color=alt.Color("sex", legend=None),
        )
        .properties(title="Distribuição das Gorjetas por Sexo")
    )
    st.altair_chart(box8, use_container_width=True)
st.info("Homens deixam, em média, gorjetas ligeiramente maiores. Contudo, a diferença não é expressiva; ambos os grupos têm distribuição similar com alguns outliers.")

st.markdown("---")

# ─── Questão 9 ───────────────────────────────────────────────────────────────
st.header("9. Fumantes e não fumantes têm comportamentos diferentes em relação à gorjeta?")
media_fumante = df.groupby("smoker")["tip"].mean().reset_index()
media_fumante.columns = ["Fumante", "Gorjeta Média (US$)"]
col_c, col_d = st.columns(2)
with col_c:
    bar9 = (
        alt.Chart(media_fumante)
        .mark_bar()
        .encode(
            x=alt.X("Fumante"),
            y=alt.Y("Gorjeta Média (US$)"),
            color=alt.Color("Fumante", legend=None),
            tooltip=["Fumante", "Gorjeta Média (US$)"],
        )
        .properties(title="Gorjeta Média: Fumantes vs Não Fumantes")
    )
    texto9 = bar9.mark_text(dy=-10, fontSize=13).encode(
        text=alt.Text("Gorjeta Média (US$):Q", format=".2f")
    )
    st.altair_chart(bar9 + texto9, use_container_width=True)
with col_d:
    box9 = (
        alt.Chart(df)
        .mark_boxplot(extent="min-max")
        .encode(
            x=alt.X("smoker", title="Fumante"),
            y=alt.Y("tip", title="Gorjeta (US$)"),
            color=alt.Color("smoker", legend=None),
        )
        .properties(title="Distribuição das Gorjetas por Grupo")
    )
    st.altair_chart(box9, use_container_width=True)
st.info("Fumantes têm gorjeta média levemente maior, mas também mais variabilidade. Não fumantes são mais consistentes. A diferença não é estatisticamente expressiva pelo boxplot.")

st.markdown("---")

# ─── Questão 10 ──────────────────────────────────────────────────────────────
st.header("10. O turno da refeição (time) influencia no valor da conta ou da gorjeta?")
media_turno = df.groupby("time")[["total_bill", "tip"]].mean().reset_index()
media_turno.columns = ["Turno", "Conta Média (US$)", "Gorjeta Média (US$)"]
col_e, col_f = st.columns(2)
with col_e:
    bar10a = (
        alt.Chart(media_turno)
        .mark_bar(color="#54A24B")
        .encode(
            x="Turno",
            y="Conta Média (US$)",
            tooltip=["Turno", "Conta Média (US$)"],
        )
        .properties(title="Conta Média por Turno")
    )
    st.altair_chart(bar10a, use_container_width=True)
with col_f:
    bar10b = (
        alt.Chart(media_turno)
        .mark_bar(color="#B279A2")
        .encode(
            x="Turno",
            y="Gorjeta Média (US$)",
            tooltip=["Turno", "Gorjeta Média (US$)"],
        )
        .properties(title="Gorjeta Média por Turno")
    )
    st.altair_chart(bar10b, use_container_width=True)
st.info("O jantar (Dinner) apresenta tanto conta média quanto gorjeta média maiores do que o almoço (Lunch), indicando que clientes do jantar gastam e gorjeiam mais.")

st.markdown("---")

# ─── Questão 11 ──────────────────────────────────────────────────────────────
st.header("11. Qual grupo deixa a maior gorjeta proporcional à conta?")
df["pct_gorjeta"] = (df["tip"] / df["total_bill"]) * 100
colunas_grupo = ["sex", "smoker", "day", "time"]
grupo_sel = st.selectbox("Analisar por:", colunas_grupo, index=0)
media_pct = df.groupby(grupo_sel)["pct_gorjeta"].mean().reset_index()
media_pct.columns = [grupo_sel, "Gorjeta Proporcional (%)"]
bar11 = (
    alt.Chart(media_pct)
    .mark_bar()
    .encode(
        x=alt.X(grupo_sel),
        y=alt.Y("Gorjeta Proporcional (%)", title="% da Gorjeta em rel. à Conta"),
        color=alt.Color(grupo_sel, legend=None),
        tooltip=[grupo_sel, "Gorjeta Proporcional (%)"],
    )
    .properties(title=f"Gorjeta Proporcional (%) por {grupo_sel}")
)
texto11 = bar11.mark_text(dy=-10, fontSize=13).encode(
    text=alt.Text("Gorjeta Proporcional (%):Q", format=".1f")
)
st.altair_chart(bar11 + texto11, use_container_width=True)
st.info("Gorjeta média gira em torno de 15-20% da conta. Pode variar por grupo — selecione acima para explorar.")

st.markdown("---")

# ─── Questão 12 ──────────────────────────────────────────────────────────────
st.header("12. Existem valores atípicos (outliers) no valor da conta ou da gorjeta?")
col_g, col_h = st.columns(2)
with col_g:
    box12a = (
        alt.Chart(df)
        .mark_boxplot(extent=1.5, color="#4C78A8")
        .encode(
            y=alt.Y("total_bill", title="Valor Total da Conta (US$)"),
        )
        .properties(title="Boxplot: total_bill")
    )
    st.altair_chart(box12a, use_container_width=True)
with col_h:
    box12b = (
        alt.Chart(df)
        .mark_boxplot(extent=1.5, color="#F58518")
        .encode(
            y=alt.Y("tip", title="Gorjeta (US$)"),
        )
        .properties(title="Boxplot: tip")
    )
    st.altair_chart(box12b, use_container_width=True)

q1_bill, q3_bill = df["total_bill"].quantile([0.25, 0.75])
iqr_bill = q3_bill - q1_bill
outliers_bill = df[df["total_bill"] > q3_bill + 1.5 * iqr_bill]
q1_tip, q3_tip = df["tip"].quantile([0.25, 0.75])
iqr_tip = q3_tip - q1_tip
outliers_tip = df[df["tip"] > q3_tip + 1.5 * iqr_tip]
st.write(f"**Outliers em total_bill:** {len(outliers_bill)} registros  |  **Outliers em tip:** {len(outliers_tip)} registros")
st.info("Os outliers representam contas ou gorjetas excepcionalmente altas. Eles podem inflar a média e distorcer análises se não forem tratados com cuidado.")

st.markdown("---")

# ─── Questão 13 ──────────────────────────────────────────────────────────────
st.header("13. As distribuições de total_bill e tip são equilibradas ou concentradas?")
col_i, col_j = st.columns(2)
with col_i:
    hist13a = (
        alt.Chart(df)
        .mark_bar(opacity=0.8, color="#4C78A8")
        .encode(
            x=alt.X("total_bill:Q", bin=alt.Bin(maxbins=20), title="Valor Total da Conta (US$)"),
            y=alt.Y("count()", title="Frequência"),
        )
        .properties(title="Distribuição: total_bill")
    )
    st.altair_chart(hist13a, use_container_width=True)
with col_j:
    hist13b = (
        alt.Chart(df)
        .mark_bar(opacity=0.8, color="#F58518")
        .encode(
            x=alt.X("tip:Q", bin=alt.Bin(maxbins=20), title="Gorjeta (US$)"),
            y=alt.Y("count()", title="Frequência"),
        )
        .properties(title="Distribuição: tip")
    )
    st.altair_chart(hist13b, use_container_width=True)
st.info(
    "Ambas as distribuições são **assimétricas à direita (positivas)**: "
    "a maioria das contas se concentra entre US$ 10–20 e das gorjetas entre US$ 1–4. "
    "Valores muito altos são raros, formando uma cauda longa à direita."
)

st.markdown("---")

# ─── Questão 14 ──────────────────────────────────────────────────────────────
st.header("14. Insights para o gerente do restaurante")
st.subheader("Principais conclusões baseadas nos dados:")

col_k, col_l, col_m = st.columns(3)
with col_k:
    st.metric("Dia mais lucrativo", "Sábado", help="Maior soma de total_bill")
    st.write(
        "**Insight 1:** Sábado e domingo são os dias com maior volume e faturamento. "
        "Investir em mais pessoal e promoções nesses dias pode maximizar a receita."
    )
with col_l:
    st.metric("Turno mais rentável", "Jantar (Dinner)", help="Maior conta e gorjeta médias")
    st.write(
        "**Insight 2:** O jantar gera contas e gorjetas maiores. "
        "Estratégias de upselling (vinhos, sobremesas) no jantar têm maior potencial de retorno."
    )
with col_m:
    st.metric("Correlação conta×gorjeta", f"{correlacao:.2f}", help="Pearson r")
    st.write(
        "**Insight 3:** Contas maiores geram gorjetas maiores. "
        "Incentivar pedidos de alto valor (combos, menus especiais) beneficia tanto o faturamento quanto a satisfação dos garçons."
    )

st.success(
    "**Resumo:** O restaurante tem seu pico de movimento no fim de semana, especialmente aos sábados no jantar. "
    "Clientes em grupos maiores gastam mais, mas o gasto por pessoa é similar. "
    "Não há diferença significativa entre fumantes/não fumantes ou homens/mulheres — o foco deve ser no dia e turno estratégico."
)