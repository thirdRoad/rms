#!/bin/sh

echo "Running database migrations (upgrade)..."
flask db upgrade

echo "Create a base roles"
flask seed-db-roles

echo "Create a base users"
flask seed-db-users

exec "$@"