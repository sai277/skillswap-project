# SkillSwap Project 💡

SkillSwap is a Django-based web application that enables users to connect, schedule sessions, and exchange skills such as mentorship, tutoring, or collaborative learning. The platform supports session booking, feedback submission, and role-based access for mentors and learners.

> _Coming soon or hosted locally_

## 🚀 Features

- 👥 User authentication (Login/Signup)
- 🔄 Role-based access: Mentor & Learner
- 📆 Schedule and manage session requests
- ✅ Accept/Reject session invitations
- 📝 Feedback system (with thumbs up/down and comments)
- 📊 Dashboard for learners and mentors
- 💬 Private messaging and optional comments
- 📷 Image and profile management
- 🔒 Secure routes and session validations

## 🛠 Tech Stack

- **Backend:** Django, SQLite3
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Auth:** Django's built-in authentication system
- **Deployment:** GitHub (for now)

## 📂 Project Structure

```plaintext
skillswap-project/
├── feedback/              # Feedback app (user ratings/comments)
├── session_requests/      # Session management between users
├── accounts/              # User authentication and profile logic
├── templates/             # HTML templates
├── static/                # Static files (CSS/JS/Images)
├── db.sqlite3             # Default Django database
├── manage.py              # Django entry point
