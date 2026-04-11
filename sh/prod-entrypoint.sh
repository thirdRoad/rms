#!/bin/sh

echo "Running database init..."
flask init-db

echo "Create a base roles"
flask seed-db-roles

echo "Create a base users"
flask seed-db-users

exec "$@"