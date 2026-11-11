# vscan-controller

A REST API for [Greenbone Vulnerability Management (GVM)](https://www.greenbone.net/).

vscan-controller talks to `gvmd` over its Unix socket using the Greenbone Management Protocol (GMP)
and exposes targets, tasks, schedules, reports and more as a JSON API. It also exports
Prometheus metrics about the state of the GVM feeds.

## Configuration

| Variable                         | Default                           | Description                                                                 |
| -------------------------------- | --------------------------------- | --------------------------------------------------------------------------- |
| `HOST`                           | `0.0.0.0`                         | Address the API listens on                                                  |
| `PORT`                           | `8080`                            | Port the API listens on                                                     |
| `GREENBONE_SOCKET_PATH`          | `/run/gvmd/gvmd.sock`             | Path to the `gvmd` Unix socket                                              |
| `GREENBONE_USER`                 | `admin`                           | GVM user                                                                    |
| `GREENBONE_PASSWORD`             | `admin`                           | Password of the GVM user (development mode only)                            |
| `GREENBONE_PASSWORD_FILE`        | `/run/secrets/greenbone_password` | File containing the GVM password (production mode only)                     |
| `API_KEY`                        | `1234567890123456789`             | API key for clients (development mode only)                                 |
| `API_KEY_FILE`                   | `/run/secrets/api_key`            | File containing the API key (production mode only)                          |
| `LOG_LEVEL`                      | `INFO`                            | One of `critical`, `error`, `warning`, `info`, `debug`, `notset` (any case) |
| `FEEDS_METRICS_INTERVAL_SECONDS` | `60`                              | How often the feed metrics are refreshed                                    |

## Metrics

| Metric             | Labels                   | Description                                                            |
| ------------------ | ------------------------ | ---------------------------------------------------------------------- |
| `gvm_feed_version` | `feed_name`, `feed_type` | Version of a GVM feed as Unix timestamp; `0` if it could not be parsed |

The values are refreshed in the background every `FEEDS_METRICS_INTERVAL_SECONDS`. If an update
fails, the last values are kept.

## Development

### Installing Dependencies

The `vscan-controller` command as well as the development dependencies can be install using `pip`

```sh
pip install -e . --group dev
```

### Project layout

```
src/vscan_controller/
├── __main__.py   # entry point: logging setup, GMP connection, uvicorn
├── config.py     # configuration from environment / secret files
├── metrics.py    # Prometheus metrics (background thread)
├── gvm_tools/    # thin wrappers around python-gvm GMP calls
├── models/       # pydantic(-xml) models for GMP responses and API payloads
├── routers/      # FastAPI routers, authentication, shared responses
└── utils/        # structlog processors
tests/            # pytest tests with sample GMP XML responses in tests/files/
```

### Development environment with Docker Compose

`compose.yml` starts the controller in development mode together with an OpenVAS/GVM container
([immauss/openvas](https://github.com/immauss/openvas)). Both share the `gvmd` socket through a volume.

```sh
cp example.env .env   # then adjust the values
docker compose up --build
```

The API is available at `http://localhost:8080`
The GVM web interface is available at `http://localhost:9392`.

### Tests

The tests are found inside the `tests` directory and are written using `pytest`

```sh
pytest
```

### Code Style

Linting and formatting are done by [ruff](https://docs.astral.sh/ruff/)

```sh
ruff check .
ruff format .
```

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE).
