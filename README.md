# 🧪 TransPolymer: AI-Powered Polymer Property Predictor

**TransPolymer** is an intelligent, full-stack AI system developed to predict various polymer properties directly from their SMILES (Simplified Molecular Input Line Entry System) notations. The project brings together the power of **natural language processing**, **deep learning**, and the **MERN stack** to provide a robust and user-friendly platform for materials science applications.

This project was initiated as part of the **KMCE GenAI Project School** and later extended with full-stack integration for real-world usability.

---

## 📌 Key Features

- 🔬 Predicts key polymer properties using a custom-trained Transformer-based masked language model and six regression heads.
- 🧠 Custom BPE tokenizer optimized for SMILES sequences.
- 🌐 MERN stack integration (MongoDB, Express.js, React.js, Node.js).
- ⚙️ Node.js server communicates with Python scripts for model execution.
- 💻 User-friendly web interface with live predictions and detailed outputs.
---

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/transpolymer.git
cd transpolymer

---
##🔧 Backend Setup – TransPolymer

This document outlines the setup instructions for the backend of the **TransPolymer** project, which includes the Python-based AI model and the Node.js server interface.

> **Directory**: `server/`

---

## ✅ Requirements

Before proceeding, ensure the following are installed:

- [Python](https://www.python.org/downloads/) ≥ 3.9  
- [Node.js](https://nodejs.org/) ≥ 18.x  
- pip (Python package installer)  
- [PyTorch](https://pytorch.org/) (with CUDA support if running on GPU)

---

## 📦 Install Python Dependencies

Navigate to the `server` directory and install all required Python packages:

```bash
cd server
pip install -r requirements.txt

Ensure the following subdirectories exist within server/:

merged_chemberta/ — Custom masked language model

regression_models/ — Contains pre-trained weights:

Eea_weights.pt

Egb_weights.pt

Ei_weights.pt

EPS_weights.pt

Nc_weights.pt

Xc_weights.pt

