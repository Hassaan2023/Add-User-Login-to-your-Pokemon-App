from app import app
from flask import redirect,render_template, request, url_for
from .forms import pokemonform, loginform ,signupform
from .utils import get_pokemon
from .models import db,User
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/")
def index_html():
    python_people = ["Shoha", "Pearl", "Jennifer", "Dimitrius", "Donte", "Brendan"]
    return render_template("index.html", message="Hello from my template", red=True, html_people=python_people)

@app.route("/new-html")
def new_html():
    return render_template("base.html")

@app.route("/page2")
def page2():
    return render_template("page2.html")

@app.route("/json")
def json():
    return {"message": "Hello from my updated API!"}


@app.route("/input",methods=["GET","POST"])
def input_pokemon():
    form = pokemonform()    
    if request.method == "POST":
        print("POST")
        print(form.pokemon.data)
        if form.validate():
            print("validate")
            query = form.pokemon.data
            pokemon = get_pokemon(query)
            print(pokemon)
            if pokemon: 
                return render_template('input.html', form=form, pokemon=pokemon)
    return render_template('input.html', form=form)
    

@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    form = signupform()  
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    print(request.method)
    if request.method == "POST":
        print("POST REQUEST MADE")
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            

            user = User(username,email,password)

            db.session.add(user)
            db.session.commit()
        
    return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"]) 
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = loginform()
    if request.method == "POST":
        print("POST REQUEST MADE")
        if form.validate():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user:
                if user.password == password:
                    login_user(user)
                else:
                    print('Password does not match')
                return redirect(url_for('input'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_page'))