# 🚀 Full-Stack Dockerized Web App with Flask, MySQL, Redis & Nginx

A complete full-stack application built with **Flask (Python)** on the backend, powered by **MySQL**, **Redis** for caching, **Nginx** as reverse proxy, and **Docker Compose** for container orchestration. Includes user authentication (JWT-based), theme toggle, and an **Admin Panel**.

---

## 📦 Features

- ✅ **User Registration & Login** with secure JWT token handling
- 🔐 **Authentication & Authorization** for protected routes
- 🧑‍💼 **Admin Dashboard** to manage and view all users
- 🌙 **Theme Toggle** (Light/Dark) stored in localStorage
- ⚡ **Data submission and retrieval** using Flask APIs
- 🐳 **Fully containerized** using Docker and Docker Compose
- 🔄 **Redis caching** integration for fast performance
- 🌐 **Nginx reverse proxy** for production-ready setup

---

## 🧱 Tech Stack

| Layer        | Technology        |
|-------------|-------------------|
| Frontend     | HTML, CSS, JavaScript |
| Backend      | Python (Flask)    |
| Database     | MySQL             |
| Caching      | Redis             |
| Web Server   | Nginx             |
| Containerization | Docker, Docker Compose |
| Auth         | JWT (via `flask-jwt-extended`) |

---

## 🧑‍💻 Folder Structure

project/
│
├── backend/
│ ├── app.py
│ ├── auth.py
│ ├── admin.py
│ ├── database.py
│ └── requirements.txt
│
├── frontend/
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ ├── admin.html
│ └── script.js
│
├── nginx/
│ └── default.conf
│
├── docker-compose.yml
└── README.md





