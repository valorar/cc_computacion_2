"""Auditoría de navegador para el sitio CC2 (Playwright).

Uso: python auditar_navegador_cc2.py [base_url] [raiz_repo]
Requiere: playwright instalado y, si la URL es local, un servidor http levantado.
Comprueba 200 en 2+16 páginas, h1 único, ausencia de desbordamiento horizontal
y errores de consola, en varias anchuras y sin JavaScript.
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765/"
ROOT = Path(sys.argv[2] if len(sys.argv) > 2 else "/Users/mag/Documents/hermes/cc_computacion_2").resolve()

RELATIVAS = ["index.html", "programa.html"]
for ev, rango in (("evaluacion_1", range(1, 7)), ("evaluacion_2", range(7, 12)), ("evaluacion_3", range(12, 17))):
    for n in rango:
        RELATIVAS.append(f"{ev}/temas/tema_{n:02d}.html")

ANCHURAS = [320, 390, 768, 1280]


def main() -> None:
    paginas = []
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        for ancho in ANCHURAS:
            pagina = navegador.new_page(viewport={"width": ancho, "height": 900})
            errores_consola = []
            pagina.on("console", lambda m: errores_consola.append(m.text) if m.type == "error" else None)
            for rel in RELATIVAS:
                url = BASE.rstrip("/") + "/" + rel
                r = pagina.goto(url, wait_until="load", timeout=20000)
                assert r is not None and r.status == 200, f"{rel} -> HTTP {(r.status if r else 'sin respuesta')}"
                assert pagina.locator("h1").count() == 1, f"{rel}: h1={pagina.locator('h1').count()}"
                ancho_doc = pagina.evaluate("document.documentElement.scrollWidth")
                assert ancho_doc <= ancho + 1, f"{rel}@{ancho}px: scrollWidth={ancho_doc}"
                paginas.append((rel, ancho, r.status))
            # Modo sin JavaScript
            ctx_sin_js = navegador.new_context(viewport={"width": 390, "height": 900}, java_script_enabled=False)
            pg = ctx_sin_js.new_page()
            for rel in RELATIVAS[:3]:
                r = pg.goto(BASE.rstrip("/") + "/" + rel, wait_until="load", timeout=20000)
                assert r is not None and r.status == 200
            ctx_sin_js.close()
            assert not errores_consola, f"errores de consola a {ancho}px: {errores_consola[:5]}"
            pagina.close()
        navegador.close()
    print(f"BROWSER_CC2_OK paginas={len(paginas)} anchuras={len(ANCHURAS)} sin_js=yes")


if __name__ == "__main__":
    main()
