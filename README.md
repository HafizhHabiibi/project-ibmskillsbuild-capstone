📝 To-Do List App – IBM SkillsBuild Capstone Project

A simple and powerful web-based task management application built with Flask and PostgreSQL. 
This project is developed as part of the IBM SkillsBuild Capstone Program, focusing on fundamental full-stack web development with database integration and modern development practices.

🚀 Project Overview

The purpose of this project is to create a functional and user-friendly To-Do List application that allows users to register, log in, and manage their daily tasks.
This project was built to solve a common problem: how to manage personal tasks efficiently in a minimal yet effective digital tool. 
The development process followed a structured approach, from designing the database schema and backend routes to implementing a clean and responsive UI.

🛠️ Tech Stack

- Backend: Flask (Python), Flask-SQLAlchemy, Flask-Migrate
- Database: PostgreSQL (deployed on Railway)
- Deployment: Railway
- Environment Management: dotenv
- AI Support Tool: IBM Granite model (via Replicate API on Google Colab)

To enhance documentation, the IBM Granite LLM model was used to automatically generate concise, readable comments for blocks of code. 
This improves the maintainability and accessibility of the code for collaborators and reviewers.

🔐 Features

✅ User Registration
Allows new users to register securely with a username and password.

🔐 User Login
Secure login system to access personalized task lists.

➕ Add Task
Users can create new tasks with a simple form.

✏️ Edit Task
Tasks can be edited to update details or correct entries.

🗑️ Delete Task
Tasks can be deleted when no longer needed.

📋 Task Listing
All tasks are displayed clearly in a dashboard-style layout.

⚙️ Installation & Setup (Local)

1. Clone the repo:
  ```
    git clone https://github.com/HafizhHabiibi/project-ibmskillsbuild-capstone.git
  ```

2. Create and activate virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate 
   ```
   
3. Install dependencies:
  ```
    pip install -r requirements.txt
  ```

4. Set up your .env file with the following:
  ```
    FLASK_ENV=development
    FLASK_APP=app
    DATABASE_URL=your_database_uri_here
  ```

5. Run database migrations:
  ```
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
  ```

6.  Run the app:
  ```
    flask run
  ```

🌐 Live Demo

https://project-ibmskillsbuild-to-dolist-habiibi.up.railway.app

👨‍💻 Author

Hafizh Habiibi Lubis

Capstone Project - IBM SkillsBuild Indonesia

GitHub: [HafizhHabiibi]
