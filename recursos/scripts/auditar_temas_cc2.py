from __future__ import annotations

"""Auditoría de pares: 16 temas de CC2 con 1 h1, ids, anclas y navegación entre temas.

Uso: python auditar_temas_cc2.py [raiz_repo]
Solo biblioteca estándar.
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/Users/mag/Documents/hermes/cc_computacion_2").resolve()
TEMAS = [
    (1, "evaluacion_1/temas/tema_01.html"),
    (2, "evaluacion_1/temas/tema_02.html"),
    (3, "evaluacion_1/temas/tema_03.html"),
    (4, "evaluacion_1/temas/tema_04.html"),
    (5, "evaluacion_1/temas/tema_05.html"),
    (6, "evaluacion_1/temas/tema_06.html"),
    (7, "evaluacion_2/temas/tema_07.html"),
    (8, "evaluacion_2/temas/tema_08.html"),
    (9, "evaluacion_2/temas/tema_09.html"),
    (10, "evaluacion_2/temas/tema_10.html"),
    (11, "evaluacion_2/temas/tema_11.html"),
    (12, "evaluacion_3/temas/tema_12.html"),
    (13, "evaluacion_3/temas/tema_13.html"),
    (14, "evaluacion_3/temas/tema_14.html"),
    (15, "evaluacion_3/temas/tema_15.html"),
    (16, "evaluacion_3/temas/tema_16.html"),
]


class Doc(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.refs = []
        self.h1 = 0
        self.titles = []
        self._en_titulo = False
        self._titulo = []

    def handle_starttag(self, tag, attrs):
        datos = dict(attrs)
        if datos.get("id"):
            self.ids.append(datos["id"])
        for k in ("href", "src"):
            if datos.get(k):
                self.refs.append(datos[k])
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self._en_titulo = True
            self._titulo = []

    def handle_endtag(self, tag):
        if tag == "title" and self._en_titulo:
            self._en_titulo = False
            self.titles.append("".join(self._titulo).strip())

    def handle_data(self, data):
        if self._en_titulo:
            self._titulo.append(data)


def parse(ruta):
    d = Doc()
    d.feed(ruta.read_text(encoding="utf-8"))
    return d


def main():
    por_numero = dict(TEMAS)
    problemas = []
    docs = {}
    for numero, rel in TEMAS:
        p = ROOT / rel
        if not p.exists():
            problemas.append(f"{rel}: FALTA")
            continue
        d = parse(p)
        docs[numero] = d
        texto = p.read_text(encoding="utf-8")
        if d.h1 != 1:
            problemas.append(f"{rel}: h1={d.h1}")
        if len(d.ids) != len(set(d.ids)):
            problemas.append(f"{rel}: ids duplicados")
        for id_obligatorio in ("pregunta", "resumen", "practicas", "evaluacion_moodle", "fuentes"):
            if id_obligatorio not in d.ids:
                problemas.append(f"{rel}: falta #{id_obligatorio}")
        if not d.titles or f"Tema {numero}" not in d.titles[0]:
            problemas.append(f"{rel}: título incorrecto -> {d.titles}")
        if len(texto) < 8000:
            problemas.append(f"{rel}: breve ({len(texto)} bytes)")
        # bloques python: los temas 12-16 deben incluir algo de código
        if numero >= 12 and "<pre><code>" not in texto:
            problemas.append(f"{rel}: sin bloque de código")
        # enlaces internos
        for ref in d.refs:
            if ref.startswith(("http", "mailto:")):
                continue
            destino, _, ancla = ref.partition("#")
            base = (p.parent / destino).resolve() if destino else p.parent
            if destino and not base.exists():
                # se permite enlazar prácticas aún no creadas (../practicas/practica_NN.html)
                if "practicas" in str(base):
                    continue
                problemas.append(f"{rel}: enlace roto {ref}")
    # cadena: cada tema enlaza anterior/siguiente cuando existe
    for numero, d in docs.items():
        texto = open(ROOT / por_numero[numero], encoding="utf-8").read()
        for otro in (numero - 1, numero + 1):
            if otro in por_numero:
                if por_numero[otro].split("/")[-1] not in texto:
                    problemas.append(f"{por_numero[numero]}: no enlaza {por_numero[otro]}")
    if problemas:
        print("PROBLEMAS:")
        for p in problemas:
            print(" -", p)
        sys.exit(1)
    print(f"AUDIT_TEMAS_OK temas={len(TEMAS)}")


if __name__ == "__main__":
    main()
