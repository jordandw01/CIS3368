from flask import Flask, request, jsonify, make_response
import mysql.connector, hashlib
from mysql.connector import Error

# Initialize Flask app
app = Flask(__name__)
app.config["DEBUG"] = True

# Pre-configured username and password
USERNAME = "admin"
PASSWORD = "password"

# Function to create MySQL connection
def create_connection(hostname, username, userpw, dbname):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=hostname,
            user=username,
            password=userpw,
            database=dbname
        )
        print("Connection Successful")
    except Error as e:
        print(f'The error {e} occurred')
    return connection

# password 'password' hashed
masterPassword = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
masterUsername = 'username'
validTokens = {"100", "200", "300", "400"}

# Basic http authentication, prompts username and password:
@app.route('/login', methods=['GET'])
def auth():
    if request.authorization:
        encoded = request.authorization.password.encode() #unicode encoding
        hashedResult = hashlib.sha256(encoded) #hashing
        if request.authorization.username == masterUsername and hashedResult.hexdigest() == masterPassword:
            return '<h1> We are allowed to be here </h1>'
    return make_response('COULD NOT VERIFY!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

# Function to get the number of children assigned to a classroom
def get_children_count(classroom_id):
    conn = create_connection('cis3368spring.cdgoaucqi4wk.us-east-1.rds.amazonaws.com', 'admin', '3368Spring2024', 'cis3368springdb')
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM child WHERE room = %s"
    cursor.execute(query, (classroom_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

# Function to get a child's classroom
def get_child_classroom(child_id):
    conn = create_connection('cis3368spring.cdgoaucqi4wk.us-east-1.rds.amazonaws.com', 'admin', '3368Spring2024', 'cis3368springdb')
    cursor = conn.cursor()
    query = "SELECT room FROM child WHERE id = %s"
    cursor.execute(query, (child_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0]  # Return the room ID
    else:
        return None  # Return None if child not found

# Read facilities table
@app.route('/facility', methods=['GET'])
def get_facilities():
    conn = create_connection('cis3368spring.cdgoaucqi4wk.us-east-1.rds.amazonaws.com', 'admin', '3368Spring2024', 'cis3368springdb')
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM facility"
    cursor.execute(query)
    facilities = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(facilities)

# Create a new facility
@app.route('/facility', methods=['POST'])
def add_facility():
    conn = create_connection('cis3368spring.cdgoaucqi4wk.us-east-1.rds.amazonaws.com', 'admin', '3368Spring2024', 'cis3368springdb')
    cursor = conn.cursor()
    details = request.json
    query = "INSERT INTO facility (name) VALUES (%s)"
    cursor.execute(query, (details['name'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Facility added successfully'}), 201

# Update facility name using id
@app.route('/facility/<int:id>', methods=['PUT'])
def update_facility(id):
    conn = create_connection('cis3368spring.cdgoaucqi4wk.us-east-1.rds.amazonaws.com', 'admin', '3368Spring2024', 'cis3368springdb')
    cursor = conn.cursor()
    details = request.json
    query = "UPDATE facility SET name = %s WHERE id = %s"
    cursor.execute(query, (details['name'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Facility updated successfully'}), 200

# Delete from facility using id
@app.route('/facility/<int:id>', methods=['DELETE'])
def delete_facility(id):
    conn = create_connection('cis3368spring.cdgoaucqi4wk.us-east-1.rds.amazonaws.com', 'admin', '3368Spring2024', 'cis3368springdb')
    cursor = conn.cursor()
    query = "DELETE FROM facility WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Facility deleted successfully'}), 200

# Read classrooms table
@app.route('/classroom', methods=['GET'])
def get_classrooms():
    conn = create_connection('cis3368spring.cdgoaucqi4wk.us-east-1.rds.amazonaws.com', 'admin', '3368Spring2024', 'cis3368springdb')
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM classroom"
    cursor.execute(query)
    classrooms = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(classrooms)

# Create a new classroom with name capacity and facility
@app.route('/classroom', methods=['POST'])
def add_classroom():
    conn = create_connection('cis3368spring.cdgoaucqi4wk.us-east-1.rds.amazonaws.com', 'admin', '3368Spring2024', 'cis3368springdb')
    cursor = conn.cursor()
    details = request.json
    query = "INSERT INTO classroom (name, capacity, facility) VALUES (%s,%s,%s)"
    cursor.execute(query, (details['name'], details['capacity'], details['facility']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Classroom added successfully'}), 201

# Update a classroom's name with id
@app.route('/classroom/<int:id>', methods=['PUT'])
def update_classroom(id):
    conn = create_connection('cis3368spring.cdgoaucqi4wk.us-east-1.rds.amazonaws.com', 'admin', '3368Spring2024', 'cis3368springdb')
    cursor = conn.cursor()
    details = request.json
    query = "UPDATE classroom SET name = %s WHERE id = %s"
    cursor.execute(query, (details['name'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Classroom updated successfully'}), 200

# Delete a classroom using id
@app.route('/classroom/<int:id>', methods=['DELETE'])
def delete_classroom(id):
    conn = create_connection('cis3368spring.cdgoaucqi4wk.us-east-1.rds.amazonaws.com', 'admin', '3368Spring2024', 'cis3368springdb')
    cursor = conn.cursor()
    query = "DELETE FROM classroom WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Classroom deleted successfully'}), 200

# Read teachers table
@app.route('/teacher', methods=['GET'])
def get_teacher():
    conn = create_connection('cis3368spring.cdgoaucqi4wk.us-east-1.rds.amazonaws.com', 'admin', '3368Spring2024', 'cis3368springdb')
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM teacher"
    cursor.execute(query)
    teachers = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(teachers)

# Create a new teacher with firstname and lastname, no room added yet
@app.route('/teacher', methods=['POST'])
def add_teacher():
    conn = create_connection('cis3368spring.cdgoaucqi4wk.us-east-1.rds.amazonaws.com', 'admin', '3368Spring2024', 'cis3368springdb')
    cursor = conn.cursor()
    details = request.json
    query = "INSERT INTO teacher (firstname, lastname) VALUES (%s, %s)"
    cursor.execute(query, (details['firstname'], details['lastname']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Teacher added successfully'}), 201

# Update a teacher's room using id
@app.route('/teacher/<int:id>', methods=['PUT'])
def update_teacher(id):
    conn = create_connection('cis3368spring.cdgoaucqi4wk.us-east-1.rds.amazonaws.com', 'admin', '3368Spring2024', 'cis3368springdb')
    cursor = conn.cursor()
    details = request.json
    query = "UPDATE teacher SET room = %s WHERE id = %s"
    cursor.execute(query, (details['room'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Teacher updated successfully'}), 200

# Delete a teacher using id
@app.route('/teacher/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    conn = create_connection('cis3368spring.cdgoaucqi4wk.us-east-1.rds.amazonaws.com', 'admin', '3368Spring2024', 'cis3368springdb')
    cursor = conn.cursor()
    query = "DELETE FROM teacher WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Teacher deleted successfully'}), 200

# Read children table
@app.route('/child', methods=['GET'])
def get_child():
    conn = create_connection('cis3368spring.cdgoaucqi4wk.us-east-1.rds.amazonaws.com', 'admin', '3368Spring2024', 'cis3368springdb')
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM child"
    cursor.execute(query)
    children = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(children)

# Create a new child and check count of the room
@app.route('/child', methods=['POST'])
def add_child():
    conn = create_connection('cis3368spring.cdgoaucqi4wk.us-east-1.rds.amazonaws.com', 'admin', '3368Spring2024', 'cis3368springdb')
    cursor = conn.cursor()
    details = request.json
    classroom_id = details['room']
    children_count = get_children_count(classroom_id)
    # Check if there's less than 10 cihldren in a classroom
    if children_count < 10:
        query = "INSERT INTO child (firstname, lastname, room, age) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (details['firstname'], details['lastname'], details['room'], details['age']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Child added successfully'}), 201
    else:
        return jsonify({'error': 'Classroom is full. Cannot add more children.'}), 400

# Update a child's room and check the amount of children in updated room
@app.route('/child/<int:id>', methods=['PUT'])
def update_child(id):
    conn = create_connection('cis3368spring.cdgoaucqi4wk.us-east-1.rds.amazonaws.com', 'admin', '3368Spring2024', 'cis3368springdb')
    cursor = conn.cursor()
    details = request.json
    new_classroom_id = details['room']
    current_classroom_id = get_child_classroom(id)
    if new_classroom_id == current_classroom_id:
        return jsonify({'message': 'Child is already in the specified classroom'}), 200
    else:
        new_children_count = get_children_count(new_classroom_id)
        #c check if there's less than 10 children in a classroom
        if new_children_count < 10:
            query = "UPDATE child SET room = %s WHERE id = %s"
            cursor.execute(query, (new_classroom_id, id))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'message': 'Child updated successfully'}), 200
        else:
            return jsonify({'error': 'Cannot move child. Destination classroom is full.'}), 400
        
# Delete a child using id
@app.route('/child/<int:id>', methods=['DELETE'])
def delete_child(id):
    conn = create_connection('cis3368spring.cdgoaucqi4wk.us-east-1.rds.amazonaws.com', 'admin', '3368Spring2024', 'cis3368springdb')
    cursor = conn.cursor()
    query = "DELETE FROM child WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Child deleted successfully'}), 200

if __name__ == '__main__':
    app.run()