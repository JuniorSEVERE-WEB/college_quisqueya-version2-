# 🎓 College Quisqueya

A **modern full-stack school management system** built with **Django REST Framework** (backend) and **React + Vite** (frontend).  
Designed for educational institutions that need a scalable, elegant, and efficient management solution.

---

## 🚀 Features

- 🔐 **User Authentication & Roles**
  - Students, Teachers, Admins, Employees, Alumni, Parents
- 🎓 **Academic Management**
  - Programs, Classrooms, Subjects, Trimesters, Steps, Grades
- 🧾 **Reports & Evaluations**
  - Report cards, Subject coefficients, Automated grade reports
- 💬 **Communication**
  - Internal messaging system, contact forms
- 💰 **Donations & Financials**
  - Online donation management and tracking
- 🏫 **Homepage Management**
  - Slides, welcome messages, values, and gallery
- 🧑‍💼 **Modern Admin Interface**
  - Powered by **Jazzmin** for an elegant and responsive Django admin
- ⚡ **Fast Frontend**
  - Built with **React + Vite** for a modern, reactive user experience

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Django, Django REST Framework, Jazzmin |
| **Frontend** | React, Vite, Axios, TailwindCSS |
| **Database** | SQLite (development) / PostgreSQL (production) |
| **API Auth** | JWT (SimpleJWT) |
| **Deployment (suggested)** | Render / Railway / Docker |

---

## 🎯 Distinctiveness and Complexity

### Why This Project Satisfies the Requirements

**Distinctiveness from Other CS50W Projects:**

This school management system is fundamentally different from all previous CS50W projects in both purpose and implementation. Unlike Project 4 (Network), this is not a social media platform - while it includes messaging capabilities between teachers, parents, and students, these serve a specific educational purpose for academic communication within a structured institutional context. The messaging is role-based and tied to academic responsibilities, not social networking features.

Regarding potential similarities to Project 2 (Commerce), while the system includes a donation module for school fundraising, this represents a minor component of the overall application. The donation feature exists solely to support educational institutions' financial needs and is completely secondary to the core academic management functionality. The primary focus is on educational administration: managing student enrollments, tracking academic progress across trimesters, generating detailed report cards, and facilitating structured communication between all educational stakeholders.

This project addresses the specific needs of educational institutions, particularly those in Haiti where I've observed firsthand the challenges schools face with manual record-keeping and inefficient communication systems. The system incorporates the trimester-based academic calendar common in Haitian schools, coefficient-weighted grade calculations used in French educational systems, and multi-generational family tracking that allows schools to maintain relationships with alumni and extended family networks.

**Technical Complexity Demonstrated:**

The system showcases substantial complexity through multiple interconnected technical layers:

1. **Advanced Database Architecture**: The application utilizes 15+ interconnected Django models that represent the complex relationships inherent in educational institutions. Students are enrolled in programs that contain multiple subjects with specific coefficients, grades are tracked across multiple trimesters with weighted calculations, and comprehensive report cards aggregate data from numerous sources with sophisticated averaging algorithms.

2. **Multi-Tier Permission System**: I implemented a comprehensive role-based access control system with six distinct user types (Student, Teacher, Admin, Employee, Alumni, Parent), each with carefully crafted permissions and data access levels. Parents can only view their children's academic information, teachers can modify grades exclusively for their assigned subjects and classes, administrators have comprehensive oversight with detailed audit trails, and students have read-only access to their own academic records.

3. **Complex Academic Business Logic**: The grade calculation engine implements weighted averages using subject coefficients, handles incomplete grade scenarios, calculates cumulative GPAs across multiple trimesters, and generates comprehensive academic transcripts. The report card system aggregates data from multiple academic periods, applies institutional grading policies, and determines student promotion eligibility based on configurable academic standards.

4. **Real-Time Data Management**: The frontend employs React hooks with custom API integration patterns to provide immediate updates when grades are entered or modified, ensuring that parents and students see changes instantaneously without requiring page refreshes or manual synchronization.

5. **Mobile-First Responsive Design**: The entire interface adapts seamlessly across device sizes, from comprehensive administrative dashboards on desktop computers to streamlined parent portals optimized for smartphone access, which is crucial for reaching parents in Haiti who predominantly use mobile devices for internet access.

The technical challenges included coordinating Django's ORM for complex multi-table queries, implementing Django REST Framework serializers for nested data relationships, managing React state for real-time updates across multiple user sessions, and ensuring data consistency across concurrent grade entry operations by multiple teachers.

