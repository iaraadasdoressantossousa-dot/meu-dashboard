import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------- CONFIG ----------------
st.set_page_config(page_title="EA Makers", layout="wide")

# ---------------- CSS MODERNO ----------------
st.markdown("""
<style>

/* Fundo geral */
.stApp {
    background-color: #F5F6FA;
}

/* Títulos */
h1 {
    color: #111;
    font-size: 42px;
    font-weight: 700;
}

h2, h3 {
    color: #222;
}

/* Subtexto */
p {
    color: #555;
}

/* Cards modernos */
.card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    margin-bottom: 15px;
}

/* KPI */
.kpi {
    font-size: 28px;
    font-weight: bold;
    color: #111;
}

.kpi-label {
    font-size: 14px;
    color: #777;
}

/* Upload box */
[data-testid="stFileUploader"] {
    background-color: white;
    border-radius: 12px;
    border: 1px solid #E0E0E0;
    padding: 10px;
}

/* Botão */
button {
    background-color: #111;
    color: white;
    border-radius: 10px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("EA Makers Dashboard")
st.write("Analytics moderno para tomada de decisão")

# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader("📂 Envie seu arquivo", type=["csv", "xlsx"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

    colunas = [
        'ano',
        'Valor total do projeto',
        'Investimento (R$)',
        'Lucro',
        'Salário médio',
        'Horas economizadas',
        'total de funcionarios'
    ]

    if all(col in df.columns for col in colunas):

        # -------- CÁLCULOS --------
        df['ROI'] = (df['Valor total do projeto'] - df['Investimento (R$)']) / df['Investimento (R$)'] * 100
        df['Payback'] = df['Investimento (R$)'] / df['Lucro']
        df['Savings'] = (df['Salário médio'] / 160) * (df['Horas economizadas'] * df['total de funcionarios'])

        # -------- KPIs --------
        st.subheader("📊 Visão Geral")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="kpi">{df['ROI'].mean():.1f}%</div>
                <div class="kpi-label">ROI Médio</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="card">
                <div class="kpi">{df['Payback'].mean():.2f}</div>
                <div class="kpi-label">Payback Médio</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="card">
                <div class="kpi">R$ {df['Savings'].sum():,.0f}</div>
                <div class="kpi-label">Savings Total</div>
            </div>
            """, unsafe_allow_html=True)

        # -------- GRÁFICOS --------
        st.subheader("📈 Análise")

        col4, col5 = st.columns(2)

        # ROI linha
        with col4:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['ano'],
                y=df['ROI'],
                mode='lines+markers'
            ))

            fig.update_layout(
                title="ROI ao longo dos anos",
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(color='black'),
                margin=dict(l=10, r=10, t=40, b=10)
            )

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Investimento vs Lucro
        with col5:
            fig2 = go.Figure()

            fig2.add_trace(go.Bar(
                x=df['ano'],
                y=df['Investimento (R$)'],
                name='Investimento'
            ))

            fig2.add_trace(go.Bar(
                x=df['ano'],
                y=df['Lucro'],
                name='Lucro'
            ))

            fig2.update_layout(
                barmode='group',
                title="Investimento vs Lucro",
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(color='black')
            )

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # -------- TABELA --------
        st.subheader("📋 Dados")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.error("Arquivo com colunas incorretas")

else:
    st.info("Envie um arquivo para começar")
