
# Celio: Multilingual Emergency Cards for Celiac Disease

![Celio Logo](Coming soon)

## Overview

Celio is a web application that helps people with celiac disease and gluten sensitivities safely communicate their dietary needs in multiple languages while traveling. Users can create personalized emergency medical cards that translate crucial medical information into six languages: English, Spanish, French, Chinese, Japanese, and Portuguese.

**[Live Demo(Coming soon)**

## Key Features

- **Multilingual Emergency Cards**: Create one card, access it in six languages
- **QR Code Sharing**: Easy sharing of cards with restaurants and medical staff
- **Printable Cards**: Download as PDF for offline use
- **Travel Guides**: Country-specific dining tips and phrases (Premium)
- **Sage AI Assistant**: Get personalized gluten-free advice powered by Claude AI (Premium)

## Technical Highlights

- **Backend**: Django 5.1.5, Python 3.13
- **Frontend**: TailwindCSS, HTMX for dynamic UI without complex JavaScript
- **Database**: PostgreSQL with JSONField for translations
- **PDF Generation**: ReportLab for creating downloadable emergency cards
- **QR Codes**: Dynamic generation of shareable card links
- **Responsive Design**: Mobile-first approach for travelers on the go

## Development Approach

This project follows modern Django best practices:

- Modular app structure with clear separation of concerns
- Class-based views and form handling
- REST API endpoints for subscription management
- Custom middleware for premium content access control
- Interactive onboarding experience for new users

## Screenshots

![Card Creation](path/to/screenshot1.png)
![Language Switching](path/to/screenshot2.png)
![Travel Guides](path/to/screenshot3.png)

## Installation and Setup

```bash
# Clone repository
git clone https://github.com/yourusername/celio.git
cd celio

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Run the development server
python manage.py runserver
```

## Future Enhancements

- Mobile apps for iOS and Android
- Additional languages and country guides
- Integration with restaurant recommendation APIs
- Offline functionality for areas with limited connectivity

## About This Project

Celio was developed as a capstone project demonstrating full-stack development skills with Django. It showcases my ability to build practical, user-centered web applications that solve real-world problems.

---


Licensed under MIT © 2025

## Connect
[LinkedIn](https://linkedin.com/in/raphealsuber/) 
