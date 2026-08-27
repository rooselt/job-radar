
import os
from dotenv import load_dotenv

load_dotenv()

# Cargo forte: título que só existe mesmo em vaga de engenharia de
# software backend/.NET/arquitetura, sem possibilidade real de ser outra
# área.
KEYWORDS_CARGO_FORTE = [
    "Desenvolvedor .NET",
    ".NET Developer",
    "Desenvolvedor C#",
    "C# Developer",
    "Engenheiro de Software",
    "Software Engineer",
    "Desenvolvedor Backend",
    "Desenvolvedor Back-end",
    "Backend Developer",
    "Backend Engineer",
    "Arquiteto de Software",
    "Software Architect",
    "Arquiteto de Soluções",
    "Solutions Architect",
    "Arquiteto Cloud",
    "Cloud Architect",
    "Tech Lead",
    "Technical Lead",
    "Líder Técnico",
    "Staff Engineer",
    "Principal Engineer",
    "Platform Engineer",
    "Engenheiro de Plataforma",
    "AI Engineer",
    "Engenheiro de IA",
    "Desenvolvedor Full Stack",
    "Full Stack Developer",
    "Fullstack Developer",
    # Genéricos de desenvolvimento — os títulos mais comuns em vaga
    # brasileira, e todos inequivocamente de desenvolvimento de software.
    "Desenvolvedor de Software",
    "Desenvolvedor de Sistemas",
    "Analista Desenvolvedor",
    "Desenvolvedor Web",
    "Web Developer",
    # Front-end e stacks JS: entram como cargo forte a pedido ("React e
    # Node também, todas as stacks"). Dados/BI fica FORA de propósito —
    # não é o hard skill do perfil.
    "Desenvolvedor React",
    "React Developer",
    "Desenvolvedor Node",
    "Node Developer",
    "Node.js Developer",
    "Desenvolvedor Angular",
    "Angular Developer",
    "Desenvolvedor Frontend",
    "Desenvolvedor Front-end",
    "Frontend Developer",
    "Front-end Developer",
    "Frontend Engineer",
    "Engenheiro Frontend",
]

# Cargo ambíguo: título que também é usado em vaga sem nada a ver com
# backend/.NET (ex: "Desenvolvedor" e "Engenheiro" existem em front-end,
# mobile, dados, civil... qualquer área). Só conta como match se o título
# TAMBÉM tiver um QUALIFICADORES_DADOS junto — é o que permite ir
# adicionando cargo adjacente sem cada um virar fonte de ruído sozinho.
KEYWORDS_CARGO_AMBIGUO = [
    "Desenvolvedor",
    "Developer",
    "Engenheiro",
    "Engineer",
    "Programador",
    "Analista de Sistemas",
    "Especialista",
    "Consultor",
]

# Termo que precisa aparecer junto no título quando o cargo é ambíguo, pra
# confirmar que é vaga de backend/.NET e não de outra área qualquer.
# NOME HERDADO: a lista guarda stack, não domínio de dados — o campo
# correspondente em job.py (RegrasFiltro.qualificadores_dados) mantém o
# nome antigo pra não espalhar rename por job.py/perfis.py/testes.
# MEDIDO (_contem_termo usa borda de palavra, ver job.py): ".net" NÃO bate
# em "ASP.NET" — o "P" antes do ponto é caractere de palavra e mata o
# (?<!\w). Mesma coisa com "node" x "NodeJS" e "react" x "ReactJS". Por
# isso cada stack aparece aqui em TODAS as grafias que os anúncios usam,
# não só na canônica.
QUALIFICADORES_DADOS = [
    # .NET / Microsoft
    ".net",
    "asp.net",
    "dotnet",
    "c#",
    "csharp",
    # papel/arquitetura
    "backend",
    "back-end",
    "frontend",
    "front-end",
    "fullstack",
    "full stack",
    "full-stack",
    "api",
    "microservi",
    "software",
    "sistemas",
    "web",
    # cloud / infra
    "cloud",
    "aws",
    "azure",
    "kubernetes",
    # stacks JS/TS e demais linguagens do perfil
    "react",
    "reactjs",
    "node",
    "nodejs",
    "node.js",
    "next.js",
    "nextjs",
    "angular",
    "typescript",
    "javascript",
    "python",
]

