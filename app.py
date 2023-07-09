from flask import Flask, render_template, request, redirect, flash, make_response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
wentToCollege = False
from random import randrange

app = Flask(__name__)

job_opportunities = [
    {"title": "Software Engineer", "company": "ABC Tech", "location": "San Francisco"},
    {"title": "Project Manager", "company": "XYZ Inc.", "location": "New York"},
    # Add more job opportunities here...
]
quotes = [
    "Healing takes time, and asking for support is a courageous step towards reclaiming your life.",
    "The greatest healing therapy is friendship and love.",
    "You are not alone. Your strength and resilience will guide you towards healing.",
    "Your scars are a testament to your strength. Keep fighting, and the wounds will transform into wisdom.",
    "Healing begins when we validate our pain and choose to seek help.",
    "PTSD is not a sign of weakness. It is a reminder of your strength to survive.",
    "Your past does not define your future. Your bravery and resilience will guide you towards a brighter tomorrow.",
    "You are not broken; you are a warrior on a journey of healing.",
    "In the midst of darkness, there is always a glimmer of hope. Keep searching for that light.",
    "Healing is not a destination; it's a journey. Be patient with yourself and celebrate every step forward."
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jobs')
def jobs():
    # return render_template('jobs.html', jobs=job_opportunities)
    return render_template('jobs2.html')

@app.route('/therapist')
def therapist():
    
    return render_template("therapist.html")

@app.route('/resume', methods=['GET', 'POST'])
def resume():
    if request.method=="GET":
        return render_template('resume.html')
    if request.method == 'POST':
        data=request.form
        userName=data["userName"]
        userEmail=data["userEmail"]
        userLoc=data["userLoc"]
        userNumber=data["userNumber"]
        userHSName=data["userHSName"]
        userHSGPA=data["userHSGPA"]
        userHSClasses=data["userHSClasses"]
        userHSClasses = userHSClasses.split()
        userCollegeName=data["userCollegeName"]
        userWK1 = data["userWK1"]
        userWK2 = data["userWK2"]
        userWK3 = data["userWK3"]
        if userCollegeName!="":
            userCollegeGPA=data["userCollegeGPA"]
            userCollegeMajor=data["userCollegeMajor"]
            userCollegeOrganizations=data["userCollegeOrganizations"]
            userCollegeOrganizations = userCollegeOrganizations.split()
            wentToCollege=True
            pdf_buffer = generate_resume_pdf(userName, userEmail, userNumber, userHSName, userHSGPA, userHSClasses, userCollegeName, userCollegeGPA, userCollegeMajor, userCollegeOrganizations, userWK1, userWK2, userWK3)
        else:
            pdf_buffer = generate_resume_pdf(userName, userEmail, userNumber, userHSName, userHSGPA, userHSClasses, userWK1, userWK2, userWK3)
        print(userName,userEmail,
        userLoc,
        userNumber,
        userHSName,
        userHSGPA,
        userHSClasses,
        userCollegeName)
        
    
        # Create a response with the PDF as attachment
        response = make_response(pdf_buffer)
        response.headers['Content-Disposition'] = 'attachment; filename=my_resume.pdf'
        response.headers['Content-Type'] = 'application/pdf'
    
        return response

def generate_resume_pdf(name, email, phone, high_school, high_school_gpa, high_school_classes, wk1, wk2, wk3):
    buffer = BytesIO()
    doc = canvas.Canvas(buffer, pagesize=letter)

    # Set up the content
    doc.setFont("Helvetica-Bold", 16)
    doc.drawString(50, 750, "Resume")
    
    doc.setFont("Helvetica", 12)
    doc.drawString(50, 700, "Name: {}".format(name))
    doc.drawString(50, 680, "Email: {}".format(email))
    doc.drawString(50, 660, "Phone: {}".format(phone))
    doc.drawString(50, 620, "High School: {}".format(high_school))
    doc.drawString(50, 600, "High School GPA: {}".format(high_school_gpa))
    for i in range(0, len(high_school_classes), 1):
        doc.drawString(50, 600-20*(i+1), "High School Class: {}".format(high_school_classes[i]))
    x = 600-20*(len(high_school_classes) + 1)
    x -= 0
    doc.drawString(50, x, "Work Experience #1: {}".format(wk1))
    doc.drawString(50, x-20, "Work Experience #2: {}".format(wk2))
    doc.drawString(50, x-40, "Work Experience #3: {}".format(wk3))
    
    doc.showPage()
    doc.save()
    
    buffer.seek(0)
    return buffer


def generate_resume_pdf(name, email, phone, high_school, high_school_gpa, high_school_classes, college, college_gpa, college_major, college_organizations, wk1, wk2, wk3):
    buffer = BytesIO()
    doc = canvas.Canvas(buffer, pagesize=letter)

    # Set up the content
    doc.setFont("Helvetica-Bold", 16)
    doc.drawString(50, 750, "Resume")

    doc.setFont("Helvetica", 12)
    doc.drawString(50, 700, "Name: {}".format(name))
    doc.drawString(50, 680, "Email: {}".format(email))
    doc.drawString(50, 660, "Phone: {}".format(phone))

    doc.setFont("Helvetica-Bold", 14)
    doc.drawString(50, 620, "Education")
    doc.setFont("Helvetica", 12)
    doc.drawString(50, 600, u"\u2022 High School: {}".format(high_school))
    doc.drawString(50, 580, u"\u2022 High School GPA: {}".format(high_school_gpa))

    doc.setFont("Helvetica-Bold", 14)
    doc.drawString(50, 540, "High School Classes")
    doc.setFont("Helvetica", 12)
    for i in range(0, len(high_school_classes), 1):
        doc.drawString(50, 520-20*(i), u"\u2022 {}".format(high_school_classes[i]))

    x = 520- 20*(len(high_school_classes)-1)
    x -= 40

    doc.setFont("Helvetica-Bold", 14)
    doc.drawString(50, x, "College")
    doc.setFont("Helvetica", 12)
    doc.drawString(50, x-20, u"\u2022 College: {}".format(college))
    doc.drawString(50, x-40, u"\u2022 College GPA: {}".format(college_gpa))
    doc.drawString(50, x-60, u"\u2022 College Major: {}".format(college_major))

    doc.setFont("Helvetica-Bold", 14)
    doc.drawString(50, x-100, "College Organizations")
    doc.setFont("Helvetica", 12)
    for i in range(0, len(college_organizations), 1):
        doc.drawString(50, x-100-20*(i+1), u"\u2022 {}".format(college_organizations[i]))

    y = x- 100 - 20 *(len(college_organizations))
    y-= 40

    doc.setFont("Helvetica-Bold", 14)
    doc.drawString(50, y, "Work Experience")
    doc.setFont("Helvetica", 12)
    doc.drawString(50, y-20, u"\u2022 Work Experience #1: {}".format(wk1))
    doc.drawString(50, y-40, u"\u2022 Work Experience #2: {}".format(wk2))
    doc.drawString(50, y-60, u"\u2022 Work Experience #3: {}".format(wk3))


    doc.showPage()
    doc.save()
    
    buffer.seek(0)
    return buffer

@app.route('/interview-prep')
def interview_prep():
    return render_template('interview_prep.html')

if __name__ == '__main__':
    app.run(debug=True)
