from typing import Any

import requests
import json
from pathlib import Path
from datetime import datetime

MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
CACHE_DIR = Path.home() / ".minecraft_cache"
CACHE_DIR.mkdir(exist_ok=True)


def fetch_manifest():
    """Downloads Mojang versions list"""
    cache_file = CACHE_DIR / "manifest.json"

    try:
        response = requests.get(MANIFEST_URL, timeout=10)
        response.raise_for_status()

        manifest = response.json()

        with open(cache_file, 'w') as f:
            json.dump(manifest, f)

        return manifest

    except requests.RequestException as e:
        if cache_file.exists():
            print(f"⚠️  Couldn't connect to Mojang API. Using cache.")
            with open(cache_file) as f:
                return json.load(f)
        else:
            raise RuntimeError(f"Couldn't download manifest: {e}")


def resolve_latest(manifest, version_type):
    return manifest["latest"][version_type]


def get_version_info(
        manifest, 
        version_type: str, 
        version_id: str
) -> None  | Any:
    """
    Checks if the version really exists

    Examples:
    - version_exists(manifest, "latest", "release") → True
    - version_exists(manifest, "1.21.4", "snapshot") → False
    - version_exists(manifest, "25w10a", "release") → False
    """
    version_info = None

    if version_id == "latest":
        resolve = resolve_latest(manifest, version_type)
        if not resolve:
            raise ValueError("Something went wrong."
                             "Mojang manifest doesn't have a value for latest"
                             f"version of {version_type}.")
        else:
            version_id = resolve

    exists = False

    for version in manifest["versions"]:
        if version["id"] == version_id:
            version_info = version
            exists = True

    if not exists:
        raise ValueError(f"Version {version_id} "
                         "was not found in Mojang manifest")

    return version_info


def fetch_version_metadata(
        manifest,
        version_id: str,
        version_type: str):
    """
    Downloads details for a specific version
    """
    cache_file = CACHE_DIR / f"version_{version_id}.json"

    version_info = get_version_info(manifest, version_type, version_id)

    # Tries to download or use cache
    try:
        response = requests.get(version_info["url"], timeout=10)
        response.raise_for_status()

        metadata = response.json()

        # Guarda en cache
        with open(cache_file, 'w') as f:
            json.dump(metadata, f)

        return metadata

    except requests.RequestException as e:
        if cache_file.exists():
            print(f"⚠️  Using cache for versión {version_id}")
            with open(cache_file) as f:
                return json.load(f)
        else:
            raise RuntimeError(f"Couldn't download metadata of"
                               f" {version_id}: {e}")


def extract_java_version(metadata):
    """Extracts de Java version number required from the metadata
    of a Minecraft Version"""

    try:
        java_version = metadata["javaVersion"]["majorVersion"]
        return java_version
    except KeyError:
        raise ValueError(" javaVersion not found in metadata.")


def extract_server_download(metadata):
    """Extracts server download URL for server.jar"""
    try:
        server_info = metadata["downloads"]["server"]
        return {
            "url": server_info["url"],
            "sha1": server_info["sha1"],
            "size": server_info["size"]
        }
    except KeyError:
        raise ValueError("downloads.server not found in metadata.")

def resolve_minecraft_version(
        version_id: str = "latest",
                              version_type: str = "release"):
    """
    Flujo completo:
    1. Downloads manifest
    2. Resolves version (latest, release → 1.21.5)
    3. Downloads version metadata
    4. Extracts Java version and server URL

    Returns:
    {
        "minecraft_version": "1.21.5",
        "java_version": 21,
        "server_url": "https://...",
        "server_sha1": "abc123...",
        "server_size": 123456789
    }
    """

    # Paso 1
    print(f"📥 Descargando manifest de versiones...")
    manifest = fetch_manifest()

    # Paso 2
    print(f"🔍 Resolviendo versión: {version_id}")
    minecraft_version = get_version_info(manifest, version_id)
    print(f"   → {minecraft_version}")

    # Paso 3
    print(f"📥 Descargando metadata de {minecraft_version}...")
    metadata = fetch_version_metadata(manifest, minecraft_version)

    # Paso 4
    java_version = extract_java_version(metadata)
    server_info = extract_server_download(metadata)

    print(f"✅ Resuelto:")
    print(f"   Minecraft: {minecraft_version}")
    print(f"   Java: {java_version}")
    print(f"   Server JAR: {server_info['size'] / 1024 / 1024:.1f} MB")

    return {
        "minecraft_version": minecraft_version,
        "java_version": java_version,
        "server_url": server_info["url"],
        "server_sha1": server_info["sha1"],
        "server_size": server_info["size"]
    }


# ========== EJEMPLO DE USO ==========

if __name__ == "__main__":
    # Prueba
    result = resolve_minecraft_version("latest")
    print("\nResultado final:")
    print(json.dumps(result, indent=2))