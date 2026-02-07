# Advanced Databases (NoSQL) Final Project: Clothing Store

Full-stack E-commerce web application

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/license/mit/)

## Key Features
- User Authentication: Secure authentication using JWT and Argon2 hashing.
- Product Catalog: Filtering by category and price range.
- Shopping Cart: Persistent cart management.
- Admin Dashboard: Aggregated statistics for total revenue and order counts.
- Reviews System: Users can rate and review products.

## Architecture

The project follows a Client-Server Architecture implemented within a unified FastAPI framework.

| Component | Technology |
|-----------|------------|
| Language | [Python](python.org) |
| Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| Database | [MongoDB](https://www.mongodb.com/) via [Beanie](https://beanie-odm.dev/) |
| Frontend | [Jinja2](https://jinja.palletsprojects.com/), [Bootstrap](https://getbootstrap.com/), [Swagger UI](https://swagger.io/tools/swagger-ui/) |
| Package Manager | [uv](https://docs.astral.sh/uv/) |

## Installation

clone repository

```sh
git clone https://github.com/pythonsogood/dbms-nosql
cd dbms-nosql
```

install [uv](https://docs.astral.sh/uv/getting-started/installation/)

install dependencies

```sh
uv sync
```

configure .env

```sh
MONGODB_CONNECTION="mongodb://localhost:27017"
MONGODB_DATABASE="database_name"
JWT_SECRET_KEY="your_secret_key"
```

## Usage

run `main.py`

```sh
uv run main.py
```

go to:
- Web App: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`