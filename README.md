
# Celio - https://celioapp.up.railway.app/

**Multilingual E-Cards for Celiac Disease**


<img width="1324" height="773" alt="Screenshot 2025-12-01 at 1 06 49 PM" src="https://github.com/user-attachments/assets/bf3bbc51-0517-4c8f-b5c9-9ffbf3b2c0fd" />



*A comprehensive demo web application showcasing modern full-stack development, designed to become a mobile app later in 2026.*



# Celio

Celio is an app I made because I needed something like it and couldn’t find it anywhere. I have celiac disease, and when I travel, it’s hard to explain what that means especially in a different language. It gets exhausting fast. Sometimes scary.

This tool creates a downloadable card that explains your condition in multiple languages so you can stay safe, eat with confidence, and not have to explain your whole medical history every time you sit down at a table.

---

### What it does

- Translates celiac safety info into 6+ languages (audio or text)
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
4. **Theme Customization**: Multiple visual themes (Teal, Blue, Dark, Purple) with CSS custom properties
5. **Export Options**: Cards can be downloaded as HTML, PDF, or shared via QR codes
6. **Accessibility First**: WCAG 2.1 AA compliant with keyboard navigation and screen reader support

---

### Technical Challenges Solved

**Multilingual Translation System:**
- Built a custom translation engine supporting 11 languages without external APIs
- Implemented phrase-based translation with intelligent fallbacks
- Handled medical terminology accuracy across cultural contexts

**Real-time Preview System:**
- Integrated HTMX for seamless form updates without JavaScript complexity (Switched to alpine.js for persistence of translations)
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

**Client-Side State Management (Alpine.js Migration):**
- **Problem:** Initial server-side rendering with HTMX caused noticeable UI stutter and full-page refreshes during high-frequency interactions (e.g., toggling themes, switching languages).
- **Solution:** Migrated interactive card state to **Alpine.js** for instant, client-side reactivity.
- **Hybrid Approach:** 
    - **Alpine.js** handles the immediate UI updates (text changes, class toggles) for a premium, app-like feel.
    - **HTMX** operates in the background, debounced, to persist state to the server without interrupting the user flow.
    - **Result:** Zero-latency interactions with robust server-side persistence.

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


<img width="1436" height="811" alt="Screenshot 2025-12-07 at 3 02 28 AM" src="https://github.com/user-attachments/assets/fe7ed4b3-38c4-4d49-aeb2-09b9d58d98d3" />

<img width="1440" height="817" alt="Screenshot 2025-12-07 at 3 03 27 AM" src="https://github.com/user-attachments/assets/4d563363-59df-428e-b29e-83d1fcb76028" />

 

Sage AI

<img width="1408" height="724" alt="Screenshot 2025-12-07 at 2 59 14 AM" src="https://github.com/user-attachments/assets/2d007fcc-139e-4b83-bf97-c4c573a7610a" />


<img width="1398" height="737" alt="Screenshot 2025-12-07 at 3 00 19 AM" src="https://github.com/user-attachments/assets/7dec9a72-5d44-49c6-856b-075fb1e93952" />





