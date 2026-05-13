# Programa SISTEDES para GitHub Pages

Paquete actualizado para publicar el programa multitrack en GitHub Pages y embeberlo en WordPress.

## Cambios incluidos

- Corrección de QUANTUM: la primera jornada pasa a **Martes 16 de Junio de 2026**.
- En ASV/TASOVA y cualquier entrada sin ponencias ya no aparece el texto "Sin ponencias listadas para esta entrada".
- Las pausas café incluyen el enlace a Aula Miguel Hernández: https://cvnet.cpd.ua.es/FichaAula/es/Aula/Ver/0101PB008
- Se han eliminado las listas numeradas de ponencias.
- Se ha eliminado el prefijo visual `S1`, `S2`, etc. delante de cada sesión.
- Se ha añadido más separación visual entre días.
- Se ha eliminado el bloque de diagnóstico de carga.
- Se han añadido las franjas generales solicitadas con sus enlaces.
- El programa usa `Alicante` como ubicación.

## Qué subir

Sube el contenido de esta carpeta a la raíz de un repositorio de GitHub Pages:

```text
index.html
style.css
README_GITHUB_PAGES.md
data/programa-config.json
data/tracks/*.json
```

No subas el ZIP como único archivo: hay que descomprimirlo y subir su contenido.

## Activar GitHub Pages

1. Entra en el repositorio.
2. Ve a Settings > Pages.
3. En Build and deployment, elige Deploy from a branch.
4. Branch: main.
5. Folder: /root.
6. Guarda.

La URL quedará parecida a:

```text
https://TU-USUARIO.github.io/NOMBRE-REPO/
```

## Embeber en WordPress

```html
<iframe src="https://TU-USUARIO.github.io/NOMBRE-REPO/" style="width:100%;height:950px;border:0;" loading="lazy"></iframe>
```

## Comprobación rápida

Abre estas URLs:

```text
https://TU-USUARIO.github.io/NOMBRE-REPO/
https://TU-USUARIO.github.io/NOMBRE-REPO/data/programa-config.json
https://TU-USUARIO.github.io/NOMBRE-REPO/data/tracks/QUANTUM.json
```

Si las tres cargan, WordPress debería poder embeber el programa.
