from app.db import database as db
from app.models.center import Center
from datetime import datetime, date


class Turn(db.Model):
    __tablename__ = "turns"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    name = db.Column(db.String(30),nullable=True)
    surname = db.Column(db.String(30),nullable=True)
    starting_time = db.Column(db.String(30))
    date = db.Column(db.Date())
    tel = db.Column(db.String(30))
    center_id = db.Column(db.Integer, db.ForeignKey('centers.id')) # or centers

    def ending_time(self):
        hour, minute = self.starting_time.split(":")
        if minute == "30":
            hour = str(int(hour)+1)
            minute = "00"
        else:
            minute= "30"
        return (":").join([hour, minute])

    def day(self):
        return str(self.date).split(" ")[0]

    def update(self, email, starting_time, date):
        self.email = email
        self.starting_time = starting_time
        self.date = date
        db.session.commit()

    @classmethod
    def first(cls):
        return Turn.query.first()

    @classmethod
    def count(cls):
        return Turn.query.count()

    @classmethod
    def all(cls):
        return Turn.query.all()

    @classmethod
    def all_hours(cls):
        return [
          "9:00",
          "9:30",
          "10:00",
          "10:30",
          "11:00",
          "11:30",
          "12:00",
          "12:30",
          "13:00",
          "13:30",
          "14:00",
          "14:30",
          "15:00",
          "15:30"
        ]

    @classmethod
    def all_weekdays(cls):
        return ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

    @classmethod
    def group_by_date_and_hour(cls):
        turns_groups = {}
        for turn in Turn.all():
            if (turn.weekday() in turns_groups):
                if turn.starting_time in turns_groups[turn.weekday()]:
                    turns_groups[turn.weekday()][turn.starting_time] += 1
                else:
                    turns_groups[turn.weekday()][turn.starting_time] = 1
            else:
                turns_groups[turn.weekday()] = { turn.starting_time: 1 }
        return turns_groups

    def weekday(self):
        return Turn.all_weekdays()[self.date.weekday()]

    @classmethod
    def hours_date(cls, center_id, date):
        return [turn.starting_time for turn in Center.find(center_id).turns if turn.date.date() == date]

    @classmethod
    def free_hours(cls, center_id, date):
        center_hours = Turn.hours_date(center_id, date)
        return [hour for hour in Turn.all_hours() if hour not in center_hours]

    @classmethod
    def free_hours_api(cls, center_id, date):
        center_hours = [turn.starting_time for turn in Center.find(center_id).turns if turn.date.strftime("%d/%m/%Y") == date]
        return [hour for hour in Turn.all_hours() if hour not in center_hours]

    @classmethod
    def create(cls, email, starting_time, date, center,tel,name='',surname=''):
        turn = Turn(
            email = email,
            starting_time = starting_time,
            date = date,
            center = center,
            tel=tel,
            name= name,
            surname=surname,
        )
        db.session.add(turn)
        db.session.commit()
        return turn

    def destroy(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find(self, id):
        return Turn.query.filter_by(id=id).one()

    @classmethod
    def find_by(cls, **args):
        return Turn.query.filter_by(**args).first()

    @classmethod
    def seed(cls, email, starting_time, date, center, tel=''):
      existing_turn = Turn.find_by(starting_time = starting_time, date = date)
      if existing_turn:
        return existing_turn
      else:
        return Turn.create(email, starting_time, date, center, tel)

    @classmethod
    def hours_assigns_api(cls, center_id, date):
        return len([turn.starting_time for turn in Center.find(center_id).turns if turn.date.date() == date.date()])
