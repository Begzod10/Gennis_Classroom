from app import *
from backend.models.basic_model import *
from backend.basics.settings import *
from backend.models.settings import *


@app.route(f'{api}/info_level/<int:subject_id>', methods=['POST', 'GET'])
def info_level(subject_id):
    subject_levels = SubjectLevel.query.filter(SubjectLevel.subject_id == subject_id,
                                               SubjectLevel.disabled == False).order_by(SubjectLevel.id).all()
    if request.method == "POST":
        get_json = request.get_json()
        name = get_json['name']
        desc = get_json['desc']
        try:
            add = SubjectLevel(name=name, desc=desc, subject_id=subject_id)
            add.add_commit()
            subject_levels = SubjectLevel.query.filter(SubjectLevel.subject_id == subject_id,
                                                       SubjectLevel.disabled == False).order_by(
                SubjectLevel.id).all()
            return create_msg(f"{name}", status=True, data=iterate_models(subject_levels))

        except:
            return create_msg(f"{name}", status=False, data=iterate_models(subject_levels))

    else:
        return jsonify({
            "data": iterate_models(subject_levels)
        })


@app.route(f'{api}/level/<int:level_id>')
def level(level_id):
    level_get = SubjectLevel.query.filter(SubjectLevel.id == level_id).first()

    return jsonify({
        "data": level_get.convert_json()
    })


@app.route(f'{api}/edit_level/<int:level_id>', methods=['POST', 'DELETE'])
def edit_level(level_id):
    if request.method == "POST":
        get_json = request.get_json()
        name = get_json['name']
        desc = get_json['desc']
        level = SubjectLevel.query.filter(SubjectLevel.id == level_id).first()
        try:
            SubjectLevel.query.filter(SubjectLevel.id == level_id).update({
                "name": name,
                "desc": desc
            })
            db.session.commit()
            return edit_msg(f"{name}", status=True, data=level.convert_json())
        except:
            return edit_msg(f"{name}", status=False, data=level.convert_json())
    else:
        level_name = SubjectLevel.query.filter(SubjectLevel.id == level_id).first()
        name = level_name.name
        level_name.disabled = True
        db.session.commit()

        return del_msg(item=name, status=True)
