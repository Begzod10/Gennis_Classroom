from backend.models.basic_model import *
from app import *
from backend.models.settings import *
from backend.basics.settings import *
from pprint import pprint
import json
from sqlalchemy import desc


@app.route(f'{api}/filter_exercise/<subject_id>/<level_id>')
def filter_exercise(subject_id, level_id):
    exercises = Exercise.query.filter(Exercise.subject_id == subject_id, Exercise.level_id == level_id).order_by(
        Exercise.id).all()

    return jsonify({
        "data": iterate_models(exercises)
    })


@app.route(f'{api}/lessons/<int:level_id>', methods=["GET", 'POST'])
def lessons(level_id):
    if request.method == "POST":
        info = request.form.get("info")
        get_json = json.loads(info)
        selected_subject = get_json['subjectId']
        name = get_json['name']
        components = get_json['components']
        order = 0
        lesson_get = Lesson.query.filter(Lesson.level_id == level_id, Lesson.subject_id == selected_subject).order_by(
            Lesson.id).all()
        if lesson_get:
            order = len(lesson_get) + 1
        lesson_add = Lesson(subject_id=selected_subject, level_id=level_id, name=name, order=order)
        lesson_add.add_commit()
        for component in components:
            exercise_id = None
            video_url = ''
            desc = ''
            if component['type'] == "exc":
                exercise_id = component['id']
            elif component['type'] == "video":
                video_url = component['videoLink']
            elif component['type'] == "text":
                desc = component['text']
            lesson_img = request.files.get(f'component-{component["index"]}-img')
            get_img = None
            if lesson_img:
                get_img = add_file(lesson_img, app, Images)
            lesson_block = LessonBlock(lesson_id=lesson_add.id, exercise_id=exercise_id, video_url=video_url, desc=desc,
                                       img_id=get_img, clone=component, type_block=component['type'])
            lesson_block.add_commit()
        return create_msg(name, True)
    lessons = Lesson.query.filter(Lesson.level_id == level_id, Lesson.disabled != True).order_by(Lesson.order).all()
    return jsonify({
        "data": iterate_models(lessons),
        "length": len(lessons)
    })


@app.route(f'{api}/info_lesson/<order>', methods=['POST', 'GET', 'DELETE'])
def info_lesson(order):
    lesson = Lesson.query.filter(Lesson.order == order).first()
    lessons = Lesson.query.filter(Lesson.level_id == lesson.level_id, Lesson.disabled != True).order_by(Lesson.order).all()
    lesson_id = lesson.id
    if request.method == "GET":
        return jsonify({
            "data": lesson.convert_json(entire=True),
            "length": len(lessons)
        })
    elif request.method == "POST":
        info = request.form.get("info")
        get_json = json.loads(info)
        name = get_json['name']

        lesson.name = name
        db.session.commit()
        components = get_json['components']

        for component in components:
            exercise_id = None
            video_url = ''
            desc = ''
            if component['type'] == "exc":
                exercise_id = component['id']
            elif component['type'] == "video":
                video_url = component['videoLink']
            elif component['type'] == "text":
                desc = component['text']
            lesson_img = request.files.get(f'component-{component["index"]}-img')
            get_img = None
            if lesson_img:
                get_img = add_file(lesson_img, app, Images)
            if 'block_id' in component:
                lesson_block = LessonBlock.query.filter(LessonBlock.id == component['block_id']).first()
                if lesson_block.img_id:
                    check_img_remove(lesson_block.img_id, Images)
                lesson_block.img_id = get_img
                lesson_block.exercise_id = exercise_id
                lesson_block.video_url = video_url
                lesson_block.desc = desc
                lesson_block.clone = component
                lesson_block.type_block = component['type']
                db.session.commit()
            else:
                lesson_block = LessonBlock(lesson_id=lesson_id, exercise_id=exercise_id, video_url=video_url,
                                           desc=desc,
                                           img_id=get_img, clone=component, type_block=component['type'])
                lesson_block.add_commit()
        return edit_msg(lesson.name, status=True)

    else:
        lesson.disabled = True
        db.session.commit()
        return del_msg(lesson.name, True)


@app.route(f'{api}/del_lesson_block/<int:block_id>', methods=['DELETE'])
def del_lesson_block(block_id):
    lesson_block = LessonBlock.query.filter(LessonBlock.id == block_id).first()
    if lesson_block.img_id:
        check_img_remove(lesson_block.img_id, Images)
    lesson_block.delete_commit()
    return del_msg(item="block", status=True)


@app.route(f'{api}/set_order', methods=['POST'])
def set_order():
    lessons_list = request.get_json()['lessons']
    lesson_get = Lesson.query.filter(Lesson.id == lessons_list[0]['id']).first()
    for lesson in lessons_list:
        Lesson.query.filter(Lesson.id == lesson['id']).update({"order": lesson['order']})
        db.session.commit()
    lessons = Lesson.query.filter(Lesson.level_id == lesson_get.level_id, Lesson.disabled != True).order_by(Lesson.order).all()
    return jsonify({
        "data": iterate_models(lessons),
        "length": len(lessons)
    })
