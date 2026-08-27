
import time

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from job import Job, extrair_data_publicacao
from logger import get_logger
from scrapers.base import BaseScraper

logger = get_logger()

_MODALIDADES = {"remoto", "híbrido", "hibrido", "presencial"}

# Busca só a 1a página (10-12 vagas) nunca alcançava vaga de cidade menor
# (Recife, Natal, Maceió etc.) — um termo genérico tipo "analista de dados"
# tem centenas de resultados nacionais, e São Paulo/grandes polos sempre
# dominam a 1a página. Paginando, aumenta a chance real de achar vaga das
# cidades monitoradas, ao custo de mais requests por termo.
MAX_PAGINAS = 3


class GupyScraper(BaseScraper):
    """Busca vagas no portal público da Gupy (https://portal.gupy.io)."""

    def __init__(self, termos_busca: list[str]):
        self.termos_busca = termos_busca

    def buscar_vagas(self) -> list[Job]:
        vagas: list[Job] = []
        for termo in self.termos_busca:
            vagas.extend(self._buscar_termo(termo))

        logger.info(f"[Gupy] {len(vagas)} vaga(s) encontrada(s) no total")
        return vagas

    def _buscar_termo(self, termo: str) -> list[Job]:
        logger.info(f"[Gupy] Buscando: {termo}")
        vagas: list[Job] = []
        base_url = f"https://portal.gupy.io/job-search/term={termo.replace(' ', '%20')}"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                for pagina in range(1, MAX_PAGINAS + 1):
                    url = base_url if pagina == 1 else f"{base_url}?page={pagina}"
                    page.goto(url, timeout=60000)
                    sem_resultados = False
                    try:
                        page.wait_for_selector("a:has(h3)", timeout=15000)
                    except PlaywrightTimeoutError:
                        # MEDIDO: a Gupy NÃO renderiza "a:has(h3)" quando a
                        # página está vazia — ela renderiza o texto "Nenhum
                        # resultado foi encontrado" e mais nada. Ou seja, o
                        # fim natural da paginação chega aqui como timeout,
                        # exatamente igual a um site lento. Reproduzido com
                        # 'arquiteto de software': pág. 1 = 12 cards, pág. 2 =
                        # 6 cards (parcial, última), pág. 3 = 0 cards + o
                        # texto de vazio.
                        #
                        # Por isso o texto de vazio é checado ANTES de julgar
                        # o timeout, em QUALQUER página. Antes essa checagem
                        # vinha depois de um `if pagina > 1: warning; break`,
                        # então só era alcançável na página 1 — e todo fim de
                        # paginação normal virava um WARNING dizendo
                        # "parando por falha de carregamento, não por fim
                        # real dos resultados", que é o oposto do que estava
                        # acontecendo.
                        if "Nenhum resultado foi encontrado" in page.inner_text("body"):
                            logger.info(
                                f"[Gupy] Fim dos resultados de '{termo}' na página {pagina}."
                                if pagina > 1 else
                                f"[Gupy] 0 resultados reais para '{termo}'."
                            )
                            sem_resultados = True
                        elif pagina > 1:
                            # Timeout de verdade (site lento, bloqueio): a
                            # página não trouxe card NEM o texto de vazio.
                            # Aqui o aviso é legítimo — pode ter ficado vaga
                            # de fora e o log precisa registrar isso.
                            logger.warning(
                                f"[Gupy] Timeout esperando resultados na página {pagina} de "
                                f"'{termo}' — parando de paginar por falha de carregamento, "
                                "não por fim real dos resultados. Pode ter ficado vaga de "
                                "página seguinte de fora."
                            )
                            break
                        else:
                            raise
                    time.sleep(2 if not sem_resultados else 0)  # dá tempo do React terminar de renderizar

                    cards = [] if sem_resultados else page.query_selector_all("a:has(h3)")
                    if not cards:
                        break

                    for card in cards:
                        try:
                            titulo_el = card.query_selector("h3")
                            if not titulo_el:
                                continue
                            titulo = titulo_el.inner_text().strip()

                            empresa_el = card.query_selector("p")
                            empresa = empresa_el.inner_text().strip() if empresa_el else "Não informado"

                            local_el = card.query_selector('[data-testid="job-location"]')
                            cidade = local_el.inner_text().strip() if local_el else "Não informado"

                            # O modelo de trabalho (Remoto/Híbrido/Presencial) fica num span
                            # solto no card. Antes dependia do atributo alt do ícone ao lado
                            # (alt="Ícone de Modelo de Trabalho"), mas a Gupy parou de renderizar
                            # esse atributo — agora procura direto pelo texto do span, mesma
                            # técnica usada nos outros scrapers.
                            modelo = ""
                            for span in card.query_selector_all("span"):
                                texto_span = span.inner_text().strip()
                                if texto_span.lower() in _MODALIDADES:
                                    modelo = texto_span
                                    break

                            link = card.get_attribute("href")
                            if not link:
                                continue

                            publicado_em = extrair_data_publicacao(card.inner_text())

                            vagas.append(Job(
                                titulo=titulo,
                                empresa=empresa,
                                local=cidade,
                                link=link,
                                site="Gupy",
                                publicado_em=publicado_em,
                                modalidade=modelo,
                            ))
                        except Exception as e:
                            logger.warning(f"[Gupy] Erro ao processar card: {e}")
                            continue

                    if sem_resultados:
                        break

            except Exception as e:
                logger.error(f"[Gupy] Erro ao buscar '{termo}': {e}")
            finally:
                browser.close()

        return vagas