# Ferramenta/stack que aparece como núcleo do título ("Especialista .NET").
# Só conta como match se o título TAMBÉM tiver uma palavra de cargo — é o
# espelho da regra de KEYWORDS_CARGO_AMBIGUO: lá o cargo é ambíguo e pede
# stack, aqui a stack é ambígua e pede cargo. Sem isso, "Azure" sozinho
# aprovaria "Azure Data Engineer" e "Suporte Azure", que não são vaga de
# desenvolvimento backend.
FERRAMENTAS_TITULO = [
    ".NET",
    "ASP.NET",
    "C#",
    "Azure",
    "AWS",
    "Kubernetes",
    "React",
    "Node",
    "Node.js",
    "Angular",
    "TypeScript",
]

# Palavra de cargo que confirma que a vaga de stack é de engenharia.
# "desenvolvedor"/"engenheiro"/"arquiteto" ENTRAM aqui (na configuração
# anterior deste projeto ficavam fora de propósito, porque o alvo era vaga
# de análise de dados — aqui é o contrário).
QUALIFICADORES_CARGO = [
    "desenvolvedor",
    "developer",
    "engenheiro",
    "engineer",
    "arquiteto",
    "architect",
    "tech lead",
    "analista",
    "analyst",
    "especialista",
    "specialist",
    "consultor",
    "consultant",
]

KEYWORDS = KEYWORDS_CARGO_FORTE + KEYWORDS_CARGO_AMBIGUO

# Termos de busca enviados a cada site. Ficam separados das KEYWORDS de
# propósito: TERMOS_BUSCA é a rede ampla (o que é pesquisado em cada site,
# incluindo termos de ferramenta/stack pra achar vaga com título atípico),
# enquanto KEYWORDS é o filtro final e só olha o título da vaga já
# encontrada. Um termo de ferramenta (ex: "dax") só resulta em notificação
# se o TÍTULO da vaga também bater com uma keyword de cargo — isso evita
# falso positivo de vaga que só cita a ferramenta como diferencial.
#
# TERMOS_CARGO é derivado direto de KEYWORDS (em vez de mantido à mão em
# lista separada) — antes as duas listas divergiam: metade das KEYWORDS
# (ex: "Desenvolvedor BI", "BI Analyst", "Analista de Negócios") nunca era
# buscada de verdade, só existia como filtro, então só pegava essas vagas
# por sorte via outro termo. Com a derivação automática isso não pode mais
# acontecer — toda keyword nova em KEYWORDS já vira busca também.
TERMOS_CARGO_EXTRA = [
    # termos mais amplos que a keyword exata, mantidos por dar rede mais
    # larga na busca (a keyword em si é mais restrita, de propósito, pra
    # não gerar falso positivo no filtro de título).
    ".net",
    "c#",
    "microsserviços",
    "arquiteto de software",
]

TERMOS_CARGO = sorted(set(k.lower() for k in KEYWORDS) | set(TERMOS_CARGO_EXTRA))

# Termo de stack (não de cargo): serve pra achar vaga com título atípico
# que as KEYWORDS não cobrem. Só vira notificação se o TÍTULO da vaga
# também bater no filtro de cargo — termo de stack sozinho nunca aprova.
# Herdado do dono anterior deste radar: cada termo custa uma sessão de
# browser igual a um termo de cargo, então a lista fica curta de propósito
# e só cresce com termo que renda vaga de verdade (medir em jobradar.log
# antes de adicionar).
TERMOS_FERRAMENTA = [
    "asp.net",
    "aws",
    "azure",
    "kubernetes",
    "docker",
    "kafka",
    "sql server",
    "react",
    "node.js",
    "angular",
    "typescript",
    "next.js",
]

TERMOS_BUSCA = TERMOS_CARGO + TERMOS_FERRAMENTA

