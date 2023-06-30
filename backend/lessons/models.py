from backend.models.basic_model import *


class Subject(db.Model):
    __tablename__ = "subject"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    img_id = Column(Integer, ForeignKey('images.id'))
    desc = Column(String)
    levels = relationship("SubjectLevel", backref="subject", order_by="SubjectLevel.id")
    answer = relationship('ExerciseAnswers', backref="subject", order_by="ExerciseAnswers.id")
    lesson = relationship('Lesson', backref="subject", order_by="Lesson.id")
    exercise = relationship('Exercise', backref="subject", order_by="Exercise.id")
    student_question = relationship("StudentQuestion", lazy="select", order_by="StudentQuestion.id")
    question_answers = relationship("QuestionAnswers", lazy="select", order_by="QuestionAnswers.id")
    answer_comment = relationship("QuestionAnswerComment", lazy="select", order_by="QuestionAnswerComment.id")
    donelessons = relationship('StudentExercise', backref="subject", order_by="StudentExercise.id")
    studentsubject = relationship('StudentSubject', backref="subject", order_by="StudentSubject.id")
    certificate = relationship('Certificate', backref="subject", order_by="Certificate.id")
    disabled = Column(Boolean, default=False)

    def convert_json(self, entire=False):
        info = {
            "id": self.id,
            "name": self.name,
            "img": None,
            "desc": self.desc
        }
        if self.img and self.img.url:
            info['img'] = self.img.url
        return info

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class LevelCategory(db.Model):
    __tablename__ = "level_category"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ot = Column(Float)
    do = Column(Float)
    # students = relationship("Student", backref="level", order_by="Student.id", lazy="select")


class SubjectLevel(db.Model):
    __tablename__ = "subject_level"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)
    subject_id = Column(Integer, ForeignKey("subject.id"))
    disabled = Column(Boolean, default=False)
    lesson = relationship('Lesson', backref="subject_level", order_by="Lesson.id")
    exercise = relationship('Exercise', backref="subject_level", order_by="Exercise.id")
    donelessons = relationship("StudentExercise", backref="subject_level", order_by="StudentExercise.id")
    studentcourse = relationship('StudentCourse', backref="subject_level", order_by="StudentCourse.id")
    certificate = relationship('Certificate', backref="subject_level", order_by="Certificate.id")

    def convert_json(self, entire=False):
        return {
            "id": self.id,
            "name": self.name,
            "subject_id": self.subject_id,
            "desc": self.desc
        }

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class Lesson(db.Model):
    __tablename__ = "lesson"
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subject.id"))
    level_id = Column(Integer, ForeignKey("subject_level.id"))
    name = Column(String)
    blocks = relationship("LessonBlock", backref="lesson", order_by="LessonBlock.id")
    disabled = Column(Boolean, default=False)
    order = Column(Integer)

    def convert_json(self, entire=False):
        if entire:
            info = {
                "id": self.id,
                "name": self.name,
                "subject_id": self.subject.id,
                "subject_name": self.subject.name,
                "level_id": self.subject_level.id,
                "level_name": self.subject_level.name,
                "blocks": [],
                "order": self.order,
            }
            for block in self.blocks:
                block_info = {
                    "id": block.id,
                    "video_url": block.video_url,
                    "img": None,
                    "desc": block.desc,
                    "clone": block.clone,
                    "exercise_id": block.exercise_id,
                    "type": block.type_block
                }
                if block.img_id:
                    block_info['img'] = block.img.url
                info['blocks'].append(block_info)
            return info
        else:

            return {
                "id": self.id,
                "name": self.name,
                "subject_id": self.subject.id,
                "subject_name": self.subject.name,
                "level_id": self.subject_level.name,
                "order": self.order

            }

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class LessonBlock(db.Model):
    __tablename__ = "lesson_block"
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lesson.id'))
    exercise_id = Column(Integer, ForeignKey('exercise.id'))
    video_url = Column(String)
    img_id = Column(Integer, ForeignKey('images.id'))
    desc = Column(String)
    clone = Column(JSON)
    type_block = Column(String)

    def add_commit(self):
        db.session.add(self)
        db.session.commit()

    def delete_commit(self):
        db.session.delete(self)
        db.session.commit()


