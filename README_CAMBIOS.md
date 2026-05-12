# Ficheros regenerados para SISTEDES 2026

Este paquete incluye una versión regenerada de los ficheros necesarios para aplicar los cambios pedidos al programa.

## Opción A: reemplazo directo

Copia estos ficheros en la raíz del repositorio:

- `index.html`
- `style.css`

El `index.html` nuevo carga los datos desde:

- `data/programa-config.json`
- `data/tracks/*.json`

Y aplica en tiempo de ejecución:

- eliminación de la columna `Aula Institucional / PROLE`;
- eliminación de las celdas PROLE;
- eliminación del enlace `Vestíbulo sede` cuando apunta a `#`;
- enlaces correctos en `Aula 1.2`, `Aula 1.1`, `Aula Rafael Altamira` y `Aula 2.2`;
- tablas de detalle de track solo para los días con contenido de ese track;
- textos de tracks sin enlaces HTML ni Markdown.

## Opción B: parche sobre el repositorio actual

Copia estos ficheros en la raíz del repositorio:

- `apply_sistedes_changes.py`
- `sistedes-postprocess.js`

Después ejecuta:

```bash
python3 apply_sistedes_changes.py .
```

El script crea copias `.bak` de los ficheros que modifique.

## Notas

- Si usas la opción A, asegúrate de conservar la carpeta `data/` del repositorio.
- Si usas la opción B, el script modifica `data/programa-config.json`, `data/tracks/*.json` e intenta actualizar también los JSON embebidos de `index.html` si existen.
