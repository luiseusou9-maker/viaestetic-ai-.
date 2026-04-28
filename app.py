import streamlit as st
import pandas as pd
from groq import Groq
import os

# Configuração visual da página
st.set_page_config(page_title="Viaestetic AI Lab", page_icon="🩺", layout="wide")

# Estilização básica para ficar com a cara da marca (Azul/Branco)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { background-color: #004a99; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 1. SEGURANÇA: Carregando a API Key
api_key = os.getenv("GROQ_API_KEY")

# Cabeçalho
st.title("🩺 Viaestetic - Sistema de Inteligência Logística")
st.subheader("Protótipo de Gestão de Estoque e Validades (IA)")
st.write("---")

# 2. DATASET: Simulação de estoque
data = {
    'SKU': ['VIA-BOT-01', 'VIA-HIAL-05', 'VIA-PDO-22', 'VIA-CAN-99', 'VIA-LUVA-M'],
    'Produto': ['Toxina Botulínica Tipo A', 'Ácido Hialurônico 2ml', 'Fios de PDO Espiculados', 'Microcânulas 22G', 'Luva Nitrílica Rosa M'],
    'Categoria': ['Injetáveis', 'Preenchedores', 'Fios', 'Hospitalar', 'EPI'],
    'Estoque': [15, 42, 8, 150, 500],
    'Validade': ['2026-05-15', '2026-11-20', '2026-04-30', '2027-02-10', '2026-09-12'],
    'Preço_Compra': [480.00, 310.00, 145.00, 15.00, 0.55]
}
df = pd.DataFrame(data)
df['Validade'] = pd.to_datetime(df['Validade'])

# 3. INTERFACE: Visualização dos Dados
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📦 Inventário em Tempo Real")
    st.dataframe(df, use_container_width=True)

with col2:
    st.markdown("### 📊 Alertas Críticos")
    vencendo = df[df['Validade'] <= (pd.Timestamp.now() + pd.Timedelta(days=30))]
    if not vencendo.empty:
        st.error(f"Atenção: {len(vencendo)} itens vencem em 30 dias!")
        st.write(vencendo[['Produto', 'Validade']])
    else:
        st.success("Nenhum produto vencendo nos próximos 30 dias.")

# 4. INTELIGÊNCIA ARTIFICIAL: Groq + Llama 3
st.write("---")
st.markdown("### 🤖 Assistente Logístico IA (Groq)")
pergunta = st.text_input("Faça uma pergunta estratégica sobre o estoque:", placeholder="Ex: 'Quais produtos de alto valor devo priorizar a venda pelo vencimento?'")

if pergunta:
    if not api_key:
        st.warning("⚠️ Configure a variável GROQ_API_KEY nos Secrets para usar a IA.")
    else:
        with st.spinner('A Groq está analisando os dados...'):
            try:
                client = Groq(api_key=api_key)
                contexto_csv = df.to_csv(index=False)
                
                prompt = f"""
                Você é o Especialista em Logística da Viaestetic em Campinas.
                Analise os seguintes dados de estoque e responda à pergunta do gestor.
                Regra: Foque em redução de prejuízo e normas da ANVISA.
                Dados: {contexto_csv}
                Pergunta: {pergunta}
                """

                # CORREÇÃO AQUI: Modelo atualizado e sintaxe corrigida
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                
                st.markdown("#### ✨ Insight da IA:")
                st.info(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Erro na API Groq: {e}")

# Sidebar com logo corrigido (usando uma imagem real)
st.sidebar.image("https://viaestetic.com.br", width=150)
st.sidebar.markdown("---")
st.sidebar.write("📍 **Local:** Campinas/SP")
st.sidebar.write("🚀 **Dev:** Estágio Tecnologia")
