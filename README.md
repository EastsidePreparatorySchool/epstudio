# EPStudio

**EPStudio** is a web application designed to help students document and showcase their creations. Whether it's artwork, projects, or any creative work, EPStudio provides a platform for students to share their creations with others. This guide will help you set up and run EPStudio on your computer, even if you have no prior experience with Flask or web development.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
  - [1. Install Python](#1-install-python)
  - [2. Install Git](#2-install-git)
  - [3. Clone the Repository](#3-clone-the-repository)
  - [4. Create a Virtual Environment](#4-create-a-virtual-environment)
  - [5. Activate the Virtual Environment](#5-activate-the-virtual-environment)
  - [6. Install Dependencies](#6-install-dependencies)
  - [7. Set Up the Database](#7-set-up-the-database)
  - [8. Run the Application](#8-run-the-application)
- [Exploring EPStudio](#exploring-epstudio)
  - [Home Page](#home-page)
  - [Users Page](#users-page)
  - [User Profile](#user-profile)
  - [Adding a Creation](#adding-a-creation)
- [GitHub Basics](#github-basics)
  - [What is GitHub?](#what-is-github)
  - [Creating a Branch](#creating-a-branch)
  - [Working on Your Branch](#working-on-your-branch)
  - [Committing Your Changes](#committing-your-changes)
  - [Pushing Your Branch to GitHub](#pushing-your-branch-to-github)
  - [Creating a Pull Request](#creating-a-pull-request)
- [Additional Information](#additional-information)
  - [What is Flask?](#what-is-flask)
  - [Understanding Virtual Environments](#understanding-virtual-environments)
  - [Database Migrations](#database-migrations)
  - [Progressive Web App (PWA) Features](#progressive-web-app-pwa-features)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)
- [License](#license)

---

## Features

- **User Authentication**: Secure login system to protect user data.
- **User Profiles**: Each user has a profile page displaying their information and creations.
- **Add Creations**: Users can add their own creations to showcase.
- **List of Users**: View all users registered on the platform.
- **Progressive Web App**: Install EPStudio on your device like a native app.
- **SQLite Database**: Stores all user information and creations.
- **Docker Support**: Optionally run the application in a Docker container.

---

## Requirements

Before you begin, make sure you have the following installed on your computer:

- **Python 3.9 or higher**: The programming language used to build EPStudio.
- **Git**: A tool for cloning (copying) the project repository.
- **Internet Connection**: To download necessary packages and dependencies.

*Note: Docker is optional and is used for running the application in a containerized environment. Beginners can skip Docker for now.*

---

## Getting Started

Follow these steps to set up and run EPStudio on your computer.

### 1. Install Python

**Python** is a programming language that EPStudio is built with.

- **Windows**:
  1. Go to the [Python Downloads](https://www.python.org/downloads/) page.
  2. Download the latest version of Python 3 (make sure it's version 3.9 or higher).
  3. Run the installer.
  4. **Important**: During installation, check the box that says **"Add Python to PATH"**.

- **macOS**:
  1. macOS may come with Python pre-installed, but it's often an older version.
  2. Download the latest Python 3 installer from [Python Downloads](https://www.python.org/downloads/).
  3. Run the installer and follow the instructions.

- **Linux**:
  - Use your distribution's package manager to install Python 3.

    ```bash
    # For Debian/Ubuntu:
    sudo apt-get update
    sudo apt-get install python3 python3-venv python3-pip
    ```

### 2. Install Git

**Git** is a tool that allows you to download (clone) the project code from GitHub.

- **Windows**:
  1. Download the Git installer from [Git for Windows](https://gitforwindows.org/).
  2. Run the installer and follow the instructions.

- **macOS**:
  - Install Git using Homebrew (if you have it installed):

    ```bash
    brew install git
    ```

  - Or download the installer from [Git Downloads](https://git-scm.com/downloads).

- **Linux**:
  - Use your distribution's package manager.

    ```bash
    # For Debian/Ubuntu:
    sudo apt-get update
    sudo apt-get install git
    ```

### 3. Clone the Repository

Now, you'll download the EPStudio project code to your computer.

1. **Open Git Bash and clone**:

   - Create a folder where you want EPStudio to be installed
   - Open that folder in Git Bash (select folder, right click, more options, Open Git Bash Here)
   - git clone https://github.com/EastsidePreparatorySchool/epstudio
2. **Open the Folder in VS Code**:

   - Open VS Code
   - Open Folder
   - Select the "epstudio" folder that contains all the files just cloned down from git
  
3. **Git Commands in VS Code**:
   - In the Source Control Area in VS Code, you can click the 3 dots to choose push, pull, or fetch
   - Unless you have changes to push, you'll generally want to fetch


Clone the Repository:

git clone https://github.com/yourusername/EPStudio.git
cd EPStudio
This will download the project files into a folder named EPStudio and navigate into it.

4. Create a Virtual Environment
A virtual environment is like a separate box where you can install Python packages without affecting your main Python installation.

Create the Virtual Environment:

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

python3 -m venv venv<br />
This command creates a new directory called venv inside your project folder.

5. Activate the Virtual Environment
Before installing packages, you need to activate the virtual environment.

Windows:

<br />
venv\Scripts\activate<br />

macOS/Linux:

<br />
source venv/bin/activate<br />
After activation, your command prompt should show (venv) at the beginning.

6. Install Dependencies
Dependencies are the packages that EPStudio needs to run.

<br />
python -m pip install -r requirements.txt<br />
This command reads the requirements.txt file and installs all the listed packages.<br />
This might break on the SQL Alchemy install, so we installed those manually with:<br />

7. Set Up the Database
EPStudio uses a database to store information. You'll need to set it up.

Initialize the Database Migrations:

<br />
flask db init<br />
<br />
<br />
Create the Migration Script:
<br />

flask db migrate -m "Initial migration."<br />
<br />
<br />
Apply the Migration to the Database:

<br />
flask db upgrade<br />
<br />
<br />
These commands create the necessary database files and tables.

8. Run the Application
Now you're ready to start EPStudio!
<br />
flask run (or now, flask run --host=localhost --port=5000)<br />
If everything is set up correctly, you should see output indicating that the server is running, like:

markdown
Copy code
 * Serving Flask app 'app.py' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 123-456-789
Exploring EPStudio
With the server running, you can now explore EPStudio in your web browser.

Home Page
Open Your Web Browser:

You can use Chrome, Firefox, Edge, or any modern browser.
Go to the Home Page:

Type http://127.0.0.1:5000/ or http://localhost:5000/ in the address bar and press Enter.

This is the home page of EPStudio. You should see a welcome message and some recent creations (if any).

Users Page
Click on the "Users" link in the navigation bar to see a list of all users.

Since this is your first time, there might not be any users yet.

User Profile
Click on "My Profile" in the navigation bar to view your profile.

You'll see your user information and any creations you've added.

Adding a Creation
Let's add a sample creation to your profile.

On Your Profile Page, click on "Add Creation".

Fill Out the Form:

Creation Name: Give your creation a name (e.g., "My First Creation").
Caption: Write a brief description.
Photo Path and Video Path: For now, you can leave these blank or enter a placeholder.
Submit the Form:

Click on the "Add Creation" button.
View Your Creation:

After submitting, you'll be redirected to your profile page, and your new creation will be listed.
GitHub Basics
If you'd like to contribute to the EPStudio project or manage your own code changes, learning how to use GitHub is essential.

What is GitHub?
GitHub is a platform that uses Git, a version control system, to help people collaborate on code. It allows multiple people to work on the same project without overwriting each other's changes.

Creating a Branch
A branch is like a separate workspace where you can make changes without affecting the main project code (often called the "main" or "master" branch).

Check the Current Branch:

bash
Copy code
git branch
The branch with an asterisk (*) next to it is your current branch.

Create a New Branch:

bash
Copy code
git checkout -b my-new-branch
Replace my-new-branch with a name that describes what you're working on (e.g., add-new-feature).

Verify You're on the New Branch:

bash
Copy code
git branch
You should see * my-new-branch indicating you're now working on your new branch.

Working on Your Branch
Now you can make changes to the code without affecting the main branch.

Edit Files: Use a code editor or text editor to make changes to the files.
Committing Your Changes
After making changes, you need to commit them to your branch.

Check the Status:

bash
Copy code
git status
This shows which files have changed.

Add Changes to Be Committed:

bash
Copy code
git add .
This adds all changed files to the commit. You can also add specific files:

bash
Copy code
git add filename.py
Commit the Changes:

bash
Copy code
git commit -m "Describe your changes here"
Replace "Describe your changes here" with a brief message explaining what you did.

Pushing Your Branch to GitHub
To share your changes or submit them for review, you need to push your branch to GitHub.

Push the Branch:

bash
Copy code
git push origin my-new-branch
You'll need to replace my-new-branch with your branch name.

Authentication:

You may be prompted to enter your GitHub username and password.
Alternatively, you can set up SSH keys or use a personal access token.
Creating a Pull Request
A pull request lets you tell others about changes you've pushed to a GitHub repository. Once a pull request is submitted, someone can review your changes and merge them into the main branch.

Go to the GitHub Repository:

Visit your repository on GitHub (e.g., https://github.com/yourusername/EPStudio).
Compare & Pull Request:

GitHub may show a notification about your recently pushed branch with a button to "Compare & pull request". Click it.
If not, click on the "Pull requests" tab and then "New pull request".
Select Your Branch:

Ensure the base branch is main (or master) and the compare branch is your branch (e.g., my-new-branch).
Add a Title and Description:

Provide a meaningful title and describe the changes you've made.
Create Pull Request:

Click on "Create pull request".
Review and Merge:

If you have permission, you can merge the pull request yourself.
Otherwise, someone else will review your changes and merge them.
Keeping Your Fork Updated (If Applicable)
If you've forked the repository and want to keep your version updated with the original, you can set up an upstream remote.

Add Upstream Remote:

bash
Copy code
git remote add upstream https://github.com/originalusername/EPStudio.git
Fetch and Merge Changes:

bash
Copy code
git fetch upstream
git checkout main
git merge upstream/main
Additional Information
What is Flask?
Flask is a web framework for Python. It allows you to build web applications by providing tools and libraries that handle common tasks like routing URLs, handling requests, and rendering templates.

Understanding Virtual Environments
A virtual environment is a way to keep your project's dependencies (the Python packages it needs) separate from other projects and your main Python installation. This ensures that changes in one project don't affect others.

Database Migrations
Database migrations are a way to update your database schema (the structure of your database) over time as your application evolves. The commands you ran during setup help create and manage the database tables.

Progressive Web App (PWA) Features
EPStudio is a Progressive Web App, which means:

Installable: You can "install" it on your device like a native app.
Offline Support: Some features may work even when you're not connected to the internet.
Responsive Design: It looks good on both desktop and mobile devices.
How to Install EPStudio as a PWA
In Your Browser, look for an install prompt:

Chrome: You might see an icon in the address bar to install the app.
Safari (iOS): Tap the share button and select "Add to Home Screen".
Follow the Prompts:

Confirm the installation, and the app will be added to your device.
Troubleshooting
I get an error saying 'flask' is not recognized:

Make sure your virtual environment is activated. See Step 5.
The server starts but I can't access the web page:

Ensure you're visiting http://127.0.0.1:5000/ in your browser.
Check for any error messages in the terminal where the server is running.
I get a database error:

Make sure you completed Step 7 to set up the database.
I'm having trouble installing Python or Git:

Ask for help from a teacher, parent, or friend who is familiar with installing software.<br />
Next Steps<br />
Now that you have EPStudio running, here are some ideas to explore:
<br />
Add More Users: Modify the code to allow new user registration.
<br />
Enhance the UI: Customize the templates to change the look and feel of the app.
<br />
Learn Flask: Visit the Flask Documentation to learn more about how the framework works.
<br />
Experiment with Features: Try adding new features like editing creations, deleting items, or integrating other tools.

