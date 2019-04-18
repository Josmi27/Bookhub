from flask import render_template, flash, redirect, url_for, request
from app import app, db 
from app.forms import LoginForm, RegistrationForm, EditProfileForm, RecommendationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Recommendation
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
       # recommendation = Recommendation(book_title)
        recommender=current_user
        page = request.args.get('page', 1, type=int)
        recommendations = current_user.followed_posts().paginate(
                page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('index', page=recommendations.next_num) \
                if recommendations.has_next else None
        prev_url = url_for('index', page = recommendations.prev_num) \
                if recommendations.has_prev else None
        return render_template('index.html', title='Home', recommender=recommender, recommendations=recommendations.items, next_url=next_url, prev_url=prev_url)


# Function for routing recommendation button
@app.route('/new_recommendation', methods=['GET', 'POST'])
@login_required
def new_recommendation():
        form = RecommendationForm()
        if form.validate_on_submit():
                recommendation = Recommendation(book_title=form.book_title.data, book_author=form.book_author.data, book_category=form.book_category.data, book_summary=form.book_summary.data, author=current_user)
                db.session.add(recommendation)
                db.session.commit()
                flash('Awesome, your recommendation is now posted!')

                # # I wanted to redirect the user to their profile page, so that they could see their new recommendation
                  # on top of their other recommendations, but I need to keep things simple for now.
                # return redirect(url_for('user', username=current_user.username))
                
                return redirect(url_for('index'))
        # if the form has not been filled out yet, then it will be come to this return function to be rendered
        return render_template('new_recommendation.html', title='New Recommendation', form=form)

@app.route('/explore')
@login_required
def explore():

        recommender=current_user
        page = request.args.get('page', 1, type=int)
        recommendations = current_user.followed_posts().paginate(
                page, app.config['POSTS_PER_PAGE'], False)
        return render_template('index.html', title='Home', recommender=recommender, recommendations=recommendations.items)


#     page = request.args.get('page', 1, type=int)
#     recommendations = Recommendation.query.order_by(Recommendation.timestamp.desc()).paginate(
#         page, app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('explore', page=recommendations.next_num) \
#         if recommendations.has_next else None
#     prev_url = url_for('explore', page=recommendations.prev_num) \
#         if recommendations.has_prev else None
#     return render_template("index.html", title='Explore', author=current_user, recommendations=recommendations.items, next_url=next_url, prev_url=prev_url)
#     page = request.args.get('page', 1, type=int)
#     recommendations = Recommendation.query.order_by(Recommendation.timestamp.desc()).all()
# #     recommender=current_user
#     return render_template('index.html', title='Explore', recommendations=recommendations)


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
        page = request.args.get('page', 1, type=int)
        recommendations = user.recommendations.order_by(Recommendation.timestamp.desc()).paginate(
                page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('user', username=user.username, page=recommendations.next_num) \
                if recommendations.has_next else None
        prev_url = url_for('user', username=user.username, page=recommendations.prev_num) \
                if recommendations.has_prev else None
        return render_template('user.html', user=user, recommendations=recommendations.items, next_url=next_url, prev_url=prev_url)


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

@app.route('/follow/<username>')
@login_required
def follow(username):
        user = User.query.filter_by(username=username).first()
        if user is None:
                flash('User {} not found.'.format(username))
                return redirect(url_for('index'))
        if user == current_user:
                flash('You cannot follow yourself!')
                return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}'.format(username))
        return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))