---

## 📁 File Structure and Documentation

### Backend Django Application Structure

**`school/models.py`** - Core database models representing the complete school ecosystem:
- `CustomUser` model extending Django's AbstractUser with role-specific fields and academic affiliations
- `Program`, `Subject`, `Classroom` models defining the academic structural hierarchy
- `Trimester`, `Step`, `Grade` models for temporal academic tracking and evaluation
- `ReportCard` model for comprehensive academic summaries with calculated averages
- `Donation`, `Slide`, `Message`, `Contact` models for institutional communication and fundraising
- Complex many-to-many relationships with custom through tables for academic associations

**`school/serializers.py`** - Django REST Framework serializers for comprehensive API data transformation:
- Nested serializers for complex relational data including grades with student and subject details
- Custom validation logic ensuring academic integrity constraints and grade range validation
- Optimized read-only and write-only field configurations for security and performance
- Specialized serializers for report card generation with calculated field aggregation

**`school/views.py`** - API endpoints implementing sophisticated business logic:
- ModelViewSets providing full CRUD operations for all major educational entities
- Custom endpoints for advanced operations like bulk grade entry and report card generation
- Authentication and permission enforcement with role-based access control
- Optimized database queries using select_related and prefetch_related for performance
- Custom filtering and search capabilities for large datasets

**`school/urls.py`** - Comprehensive API routing with nested resources and custom endpoints for educational workflows

**`school/admin.py`** - Extensively customized Django admin interface using Jazzmin theming:
- Enhanced admin classes with advanced filtering, search, and bulk operation capabilities
- Inline editing interfaces for related models like grades and subject assignments
- Custom admin actions for academic operations like transcript generation and grade import
- Role-appropriate admin access with customized interfaces for different user types

**`config/settings.py`** - Django configuration optimized for educational institutions:
- Environment-based configuration supporting development and production deployments
- JWT authentication configuration with appropriate token lifetimes for academic use
- CORS setup enabling seamless frontend-backend integration
- Media and static file handling for academic documents and institutional branding

### Frontend React Application Architecture

**`src/components/`** - Modular, reusable React components:
- `Layout.jsx` - Main application shell with role-appropriate navigation and responsive design
- `GradeEntry.jsx` - Interactive grade input interface with real-time validation and calculation
- `ReportCardGenerator.jsx` - Dynamic report card creation with print-optimized formatting
- `StudentProfile.jsx` - Comprehensive student information display with academic history
- `ParentDashboard.jsx` - Simplified interface showing relevant student information for parents
- `TeacherGradebook.jsx` - Professional grade management interface for educators

**`src/pages/`** - Main application views optimized for different user roles:
- `Dashboard.jsx` - Role-specific landing pages with relevant information and quick actions
- `StudentManagement.jsx` - Administrative interface for student enrollment and record management
- `GradeManagement.jsx` - Comprehensive grade entry and modification system for teachers
- `AcademicReports.jsx` - Report generation and academic analytics for administrators
- `Communication.jsx` - Internal messaging system for institutional communication

**`src/hooks/`** - Custom React hooks encapsulating complex API interactions:
- `useAuth.js` - Authentication state management with automatic token refresh and role detection
- `useAcademicData.js` - Optimized data fetching for grades, subjects, and academic records
- `useRealTimeUpdates.js` - WebSocket-like functionality for live grade updates and notifications
- `usePermissions.js` - Role-based permission checking for UI element visibility and functionality

**`src/utils/`** - Utility functions and application configuration:
- `api.js` - Axios configuration with interceptors for authentication, error handling, and request optimization
- `academicHelpers.js` - Utility functions for grade calculations, GPA computation, and academic formatting
- `dateUtils.js` - Date handling utilities for academic calendars and trimester management
- `constants.js` - Application-wide constants including academic standards and institutional configuration

**`src/styles/`** - Comprehensive styling system:
- TailwindCSS configuration optimized for educational interfaces
- Custom component styles for academic-specific elements like report cards and grade displays
- Responsive design utilities ensuring accessibility across all device types

### Configuration and Deployment Files

**`requirements.txt`** - Complete Python dependency specification including Django ecosystem packages, database drivers, and production deployment utilities

**`package.json`** - Node.js dependencies with optimized versions for performance and security, including React ecosystem packages and build tools

