# Assignment Management System

## Project Overview
The Assignment Management System is a web-based application designed to simplify and manage the academic assignment workflow. It helps instructors create and publish assignments, allows learners to submit their work, and supports rubric-based grading, feedback, resubmissions, and appeals.

## Technologies Used
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI
- **Database:** MySQL
- **Database Tool:** MySQL Workbench

## Key Features
- Course and learner management
- Assignment creation and publication
- Learner enrollment in courses
- Online assignment submissions
- Submission tracking and status management
- Rubric-based grading
- Feedback management
- Resubmission handling
- Grade appeal management
- Audit logs for tracking important changes

## Project Structure
```text
Assignment-Management-System/
│
├── app/
│   ├── main.py
│   ├── models/
│   └── routes/
│
├── static/
│   ├── index.html
│   ├── css/
│   └── js/
│
├── database/
│   ├── schema.sql
│   └── demo_seed.sql
│
├── scripts/
├── data/
├── docs/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Assignment-Management-System.git
```

### 2. Open the Project Folder
```bash
cd Assignment-Management-System
```

### 3. Create a Virtual Environment
```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

Windows:
```bash
venv\Scripts\activate
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

### 6. Configure MySQL
- Open MySQL Workbench.
- Create the `assignment_management` database.
- Execute the SQL script inside the `database` folder.
- Configure your MySQL connection details in the `.env` file.

### 7. Run the Application
```bash
uvicorn app.main:app --reload
```

Open your browser and visit:

`http://127.0.0.1:8000`

## Database
The project uses MySQL to store:
- Courses
- Learners
- Enrollments
- Assignments
- Rubrics and criteria
- Submissions
- Grades and feedback
- Resubmissions
- Appeals
- Audit events

## Future Enhancements
- Role-based authentication
- Email notifications
- Assignment file uploads
- Advanced analytics and reports
- Automated deadline reminders

## Author
Developed as an academic project using Python FastAPI, MySQL, HTML, CSS, and JavaScript.
