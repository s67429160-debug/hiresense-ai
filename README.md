# HireSense AI 🚀

AI-Powered Resume & Job Matching Platform

HireSense AI is an intelligent resume analysis platform that helps job seekers understand how well their resume matches a job description.

It analyzes the uploaded resume, extracts relevant skills and keywords, calculates an ATS compatibility score, identifies missing skills, and provides actionable recommendations.

## 🌐 Live Demo

Frontend:
https://hiresense-ai-frontend-d8y4.onrender.com

Backend API:
https://hiresense-ai-backend-docker.onrender.com

API Documentation:
https://hiresense-ai-backend-docker.onrender.com/docs

## ✨ Features

- 🔐 User Registration & Login
- 🔑 JWT Authentication
- 📄 Resume PDF Upload
- 🔎 PDF Text Extraction
- 🧠 OCR Support for Scanned Resumes
- 📋 Job Description Analysis
- 🎯 ATS Compatibility Score
- 🛠️ Skill Matching
- ❌ Missing Skill Detection
- 🔍 Keyword Matching
- 👨‍💻 Job Role Matching
- 🎓 Education Requirement Matching
- 📊 Detailed ATS Score Breakdown
- 💡 Personalized Skill Recommendations
- 📜 Analysis History
- 📑 Downloadable ATS Reports
- 👤 User Profile & Statistics
- 🗄️ PostgreSQL Database
- 🐳 Docker Deployment
- ☁️ Cloud Deployment with Render

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │      User           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   React Frontend    │
                    │      + Vite         │
                    └──────────┬──────────┘
                               │
                         REST API
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        Resume Service     ATS Engine      Auth System
              │                │                │
              ▼                ▼                ▼
          PDF/OCR       Skill Matching       JWT
                               │
                               ▼
                    ┌─────────────────────┐
                    │     PostgreSQL      │
                    │      Database       │
                    └─────────────────────┘