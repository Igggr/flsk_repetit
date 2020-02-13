from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, Form, FormField
from wtforms.validators import DataRequired, Length, ValidationError
import phonenumbers


class NamePhoneForm(Form):     # will not work with FlaskForm
    student_name = StringField("Вас зовут",
                               validators=[DataRequired(message="заполни")],
                               render_kw={"class": "form-control"})
    student_phone = StringField("Ваш телефон",
                                validators=[DataRequired(message="заполни"),
                                            Length(min=6,
                                            message="должен быть > 5 символов"
                                                   )
                                            ],
                                render_kw={"class": "form-control"}
                                )
    submit = SubmitField()

    def validate_student_phone(form, field):
        try:
            input_number = phonenumbers.parse(field.data, 'RU')
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError("Некоректный номер")
        except:
            raise ValidationError("Некоректный номер")


class BookingForm(FlaskForm):
    contact_info = FormField(NamePhoneForm)


class RequestMatchingTeacherForm(FlaskForm):

    # want choices like that
    # [(goal.goal_id, goal.title_rus) for goal in Goal.query],
    # so it will be single source of truth
    # now it prone to errors
    # unfortunately  can't read from database here
    # something about context
    goal_id = RadioField("goal_id",
                         choices=[("1", "Для путешествий"),
                                  ("2", "Для учебы"),
                                  ("3", "Для работы"),
                                  ("4", "Для переезда")
                                  ],
                         default="1")

    time_per_week = RadioField("time_per_week",
                               choices=[("1-2", "1-2 часа в неделю"),
                                        ("3-5", "3-5 часов в неделю"),
                                        ("5-7", "5-7 часов в неделю"),
                                        ("7-10", "7-10 часов в неделю")
                                        ],
                               default="1-2",
                               )

    contact_info = FormField(NamePhoneForm)
