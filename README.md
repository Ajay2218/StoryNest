
---

# 🚀 StoryNest – Online Bookstore 

StoryNest is a full-stack e-commerce web application built using Django that allows users to browse, explore, and purchase books online. It provides a seamless shopping experience with product filtering, cart management, and secure payment integration.

---

## 🌟 Features

* 🏠 Dynamic homepage with featured books
* 📚 Product listing with category-based filtering
* 🔍 Search and filtered product view
* 📄 Individual product detail page
* 🛒 Add to cart and cart management
* 💳 Secure checkout system
* 💰 Online payment integration using Razorpay
* 🔐 User authentication (Register/Login)
* 📱 Responsive user interface

---

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite
* **Payment Gateway:** Razorpay
* **Tools:** Git, GitHub

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally:

### 1. Clone the Repository

```bash
git clone <repository-url>
cd storynest
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configuration

* Ensure `settings.py` is properly configured
* Add Razorpay API keys in settings
* Set `DEBUG = True` for development
* Configure `ALLOWED_HOSTS` if required

### 6. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Run the Server

```bash
python manage.py runserver
```

### 9. Access the Application

* 🌐 Home: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📂 Project Structure

* **StoryNest/**: Project configuration, settings, and main URL routing
* **Store/** (or your app name): Handles product listing, filtering, and product details
* **Cart/**: Manages cart operations and checkout process
* **Orders/**: Handles order processing and payment integration
* **media/**: Stores uploaded product images
* **static/**: Contains global CSS, JavaScript, and UI assets

---


