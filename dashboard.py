import streamlit as st
import pandas as pd
import plotly.graph_objects as go
# 1. Configuração da página
st.set_page_config(page_title="EA Makers - Analytics", layout="wide")

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass 

local_css("Stylepy.css")

st.title("EA Makers")
st.subheader("Bem-vindo ao dashboard que transforma dados em resultados que redefinem a sua empresa.")

uploaded_file = st.file_uploader("Escolha seu arquivo Excel ou CSV", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Ler o arquivo
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

    # Verificação de colunas
    colunas_obrigatorias = ['ano', 'Valor total do projeto', 'Investimento (R$)', 'Lucro', 'Salário médio', 'Horas economizadas', 'total de funcionarios']
    
    if all(col in df.columns for col in colunas_obrigatorias):
        # --- CÁLCULOS GERAIS ---
        df['ROI'] = (df['Valor total do projeto'] - df['Investimento (R$)']) / df['Investimento (R$)'] * 100
        df['Payback'] = df['Investimento (R$)'] / df['Lucro']
        df['Savings'] = (df['Salário médio'] / 160) * (df['Horas economizadas'] * df['total de funcionarios'])
        
        st.write("### Tabela de Dados Calculada")
        st.dataframe(df)

        # --- EXIBIÇÃO POR ANO ---
        st.write("### 📊 Performance por Ano")
        
        col23, col24, col25 = st.columns(3)
        mapa_colunas = {2023: col23, 2024: col24, 2025: col25}

        for ano in [2023, 2024, 2025]:
            dados_ano = df[df['ano'] == ano]
            
            if not dados_ano.empty:
                r = dados_ano.iloc[0]
                with mapa_colunas[ano]:
                    st.markdown(f"#### Ano {ano}")
                    st.metric("ROI", f"{r['ROI']:.1f}%")
                    st.metric("Payback", f"{r['Payback']:.2f} anos")
                    st.metric("Savings", f"R$ {r['Savings']:,.2f}")
                    
                    if r['ROI'] > 50:
                        st.success("✅ Projeto Viável")
                    else:
                        st.error("⚠️ Inviável")
            else:
                mapa_colunas[ano].warning(f"Dados de {ano} não encontrados.")

        # --- GRÁFICO (Agora dentro do IF de colunas) ---
        st.write("### 📈 Gráfico de ROI ")
        df['ano'] = df['ano'].astype(int).astype(str)
        st.line_chart(
        data=df, 
        x="ano", 
        y="ROI", 
        x_label="Ano de Operação", 
        y_label="Retorno sobre Investimento (%)", 
        color="#2E7D32", 
        use_container_width=True
        )
        st.write("### 📊 Comparativo: Investimento vs Lucro")

        # Criando o gráfico com Plotly
        fig = go.Figure()

        # Barra de Investimento
        fig.add_trace(go.Bar(
          x=df['ano'],
          y=df['Investimento (R$)'],
          name='Investimento',
          marker_color='#E53935' # Vermelho para saída/custo
        ))

        # Barra de Lucro
        fig.add_trace(go.Bar(
         x=df['ano'],
         y=df['Lucro'],
         name='Lucro',
         marker_color='#2E7D32' # Verde para entrada/retorno
        ))

        # Ajustando o layout para barras duplas (lado a lado)
        fig.update_layout(
          barmode='group', 
          xaxis_title="Ano de Operação",
          yaxis_title="Valor (R$)",
          legend_title="Indicadores",
          template="plotly_white",
          margin=dict(l=20, r=20, t=20, b=20)
        )

        # Exibindo no Streamlit
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Este else avisa se as colunas obrigatórias não foram encontradas
        st.error(f"O arquivo precisa conter: {', '.join(colunas_obrigatorias)}")

else:
    st.info("Aguardando upload do arquivo para processar os 3 anos.")
