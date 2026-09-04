import sqlite3

DATABASE_NAME = "employee.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            employee_id TEXT NOT NULL UNIQUE,
            salary REAL NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_employee(name, employee_id, salary, phone, email, department):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO employees
            (name, employee_id, salary, phone, email, department)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, employee_id, salary, phone, email, department))

        connection.commit()
        connection.close()

        return True, "Employee added successfully."

    except sqlite3.IntegrityError:
        return False, "Employee ID already exists."

    except Exception as e:
        return False, f"Error: {e}"


def get_employees():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, employee_id, salary, phone, email, department
        FROM employees
        ORDER BY id DESC
    """)

    data = cursor.fetchall()
    connection.close()

    return data


def get_employee(employee_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, employee_id, salary, phone, email, department
        FROM employees
        WHERE id = ?
    """, (employee_id,))

    data = cursor.fetchone()
    connection.close()

    return data


def update_employee(row_id, name, employee_id, salary, phone, email, department):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE employees
            SET name = ?,
                employee_id = ?,
                salary = ?,
                phone = ?,
                email = ?,
                department = ?
            WHERE id = ?
        """, (name, employee_id, salary, phone, email, department, row_id))

        connection.commit()
        connection.close()

        return True, "Employee updated successfully."

    except sqlite3.IntegrityError:
        return False, "Employee ID already exists."

    except Exception as e:
        return False, f"Error: {e}"


def delete_employee(row_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM employees WHERE id = ?", (row_id,))

        connection.commit()
        connection.close()

        return True, "Employee deleted successfully."

    except Exception as e:
        return False, f"Error: {e}"


def get_statistics():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*), COALESCE(SUM(salary), 0) FROM employees")
    total, salary_total = cursor.fetchone()

    cursor.execute("SELECT COUNT(DISTINCT department) FROM employees")
    departments = cursor.fetchone()[0]

    connection.close()

    return total, salary_total, departments
