import smtplib
import ssl
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory

load_dotenv("env.config")

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_portfolio_2025')

# Assets
RESUME_FILENAME = "resume_update_1.pdf"

# Data for the portfolio
PROJECTS = [
    {
        "title": "Myntra_scrapper",
        "description": "web scraping application designed to extract and analyze customer reviews from the Myntra e-commerce platform",
        "tags": ["Python", "ML", "Scikit-Learn"]
    },
    {
        "title": "Phishing Classifier",
        "description": "Built a machine learning model to detect phishing URLs with high accuracy.",
        "tags": ["Python", "ML", "Pandas"]
    },
    {
        "title": "Climate_visibility",
        "description": "To develop a machine learning model that can accurately predict the maximum visibility distance in a given location and weather condition.",
        "tags": ["Flask", "K-Means", "Logistic Reg", "Scikit-Learn"]
    },
    {
        "title": "ResearchLens",
        "description": "research paper analysis tool that lets you upload any academic paper and interact with it through 4 specialized analysis modes",
        "tags": ["Flask", "LLM", "LangChain" , "RAG" , "Supabase"]
    },
    {
        "title": "Personal Angry AI Assistant",
        "description": "Angry AI assistant capable of performing daily tasks and answering queries.",
        "tags": ["AI", "LangChain", "API Integration" , "AngryAI"]
    },
    {
        "title": "Brain Tumor Detection",
        "description": "A deep learning–powered web application for brain tumor segmentation using YOLOv11n.",
        "tags": ["Flask", "YOLOv11n", "Deep learning" ,"Computer Vision"]
    },
    {
        "title": "Helmet Detection",
        "description": "Real-time helmet detection using YOLOv8 for industrial safety applications.",
        "tags": ["YOLOv8", "Computer-Vision", "Deep Learning"]
    },
    {
        "title": "Customer_category",
        "description": "Categoring the customers based on their purchase history and demographics",
        "tags": ["Clustering", "ML", "Python"]
    },
    
]

SKILLS = [
    "Python", "Pandas", "NumPy", "SQL", "Machine Learning", 
    "Deep Learning", "NLP", "Generative AI", "Scikit-Learn", 
    "Data Visualization", "MongoDB", "Docker", "Kubernetes", 
    "MLOps", "Power BI", "GitHub" , "Computer Vision" , "LLM" , 
    "HuggingFace","LangChain" , "Flask"
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

@app.route('/resume')
def download_resume():
    resume_path = os.path.join(app.root_path, RESUME_FILENAME)
    if os.path.exists(resume_path):
        return send_from_directory(app.root_path, RESUME_FILENAME, as_attachment=True)
    flash("Resume file is missing. Please check back later.", "error")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
