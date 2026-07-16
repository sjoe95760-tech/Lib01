import requests
import os
import json
from datetime import datetime

# --- List of all major programming languages to learn ---
languages = [
    "Python", "JavaScript", "Java", "C++", "C#", 
    "Go", "Rust", "Swift", "Kotlin", "TypeScript", 
    "Ruby", "PHP", "SQL", "HTML/CSS", "Scala", "Perl"
]

# --- Pick one language based on the current hour (so it rotates automatically) ---
current_hour = datetime.now().hour
target_language = languages[current_hour % len(languages)]

print(f"⏳ Learning about: {target_language}")

# --- 1. Ask DeepSeek to teach us about this language ---
deepseek_key = os.environ['DEEPSEEK_API_KEY']

prompt = f"""
Act as a senior software architect and programming language theorist.
Provide a deep, educational breakdown of the programming language: {target_language}.

Structure your response as clean HTML with these exact sections:
<h2>🔍 Deep Dive: {target_language}</h2>
<p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</p>

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

Return ONLY the HTML block. No markdown formatting, no extra text outside the HTML.
"""

headers = {
    'Authorization': f'Bearer {deepseek_key}',
    'Content-Type': 'application/json'
}

data = {
    'model': 'deepseek-chat',
    'messages': [{'role': 'user', 'content': prompt}],
    'temperature': 0.8,
    'max_tokens': 1500
}

# Call the DeepSeek API
ds_response = requests.post(
    'https://api.deepseek.com/v1/chat/completions',
    headers=headers,
    json=data
)

result = ds_response.json()
html_content = result['choices'][0]['message']['content']

# --- 2. Read the existing knowledge log (history) ---
log_file = 'knowledge_log.json'

if os.path.exists(log_file):
    with open(log_file, 'r') as f:
        log = json.load(f)
else:
    log = []

# --- 3. Append the new lesson to the log ---
log.append({
    "language": target_language,
    "html": html_content,
    "timestamp": datetime.now().isoformat()
})

# Keep only the last 50 lessons to prevent the file from getting too big
if len(log) > 50:
    log = log[-50:]

# Save the updated log
with open(log_file, 'w') as f:
    json.dump(log, f)

# --- 4. Build the new index.html page from the entire log ---
page_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>AI Learns Programming Languages</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; max-width: 1000px; margin: 30px auto; padding: 20px; background: #f8f9fa; }}
        h1 {{ color: #0d6efd; }}
        .lesson {{ background: white; padding: 25px; margin-bottom: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 5px solid #0d6efd; }}
        .timestamp {{ color: #6c757d; font-size: 0.9em; }}
        hr {{ margin: 40px 0; }}
        footer {{ text-align: center; color: #6c757d; margin-top: 30px; }}
    </style>
</head>
<body>
    <h1>🧠 AI's Programming Knowledge Base</h1>
    <p>This page is automatically updated every hour by DeepSeek AI. 
       It learns the logic, structure, and patterns of every known programming language.</p>
    <hr>
"""

# Display the lessons (newest first)
for entry in reversed(log):
    page_html += f"<div class='lesson'>{entry['html']}</div><hr>"

page_html += """
    <footer>🔄 Updated hourly by DeepSeek AI. No human interaction required.</footer>
</body>
</html>
"""

# Write the new index.html
with open('index.html', 'w') as f:
    f.write(page_html)

print(f"✅ Successfully added lesson for {target_language}. Total lessons stored: {len(log)}")
