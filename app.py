from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import PetForm, PetEdit

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption_agency_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'Thisisacoolproject1000!'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

db.create_all()

@app.route('/')
def pets_homepage():
    """Displays the pets homepage; listing all the pets"""
    all_pets = Pet.query.all()
    return render_template('pets_homepage.html', pets=all_pets)

@app.route('/add', methods=['GET','POST'])
def add_pet_form():
    """Displays the form to add a pet"""
    form = PetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        new_pet = None

        if photo_url and age and notes: #This is to prevent an integrity error and to prevent null values
             new_pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        elif photo_url and age:
             new_pet = Pet(name=name, species=species, photo_url=photo_url, age=age)
        elif photo_url and notes:
             new_pet = Pet(name=name, species=species, photo_url=photo_url, notes=notes)
        elif age and notes:
             new_pet = Pet(name=name, species=species, age=age, notes=notes)
        elif photo_url:
             new_pet = Pet(name=name, species=species, photo_url=photo_url)
        elif notes:
             new_pet = Pet(name=name, species=species, notes=notes)
        elif age:
             new_pet = Pet(name=name, species=species, age=age)
        else:
             new_pet = Pet(name=name,species=species)

        db.session.add(new_pet)
        db.session.commit()
        return redirect('/')
    else:
         return render_template('pet_add_form.html', form=form)

@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def pet_details_and_edit_form(pet_id):
    """Retrieves further details of the pet and gives the ability to edit and submit its changes"""
    pet = Pet.query.get(pet_id)
    form = PetEdit(obj=pet)

    if form.validate_on_submit():
        photo = form.photo_url.data
        notes = form.notes.data
        available = form.available.data
        pet.photo_url = photo
        pet.notes = notes
        pet.available = available
        db.session.add(pet)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('pet_page.html', pet=pet, form=form)
