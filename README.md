
# Celio - https://celioapp.up.railway.app/

**Multilingual E-Cards for Celiac Disease**

![Screenshot 2025-07-08 171654](https://github.com/user-attachments/assets/b891d1ef-be56-4533-b480-76687eaa0cbb)

*A comprehensive demo web application showcasing modern full-stack development, designed to become a mobile app later in 2025.*



# Celio

Celio is an app I made because I needed something like it and couldn’t find it anywhere. I have celiac disease, and when I travel, it’s hard to explain what that means especially in a different language. It gets exhausting fast. Sometimes scary.

This tool creates a downloadable card that explains your condition in multiple languages so you can stay safe, eat with confidence, and not have to explain your whole medical history every time you sit down at a table.

---

### What it does

- Translates celiac safety info into 6+ languages
- Generates an emergency card you can save or print
- Doesn’t need an account or any login
- Works on your phone or laptop

---

### Why I built it

I wanted something that felt simple and reliable. No friction, no nonsense. Just a way to say what you need to say when it matters. This is for people who’ve had to Google-Translate their diagnosis and still felt misunderstood. I’ve been there.

---

### Architecture & Tech Stack

**Backend:**
- Django 5.0 with Django ORM for data management
- PostgreSQL database with JSONField for multilingual content storage
- Django REST Framework for API endpoints
- Custom translation engine with fallback phrase dictionaries
- Session-based demo mode for anonymous users

**Frontend:**
- HTMX for seamless, server-driven interactivity
- Alpine.js for lightweight client-side enhancements
- Tailwind CSS for responsive, accessible styling
- Mobile-first responsive design
- Progressive enhancement with graceful degradation

**Infrastructure:**
- Docker containerization for consistent deployment
- Railway.app for cloud hosting and CI/CD
- Static file optimization with WhiteNoise
- QR code generation for card sharing

---

### How it works

The application follows a modern web architecture pattern combining server-side rendering with progressive enhancement:

1. **Dynamic Card Creation**: Users input their medical condition and personal details
2. **Real-time Translation**: Custom translation engine converts medical information into 11+ languages
3. **Live Preview**: HTMX enables instant updates without page refreshes
4. **Theme Customization**: Multiple visual themes (Teal, Light, Dark, Purple) with CSS custom properties
5. **Export Options**: Cards can be downloaded as HTML, PDF, or shared via QR codes
6. **Accessibility First**: WCAG 2.1 AA compliant with keyboard navigation and screen reader support

---

### Technical Challenges Solved

**Multilingual Translation System:**
- Built a custom translation engine supporting 11 languages without external APIs
- Implemented phrase-based translation with intelligent fallbacks
- Handled medical terminology accuracy across cultural contexts

**Real-time Preview System:**
- Integrated HTMX for seamless form updates without JavaScript complexity
- Managed complex state synchronization between form inputs and card preview
- Optimized for mobile performance with minimal network requests

**Accessibility & UX:**
- Achieved WCAG 2.1 AA compliance through systematic testing
- Designed for users in stressful situations (travel, medical emergencies)
- Balanced feature richness with cognitive load reduction

**Session Management:**
- Implemented demo mode allowing full functionality without user accounts
- Built robust session recovery for interrupted card creation workflows
- Managed multilingual content persistence across user sessions

---

### What I learned

This project taught me a lot about edge cases, health tech, and designing for clarity under stress. I interviewed other celiac travelers and paid attention to what scared them the most. Celio is what came out of that.

Key technical insights:
- The importance of progressive enhancement in modern web development
- Balancing technical complexity with user experience simplicity
- The value of user research in understanding real-world usage patterns
- Building resilient systems that work offline and across different devices

---

### Try it out

[celioapp.up.railway.app](https://celioapp.up.railway.app)

---

### Development Process

This project represents a complete product development cycle:

**Research Phase:**
- Conducted interviews with celiac disease community members
- Analyzed existing solutions and identified gaps
- Defined user personas and journey maps for travel scenarios

**Design Phase:**
- Created wireframes and prototypes focusing on mobile-first design
- Iterated on information architecture for medical content clarity
- Designed accessible color schemes and typography for stress situations

**Development Phase:**
- Built with test-driven development principles
- Implemented continuous integration with automated deployment
- Regular user testing sessions to validate assumptions

**Launch & Iteration:**
- Deployed to production with monitoring and error tracking
- Gathered user feedback for continuous improvement
- Maintained codebase with regular security updates

---

### Built by

Rapheal Suber — UX Designer & Full-Stack Developer passionate about creating technology that addresses real human needs. Combining psychology background with technical expertise to build accessible, user-centered applications.

### Key Features for Portfolio Showcase

- **Multilingual Translation**: Instant translation of medical information into 11 languages
- **Live Preview**: Real-time card customization with HTMX-powered updates
- **Theme System**: 4 visually distinct themes (Celio, Light, Dark, Purple) for different preferences
- **Mobile-First Design**: Responsive interface optimized for phones and tablets
- **Accessibility**: WCAG 2.1 AA compliant with keyboard navigation and screen reader support
- **Export Options**: Download as HTML, PDF, or share via QR codes
- **Progressive Enhancement**: Works without JavaScript for core functionality

## Screenshots

Card Creation

![Screenshot 2025-07-08 122102](https://github.com/user-attachments/assets/97ddf50e-e474-4011-9b9c-ea69d97925bf)
![Screenshot 2025-07-08 122132](https://github.com/user-attachments/assets/8219939c-1a93-4fcc-81a5-c8d03888c25c)

![Screenshot 2025-07-08 122036](https://github.com/user-attachments/assets/d68a354c-b6c2-4ed1-ac3a-f40a73a00748)
![Screenshot 2025-07-08 121949](https://github.com/user-attachments/assets/3fc86239-f5d1-4c92-873b-ce9ac8b3eee1)
![Screenshot 2025-07-08 122153](https://github.com/user-attachments/assets/1dab4b89-1c8b-4d03-a710-14931fcc9c04)

 

Travel Guides
![Screenshot 2025-07-08 164954](https://github.com/user-attachments/assets/e02b106f-2ca9-4b4b-b877-ed80acc4bdd1)
![Screenshot 2025-07-08 164938](https://github.com/user-attachments/assets/c0f95c8a-19c9-4330-b0ac-b16a0f11291e)
![Screenshot 2025-07-08 165042](https://github.com/user-attachments/assets/dc768051-8799-408c-90fb-9fba87557f2a)



Sage Assistant
![Screenshot 2025-07-08 122309](https://github.com/user-attachments/assets/c59dc3f3-c1e2-4fbb-a4b9-2a09c7a310ed)



