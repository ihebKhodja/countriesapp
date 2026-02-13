# CountriesApp

A Django web application for listing, searching, and viewing statistics about countries, with Docker support and automated data import.

## Features
- List countries with pagination, region filter, and search
- Country detail view
- Statistics page (population, area, region stats)
- Data import from REST Countries API
- Management commands and unit tests
- Dockerized for easy deployment

## Installation

### Prerequisites
- Docker & Docker Compose
- (Optional) Python 3.12+ and pip for local development

### Clone the repository
```
git clone https://github.com/ihebKhodja/countriesapp.git
cd countriesapp
```

### Environment setup
- All environment variables are in `.env` (already present)
- No manual editing needed unless you want to change DB or API settings

### Build and start with Docker
```
make build   # Build Docker images
make up      # Start containers in background
make run     # Start containers interactively
```

### Run migrations and import countries
```
make migrate           # Apply database migrations
make import_countries  # Import country data from API
```

### Run tests
```
make test              # Run unit tests
make coverage          # Run tests with coverage report
```

## Useful Commands
- `make shell` : Open Django shell in Docker
- `make makemigrations` : Create new migrations
- `make down` : Stop and remove containers

## URLs
- Home/List:        `/countries/` or `/`
- Country detail:   `/countries/<cca3>/` (ex: `/countries/FRA/`)
- Statistics:       `/stats/`

## Management Commands
- `python manage.py import_countries` : Import/update countries from API

## Notes
- Data is imported automatically on container start (see entrypoint.sh)
- All tests and coverage run inside Docker
- To customize API source, edit `.env` or use `--url` option with the management command

## License
MIT
