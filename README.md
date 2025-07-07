
# Celio
**Multilingual Emergency Cards for Celiac Disease**

*A comprehensive demo web application showcasing modern full-stack development, designed to become a mobile app later in 2025.*

Medium Blog: https://raphealsuber.medium.com/836e1eca60dc


<img width="369" alt="Screenshot 2025-03-27 at 11 43 25 PM" src="https://github.com/user-attachments/assets/18abc19a-7b71-4b2e-a7f9-6f9ade307148" />



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
