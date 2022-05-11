FROM mysql

MAINTAINER root

ENV MYSQL_ROOT_PASSWORD 9477
COPY dump.sql /docker-entrypoint-initdb.d

EXPOSE 3306
