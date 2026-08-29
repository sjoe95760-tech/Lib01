import requests
import os
import json
from datetime import datetime

# --- List of topics ---
topics = [
    ("language", "Python"), ("language", "JavaScript"), ("language", "Java"),
    ("language", "C++"), ("language", "C#"), ("language", "Go"),
    ("language", "Rust"), ("language", "Swift"), ("language", "Kotlin"),
    ("language", "TypeScript"), ("language", "Ruby"), ("language", "PHP"),
    ("language", "SQL"), ("language", "HTML/CSS"), ("language", "Scala"), ("language", "Perl"),

    ("security", "Network Security"), ("security", "Cryptography"),
    ("security", "Penetration Testing"), ("security", "Social Engineering"),
    ("security", "Malware Analysis"), ("security", "Web Application Security"),
    ("security", "Firewalls & IDS/IPS"), ("security", "Zero Trust Architecture"),
    ("security", "Threat Intelligence"), ("security", "Incident Response"),
    ("security", "Digital Forensics"), ("security", "Identity & Access Management"),
    ("security", "Vulnerability Management"), ("security", "OWASP Top 10"),
    ("security", "Cloud Security"), ("security", "SIEM & Log Monitoring"),
    ("security", "Ethical Hacking Methodology"), ("security", "Ransomware & Extortion Tactics"),
]

current_hour = datetime.now().hour
category, target_topic = topics[current_hour % len(topics)]

print(f"⏳ Learning about: {target_topic} ({category})")

# --- Use Gemini free tier ---
api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found. Add it as a repo secret.")
    exit(1)

print("✅ API key found. Calling Gemini...")

if category == "language":
    role = "a senior software architect and programming language theorist"
    sections = """
<h3>1. Core Logic & Design Philosophy</h3>
<p>Why was it created? What problems does it solve? (OOP, Functional, Procedural?)</p>

<h3>2. Syntax, Structure & Flow</h3>
<p>Key syntactic rules, indentation vs braces, semicolons, how code is organized.</p>

<h3>3. Memory Management</h3>
<p>Garbage collection, manual memory, ownership (like Rust), or reference counting.</p>

<h3>4. Paradigms & Tactics</h3>
<p>How it handles OOP, concurrency (threads, async), error handling (exceptions or results).</p>

<h3>5. Unique Patterns & Ecosystem</h3>
<p>Famous frameworks, design patterns commonly used in this language.</p>

<h3>6. How it "Makes Sense" (Internal Logic)</h3>
<p>Explain the internal logic of the language and how a programmer thinks in it.</p>
"""
else:  # security
    role = "a senior cybersecurity analyst and educator"
    sections = """
<h3>1. What It Is & Why It Matters</h3>
<p>Core definition and the real-world risk or problem it addresses.</p>

<h3>2. How It Works</h3>
<p>The underlying mechanics, techniques, tools, or processes involved.</p>

<h3>3. Common Attack/Defense Techniques</h3>
<p>Widely used offensive techniques and corresponding defensive measures.</p>

<h3>4. Real-World Examples</h3>
<p>Notable incidents, breaches, or practical scenarios illustrating the topic.</p>

<h3>5. Tools & Frameworks</h3>
<p>Industry-standard tools, frameworks, or compliance standards related to this topic.</p>

<h3>6. How a Security Professional Thinks About It</h3>
<p>The mindset, risk model, or approach an analyst/pentester brings to this topic.</p>
"""

prompt = f"""
Act as {role}.
Provide a deep, educational breakdown of the topic: {target_topic}.

Structure your response as clean HTML with these exact sections:
<h2>🔍 Deep Dive: {target_topic}</h2>
<p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</p>
{sections}
Return ONLY the HTML block. No markdown formatting, no extra text outside the HTML.
"""

# --- Gemini's OpenAI-compatible endpoint ---
url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "gemini-2.5-flash",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.8,
    "max_tokens": 2000
}

# --- Call the API ---
try:
    print("📡 Sending request to Gemini...")
    response = requests.post(url, headers=headers, json=data, timeout=120)

    print(f"📊 HTTP Status Code: {response.status_code}")

    if response.status_code != 200:
        print(f"❌ API Error Response: {response.text}")
        exit(1)

    result = response.json()
    html_content = result['choices'][0]['message']['content']
    print("✅ Successfully received response from Gemini")

except Exception as e:
    print(f"❌ Request failed with exception: {e}")
    exit(1)

# --- Save to knowledge log ---
log_file = 'knowledge_log.json'

if os.path.exists(log_file):
    with open(log_file, 'r') as f:
        log = json.load(f)
else:
    log = []

log.append({
    "topic": target_topic,
    "category": category,
    "html": html_content,
    "timestamp": datetime.now().isoformat()
})

if len(log) > 50:
    log = log[-50:]

with open(log_file, 'w') as f:
    json.dump(log, f)

# --- Build the webpage ---
page_html = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Knowledge Base</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, sans-serif; max-width: 1000px; margin: 30px auto; padding: 20px; background: #f8f9fa; }
        h1 { color: #0d6efd; }
        .lesson { background: white; padding: 25px; margin-bottom: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 5px solid #0d6efd; }
        .timestamp { color: #6c757d; font-size: 0.9em; }
        hr { margin: 40px 0; }
        footer { text-align: center; color: #6c757d; margin-top: 30px; }
    </style>
</head>
<body>
    <h1>🧠 AI Knowledge Base</h1>
    <p>This page is automatically updated hourly by Gemini (free tier).
       It learns the logic, structure, and patterns of programming languages and cybersecurity topics.</p>
    <hr>
"""

for entry in reversed(log):
    page_html += f"<div class='lesson'>{entry['html']}</div><hr>"

page_html += """
    <footer>🔄 Updated hourly by Gemini (free tier). No human interaction required.</footer>
</body>
</html>
"""

with open('index.html', 'w') as f:
    f.write(page_html)

print(f"✅ Successfully added lesson for {target_topic}. Total lessons stored: {len(log)}")
