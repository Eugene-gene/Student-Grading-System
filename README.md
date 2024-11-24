# Student-Grading-System

## Project Title
Student Grading System with Login

## Objective
This project is a simple student grading management system developed using Python and PyQt5. It allows users (with admin login) to manage student records, including adding, updating, deleting, and viewing student grades across multiple subjects and semesters. The system also supports dark mode and generates detailed reports of student performance.

## Features
- **Login System**: Secure login screen with a hardcoded username ("admin") and password ("password123").
- **Student Management**: Add, update, and delete student records. The student data includes name, course, semester, and grades for multiple subjects (Math, Science, History, Filipino).
- **Report Generation**: Generate a detailed report showing student performance, including average grades and letter grades.
- **Student Search**: Filter students by name using a search bar.
- **Dark Mode**: Toggle between dark and light themes for a more user-friendly interface.
- **CSV File Storage**: Save and load student records to/from a CSV file.
- **User Interface**: Built with PyQt5, offering a responsive and intuitive design with input fields for grades, a table to display records, and buttons for user actions.

## Instructions on How to Run the Program

### Prerequisites
To run this program, you'll need Python 3.6+ and the following libraries:
- PyQt5
- CSV (standard Python library)
- OS (standard Python library)

You can install PyQt5 using pip:
```bash
pip install PyQt5

## Running the Program
- Clone or download the repository to your local machine.
- Place a logo image (logo.png) in the same directory as the script (or update the file path in the code).
- Open a terminal and navigate to the project directory.
- Run the application by executing the following command:

## Bash Terminal
>> python student_grading_system.py

## Steps to log-in
- This will launch the login window. Use the credentials:
- Username: admin
- Password: password123
- After logging in, you'll be directed to the Student Grading System interface where you can manage student records.

*** Limitations ***
- **Hardcoded Login: The login system is currently hardcoded with a username and password (admin/password123). A more secure, dynamic authentication system is recommended for real-world use.
- **Error Handling: Basic error handling is implemented, but there could be improvements, such as handling invalid data input more gracefully.
- **Single User: The system supports a single user (admin) at a time. Multiple user support could be added in future versions.
- **CSV File Handling: The program assumes that the student_records.csv file is well-formatted. If the file is corrupted, the system may fail to load or save records properly.

*** Future Improvements ***
- **Enhanced Authentication**: Implement a more secure authentication system, such as using hashed passwords or integrating with a database.
- **Multi-User Support**: Allow multiple users (e.g., teachers or admins) to access the system with different levels of permissions.
- **Better Validation**: Improve data validation, such as ensuring that grades are numeric and fall within a valid range (e.g., 0-100).
- **Data Backup/Restore**: Implement features to backup and restore student records to prevent data loss.
- **Subject Customization**: Allow users to add or remove subjects based on the course requirements.
- **UI Enhancements**: Add more advanced UI features such as charts/graphs to visualize student performance.
- **Exporting Reports**: Allow the generation of student reports in formats such as PDF or Excel.

#License
This project is open-source and available under the MIT License.

Acknowledgements
PyQt5: https://riverbankcomputing.com/software/pyqt/intro
Python: https://www.python.org/


### Explanation of Sections:

1. **Project Title**: This provides a clear title for the project.
2. **Objective**: Describes the core functionality and purpose of the program.
3. **Features**: A list of key functionalities, from login and student management to dark mode and CSV file support.
4. **Instructions on How to Run the Program**: This section outlines the steps required to set up and run the application, including dependencies and setup instructions.
5. **Limitations**: Highlights areas where the program can be improved, such as authentication and error handling.
6. **Future Improvements**: Lists potential features to enhance the system, such as multi-user support and report exporting.
7. **License and Acknowledgements**: Credits the libraries and resources used in the project, and provides a license for open-source distribution.

This README should help users understand the project and guide them through installation and usage. Let me know if you'd like to adjust anything!
