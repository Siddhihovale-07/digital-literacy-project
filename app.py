from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import sqlite3
import json 
from pathlib import Path
from datetime import datetime
import io

app = Flask(__name__)
app.secret_key = "cep-digital-literacy-demo-key"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database.db"

MODULES = [
    {
        "id": "smartphone",
        "title": "Smartphone Basics",
        "icon": "📱",
        "description": "Learn basic phone functions such as calls, contacts, camera, Wi-Fi and settings.",
        "steps": [
            "Open the phone and understand the Home screen.",
            "Make and receive a phone call.",
            "Save a new contact with a name and phone number.",
            "Use the camera to take a photo.",
            "Connect to a trusted Wi-Fi network.",
            "Increase font size and volume if needed."
        ],
        "tips": ["Use a larger font if reading is difficult.", "Save important family contacts clearly."]
    },
    {
        "id": "whatsapp",
        "title": "WhatsApp",
        "icon": "💬",
        "description": "Learn messaging, voice calls, video calls and sharing photos safely.",
        "steps": [
            "Open WhatsApp and select a saved contact.",
            "Type a short message and press Send.",
            "Press the microphone button for a voice message.",
            "Use the call or video icon to contact a trusted person.",
            "Use the attachment button to send a photo or document.",
            "Block or report unknown contacts when necessary."
        ],
        "tips": ["Do not forward messages just because they look urgent.", "Check the sender before opening a link."]
    },
    {
        "id": "internet",
        "title": "Internet & Google",
        "icon": "🌐",
        "description": "Learn how to search for useful information and use YouTube and Maps.",
        "steps": [
            "Open a browser or Google Search.",
            "Type a simple question using clear words.",
            "Check more than one trusted result when possible.",
            "Open YouTube and search for an educational video.",
            "Open Google Maps and search for a known place.",
            "Avoid websites that ask for unnecessary personal information."
        ],
        "tips": ["Prefer official websites for important services.", "Do not believe every result on the internet."]
    },
    {
        "id": "upi",
        "title": "UPI & Digital Payments",
        "icon": "💳",
        "description": "Understand UPI, QR codes and safe digital payment habits.",
        "steps": [
            "Understand that UPI allows money to move digitally between bank accounts.",
            "Learn that a QR code can be used to start a payment.",
            "Check the receiver's name before confirming a payment.",
            "Enter your UPI PIN only on your own trusted payment app.",
            "Check the transaction status after payment.",
            "Ask a trusted person or bank if something looks suspicious."
        ],
        "tips": ["NEVER share your UPI PIN or OTP.", "Receiving money does not require entering your UPI PIN."]
    },
    {
        "id": "cyber",
        "title": "Cyber Safety & Scams",
        "icon": "🔐",
        "description": "Learn how to identify fake calls, messages, links and online scams.",
        "steps": [
            "Do not share OTPs, passwords, PINs or banking details with callers.",
            "Do not click suspicious links received by SMS or messaging apps.",
            "Be careful with fake prize, lottery, job and refund messages.",
            "Never install an app because an unknown caller tells you to.",
            "If a message creates panic or urgency, stop and verify it.",
            "Report suspicious activity to the relevant bank or authority."
        ],
        "tips": ["Pause before you click.", "When unsure, ask a trusted family member."]
    },
    {
        "id": "passwords",
        "title": "Password & Privacy Safety",
        "icon": "🔑",
        "description": "Learn simple ways to protect accounts and personal information.",
        "steps": [
            "Use different passwords for important accounts.",
            "Avoid easy passwords such as birthdays or simple number sequences.",
            "Do not share passwords with strangers.",
            "Use a phone screen lock.",
            "Avoid posting private information publicly.",
            "Log out from accounts on shared devices."
        ],
        "tips": ["Keep recovery information updated.", "Never send your password in a chat message."]
    },
    {
        "id": "services",
        "title": "Online Services",
        "icon": "🏛️",
        "description": "Understand how to access basic online government and public services safely.",
        "steps": [
            "Identify the official website or app for the service.",
            "Check the website address before entering personal details.",
            "Read instructions carefully before submitting a form.",
            "Keep copies of important application or receipt numbers.",
            "Do not pay unknown people for unofficial help.",
            "Ask for assistance when a service requires information you do not understand."
        ],
        "tips": ["Use official government portals whenever possible.", "Never share an OTP with an unknown person."]
    },
    {
        "id": "social",
        "title": "Safe Social Media",
        "icon": "👥",
        "description": "Learn safe habits for social media and online communication.",
        "steps": [
            "Keep your account privacy settings appropriate.",
            "Accept requests only from people you know or trust.",
            "Avoid posting sensitive personal details.",
            "Verify surprising news before forwarding it.",
            "Block and report abusive or suspicious accounts.",
            "Tell a trusted person if you experience online harassment."
        ],
        "tips": ["Think before posting.", "A forwarded message is not automatically true."]
    }
]

