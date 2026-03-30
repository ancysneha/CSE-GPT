# 🚀 CSE-GPT: Agentic AI-Powered Intelligent Department Assistant

## 📌 Overview
CSE-GPT is an **Agentic AI-based department assistant** designed for Computer Science students.  
It transforms static department data (website + PDFs) into an **interactive, intelligent, and personalized academic support system**.

---

## 🎯 Features
- 📚 **Department Knowledge Assistant**  
  Answers queries about vision, mission, courses, labs, MoUs, etc.

- 📖 **Smart Syllabus Navigator**  
  Explains subjects, units, and key topics.

- 🏅 **Certification Advisor**  
  Suggests certifications based on student interests and goals.

- 🤖 **Agentic AI Routing**  
  Automatically identifies user intent and routes queries to the appropriate AI agent.

- 🎯 **Courses offered**  
  Answers UG, PG and PhD courses in the department.

- 🌟 **Shows placement details**
  Lists the details of placements batch wise.

- 👩🏻‍💻 **Faculty details**
  Shows the department faculties with their designation.

---

## 🧠 Tech Stack
- **Frontend:** React  
- **Backend:** Python  
- **LLM API:** Groq (LLaMA 3)  
- **Framework:** LangChain  
- **Vector Database:** FAISS  
- **Document Processing:** PyPDF  

---

## ⚙️ Architecture
1. Collect data from **college website + PDFs**
2. Convert into text and split into chunks
3. Generate embeddings using HuggingFace models
4. Store in FAISS vector database
5. Retrieve relevant context using RAG
6. Process queries using Groq LLM
7. Route queries via **Agentic AI system**
8. Generate intelligent, context-aware responses

---

## 👩‍💻 Team
- Aishwarya R
- Ancy Sneha P
- Madhu Mithra A

---

## 📌 Conclusion
CSE-GPT bridges the gap between **department information and student success** by providing an intelligent, autonomous, and personalized learning assistant.

---