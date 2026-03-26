import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Configuração da página para tela cheia
st.set_page_config(page_title="Dashboard - EA Makers", layout="wide")

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass 

local_css("Stylepy.css")

# --- SIDEBAR (MENU LATERAL) ---
with st.sidebar:
    st.image("yp.jpg")
    st.title("EA Makers")
    
    # Navegação entre páginas
    pagina = st.radio("Navegação", ["Dashboard", "Visualizar dados"])
    
    st.divider()
    uploaded_file = st.file_uploader("Upload de Dados", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Ler o arquivo
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

    # Verificação de colunas
    colunas_obrigatorias = ['ano', 'Valor total do projeto', 'Investimento (R$)', 'Lucro', 'Salário médio', 'Horas economizadas', 'total de funcionarios']
    
    if all(col in df.columns for col in colunas_obrigatorias):
        # --- CÁLCULOS GLOBAIS ---
        df['ROI'] = (df['Valor total do projeto'] - df['Investimento (R$)']) / df['Investimento (R$)'] * 100
        df['Payback'] = df['Investimento (R$)'] / df['Lucro']
        df['Savings'] = (df['Salário médio'] / 160) * (df['Horas economizadas'] * df['total de funcionarios'])

        # Filtro de Anos dinâmico na Sidebar
        with st.sidebar:
            anos_disponiveis = sorted(df['ano'].unique())
            anos_selecionados = st.multiselect("Filtrar Anos", options=anos_disponiveis, default=anos_disponiveis)
        
        df_filtrado = df[df['ano'].isin(anos_selecionados)]

        # --- PÁGINA 1: DASHBOARD ---
        if pagina == "Dashboard":
            with st.container(border=True):
                st.title("EA Makers - Analytics")
                st.subheader("Insights que redefinem sua empresa.")

            # --- MÉTRICAS POR ANO (DINÂMICAS) ---
            if anos_selecionados:
                cols = st.columns(len(anos_selecionados))
                for ano, col in zip(anos_selecionados, cols):
                    dados_ano = df_filtrado[df_filtrado['ano'] == ano]
                    with col:
                        st.markdown(f"#### Ano {ano}")
                        if not dados_ano.empty:
                            r = dados_ano.iloc[0]
                            with st.container(border=True): # Borda Dourada via CSS
                                st.metric("ROI", f"{r['ROI']:.1f}%")
                                st.metric("Payback", f"{r['Payback']:.2f} anos")
                                st.metric("Savings", f"R$ {r['Savings']:,.2f}")
                                
                                if r['ROI'] > 50:
                                    st.success("✅ Viável")
                                else:
                                    st.error("⚠️ Inviável")

            # --- GRÁFICOS LADO A LADO ---
            col_g1, col_g2 = st.columns(2)
            
            with col_g1.container(border=True):
                st.markdown("#### 📈 ROI por Ano")
                st.line_chart(data=df_filtrado, x="ano", y="ROI", height=300)

            with col_g2.container(border=True):
                st.markdown("#### 📊 Investimento vs Lucro")
                fig = go.Figure()
                fig.add_trace(go.Bar(x=df_filtrado['ano'], y=df_filtrado['Investimento (R$)'], name='Investimento', marker_color='#FFEB3B'))
                fig.add_trace(go.Bar(x=df_filtrado['ano'], y=df_filtrado['Lucro'], name='Lucro', marker_color='#0097A7'))
                fig.update_layout(barmode='group', template="plotly_white", height=300, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig, use_container_width=True)

        # --- PÁGINA 2: TABELA DE DADOS ---
        elif pagina == "Tabela de Dados":
            st.title("Base de Dados")
            with st.container(border=True):
                st.write("### Dados Brutos (Filtrados)")
                st.dataframe(df_filtrado, use_container_width=True, height=500)
                
                # Botão de Download
                csv = df_filtrado.to_csv(index=False).encode('utf-8')
                st.download_button("Exportar para CSV", data=csv, file_name="dados_makers.csv", mime="text/csv")

    else:
        st.error(f"O arquivo precisa conter: {', '.join(colunas_obrigatorias)}")
else:
    st.info("Aguardando upload do arquivo no menu lateral.")
