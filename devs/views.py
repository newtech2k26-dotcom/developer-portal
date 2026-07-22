from django.shortcuts import render
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="TEST_PYTHON"
    )

def hello(request):
    return render(request, "devs/home.html")

def search_developer(request):
    selected_id = request.GET.get("dev_id")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # all developers for the dropdown
    cursor.execute("SELECT ID, NAME FROM PY_DEVELOPER_INFO ORDER BY ID")
    all_devs = cursor.fetchall()

    # the selected developer's details (if one was chosen)
    dev = None
    if selected_id:
        cursor.execute(
            "SELECT * FROM PY_DEVELOPER_INFO WHERE ID = %s", (selected_id,)
        )
        dev = cursor.fetchone()

    cursor.close()
    conn.close()

    return render(request, "devs/search.html", {
        "all_devs": all_devs,
        "dev": dev,
        "selected_id": selected_id,
    })