# Medido: os TERMOS_BUSCA inteiros (hoje 42) rodando em TODO ciclo é o que
# gera as centenas de sessões de navegador por execução — o custo cresce
# linear com o tamanho da lista, e a lista só cresce (mais ainda com a
# expansão internacional puxando mais termos no radar). TERMOS_POR_CICLO é
# o tamanho do BLOCO usado por ciclo, não o total de termos — main.py roda
# um bloco por vez em rodízio (ver _proximo_bloco_termos) e avança pro
# próximo bloco no ciclo seguinte, salvando a posição no jobs.db. Isso
# desacopla custo por ciclo de tamanho da lista: dobrar TERMOS_BUSCA dobra
# quantos ciclos até cobrir tudo de novo, não o custo de cada ciclo.
# 14 (era 10): o perfil internacional saiu da execução (ver workflow), o
# que liberou 3 fontes x 10 termos por ciclo, e a expansão pra todas as
# stacks levou TERMOS_BUSCA de 45 pra 69 — com 10/ciclo a cobertura
# completa ia de ~15h pra ~21h. 14 devolve os ~15h originais gastando um
# orçamento que o perfil internacional já consumia. Referência de custo
# medido: LinkedIn leva ~13s por passada (2 passadas por termo), e o
# timeout do workflow é 150min — tem folga. Se algum ciclo chegar perto do
# timeout, baixar aqui é o primeiro ajuste.
TERMOS_POR_CICLO = 14

# Só remoto: nenhuma cidade na whitelist. Job.combina_com aprova pela
# modalidade ("Remoto", campo próprio preenchido pelo scraper) — com a
# lista só com "Remoto", vaga presencial/híbrida é barrada em qualquer
# cidade, que é a decisão atual do perfil.
CIDADES = [
    "Remoto",
]

# MEDIDO: "Data Analyst @ Lisboa" e "Analista de Datos @ Madrid" reprovavam
# na localização, não no cargo — CIDADES acima é whitelist só de cidade
# brasileira, e a expansão de LOCATIONS_LINKEDIN pra Argentina/Chile (ver
# abaixo) passou a trazer vaga presencial/híbrida em Portugal/Espanha de
# vez em quando junto. Lista SEPARADA (não misturada em CIDADES, que
# continua só-Brasil de propósito — ver decisão registrada na criação do
# config_intl.py) com toggle próprio, pra dar pra ligar/desligar esse eixo
# sem mexer no resto do filtro. Canônica aqui porque config_intl.py já
# importa de config.py (não o contrário) — o pipeline internacional reusa
# essa mesma lista em vez de manter uma cópia (risco de divergir, mesmo
# motivo da unificação de _contem_termo/_tem_termo).
CIDADES_EUROPA_IBERICA = [
    "Portugal",
    "Lisboa",
    "Porto",
    "Braga",
    "Espanha",
    "España",
    "Spain",
    "Madrid",
    "Barcelona",
    "Valencia",
]

# Toggle independente do ATIVAR_EIXO_IBERICO de config_intl.py — são dois
# eixos diferentes (esse aqui é do pipeline BR/main.py, aquele é do
# pipeline internacional/main_intl.py), cada um com seu próprio liga/
# desliga, mesmo compartilhando a mesma lista de cidades acima.
#
# DESLIGADO: do mercado internacional, só interessa vaga remota — vaga
# presencial/híbrida em Lisboa/Madrid (o que esse eixo notifica, marcada
# "exploratória") não é o que o usuário quer. CIDADES_EUROPA_IBERICA
# continua definida (não precisa apagar) pra caso o eixo volte a ser
# ligado depois — só o toggle muda.
ATIVAR_EIXO_IBERICO_BR = False

# LinkedInScraper é a única fonte do pipeline BR que também alcança vaga
# fora do Brasil (as outras são portais brasileiros) — mas até aqui rodava
# só com location=Brasil fixo no código (scrapers/linkedin.py:88), então
# essa "porta pra fora" nunca era usada.
#
# Mercado "casa": busca modalidade completa (presencial/híbrida + remoto),
# porque é o único mercado do perfil atual.
#
# MEDIDO: "Brasil" (português) NÃO é resolvido pelo endpoint guest do
# LinkedIn — ele ignora o valor e cai no default por IP. Testado lado a
# lado com o mesmo termo ("desenvolvedor .net", 50 vagas cada):
#   location=Brasil -> 0 de 50 vagas no Brasil (tudo Seffner/FL, Austin/TX...)
#   location=Brazil -> 48 de 50 no Brasil, 20 aprovadas pelo filtro
# Ou seja: a passada nacional inteira era desperdício e o que entrava era
# vaga americana que o filtro de escopo tinha que barrar depois. Nome de
# país aqui vai em INGLÊS — é o que LOCATIONS_INTL em config_intl.py já
# usava ("Spain", "Portugal"), sem que a ligação tivesse sido feita.
LOCATIONS_LINKEDIN = ["Brazil"]

