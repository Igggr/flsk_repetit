from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length


class NamePhoneForm(FlaskForm):
    name = StringField("Вас зовут",
                       validators=[DataRequired(message="заполни")])
    phone = StringField("Ваш телефон",
                        validators=[DataRequired(message="заполни"),
                                    Length(min=6,
                                           message="должен быть > 5 символов"
                                           )  # length check don't work
                                    ]
                        )
    submit = SubmitField()


class RequestMatchingTeacherForm(NamePhoneForm):
    # bad. I want composition, not inheritance
    # I just doesn't know - how to get data from embeded FormField
    # contacts = FormField(NamePhoneForm)

    goal = RadioField("goal", choices=[("travel", "Для путешествий"),
                                       ("study", "Для учебы"),
                                       ("work", "Для работы"),
                                       ("relocate", "Для переезда")
                                       ])

    time = RadioField("time", choices=[("1-2", "1-2 часа в неделю"),
                                       ("3-5", "3-5 часов в неделю"),
                                       ("5-7", "5-7 часов в неделю"),
                                       ("7-10", "7-10 часов в неделю")
                                       ])
