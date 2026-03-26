import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io

# 1. Configuração da página para ocupar a tela toda
st.set_page_config(page_title="EA Makers - Dashboard", layout="wide")

# 2. Função para carregar o CSS personalizado
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass 

local_css("Stylepy.css")

# --- SIDEBAR (MENU LATERAL) ---
with st.sidebar:
    try:
        st.image("yp.jpg", use_container_width=True)
    except:
        st.title("EA MAKERS")
    
    st.markdown("### Menu")
    pagina = st.radio('Navegação', ["Dashboard", "Visualizar base de dados"])
    
    st.divider()
    st.markdown("### Dados")
    uploaded_file = st.file_uploader("Upload de Dados (CSV ou XLSX)", type=["csv", "xlsx"])

# --- LÓGICA PRINCIPAL ---
if uploaded_file is not None:
    # Leitura dos dados
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Colunas necessárias
    colunas_req = ['ano', 'Valor total do projeto', 'Investimento (R$)', 'Lucro', 'Salário médio', 'Horas economizadas', 'total de funcionarios']
    
    if all(col in df.columns for col in colunas_req):
        # Cálculos
        df['ROI'] = (df['Valor total do projeto'] - df['Investimento (R$)']) / df['Investimento (R$)'] * 100
        df['Payback'] = df['Investimento (R$)'] / df['Lucro']
        df['Savings'] = (df['Salário médio'] / 160) * (df['Horas economizadas'] * df['total de funcionarios'])

        # Filtro de Anos
        with st.sidebar:
            st.divider()
            anos_disponiveis = sorted(df['ano'].unique())
            anos_selecionados = st.multiselect("Filtrar Anos", options=anos_disponiveis, default=anos_disponiveis)
        
        df_filtrado = df[df['ano'].isin(anos_selecionados)]

        # --- PÁGINA: DASHBOARD ---
        if pagina == "Dashboard":
            with st.container(border=True):
                st.markdown("<h2 style='text-align: center;'>Dashboard</h2>", unsafe_allow_html=True)
                st.markdown("<h1 style='text-align: center;'>Resultados de KPIs anuais</h1>", unsafe_allow_html=True)
                
                if anos_selecionados:
                    cols = st.columns(len(anos_selecionados))
                    for ano, col in zip(anos_selecionados, cols):
                        dados_ano = df_filtrado[df_filtrado['ano'] == ano]
                        with col:
                            st.markdown(f"#### {ano}")
                            if not dados_ano.empty:
                                r = dados_ano.iloc[0]
                                with st.container(border=True):
                                    st.metric("ROI", f"{r['ROI']:.1f}%")
                                    st.metric("Payback", f"{r['Payback']:.2f} anos")
                                    st.metric("Savings", f"R${r['Savings']:,.
