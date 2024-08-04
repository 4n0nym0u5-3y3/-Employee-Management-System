import mysql.connector

# Database connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="emp"
)

db_cursor = connection.cursor()

# Function to check if an employee exists
def check_employee(employee_id):
    query = 'SELECT * FROM employees WHERE id=%s'
    db_cursor.execute(query, (employee_id,))
    return db_cursor.rowcount == 1

# Function to add an employee
def add_employee():
    employee_id = input("Enter Employee Id: ")
    if check_employee(employee_id):
        print("Employee already exists. Please try again.")
        return
    
    employee_name = input("Enter Employee Name: ")
    employee_position = input("Enter Employee Position: ")
    employee_salary = input("Enter Employee Salary: ")

    query = 'INSERT INTO employees (id, name, position, salary) VALUES (%s, %s, %s, %s)'
    data = (employee_id, employee_name, employee_position, employee_salary)
    try:
        db_cursor.execute(query, data)
        connection.commit()
        print("Employee Added Successfully")
    except mysql.connector.Error as error:
        print(f"Error: {error}")
        connection.rollback()

# Function to remove an employee
def remove_employee():
    employee_id = input("Enter Employee Id: ")
    if not check_employee(employee_id):
        print("Employee does not exist. Please try again.")
        return
    
    query = 'DELETE FROM employees WHERE id=%s'
    data = (employee_id,)
    try:
        db_cursor.execute(query, data)
        connection.commit()
        print("Employee Removed Successfully")
    except mysql.connector.Error as error:
        print(f"Error: {error}")
        connection.rollback()

# Function to promote an employee
def promote_employee():
    employee_id = input("Enter Employee's Id: ")
    if not check_employee(employee_id):
        print("Employee does not exist. Please try again.")
        return
    
    try:
        salary_increase = float(input("Enter Salary Increase: "))

        query_select = 'SELECT salary FROM employees WHERE id=%s'
        db_cursor.execute(query_select, (employee_id,))
        current_salary = db_cursor.fetchone()[0]
        new_salary = current_salary + salary_increase

        query_update = 'UPDATE employees SET salary=%s WHERE id=%s'
        db_cursor.execute(query_update, (new_salary, employee_id))
        connection.commit()
        print("Employee Promoted Successfully")

    except (ValueError, mysql.connector.Error) as error:
        print(f"Error: {error}")
        connection.rollback()

# Function to display all employees
def display_employees():
    try:
        query = 'SELECT * FROM employees'
        db_cursor.execute(query)
        employees = db_cursor.fetchall()
        for employee in employees:
            print("Employee Id : ", employee[0])
            print("Employee Name : ", employee[1])
            print("Employee Position : ", employee[2])
            print("Employee Salary : ", employee[3])
            print("------------------------------------")

    except mysql.connector.Error as error:
        print(f"Error: {error}")

# Function to display the menu
def menu():
    while True:
        print("\nWelcome to Employee Management System")
        print("Press:")
        print("1 to Add Employee")
        print("2 to Remove Employee")
        print("3 to Promote Employee")
        print("4 to Display Employees")
        print("5 to Exit")
        
        choice = input("Enter your Choice: ")

        if choice == '1':
            add_employee()
        elif choice == '2':
            remove_employee()
        elif choice == '3':
            promote_employee()
        elif choice == '4':
            display_employees()
        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid Choice! Please try again.")

if __name__ == "__main__":
    menu()
