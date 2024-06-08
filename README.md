# DIS
### Initialization ✔

Clone / download repository files 

Check that you are in the DatabaseProject_v2 folder or navigate into it

To start and run the server, use the following commands
    python create_database.py
    python app.py
 ### Interaction 🖥️
- You can interact both as an anonymous user or by creating a user and logging in.
- Choose a difficulty level and a muscle group.
- Select the exercise you want to add to your program
- Get the program shown.
- If the desired exercise is not found, it can be added under 'add exercies'

### Folder Setup 📁
The project directory is structured to separate different aspects of the application:
- `static`: Contains static files such as CSS. For this project:
  - `css/styles.css`: The CSS file that styles the web pages.
- `templates`: Holds the HTML files used for rendering the web views. It includes:
  - `add_new_exercise.html`: HTML form to add new exercises.
  - `index.html`: The homepage of the web application.
  - `login.html`: Page for user authentication.
  - `personal_program.html`: Page displaying personalized workout programs.
  - `register.html`: Registration page for new users.
- `app.py`: The main Python Flask application file.
- `create_database.py`: Python script to set up the database.
- `database.db`: SQLite database file.
- `fitness.csv`: CSV file, possibly used for initial data import.
- `requirements.txt`: Contains all necessary Python packages.

### Routes 📌
Here's an overview of the main routes and their functions, assuming standard web application practices:
- `/`: Serves the `index.html`, the landing page of the application.
- `/login`: Handles user login, displays `login.html`.
- `/register`: Registration page for new users, associated with `register.html`.
- `/add-new-exercise`: Route to add new exercises using `add_new_exercise.html`.
- `/personal-program`: Displays a personalized workout program using `personal_program.html`.
