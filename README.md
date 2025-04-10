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

## Hotel Data Model

Each hotel record contains:
- `id`: Integer (primary key)
- `name`: String (max length 100)
- `address`: Text
- `rating`: Decimal (format x.x, max 5.0)
- `price`: Integer
- `available`: Boolean (can be null)

## Technology Stack

- Django 5.2
- Django REST Framework
- SQLite database
