#!/usr/bin/env python3
"""Aplica los cambios pedidos al proyecto Sistedes2026.

Uso:
  python3 apply_sistedes_changes.py /ruta/al/repositorio/Sistedes2026

Hace copia .bak de cada fichero modificado.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

PROLE_ROOM = "Aula Institucional / PROLE"
ROOM_LINKS = {
    "Aula 1.2": "https://cvnet.cpd.ua.es/FichaAula/es/Aula/Ver/0101P2007",
    "Aula 1.1": "https://cvnet.cpd.ua.es/FichaAula/es/Aula/Ver/0101P1003",
    "Aula Rafael Altamira": "https://cvnet.cpd.ua.es/FichaAula/es/Aula/Ver/0101PB005",
    "Aula 2.2": "https://cvnet.cpd.ua.es/FichaAula/es/Aula/Ver/0101P2001",
}

ANCHOR_RE = re.compile(r"<a\b[^>]*>(.*?)</a>", re.IGNORECASE | re.DOTALL)
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\((?:[^)(]+|\([^)]*\))*\)")


def strip_links(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    value = ANCHOR_RE.sub(r"\1", value)
    value = MD_LINK_RE.sub(r"\1", value)
    return value


def backup(path: Path) -> None:
    bak = path.with_suffix(path.suffix + ".bak")
    if not bak.exists():
        shutil.copy2(path, bak)


def write_json(path: Path, data: Any) -> None:
    backup(path)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def remove_vestibulo_link(row: dict[str, Any]) -> None:
    links = row.get("links")
    if not isinstance(links, list):
        return
    kept = []
    removed = False
    for link in links:
        if (
            isinstance(link, dict)
            and strip_links(link.get("label", "")).strip().lower() == "vestíbulo sede"
            and link.get("url", "#") == "#"
        ):
            removed = True
            continue
        kept.append(link)
    if removed and row.get("label") and "Vestíbulo sede" not in row["label"]:
        row["label"] = f"{row['label']} · Vestíbulo sede"
    if kept:
        row["links"] = kept
    else:
        row.pop("links", None)


def patch_config(config: dict[str, Any]) -> dict[str, Any]:
    config["rooms"] = [room for room in config.get("rooms", []) if room != PROLE_ROOM]
    config["roomLinks"] = {**config.get("roomLinks", {}), **ROOM_LINKS}

    aliases = config.get("roomAliases")
    if isinstance(aliases, dict):
        for key in list(aliases):
            if key == "SALA E" or aliases[key] == PROLE_ROOM:
                del aliases[key]

    for day in config.get("days", []):
        if isinstance(day, dict):
            day["rooms"] = [room for room in day.get("rooms", []) if room != PROLE_ROOM]
            for row in day.get("rows", []):
                if not isinstance(row, dict):
                    continue
                if isinstance(row.get("cells"), list):
                    row["cells"] = [cell for cell in row["cells"] if not (isinstance(cell, dict) and cell.get("room") == PROLE_ROOM)]
                remove_vestibulo_link(row)
    return config


def has_track_content(sessions: Any) -> bool:
    if not isinstance(sessions, list):
        return False
    for session in sessions:
        if isinstance(session, dict) and any(key != "hora" for key in session):
            return True
    return False


def clean_track_data(value: Any) -> Any:
    if isinstance(value, str):
        return strip_links(value)
    if isinstance(value, list):
        return [clean_track_data(item) for item in value]
    if isinstance(value, dict):
        cleaned = {strip_links(key): clean_track_data(item) for key, item in value.items()}
        # Si parece un diccionario track -> día -> sesiones, quita los días sin contenido.
        if cleaned and all(isinstance(v, list) for v in cleaned.values()):
            cleaned = {day: sessions for day, sessions in cleaned.items() if has_track_content(sessions)}
        return cleaned
    return value


def patch_json_file(path: Path, kind: str) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    new_data = patch_config(data) if kind == "config" else clean_track_data(data)
    if new_data != data:
        write_json(path, new_data)
        return True
    return False


def replace_embedded_json(html: str, script_id: str, transform) -> tuple[str, bool]:
    pattern = re.compile(
        rf'(<script\s+id=["\']{re.escape(script_id)}["\'][^>]*>)(.*?)(</script>)',
        re.IGNORECASE | re.DOTALL,
    )

    def repl(match: re.Match[str]) -> str:
        raw = match.group(2).strip()
        data = json.loads(raw)
        transformed = transform(data)
        formatted = json.dumps(transformed, ensure_ascii=False, indent=2)
        return f"{match.group(1)}\n{formatted}\n{match.group(3)}"

    new_html, count = pattern.subn(repl, html, count=1)
    return new_html, bool(count)


def patch_index(path: Path) -> bool:
    if not path.exists():
        return False
    original = path.read_text(encoding="utf-8")
    html = original
    html, _ = replace_embedded_json(html, "sprog-fallback-config", patch_config)
    html, _ = replace_embedded_json(html, "sprog-embedded-track-data", clean_track_data)

    script_tag = '  <script src="sistedes-postprocess.js"></script>'
    if "sistedes-postprocess.js" not in html:
        html = html.replace("</body>", f"{script_tag}\n</body>")

    if html != original:
        backup(path)
        path.write_text(html, encoding="utf-8")
        return True
    return False


def copy_postprocess(root: Path, source_dir: Path) -> bool:
    src = source_dir / "sistedes-postprocess.js"
    dst = root / "sistedes-postprocess.js"
    if not src.exists():
        return False
    if not dst.exists() or dst.read_text(encoding="utf-8") != src.read_text(encoding="utf-8"):
        shutil.copy2(src, dst)
        return True
    return False


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    if not root.exists():
        print(f"No existe la ruta: {root}", file=sys.stderr)
        return 2

    source_dir = Path(__file__).resolve().parent
    changed: list[str] = []

    config_path = root / "data" / "programa-config.json"
    if config_path.exists() and patch_json_file(config_path, "config"):
        changed.append(str(config_path.relative_to(root)))

    tracks_dir = root / "data" / "tracks"
    if tracks_dir.exists():
        for path in sorted(tracks_dir.glob("*.json")):
            if patch_json_file(path, "track"):
                changed.append(str(path.relative_to(root)))

    if patch_index(root / "index.html"):
        changed.append("index.html")

    if copy_postprocess(root, source_dir):
        changed.append("sistedes-postprocess.js")

    if changed:
        print("Ficheros modificados:")
        for item in changed:
            print(f"- {item}")
    else:
        print("No se han detectado cambios pendientes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
