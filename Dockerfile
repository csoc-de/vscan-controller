FROM python:3.15.2-alpine3.23

ARG VERSION="<version>"
ARG COMMIT="<commit>"
ARG BUILD_AT="<built_at>"

WORKDIR /data
COPY . .

RUN chmod +x ./entrypoint.sh

RUN printf 'VERSION = "%s"\nCOMMIT = "%s"\nBUILD_AT = "%s"\n' \
    "${VERSION}" "${COMMIT}" "${BUILD_AT}" > ./src/vscan_controller/build_info.py

RUN pip3 install --upgrade pip --no-warn-script-location
RUN pip3 install . --no-warn-script-location --no-cache-dir

CMD ["/bin/sh", "entrypoint.sh"]
