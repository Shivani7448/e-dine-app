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
  app.run()