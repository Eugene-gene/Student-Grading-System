import sys
import csv
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QComboBox, QTextEdit, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 100)
    
        self.init_ui()
    
    def init_ui(self):
        """Set up the user interface for the login window"""
        layout = QVBoxLayout()

        # Add Logo
        self.logo_label = QLabel(self)
        pixmap = QPixmap("logo.png")  # Replace 'logo.png' with the path to your logo file
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)
        
        # Login form
        form_layout = QFormLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter username")
        form_layout.addRow("Username:", self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Password:", self.password_input)

        layout.addLayout(form_layout)

        # Apply dark mode stylesheet to the LoginWindow
        self.setStyleSheet(self.get_dark_mode_stylesheet1())


        # Login button
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        """Validate login credentials"""
        username = self.username_input.text()
        password = self.password_input.text()

        # Simple hardcoded username and password for demonstration
        if username == "admin" and password == "password123":
            self.accept_login()
            self.main_window = StudentGradingSystem()  # Only create the main window after login
            self.main_window.show()
            self.close()
        else:
            self.show_error("Invalid credentials. Please try again.")

    def accept_login(self):
        """On successful login, open the StudentGradingSystem"""
        self.main_window = StudentGradingSystem()
        self.main_window.show()
        self.close()

    def show_error(self, message):
        """Show error dialog"""
        QMessageBox.critical(self, "Error", message)

    def get_dark_mode_stylesheet1(self):
        return """
            QWidget {
                background-color: #2E2E2E;
                color: green;
                font-weight: bold;
            }
            QPushButton {
                background-color: #3A3A3A;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4CAF50;
            }
            QLineEdit {
                background-color: #444;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #FF6347;
            }
        """


class StudentGradingSystem(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Student Grading System")
        self.setGeometry(100, 100, 800, 600)

        self.student_records = {}
        self.subjects = ["Math", "Science", "History", "Filipino"]
        self.is_dark_mode = False  # Default to light mode

        self.init_ui()
        self.load_student_records()

    def init_ui(self):
        """Set up the user interface"""
        self.setStyleSheet(self.get_light_mode_stylesheet())  # Default to light mode

        layout = QVBoxLayout()

        # Input Form for Student
        form_layout = QFormLayout()
        self.student_name_input = QLineEdit(self)
        self.student_name_input.setPlaceholderText("Enter student name")
        form_layout.addRow("Student Name:", self.student_name_input)

        self.course_input = QLineEdit(self)
        self.course_input.setPlaceholderText("Enter course")
        form_layout.addRow("Course:", self.course_input)

        # Semester selection dropdown
        self.semester_select = QComboBox(self)
        self.semester_select.addItem("1st Semester")
        self.semester_select.addItem("2nd Semester")
        self.semester_select.addItem("3rd Semester")
        form_layout.addRow("Semester:", self.semester_select)

        self.grade_inputs = {}
        for subject in self.subjects:
            grade_input = QLineEdit(self)
            grade_input.setPlaceholderText(f"Enter {subject} grade")
            form_layout.addRow(f"{subject} Grade:", grade_input)
            self.grade_inputs[subject] = grade_input

        layout.addLayout(form_layout)

        # Button Layout
        button_layout = QHBoxLayout()

        self.add_student_button = QPushButton("Add Student", self)
        self.add_student_button.clicked.connect(self.add_student)
        button_layout.addWidget(self.add_student_button)

        self.update_student_button = QPushButton("Update Student", self)
        self.update_student_button.clicked.connect(self.update_student)
        button_layout.addWidget(self.update_student_button)

        self.delete_student_button = QPushButton("Delete Student", self)
        self.delete_student_button.clicked.connect(self.delete_student)
        button_layout.addWidget(self.delete_student_button)

        self.generate_report_button = QPushButton("Generate Report", self)
        self.generate_report_button.clicked.connect(self.generate_report)
        button_layout.addWidget(self.generate_report_button)

        self.save_button = QPushButton("Save Records", self)
        self.save_button.clicked.connect(self.save_student_records)
        button_layout.addWidget(self.save_button)

        self.toggle_dark_mode_button = QPushButton("Toggle Dark Mode", self)
        self.toggle_dark_mode_button.clicked.connect(self.toggle_dark_mode)
        button_layout.addWidget(self.toggle_dark_mode_button)

        """# Add Load Records button
        self.load_records_button = QPushButton("Load Records", self)
        self.load_records_button.clicked.connect(self.load_student_records)
        button_layout.addWidget(self.load_records_button)"""

        layout.addLayout(button_layout)

        # Search Bar
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search student...")
        self.search_input.textChanged.connect(self.filter_students_by_name)
        layout.addWidget(self.search_input)

        # Student Table
        self.student_table = QTableWidget(self)
        self.student_table.setColumnCount(len(self.subjects) + 5)  # Extra columns for course, semester, average, and letter grade
        self.student_table.setHorizontalHeaderLabels(["Student Name", "Course", "Semester"] + self.subjects + ["Average", "Letter Grade"])
        layout.addWidget(self.student_table)

        # Add QTextEdit widget for the report display
        self.report_text_edit = QTextEdit(self)
        self.report_text_edit.setReadOnly(True)
        layout.addWidget(self.report_text_edit)  # Add the report area to the layout

        self.setLayout(layout)

    def generate_report(self):
        """Generate and show a report"""
        report = "Student Report\n\n"
        for name, semesters in self.student_records.items():
            report += f"Student: {name}\n"
            for semester, data in semesters.items():
                grades = ", ".join([f"{subject}: {grade}" for subject, grade in data['grades'].items()])
                avg_grade = sum(data['grades'].values()) / len(data['grades'])
                letter_grade = self.get_letter_grade(avg_grade)
                report += f"{semester} - {data['course']}\n"
                report += f"Grades: {grades}\n"
                report += f"Average: {avg_grade:.2f} ({letter_grade})\n\n"

        # Display the generated report in the QTextEdit widget
        self.report_text_edit.setText(report)
   

    def get_dark_mode_stylesheet(self):
        return """
            QWidget {
                background-color: #2E2E2E;
                color: red;
            }
            QPushButton {
                background-color: #3A3A3A;
                color: white;
                border-radius: 5px;
            }
            QTableWidget {
                background-color: #3A3A3A;
                border: 1px solid #555;
            }
            QPushButton:hover {
                background-color: #4CAF50;
            }
            QLineEdit {
                background-color: #444;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            /* Style for specific fields */
            QLineEdit#student_name_input {
                background-color: #FFD700;  /* SteelBlue */
                color: yellow;
            }
            QLineEdit#course_input {
                background-color: #FFD700;  /* LimeGreen */
                color: green;
            }
            QComboBox {
                background-color: #FFD700;  /* Gold */
                color: #00008B;  /* DarkBlue */
            }
            QLineEdit#math_grade_input {
                background-color: #FFD700; /* Gold */
                color: #8B4513; /* SaddleBrown */
            }
            QLineEdit#science_grade_input {
                background-color: #98FB98; /* PaleGreen */
                color: #006400; /* DarkGreen */
            }
            QLineEdit#history_grade_input {
                background-color: #ADD8E6; /* LightBlue */
                color: #00008B; /* DarkBlue */
            }
            QLineEdit#filipino_grade_input {
                background-color: #FF6347; /* Tomato */
                color: #8B0000; /* DarkRed */
            }
        """

    def get_light_mode_stylesheet(self):
        return """
            QWidget {
                background-color: #F0F0F0;
                color: green;
                font-weight: bold;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 3px;
            }
            QTableWidget {
                background-color: #FFFFFF;
                border: 1px solid #ddd;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                background-color: #fff;
                color: black;
                border-radius: 5px;
                padding: 5px;
            }
        """

    def load_student_records(self):
        """Load student records from CSV file"""
        try:
            if os.path.exists('student_records.csv'):
                with open('student_records.csv', 'r') as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip header row
                    for row in reader:
                        name = row[0]
                        course = row[1]
                        semester = row[2]
                        grades = {self.subjects[i]: float(row[i + 3]) for i in range(len(self.subjects))}
                        if name not in self.student_records:
                            self.student_records[name] = {}
                        self.student_records[name][semester] = {'course': course, 'grades': grades}
                self.update_student_table()
           
        except Exception as e:
            self.show_error(f"Failed to load student records: {str(e)}")

    def save_student_records(self):
        """Save student records to CSV"""
        try:
            with open('student_records.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Student Name', 'Course', 'Semester'] + self.subjects + ['Average', 'Letter Grade'])
                for student_name, semesters in self.student_records.items():
                    for semester, data in semesters.items():
                        row = [student_name, data['course'], semester] + list(data['grades'].values())
                        
                        # Calculate the average grade
                        grades = data['grades'].values()
                        avg_grade = sum(grades) / len(grades)
                        row.append(f"{avg_grade:.2f}")  # Add average grade to the row
                    
                        # Get the letter grade
                        letter_grade = self.get_letter_grade(avg_grade)
                        row.append(letter_grade)  # Add letter grade to the row
        
                        writer.writerow(row)
            QMessageBox.information(self, "Success", "Student records have been saved.")
        except Exception as e:
            self.show_error(f"Failed to save student records: {str(e)}")

    def update_student_table(self, filtered_records=None):
        """Update the student table to reflect the current records, sorted by average grade"""
        self.student_table.setRowCount(0)

        # Use filtered records if provided, otherwise use all student records
        records_to_display = filtered_records if filtered_records else self.student_records

        # Sort students by their average grade across all semesters
        sorted_students = []

        for student_name, semesters in records_to_display.items():
            total_grades = []
            for semester, data in semesters.items():
                grades = data['grades']
                total_grades.append(sum(grades.values()) / len(grades))  # average grade per semester

            # Calculate the overall average for the student
            overall_average = sum(total_grades) / len(total_grades) if total_grades else 0
            sorted_students.append((student_name, semesters, overall_average))

        # Now sort the students based on the overall average
        sorted_students.sort(key=lambda x: x[2], reverse=True)

        for student_name, semesters, _ in sorted_students:
            for semester, data in semesters.items():
                row_position = self.student_table.rowCount()
                self.student_table.insertRow(row_position)
                self.student_table.setItem(row_position, 0, QTableWidgetItem(student_name))
                self.student_table.setItem(row_position, 1, QTableWidgetItem(data['course']))
                self.student_table.setItem(row_position, 2, QTableWidgetItem(semester))

                grades = data['grades']
                total_grade = 0
                for i, subject in enumerate(self.subjects):
                    grade = grades[subject]
                    grade_item = QTableWidgetItem(str(grade))
                    self.student_table.setItem(row_position, i + 3, grade_item)
                    total_grade += grade

                    # Highlight failing students in red
                    if grade < 60:
                        grade_item.setBackground(Qt.red)
                    else:
                        grade_item.setBackground(Qt.green)

                avg_grade = total_grade / len(self.subjects)
                avg_item = QTableWidgetItem(f"{avg_grade:.2f}")
                self.student_table.setItem(row_position, len(self.subjects) + 3, avg_item)

                # Convert average grade to letter grade
                letter_grade = self.get_letter_grade(avg_grade)
                self.student_table.setItem(row_position, len(self.subjects) + 4, QTableWidgetItem(letter_grade))

    def get_letter_grade(self, average):
        """Convert average grade to letter grade"""
        if average >= 90:
            return "A"
        elif average >= 87:
            return "A-"
        elif average >= 83:
            return "B+"
        elif average >= 80:
            return "B"
        elif average >= 77:
            return "B-"
        elif average >= 73:
            return "C+"
        elif average >= 70:
            return "C"
        elif average >= 67:
            return "C-"
        elif average >= 63:
            return "D+"
        elif average >= 60:
            return "D"
        else:
            return "F"

    def add_student(self):
        """Add a student to the student records"""
        name = self.student_name_input.text()
        course = self.course_input.text()
        semester = self.semester_select.currentText()
        
        if not name or not course:
            self.show_error("Please provide a valid student name and course.")
            return
        
         # I put this to not crash the system when i add student when no input
        grades = {subject: float(self.grade_inputs[subject].text()) for subject in self.subjects}
 
        # Check if the student already has a record for the same semester
        if name in self.student_records and semester in self.student_records[name]:
            self.show_error(f"Student '{name}' already has a record for {semester}.")
            return

        if name not in self.student_records:
            self.student_records[name] = {}
        
        self.student_records[name][semester] = {'course': course, 'grades': grades}
        self.update_student_table()
        self.clear_form()

    def update_student(self):
        """Update student information"""
        name = self.student_name_input.text()
        if name not in self.student_records:
            self.show_error(f"Student '{name}' not found.")
            return

        semester = self.semester_select.currentText()
        grades = {subject: float(self.grade_inputs[subject].text()) for subject in self.subjects}
        course = self.course_input.text()

        # Check if the student exists for the given semester
        if name in self.student_records and semester in self.student_records[name]:
            # Allow update even if the semester is the same
            self.student_records[name][semester] = {'course': course, 'grades': grades}
            self.update_student_table()
            self.clear_form()
            QMessageBox.information(self, "Success", f"Student '{name}' updated for {semester}.")
            return

        # If the student doesn't already have a record for this semester, allow adding a new semester record
        self.student_records[name][semester] = {'course': course, 'grades': grades}
        self.update_student_table()
        self.clear_form()
        QMessageBox.information(self, "Success", f"New record added for {name} in {semester}.")
        
        # Check if the semester already exists for this student
        if semester in self.student_records[name]:
            self.show_error(f"Student '{name}' already has a record for {semester}. You cannot update the same semester.")
            return

        self.student_records[name][semester] = {'course': course, 'grades': grades}
        self.update_student_table()
        self.clear_form()

    def delete_student(self):
        """Delete student record"""
        name = self.student_name_input.text()

        # Confirm deletion with the user
        reply = QMessageBox.question(
            self,
            'Confirm Deletion',
            f"Are you sure you want to delete the student '{name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if name in self.student_records:
                del self.student_records[name]
                self.update_student_table()
                self.clear_form()
            else:
                self.show_error(f"Student '{name}' not found.")

    def filter_students_by_name(self):
        """Filter students by name"""
        search_term = self.search_input.text().lower()
        filtered_records = {
            name: semesters for name, semesters in self.student_records.items() if search_term in name.lower()
        }
        self.update_student_table(filtered_records)

    def show_error(self, message):
        """Show error message in a pop-up"""
        QMessageBox.critical(self, "Error", message)

    def clear_form(self):
        """Clear all form inputs"""
        self.student_name_input.clear()
        self.course_input.clear()
        self.semester_select.setCurrentIndex(0)
        for grade_input in self.grade_inputs.values():
            grade_input.clear()

    def toggle_dark_mode(self):
        """Toggle between dark and light modes"""
        if self.is_dark_mode:
            self.setStyleSheet(self.get_light_mode_stylesheet())
        else:
            self.setStyleSheet(self.get_dark_mode_stylesheet())
        self.is_dark_mode = not self.is_dark_mode

  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    window = StudentGradingSystem()
 
    sys.exit(app.exec_())
