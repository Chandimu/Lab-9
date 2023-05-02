from flask import Flask,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from models import *
from flask import request,url_for


app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes_app.db"
db.init_app(app)


@app.route('/',methods=["GET","POST"])
def main_menu():
    if request.method=="POST":
        note=Note(title="title",memo="memo",important=1)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for("item",note_pk=note.id))
        
    notes=db.session.execute(db.select(Note)).scalars()
    return render_template('main_menu.html',notes=notes)

@app.route('/create-note')
def create_note():
        note=Note(title="title",memo="memo",important=1)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for("item",note_pk=note.id))
@app.route('/item-<int:note_pk>',methods=["GET","POST"])
def item(note_pk):
    note=db.get_or_404(Note,note_pk)
    # if request.method=="POST" and re:
    #     note=Note(title=request.POST["title"],memo=request.POST["memo"],important=request.POST["important"])
    return render_template('item.html',note=note)


@app.route('/item-<int:note_pk>/change',methods=["GET","POST"])
def change_item(note_pk):
    note=db.get_or_404(Note,note_pk)
    if request.method=="POST":
            note.title=request.form.get("title")
            note.memo=request.form.get("memo")
            temp=request.form.get("important")
            if temp=='on':
                note.important=1
            else:
                note.important=0
            
            db.session.commit()
            return redirect(url_for("main_menu"))
       


@app.route('/item-<int:note_pk>/delete',methods=["GET","POST"])
def delete_item(note_pk):
    note=db.get_or_404(Note,note_pk)
    
      
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("main_menu"))


if __name__ == '__main__':
    app.run(port=7500)