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
    # Tenta carregar a logo, se não existir, usa apenas o texto
    try:
        st.image("yp.jpg", use_column_width=True)
    except:
        st.title("EA MAKERS")
    
    st.markdown("### Navegação")
    pagina = st.radio('', ["📊 Dashboard", "📅 Visualizar base de dados"])
    
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

    # Colunas necessárias para os cálculos da EA Makers
    colunas_req = ['ano', 'Valor total do projeto', 'Investimento (R$)', 'Lucro', 'Salário médio', 'Horas economizadas', 'total de funcionarios']
    
    if all(col in df.columns for col in colunas_req):
        # Cálculos de Engenharia Financeira
        df['ROI'] = (df['Valor total do projeto'] - df['Investimento (R$)']) / df['Investimento (R$)'] * 100
        df['Payback'] = df['Investimento (R$)'] / df['Lucro']
        df['Savings'] = (df['Salário médio'] / 160) * (df['Horas economizadas'] * df['total de funcionarios'])

        # Filtro de Anos Dinâmico na Sidebar
        with st.sidebar:
            st.divider()
            anos_disponiveis = sorted(df['ano'].unique())
            anos_selecionados = st.multiselect("Filtrar Anos", options=anos_disponiveis, default=anos_disponiveis)
        
        df_filtrado = df[df['ano'].isin(anos_selecionados)]

        # --- PÁGINA: DASHBOARD ---
        if pagina == "📊 Dashboard":
          with st.container(border=True):
            st.markdown("<h1 style='text-align: center;'>Dashboard</h1>", unsafe_allow_html=True)
            
            # Métricas por Ano em Colunas Dinâmicas
            if anos_selecionados:
                cols = st.columns(len(anos_selecionados))
                for ano, col in zip(anos_selecionados, cols):
                    dados_ano = df_filtrado[df_filtrado['ano'] == ano]
                    with col:
                        st.markdown(f"#### {ano}")
                        if not dados_ano.empty:
                            r = dados_ano.iloc[0]
                            with st.container(border=True): # Borda Dourada aplicada via CSS
                                st.metric("ROI", f"{r['ROI']:.1f}%")
                                st.metric("Payback", f"{r['Payback']:.2f} anos")
                                st.metric("Savings", f"R${r['Savings']:,.0f}")
                                
                                if r['ROI'] > 50:
                                    st.success("☑ Viável")
                                else:
                                    st.error("☒ Inviável")
            
            st.divider()

            # Gráficos Lado a Lado
            col_g1, col_g2 = st.columns(2)

            with col_g1:
                with st.container(border=True):
                    st.markdown("#### 📈 Evolução do ROI (%)")
                    st.line_chart(df_filtrado, x="ano", y="ROI", height=280)

            with col_g2:
                with st.container(border=True):
                    st.markdown("#### 📊 Investimento vs Lucro")
                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=df_filtrado['ano'], y=df_filtrado['Investimento (R$)'], name='Investimento', marker_color='#a9871f'))
                    fig.add_trace(go.Bar(x=df_filtrado['ano'], y=df_filtrado['Lucro'], name='Lucro', marker_color='#0097A7'))
                    fig.update_layout(barmode='group', height=280, margin=dict(l=0, r=0, t=10, b=0), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                    st.plotly_chart(fig, use_container_width=True)

        # --- PÁGINA: TABELA DE DADOS ---
        elif pagina == "📅 Visualizar base de dados":
            st.title("Base de Dados do usuário")
            with st.container(border=True):
                st.dataframe(df_filtrado, use_container_width=True, height=400)
                
                st.markdown("### Exportar Resultados")
                btn_csv, btn_xlsx = st.columns(2)
                
                with btn_csv:
                    csv = df_filtrado.to_csv(index=False).encode('utf-8')
                    st.download_button("Baixar CSV", data=csv, file_name="ea_makers_dados.csv", mime="text/csv", use_container_width=True)
                
                with btn_xlsx:
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        df_filtrado.to_excel(writer, index=False)
                    st.download_button("Baixar Excel (XLSX)", data=buffer.getvalue(), file_name="ea_makers_dados.xlsx", mime="application/vnd.ms-excel", use_container_width=True)

    else:
        st.error(f"Erro: O ficheiro deve conter as colunas: {', '.join(colunas_req)}")
else:
    st.title("Dashboard dinâmico - EA Makers")
    st.info(" Bem-vindo! Por favor, faça o upload da base de dados no menu lateral para começar.")
