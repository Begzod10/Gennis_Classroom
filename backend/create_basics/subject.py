from app import *
from backend.models.basic_model import *
from backend.basics.settings import *


@app.route(f"{api}/info_subjects", methods=["GET", "POST"])
def info_subjects():
    print('subject')
    subjects = Subject.query.filter(or_(Subject.disabled == False, Subject.disabled == None)).order_by(Subject.id).all()
    print(subjects)
    if request.method == "POST":
        info = request.form.get("info")
        print("post")
        json_file = json.loads(info)
        name = json_file['title']
        photo = request.files.get('file')
        desc = json_file['desc']

        if photo and check_file(photo.filename):
            get_img = add_file(photo, app, Images)
            add = Subject(name=name, desc=desc, img_id=get_img)
            add.add_commit()
            subjects = Subject.query.filter(or_(Subject.disabled == False, Subject.disabled == None)).order_by(
                Subject.id).all()
        return create_msg(f"{name}", status=True, data=iterate_models(subjects))

    else:
        return jsonify({
            "subjects": iterate_models(subjects)
        })


@app.route(f'{api}/subject/<int:subject_id>')
def subject(subject_id):
    try:
        subject_view = Subject.query.filter(Subject.id == subject_id).first()
        return jsonify({
            "data": subject_view.convert_json(),
            "status": True
        })
    except:
        return jsonify({
            "status": False
        })


@app.route(f'{api}/edit_subject/<int:subject_id>', methods=['POST'])
def edit_subject(subject_id):
    subject_get = Subject.query.filter(Subject.id == subject_id).first()
    if request.method == "POST":
        info = request.form.get("info")
        json_file = json.loads(info)
        photo = request.files.get('file')
        name = json_file['title']
        desc = json_file['desc']
        try:
            if photo and check_file(photo.filename):
                get_img = add_file(photo, app, Images)
                check_img_remove(subject_get.img_id, Images)
                Subject.query.filter(Subject.id == subject_id).update({
                    "name": name,
                    "desc": desc,
                    "img_id": get_img

                })
            else:
                Subject.query.filter(Subject.id == subject_id).update({
                    "name": name,
                    "desc": desc
                })
            db.session.commit()

            return edit_msg(f"{name}", status=True, data=subject_get.convert_json())
        except:
            return edit_msg(f"{name}", status=False, data=subject_get.convert_json())


@app.route(f'{api}/del_subject/<int:subject_id>', methods=['DELETE'])
def del_subject(subject_id):
    sub_name = Subject.query.filter(Subject.id == subject_id).first()
    name = sub_name.name
    sub_name.disabled = True
    db.session.commit()
    if sub_name.img_id:
        check_img_remove(sub_name.img_id, Images)
    return del_msg(item=name, status=True)
