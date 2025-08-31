# ALX Travel App 🏠✈️

A comprehensive real estate and travel booking platform built with Django REST Framework, designed to connect property owners with travelers seeking accommodations.

## 🚀 Features

### Core Functionality
- **Property Listings**: Browse and search available properties
- **User Management**: Multi-role system (Admin, User, Realtor)
- **Address Management**: Comprehensive location tracking
- **Review System**: Property ratings and feedback
- **Booking System**: Reservation management
- **Payment Integration**: Secure payment processing
- **Asynchronous Tasks:** Using Celery with RabbitMQ to handle background tasks like sending confirmation emails.
- **Django Chapa Payment Gateway Integration** Connecting a Django backend to the Chapa API for payment processing.

### User Roles
- **Admin**: Full system access and management
- **Realtor**: Property listing and management
- **User**: Browse, book, and review properties

## 🏗️ Architecture

### Apps Structure
```
alx_travel_app/
├── alx_travel_app/     # Main Django project
├── users/             # User management & authentication
├── addresses/         # Location & address handling
├── listings/          # Property listings & search
├── reviews/           # Rating & review system
├── bookings/          # Reservation management
└── payments/          # Payment processing
```

### Database Models
- **User**: Authentication, roles, profiles
- **Address**: Location data with status tracking
- **Listing**: Property details, pricing, availability
- **Review**: Ratings, comments, user feedback
- **Booking**: Reservation details and status
- **Payment**: Transaction records and processing

## 🛠️ Technology Stack

- **Backend**: Django 5.2.4 + Django REST Framework
- **Database**: SQLite (development) / MySQL (production)
- **Authentication**: Django built-in auth system
- **API Documentation**: drf-yasg (Swagger/OpenAPI)
- **Task Queue**: Celery with Redis
- **Environment**: django-environ for configuration
- **Data Seeding**: Faker for realistic test data

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git
- Virtual environment (recommended)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/chinazagideon/alx_travel_app_0x00.git
cd alx_travel_app_0x00/alx_travel_app
```

### 2. Set Up Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r alx_travel_app/requirement.txt
```

### 4. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Seed Sample Data
```bash
python manage.py seed
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# API Keys
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
```

## 📚 API Documentation

### Available Endpoints
- **Users**: `/api/users/` - User management
- **Addresses**: `/api/addresses/` - Location data
- **Listings**: `/api/listings/` - Property listings
- **Reviews**: `/api/reviews/` - Property reviews
- **Bookings**: `/api/bookings/` - Reservation management
- **Payments**: `/api/payments/` - Payment processing

### API Documentation
Access interactive API documentation at:
- Swagger UI: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`

## 🗄️ Database Schema

### Key Relationships
- Users can have multiple addresses
- Listings belong to users and have addresses
- Reviews are linked to listings and reviewers
- Bookings connect users to listings
- Payments are associated with bookings

### Sample Data
The seeder creates:
- 10 users with different roles
- 10 addresses across various cities
- 10 property listings with realistic data
- 10 reviews with ratings and comments

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
python manage.py test listings
```

## 📦 Management Commands

### Data Seeding
```bash
python manage.py seed  # Creates sample data for all entities
```

### Database Operations
```bash
python manage.py makemigrations  # Create migrations
python manage.py migrate         # Apply migrations
python manage.py createsuperuser # Create admin user
```

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure production database (MySQL/PostgreSQL)
- [ ] Set up static file serving
- [ ] Configure email settings
- [ ] Set up SSL/HTTPS
- [ ] Configure environment variables
- [ ] Set up monitoring and logging

### Docker Support
```bash
# Build and run with Docker (if Dockerfile exists)
docker build -t alx-travel-app .
docker run -p 8000:8000 alx-travel-app
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is part of the ALX Software Engineering program.

## 👥 Authors

- **Chinaza Gideon** - *Initial work* - [chinazagideon](https://github.com/chinazagideon)

## 🙏 Acknowledgments

- ALX Software Engineering Program
- Django and Django REST Framework communities
- All contributors and reviewers

---

**Note**: This is a learning project developed as part of the ALX Software Engineering curriculum. For production use, additional security measures and optimizations should be implemented.
