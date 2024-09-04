#!/bin/sh

# Wait for the PostgreSQL and MongoDB services to be ready
/usr/local/bin/wait-for-it.sh flask_db:5432 -- /usr/local/bin/wait-for-it.sh flask_mongo:27017 -- "$@"
