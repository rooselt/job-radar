<div align="center">

<!-- ![JobRadar](assets/cover.png) -->

# 📡 JobRadar
### Monitor Automatizado de Vagas de Engenharia de Software

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-Scraping-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Banco%20versionado-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Cron-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Tests](https://img.shields.io/badge/testes-75%20passing-success?style=for-the-badge)
![Status](https://img.shields.io/badge/status-em%20produção-success?style=for-the-badge)

**Configuração atual:** Rooselt Adam S. H. de Oliveira — backend .NET / arquitetura, sênior+, 100% remoto

*Motor original por Liliam Kezia Oliveira Souza (perfil Dados & BI, Nordeste). Este fork mantém a engenharia e troca o vocabulário de busca, o alvo de senioridade e a regra de localização.*

</div>

---

## 💎 Proposta de valor

> Vaga sênior de backend .NET 100% remota aparece em oito boards diferentes, some rápido e vem afogada em ruído de front-end, dados e júnior. **JobRadar** é um sistema de monitoramento contínuo que substitui a checagem manual: varre **8 fontes** a cada **3 horas**, filtra por cargo/modalidade/mercado com três níveis de confiança, pontua cada vaga por relevância (senioridade alta pontua mais) e notifica no Telegram — rodando de graça, sem servidor próprio, 24 horas por dia.

## 📄 Resumo executivo

Números medidos entre 07 e 15 de agosto de 2026, **na configuração anterior (Dados & BI)** — valem como medição da arquitetura, não deste perfil, que ainda não acumulou histórico próprio:

| Achado | Número |
|---|---|
| 📊 Vagas processadas (deduplicadas) | **1.052** |
| 🔗 Concentração numa única fonte (LinkedIn) | **89,5%** |
| 🧪 Testes automatizados (CI a cada push) | **75** |
| 🌎 Fontes monitoradas em paralelo | **8** |
| ⏱️ Frequência de checagem | **a cada 3h** |
| 💰 Custo de infraestrutura | **R$ 0** |

A concentração em LinkedIn é um risco medido, não ignorado: o endpoint usado não é oficial e o próprio código documenta a chance de bloqueio — por isso parte do trabalho recente foi medir o rendimento de cada fonte secundária e paginar mais fundo nelas, em vez de só empilhar fonte nova.

---

## 📸 Como chega pra você

<!-- ![Notificação no Telegram](assets/screenshots/notificacao.png) -->

Vaga de alta relevância chega na hora, com motivo da aprovação, nível e link. O resto do dia entra num resumo único, ranqueado — sem virar spam.

---

## 🗂️ Sumário

- [Como funciona (pipeline)](#-como-funciona-pipeline)
- [Arquitetura técnica](#%EF%B8%8F-arquitetura-técnica)
- [Estrutura do repositório](#-estrutura-do-repositório)
- [Como rodar](#-como-rodar)
- [Testes](#-testes)

---

## 🧭 Como funciona (pipeline)

| Etapa | O que faz |
|---|---|
| **Busca** | Varre as fontes em paralelo, com rodízio de termos pra controlar custo por ciclo |
| **Filtra** | Cargo (forte / ambíguo + qualificador / stack + cargo), modalidade remota e mercado aceito (Brasil/LATAM) |
| **Pontua** | Score 0–10 por vaga: cargo, stack, senioridade, mercado, idioma — soma de sinais, sem IA |
| **Deduplica** | Por link e por empresa+título, pra pegar a mesma vaga republicada em fonte diferente |
| **Notifica** | Alta relevância na hora; o resto num resumo diário ranqueado, melhor vaga no topo |
| **Aprende** | Botão 👍/👎 em cada notificação — feedback vira dado pra medir precisão por fonte e por semana (ainda sem reação registrada no banco) |

## 🏗️ Arquitetura técnica

- **Filtro em 3 níveis de confiança:** cargo inequívoco passa sozinho ("Arquiteto de Software"); cargo ambíguo (ex: "Desenvolvedor") só conta com qualificador de stack junto no título; stack (ex: "Azure") só conta com palavra de cargo junto — nada aprova por palavra-chave solta.
- **Score de relevância sem ML:** 5 sinais conhecidos (cargo, stack, senioridade, mercado, idioma), soma simples de pesos. Senioridade alta (Sênior/Especialista/Tech Lead/Arquiteto) pontua bônus; júnior/pleno pontua deságio — nada disso é filtro, só ordena o que já passou.
- **Zero infraestrutura:** GitHub Actions como motor de cron, SQLite como banco — versionado no próprio Git, o histórico de vagas já vistas *é* o commit.
- **Resiliente:** nunca marca vaga como "vista" sem confirmar que a notificação saiu; alerta automático se metade das fontes falhar num ciclo; heartbeat diário confirmando que o robô ainda está de pé.
- **75 testes automatizados em CI:** cada caso documenta um bug real já corrigido nesta base — não é cenário hipotético, é regressão registrada.

## 📁 Estrutura do repositório

```
jobradar/
├── README.md
├── requirements.txt
├── main.py ← motor único: um ciclo de busca por perfil
├── perfis.py ← Brasil vs Internacional (dado, não lógica duplicada)
├── config.py / config_intl.py ← cargos, cidades, termos de busca, pesos
├── job.py ← Job, filtro, score de relevância
├── relatorio_precisao.py ← aprovadas/notificadas por fonte e por semana
├── database/
│ └── database.py ← SQLite: dedup, fila de digest, metadados
├── notifier/
│ └── telegram.py ← notificação individual, digest, botão 👍/👎
├── scrapers/ ← um módulo por fonte (LinkedIn, Gupy, Indeed...)
├── utils/
│ └── filtro.py
├── tests/ ← 75 casos, roda em CI a cada push
├── data/
│ └── jobs.db ← banco versionado (histórico de dedup)
└── .github/workflows/
├── jobradar.yml ← cron de produção (a cada 3h)
└── testes.yml ← CI
```

## 💻 Como rodar

```bash
git clone <repo>
cd jobradar
python -m venv venv && venv\Scripts\activate   # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

Copiar `.env.example` para `.env` e preencher `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` (via [@BotFather](https://t.me/BotFather)), depois:

```bash
python main.py --perfil brasil --once
```

O perfil `internacional` (LATAM/Ibéria, exige espanhol/português) continua definido em `config_intl.py` e coberto por testes, mas não roda — a configuração atual é só mercado Brasil.

## 🧪 Testes

```bash
pytest tests/ -v
```

75 casos parametrizados, cobrindo a camada de filtro, o parsing de callback do Telegram e o relatório de precisão — todos rodando automaticamente a cada push via GitHub Actions.

---

<div align="center">

*Case de portfólio em automação — Python, Playwright, SQLite, GitHub Actions e engenharia de filtro sem ML.*

</div>
