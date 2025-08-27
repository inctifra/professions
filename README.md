# PKenya – Professional Verification Platform

PKenya is a two-part platform designed to help **developers** integrate professional verification into their applications and provide the **general public** with a mobile app for quick professional lookups.  

The system is divided into three major components:

1. **Developer Web Portal (Django + Webpack)** – for managing verification workflows, developer APIs, and domain registrations.
2. **Mobile Backend (NestJS)** – a dedicated backend optimized for mobile queries and public search.
3. **Mobile App (React Native)** – for the general public to search professionals by name, license number, registration number, or scan QR codes.

📖 **Developer Documentation**: [https://docs.pkenya.co.ke](https://docs.pkenya.co.ke)  

---

## 🚀 Features

- **Developer Portal**
  - API key management & role-based admin
  - Bulk verification and CSV imports
  - Audit logs & traceability
  - Domain registration & verification
  - Webpack-bundled assets for performance

- **Mobile Application**
  - Quick search by name, license number, or registration number
  - Offline caching of recent lookups
  - Feedback & reporting tools

- **Mobile Backend (NestJS)**
  - Lightweight, fast REST API for mobile clients
  - JWT-based authentication
  - Rate limiting & caching with Redis
  - Webhook support for third-party integrations

---

## 🛠️ Technology Stack

- **Web Portal**: Django, Django REST Framework, Webpack  
- **Mobile Backend**: NestJS, Node.js  
- **Mobile App**: React Native  
- **Database**: PostgreSQL  
- **Cache/Queue**: Redis, Celery
- **Security**: JWT, HTTPS, session, role-based access control  

---
