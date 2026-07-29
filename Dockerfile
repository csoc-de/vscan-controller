FROM python:3.14.6-alpine3.23

ARG VERSION="nothing"
ARG COMMIT="nothing"
ARG BUILD_AT="nothing"

RUN apk add make build-base bash curl htop tmux
RUN apk add --no-cache python3-dev libffi-dev gcc musl-dev make

COPY . /app
RUN chmod +x /app/entrypoint.sh

#RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#RUN chown -R appuser:appgroup /app

RUN mkdir -p /var/log/csoc-vscan
RUN mkdir -p /data
RUN mkdir -p /import

#USER appuser

WORKDIR /app

RUN echo "VERSION = ${VERSION}" > build_info.py
RUN echo "COMMIT = ${COMMIT}" >> build_info.py
RUN echo "BUILD_AT = ${BUILD_AT}" >> build_info.py

RUN pip3 install --upgrade pip --no-warn-script-location
RUN pip3 install -r /app/requirements.txt --no-warn-script-location --no-cache-dir

CMD ["./entrypoint.sh"]
