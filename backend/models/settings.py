from backend.basics.settings import *


def iterate_models(model, relationship=None, entire=False):
    list = []
    for subject in model:
        if relationship == "exercise_types":
            if not subject.exercises:
                list.append(subject.convert_json(entire=entire))
            else:
                list.append(subject.convert_json_check())
        else:
            list.append(subject.convert_json(entire=entire))
    return list


def delete_list_models(model, Images):
    for subject in model:
        if subject.img_id:
            check_img_remove(subject.img_id, Images)
        subject.delete_commit()
