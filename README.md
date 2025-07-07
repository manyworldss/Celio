
# Celio

## Dynamic Country-Specific Card Colors

This project now supports dynamic country-specific card colors for the travel guide list. Each travel guide card uses a unique color defined in the `Country` model's `color` field.

### Features
- Dynamic background colors for travel guide cards based on country.
- Custom Django template filter `darken` to create darker shades for button styling.
- Database migration added to include the `color` field in the `Country` model.

### Usage
- The `color` field in the `Country` model stores the hex color code.
- The `darken` template filter is used in templates to adjust button colors dynamically.

### Implementation Details
- The color darkening uses HSV color space for natural color adjustments.
- The feature enhances the visual distinction of travel guides by country.

For more details, see the travel app's `templatetags/travel_filters.py` and the `travel_guide_list.html` template.

: Multilingual Emergency Cards for Celiac Disease

Medium Blog: https://raphealsuber.medium.com/836e1eca60dc


<img width="369" alt="Screenshot 2025-03-27 at 11 43 25 PM" src="https://github.com/user-attachments/assets/18abc19a-7b71-4b2e-a7f9-6f9ade307148" />



## Overview

Celio is a web application that helps people with celiac disease and gluten sensitivities safely communicate their dietary needs in multiple languages while traveling. Users can create personalized emergency medical cards that translate crucial medical information into six languages: English, Spanish, French, Chinese, Japanese, and Portuguese.

**[Live Demo(Coming soon)**

## Key Features

- **Multilingual Emergency Cards**: Create and view cards in multiple languages
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Modern UI/UX**: Clean, intuitive interface built with TailwindCSS
- **Interactive Elements**: Dynamic form handling with HTMX
- **User Authentication**: Complete user account management system

## Technical Stack

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

Card Creation <img width="1401" alt="Screenshot 2025-03-29 at 8 21 12 PM" src="https://github.com/user-attachments/assets/353dd83d-8f9b-4cb7-b364-2280534b9403" />
 

Travel Guides<img width="1374" alt="Screenshot 2025-03-29 at 8 23 43 PM" src="https://github.com/user-attachments/assets/213e5308-44f7-4e8c-af10-4a480c64eb30" />


Sage Assistant<img width="1403" alt="Screenshot 2025-03-29 at 8 22 42 PM" src="https://github.com/user-attachments/assets/da1a40d8-ea6d-487a-91d6-560c2852dc24" />



## Installation and Setup

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
