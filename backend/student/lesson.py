from backend.models.basic_model import *
from app import *


@app.route(f'{api}/complete_exercise', methods=['POST'])
def complete_exercise():
    pprint(request.get_json())
    answers = request.get_json()['answers']
    student = Student.query.first()
    lesson_id = request.get_json()['lessonId']
    for answer in answers:
        block = ExerciseBlock.query.filter(ExerciseBlock.id == answer['block_id']).first()
        exercise = Exercise.query.filter(Exercise.id == block.exercise_id).first()
        if answer['innerType'] == "text" and answer['type'] == "question" or answer['innerType'] == "image" and answer['type'] == "question":
            exercise_answer = ExerciseAnswers.query.filter(ExerciseAnswers.block_id == answer['block_id'],
                                                           ExerciseAnswers.status == True).first()
            for ans in answer['answers']:
                if ans['checked'] == True:
                    if exercise_answer.id == ans['id']:
                        student_exercise = StudentExercise(student_id=student.id, lesson_id=lesson_id,
                                                           exercise_id=exercise.id, subject_id=exercise.subject_id,
                                                           type_id=exercise.type_id, level_id=exercise.level_id,
                                                           boolean=exercise_answer.status)
                        student_exercise.add_commit()
        elif answer["innerType"] == "innerInputs" and answer['type'] == "text":

            for ans in answer['answers']:
                exercise_answer = ExerciseAnswers.query.filter(ExerciseAnswers.block_id == answer['block_id'],
                                                               ExerciseAnswers.id == ans['back_id']).first()
                if exercise_answer.desc == ans['value']:
                    exercise_status = True
                else:
                    exercise_status = False

                student_exercise = StudentExercise(student_id=student.id, lesson_id=lesson_id,
                                                   exercise_id=exercise.id, subject_id=exercise.subject_id,
                                                   type_id=exercise.type_id, level_id=exercise.level_id,
                                                   boolean=exercise_status)
                student_exercise.add_commit()
        elif answer["innerType"] == "matchWords" and answer['type'] == "text":
            for ans in answer['answers']:
                exercise_answer = ExerciseAnswers.query.filter(ExerciseAnswers.block_id == answer['block_id'],
                                                               ExerciseAnswers.id == ans['back_id']).first()
                if exercise_answer.order == ans['parentIndex']:
                    exercise_status = True
                else:
                    exercise_status = False
                student_exercise = StudentExercise(student_id=student.id, lesson_id=lesson_id,
                                                   exercise_id=exercise.id, subject_id=exercise.subject_id,
                                                   type_id=exercise.type_id, level_id=exercise.level_id,
                                                   boolean=exercise_status)
                student_exercise.add_commit()
    return jsonify({
        "success": True
    })