**`vite.config.js`** - Vite configuration optimized for educational application deployment with appropriate build settings and proxy configuration for API integration

---

## 🏃‍♂️ How to Run the Application

### System Prerequisites
- Python 3.9+ with pip package manager
- Node.js 16+ with npm for frontend package management
- Git version control system for project cloning and management

### Backend Django Setup Process

1. **Repository Setup:**
```bash
git clone https://github.com/JuniorSEVERE-WEB/college_quisqueya-version2-
cd college_quisqueya

Application Access Points
Main Application Interface: http://localhost:5173/
API Documentation & Testing: http://localhost:8000/api/
Administrative Dashboard: http://localhost:8000/admin/
Sample Login Credentials (After Loading Fixtures)
Admin: severejunior2017@gmail.com / django2017@


Python Environment Configuration:
# Create isolated Python environment
python -m venv venv

# Activate virtual environment
# Windows Command Prompt:
venv\Scripts\activate
# Windows PowerShell:
venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate


Backend Dependencies Installation:
pip install -r requirements.txt


Database Setup and Migration:
# Create database migrations
python manage.py makemigrations school

# Apply migrations to create database structure
python manage.py migrate

# Load initial academic data (optional)
python manage.py loaddata fixtures/initial_data.json


Administrative User Creation:
python manage.py createsuperuser
# Follow prompts to create admin account with full system access


Django Development Server Launch:
python manage.py runserver
# Backend API available at http://localhost:8000/


Frontend React Setup Process
Frontend Directory Navigation:
# Open new terminal window/tab and navigate to frontend
cd frontend


Node.js Dependencies Installation:
npm install
# This installs all React, Vite, and utility packages

Development Server Launch
npm run dev
# Frontend application available at http://localhost:5173/







Additional Information for CS50W Staff
Mobile Responsiveness Implementation
The application prioritizes mobile accessibility, recognizing that many parents and students in Haiti access web applications primarily through smartphones. The responsive design employs TailwindCSS breakpoint system with touch-optimized interfaces for grade entry, report viewing, and communication features. All interactive elements maintain appropriate touch targets (minimum 44px), and the layout adapts fluidly from 320px mobile screens to large desktop displays.


 displays.

Security Architecture
JWT Authentication: Implemented with djangorestframework-simplejwt providing secure token-based authentication with configurable expiration times appropriate for educational environments
Role-Based Access Control: Comprehensive permission system enforced at both database and API levels, ensuring users can only access appropriate academic information
Data Validation: Multi-layer input validation including Django model constraints, DRF serializer validation, and frontend form validation to maintain academic data integrity
CSRF Protection: Full CSRF protection for all state-changing operations, with additional security headers for production deployment
Performance Optimization Strategies
Database Query Optimization: Extensive use of select_related() and prefetch_related() to minimize database queries when loading complex academic relationships
Frontend Code Splitting: React lazy loading implementation reducing initial bundle size and improving perceived performance


Caching Strategy: Strategic use of Django caching for frequently accessed academic data like grade calculations and report generation
API Response Optimization: Paginated responses for large datasets and optimized serializers to minimize data transfer
Cultural and Educational Context
The system incorporates specific features relevant to Haitian educational institutions:

Trimester Academic Calendar: Unlike US semester systems, accommodates the trimester structure common in Haitian schools
Coefficient-Based Grading: Implements weighted grade calculations using subject coefficients as practiced in French educational systems
Extended Family Tracking: Supports complex family relationships common in Haitian culture, allowing multiple guardians and extended family access to student information
Bilingual Considerations: Architecture supports future French/Creole localization for broader accessibility
Deployment and Production Readiness
The application architecture supports seamless deployment to cloud platforms:

Environment Configuration: Comprehensive environment variable system for secure production deployment
Database Flexibility: Easy migration from SQLite development database to PostgreSQL for production scaling
Static File Handling: Optimized static file and media management for CDN integration
Docker Support: Containerization-ready with appropriate configuration for modern deployment workflows
Academic Data Integrity Features
Grade Validation: Comprehensive validation ensuring grades fall within institutional ranges and academic standards
Audit Trails: Complete logging of all academic record modifications with timestamp and user attribution
Backup Integration: Database backup strategies ensuring academic record preservation and disaster recovery
Data Export: Academic transcript and report export functionality for institutional reporting and student transfers
This project represents a production-ready educational management system that demonstrates mastery of full-stack web development while addressing real-world institutional needs through thoughtful design and robust implementation.

