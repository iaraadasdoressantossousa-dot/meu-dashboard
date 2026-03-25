import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Configuração da página com sua paleta de cores
st.set_page_config(page_title="EA Makers - Analytics", layout="wide")

st.title("Upload de Dados para Consultoria")

# 2. Receber o arquivo (Excel ou CSV)
uploaded_file = st.file_uploader("Escolha seu arquivo Excel ou CSV", type=["csv", "xlsx"])

if uploaded_file is not None:
    # 3. Ler o arquivo dependendo da extensão
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # 4. Mostrar os dados
    st.write("### Visualização dos Dados Brutos", df.head())

    # 5. Realizar seus cálculos (Exemplo: Média de Investimentos)
    # st.write(df.describe())  # Exemplo rápido de estatística

    # 6. Gerar Gráficos
    st.subheader("Análise Visual EA Makers")
    st.line_chart(df) # Gráfico rápido do Streamlit