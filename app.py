from flask import Flask
app = None
from application.database import db
def create_app():
  app = Flask(__name__)
  app.debug = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///e-dine.sqlite3'
  db.init_app(app)
  app.app_context().push()
  return app

app = create_app()
from application.controllers import * #controllers file resides in application folder
if __name__ == "__main__":
  with app.app_context():
    db.create_all()
    Manager = User.query.filter_by(role='manager').first()
    if Manager is None:
      Manager = User(username='manager1',email='manager@user.com',password='1234',role='manager')
      db.session.add(Manager)
      db.session.commit()
  app.run()