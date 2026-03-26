import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Configuração da página
st.set_page_config(page_title="EA Makers - Analytics", layout="wide")

# --- INJEÇÃO DE CSS ESTILO DARK PREMIUM ---
st.markdown("""
    <style>
    /* Fundo geral da aplicação */
    .stApp {
        background-color: #0d1117;
    }

    /* Estilização dos Containers (Cards) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 25px !important;
        margin-bottom: 15px !important;
    }

    /* Títulos e textos em tons de cinza claro/branco */
    h1, h2, h3, h4, p, span, label {
        color: #c9d1d9 !important;
    }

    /* Customização das Métricas (KPIs) individuais */
    [data-testid="stMetric"] {
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
        padding: 15px !important;
        border-radius: 10px !important;
    }

    /* Cor dos números das métricas (Azul suave) */
    [data-testid="stMetricValue"] {
        color: #58a6ff !important;
    }

    /* Ajuste na barra lateral (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("EA Makers")
st.subheader("Bem-vindo ao dashboard que transforma dados em resultados.")

# Usando o sidebar para o upload como na imagem de referência
with st.sidebar:
    st.header("Configurações")
    uploaded_file = st.file_uploader("Escolha seu arquivo", type=["csv", "xlsx"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    colunas_obrigatorias = ['ano', 'Valor total do projeto', 'Investimento (R$)', 'Lucro', 'Salário médio', 'Horas economizadas', 'total de funcionarios']
    
    if all(col in df.columns for col in colunas_obrigatorias):
        # --- CÁLCULOS ---
        df['ROI'] = (df['Valor total do projeto'] - df['Investimento (R$)']) / df['Investimento (R$)'] * 100
        df['Payback'] = df['Investimento (R$)'] / df['Lucro']
        df['Savings'] = (df['Salário médio'] / 160) * (df['Horas economizadas'] * df['total de funcionarios'])
        df['ano_str'] = df['ano'].astype(int).astype(str) # Para o eixo X do gráfico

        # --- SEÇÃO DE DADOS ---
        with st.container(border=True):
            st.write("### 📂 Repositório de Dados")
            st.dataframe(df, use_container_width=True)

        # --- SEÇÃO DE KPIS (POR ANO) ---
        st.write("### 📊 Performance por Ano")
        cols = st.columns(3)
        
        for i, ano in enumerate([2023, 2024, 2025]):
            dados_ano = df[df['ano'] == ano]
            if not dados_ano.empty:
                r = dados_ano.iloc[0]
                with cols[i]:
                    with st.container(border=True):
                        st.markdown(f"#### Ano {ano}")
                        st.metric("ROI", f"{r['ROI']:.1f}%")
                        st.metric("Payback", f"{r['Payback']:.2f} anos")
                        st.metric("Savings", f"R$ {r['Savings']:,.2f}")
                        
                        if r['ROI'] > 50:
                            st.success("✅ Projeto Viável")
                        else:
                            st.error("⚠️ Inviável")

        # --- SEÇÃO DE GRÁFICOS (LADO A LADO) ---
        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            with st.container(border=True):
                st.write("### 📈 Tendência de ROI")
                st.line_chart(data=df, x="ano_str", y="ROI", color="#58a6ff")

        with col_graf2:
            with st.container(border=True):
                st.write("### 📊 Investimento vs Lucro")
                fig = go.Figure()
                fig.add_trace(go.Bar(x=df['ano_str'], y=df['Investimento (R$)'], name='Investimento', marker_color='#f85149'))
                fig.add_trace(go.Bar(x=df['ano_str'], y=df['Lucro'], name='Lucro', marker_color='#3fb950'))
                
                fig.update_layout(
                    barmode='group',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    template="plotly_dark",
                    margin=dict(l=10, r=10, t=10, b=10),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)
                
    else:
        st.error(f"O arquivo precisa conter: {', '.join(colunas_obrigatorias)}")
else:
    st.info("Aguardando upload no menu lateral.")
