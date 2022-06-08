FROM postgres
ENV POSTGRES_PASSWORD npd
ENV POSTGRES_DB npd
COPY dump.sql /docker-entrypoint-initdb.d/
