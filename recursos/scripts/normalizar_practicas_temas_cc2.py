"""Normaliza la sección #practicas de cada tema CC2.

Las páginas de práctica aún no existen (fase posterior). Para que los temas no
contradigan el reparto real (15 autocorregibles + 5 con rúbrica: 04, 08, 12,
16 y 20), esta sección se sustituye por enlaces neutros con la modalidad
correcta y títulos genéricos que se actualizarán al crear las prácticas.

Uso: python normalizar_practicas_temas_cc2.py [raiz]
"""

import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/Users/mag/Documents/hermes/cc_computacion_2").resolve()
RUTAS = sorted(p for e in ("1", "2", "3") for p in (ROOT / f"evaluacion_{e}" / "temas").glob("tema_*.html"))


def nueva_seccion(eval_id: str) -> str:
    items = []
    for n in range(1, 21):
        modo = "modalidad_docente" if n in (4, 8, 12, 16, 20) else "modalidad_auto"
        texto = "Rúbrica" if n in (4, 8, 12, 16, 20) else "Moodle"
        etiqueta = f"{eval_id}_P{n:02d}"
        items.append(
            f'<li><a href="../practicas/practica_{n:02d}.html"><strong>{etiqueta}</strong> · '
            f'Práctica {n:02d} de la evaluación</a> <span class="pildora {modo}">{texto}</span></li>'
        )
    lista = "\n".join(items)
    return (
        '<section id="practicas">\n'
        '            <span class="etiqueta">PRÁCTICA EN EL AULA</span>\n'
        '            <h2>Prácticas vinculadas al tema</h2>\n'
        "            <p>La teoría y las instrucciones de trabajo se mantienen separadas. Esta evaluación tiene 20 prácticas: "
        "15 autocorregibles en Moodle y 5 corregidas por el profesor con rúbrica (las prácticas 04, 08, 12, 16 y 20). "
        "Cada tema enlaza las prácticas donde aplica lo aprendido:</p>\n"
        f"            <ol class=\"enlaces_teoria\">\n{lista}\n            </ol>\n"
        '            <p><a class="boton boton_secundario" href="../practicas/index.html">Ver las 20 prácticas de la evaluación</a></p>\n'
        '            <p class="nota">Las prácticas autocorregibles registran su nota en Moodle dentro de la categoría Prácticas (70%). '
        "Las señaladas como «Rúbrica» son corregidas por el profesor con criterios publicados antes de empezar.</p>\n"
        "          </section>"
    )


def main() -> None:
    cambios = 0
    for p in RUTAS:
        texto = p.read_text(encoding="utf-8")
        ev = p.parent.parent.name  # evaluacion_1/2/3
        numero = int(re.search(r"tema_(\d+)", p.name).group(1))
        prefijo = {"evaluacion_1": "E1", "evaluacion_2": "E2", "evaluacion_3": "E3"}[ev]
        # localizar la sección #practicas completa (hasta </section> que cierra)
        m = re.search(r'<section id="practicas">.*?</section>', texto, re.S)
        if not m:
            print(f"  AVISO: {p.name} no tiene #practicas")
            continue
        texto2 = texto.replace(m.group(0), nueva_seccion(prefijo))
        # el título «Prácticas de la evaluación» que usan algunas páginas en el menú lateral
        # puede referirse a #practicas; se conserva tal cual.
        if texto2 != texto:
            p.write_text(texto2, encoding="utf-8")
            cambios += 1
            print(f"  OK {p.name} (E{numero}) -> {prefijo}")
    print(f"NORMALIZADAS_PRACTICAS={cambios} de {len(RUTAS)}")


if __name__ == "__main__":
    main()
