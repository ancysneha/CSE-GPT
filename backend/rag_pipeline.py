import os
from dotenv import load_dotenv
import faiss
import numpy as np
import PyPDF2
from groq import Groq
from sentence_transformers import SentenceTransformer

load_dotenv()

# =========================
# CONFIG
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
PDF_FOLDER = os.path.join(PROJECT_ROOT, "data", "pdfs")

EMBED_MODEL = "all-MiniLM-L6-v2"

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Please set it in your .env file.")

client = Groq(api_key=GROQ_API_KEY)
embedder = SentenceTransformer(EMBED_MODEL)

# =========================
# PDF CATEGORY MAP
# =========================
CATEGORY_FILES = {
    "department_info": ["cse-gpt1.pdf"],
    "faculty": ["cse-gpt1.pdf"],
    "placement": ["cse-gpt1.pdf"],
    "lab": ["cse-gpt1.pdf"],
    "mou": ["cse-gpt1.pdf"],
    "certification": ["cse-gpt1.pdf"],
    "regulation": ["R2023-UG.pdf", "R2023-PG.pdf"],
    "syllabus": ["s-2023 ug.pdf", "s-2023 pg.pdf", "s-2025 ug.pdf"],
    "general": [
        "cse-gpt1.pdf",
        "R2023-UG.pdf",
        "R2023-PG.pdf",
        "s-2023 ug.pdf",
        "s-2023 pg.pdf",
        "s-2025 ug.pdf"
    ]
}

# =========================
# READ PDF TEXT
# =========================
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# =========================
# LOAD SELECTED PDF TEXTS
# =========================
def load_selected_documents(folder_path, selected_files):
    docs = []
    for file_name in os.listdir(folder_path):
        if file_name in selected_files and file_name.endswith(".pdf"):
            full_path = os.path.join(folder_path, file_name)
            text = extract_text_from_pdf(full_path)
            docs.append({
                "file": file_name,
                "text": text
            })
    return docs

# =========================
# DIRECT FACT SEARCH FOR DEPARTMENT INFO
# =========================
def direct_department_answer(question):
    pdf_path = os.path.join(PDF_FOLDER, "cse-gpt1.pdf")
    full_text = extract_text_from_pdf(pdf_path).lower()
    q = question.lower()

    if "vision" in q:
        return "To produce intellectual graduates to excel in the field of Computer Science Engineering and Technologies.", ["cse-gpt1.pdf"]

    elif "mission" in q:
        return """Mission of the Department:
1. Providing excellent and intellectual inputs to the students through qualified faculty members.
2. Imparting technical knowledge in latest technologies through the industry institute interaction and thereby making the graduates ready for the industrial environment.
3. Enriching the student’s knowledge for active participation in co-curricular and extracurricular activities.
4. Promoting research-based projects in contexts to social, legal and technical aspects.""", ["cse-gpt1.pdf"]

    elif "hod" in q or "head of department" in q:
        return "The Head of the Department is Dr. S. Raja Mohamed, M.E., Ph.D. – Associate Professor & HoD.", ["cse-gpt1.pdf"]

    elif "course offered" in q or "courses offered" in q:
        return """The department offers the following courses:
1. 4 year UG Course – B.E. Computer Science & Engineering
2. 2 year PG Course – M.E. Computer Science & Engineering
3. Ph.D. in Computer Science & Engineering""", ["cse-gpt1.pdf"]

    elif "lab" in q or "labs" in q or "laboratory" in q:
        return """Lab Facilities:
1. Internet and Software Systems Lab
2. Open Source and Mobile Computing Lab
3. Graphics and Multimedia Lab
4. Data Structures Lab
5. Computer Centre

Labs with Centre of Excellence:
6. Intel powered AI – High Performance Computing Lab
7. Advanced Computing Lab in collaboration with CDAC, Bangalore
8. AICTE – Juniper MistAI Networks Lab
9. DELL-EMC Centre of Excellence for Data Science and Big Data Analytics
10. NVidia DLI Teaching Kits for AI and Deep Learning""", ["cse-gpt1.pdf"]

    elif "mou" in q:
        return """MoUs Signed:
1. Yardstick Digital Solutions
2. Nandha Infotech Solutions
3. Redhat Academy
4. Oracle IT Academy
5. VMWare IT Academy
6. Microsoft IT Academy""", ["cse-gpt1.pdf"]

    elif "certification" in q or "certifications" in q:
        return """Certification Courses / Value Added Programs:
1. Coursera (Exclusive Login)
2. Altair (Rapid miner, IoT)
3. Java certification through WIPRO
4. NMEICT - FOSSEE
5. IBM Power Skills Academy
6. Google Cloud Ready Facilitator Program""", ["cse-gpt1.pdf"]

    elif "faculty" in q or "staff" in q:
        return """Faculty Members:
1. Dr. S. Vimal – Professor & Dean
2. Dr. S. Raja Mohamed – Associate Professor & HoD
3. Dr. S. Santhi – Professor
4. Dr. K. Mahalakshmi – Professor
5. Dr. K. Deeba – Professor
6. Dr. S. Dhanabal – Professor
7. Dr. C. Suresh – Associate Professor
8. Dr. S. Pandiarajan – Assistant Professor
... and more faculty members are available in the department faculty list.""", ["cse-gpt1.pdf"]

    return None, None

# =========================
# SPLIT INTO CHUNKS
# =========================
def split_into_chunks(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

# =========================
# CREATE VECTOR STORE
# =========================
def build_vector_store(docs):
    all_chunks = []
    metadata = []

    for doc in docs:
        chunks = split_into_chunks(doc["text"])
        for chunk in chunks:
            all_chunks.append(chunk)
            metadata.append(doc["file"])

    embeddings = embedder.encode(all_chunks, show_progress_bar=False)
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return index, all_chunks, metadata

# =========================
# RETRIEVE TOP CHUNKS
# =========================
def retrieve_relevant_chunks(query, index, chunks, metadata, top_k=3):
    query_embedding = embedder.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    retrieved_chunks = []
    retrieved_sources = []

    for idx in indices[0]:
        retrieved_chunks.append(chunks[idx])
        retrieved_sources.append(metadata[idx])

    return retrieved_chunks, retrieved_sources

# =========================
# ASK GROQ
# =========================
def ask_groq(question, context):
    prompt = f"""
You are a helpful AI assistant for the Computer Science and Engineering department.

Answer the user's question ONLY using the context below.
If the answer is not found in the context, say:
"Sorry, I couldn't find that information in the provided department documents."

Keep the answer clear, concise, and student-friendly.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content

# =========================
# MAIN SETUP FOR CATEGORY
# =========================
def setup_rag(category="general"):
    selected_files = CATEGORY_FILES.get(category, CATEGORY_FILES["general"])
    docs = load_selected_documents(PDF_FOLDER, selected_files)
    index, chunks, metadata = build_vector_store(docs)
    return index, chunks, metadata

# =========================
# MAIN QUERY FUNCTION
# =========================
def ask_question(query, index, chunks, metadata, category="general"):
    # Direct answer for department facts
    if category == "department_info" or category in ["faculty", "lab", "mou", "certification"]:
        direct_answer, direct_sources = direct_department_answer(query)
        if direct_answer:
            return direct_answer, direct_sources

    # Otherwise use RAG
    expanded_query = f"{query} CSE department syllabus regulation faculty placement"
    relevant_chunks, sources = retrieve_relevant_chunks(expanded_query, index, chunks, metadata)
    context = "\n\n".join(relevant_chunks)
    answer = ask_groq(query, context)
    return answer, sources