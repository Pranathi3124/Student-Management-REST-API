
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory student storage
students = {}
next_id = 1


# CREATE STUDENT
@app.route('/students', methods=['POST'])
def create_student():
    global next_id

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON payload"}), 400

    required_fields = ['name', 'roll_number', 'email']

    for field in required_fields:
        if not isinstance(data.get(field), str) or not data[field].strip():
            return jsonify({"error": f"{field} is required"}), 400

    if '@' not in data['email'] or '.' not in data['email']:
        return jsonify({"error": "Invalid email address"}), 400

    student = {
        "id": next_id,
        "name": data['name'].strip(),
        "roll_number": data['roll_number'].strip(),
        "email": data['email'].strip()
    }

    students[next_id] = student
    next_id += 1

    return jsonify(student), 201


# READ ALL STUDENTS
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(list(students.values())), 200


# READ STUDENT BY ID
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = students.get(student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student), 200


# UPDATE STUDENT
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = students.get(student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON payload"}), 400

    required_fields = ['name', 'roll_number', 'email']

    for field in required_fields:
        if not isinstance(data.get(field), str) or not data[field].strip():
            return jsonify({"error": f"{field} is required"}), 400

    if '@' not in data['email'] or '.' not in data['email']:
        return jsonify({"error": "Invalid email address"}), 400

    student.update({
        "name": data['name'].strip(),
        "roll_number": data['roll_number'].strip(),
        "email": data['email'].strip()
    })

    return jsonify(student), 200


# DELETE STUDENT
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    if student_id not in students:
        return jsonify({"error": "Student not found"}), 404

    deleted_student = students.pop(student_id)

    return jsonify({
        "message": "Student deleted successfully",
        "student": deleted_student
    }), 200


# RUN APPLICATION
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
