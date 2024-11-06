import mysql.connector 
import tkinter as tk 
from tkinter import ttk, messagebox 
import matplotlib.pyplot as plt 
import pandas as pd 
 

def connect_db(): 
    return mysql.connector.connect( 
        host="localhost", 
        user="root", 
        password="Badal@8102", 
        database="StudentsAcademic", 
    ) 
 
def fetch_data(): 
    conn = connect_db() 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM Students") 
    rows = cursor.fetchall() 
    conn.close() 
    return rows 
 
def insert_student(first_name, last_name, age, gender, enrollment_year, major): 
    conn = connect_db() 
    cursor = conn.cursor() 
    cursor.execute("INSERT INTO students (first_name, last_name, age, gender, enrollment_year, major) VALUES (%s, %s, %s, %s, %s, %s)",
                    (first_name, last_name, age, gender, enrollment_year, major)) 
    conn.commit() 
    conn.close() 
    messagebox.showinfo("Success", "Student added successfully!") 
 
def update_student( 
    student_id, first_name, last_name, age, gender, enrollment_year, major 
): 
    conn = connect_db() 
    cursor = conn.cursor() 
    cursor.execute("UPDATE Students SET first_name=%s, last_name=%s, age=%s, gender=%s, enrollment_year=%s, major=%s WHERE student_id=%s", 
        (first_name, last_name, age, gender, enrollment_year, major, student_id)) 
    conn.commit() 
    conn.close() 
    messagebox.showinfo("Success", "Student updated successfully!") 
 

def delete_student(student_id): 
    conn = connect_db() 
    cursor = conn.cursor() 
    cursor.execute("DELETE FROM Students WHERE student_id=%s", 
(student_id,)) 
    conn.commit() 
    conn.close() 
    messagebox.showinfo("Success", "Student deleted successfully!") 
 
def visualize_student(student_id): 
    conn = connect_db() 
    query = """ 
    SELECT c.course_name, e.grade FROM Enrollments e 
    JOIN Courses c ON e.course_id = c.course_id 
    WHERE e.student_id = %s""" 
    df = pd.read_sql(query, conn, params=(student_id,)) 
    conn.close() 
 
    grade_mapping = {"A": 4, "B": 3, "C": 2, "D": 1, "F": 0} 
    df["numeric_grade"] = df["grade"].map(grade_mapping) 
 
    # Create a bar chart 
    plt.bar(df["course_name"], df["numeric_grade"], color="blue") 
    plt.xlabel("Courses") 
    plt.ylabel("Grades (Numeric)") 
    plt.title("Student Grades Visualization") 
    plt.xticks(rotation=45) 
    plt.show() 
 
def load_students(): 
    for row in tree.get_children(): 
        tree.delete(row) 
    for student in fetch_data(): 
        tree.insert("", "end", values=student) 
 
root = tk.Tk() 
root.title("Academic Performance Management") 
ttk.Label(root, text="First Name").grid(row=0, column=0) 
first_name_var = tk.StringVar() 
ttk.Entry(root, textvariable=first_name_var).grid(row=0, column=1) 
 
 
ttk.Label(root, text="Last Name").grid(row=1, column=0) 
last_name_var = tk.StringVar() 
ttk.Entry(root, textvariable=last_name_var).grid(row=1, column=1) 
ttk.Label(root, text="Age").grid(row=2, column=0) 
age_var = tk.IntVar() 
ttk.Entry(root, textvariable=age_var).grid(row=2, column=1) 
ttk.Label(root, text="Gender").grid(row=3, column=0) 
gender_var = tk.StringVar() 
ttk.Combobox(root, textvariable=gender_var, values=["M", "F", "Other"]).grid( 
    row=3, column=1 
) 
ttk.Label(root, text="Enrollment Year").grid(row=4, column=0) 
enrollment_year_var = tk.IntVar() 
ttk.Entry(root, textvariable=enrollment_year_var).grid(row=4, column=1) 
ttk.Label(root, text="Major").grid(row=5, column=0) 
major_var = tk.StringVar() 
ttk.Entry(root, textvariable=major_var).grid(row=5, column=1) 
 
def add_student(): 
    insert_student( 
        first_name_var.get(), 
        last_name_var.get(), 
        age_var.get(), 
        gender_var.get(), 
        enrollment_year_var.get(), 
        major_var.get(), 
    ) 
    load_students() 
 
def update_student_info(): 
    selected_item = tree.selection() 
    if selected_item: 
        student_id = tree.item(selected_item, "values")[0] 
        update_student( 
            student_id, 
            first_name_var.get(), 
            last_name_var.get(), 
            age_var.get(), 
            gender_var.get(), 
            enrollment_year_var.get(), 
            major_var.get(), 

 
        ) 
        load_students() 
 
def delete_student_info(): 
    selected_item = tree.selection() 
    if selected_item: 
        student_id = tree.item(selected_item, "values")[0] 
        delete_student(student_id) 
        load_students() 
 
def visualize_data(): 
    selected_item = tree.selection() 
    if selected_item: 
        student_id = tree.item(selected_item, "values")[0] 
        visualize_student(student_id) 
 
add_frame = ttk.LabelFrame(root, text="Add Student") 
add_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=10) 
ttk.Button(add_frame, text="Add Student", command=add_student).grid(row=0, 
column=0) 
update_delete_frame = ttk.LabelFrame(root, text="Update/Delete Student") 
update_delete_frame.grid(row=7, column=0, columnspan=2, padx=10, 
pady=10) 
ttk.Button( 
    update_delete_frame, text="Update Student", command=update_student_info 
).grid(row=0, column=0) 
ttk.Button( 
    update_delete_frame, text="Delete Student", command=delete_student_info 
).grid(row=0, column=1) 
visualize_frame = ttk.LabelFrame(root, text="Visualize Student Grades") 
visualize_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=10) 
ttk.Button(visualize_frame, text="Visualize Grades", 
command=visualize_data).grid( 
    row=0, column=0 
) 
columns = ( 
    "student_id", 
    "first_name", 
    "last_name", 
    "age", 
    "gender", 

 
    "enrollment_year", 
    "major", 
) 
tree = ttk.Treeview(root, columns=columns, show="headings") 
for col in columns: 
    tree.heading(col, text=col.replace("_", " ").title()) 
tree.grid(row=9, column=0, columnspan=2) 
load_students() 
root.mainloop()