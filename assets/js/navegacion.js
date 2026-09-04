(() => {
  "use strict";

  document.documentElement.classList.add("js");

  const botonMenu = document.querySelector("[data_boton_menu]");
  const navegacion = document.querySelector("[data_navegacion]");

  if (botonMenu && navegacion) {
    botonMenu.addEventListener("click", () => {
      const abierta = navegacion.classList.toggle("abierta");
      botonMenu.setAttribute("aria-expanded", String(abierta));
      botonMenu.textContent = abierta ? "Cerrar" : "Menú";
    });

    navegacion.addEventListener("click", (evento) => {
      if (evento.target.closest("a")) {
        navegacion.classList.remove("abierta");
        botonMenu.setAttribute("aria-expanded", "false");
        botonMenu.textContent = "Menú";
      }
    });
  }

  const indicador = document.querySelector("[data_progreso]");
  if (indicador) {
    const actualizarProgreso = () => {
      const altura = document.documentElement.scrollHeight - window.innerHeight;
      const porcentaje = altura > 0 ? Math.min(100, Math.max(0, (window.scrollY / altura) * 100)) : 0;
      indicador.style.width = `${porcentaje}%`;
    };
    actualizarProgreso();
    window.addEventListener("scroll", actualizarProgreso, { passive: true });
    window.addEventListener("resize", actualizarProgreso);
  }
})();
