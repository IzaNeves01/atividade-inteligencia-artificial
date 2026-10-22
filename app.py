import streamlit as st

from motor_inferencia import diagnosticar

st.set_page_config(page_title="Consultor Inteligente de Carreiras em TI", page_icon="💻", layout="centered")

st.title("Consultor Inteligente de Carreiras em TI")
st.write(
    "Responda às quatro perguntas abaixo. O sistema especialista aplica suas regras "
    "ao seu perfil e indica a trilha de TI mais adequada, explicando o motivo."
)
st.divider()

ATUACAO = {
    "Escrever lógica de servidores, APIs e bancos de dados": "backend",
    "Criar layouts visuais, interfaces responsivas e UI/UX": "frontend",
    "Analisar dados brutos, criar estatísticas e modelos preditivos": "analise_dados",
    "Construir pipelines de dados (ETL/ELT) e Data Lakes": "pipeline_dados",
    "Analisar vulnerabilidades, redes e defesa cibernética": "seguranca",
    "Automatizar processos de CI/CD e contêineres": "automacao",
    "Gerenciar e migrar infraestruturas escaláveis em nuvem": "nuvem",
    "Desenvolver aplicativos móveis (iOS/Android/Flutter)": "mobile",
    "Garantir a confiabilidade com testes automatizados": "qualidade",
    "Conectar regras de negócio, design e metodologias ágeis": "negocios",
}

ENTREGA = {
    "O produto final, direto na tela do usuário": "produto",
    "As regras de negócio e serviços que fazem o sistema funcionar": "regras_negocio",
    "A infraestrutura e a plataforma que sustentam o sistema": "infraestrutura",
    "Dados organizados e confiáveis para outros times usarem": "dados_confiaveis",
    "Modelos preditivos, inteligência artificial e análises": "analise",
    "A proteção contra invasões e vazamentos": "seguranca",
    "A garantia de que o software funciona sem erros": "qualidade",
    "A estratégia, o planejamento e a priorização do produto": "estrategia",
}

FERRAMENTAS = ["Python", "JavaScript", "Java/Kotlin/Swift", "SQL/Bancos de dados",
               "Linux/Redes", "Nenhuma/Iniciante"]

with st.form("entrevista"):
    matematica = st.select_slider(
        "1. Qual a sua afinidade com Matemática e Estatística?",
        options=["Baixa", "Média", "Alta"], value="Média")
    atuacao = st.selectbox("2. Qual atividade diária você mais gostaria de exercer?", list(ATUACAO))
    ferramenta = st.selectbox("3. Com qual linguagem/ferramenta você tem mais afinidade hoje?", FERRAMENTAS)
    entrega = st.selectbox("4. Que tipo de entrega de valor mais te satisfaz?", list(ENTREGA))
    enviado = st.form_submit_button("Executar diagnóstico")

if enviado:
    r = diagnosticar(matematica, ATUACAO[atuacao], ferramenta, ENTREGA[entrega])
    st.divider()
    if not r.trilha:
        st.warning("Nenhuma regra foi ativada para essa combinação de respostas.")
    else:
        st.success(f"Trilha recomendada: **{r.trilha}** ({r.pontos} pontos)")
        st.subheader("Por que essa trilha?")
        for regra, motivo, pontos in r.justificativas:
            st.markdown(f"- **{regra}** (+{pontos}): {motivo}")
        with st.expander("Pontuação de todas as trilhas"):
            st.table({"Trilha": [n for n, _ in r.ranking], "Pontos": [p for _, p in r.ranking]})