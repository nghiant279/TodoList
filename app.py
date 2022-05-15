from flask import request
from flask import Flask, render_template, url_for, redirect 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(100))
    status = db.Column(db.String(100))

@app.route('/')
def index():
    todoList = Todo.query.all()
    return render_template("final.html", todoList = todoList)

@app.route("/add", methods = ["POST"])
def add():
    itemDescription = request.form.get("itemDescription")
    newTodo = Todo(description = itemDescription, status = "Doing")
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit", methods = ["POST"])
def edit():
    itemDescription = request.form.get("itemDescription")
    htmlID = request.form.get("itemID")
    intID = int(htmlID)
    todo = Todo.query.filter_by(id = intID).first() #from DB
    button = request.form.get("clickBtn")
    status = request.form.get("itemStatus")
    if status == "Doing":
        if button == "update":
                todo.description = itemDescription
                todo.status = "Done"
                db.session.commit()
        elif button == "delete":
            db.session.delete(todo)
            db.session.commit()

    elif status == None:
        if button == "update":
            todo.description = itemDescription
            db.session.commit()           
        elif button == "delete":
            db.session.delete(todo)
            db.session.commit()

    return redirect(url_for("index"))

if __name__ == "__main__":
    db.create_all()
    todoList = Todo.query.all()
    if todoList == []:
        sampleTodo = Todo(description = 'SS1 Assignment 1', status = "Done")
        db.session.add(sampleTodo)
        sampleTodo = Todo(description = 'SS1 Assignment 2', status = "Doing")
        db.session.add(sampleTodo)
        sampleTodo = Todo(description = 'SS1 Final', status = "Doing")
        db.session.add(sampleTodo)
        db.session.commit()
    app.run(debug=True)