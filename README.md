# Abstract Syntax Tree (AST) of Rules
- This app can take New rules, can Evaluate rules.
- It can handle different rules simultaneously on same data.

## Design Parameters
- Tech Stack -> Python, Django, REST framework, HTML, Bootstrap, JavaScript.
- I followed Django’s app-based structure, dividing the code into separate apps for better maintainability and scalability.
- The project adheres to the MVC pattern to clearly separate business logic from the user interface.
- We used Django's built-in security features, such as CSRF protection and secure password hashing, to ensure the application is secure by default.
- The UI was built using Bootstrap to ensure a responsive design and consistent user experience across devices
- I have used PostgreSQL as my Database for local machine. To make installation easy, I have changed it to SQLite.
- Handles the redundancy efficiently.
- It handles with incorrect sentences and notify the user if there is a mistake.

## Build Instructions for windows
- Clone the repository and ...
- Create and Activate virtual environment
  - Open the folder.
  - ``` bash
     python -m venv venv
    ```
  - ``` bash
      cd venv\Script\activate
    ```
- Install requirements
  - ``` bash
      pip install -r requirements.txt
    ```
- Run the App
  - ``` bash
    python manage.py makemigrations
    ```
  - ``` bash
     python manage.py migrate
    ```
  - ``` bash
     python manage.py runserver
    ```
  - Navigate to the Link and view the website.
