# Programa SISTEDES multitrack - listo para GitHub Pages

Este paquete está preparado para subirlo a GitHub Pages como sitio estático.

## Qué subir

Sube al repositorio el CONTENIDO de esta carpeta, no el ZIP:

- `index.html`
- `style.css`
- `.nojekyll`
- `data/programa-config.json`
- `data/tracks/*.json`

La estructura final del repositorio debe quedar así:

```text
/
├── index.html
├── style.css
├── .nojekyll
└── data/
    ├── programa-config.json
    └── tracks/
        ├── AI4SE.json
        ├── ASV.json
        ├── ICD.json
        ├── ISDM.json
        ├── ISGD.json
        ├── MCPS.json
        ├── METODOS.json
        └── QUANTUM.json
```

## Activar GitHub Pages

1. Crea un repositorio en GitHub, por ejemplo `programa-sistedes`.
2. Sube los archivos anteriores al repositorio, en la raíz.
3. Ve a `Settings → Pages`.
4. En `Build and deployment`, selecciona `Deploy from a branch`.
5. Elige:
   - Branch: `main`
   - Folder: `/root`
6. Guarda.

La URL será similar a:

```text
https://TU-USUARIO.github.io/programa-sistedes/
```

## Comprobación rápida

Antes de embeberlo, abre directamente:

```text
https://TU-USUARIO.github.io/programa-sistedes/data/programa-config.json
https://TU-USUARIO.github.io/programa-sistedes/data/tracks/ICD.json
```

Si se ve el JSON en el navegador, el widget lo podrá cargar.

## WordPress

Pega en un bloque HTML:

```html
<iframe src="https://TU-USUARIO.github.io/programa-sistedes/"
        style="width:100%;height:950px;border:0;"
        loading="lazy"></iframe>
```

## Ajustes incluidos

- Se ha añadido `.nojekyll`.
- Se han eliminado archivos de macOS del paquete.
- Se ha corregido la ruta `QuantumX.json` → `QUANTUM.json`.
- Se han incluido todos los tracks del ZIP: `AI4SE`, `ASV`, `ICD`, `ISDM`, `ISGD`, `MCPS`, `METODOS`, `QUANTUM`.
- La tabla principal se genera dinámicamente desde los JSON, con filas transversales configuradas en `data/programa-config.json`.
- Si un JSON no carga, el diagnóstico muestra la URL exacta que ha fallado.
- `index.html` contiene datos embebidos como respaldo para pruebas locales, pero en GitHub Pages cargará los JSON externos.
- Se normalizan fechas mezcladas como `16 de Junio de 2026`, `Martes 16 de Junio` o `Jueves 2026` para construir una tabla principal coherente.
