from flask import render_template, flash, redirect, url_for, request
from app import app, db 
from app.forms import LoginForm, RegistrationForm, EditProfileForm, RecommendationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Recommendation
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():

#         >>> # print post author and body for all posts 
# >>> posts = Post.query.all()
# >>> for p in posts:
# ...     print(p.id, p.author.username, p.body)
# ...
# 1 john my first post!
        recommendations = Recommendation.query.all()
     # [
#         {
#                 'recommender': {'username':'John'},
#                 'content': 'Diary of a Wimpy Kid.'
#         },
#         {
#                 'recommender': {'username': 'Susan'},
#                 'content': 'A Different World'
#         }
#     ]
        return render_template('index.html', title='Home', recommendations=recommendations)

@app.route('/login', methods=['GET', 'POST'])
def login():
        if current_user.is_authenticated:
                return redirect(url_for('index'))
                
        form = LoginForm()
        if form.validate_on_submit():
                user = User.query.filter_by(username=form.username.data).first()
                if user is None or not user.check_password(form.password.data):
                        flash('Invalid username or password')
                        return redirect(url_for('login'))
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                        next_page = url_for('index')
                return redirect(next_page)
        return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
        logout_user()
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
        if current_user.is_authenticated:
                return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
                user = User(username=form.username.data, email=form.email.data)
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Congratulations, you are now a registered user!')
                return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)

# Profile link
@app.route('/user/<username>')
@login_required
def user(username):    
        user = User.query.filter_by(username=username).first_or_404()
        user_recommendations = user.recommendations.all()
        recommendations = [
                # Later, I need to add if case for if a summary was not given
            {'recommender': user, 'content': user_recommendations},
            {'recommender': user, 'content': 'Test Recommendation'}]
                                                # {
                                                # {'book_title': }, 
                                                # {'book_author':}, 
                                                # {'book_summary':}}
        
        return render_template('user.html', user=user, recommendations=recommendations)
        # recommendations = [
        #     {'author': user, 'body': 'Test recommendation #1'},
        #     {'author': user, 'body': 'Test recommendation #2'}
        # ]
        # return render_template('user.html', user=user, recommendations=recommendations)

@app.before_request
def before_request():
        if current_user.is_authenticated:
                current_user.last_seen = datetime.utcnow()
                db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
        form = EditProfileForm()
        if form.validate_on_submit():
                current_user.username = form.username.data
                current_user.about_me = form.about_me.data
                db.session.commit()
                flash('Your changes have been saved.')
                return redirect(url_for('edit_profile'))
        elif request.method == 'GET':
                form.username.data = current_user.username
                form.about_me.data = current_user.about_me
        return render_template('edit_profile.html', title='Edit Profile', form=form)

# Function for routing recommendation button
@app.route('/new_recommendation', methods=['GET', 'POST'])
@login_required
def new_recommendation():
        form = RecommendationForm()
        if form.validate_on_submit():
                #gets all information from the Recommendation form created in forms.py
                u = User.query.get(1)
                recommendation = Recommendation(book_title=form.book_title.data, book_author=form.book_author.data, book_summary=form.book_summary.data, recommender=u)
                db.session.add(recommendation)
                db.session.commit()
                flash('Awesome, your recommendation is now posted!')

                # # I wanted to redirect the user to their profile page, so that they could see their new recommendation
                  # on top of their other recommendations, but I need to keep things simple for now.
                # return redirect(url_for('user', username=current_user.username))
                return redirect(url_for('index'))


        # if the form has not been filled out yet, then it will be come to this return function to be rendered
        return render_template('new_recommendation.html', title='New Recommendation', form=form)