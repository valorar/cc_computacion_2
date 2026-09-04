from __future__ import annotations

"""Auditoría estructural del sitio CC2.

Uso: python auditar_sitio_cc2.py [raiz_repo]
Comprueba: 16 temas en sus evaluaciones, 1 h1 por página, ids únicos,
secciones de evaluación Moodle y prácticas, contrato de curso, enlaces
internos y anclas, y presencia en programa.html.
Solo biblioteca estándar.
"""

import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/Users/mag/Documents/hermes/cc_computacion_2").resolve()
EXPECTED = {
    n: f"evaluacion_{1 if n <= 6 else 2 if n <= 11 else 3}/temas/tema_{n:02d}.html"
    for n in range(1, 17)
}


class Document(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.refs: list[str] = []
        self.h1 = 0
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if data.get("id"):
            self.ids.append(data["id"] or "")
        for key in ("href", "src"):
            if data.get(key):
                self.refs.append(data[key] or "")
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def parse(path: Path) -> Document:
    doc = Document()
    doc.feed(path.read_text(encoding="utf-8"))
    doc.close()
    return doc


def main() -> None:
    paths = [ROOT / "index.html", ROOT / "programa.html"] + [ROOT / p for p in EXPECTED.values()]
    missing = [str(p.relative_to(ROOT)) for p in paths if not p.exists()]
    assert not missing, f"Faltan archivos: {missing}"
    documents = {p: parse(p) for p in paths}

    for number, relative in EXPECTED.items():
        path = ROOT / relative
        doc = documents[path]
        text = path.read_text(encoding="utf-8")
        assert doc.h1 == 1, f"{relative}: h1={doc.h1}"
        assert len(doc.ids) == len(set(doc.ids)), f"{relative}: identificadores duplicados"
        assert "evaluacion_moodle" in doc.ids, f"{relative}: falta evaluación Moodle"
        assert "practicas" in doc.ids, f"{relative}: falta sección de prácticas"
        assert "Moodle" in text and "../practicas/" in text, f"{relative}: contrato o enlaces incompletos"
        assert f"Tema {number}" in doc.title or str(number) in doc.title, f"{relative}: título no identifica el tema"
        assert len(text) >= 8000, f"{relative}: contenido sospechosamente breve ({len(text)})"

    for page, doc in documents.items():
        for ref in doc.refs:
            if ref.startswith(("http://", "https://", "mailto:", "tel:")):
                continue
            target_text, _, fragment = ref.partition("#")
            target = (page.parent / target_text).resolve() if target_text else page
            # Permitir enlaces a páginas de prácticas aún no creadas (fase posterior)
            if not target.exists() and "practicas" in str(target):
                continue
            assert target.exists(), f"{page.relative_to(ROOT)} -> enlace roto: {ref}"
            if fragment and target.suffix == ".html":
                target_doc = documents.get(target) or parse(target)
                assert fragment in target_doc.ids, f"{page.relative_to(ROOT)} -> ancla rota: {ref}"

    program = (ROOT / "programa.html").read_text(encoding="utf-8")
    for relative in EXPECTED.values():
        assert relative in program, f"programa.html no enlaza {relative}"

    print(f"AUDIT_OK pages={len(paths)} topics={len(EXPECTED)} moodle_y_practicas=yes")


if __name__ == "__main__":
    main()
