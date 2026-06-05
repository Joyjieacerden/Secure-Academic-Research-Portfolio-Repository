# Secure Academic Research & Portfolio Repository

An enterprise-grade, secure digital portfolio generator and research repository built with the Django Framework. This platform empowers university faculty to publish and manage their academic publications, credentials, and datasets, while leveraging advanced cryptographic controls, JSON Web Tokens (JWT), and active defensive countermeasures to protect sensitive raw research assets from public exposure.

---

## 👥 Professional Team Roles & Accountability Ledger

Every team member is graded individually during the face-to-face defense based on their mastery of their assigned enterprise domain:

Joyce L. Acerden - Handles the automated deployment process using a Linux script (build.sh) that is configured to stop immediately if any error occurs (set -o errexit). She also set up Cloudinary (MediaCloudinaryStorage) to handle large media files so they don't take up local disk space, and used python-dotenv to safely hide private credentials and keys from the public repository.
Mark Steven Camposano- Built the API endpoints using Django REST Framework (DRF) to handle data requests. He set up token authentication with JSON Web Tokens (JWT) to manage user login sessions, and created a security layer inside the API serializers to hide sensitive data fields from unverified users.
Ann Trecia C. Balendo- Designed the database structure by linking research papers (ResearchPaper) with their co-authors (CoAuthor) using proper foreign keys. She also wrote custom permission logic in the backend views to prevent IDOR attacks, making sure users can only see or edit their own records and can't tamper with anyone else's files.
Rochelle M. Florendo - Designed and built the responsive user dashboards and interactive search filters for the website. She also developed dynamic inline formsets for the co-authors, allowing users to add multiple authors on the fly without the whole page having to reload, and created custom backend template tags to display data cleaner.
Rainier O. Orogan - Focused on the defensive security setup for our project. He integrated django-axes to stop brute-force attacks by temporarily blocking IPs that fail to log in too many times. He also put in threat-monitoring honeypots to catch attackers, created an audit trail that logs high-severity system events automatically, and ran vulnerability scans to make sure our code was secure.

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
