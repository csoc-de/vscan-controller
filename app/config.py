import os

from dotenv import load_dotenv

try:
    from app.build_info import VERSION, COMMIT, BUILD_AT
except ImportError:
    VERSION = "{version}"
    COMMIT = "{commit}"
    BUILD_AT = "{build_at}"

load_dotenv()
API_KEY: str = os.getenv("API_KEY", "1234567890123456789")
HOST: str = os.getenv("HOST", "localhost")
PORT: int = int(os.getenv("PORT", "8080"))
GREENBONE_SOCKET_PATH: str = os.getenv("GREENBONE_SOCKET_PATH", "/run/gvmd/gvmd.sock")
GREENBONE_USER: str = os.getenv("GREENBONE_USER", "admin")
GREENBONE_PASSWORD: str = os.getenv("GREENBONE_PASSWORD", "admin")
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
