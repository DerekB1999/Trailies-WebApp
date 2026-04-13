# Trailies

Trailies is a web-application that allows users to discover, review, and manage hiking trails.
I made this app with the intent of it being used by students at UMASS Amherst, therefore it mainly contains trails near the university.
This app was built as a full-stack project to show dynamic frontend rendering, backend architecture, and database design. This application also uses containers with Docker, making it easy to run across different environments.

## Backend
- FastAPI
- SQLModel/SQLAlchemy
- PostgreSQL
- Python

## Frontend
- HTML
- CSS
- Jinja2 Templates
- HTMX

## Features:

### Authentication And Authorization
- User signup and login
- Password hashing
- JWT-based authentication using secure cookies
- Role-based authorization(admin and users)

### Trail Management
- Admin users can add new trails
- Admin users can delete trails
- Trails are stored with a location and difficulty, along with other information

### Reviews
- Users can review trails
- Dynamic UI updates using HTMX

### Purpose of this project:
This project was built to demonstrate full-stack engineering skills, such as:
- Designing relational database schemas
- Building RESTful backend systems
- Implementing authentication and authorization
- Dynamic frontend rendering using HTMX

## Setup
  1. Clone the repo
  2. Create a .env file in the root directory and add in it:
    SECRET_KEY=add_any_secret_key_here
  3. Run with Docker:
    - First time running this: docker compose up --build
    - Afterwards can just run: docker compose up
  4. Open a browser and go to: http://localhost:8000

## Video showing how the app works
  ![Demo](/videos_and_images/Trailies_Demo.mov)

## Screenshots showing admin view
  - Delete and add trail buttons:
    ![](/videos_and_images/Delete_Add_Trail_Buttons.png)
  - Add trail page:
    ![](/videos_and_images/Add_Trail_Page1.png)
    ![](/videos_and_images/Add_Trail_Page2.png)