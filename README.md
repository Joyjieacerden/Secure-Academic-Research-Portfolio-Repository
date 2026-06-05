# Secure Academic Research & Portfolio Repository

An enterprise-grade, secure digital portfolio generator and research repository built with the Django Framework. This platform empowers university faculty to publish and manage their academic publications, credentials, and datasets, while leveraging advanced cryptographic controls, JSON Web Tokens (JWT), and active defensive countermeasures to protect sensitive raw research assets from public exposure.

---
### 🔗 Project Links
[![GitHub Repository] https://github.com/Joyjieacerden/Secure-Academic-Research-Portfolio-Repository.git

[![Live on Render] https://secure-academic-research-portfolio.onrender.com

## 👥 Professional Team Roles & Accountability Ledger

Every team member is graded individually during the face-to-face defense based on their mastery of their assigned enterprise domain:

### 📋 Overview Matrix

| Team Member | Domain / Focus Area | Core Technical Stack & Implementations |
| :--- | :--- | :--- |
| **Joyce L. Acerden** | DevOps & Cloud Infrastructure | Bash scripting (`build.sh`), `set -o errexit`, Cloudinary, `python-dotenv` |
| **Mark Steven Camposano** | Backend API & Authentication | Django REST Framework (DRF), JWT, Serializer-level data masking |
| **Ann Trecia C. Balendo** | Data Architecture & Security | Relational database mapping, IDOR mitigation, View-level permissions |
| **Rochelle M. Florendo** | UI/UX & Frontend Engineering | Responsive dashboards, Dynamic inline formsets, Custom template tags |
| **Rainier O. Orogan** | Cyber Security & Auditing | `django-axes`, Threat-monitoring honeypots, Automated audit logging |

---

### 👤 Detailed Contributions

#### 🚀 Joyce L. Acerden — DevOps & Cloud Infrastructure
* **Automated Deployment:** Engineered the automated deployment pipeline using a Linux script (`build.sh`) configured with `set -o errexit` to halt execution immediately upon encountering an error.
* **Cloud Storage Management:** Integrated Cloudinary (`MediaCloudinaryStorage`) to handle large media file uploads, optimizing local disk space utilization.
* **Environment Security:** Implemented `python-dotenv` to isolate and securely manage private credentials and API keys away from the public repository.

#### 🛠️ Mark Steven Camposano — Backend API & Authentication
* **API Endpoints:** Developed robust RESTful API endpoints using the Django REST Framework (DRF) to efficiently handle system data requests.
* **Session Management:** Established a secure token authentication system using JSON Web Tokens (JWT) to manage user login sessions.
* **Data Privacy:** Implemented a security layer directly within the API serializers to mask and restrict sensitive data fields from unverified users.

#### 📊 Ann Trecia C. Balendo — Data Architecture & Security
* **Database Design:** Structured the relational database schema, properly mapping relationships between research papers (`ResearchPaper`) and their respective co-authors (`CoAuthor`) using explicit foreign keys.
* **Access Control:** Developed custom backend permission logic within views to prevent Insecure Direct Object Reference (IDOR) attacks, ensuring users can only view or modify their own records.

#### 💻 Rochelle M. Florendo — UI/UX & Frontend Engineering
* **Dashboard Design:** Designed and developed the website's responsive user dashboards and interactive search filter systems.
* **Dynamic Form Handling:** Built dynamic inline formsets for the co-author management module, allowing seamless, real-time author additions without requiring page reloads.
* **Data Presentation:** Created custom backend template tags to clean and properly format raw data before rendering it to the frontend.

#### 🛡️ Rainier O. Orogan — Cyber Security & Auditing
* **Brute-Force Defense:** Integrated `django-axes` to defend against brute-force attacks by implementing temporary IP rate-limiting and lockout mechanics after successive failed logins.
* **Threat Detection:** Deployed active threat-monitoring honeypots to detect and trap malicious actors.
* **Compliance & Monitoring:** Built an automated audit trail system that logs high-severity system events, paired with routine vulnerability scans to ensure code integrity.
---

## 🛠️ Advanced Technical Architecture & Implementation

### 1. Cloud Infrastructure & DevOps Pipeline
* **Dynamic Cloud Offloading:** Leverages `MediaCloudinaryStorage` backends to pipe heavy PDF files and raw datasets directly to Cloudinary, bypassing disk storage constraints.
* **Hermetic Environment Isolation:** Completely seals operational master keys, database variables, and third-party secrets within a local `.env` file, locked out of version control via explicit `.gitignore` matrices.
* **Automated Environment Staging:** Uses an orchestrated `./build.sh` sequence that enforces strict pipeline failure catching (`set -o errexit`), dependency assembly, static compilation (`collectstatic`), and database schema updates (`migrate`).

### 2. API Engineering & Identity Access Management (IAM)
* **JWT Access Escalation:** Implements stateless tokens where basic public requests return generic bibliographic strings, while verified Premium or Reviewer JWT signatures unlock full down-stream metadata fields.
* **Field-Level Data Masking:** Implements structural masking layers inside Django REST Framework serializers to explicitly obscure raw URLs unless specific user group criteria are satisfied.

### 3. Database Architecture & Anti-IDOR Logic
* **Relational Normalization:** Structured explicit foreign key bindings between primary `ResearchPaper` records and dynamic `CoAuthor` datasets.
* **Anti-IDOR Constraints:** Enforces strict multi-tenant validation via custom view logic, ensuring a logged-in researcher cannot access or manipulate record Primary Keys belonging to other faculty accounts.

### 4. Interactive Interface UI & Formsets
* **Dynamic Inline Formsets:** Empowers faculty to dynamically append an arbitrary number of co-authors to a single research abstract directly inside the creation view without reloading the page.

### 5. DevSecOps Active Defense & Logging
* **Brute-Force Mitigation:** Employs monitoring configurations (`django-axes`) to dynamically track login attempts and drop temporary firewalls against suspicious source IPs.
* **System Audit Trail:** Records a chronological stream of high-severity system events, tracking raw data downloads, user elevation requests, and failed cryptographic handshakes.

---

### 🛠️ Project Tech Stack & Dependency Mapping

The following production dependencies are managed within the enterprise architecture to support security, data integrity, and deployment workflows:

* **Core Framework & WSGI:** `Django==5.1.6`, `asgiref==3.11.1`, `gunicorn==26.0.0`
* **Database & Storage:** `psycopg2-binary==2.9.12`, `dj-database-url==3.1.2`, `cloudinary==1.44.2`, `django-cloudinary-storage==0.3.0`
* **API & Authentication:** `djangorestframework==3.17.1`, `djangorestframework_simplejwt==5.5.1`, `PyJWT==2.13.0`, `Authlib==1.7.2`
* **Application Hardening & Security:** `django-axes==8.3.1`, `django-honeypot==1.3.0`, `django-csp==4.0`, `django-permissions-policy==4.30.0`, `django-ratelimit==4.1.0`
* **Vulnerability Auditing & Compliance:** `pip_audit==2.9.0`, `safety==3.5.1`, `bandit==1.8.3`
* **Environment & Assets:** `python-dotenv==1.2.2`, `django-environ==0.13.0`, `whitenoise==6.12.0`
* **Data Validation & Parsing:** `pydantic==2.9.2`, `annotated-types==0.7.0`, `marshmallow==4.3.0`
* **Utilities & Utilities:** `pillow==12.2.0`, `fpdf2==2.8.7`, `nltk==3.9.4`, `sqlparse==0.5.5`

## 🗂️ Project Directory Layout

```text
Secure Academic Research and Portfolio Repository/
├── .venv/                     # Python Virtual Environment
├── config/                    # Core Project Configuration Folder
│   ├── __init__.py
│   ├── settings.py            # Decoupled Security Configuration
│   ├── urls.py                # Main System Routing Table
│   └── wsgi.py                # Gunicorn Staging Entrypoint
├── deliverables/              # Project Deliverables & Documentation
├── logs/                      # System Audit Trail & Event Logs
├── publication_api/           # DRF App (Token-Masked APIs)
│   ├── models.py              # Publication Database Schema
│   ├── serializers.py         # JWT Token-Masked Serializers
│   └── views.py               # Masked Endpoint Controllers
├── research_repo/             # Monolithic Web App Module
│   ├── models.py              # Primary Research Data Models
│   ├── views.py               # Inline Formset Controllers
│   └── templates/             # App-Specific Frontend Layouts
├── security/                  # DevSecOps (Active Defense & Axes)
├── static/                    # Root Global Static Asset Directory
├── staticfiles/               # Collected Static Assets (Production)
├── templates/                 # Shared Global UI & Dashboard Components
├── .env                       # Private Secrets (Git Blocked)
├── .gitignore                 # Strict Exclusion Rule Matrix
├── build.sh                   # Production Linux Automation Script
├── db.sqlite3                 # Local Sandbox SQLite Database
├── IMPLEMENTATION_MATRIX.md   # Project Implementation Docs
├── manage.py                  # Django CLI Orchestration Engine
├── README.md                  # System Documentation Entrypoint
└── requirements.txt           # Production Dependencies Manifest
