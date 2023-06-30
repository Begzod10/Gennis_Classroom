import requests

from app import *
from backend.lessons.student_views import *

import json


@app.route(f'{api}/send_user/<token>')
def send_user(token):
    # response = requests.get(f"http://192.168.1.13:5000/get_user", headers={
    #     # "Authorization": "Bearer " + token,
    #     # 'Content-Type': 'application/json'
    # })
    response = requests.get(f"http://192.168.1.20:5000/get_user/{token}")
    # if 'data' not in response.json():
    #     return jsonify({
    #         "msg": "Not logged in"
    #     })
    subject_list = response.json()['subject_list']
    for sub in subject_list:
        get_subject = Subject.query.filter(Subject.name == sub['name']).first()
        if not get_subject:
            get_subject = Subject(name=sub['name'])
            get_subject.add_commit()
    pprint(response.json())

    item = response.json()['data']

    location_id = item['location']['id']
    location_name = item['location']['name']
    role_id = item["role"]['id']
    role_type = item['role']['name']
    role_token = item['role']['role']
    role = Role.query.filter(Role.platform_id == role_id).first()
    if not role:
        role = Role(platform_id=role_id, type=role_type, role=role_token)
        role.add_commit()
    location = Location.query.filter(Location.platform_id == location_id).first()
    if not location:
        location = Location(name=location_name, platform_id=location_id)
        location.add_commit()

    user = User.query.filter(User.username == item['username']).first()
    if not user:
        user = User(username=item['username'], name=item['name'], surname=item['surname'], balance=item['balance'],
                    password=item['password'], platform_id=item['id'], location_id=location.id, role_id=role.id)
        user.add_commit()
    else:
        User.query.filter(User.username == item['username']).update({
            "location_id": location.id,
            "role_id": role.id,
            "balance": item['balance']
        })
        db.session.commit()
    if item['student']:
        student = Student.query.filter(Student.user_id == user.id).first()
        if not student:
            student = Student(user_id=user.id, debtor=item['student']['debtor'],
                              representative_name=item['student']['representative_name'],
                              representative_surname=item['student']['representative_surname'])
            student.add_commit()
        else:
            Student.query.filter(Student.user_id == user.id).update({
                "debtor": item['student']['debtor'],
                "representative_name": item['student']['representative_name'],
                "representative_surname": item['student']['representative_surname']
            })
            db.session.commit()
        for gr in item['student']['group']:
            group = check_group_info(gr)
            if group not in student.groups:
                student.groups.append(group)
                db.session.commit()
    if item['teacher']:
        teacher = Teacher.query.filter(Teacher.user_id == user.id).first()
        if not teacher:
            teacher = Teacher(user_id=user.id)
            teacher.add_commit()
        for gr in item['teacher']['group']:
            group = check_group_info(gr)
            if group not in teacher.groups:
                teacher.groups.append(group)
                db.session.commit()
    return jsonify({
        "user_id": True
    })


def check_group_info(gr):
    group = Group.query.filter(Group.platform_id == gr['id']).first()
    if not group:
        location = Location.query.filter(Location.platform_id == gr['location']['id']).first()
        subject_name = gr['subjects']['name']
        subject = Subject.query.filter(Subject.name == subject_name).first()
        group = Group(platform_id=gr['id'], name=gr['name'], price=gr['price'],
                      teacher_salary=gr['teacher_salary'], location_id=location.id,
                      subject_id=subject.id)
        group.add_commit()
    else:
        Group.query.filter(Group.platform_id == gr['id']).update({
            "teacher_salary": gr['teacher_salary'],
            "price": gr['price'], "name": gr['name']
        })
        db.session.commit()
    return group


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    return app.send_static_file("index.html")
