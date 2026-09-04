import streamlit as st
import pandas as pd
from database import (
    initialize_database,
    add_employee,
    get_employees,
    get_employee,
    update_employee,
    delete_employee,
    get_statistics,
)

st.set_page_config(
    page_title="Employee Management System",
    page_icon="👨‍💼",
    layout="wide",
)

initialize_database()

# ---------- Styling ----------
st.markdown("""
<style>
.main-title {
    font-size: 34px;
    font-weight: 700;
    margin-bottom: 0;
}
.subtitle {
    color: #666;
    margin-top: 0;
}
.card {
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e6e6e6;
    background: #ffffff;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("👨‍💼 Employee Management System")
st.sidebar.caption("Manage employee records easily")

page = st.sidebar.radio(
    "Select Option",
    ["Dashboard", "Add Employee", "View Employees", "Update Employee", "Delete Employee"]
)

# ---------- Dashboard ----------
if page == "Dashboard":
    st.markdown('<p class="main-title">👨‍💼 Employee Management System</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Manage employee records easily using Streamlit and SQLite.</p>', unsafe_allow_html=True)

    total, salary_total, departments = get_statistics()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Employees", total)
    c2.metric("Total Salary", f"₹{salary_total:,.2f}")
    c3.metric("Departments", departments)

    st.subheader("📋 Employee Records")
    employees = get_employees()

    if employees:
        df = pd.DataFrame(
            employees,
            columns=["ID", "Employee Name", "Employee ID", "Salary", "Phone", "Email", "Department"]
        )
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No employee records found. Add an employee to get started.")

# ---------- Add Employee ----------
elif page == "Add Employee":
    st.markdown('<p class="main-title">➕ Add Employee</p>', unsafe_allow_html=True)
    st.write("Enter employee details below.")

    with st.form("add_employee_form", clear_on_submit=True):
        name = st.text_input("Employee Name")
        employee_id = st.text_input("Employee ID")
        salary = st.number_input("Salary", min_value=0.0, step=1000.0)
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        department = st.text_input("Department")

        submitted = st.form_submit_button("Add Employee", type="primary")

        if submitted:
            if not name or not employee_id or not phone or not email or not department:
                st.error("Please fill all required fields.")
            elif salary <= 0:
                st.error("Please enter a valid salary.")
            else:
                success, message = add_employee(
                    name, employee_id, salary, phone, email, department
                )
                if success:
                    st.success(message)
                else:
                    st.error(message)

# ---------- View Employees ----------
elif page == "View Employees":
    st.markdown('<p class="main-title">👥 View Employees</p>', unsafe_allow_html=True)

    employees = get_employees()

    if employees:
        df = pd.DataFrame(
            employees,
            columns=["ID", "Employee Name", "Employee ID", "Salary", "Phone", "Email", "Department"]
        )

        search = st.text_input("🔍 Search by name, employee ID or department")

        if search:
            mask = (
                df["Employee Name"].astype(str).str.contains(search, case=False, na=False)
                | df["Employee ID"].astype(str).str.contains(search, case=False, na=False)
                | df["Department"].astype(str).str.contains(search, case=False, na=False)
            )
            df = df[mask]

        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"{len(df)} employee record(s) shown.")
    else:
        st.info("No employee records found.")

# ---------- Update Employee ----------
elif page == "Update Employee":
    st.markdown('<p class="main-title">✏️ Update Employee</p>', unsafe_allow_html=True)

    employees = get_employees()

    if not employees:
        st.info("No employees available to update.")
    else:
        employee_options = {
            f"{row[1]} ({row[2]})": row[0] for row in employees
        }
        selected_label = st.selectbox("Select Employee", list(employee_options.keys()))
        selected_id = employee_options[selected_label]
        employee = get_employee(selected_id)

        if employee:
            with st.form("update_employee_form"):
                name = st.text_input("Employee Name", value=employee[1])
                employee_code = st.text_input("Employee ID", value=employee[2])
                salary = st.number_input("Salary", min_value=0.0, value=float(employee[3]), step=1000.0)
                phone = st.text_input("Phone", value=employee[4])
                email = st.text_input("Email", value=employee[5])
                department = st.text_input("Department", value=employee[6])

                submitted = st.form_submit_button("Update Employee", type="primary")

                if submitted:
                    if not name or not employee_code or not phone or not email or not department:
                        st.error("Please fill all required fields.")
                    elif salary <= 0:
                        st.error("Please enter a valid salary.")
                    else:
                        success, message = update_employee(
                            selected_id, name, employee_code, salary,
                            phone, email, department
                        )
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

# ---------- Delete Employee ----------
elif page == "Delete Employee":
    st.markdown('<p class="main-title">🗑️ Delete Employee</p>', unsafe_allow_html=True)

    employees = get_employees()

    if not employees:
        st.info("No employees available to delete.")
    else:
        employee_options = {
            f"{row[1]} ({row[2]})": row[0] for row in employees
        }
        selected_label = st.selectbox("Select Employee", list(employee_options.keys()))
        selected_id = employee_options[selected_label]

        st.warning("Deleting an employee permanently removes the record from the database.")

        confirm = st.checkbox("I confirm that I want to delete this employee.")

        if st.button("Delete Employee", type="primary"):
            if not confirm:
                st.error("Please confirm deletion first.")
            else:
                success, message = delete_employee(selected_id)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