SURVEY_QUESTIONS = [
    ("smartphone", "Can you use the basic functions of a smartphone?"),
    ("contacts", "Can you save a new contact in your phone?"),
    ("whatsapp", "Can you send a WhatsApp message?"),
    ("video_call", "Can you make a WhatsApp video call?"),
    ("internet", "Can you search for information on Google?"),
    ("maps", "Can you use a map application to find a place?"),
    ("upi", "Do you understand the basic idea of UPI payments?"),
    ("otp", "Do you know that an OTP should not be shared with anyone?"),
    ("scam", "Can you identify a suspicious message or link?"),
    ("password", "Do you use a screen lock or password to protect your phone?")
]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS surveys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        survey_type TEXT NOT NULL,
        participant_name TEXT NOT NULL,
        age INTEGER,
        answers TEXT NOT NULL,
        score INTEGER NOT NULL,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        participant_name TEXT NOT NULL,
        rating INTEGER NOT NULL,
        comment TEXT,
        created_at TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

def survey_stats():
    conn = get_db()
    rows = conn.execute(
        "SELECT survey_type, COUNT(*) AS count, AVG(score) AS avg_score FROM surveys GROUP BY survey_type"
    ).fetchall()
    participants = conn.execute("SELECT COUNT(DISTINCT participant_name) AS n FROM surveys").fetchone()["n"]
    feedback_count = conn.execute("SELECT COUNT(*) AS n FROM feedback").fetchone()["n"]
    conn.close()

    stats = {"pre": {"count": 0, "avg": 0}, "post": {"count": 0, "avg": 0}}
    for row in rows:
        stats[row["survey_type"]] = {
            "count": row["count"],
            "avg": round(row["avg_score"] or 0, 1)
        }
    return stats, participants, feedback_count

@app.context_processor
def inject_globals():
    stats, participants, feedback_count = survey_stats()
    return {
        "modules": MODULES,
        "stats": stats,
        "participants": participants,
        "feedback_count": feedback_count
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/modules")
def modules():
    return render_template("modules.html")

@app.route("/module/<module_id>")
def module_detail(module_id):
    module = next((m for m in MODULES if m["id"] == module_id), None)
    if not module:
        return "Module not found", 404
    return render_template("module_detail.html", module=module)

@app.route("/survey/<survey_type>", methods=["GET", "POST"])
def survey(survey_type):
    if survey_type not in ("pre", "post"):
        return "Invalid survey type", 400

    if request.method == "POST":
        name = request.form.get("participant_name", "").strip()
        age_raw = request.form.get("age", "").strip()

        if not name or not age_raw.isdigit():
            flash("Please enter the participant name and a valid age.", "error")
            return redirect(url_for("survey", survey_type=survey_type))

        age = int(age_raw)
        answers = {}
        score = 0

        for key, _ in SURVEY_QUESTIONS:
            value = request.form.get(key, "no").lower()
            if value not in ("yes", "no"):
                value = "no"
            answers[key] = value
            if value == "yes":
                score += 1

        conn = get_db()
        conn.execute(
            "INSERT INTO surveys (survey_type, participant_name, age, answers, score, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (survey_type, name, age, json.dumps(answers), score, datetime.now().isoformat(timespec="seconds"))
        )
        conn.commit()
        conn.close()

        flash(f"{survey_type.title()}-training survey submitted successfully. Score: {score}/10", "success")
        return redirect(url_for("results"))

    return render_template(
        "survey.html",
        survey_type=survey_type,
        questions=SURVEY_QUESTIONS
    )

@app.route("/results")
def results():
    stats, participants, feedback_count = survey_stats()
    conn = get_db()
    recent = conn.execute(
        "SELECT survey_type, participant_name, age, score, created_at FROM surveys ORDER BY id DESC LIMIT 10"
    ).fetchall()
    conn.close()

    improvement = None
    if stats["pre"]["avg"] and stats["post"]["avg"]:
        improvement = round(stats["post"]["avg"] - stats["pre"]["avg"], 1)

    return render_template(
        "results.html",
        stats=stats,
        participants=participants,
        feedback_count=feedback_count,
        recent=recent,
        improvement=improvement
    )

@app.route("/safety")
def safety():
    return render_template("safety.html")

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("participant_name", "").strip()
        rating = request.form.get("rating", "")
        comment = request.form.get("comment", "").strip()

        if not name or rating not in {"1", "2", "3", "4", "5"}:
            flash("Please enter your name and select a rating.", "error")
            return redirect(url_for("feedback"))

        conn = get_db()
        conn.execute(
            "INSERT INTO feedback (participant_name, rating, comment, created_at) VALUES (?, ?, ?, ?)",
            (name, int(rating), comment, datetime.now().isoformat(timespec="seconds"))
        )
        conn.commit()
        conn.close()

        flash("Thank you for your feedback!", "success")
        return redirect(url_for("feedback"))

    return render_template("feedback.html")

@app.route("/certificate")
def certificate():
    return render_template("certificate.html")

@app.route("/admin")
def admin():
    stats, participants, feedback_count = survey_stats()
    conn = get_db()
    survey_rows = conn.execute(
        "SELECT id, survey_type, participant_name, age, score, created_at FROM surveys ORDER BY id DESC"
    ).fetchall()
    feedback_rows = conn.execute(
        "SELECT participant_name, rating, comment, created_at FROM feedback ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template(
        "admin.html",
        survey_rows=survey_rows,
        feedback_rows=feedback_rows,
        stats=stats,
        participants=participants
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
