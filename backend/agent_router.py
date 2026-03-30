def classify_question(question):
    question = question.lower()

    if any(word in question for word in ["vision", "mission", "peo", "pso", "po", "department", "about", "hod"]):
        return "department_info"

    elif any(word in question for word in ["faculty", "staff", "professor", "dean", "assistant professor", "associate professor"]):
        return "faculty"

    elif any(word in question for word in ["placement", "company", "recruitment", "package", "job"]):
        return "placement"

    elif any(word in question for word in ["lab", "laboratory", "facilities", "infrastructure"]):
        return "lab"

    elif any(word in question for word in ["mou", "collaboration", "industry tie-up", "partnership"]):
        return "mou"

    elif any(word in question for word in ["certification", "course", "value added", "training"]):
        return "certification"

    elif any(word in question for word in ["regulation", "attendance", "cia", "exam", "credit", "pass mark", "eligibility"]):
        return "regulation"

    elif any(word in question for word in ["syllabus", "subject", "semester", "course code", "unit", "3rd sem", "4th sem", "5th sem", "6th sem", "7th sem", "8th sem"]):
        return "syllabus"

    else:
        return "general"