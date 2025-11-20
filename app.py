import smtplib
import ssl
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for

load_dotenv("env.config")

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_portfolio_2025')

# Data for the portfolio
PROJECTS = [
    {
        "title": "Sentiment Analysis",
        "description": "Analyzed customer reviews to determine sentiment polarity using NLP techniques.",
        "tags": ["Python", "NLP", "Scikit-Learn"]
    },
    {
        "title": "Phishing Classifier",
        "description": "Built a machine learning model to detect phishing URLs with high accuracy.",
        "tags": ["Python", "ML", "Pandas"]
    },
    {
        "title": "Crop Disease Detection",
        "description": "Computer vision model to identify diseases in crops from leaf images.",
        "tags": ["Deep Learning", "TensorFlow", "CNN"]
    },
    {
        "title": "Child Birth Weight Prediction",
        "description": "Predictive model to estimate birth weight based on maternal health data.",
        "tags": ["Data Science", "Regression", "Healthcare"]
    },
    {
        "title": "Personal AI Assistant",
        "description": "Voice-activated AI assistant capable of performing daily tasks and answering queries.",
        "tags": ["AI", "Speech Recognition", "API Integration"]
    },
    {
        "title": "Market-Cap Crop Dashboard",
        "description": "Interactive dashboard visualizing crop market trends and capitalization.",
        "tags": ["Power BI", "Data Viz", "Analytics"]
    }
]

SKILLS = [
    "Python", "Pandas", "NumPy", "SQL", "Machine Learning", 
    "Deep Learning", "NLP", "Generative AI", "Scikit-Learn", 
    "Data Visualization", "MongoDB", "Docker", "Kubernetes", 
    "MLOps", "Power BI", "GitHub"
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=PROJECTS)

@app.route('/skills')
def skills():
    return render_template('skills.html', skills=SKILLS)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Email Configuration
        smtp_server = "smtp.gmail.com"
        port = 587
        sender_email = "poornachandradh34@gmail.com"
        password = os.environ.get("EMAIL_PASSWORD", "").replace(" ", "")
        
        if not password:
            flash("Email password not configured. Please set EMAIL_PASSWORD environment variable.", "error")
            return render_template('contact.html')

        context = ssl.create_default_context()
        
        try:
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls(context=context)
                server.login(sender_email, password)
                
                email_content = f"Subject: Portfolio Contact from {name}\n\nName: {name}\nEmail: {email}\n\nMessage:\n{message}"
                
                server.sendmail(sender_email, sender_email, email_content)
                flash("Message sent successfully!", "success")
                return redirect(url_for('contact'))
        except Exception as e:
            print(f"Error: {e}")
            flash("Failed to send message. Please try again.", "error")
            
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