class ExerciseTypes(db.Model):
    __tablename__ = "exercise_types"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    exercises = relationship("Exercise", backref="exercise_types", order_by="Exercise.id")
    donelessons = relationship("StudentExercise", backref="exercise_types", order_by="StudentExercise.id")
    disabled = Column(Boolean, default=False)

    def convert_json(self, entire=False):
        return {
            "id": self.id,
            "del_status": False,
            "name": self.name,
        }

    def convert_json_check(self):
        return {
            "id": self.id,
            "del_status": True,
            "name": self.name
        }

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class Component(db.Model):
    __tablename__ = "component"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    exercise_blocks = relationship("ExerciseBlock", backref="component", order_by="ExerciseBlock.id")

    def convert_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "desc": self.desc
        }

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class Exercise(db.Model):
    __tablename__ = "exercise"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    subject_id = Column(Integer, ForeignKey("subject.id"))
    type_id = Column(Integer, ForeignKey('exercise_types.id'))
    level_id = Column(Integer, ForeignKey("subject_level.id"))
    block = relationship("ExerciseBlock", backref="exercise", lazy="select", order_by="ExerciseBlock.id")
    exercise_answers = relationship("ExerciseAnswers", backref="exercise", order_by="ExerciseAnswers.id")
    donelessons = relationship("StudentExercise", backref="exercise", order_by="StudentExercise.id")

    def add_commit(self):
        db.session.add(self)
        db.session.commit()

    def convert_json(self, entire=False):
        if entire:
            info = {
                "id": self.id,
                "name": self.name,
                "subject": {
                    "id": self.subject.id,
                    "name": self.subject.name
                },
                "type": {
                    "id": self.exercise_types.id,
                    "name": self.exercise_types.name

                },
                "level": {
                    "id": self.subject_level.id,
                    "name": self.subject_level.name
                },
                "block": [],
                "exercise_answers": [],
                "done_lessons": []
            }

            for block in self.block:
                info_block = {
                    "id": block.id,
                    "desc": block.desc,
                    "clone": block.clone,
                    "component": block.component.id,
                    "img": None,
                    "audio": block.audio_url,
                    "answers": []
                }
                if block.img:
                    info_block['img'] = block.img.url
                info['block'].append(info_block)
                for answers in block.exercise_answers:
                    info_answer = {
                        "id": answers.id,
                        "desc": answers.desc,
                        "order": answers.order,
                        "img": None,
                        "block_id": answers.block_id,
                        "type_img": answers.type_img
                    }
                    if answers.img:
                        info_answer['img'] = answers.img.url
                    info_block['answers'].append(info_answer)
            return info
        return {
            "id": self.id,
            "name": self.name,
            "subject": {
                "id": self.subject.id,
                "name": self.subject.name
            },
            "type": {
                "id": self.exercise_types.id,
                "name": self.exercise_types.name

            },
            "level": {
                "id": self.subject_level.id,
                "name": self.subject_level.name
            },
            "block": [],
            "exercise_answers": [],
            "done_lessons": []
        }

    def delete_commit(self):
        db.session.delete(self)
        db.session.commit()


class ExerciseBlock(db.Model):
    __tablename__ = "exercise_block"
    id = Column(Integer, primary_key=True)
    desc = Column(String)
    exercise_id = Column(Integer, ForeignKey('exercise.id'))
    clone = Column(JSON())
    component_id = Column(Integer, ForeignKey('component.id'))
    img_id = Column(Integer, ForeignKey('images.id'))
    audio_url = Column(String)
    exercise_answers = relationship("ExerciseAnswers", backref="exercise_block", order_by="ExerciseAnswers.id")

    def add_commit(self):
        db.session.add(self)
        db.session.commit()

    def delete_commit(self):
        db.session.delete(self)
        db.session.commit()


db.Table('lesson_exercise',
         db.Column('lesson_id', db.Integer, db.ForeignKey('lesson.id')),
         db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id'))
         )


class ExerciseAnswers(db.Model):
    __tablename__ = "exercise_answers"
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('exercise_types.id'))
    exercise_id = Column(Integer, ForeignKey('exercise.id'))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    level_id = Column(Integer, ForeignKey("subject_level.id"))
    desc = Column(String)
    order = Column(Integer)
    img_id = Column(Integer, ForeignKey('images.id'))
    status = Column(Boolean, default=False)
    block_id = Column(Integer, ForeignKey('exercise_block.id'))
    type_img = Column(String)

    def convert_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img.url,
            "desc": self.desc
        }

    def add_commit(self):
        db.session.add(self)
        db.session.commit()

    def delete_commit(self):
        db.session.delete(self)
        db.session.commit()


class StudentExercise(db.Model):
    __tablename__ = "student_exercise"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("student.id"))
    lesson_id = Column(Integer, ForeignKey("lesson.id"))
    level_id = Column(Integer, ForeignKey("subject_level.id"))
    type_id = Column(Integer, ForeignKey("exercise_types.id"))
    subject_id = Column(Integer, ForeignKey("subject.id"))
    exercise_id = Column(Integer, ForeignKey("exercise.id"))
    boolean = Column(Boolean)

    def convert_json(self, entire=False):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "desc": self.desc
        }

    def add_commit(self):
        db.session.add(self)
        db.session.commit()

    def delete_commit(self):
        db.session.delete(self)
        db.session.commit()


class StudentLesson(db.Model):
    __tablename__ = "student_lesson"
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lesson.id"))
    student_id = Column(Integer, ForeignKey("student.id"))
    percentage = Column(Integer)
    finished = Column(Boolean)

    def convert_json(self, entire=False):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "desc": self.desc
        }

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class StudentCourse(db.Model):
    __tablename__ = "student_course"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("subject_level.id"))
    student_id = Column(Integer, ForeignKey("student.id"))
    percentage = Column(Integer)
    finished = Column(Boolean)

    def convert_json(self, entire=False):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "desc": self.desc
        }

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class StudentSubject(db.Model):
    __tablename__ = "student_subject"
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subject.id"))
    student_id = Column(Integer, ForeignKey("student.id"))
    percentage = Column(Integer, default=0)
    finished = Column(Boolean, default=False)

    def convert_json(self, entire=False):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "desc": self.desc
        }

    def add_commit(self):
        db.session.add(self)
        db.session.commit()
