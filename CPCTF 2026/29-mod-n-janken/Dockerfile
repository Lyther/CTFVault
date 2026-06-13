FROM python:3.11-slim AS base
WORKDIR /app

COPY server.py run

FROM pwn.red/jail
COPY --from=base / /srv
RUN chmod +x /srv/app/run

ENV JAIL_TIME=3600 JAIL_MEM=32M