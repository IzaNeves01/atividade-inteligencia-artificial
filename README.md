# Consultor Inteligente de Carreiras em TI

Trabalho da disciplina de Inteligência Artificial, Ciência da Computação, UNIPAC Barbacena.
Aluna: Izadora Aparecida do Carmo Ferreira Neves
Professor: Felipe Roncalli de Paula Carneiro

Sistema especialista em Python que faz quatro perguntas ao usuário e recomenda uma entre 10 trilhas de carreira em TI, mostrando as regras que levaram à resposta.

## Como funciona

O motor usa a biblioteca Experta (encadeamento para frente) com 32 regras:

1. As respostas viram um fato `PerfilUsuario`.
2. As regras R01 a R30 geram fatos `Indicio`, cada um somando pontos a uma trilha.
3. A regra R31 dispara por último, soma os pontos e declara a trilha vencedora.
4. A regra R32 monta a justificativa só com os motivos da trilha vencedora.

Como as regras somam pontos em vez de substituir a resposta anterior, duas regras não se sobrepõem e toda combinação de respostas gera uma recomendação. A tabela completa está em [MATRIZ_DECISAO.md](MATRIZ_DECISAO.md).

## Arquivos

- `app.py`: interface em Streamlit
- `motor_inferencia.py`: fatos e regras
- `testes_personas.py`: testes com 12 personas
- `MATRIZ_DECISAO.md`: tabela de decisão
- `requirements.txt`: dependências

## Instalação e execução

```bash
git clone <url-do-repositorio>
cd <pasta-do-repositorio>
python -m venv .venv
source .venv/bin/activate      # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Testes

```bash
python testes_personas.py
```

O script confere 12 personas (as quatro do enunciado, uma para cada trilha restante e dois casos de fronteira entre Ciência e Engenharia de Dados) e testa todas as combinações possíveis de respostas, garantindo que nenhuma fique sem resultado.

| Persona | Perfil | Trilha obtida |
|---|---|---|
| Ana | matemática alta, analisa dados, Python, quer entregar modelos | Ciência de Dados |
| Bruno | Linux/Redes, defesa cibernética, quer entregar segurança | Cibersegurança |
| Carla | matemática baixa, layouts, JavaScript, quer entregar o produto | Front-end & UI/UX |
| Diego | negócios, sem programação, quer entregar estratégia | Product Management |
| Karen | quer analisar dados, mas matemática baixa | Engenharia de Dados |
| Lucas | matemática alta, mas prefere construir pipelines | Engenharia de Dados |

As outras seis personas (back-end, DevOps, Cloud, Mobile, QA e Engenharia de Dados) estão em `testes_personas.py`.

## Observação sobre versões do Python

O `experta` usa `collections.Mapping`, que foi removido no Python 3.10, então a importação falha nessas versões. Para o projeto rodar no Python 3.10 ou superior, o início de `motor_inferencia.py` recoloca esses nomes em `collections` antes de importar a biblioteca. Testei com Python 3.12.