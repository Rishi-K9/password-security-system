
# Password Security & Authentication Analysis

## Project Overview
This project is an educational cybersecurity application developed using Python and Flask. It demonstrates secure password handling and basic authentication security practices.

## Objectives
- Understand secure password storage.
- Implement password strength evaluation.
- Demonstrate user registration and login.
- Track failed login attempts.
- Implement temporary account lockout.
- Record authentication security events.

## Technologies Used
- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Werkzeug
- GitHub
- Python Logging

## Features

### 1. User Registration
Allows users to create accounts using a username and password.

### 2. Password Hashing
Uses Werkzeug password hashing instead of storing plaintext passwords.

### 3. Password Strength Checker
Evaluates password length and character diversity.

### 4. Password Policy
Requires uppercase letters, lowercase letters, numbers, special characters and at least 8 characters.

### 5. Login Authentication
Verifies submitted passwords against stored password hashes.

### 6. Failed Login Tracking
Tracks unsuccessful login attempts.

### 7. Account Lockout
Temporarily locks accounts after five unsuccessful login attempts.

### 8. Security Logging
Records registration, successful login, failed login and account lockout events.

## Project Structure

password-security-system/
│
├── app.py
├── requirements.txt
├── Procfile
├── .gitignore
├── README.md
│
└── templates/
    └── index.html

## Installation

Install dependencies:

pip install -r requirements.txt

Set the Flask secret key using an environment variable:

SECRET_KEY=your-secure-random-secret

Run the application:

python app.py

## Security Practices
- Never store plaintext passwords.
- Use established password hashing libraries.
- Use parameterized SQL queries.
- Limit repeated failed login attempts.
- Avoid logging passwords or sensitive information.
- Use HTTPS in deployment.
- Use synthetic accounts for testing.

## Testing
The application was tested using synthetic accounts.

Tests include:
- User registration.
- Correct password authentication.
- Incorrect password rejection.
- Failed login tracking.
- Temporary account lockout.

## Limitations
This is an educational demonstration and is not intended for production authentication without additional security controls.

## Conclusion
The project demonstrates fundamental password security and authentication concepts and provides practical experience in developing a basic defensive cybersecurity application.

## Author
Internship Project
