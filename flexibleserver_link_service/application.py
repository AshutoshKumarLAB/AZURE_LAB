from flask import Flask, request, render_template_string
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="blazewarrison.mysql.database.azure.com",
    user="azure",
    password="warrison@123",
    database="company"
)

@app.route('/', methods=['GET', 'POST'])
def form():
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form['name']
        designation = request.form['designation']
        location = request.form['location']

        cursor.execute(
            "INSERT INTO employees (name, designation, location) VALUES (%s, %s, %s)",
            (name, designation, location)
        )
        db.commit()

    cursor.execute("SELECT * FROM employees")
    data = cursor.fetchall()

    html = """
    <h2>Employee Form</h2>
    <form method="POST">
        Name: <input name="name"><br>
        Designation: <input name="designation"><br>
        Location: <input name="location"><br>
        <input type="submit">
    </form>

    <h2>Data from MySQL</h2>
    <table border=1>
    <tr><th>ID</th><th>Name</th><th>Designation</th><th>Location</th></tr>
    {% for row in data %}
    <tr>
        <td>{{row[0]}}</td>
        <td>{{row[1]}}</td>
        <td>{{row[2]}}</td>
        <td>{{row[3]}}</td>
    </tr>
    {% endfor %}
    </table>
    """

    return render_template_string(html, data=data)

app.run(host='0.0.0.0', port=30080)
