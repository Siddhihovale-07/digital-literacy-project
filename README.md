# Digital Literacy Training for Senior Citizens – CEP Web Application

A simple college CEP web application built with Flask, SQLite, HTML, CSS and JavaScript.

## Features

- Home page
- About CEP project
- 8 digital learning modules
- Step-by-step lessons
- Browser text-to-speech button
- Pre-training survey
- Post-training survey
- SQLite storage for survey responses
- Results dashboard with Chart.js charts
- Cyber safety page
- Participant feedback
- Sample certificate page
- Project dashboard for survey records
- Responsive mobile-friendly design

## Important

The application does not contain fake field results. The Results page starts at zero and updates when you submit survey responses. For the final CEP report, use actual data collected from your community activity.

## Run in VS Code

### 1. Open the project folder

Open `DigitalLiteracyCEP` in VS Code.

### 2. Create a virtual environment (recommended)

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Flask

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open in browser

Go to:

`http://127.0.0.1:5000`

The SQLite database file `database.db` will be created automatically the first time the application starts.

## Pages

- `/` – Home
- `/about` – Project information
- `/modules` – Learning modules
- `/survey/pre` – Pre-training survey
- `/survey/post` – Post-training survey
- `/results` – Results and charts
- `/safety` – Cyber safety
- `/feedback` – Feedback form
- `/certificate` – Certificate
- `/admin` – Project dashboard

## How to use it for the CEP activity

1. Meet senior citizens with permission.
2. Explain the purpose of the project.
3. Complete the pre-training survey.
4. Teach the selected digital modules.
5. Let participants practise.
6. Complete the post-training survey.
7. Collect feedback.
8. Take project photographs only with appropriate permission.
9. Use the Results page for your report's data analysis.
