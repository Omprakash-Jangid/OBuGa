
# 📋 OBuGa – Private Attendance Tracker

**OBuGa** is a web-based application designed to streamline employee attendance management. It offers features like employee records, attendance tracking, task assignments, and status updates, all within a secure and user-friendly interface.

---

## 🛠️ Features

- **Employee Management**: Maintain comprehensive employee profiles.
- **Attendance Tracking**: Record and monitor daily attendance.
- **Task Assignment**: Allocate tasks to employees with deadlines.
- **Status Updates**: Track the progress of assigned tasks.
- **Secure Access**: Ensure data privacy with authentication mechanisms.

---

## 🚀 Technologies Used

- **Backend**: Python with Django
- **Database**: SQLite
- **Environment**: Virtual environment (`obuga_env`)
- **Deployment**: Not specified

---

## 📂 Project Structure

```OBuGa/
│
├── obuga_env/ # Virtual environment
├── obuga_project/ # Django project files
├── attendance/ # Attendance app
├── manage.py # Django management script
├── db.sqlite3 # SQLite database
└── requirements.txt # Project dependencies```
```


---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Omprakash-Jangid/OBuGa.git
cd OBuGa
python -m venv obuga_env
source obuga_env/bin/activate  # On Windows: obuga_env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```



