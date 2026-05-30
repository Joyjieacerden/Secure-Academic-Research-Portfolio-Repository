# Secure-Academic-Research-Portfolio-Repository

A secure, digital enterprise portfolio generator and repository built with the Django Framework. This platform empowers university faculty to publish and manage their academic publications, credentials, and datasets, while leveraging strict cryptographic and permission-based controls to protect raw, sensitive research data from unauthorized external access.

---

## 👥 Project Team Roles & Contributions

-Joyce (Lead Cloud & DevOps Engineer): Engineered the automated CI/CD deployment pipelines via `build.sh` for Linux container hosting platforms (Render). Integrated cloud-native media structures with Cloudinary and decoupled development secrets utilizing strict environment variable abstractions (`python-dotenv`).
-[Member 2 Name] (Lead Backend Architect):** Designed the relational database architecture, relational co-author mechanics using dynamic formsets, and RESTful API endpoints for downstream citation indexers.
-[Member 3 Name] (Security & DevSecOps Engineer):** Implemented strict object-level validation layers (`OwnerOrManagerMixin`), secure credential hashing configurations, dynamic JWT payload permission parsing, and rate-limiting infrastructure on sensitive download nodes.



🛠️ Advanced Technical Architecture

1. Cloud Media & Asset Processing
* **Cloudinary Engine Integration:** Configured specialized storage backends (`MediaCloudinaryStorage`) to seamlessly offload high-volume research PDFs, document attachments, and multi-gigabyte raw datasets to the cloud, preserving server compute cycles.
* **Production Static Compiling:** Integrated `WhiteNoise` compression mechanisms (`CompressedManifestStaticFilesStorage`) inside the deployment routine to aggregate, cache, and serve core static stylesheets securely.

 2. Enterprise Security Architecture
* **Strict Object-Level Permissions:** Engineered a modular `OwnerOrManagerMixin` tracking layer that intercepts CRUD requests at the controller level—guaranteeing researchers can only update or alter properties belonging explicitly to their verified profile.
* **Dynamic JWT Visibility Routing:** Developed an adaptive Django REST Framework serialization protocol. Basic requests automatically truncate outputs to safe public abstracts, while authenticated Premium or Peer Reviewer JWT tokens securely reveal encrypted download links.
* **Zero-Trust Credential Isolation:** Enforced a zero-exposure environment state by completely abstracting security keys, database roots, and Cloudinary secrets into a protected `.env` file that is kept out of source control via strict `.gitignore` filters.

---

## 🗂️ Project Directory Layout

```text
Secure Academic Research and Portfolio Repository/
│
├── config/                  # Core Project Configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py          # Decoupled Security Settings (Cloudinary + WhiteNoise)
│   ├── urls.py              # Main URL Route Mappings
│   └── wsgi.py
│
├── repository/              # Core Application Directory
│   ├── mixins.py            # OwnerOrManagerMixin Security Assertions
│   ├── models.py            # Academic Schema (ResearchPaper, CoAuthor)
│   ├── serializers.py       # DRF JWT-Driven Dynamic Value Serializers
│   └── views.py             # Business Logic & Formset Controllers
│
├── .env                     # Private App Secrets (Blocked from Version Control)
├── .env.example             # Safe, Shared Template for Peer Environments
├── .gitignore               # Active Git Rules Filtering .env & db.sqlite3
├── build.sh                 # Production Orchestration Script (Migrate & Collectstatic)
├── db.sqlite3               # Local Sandboxed Database
├── manage.py                # Django CLI Orchestrator
└── requirements.txt         # Consolidated Enterprise Dependencie

