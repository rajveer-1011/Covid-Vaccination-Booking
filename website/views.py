from . import db
from datetime import datetime
from .models import Vaccinationcenter,Booking
from flask_login import login_required, current_user
from flask import Blueprint,render_template,request,flash, redirect,url_for

views = Blueprint('views', __name__)

@views.route('/',  methods=['GET','POST'])
@login_required
def home():
    centers = Vaccinationcenter.query.order_by(Vaccinationcenter.name).all()
    bookings = Booking.query.filter(Booking.user_id== current_user.id).all()
    return render_template("home.html", user=current_user, centers=centers, bookings=bookings)


@views.route('/add/center',  methods=['GET','POST'])
@login_required
def add_center():
    if request.method == 'POST':
        centername = request.form.get('centername')        
        location = request.form.get('location')
        workinghours = request.form.get('workinghours')
        dosage = request.form.get('dosage')
        new_center=Vaccinationcenter(name=centername, location=location, working_hours=workinghours,  dosage=dosage)
        db.session.add(new_center)
        db.session.commit()
        flash('Center added successfully', category="success")
        return redirect(url_for("views.home"))

    return render_template("home.html", user=current_user)


@views.route('/delete/center/<int:id>',  methods=['GET','POST'])
@login_required
def delete_center(id):
    center = db.get_or_404(Vaccinationcenter, id)
    db.session.delete(center)
    db.session.commit()
    flash("Center deleted sucessfully", category='success')
    return redirect(url_for("views.home"))


@views.route('/search/result', methods=['GET', 'POST'])
def search():
    centers = Vaccinationcenter.query
    searchbox = request.form['search']
    # search query
    squery = centers.filter(Vaccinationcenter.name.like('%' + searchbox + '%')
                          | Vaccinationcenter.location.like('%' + searchbox + '%')
                          | Vaccinationcenter.working_hours.like('%' + searchbox + '%'))
    squery = squery.order_by(Vaccinationcenter.name).all()
    return render_template('searchresult.html', squery=squery, user=current_user, keyword=searchbox)


@views.route('/book/center/<int:id>',  methods=['GET','POST'])
@login_required
def bookcenter(id):
    centerid=id
    userid=current_user.id
    booking_date= datetime.utcnow().date()
    check = db.session.query(Booking).filter(Booking.user_id==userid).count()
    slots_availabel = db.session.query(Booking).filter((Booking.booking_date==datetime.utcnow().date()) & (Booking.center_id==id)).count()

    if check:
        flash('You already booked slot earlier',category="error")
        return redirect(url_for("views.home"))

    else:
        center = Vaccinationcenter.query.get(id)

        if ((slots_availabel >10)):
            flash('Center daily limit reached', category="error")
            center.slots_booked=10
            db.session.commit()
    
        book=Booking(user_id=userid, center_id=centerid, booking_date=booking_date)
        center.slots_booked=center.slots_booked-1
        center.dosage=center.dosage-1
        db.session.add(book)
        db.session.commit()
        flash('Vaccine slot boooked', category="success")
        return redirect(url_for("views.home"))





