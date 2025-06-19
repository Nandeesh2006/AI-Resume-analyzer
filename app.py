import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from utils.parser import extract_resume_data
from utils.matcher import match_jobs
from utils.analytics import record_click
from utils.pdf_generator import generate_pdf

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Jobs file path
JOBS_FILE = "utils/jobs.json"

# Helper functions
def load_jobs():
    with open(JOBS_FILE, "r") as f:
        return json.load(f)

def save_jobs(jobs):
    with open(JOBS_FILE, "w") as f:
        json.dump(jobs, f, indent=2)

# Routes

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("resume")
        if file:
            filename = file.filename
            ext = os.path.splitext(filename)[1].lower()
            if ext not in [".pdf", ".docx"]:
                return "Unsupported file type", 400

            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            resume_data = extract_resume_data(filepath)
            matches = match_jobs(resume_data)

            return render_template("results.html", resume=resume_data, matches=matches)
        else:
            return "No file uploaded", 400

    return render_template("index.html")

# Admin panel

@app.route("/admin")
def admin_panel():
    jobs = load_jobs()
    return render_template("admin.html", jobs=jobs)

@app.route("/admin/add", methods=["POST"])
def add_job():
    title = request.form.get("title")
    description = request.form.get("description")
    if not title or not description:
        return "Missing fields", 400

    jobs = load_jobs()
    jobs.append({"title": title, "description": description})
    save_jobs(jobs)
    return redirect(url_for("admin_panel"))

@app.route("/admin/delete/<int:index>", methods=["POST"])
def delete_job(index):
    jobs = load_jobs()
    if 0 <= index < len(jobs):
        jobs.pop(index)
        save_jobs(jobs)
    return redirect(url_for("admin_panel"))

# Analytics endpoint

@app.route("/track_click", methods=["POST"])
def track_click():
    job_title = request.json.get("job_title")
    if not job_title:
        return jsonify({"error": "Missing job_title"}), 400

    record_click(job_title)
    return jsonify({"success": True})

# PDF report generation

@app.route("/download_report", methods=["POST"])
def download_report():
    resume_data = request.json.get("resume_data")
    matches = request.json.get("matches")
    if not resume_data or not matches:
        return "Missing data", 400

    pdf_buffer = generate_pdf(resume_data, matches)
    return send_file(pdf_buffer, mimetype="application/pdf", as_attachment=True, download_name="resume_report.pdf")
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory job listings store
jobs = [
    {"title": "Software Engineer", "description": "Develop and maintain software applications."},
    {"title": "Data Scientist", "description": "Analyze data to extract insights and build models."}
]

@app.route('/admin/jobs', methods=['GET'])
def get_jobs():
    # Return JSON list of jobs
    return jsonify(jobs)

@app.route('/admin/jobs', methods=['POST'])
def add_job():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title or not description:
        return jsonify({"error": "Title and description required"}), 400

    jobs.append({"title": title, "description": description})
    return jsonify({"message": "Job added successfully", "jobs": jobs}), 201

@app.route('/admin/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    if job_id < 0 or job_id >= len(jobs):
        return jsonify({"error": "Job not found"}), 404

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title or not description:
        return jsonify({"error": "Title and description required"}), 400

    jobs[job_id] = {"title": title, "description": description}
    return jsonify({"message": "Job updated successfully", "jobs": jobs})

@app.route('/admin/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    if job_id < 0 or job_id >= len(jobs):
        return jsonify({"error": "Job not found"}), 404

    jobs.pop(job_id)
    return jsonify({"message": "Job deleted successfully", "jobs": jobs})


if __name__ == "__main__":
    app.run(debug=True)


