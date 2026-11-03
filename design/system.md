# Envejecer Mejor — sistema visual existente

Fuente única: `envejecer-mejor.css`. Registro del CSS existente, no un sistema inventado. La propuesta usa fondos pastel y texto oliva para evitar los pares de bajo contraste del original.

## Colores
Todos proceden de `:root` en `envejecer-mejor.css`.

| Token | Valor | Uso original |
| --- | --- | --- |
| pink-50 | #fff5f9 | Fondo rosa |
| pink-100 | #ffe1ec | Tarjetas |
| pink-200 | #ffd6e6 | Barra |
| pink-300 | #f59fc1 | Bordes |
| pink-500 | #e8789f | Adornos |
| pink-600 | #d9628f | Títulos originales; evitar en texto pequeño |
| green-50 | #fcfdf1 | Superficie |
| green-100 | #e6f3c9 | Tarjetas |
| green-200 | #d6eca4 | Pie |
| green-300 | #b4d97a | Adornos |
| green-400 | #a9d06c | Bordes |
| green-500 | #9cc95e | Progreso |
| green-700 | #55722a | Texto |
| green-800 | #78963a | Iconos |
| blue-100 | #e3f3fb | Fondo |
| blue-200 | #a9d3e8 | Borde |
| blue-300 | #96ceee | Botón |
| blue-500 | #60acda | Botón |
| yellow | #f5c84c | Acento |
| white | #ffffff | Fondo |

## Tipografía
Fuente: `envejecer-mejor.css`, variables font-head y font-body. Encabezados: Fredoka, Arial Rounded MT Bold, Nunito, system-ui, sans-serif. Cuerpo: Nunito, Calibri, system-ui, sans-serif. Maquetas sin descargas: system-ui, sans-serif. Escalas existentes: 13, 16, 18, 26 y 30–44 px. Interlineado de cuerpo 1.5 y títulos 1.15.

## Medidas y componentes
Fuente: `envejecer-mejor.css`.
- Espaciado: 8, 10, 12, 16, 18, 20, 24 y 48 px; gap base 16 px.
- Radios: 8, 14 y 18 px; píldoras 999 px.
- Sombra: 0 6px 18px rgba(169, 208, 108, .25).
- Tarjetas: fondo blanco o pastel, padding 16 px, radio 14 px.
- Contenedor: máximo 960 px; colapsar columnas a 680 px.
- Botones: padding 10px 16px; foco visible. La maqueta usa oliva sobre blanco o blanco sobre oliva en lugar del gradiente celeste con texto blanco.
- Adornos: tréboles y corazones, sin significado funcional.
- Sin animación necesaria. No usar opacidad reducida para información importante.
