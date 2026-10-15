FROM python:3.15.0-alpine3.23

ARG VERSION="nothing"
ARG COMMIT="nothing"
ARG BUILD_AT="nothing"

WORKDIR /app
COPY . .

RUN chmod +x ./entrypoint.sh

RUN echo "VERSION = ${VERSION}" > build_info.py
RUN echo "COMMIT = ${COMMIT}" >> build_info.py
RUN echo "BUILD_AT = ${BUILD_AT}" >> build_info.py

RUN pip3 install --upgrade pip --no-warn-script-location
RUN pip3 install -r ./requirements.txt --no-warn-script-location --no-cache-dir

CMD ["/bin/sh", "entrypoint.sh"]
