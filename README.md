# Hotel API
This project implements a RESTful API for managing hotel information using Django and Django REST Framework.

## Project Structure
- Hotel model with fields for id, name, address, rating, price, and availability
- REST API endpoints for listing, creating, and retrieving hotel information
- Serializers for converting between Python objects and JSON data

## API Endpoints

Collecting workspace information# Hotel API

This project implements a RESTful API for managing hotel information using Django and Django REST Framework.

## Project Structure

The project contains a Django application called hotelapi that provides endpoints for managing hotel data. The main components include:

- `Hotel` model with fields for id, name, address, rating, price, and availability
- REST API endpoints for listing, creating, and retrieving hotel information
- Serializers for converting between Python objects and JSON data

## API Endpoints

The following endpoints are available:

- `GET /hotel_list/`: List all hotels
- `POST /hotel_list/`: Create a new hotel
- `GET /hotel_list/<id>`: Get details for a specific hotel
- `GET /generics_hotel_list/`: List all hotels (alternative implementation using generic views)
- `POST /generics_hotel_list/`: Create a new hotel (alternative implementation)
- `POST /reservation/`: Create a new reservation
- `GET /available_hotels/`: Get list of available hotels for specified dates

## Hotel Data Model

Each hotel record contains:
- `id`: Integer (primary key)
- `name`: String (max length 100)
- `address`: Text
- `rating`: Decimal (format x.x, max 5.0)
- `price`: Integer
- `available_until`: Date
- `available`: Boolean (can be null)

## Technology Stack

- Django 5.2
- Django REST Framework
- SQLite database
- python-dotenv for environment variable management

## Setup and Deployment

### Local Development

1. Clone the repository:
   ```
   git clone <repository-url>
   cd testproj
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```

4. Edit the `.env` file with your configuration:
   - Generate a new Django secret key
   - Set DEBUG=True for development
   - Configure ALLOWED_HOSTS
   - Set database configuration if needed

5. Run migrations and start the development server:
   ```
   python manage.py migrate
   python manage.py runserver
   ```

### Production Deployment

1. Set up a proper production database (PostgreSQL recommended)
2. Update the `.env` file with production settings:
   - Set DEBUG=False
   - Add your domain to ALLOWED_HOSTS
   - Configure production database settings
   - Generate a strong SECRET_KEY

3. Configure a proper web server (Nginx/Apache) with WSGI (Gunicorn/uWSGI)
4. Set up static files serving
5. Implement HTTPS with a valid SSL certificate

## Environment Variables

This project uses environment variables for configuration. The following variables can be set in the `.env` file:

- `SECRET_KEY`: Django secret key (required)
- `DEBUG`: Set to 'True' for development, 'False' for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_ENGINE`: Django database engine
- `DATABASE_NAME`: Database name
- `TIME_ZONE`: Application time zone
- `LANGUAGE_CODE`: Application language code

### Security Settings

For production deployments, the following security settings can be configured in your `.env` file:

- `SECURE_SSL_REDIRECT`: Set to 'True' to enforce HTTPS
- `SESSION_COOKIE_SECURE`: Set to 'True' to ensure cookies are only sent over HTTPS
- `CSRF_COOKIE_SECURE`: Set to 'True' to ensure CSRF cookies are only sent over HTTPS
- `SECURE_HSTS_SECONDS`: Set to a value like 31536000 (1 year) to enable HTTP Strict Transport Security
- `SECURE_HSTS_INCLUDE_SUBDOMAINS`: Set to 'True' to include subdomains in HSTS
- `SECURE_HSTS_PRELOAD`: Set to 'True' to allow preloading of HSTS header

## Authentication

The API currently uses `AllowAny` permission class for demonstration purposes. For production, it is strongly recommended to:

1. Configure Django REST Framework authentication (JWT, OAuth, etc.)
2. Replace the `AllowAny` permission class with `IsAuthenticated` to secure all endpoints
3. Implement proper user management and authentication
