from .database import db
class User(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  username = db.Column(db.String(),unique=True, nullable=False)
  email = db.Column(db.String(),unique=True, nullable=False)
  password = db.Column(db.String(), nullable=False)
  role = db.Column(db.String(), nullable=False, default='customer')
  reservations = db.relationship("Reservation", backref="user")

class Table(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  table_number = db.Column(db.String(), unique=True, nullable=False)
  capacity = db.Column(db.Integer(), nullable=False)
  location = db.Column(db.String(), nullable=False)
  status = db.Column(db.String(), nullable=False, default='available')
  reservations = db.relationship("Reservation", backref="table")

class Reservation(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
  table_id = db.Column(db.Integer(), db.ForeignKey('table.id'), nullable=False)
  date = db.Column(db.String(), nullable=False)
  time_slot = db.Column(db.String(), nullable=False)
  status = db.Column(db.String(), nullable=False, default='pending')





# 1. from database import db> error, app out of context
# 2. from application.database import db> models.py will think that there is application folder(inside application folder) inside that database.py file resides
# 3. from .database import db> this is the correct way to import db from database.py file, . means current folder, as models.py and database.py resides in same folder(application)   