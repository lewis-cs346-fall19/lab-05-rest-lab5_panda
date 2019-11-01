#! /usr/bin/python3

# CSC 346 REST project
# Programmer: Aniket Panda
  
import cgi
import cgitb
cgitb.enable()
import os
import json
import passwords
import MySQLdb

path = os.environ['PATH_INFO']
if path == '/magic_page':
    print("Content-Type: text/html")
    print("Status: 200 OK")
    print()
    print('''<html><body>
             <h1>Aniket Panda REST Project: Main Links</h1>
             <a href="people">people</a>(GET) <br>
             <a href="new_person_form">new person form</a>(form, will POST to /people)
             <hr><a href="redirect">302 redirect back to main links page</a>
             </body></html>''')
elif path == '/redirect':
    print('Status: 302 Redirect')
    print('Location: magic_page')
    print()
elif path == '/json_dumps':
    print("Content-Type: application/json")
    print("Status: 200 OK")
    print()
    x = [1,2,30,20, {"foo": "bar"}]
    x_json = json.dumps(x, indent=2)
    print(x_json)
elif path == '/people':
    print("Content-Type: application/json")
    print("Status: 200 OK")
    print()

    conn = MySQLdb.connect(host = passwords.SQL_HOST,
                           user = passwords.SQL_USER,
                           passwd = passwords.SQL_PASSWD,
                           db = "db_one")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM table_one;")
    results = cursor.fetchall()
    cursor.close()
    fields = ("id", "firstname", "lastname", "city")
    modified_results = []
    for record in results:
        d = {}
        for i in range(4):
            d[fields[i]] = record[i]
        modified_results.append(d)

    msg = json.dumps(modified_results, indent=2)
    print(msg)

    conn.close()
elif path[:8] == '/people/' and path[8:].isdigit():
    print("Content-Type: application/json")
    print("Status: 200 OK")
    print()

    conn = MySQLdb.connect(host = passwords.SQL_HOST,
                           user = passwords.SQL_USER,
                           passwd = passwords.SQL_PASSWD,
                           db = "db_one")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM table_one WHERE id=" + path[8:] + ";" )
    results = cursor.fetchall()
    cursor.close()
    fields = ("id", "firstname", "lastname", "city")
    modified_results = []
    for record in results:
        d = {}
        for i in range(4):
            d[fields[i]] = record[i]
        modified_results.append(d)

    msg = json.dumps(modified_results, indent=2)
    print(msg)
    conn.close()
elif path == '/new_person_form':
    print("Content-Type: text/html")
    print("Status: 200 OK")
    print()
    print('''<html><body>
     <form action="form_submission" method=POST>
     <p>First Name:
     <br><input type=text name="first">
     <p>Last Name:
     <br><input type=text name="last">
     <p>City:
     <br><input type=text name="city">
     <p><input type=submit>
     </form></body></html>''')
elif path == '/form_submission':
    form = cgi.FieldStorage()
    first = ''
    last = ''
    city = ''
    if "first" in form:
        first = form["first"].value
    if "last" in form:
        last = form["last"].value
    if "city" in form:
        city = form["city"].value

    conn = MySQLdb.connect(host = passwords.SQL_HOST,
                           user = passwords.SQL_USER,
                           passwd = passwords.SQL_PASSWD,
                           db = "db_one")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO table_one(firstname, lastname, city) VALUES (%s, %s, %s);", (first, last, city))
    new_id = cursor.lastrowid
    new_id = '1'
    cursor.close()
    conn.close()

    print('Status: 302 Redirect')
    print('Location: people/' + new_id)
    print()
    
else:
    print("Content-Type: text/html")
    print("Status: 200 OK")
    print()
    print(path)

