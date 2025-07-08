
# Celio
**Multilingual E-Cards for Celiac Disease**

*A comprehensive demo web application showcasing modern full-stack development, designed to become a mobile app later in 2025.*

Medium Blog: https://raphealsuber.medium.com/836e1eca60dc


![Screenshot 2025-07-08 171654](https://github.com/user-attachments/assets/cd50adff-cf62-4a41-bb46-fbccbfe685f5)




## Overview

Celio is a demo web application that empowers people with celiac disease and gluten sensitivities to safely communicate their dietary needs while traveling internationally. The platform enables users to create personalized emergency medical cards with crucial information translated into multiple languages including English, Spanish, French, Chinese, Japanese, and Portuguese.

**This is currently a demonstration web application built to showcase full-stack development capabilities, with plans to transition to a native mobile app later in 2025.**

**[Live Demo Coming Soon]**

## Key Features

### Core Functionality
- **Multilingual Emergency Cards**: Create personalized medical cards with translations in 6+ languages
- **Travel Guides**: Country-specific guides with celiac awareness information and dining tips
- **Sage AI Assistant**: AI-powered travel assistant for celiac-friendly recommendations
- **Restaurant Phrase Cards**: Essential phrases for communicating dietary needs abroad

### Technical Features
- **Responsive Design**: Mobile-first approach optimized for travelers
- **Modern UI/UX**: Glassmorphic design with smooth animations using TailwindCSS
- **Interactive Elements**: Dynamic form handling with HTMX for seamless user experience
- **User Authentication**: Complete account management with personalized profiles
- **Theme System**: Multiple card themes (Modern, Minimal, Classic) with dynamic color schemes

## Technical Stack

- **Backend**: Django 5.1.5, Python 3.13
- **Frontend**: TailwindCSS, HTMX for dynamic interactions
- **Database**: SQLite (demo) / PostgreSQL (production ready)
- **Styling**: Custom CSS with CSS variables for theming
- **PDF Generation**: ReportLab for downloadable emergency cards
- **Mobile Optimization**: Progressive Web App features for mobile experience
- **AI Integration**: Prepared for AI assistant functionality

## Development Approach

This demo showcases modern full-stack development practices:

- **Modular Architecture**: Clean separation with dedicated apps (accounts, message_cards, travel, sage)
- **Modern Django Patterns**: Class-based views, custom template tags, and middleware
- **Component-Based UI**: Reusable components with consistent theming
- **Mobile-First Design**: Responsive layouts optimized for travel scenarios
- **Scalable Structure**: Built to transition seamlessly to mobile app architecture

## Screenshots

Card Creation <!![Screenshot 2025-07-08 122132](https://github.com/user-attachments/assets/f9b40d65-963e-4f2f-bb5d-890899e985d6) ![Screenshot 2025-07-08 122153](https://github.com/user-attachments/assets/826eda6b-dc70-4177-960d-94ee642d05b0)
![Screenshot 2025-07-08 122036](https://github.com/user-attachments/assets/e455ec33-b439-4551-b406-ebd869028805)![Screenshot 2025-07-08 122102](https://github.com/user-attachments/assets/85a6ca89-b575-409a-837b-25eeeaecc8c4)


  />

 

Travel Guides<img width="1374" alt="Screenshot 2025-03-29 at 8 23 43 PM" src="https://github.com/user-attachments/assets/213e5308-44f7-4e8c-af10-4a480c64eb30" />


Sage Assistant<![Screenshot 2025-07-08 122309](https://github.com/user-attachments/assets/c59dc3f3-c1e2-4fbb-a4b9-2a09c7a310ed)/>




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

### Technical Skills
- **Full-Stack Development**: Complete Django web application with modern frontend
- **UI/UX Design**: Custom theming system with glassmorphic design principles
- **Database Design**: Efficient models for multilingual content and user management
- **Responsive Development**: Mobile-optimized interface for real-world travel use
- **Code Organization**: Clean, maintainable architecture ready for team collaboration

### Problem-Solving Approach
- **User-Centered Design**: Addressing real needs of celiac travelers
- **Accessibility**: Clear communication tools for language barriers
- **Scalability**: Architecture designed for future mobile app transition

## Roadmap

### 2025 Mobile App Transition
- **Native Mobile Development**: iOS and Android apps with offline functionality
- **Enhanced AI Features**: Advanced restaurant recommendations and real-time translation
- **Geolocation Integration**: Location-based restaurant and pharmacy finder
- **Community Features**: User reviews and crowdsourced safety information

### Current Demo Features
- ✅ Multilingual emergency cards
- ✅ Travel guides with country-specific information
- ✅ Modern responsive design
- ✅ User authentication and profiles
- ✅ PDF generation for offline use

## Project Goals

Celio demonstrates the complete development lifecycle from concept to deployment, showcasing:

- **Real-World Problem Solving**: Addressing genuine challenges faced by celiac travelers
- **Modern Development Practices**: Clean code, responsive design, and user-centered approach
- **Scalable Architecture**: Built with future mobile app development in mind
- **Technical Excellence**: Demonstrating proficiency in full-stack web development

## About the Developer

This project represents a comprehensive approach to solving real-world problems through technology. Created to demonstrate full-stack development capabilities while building something genuinely useful for the celiac community.

## Connect

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/raphealsuber/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/yourusername)

---

*This demo web application serves as a foundation for the upcoming mobile app launch in 2025, demonstrating both technical capabilities and commitment to solving real-world accessibility challenges.*
