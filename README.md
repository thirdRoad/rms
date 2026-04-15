# Tech Stack
1. [x] Framework: Flask
2. [x] Package Management: Poetry
3. [x] Database: PostgreSQL
4. [x] ORM/Migration: SQLAlchemy / Flask-Migrate
5. [x] Architecture: Application Factory & Modular Blueprints (Domains)

# Requirements
- **Python 3.12+**
- **Poetry**
- **Docker**

# Usage

## With Docker

### Build a image
- First you create a .env file.
- We have a template for .env file. `/restaurant-management-system-flask/.env.template`

```bash
cp .env.template .env
```

- Then create an image.

```bash
docker compose -f dev-compose.yml build
```

### Up the image
- Detach Mode ( release the terminal )
```bash
docker compose -f dev-compose.yml up -d
```

## CLI
Python File -> `/restaurant-management-system-flask/app.py`

### Commands
- `init-db` - Creates tables without being tied to anything.
- `seed-db-roles` - Creates a base roles.
- `seed-db-users` - Create an Admin user.

### Flask Commands
Doc Link - https://flask.palletsprojects.com/en/stable/cli/