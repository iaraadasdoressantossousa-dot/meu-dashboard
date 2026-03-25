import streamlit as st
import pandas as pd

# 1. Configuração da página (DEVE ser o primeiro comando Streamlit)
st.set_page_config(page_title="EA Makers - Analytics", layout="wide")

# 2. Função para carregar o CSS
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Arquivo {file_name} não encontrado.")

# Aplica o CSS
local_css("Stylepy.css")

st.title("EA Makers")
st.subheader("Dashboard automatizado que transforma dados em resultados.")

# 3. Upload do arquivo
uploaded_file = st.file_uploader("Escolha seu arquivo Excel ou CSV", type=["csv", "xlsx"])

if uploaded_file is not None:
    # 4. Ler o arquivo
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # 5. Cálculos (Agora que o 'df' existe)
    # Verificamos se as colunas necessárias existem no arquivo enviado
    colunas_necessarias = ['Valor total do projeto', 'Investimento (R$)']
    
    if all(col in df.columns for col in colunas_necessarias):
        # Cálculo do ROI
        df['ROI'] = (df['Valor total do projeto'] - df['Investimento (R$)']) / df['Investimento (R$)'] * 100
        
        # Exibindo um resumo do ROI médio
        roi_medio = df['ROI'].mean()
        st.metric(label="ROI do Projeto", value=f"{roi_medio:.2f}%")

        df['Payback'] = (df['Investimento (R$)']/(df['Lucro']))
        Payback= df['Payback'].mean()
        st.metric(label='Payback do projeto', value=f"{Payback:.2f} anos")
        # 6. Mostrar os dados calculados
        st.write("### Visualização dos Dados com ROI")
        st.dataframe(df)
    else:
        st.error(f"O arquivo precisa conter as colunas: {', '.join(colunas_necessarias)}")

else:
    st.info("Aguardando upload de arquivo para iniciar os cálculos.")
