# Fiverr Clone Backend

This repository contains the backend for a Fiverr-like marketplace platform built using Django. It provides RESTful APIs to manage offers, orders, user profiles, and transactions, enabling business users to post services and customers to order them.

## Features

* Dual user roles: Business users can create and manage service offerings, while customers can browse and purchase services
* Complete offer management with CRUD operations for business users
* Order processing system with status tracking and notifications
* User authentication and authorization with role-based permissions
* Profile management for both customer and business users
* Secure payment processing integration
* Review and rating system
* Search and filtering capabilities
* Scalable and modular codebase

## Prerequisites

Before you begin, ensure you have the following installed:

* Python 3.8 or higher
* pip (Python package manager)
* Git (optional, for version control)

## Installation

Follow these steps to set up the project locally:

1. Clone the repository:
```
git clone https://github.com/Hakobyan1994/Coderr-Backend.git
cd fiverr-clone-backend
```

2. Create a virtual environment:
```
python -m venv env
source env/bin/activate  # On Windows, use "env\Scripts\activate"
```

3. Install dependencies:
```
pip install -r requirements.txt
```

5. Run migrations:
```
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser (admin) optional:
```
python manage.py createsuperuser
```

7. Run the development server:
```
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/registration/` - Register a new user
- `POST /api/login/` - Login and authenticate

### Profile
- `GET /api/profile/{pk}/` - Get profile details by ID
- `PATCH /api/profile/{pk}/` - Update profile details
- `GET /api/profiles/business/` - List all business profiles
- `GET /api/profiles/customer/` - List all customer profiles

### Offers
- `GET /api/offers/` - List all offers
- `POST /api/offers/` - Create a new offer
- `GET /api/offers/{id}/` - Get offer details
- `PATCH /api/offers/{id}/` - Update an offer
- `DELETE /api/offers/{id}/` - Delete an offer
- `GET /api/offerdetails/{id}/` - Get detailed information about an offer

### Orders
- `GET /api/orders/` - List all orders
- `POST /api/orders/` - Create a new order
- `PATCH /api/orders/{id}/` - Update an order
- `DELETE /api/orders/{id}/` - Delete an order
- `GET /api/order-count/{business_user_id}/` - Get count of orders for a business user
- `GET /api/completed-order-count/{business_user_id}/` - Get count of completed orders for a business user

### Reviews
- `GET /api/reviews/` - List all reviews
- `POST /api/reviews/` - Create a new review
- `PATCH /api/reviews/{id}/` - Update a review
- `DELETE /api/reviews/{id}/` - Delete a review

### General Endpoints
- `GET /api/base-info/` - Get aggregated base information