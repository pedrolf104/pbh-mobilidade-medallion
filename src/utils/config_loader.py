from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml


def load_settings(path: str = "src/config/settings.yaml") -> Dict[str, Any]:
    """
    Lê o arquivo YAML de configuração do projeto e devolve um dicionário Python.

    Por que isso existe?
    - Evita hardcode de paths/URLs no código
    - Centraliza configurações em um único lugar (settings.yaml)
    """
    settings_path = Path(path)

    if not settings_path.exists():
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {settings_path.resolve()}")

    with settings_path.open("r", encoding="utf-8") as f:
        settings = yaml.safe_load(f)

    if not isinstance(settings, dict):
        raise ValueError("O settings.yaml não retornou um dicionário. Verifique a estrutura do YAML.")

    return settings


def get_nested(settings: Dict[str, Any], keys: list[str]) -> Any:
    """
    Acessa um valor dentro de um dicionário aninhado.
    Exemplo: get_nested(settings, ['storage', 'base_path'])
    """
    current: Any = settings
    for k in keys:
        if not isinstance(current, dict) or k not in current:
            raise KeyError(f"Chave não encontrada no settings.yaml: {'/'.join(keys)}")
        current = current[k]
    return current


if __name__ == "__main__":
    s = load_settings()

    project_name = get_nested(s, ["project", "name"])
    base_path = get_nested(s, ["storage", "base_path"])
    realtime_page = get_nested(s, ["datasets", "realtime_bus_positions", "dataset_page"])

    print("✅ Config carregada com sucesso!")
    print(f"Project: {project_name}")
    print(f"Base path: {base_path}")
    print(f"Realtime dataset page: {realtime_page}")