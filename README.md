# Reimbursement-Portal
Reimbursement Portal is an online portal where an employee can submit reimbursement claims  related to relocation, medical, and office supplies and the assigned manager can approve/reject  the claims.

## Getting Started

Welcome to this awesome project! Follow these steps to get up and running on your machine.

**Prerequisites**

Before you begin, make sure you have the following installed on your system:

* Python 3.7+
* Git

**Clone the Repository**

First,Navigate to the Directory where you want to Clone the Repository:

Use the cd command to change directories.
For example, if you want to clone the repository into a folder called projects in your home directory,
you would run: 
```
cd ~/projects
```
Copy the URL provided below.
```
git clone https://github.com/gh-gaurav/Reimbursement-Portal.git
```

**Setting Up a Virtual Environment**

It's a good practice to use a virtual environment to manage dependencies.
Run the following commands to create a virtual environment:

For Windows
```
python -m venv venv
```

For macOS and Linux:
```
python3 -m venv venv
```

Now to activate the virtual environment
For Windows:
```
myenv\Scripts\activate
```
For macOS and Linux::
```
source myenv/bin/activate
``````


Install Dependencies

__Your requirements.txt includes the following dependencies:__

makefile
```
alembic==1.13.1
Flask==3.0.3
Flask-Migrate==4.0.7
Flask-SQLAlchemy==3.1.1
itsdangerous==2.2.0
Jinja2==3.1.4
PyMySQL==1.1.0
SQLAlchemy==2.0.30
Werkzeug==3.0.3
```
Now, install the required dependencies using pip:

```
pip install -r requirements.txt
```


Database Migration

Before running the application, you'll need to set up the database.
Run the following commands to apply the database migrations:


```
flask db upgrade
```

Running the Application

You’re all set! Start the Flask application by running:

```
flask run
```
Open your browser and navigate to http://127.0.0.1:5000 to see your application in action.
Enjoy!

Feel free to explore the code, make changes, and contribute. If you have any questions or encounter any issues, don’t hesitate to open an issue on GitHub. Happy coding!
