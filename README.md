# Ciencias de la Computación II · 2.º de Bachillerato

Sitio web estático y portable para la materia optativa **Ciencias de la Computación II** (2.º de Bachillerato, Comunidad de Madrid, curso 2026–2027). Publicado con GitHub Pages: <https://valorar.github.io/cc_computacion_2/>

## Contenido

- **16 temas de teoría**, organizados en tres evaluaciones, con página propia en `evaluacion_N/temas/tema_NN.html`:
  - E1 · La red: conectar y defender (Bloque A, temas 1–6).
  - E2 · Seguridad y creación de contenidos digitales (Bloques B–C, temas 7–11).
  - E3 · Programar: de los datos al producto (Bloque D, temas 12–16).
- **Programa** (`programa.html`): evaluaciones, bloques oficiales, temas, metodología y calificación.
- **Prácticas** (fase posterior): 20 por evaluación en `evaluacion_N/practicas/`.

Marco curricular: Orden 1736/2023, de 19 de mayo (BOCM 31-05-2023), Anexo IV — currículo de la optativa «Ciencias de la Computación» de Bachillerato (apartado 2.º); Decreto 64/2022, de 20 de julio (ordenación del Bachillerato en la Comunidad de Madrid).

## Estructura

```
index.html                  Portada
programa.html               Programa del curso
assets/                     css/estilos.css · js/navegacion.js · img/favicon.svg
evaluacion_1/temas/         tema_01.html … tema_06.html
evaluacion_2/temas/         tema_07.html … tema_11.html
evaluacion_3/temas/         tema_12.html … tema_16.html
recursos/datos/             estructura_cc2.json (fuente de la estructura)
recursos/scripts/           tema_plantilla.html y utilidades
```

## Convenciones

- Nombres de archivo y carpeta con guion bajo (`_`), nunca con guion.
- HTML semántico, CSS compartido, JavaScript mínimo y no imprescindible; enlaces relativos y recursos locales.
- Imprimible y portable: el contenido funciona también como ZIP subido a Moodle con `index.html` como archivo principal.
- Sin claves, soluciones, bancos de preguntas ni datos personales en el repositorio público.

## Publicación

La raíz del repositorio es la raíz del sitio; GitHub Pages sirve la rama `main`.
