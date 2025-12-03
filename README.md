🎨 Multi-Vendor Painting E-Commerce Website (Django Project)

This is a complete Django-based e-commerce platform where artists can sign up as sellers, list and manage their paintings, view orders, respond to customer queries, and track monthly revenue. Buyers can browse paintings, ask product questions, and place orders.


---

✅ Features

Seller and buyer login

Add/update/delete products (paintings)

Customer product queries with seller replies

Cart and single-product checkout system

Order management with shipping and delivery status

Monthly revenue graph for sellers

Admin panel for managing everything



---

🖥️ 1. Install Python & VS Code

🔹 Install Python

Go to: https://www.python.org/downloads/

Download Python (3.10 or newer)

During installation, check the box ✅ “Add Python to PATH”

To confirm installation, open terminal or command prompt and run:


python --version

🔹 Install Visual Studio Code (VS Code)

Go to: https://code.visualstudio.com/

Download and install VS Code for your OS

Recommended extensions:

Python (by Microsoft)

Django Template

GitLens




---

⚙️ 2. Clone the Project

Open VS Code → Terminal → run:

git clone https://github.com/ashish-mitra/ecom.git
cd painting-ecommerce

If you're not using GitHub, just open the folder directly in VS Code.


---

🧪 3. Create & Activate Virtual Environment

# Create virtual environment
python -m venv env

# Activate it:
# Windows:
env\Scripts\activate

# Mac/Linux:
source env/bin/activate


---

📦 4. Install Django & Dependencies

pip install -r requirements.txt

(You can also run if it exists)

To save installed packages:

pip freeze > requirements.txt


---

🗄️ 5. Migrate Database & Create Admin

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # follow the prompts


---

▶️ 6. Run the Server

python manage.py runserver

Now open your browser and go to:
👉 http://127.0.0.1:8000/


---

🎨 7. Tailwind CSS (Development Only or Offline Use)

Using CDN (Quick method):

Include the CDN in your base template:

<script src="https://cdn.tailwindcss.com"></script>

Using Offline Tailwind CSS (Optional)

1. Install Node.js from https://nodejs.org/


2. In terminal:



npm install -D tailwindcss
npx tailwindcss init

3. Create input.css with:



@tailwind base;
@tailwind components;
@tailwind utilities;

4. Build CSS:



npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch

5. Link output.css in your base template instead of CDN.




---

🧱 8. Project Structure Overview

painting-ecommerce/
│
├── core/                # Main Django app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── static/
│   └── css/, js/, images/
│
├── media/               # Uploaded files
├── db.sqlite3
├── manage.py
└── requirements.txt


---

🧾 9. Basic Django Commands

# Start a new app
python manage.py startapp appname

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver


---

🧑‍💻 10. Admin Panel

Go to: http://127.0.0.1:8000/admin/
Login with your superuser credentials.


---

💬 Questions / Support

For any issues, feel free to connect or raise a GitHub issue (if hosted).
Happy coding! 💻🖌️




