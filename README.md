
# Gluten Free Emergency Card - Demo

> A demo web application showcasing full-stack development skills with Django and modern web technologies.

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![HTMX](https://img.shields.io/badge/HTMX-48A1D9?style=for-the-badge&logo=html5&logoColor=white)](https://htmx.org/)

## Overview

This is a demo application that allows users to create multilingual emergency cards for communicating dietary restrictions while traveling. The project demonstrates:

- Modern Django development practices
- Clean, responsive UI with Tailwind CSS
- Interactive features with HTMX
- Form handling and validation
- User authentication flows
- Responsive design principles

## Demo Features

- **Multilingual Emergency Cards**: Create and view cards in multiple languages
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Modern UI/UX**: Clean, intuitive interface built with TailwindCSS
- **Interactive Elements**: Dynamic form handling with HTMX
- **User Authentication**: Complete user account management system

## Technical Stack

- **Backend**: Django 5.1.5, Python 3.13
- **Frontend**: HTML5, TailwindCSS, HTMX
- **Database**: SQLite (for demo purposes)
- **Authentication**: Django's built-in auth system
- **Deployment**: Ready for platforms like Heroku or Railway

## Key Technical Achievements

- Implemented a unified card management system with real-time preview
- Created a responsive, mobile-first UI with TailwindCSS
- Used Django's template system with template inheritance for maintainable code
- Implemented form handling with client-side validation
- Set up a clean URL structure with proper namespacing

## Project Structure

```
celio/
├── accounts/           # User authentication and profiles
├── emergency_cards/    # Core emergency card functionality
├── static/             # Static files (CSS, JS, images)
├── templates/          # HTML templates
├── manage.py           # Django management script
└── requirements.txt    # Project dependencies
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/celio.git
cd celio

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up the database
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser to view the application.

## What This Demo Showcases

- Full-stack web development with Django
- Modern frontend development with TailwindCSS
- Responsive design principles
- Form handling and validation
- User authentication flows
- Clean code organization

## Future Enhancements

- Add more language options
- Implement PDF generation for printable cards
- Add QR code functionality
- Integrate with translation APIs

## About the Developer

This demo was created to showcase my skills in full-stack web development. I'm passionate about building applications that solve real-world problems with clean, maintainable code.

## Connect

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/raphealsuber/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/yourusername)