# Mercados adicionais (só busca REMOTA, f_WT=2). VAZIO: a decisão atual é
# só mercado Brasil, e cada país aqui custa uma passada de browser por
# termo — Argentina/Chile/México/Colômbia/Espanha/Portugal saíram por
# isso, não por não funcionarem (eram os países já testados ao vivo no
# endpoint do LinkedIn). Repovoar a lista é o único passo pra religar.
LOCATIONS_LINKEDIN_REMOTO_APENAS = []

# Mercado que a vaga remota precisa aceitar pra contar, quando o texto de
# local DECLARA um escopo geográfico ("Remote — US only", "Remote — India").
# Ver Job.escopo_remoto/RegrasFiltro.mercados_remoto_aceitos em job.py — sem
# isso, uma vaga remota só pra outro país passava igual a uma remota de
# verdade pro Brasil. Vaga remota SEM escopo declarado no texto (a grande
# maioria) continua batendo normalmente, isso só filtra quando a fonte
# EXPLICITA um mercado incompatível.
#
# MEDIDO: Argentina/Chile/México/Colômbia ENTRAM nominalmente agora — a
# suposição de que "LATAM" cobria os quatro como guarda-chuva só valia
# enquanto extrair_escopo_remoto resolvia o texto pra "LATAM" literal.
# Depois que passou a reconhecer cidade (Buenos Aires/Santiago/Cidade do
# México/Bogotá — ver _CIDADES_MERCADO em job.py), o escopo passou a
# resolver pro PAÍS específico, não mais pro guarda-chuva — e o país
# específico nunca esteve nessa lista. Resultado: LOCATIONS_LINKEDIN_
# REMOTO_APENAS pagava o custo de buscar nesses 4 países e o filtro
# descartava tudo que a busca trazia de lá. "LATAM" continua na lista pra
# quando o texto disser isso literalmente (guarda-chuva de verdade, não
# substituto de nome de país). Portugal e Espanha entraram nominalmente
# pelo mesmo motivo, desde antes.
MERCADOS_REMOTO_ACEITOS = ["Brasil", "LATAM"]

INTERVALO_MINUTOS = int(os.getenv("INTERVALO_MINUTOS", 180))

# Digest ranqueado (item 08): vaga com Job.pontuar_relevancia() >= este
# limiar notifica na hora (como sempre foi); abaixo disso, fica na fila do
# digest diário — ver _enviar_digest_diario em main.py.
#
# NÃO CALIBRADO AINDA pra este perfil. O 7 anterior veio de medição real
# do perfil de dados/BI do dono anterior (score 4-8, 7 deixava ~7%
# imediata) — com os pesos e o vocabulário atuais a conta é outra:
# "Desenvolvedor .NET Sênior" remoto com mercado confirmado já soma 3+2+2
# = 7, e com ".NET" no título vai a 9. Com limiar 7 quase tudo viraria
# notificação imediata e o digest perderia a função. Começa em 8 e
# recalibra com a distribuição real depois de ~1 semana rodando
# (relatorio_precisao.py + coluna relevancia no jobs.db).
#
# 9 (e não 8): medido no LinkedIn ao vivo, 9 é ~17% das aprovadas e
# exige acertar TODO sinal ao mesmo tempo — cargo forte + stack no
# título + senioridade alvo + mercado confirmado. Com 8 a fatia ia
# pra ~30%, o que na PRIMEIRA execução (banco sem nenhuma vaga de
# dev vista ainda) viraria 50+ mensagens seguidas e risco de rate
# limit do bot. O resto não some: cai no digest diário ranqueado.
LIMIAR_DIGEST_IMEDIATO = 9

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "jobs.db")