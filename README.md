# Advanced Restaurant Management System

A production-style restaurant management system built using Django,
Django REST Framework and PostgreSQL.

## Technology Stack

- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- React.js
- REST API
- Swagger/OpenAPI

## Main Modules

- Authentication
- Restaurant Management
- Menu Management
- Table Management
- Reservations
- Orders
- Kitchen Management
- Inventory
- Payments
- Reports
- Admin Dashboard

## How to Run the System

### 1. Backend (Django REST Framework)
To run the backend server:

1. Open a new terminal.
2. Activate your virtual environment (if not already active):
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
3. Navigate to the `backend` directory: `cd backend`
4. Apply any pending database migrations: `python manage.py migrate`
5. Start the development server: `python manage.py runserver`

The backend will start at `http://127.0.0.1:8000/`.
You can view the Swagger API Documentation at `http://127.0.0.1:8000/api/schema/swagger-ui/`.

### 2. Frontend (React + Vite)
To run the frontend React application:

1. Open a **second** terminal (leave the backend running in the first).
2. Navigate to the `frontend` directory: `cd frontend`
3. Install the dependencies (if you haven't already): `npm install`
4. Start the Vite development server: `npm run dev`

The frontend will start at `http://localhost:5173/`.