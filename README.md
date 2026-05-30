# Secure Academic Research & Portfolio Repository

An enterprise-grade, secure digital portfolio generator and research repository built with the Django Framework. This platform empowers university faculty to publish and manage their academic publications, credentials, and datasets, while leveraging advanced cryptographic controls, JSON Web Tokens (JWT), and active defensive countermeasures to protect sensitive raw research assets from public exposure.

---

## 👥 Professional Team Roles & Accountability Ledger

Every team member is graded individually during the face-to-face defense based on their mastery of their assigned enterprise domain:

* **Joyce (Lead Cloud & DevOps Engineer):** Orchestrates infrastructure deployment automation, cloud-native media structures via Cloudinary, zero-trust credential abstraction (`python-dotenv`), and compilation configurations.
* **Mark Steven Camposano (API & IAM Engineer):** Constructs the Django REST Framework (DRF) endpoints, handles JSON Web Token (JWT) identity lifetimes, and engineers conditional field-level data masking.
* **Ann Trecia C. Balendo (Database Architect & RBAC Lead):** Directs schema modeling relationships, handles bulk database execution pipelines, and implements anti-IDOR (Insecure Direct Object Reference) access control logic.
* **Rochelle M. Florendo (Frontend UI & Component Engineer):** Builds responsive dashboard layouts, designs interactive search filtering grids, handles dynamic inline co-author formsets, and codes custom template tags.
* **Rainier Orogan (DevSecOps & Compliance Analyst):** Integrates active runtime application defenses (`django-axes`), deploys threat-monitoring honeypots, structures audit log streams, and executes automated vulnerability scans.

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
│
├── config/                  # Core Project Configuration Folder
│   ├── __init__.py
│   ├── settings.py          # Decoupled Security Configuration
│   ├── urls.py              # Main System Routing Table
│   └── wsgi.py              # Gunicorn Staging Entrypoint
│
├── repository/              # Core Repository Application Module
│   ├── mixins.py            # Object-Level Permission Control Layers
│   ├── models.py            # Database Models (ResearchPaper, CoAuthor)
│   ├── serializers.py       # DRF Token-Masked Serializers
│   └── views.py             # Formset Controllers & Core Logic
│
├── .env                     # Private Secrets (Blocked from Version Control)
├── .env.example             # Shared Configuration Layout Template
├── .gitignore               # Strict Exclusion Pattern Rules
├── build.sh                 # Production Linux Deployment Automation Script
├── db.sqlite3               # Local Sandbox Database System
├── manage.py                # Django CLI Orchestration Engine
└── requirements.txt         # Production Dependency Packages Manifest
