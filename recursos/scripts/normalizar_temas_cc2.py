"""Normaliza las páginas de tema de CC2 para cumplir html-validate.

1. <title> a 70 caracteres máximo.
2. aria-label únicos entre landmarks repetidos en la misma página.
3. Quita aria-label de <div>/<span> (no landmarks).

Uso: python normalizar_temas_cc2.py [raiz]
"""

import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/Users/mag/Documents/hermes/cc_computacion_2").resolve()
RUTAS = sorted(p for e in ("1", "2", "3") for p in (ROOT / f"evaluacion_{e}" / "temas").glob("tema_*.html"))


def acortar_titulo(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    if not m:
        return html
    titulo = m.group(1).strip()
    nuevo = titulo.split(" | ")[0].strip()
    if len(nuevo) > 68:
        nuevo = nuevo[:67].rstrip() + "…"
    return html.replace(m.group(0), f"<title>{nuevo}</title>")


def arreglar_aria_labels(html: str) -> str:
    # aside/div/section con aria-label repetido: enumerar a partir del segundo
    def numerar(match, clase):
        etiquetas = []
        def reemplazo(mm):
            etiqueta = mm.group(1)
            if etiqueta in etiquetas:
                # cuenta de apariciones anteriores
                n = etiquetas.count(etiqueta) + 1
                nueva = f"{etiqueta} {n}" if not etiqueta.endswith(" ") else f"{etiqueta}{n}"
                etiquetas.append(etiqueta)
                return mm.group(0).replace(etiqueta, nueva)
            etiquetas.append(etiqueta)
            return mm.group(0)
        patron = rf'<{clase}\b[^>]*\baria-label="([^"]+)"'
        return re.sub(patron, reemplazo, match)
    for clase in ("aside", "section", "nav"):
        html = numerar(html, clase)
    # quitar aria-label de div y span
    html = re.sub(r'<div\b([^>]*?)\saria-label="[^"]*"', r"<div\1", html)
    html = re.sub(r'<span\b([^>]*?)\saria-label="[^"]*"', r"<span\1", html)
    return html


def main() -> None:
    cambios = 0
    for p in RUTAS:
        original = p.read_text(encoding="utf-8")
        html = acortar_titulo(original)
        html = arreglar_aria_labels(html)
        if html != original:
            p.write_text(html, encoding="utf-8")
            cambios += 1
            print("normalizado:", p.name)
    print(f"NORMALIZADOS={cambios} de {len(RUTAS)}")


if __name__ == "__main__":
    main()
