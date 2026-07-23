# Advanced AI Medical Intelligence Platform

An end-to-end Explainable AI (XAI) and LLM-driven medical intelligence application designed for automated radiographic scan diagnostic analysis, interpretability, and clinical report generation.

## 🌟 Key Features
- **Deep Learning Classification:** ResNet-18 architecture fine-tuned for high-accuracy diagnostic analysis.
- **Explainable AI (XAI):** Integrated Grad-CAM heatmaps to visually justify AI model classification regions.
- **Automated Clinical Summaries:** LLM-assisted clinical findings generation for medical practitioner reference.
- **RESTful API Backend:** High-performance FastAPI server managing async inference pipelines and DB persistent storage.
- **Interactive UI:** Streamlit frontend dashboard for real-time image uploads, dual image rendering, and audit database logging.

## 🛠️ Architecture Overview
- **Backend Framework:** FastAPI, SQLAlchemy (SQLite Database)
- **Machine Learning Engine:** PyTorch, Torchvision, `pytorch-grad-cam`
- **Frontend App:** Streamlit
- **Containerization:** Docker

## 🚀 Local Quickstart Guide

### 1. Clone Repository & Setup Virtual Environment
```bash
git clone <your-github-repo-link>
cd medical-ai-platform
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt