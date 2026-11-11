## Setup Development Environment

1. copy `example.env` with the name `.env` and update the vars in `.env` file
2. use `make restart`

## Make File Commands

`̀make down` - docker compose down + delete of socket files  
`make up` - docker compose up  
`make restart` - make down + make up

## OpenAPI Spec

1. setup development environment
2. run `main.py`
3. go with the browser to `http://{.env:HOST}:{.env:PORT}/docs` (default: `http://localhost:8085/docs`)

