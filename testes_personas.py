"""
Validação do motor com personas de teste.
Executar:  python testes_personas.py   (ou: pytest testes_personas.py)
"""
from itertools import product

from motor_inferencia import ATUACAO_TRILHA, TRILHAS, diagnosticar

# (nome, matematica, atuacao, ferramenta, entrega, trilha esperada)
PERSONAS = [
    # As quatro personas pedidas no enunciado
    ("Ana - perfil analítico", "Alta", "analise_dados", "Python", "analise", "ciencia"),
    ("Bruno - perfil infra/segurança", "Média", "seguranca", "Linux/Redes", "seguranca", "seguranca"),
    ("Carla - perfil visual/front-end", "Baixa", "frontend", "JavaScript", "produto", "frontend"),
    ("Diego - perfil negócios/produto", "Média", "negocios", "Nenhuma/Iniciante", "estrategia", "pm"),
    # Demais trilhas
    ("Elisa - dados, mas pipelines", "Média", "pipeline_dados", "SQL/Bancos de dados", "dados_confiaveis", "engdados"),
    ("Fábio - servidores e APIs", "Média", "backend", "Java/Kotlin/Swift", "regras_negocio", "backend"),
    ("Gabi - automação", "Média", "automacao", "Linux/Redes", "infraestrutura", "devops"),
    ("Hugo - arquitetura em nuvem", "Média", "nuvem", "Linux/Redes", "infraestrutura", "cloud"),
    ("Iara - aplicativos", "Baixa", "mobile", "Java/Kotlin/Swift", "produto", "mobile"),
    ("João - testes", "Média", "qualidade", "Python", "qualidade", "qa"),
    # Casos de fronteira (Cientista x Engenheiro de Dados)
    ("Karen - quer analisar, mas sem estatística", "Baixa", "analise_dados", "SQL/Bancos de dados", "dados_confiaveis", "engdados"),
    ("Lucas - matemática alta, mas gosta de pipelines", "Alta", "pipeline_dados", "Python", "dados_confiaveis", "engdados"),
]


def test_personas():
    erros = []
    for nome, mat, atu, fer, ent, esperado in PERSONAS:
        r = diagnosticar(mat, atu, fer, ent)
        if r.trilha != TRILHAS[esperado]:
            erros.append(f"{nome}: esperado {TRILHAS[esperado]}, obtido {r.trilha}")
    assert not erros, "\n".join(erros)


def test_todas_as_combinacoes_geram_uma_trilha():
    """Nenhuma combinação de respostas pode ficar sem resultado."""
    matematica = ["Baixa", "Média", "Alta"]
    ferramentas = ["Python", "JavaScript", "Linux/Redes", "Java/Kotlin/Swift",
                   "SQL/Bancos de dados", "Nenhuma/Iniciante"]
    entregas = ["produto", "regras_negocio", "infraestrutura", "dados_confiaveis",
                "analise", "seguranca", "qualidade", "estrategia"]
    for mat, atu, fer, ent in product(matematica, ATUACAO_TRILHA, ferramentas, entregas):
        r = diagnosticar(mat, atu, fer, ent)
        assert r.trilha in TRILHAS.values(), (mat, atu, fer, ent)
        assert r.justificativas, (mat, atu, fer, ent)


def test_toda_trilha_pode_ser_recomendada():
    """Cada uma das 10 trilhas precisa ser alcançável por alguma persona."""
    obtidas = {diagnosticar(m, a, f, e).trilha for _, m, a, f, e, _ in PERSONAS}
    assert obtidas == set(TRILHAS.values())


if __name__ == "__main__":
    print(f"{'Persona':50} {'Esperado':42} {'Obtido':42} OK")
    acertos = 0
    for nome, mat, atu, fer, ent, esperado in PERSONAS:
        r = diagnosticar(mat, atu, fer, ent)
        ok = r.trilha == TRILHAS[esperado]
        acertos += ok
        print(f"{nome:50} {TRILHAS[esperado]:42} {r.trilha:42} {'sim' if ok else 'NÃO'}")
    print(f"\n{acertos}/{len(PERSONAS)} personas corretas")
    test_todas_as_combinacoes_geram_uma_trilha()
    test_toda_trilha_pode_ser_recomendada()
    print("Varredura de todas as combinações: ok")