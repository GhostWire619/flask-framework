# Flask-Framework 🌐

## Description

Flask-Framework is an open-source Python project that helps you set up a full Flask project environment quickly. It comes with pre-written code for Authentication and includes the following features:

- **🧩 Flask-Restx**: Provides a structured and documented REST API.
- **🔐 JWT and Werkzeug powered authentication**: Secure user authentication with JSON Web Tokens and Werkzeug for Flask.
- **📘 Full documentation**: Guides for integrating with **React TypeScript**, ensuring a seamless connection between your backend and frontend.

### Key Features:

- **✅ Pre-written authentication setup**: Includes signup, login, and logout functionalities.
- **🔌 Easy integration**: Quickly integrate with your existing Flask project.
- **📊 Scalable and modular**: Designed to be easily extended for additional features.

## Instructions for Running the Project

To run the project, follow these steps:

0. **Download the create_flask_app.py file and put it in a folder for your new project and run it**

   - **for Python**

   ```bash
   python create_flask_app.py
   ```

   - **or for Python3**

   ```bash
   python3 create_flask_app.py
   ```

1. **Navigate to the project directory:**

   ```bash
   cd your_project_directory
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - **On Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **On Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations to set up the database:**
   a. **Initialize migrations:**

   ```bash
   python manage.py db init
   ```

   b. **Generate migration scripts:**

   ```bash
   python manage.py db migrate -m "Initial migration"
   ```

   c. **Apply migrations:**

   ```bash
   python manage.py db upgrade
   ```

6. **Run the application:**
   ```bash
   python manage.py run
   ```

## Updating the Requirements File

If you need to update the `requirements.txt` file to reflect new or updated dependencies, follow these steps:

1. Ensure your virtual environment is active.

   - **On Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **On Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```

2. Install the new or updated dependencies using `pip install`:

   ```bash
   pip install package_name
   ```

3. Freeze the current dependencies into the `requirements.txt` file:

   ```bash
   pip freeze > requirements.txt
   ```

4. **Commit the updated `requirements.txt` to your version control system**:
   ```bash
   git add requirements.txt
   git commit -m "Update requirements.txt"
   ```

---

### Tags

- **Flask**
- **Python**
- **Open Source**
- **Authentication**
- **Flask-Restx**
- **JWT**
- **Werkzeug**
- **React TypeScript**
- **Scalable**
- **Modular**
- **Documentation**
