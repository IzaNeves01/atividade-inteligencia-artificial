"""
  1. O perfil do usuário entra como um fato (PerfilUsuario).
  2. As regras R01..R30 comparam o perfil e declaram fatos Indicio, cada um
     somando (ou subtraindo) pontos de uma trilha e guardando o motivo.
  3. A regra R31 (decidir), de baixa prioridade, só dispara depois de todos os
     indícios existirem. Ela soma os pontos, escolhe a trilha vencedora e
     declara o fato Recomendacao.
  4. A regra R32 (justificar) dispara a partir do fato Recomendacao e monta a
     explicação usando apenas os indícios da trilha vencedora.
"""
import collections
import collections.abc
from dataclasses import dataclass, field

for _nome in ("Mapping", "MutableMapping", "Sequence", "Iterable", "Callable"):
    if not hasattr(collections, _nome):
        setattr(collections, _nome, getattr(collections.abc, _nome))

from experta import AS, MATCH, Fact, Field, KnowledgeEngine, L, Rule  # noqa: E402

TRILHAS = {
    "backend": "1. Desenvolvimento Back-end",
    "frontend": "2. Desenvolvimento Front-end & UI/UX",
    "ciencia": "3. Ciência de Dados e Machine Learning",
    "engdados": "4. Engenharia de Dados",
    "seguranca": "5. Cibersegurança (Security / Pentesting)",
    "devops": "6. DevOps & SRE",
    "cloud": "7. Computação em Nuvem (Cloud Architecture)",
    "mobile": "8. Desenvolvimento Mobile",
    "qa": "9. Engenharia de Qualidade e Testes (QA)",
    "pm": "10. Gestão de Produtos (Product Management)",
}

ATUACAO_TRILHA = {
    "backend": "backend",
    "frontend": "frontend",
    "analise_dados": "ciencia",
    "pipeline_dados": "engdados",
    "seguranca": "seguranca",
    "automacao": "devops",
    "nuvem": "cloud",
    "mobile": "mobile",
    "qualidade": "qa",
    "negocios": "pm",
}

PYTHON_OU_SQL = L("Python") | L("SQL/Bancos de dados")

class PerfilUsuario(Fact):
    """Respostas da entrevista."""
    matematica = Field(str, mandatory=True)   
    atuacao = Field(str, mandatory=True)      
    ferramenta = Field(str, mandatory=True)   
    entrega = Field(str, mandatory=True)      


class Indicio(Fact):
    trilha = Field(str, mandatory=True)
    pontos = Field(int, mandatory=True)
    regra = Field(str, mandatory=True)
    motivo = Field(str, mandatory=True)


class Recomendacao(Fact):
    trilha = Field(str, mandatory=True)
    pontos = Field(int, mandatory=True)


@dataclass
class Resultado:
    trilha: str = ""
    pontos: int = 0
    ranking: list = field(default_factory=list)        
    justificativas: list = field(default_factory=list)  

