from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generate_pdf(resume_data, matches):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Resume Analysis Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Name: {resume_data.get('name', 'N/A')}")
    c.drawString(50, height - 100, f"Email: {resume_data.get('email', 'N/A')}")

    c.drawString(50, height - 130, "Top Job Matches:")

    y = height - 160
    for job in matches:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, y, f"{job['title']} (Score: {job['score']}%)")
        y -= 20
        c.setFont("Helvetica", 10)
        text = job['description']
        text_lines = split_text(text, 80)
        for line in text_lines:
            c.drawString(70, y, line)
            y -= 15
        y -= 10
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    buffer.seek(0)
    return buffer

def split_text(text, max_chars):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars:
            current_line += (word + " ")
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return lines
