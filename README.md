
# Celio: Multilingual Emergency Cards for Celiac Disease

Medium Blog: https://raphealsuber.medium.com/836e1eca60dc


<img width="369" alt="Screenshot 2025-03-27 at 11 43 25 PM" src="https://github.com/user-attachments/assets/18abc19a-7b71-4b2e-a7f9-6f9ade307148" />



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

Card Creation <img width="1401" alt="Screenshot 2025-03-29 at 8 21 12 PM" src="https://github.com/user-attachments/assets/353dd83d-8f9b-4cb7-b364-2280534b9403" />
 

Travel Guides<img width="1374" alt="Screenshot 2025-03-29 at 8 23 43 PM" src="https://github.com/user-attachments/assets/213e5308-44f7-4e8c-af10-4a480c64eb30" />


Sage Assistant<img width="1403" alt="Screenshot 2025-03-29 at 8 22 42 PM" src="https://github.com/user-attachments/assets/da1a40d8-ea6d-487a-91d6-560c2852dc24" />



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


## Connect
[LinkedIn](https://linkedin.com/in/raphealsuber/) 