class ConsultorCarreira(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self._limpar()

    def _limpar(self):
        self.resultado = None

    def reset(self, **kwargs):
        self._limpar()
        return super().reset(**kwargs)

    def _indicio(self, trilha, pontos, regra, motivo):
        self.declare(Indicio(trilha=trilha, pontos=pontos, regra=regra, motivo=motivo))

    #Back-end
    @Rule(PerfilUsuario(atuacao="backend"))
    def r01_backend_atuacao(self):
        self._indicio("backend", 4, "R01", "Você prefere trabalhar com lógica de servidores, APIs e bancos de dados.")

    @Rule(PerfilUsuario(entrega="regras_negocio"))
    def r02_backend_entrega(self):
        self._indicio("backend", 3, "R02", "Você quer entregar as regras de negócio e os serviços que fazem o sistema funcionar.")

    @Rule(PerfilUsuario(atuacao="backend", ferramenta=L("Python") | L("Java/Kotlin/Swift") | L("SQL/Bancos de dados")))
    def r03_backend_ferramenta(self):
        self._indicio("backend", 2, "R03", "Sua ferramenta de maior afinidade (Python, Java ou SQL) é muito usada no desenvolvimento de servidores.")

    #Front-end
    @Rule(PerfilUsuario(atuacao="frontend"))
    def r04_frontend_atuacao(self):
        self._indicio("frontend", 4, "R04", "Você prefere criar layouts, interfaces responsivas e cuidar da experiência do usuário.")

    @Rule(PerfilUsuario(entrega="produto", ferramenta="JavaScript"))
    def r05_frontend_js_produto(self):
        self._indicio("frontend", 3, "R05", "JavaScript combinado com o desejo de entregar o produto final na tela do usuário aponta para interfaces web.")

    @Rule(PerfilUsuario(atuacao="frontend", entrega="produto"))
    def r06_frontend_produto(self):
        self._indicio("frontend", 2, "R06", "Sua atividade preferida e o tipo de entrega escolhido estão ambos ligados ao que o usuário vê e usa.")

    #Ciência de Dados
    @Rule(PerfilUsuario(atuacao="analise_dados"))
    def r07_ciencia_atuacao(self):
        self._indicio("ciencia", 4, "R07", "Você prefere analisar dados brutos, extrair estatísticas e construir modelos preditivos.")

    @Rule(PerfilUsuario(matematica="Alta", entrega="analise"))
    def r08_ciencia_matematica_analise(self):
        self._indicio("ciencia", 3, "R08", "Afinidade alta com matemática/estatística e interesse em entregar modelos e inteligência artificial.")

    @Rule(PerfilUsuario(matematica="Alta", ferramenta="Python"))
    def r09_ciencia_matematica_python(self):
        self._indicio("ciencia", 2, "R09", "Python com base matemática forte é a combinação típica de quem trabalha com Machine Learning.")

    @Rule(PerfilUsuario(matematica="Baixa", atuacao="analise_dados"))
    def r10_dados_sem_matematica(self):
        self._indicio("ciencia", -2, "R10", "Modelagem preditiva exige estatística, e você indicou afinidade baixa com ela.")
        self._indicio("engdados", 2, "R10", "Você gosta de lidar com dados, mas sem depender de estatística avançada, o que combina com a engenharia de dados.")

    #Engenharia de Dados
    @Rule(PerfilUsuario(atuacao="pipeline_dados"))
    def r11_engdados_atuacao(self):
        self._indicio("engdados", 4, "R11", "Você prefere construir pipelines (ETL/ELT) e a infraestrutura de Data Lakes.")

    @Rule(PerfilUsuario(entrega="dados_confiaveis"))
    def r12_engdados_entrega(self):
        self._indicio("engdados", 3, "R12", "Você quer entregar dados organizados e confiáveis para que outros times os utilizem.")

    @Rule(PerfilUsuario(atuacao="pipeline_dados", ferramenta=PYTHON_OU_SQL))
    def r13_engdados_ferramenta(self):
        self._indicio("engdados", 2, "R13", "Python ou SQL são as principais ferramentas para transformar e mover grandes volumes de dados.")

    #Cibersegurança
    @Rule(PerfilUsuario(atuacao="seguranca"))
    def r14_seguranca_atuacao(self):
        self._indicio("seguranca", 4, "R14", "Você prefere analisar vulnerabilidades, redes e trabalhar com defesa cibernética.")

    @Rule(PerfilUsuario(entrega="seguranca"))
    def r15_seguranca_entrega(self):
        self._indicio("seguranca", 3, "R15", "O valor que você quer entregar é proteção contra invasões e vazamentos.")

    @Rule(PerfilUsuario(entrega="seguranca", ferramenta="Linux/Redes"))
    def r16_seguranca_linux(self):
        self._indicio("seguranca", 2, "R16", "Conhecimento de Linux e redes é a base para análise de vulnerabilidades e testes de invasão.")

    #DevOps & SRE
    @Rule(PerfilUsuario(atuacao="automacao"))
    def r17_devops_atuacao(self):
        self._indicio("devops", 4, "R17", "Você prefere automatizar processos, pipelines de CI/CD e trabalhar com contêineres.")

    @Rule(PerfilUsuario(atuacao="automacao", ferramenta="Linux/Redes"))
    def r18_devops_linux(self):
        self._indicio("devops", 2, "R18", "Linux é o ambiente central de automação, contêineres e servidores.")

    @Rule(PerfilUsuario(atuacao="automacao", entrega="infraestrutura"))
    def r19_devops_infra(self):
        self._indicio("devops", 2, "R19", "Você quer sustentar a plataforma em que o sistema roda, e a automação é o meio para isso.")

    #Cloud
    @Rule(PerfilUsuario(atuacao="nuvem"))
    def r20_cloud_atuacao(self):
        self._indicio("cloud", 4, "R20", "Você prefere planejar, migrar e gerenciar infraestruturas escaláveis em nuvem.")

    @Rule(PerfilUsuario(atuacao="nuvem", entrega="infraestrutura"))
    def r21_cloud_infra(self):
        self._indicio("cloud", 3, "R21", "Planejar a infraestrutura que sustenta o sistema é o foco de quem projeta arquiteturas em AWS, Azure ou GCP.")

    #Mobile
    @Rule(PerfilUsuario(atuacao="mobile"))
    def r22_mobile_atuacao(self):
        self._indicio("mobile", 4, "R22", "Você prefere desenvolver aplicativos para dispositivos móveis.")

    @Rule(PerfilUsuario(atuacao="mobile", entrega="produto"))
    def r23_mobile_produto(self):
        self._indicio("mobile", 2, "R23", "Você quer entregar o produto final direto para o usuário, e o celular é o canal escolhido.")

    @Rule(PerfilUsuario(atuacao="mobile", ferramenta=L("Java/Kotlin/Swift") | L("JavaScript")))
    def r24_mobile_ferramenta(self):
        self._indicio("mobile", 2, "R24", "Kotlin, Swift ou JavaScript (React Native) são caminhos diretos para apps nativos ou multiplataforma.")

    #QA
    @Rule(PerfilUsuario(atuacao="qualidade"))
    def r25_qa_atuacao(self):
        self._indicio("qa", 4, "R25", "Você prefere garantir a confiabilidade do software com testes automatizados.")

    @Rule(PerfilUsuario(entrega="qualidade"))
    def r26_qa_entrega(self):
        self._indicio("qa", 3, "R26", "O valor que você quer entregar é um software que funciona sem erros.")

    @Rule(PerfilUsuario(atuacao="qualidade", ferramenta=L("Python") | L("JavaScript") | L("Java/Kotlin/Swift")))
    def r27_qa_automacao(self):
        self._indicio("qa", 1, "R27", "Dominar uma linguagem de programação permite escrever testes automatizados.")

    #Product Management
    @Rule(PerfilUsuario(atuacao="negocios"))
    def r28_pm_atuacao(self):
        self._indicio("pm", 4, "R28", "Você prefere conectar regras de negócio, design e desenvolvimento usando metodologias ágeis.")

    @Rule(PerfilUsuario(entrega="estrategia"))
    def r29_pm_entrega(self):
        self._indicio("pm", 3, "R29", "Você quer entregar estratégia, planejamento e priorização do produto.")

    @Rule(PerfilUsuario(atuacao="negocios", ferramenta="Nenhuma/Iniciante"))
    def r30_pm_sem_codigo(self):
        self._indicio("pm", 2, "R30", "Seu foco é gestão e processos de produto, sem depender de programar no dia a dia.")

    #Regras de decisão (encadeamento)
    @Rule(AS.perfil << PerfilUsuario(), salience=-10)
    def r31_decidir(self, perfil):
        """Soma os indícios e declara a trilha vencedora."""
        pontos = {}
        quantidade = {}
        for fato in self.facts.values():
            if isinstance(fato, Indicio):
                t = fato["trilha"]
                pontos[t] = pontos.get(t, 0) + fato["pontos"]
                quantidade[t] = quantidade.get(t, 0) + 1

        if not pontos:
            return

        natural = ATUACAO_TRILHA.get(perfil["atuacao"])
        ordem = sorted(
            pontos,
            key=lambda t: (pontos[t], t == natural, quantidade[t]),
            reverse=True,
        )
        self.resultado = Resultado(
            ranking=[(TRILHAS[t], pontos[t]) for t in ordem],
        )
        self.declare(Recomendacao(trilha=ordem[0], pontos=pontos[ordem[0]]))

    @Rule(Recomendacao(trilha=MATCH.trilha, pontos=MATCH.pontos), salience=-20)
    def r32_justificar(self, trilha, pontos):
        """Reúne os motivos da trilha vencedora."""
        motivos = [
            (f["regra"], f["motivo"], f["pontos"])
            for f in self.facts.values()
            if isinstance(f, Indicio) and f["trilha"] == trilha and f["pontos"] > 0
        ]
        motivos.sort(key=lambda m: (-m[2], m[0]))
        self.resultado.trilha = TRILHAS[trilha]
        self.resultado.pontos = pontos
        self.resultado.justificativas = motivos


def diagnosticar(matematica, atuacao, ferramenta, entrega):
    """Executa o motor para um perfil e devolve um Resultado."""
    motor = ConsultorCarreira()
    motor.reset()
    motor.declare(PerfilUsuario(
        matematica=matematica,
        atuacao=atuacao,
        ferramenta=ferramenta,
        entrega=entrega,
    ))
    motor.run()
    return motor.resultado