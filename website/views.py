import os
import uuid as uuid

from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from website import app, cache, db, login_manager
from website.forms import *
from website.models import *
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from sqlalchemy.exc import IntegrityError


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route("/")
def index():
    all_services = Services.query.all()
    return render_template("index.html", title="Головна сторінка", services=all_services)


@app.route("/login", methods=["GET", "POST"])
def login():
    print("user_login")
    form = UserLogin()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html", title="Авторизація", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = Registration()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data, method="scrypt")
        user = Users(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=password_hash,
        )
        try:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
        except IntegrityError:
            db.session.rollback()

    return render_template("register.html", title="Реєстрація", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    user_services = Services.query.filter_by(user_id=current_user.id).all()
    return render_template("profile.html", title="Мій профіль", services=user_services)


@app.route("/add_service", methods=["GET", "POST"])
@login_required
def add_service():
    form = ServiceForm()
    if form.validate_on_submit():
        service = Services(
            service_name=form.service_name.data,
            description=form.description.data,
            price=float(form.price.data),
            user_id=current_user.id,
            contact=form.contact.data,
        )
        db.session.add(service)
        db.session.commit()

        if "photo" in request.files:
            photo = request.files["photo"]
            if photo.filename != "":
                filename = secure_filename(photo.filename)
                unique_filename = str(uuid.uuid4()) + "_" + filename
                photo.save(os.path.join("website/static/photo", unique_filename))

                photo_record = Photos(
                    service_id=service.id,
                    photo_url="/static/photo/" + unique_filename,
                )
                db.session.add(photo_record)
                db.session.commit()

        return redirect(url_for("index"))

    return render_template("add_service.html", title="Додати послугу", form=form)



@app.route("/service/<int:service_id>")
@cache.cached(timeout=60)
def service(service_id):
    service = Services.query.get_or_404(service_id)
    service.views += 1
    db.session.commit()
    return render_template("service.html", title="Послуга", service=service)


@app.route("/edit_service/<int:service_id>", methods=["GET", "POST"])
@login_required
def edit_service(service_id):
    service = Services.query.get_or_404(service_id)

    if service.user_id != current_user.id:
        return redirect(url_for("index"))

    form = ServiceForm(obj=service)

    if form.validate_on_submit():
        service.service_name = form.service_name.data
        service.description = form.description.data
        service.price = float(form.price.data)
        service.contact = form.contact.data

        db.session.commit()

        if "photo" in request.files:
            photo = request.files["photo"]
            if photo.filename != "":
                filename = secure_filename(photo.filename)
                unique_filename = str(uuid.uuid4()) + "_" + filename
                photo.save(os.path.join("website/static/photo", unique_filename))

                photo_record = Photos(
                    service_id=service.id,
                    photo_url="/static/photo/" + unique_filename,
                )
                db.session.add(photo_record)
                db.session.commit()

        return redirect(url_for("service", service_id=service.id))

    return render_template(
        "edit_service.html",
        title="Редагування послуги",
        form=form,
        service=service,
    )


@app.route("/delete_service/<int:service_id>")
@login_required
def delete_service(service_id):
    service = Services.query.get_or_404(service_id)

    if service.user_id != current_user.id:
        return redirect(url_for("index"))

    Photos.query.filter_by(service_id=service.id).delete()
    db.session.delete(service)
    db.session.commit()
    return redirect(url_for("profile"))

@app.route('/admin_panel')
@login_required
def admin_panel():
    if not current_user.is_admin:
        return redirect(url_for("index"))
    return render_template('admin_panel.html', title='Адмін панель')


@app.route('/add_admin', methods=['GET', 'POST'])
@login_required
def add_admin():
    if not current_user.is_admin:
        return redirect(url_for("index"))
    
    form = AdminForm()
    if form.validate_on_submit():
        username = form.username.data
        user = Users.query.filter_by(username=username).first()
        if user:
            user.is_admin = True
            db.session.commit()
    
    return render_template('admin_panel.html', title='Додати адміна', show="додати адміна", form=form)


@app.route('/manage_services')
@login_required
def manage_services():
    if not current_user.is_admin:
        return redirect(url_for("index"))
    return render_template('admin_panel.html', title='Керування послугами', services=Services.query.all(), show="керування послугами")


@app.route('/admin_delete_service/<int:service_id>')
@login_required
def admin_delete_service(service_id):
    if not current_user.is_admin:
        return redirect(url_for("index"))
    
    service_delete = Services.query.get_or_404(service_id)
    
    # Delete associated photos first
    Photos.query.filter_by(service_id=service.id).delete()
    
    # Delete the service
    db.session.delete(service_delete)
    db.session.commit()
    
    return redirect(url_for('manage_services'))