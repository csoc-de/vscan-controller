import os
import sys
import traceback
from argparse import ArgumentError, ArgumentParser

from dotenv import load_dotenv

try:
    from app.build_info import BUILD_AT, COMMIT, VERSION
except ImportError:
    VERSION = "<version>"
    COMMIT = "<commit>"
    BUILD_AT = "<build_at>"

try:
    parser = ArgumentParser()
    parser.add_argument("--dev", help="development mode", action="store_true")
    args = parser.parse_args()
    DEVELOPMENT_MODE = args.dev
except ArgumentError as e:
    DEVELOPMENT_MODE = False
    print(f"could not setup mode, set default mode prod\n ERROR: {e}\n{traceback.format_exc()}")

if DEVELOPMENT_MODE:
    load_dotenv()
    GREENBONE_PASSWORD: str = os.getenv("GREENBONE_PASSWORD", "admin")
    API_KEY: str = os.getenv("API_KEY", "1234567890123456789")
else:
    API_KEY_FILE: str = os.getenv("API_KEY_FILE", "/run/secrets/api_key")
    GREENBONE_PASSWORD_FILE: str = os.getenv(
        "GREENBONE_PASSWORD_FILE", "/run/secrets/greenbone_password"
    )
    try:
        with open(API_KEY_FILE, "r", encoding="utf-8") as f:
            API_KEY: str = f.read().strip()
        with open(GREENBONE_PASSWORD_FILE, "r", encoding="utf-8") as f:
            GREENBONE_PASSWORD: str = f.read().strip()
    except (OSError, UnicodeDecodeError) as e:
        print(f"could not read env vars\n ERROR: {e}\n{traceback.format_exc()}")
        sys.exit(-1)

HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8080"))
GREENBONE_SOCKET_PATH: str = os.getenv("GREENBONE_SOCKET_PATH", "/run/gvmd/gvmd.sock")
GREENBONE_USER: str = os.getenv("GREENBONE_USER", "admin")
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
FEEDS_METRICS_INTERVAL_SECONDS: int = int(os.getenv("FEEDS_METRICS_INTERVAL_SECONDS", "60"))
