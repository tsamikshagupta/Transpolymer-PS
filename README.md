## 🧾 Project Description

**Transpolymer** is a collaborative, research-driven AI project developed by a team of five Computer Science engineering students. The project aims to build an intelligent, full-stack system capable of **predicting critical physical and chemical properties of polymers** directly from their **SMILES (Simplified Molecular Input Line Entry System)** representations.

In recent years, the demand for rapid materials discovery has surged, especially in fields such as **bioengineering**, **flexible electronics**, and **sustainable chemistry**. Traditional experimental methods for analyzing polymer properties are often **time-consuming**, **expensive**, and **not scalable**. Transpolymer was conceived to address these challenges by leveraging AI to enable **fast, reliable, and cost-effective predictions**, helping researchers screen polymer candidates before experimental synthesis.

---

## 🧠 Core Functionality

At the heart of Transpolymer lies a **custom Transformer-based language model**, inspired by ChemBERTa and RoBERTa, and trained to understand the structure and semantics of polymer SMILES strings. This model generates encoded representations which are then passed through a **multi-headed regression module** to predict six essential polymer properties:

- **Electron Affinity (Eea)** – Affinity of a polymer to gain electrons  
- **Optical Band Gap (Egb)** – Energy difference related to light absorption and conductivity  
- **Ionization Energy (Ei)** – Energy required to remove an electron  
- **Dielectric Constant (EPS)** – Capacity to store electrical energy  
- **Number of Charge Carriers (Nc)** – Quantity of mobile charge carriers  
- **Degree of Crystallinity (Xc)** – Extent of structural order in the polymer matrix

---

## 🧩 System Architecture

The project uses a full-stack architecture that combines the flexibility of web development with the power of machine learning:

- 🎨 **Frontend**: Built using `React.js`, the UI provides a user-friendly platform for researchers to input SMILES and view results.  
- ⚙️ **Backend**: Developed in `FastAPI`, it connects the frontend with the ML pipeline and serves predictions in real-time.  
- 🧠 **Modeling**: Utilizes a **custom BPE Tokenizer** and **Transformer-based Masked Language Model** built in `PyTorch`.  
- 🗃️ **Database**: `MongoDB` is used to store inputs, prediction logs, and user interaction history.

---

## 👥 Team Collaboration

Transpolymer was developed by a dedicated team of 5 members, each focusing on specialized domains:
- **Model Training & Tokenizer Design**  
- **Backend Integration with FastAPI & PyTorch**  
- **Frontend UI/UX Development in React**  
- **Dataset Curation & Preprocessing**  
- **Testing, Documentation & Research Coordination**

Our combined efforts led to a fully functional and academically robust platform aimed at real-world use in laboratories and research institutes.

---

## 🎯 Highlights

- ✅ Fine-tuned Transformer model for scientific SMILES sequences  
- ✅ Real-time predictions of 6 polymer properties  
- ✅ Clean and intuitive UI built with React.js  
- ✅ FastAPI-powered backend with efficient RESTful architecture  
- ✅ Integrated MongoDB database for persistent user history  
- ✅ Trained BPE tokenizer specialized for polymer input data

---

## 📚 Use Cases

- 🔬 **Research Labs** – Preliminary screening of polymer candidates  
- 🧪 **Material Science Courses** – Educational demos on AI-driven materials modeling  
- 🧠 **AI Research** – Fine-tuning and benchmarking of molecular representation models  
- 🌱 **Startups/Industry** – Rapid evaluation of polymer formulations before testing

---

## 🚀 Future Enhancements

- Add 3D visualization for polymer structures  
- Extend predictions to thermal and mechanical properties  
- Enable user-authenticated sessions and exportable reports  
- Incorporate explainable AI (XAI) tools for model transparency

---

> 💡 *Transpolymer is more than a project—it's a step toward democratizing scientific insight through intelligent software.*

