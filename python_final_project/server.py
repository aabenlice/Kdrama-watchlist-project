from flask_app import app
import flask_app.controllers.users_controller
import flask_app.controllers.kdramas_controller

if __name__ == "__main__":
    app.run(debug=True)