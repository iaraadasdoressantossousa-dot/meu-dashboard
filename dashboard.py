import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------- CONFIGURAÇÃO ----------------
st.set_page_config(page_title="EA Makers - Analytics", layout="wide")

# ---------------- TEMA BRANCO (XBOX STYLE) ----------------
st.markdown("""
<style>
/* Fundo geral */
.stApp {
    background-color: #FFFFFF;
    color: #000000;
}

/* Textos */
h1, h2, h3, h4, h5, h6, p, span, label, div {
    color: #000000;
}

/* Containers */
[data-testid="stContainer"] {
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 10px;
    padding: 10px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
}

/* Botões */
button {
    background-color: #107C10;
    color: white;
    border-radius: 8px;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 10px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("EA Makers")
st.subheader("Bem-vindo ao dashboard que transforma dados em resultados que redefinem a sua empresa.")

# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader("Escolha seu arquivo Excel ou CSV", type=["csv", "xlsx"])

if uploaded_file is not None:

    # Ler arquivo
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

    # Colunas obrigatórias
    colunas_obrigatorias = [
        'ano',
        'Valor total do projeto',
        'Investimento (R$)',
        'Lucro',
        'Salário médio',
        'Horas economizadas',
        'total de funcionarios'
    ]

    if all(col in df.columns for col in colunas_obrigatorias):

        # ---------------- CÁLCULOS ----------------
        df['ROI'] = (df['Valor total do projeto'] - df['Investimento (R$)']) / df['Investimento (R$)'] * 100
        df['Payback'] = df['Investimento (R$)'] / df['Lucro']
        df['Savings'] = (df['Salário médio'] / 160) * (df['Horas economizadas'] * df['total de funcionarios'])

        st.write("### Tabela de Dados Calculada")
        st.dataframe(df, use_container_width=True)

        # ---------------- KPIs POR ANO ----------------
        st.write("### 📊 Performance por Ano")

        col1, col2, col3 = st.columns(3)
        mapa = {2023: col1, 2024: col2, 2025: col3}

        for ano in [2023, 2024, 2025]:
            dados_ano = df[df['ano'] == ano]

            if not dados_ano.empty:
                r = dados_ano.iloc[0]

                with mapa[ano]:
                    with st.container(border=True):
                        st.markdown(f"#### Ano {ano}")
                        st.metric("ROI", f"{r['ROI']:.1f}%")
                        st.metric("Payback", f"{r['Payback']:.2f} anos")
                        st.metric("Savings", f"R$ {r['Savings']:,.2f}")

                        if r['ROI'] > 50:
                            st.success("✅ Projeto Viável (ROI > 50%)")
                        else:
                            st.error("⚠️ Projeto Inviável (ROI < 50%)")
            else:
                mapa[ano].warning(f"Dados de {ano} não encontrados.")

        # ---------------- GRÁFICO ROI ----------------
        st.write("### 📈 Gráfico de ROI")

        df['ano'] = df['ano'].astype(int).astype(str)

        st.line_chart(
            data=df,
            x="ano",
            y="ROI",
            use_container_width=True
        )

        # ---------------- GRÁFICO INVESTIMENTO X LUCRO ----------------
        st.write("### 📊 Comparativo: Investimento vs Lucro")

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df['ano'],
            y=df['Investimento (R$)'],
            name='Investimento',
            marker_color='#E53935'
        ))

        fig.add_trace(go.Bar(
            x=df['ano'],
            y=df['Lucro'],
            name='Lucro',
            marker_color='#2E7D32'
        ))

        fig.update_layout(
            barmode='group',
            xaxis_title="Ano de Operação",
            yaxis_title="Valor (R$)",
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(color='black'),
            legend_title="Indicadores",
            template="plotly_white",
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error(f"O arquivo precisa conter: {', '.join(colunas_obrigatorias)}")

else:
    st.info("Aguardando upload do arquivo para processar os dados.")
