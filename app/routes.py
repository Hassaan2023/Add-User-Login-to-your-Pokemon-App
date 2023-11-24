from app import app
from flask import redirect,render_template, request, url_for, flash
from .forms import pokemonform, loginform ,signupform
from .utils import get_pokemon
from .models import db,User, Pokemon
from flask_login import login_user, logout_user, current_user, login_required
from flask import current_app


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


@app.route("/input", methods=["GET", "POST"])
@login_required
def input_pokemon():
    form = pokemonform()
    if request.method == "POST" and form.validate():
        query = form.pokemon.data
        pokemon_data = get_pokemon(query)

        if pokemon_data:
            user_collection = current_user.pokemon_collection

            # Check if the user already has this Pokemon
            if any(pokemon.pokemon_name == pokemon_data['pokemon_name'] for pokemon in user_collection):
                return render_template('input.html', form=form, pokemon=pokemon_data, message="You already have this Pokemon in your collection!")

            # Check if the user has less than 5 total Pokemon in their collection
            if len(user_collection) < 5:
                new_pokemon = Pokemon(
                    pokemon_name=pokemon_data['pokemon_name'],
                    ability_name=pokemon_data['ability_name'],
                    base_experience=pokemon_data['base_experience'],
                    front_shiny=pokemon_data['front_shiny'],
                    user_id=current_user.id
                )

                db.session.add(new_pokemon)
                db.session.commit()

                return render_template('input.html', form=form, pokemon=pokemon_data, message="You caught a new Pokemon!")
            else:
                return render_template('input.html', form=form, pokemon=pokemon_data, message="Your Pokemon collection is full! Release a Pokemon to make space.")

    return render_template('input.html', form=form)
    

@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    form = signupform()
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == "POST" and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email address is already in use. Please use a different email.", 'error')
            return render_template('signup.html', form=form)

        user = User(username, email, password)

        db.session.add(user)
        db.session.commit()

        # Redirect to the login page
        flash("Account created successfully! Please log in.", 'success')
        return redirect(url_for('login_page'))

    return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = loginform()
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            # Redirect to 'index' if the user is authenticated
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_page'))

@app.route("/manage_collection", methods=["GET", "POST"])
@login_required
def manage_collection():
    user_collection = current_user.pokemon_collection

    if request.method == "POST":
        action = request.form.get('action')
        pokemon_id = request.form.get('pokemon_id')

        if action == 'add' and len(user_collection) < 5:
            selected_pokemon = Pokemon.query.get(pokemon_id)

            if selected_pokemon not in user_collection:
                current_user.pokemon_collection.append(selected_pokemon)
                db.session.commit()
                flash("Pokemon added to your collection!", 'success')
            else:
                flash("You already have this Pokemon in your collection!", 'info')

        elif action == 'remove':
            pokemon_to_remove = Pokemon.query.get(pokemon_id)

            if pokemon_to_remove in user_collection:
                current_user.pokemon_collection.remove(pokemon_to_remove)
                db.session.commit()
                flash("Pokemon removed from your collection!", 'success')
            else:
                flash("You don't have this Pokemon in your collection!", 'info')

    return render_template('manage_collection.html', user_collection=user_collection)

@app.route("/attack_users", methods=["GET", "POST"])
@login_required
def attack_users():
    other_users = User.query.filter(User.id != current_user.id).all()

    return render_template('attack_users.html', other_users=other_users)

@app.route("/attack/<int:user_id>", methods=["GET", "POST"])
@login_required
def attack_user(user_id):
    opponent = User.query.get(user_id)

    if request.method == "POST":
        # Assuming a simple logic for determining the winner based on random chance
        import random
        if random.random() < 0.5:  # 50% chance of winning
            winner = current_user
        else:
            winner = opponent

        current_user.wins += 1 if winner == current_user else 0
        current_user.losses += 1 if winner == opponent else 0
        db.session.commit()
        flash("Attack completed! You " + ("won!" if winner == current_user else "lost!"), 'info')

    return render_template('attack_user.html', user=current_user, opponent=opponent, winner=winner)