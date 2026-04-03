from flask import Flask, render_template, redirect, url_for,request
# from app import app circular import error
from flask import current_app as app
from .models import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

@app.route("/login", methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username= request.form.get("username")
    pwd = request.form.get("pwd")
    this_user = User.query.filter_by(username=username).first()
    if this_user:
      if this_user.password == pwd:
        if this_user.role == "manager":
          return redirect("/manager")
          # return render_template("manager_dash.html", this_user=this_user)
        else:
          return redirect(f"/home/{this_user.id}")
      else:
        return render_template("incorrect_p.html")
        # return "<h1> Incorrect Password </h1>"
    else:
      return render_template("not_exist.html")
  return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
  if request.method == "POST":
    username= request.form.get("username")
    email = request.form.get("email")
    pwd = request.form.get("pwd")
    user_name = User.query.filter_by(username=username).first()
    user_email = User.query.filter_by(email=email).first()
    if user_name or user_email:
      return render_template("already.html")
    else:

      new_user = User(username=username, email=email, password=pwd)#LHS>model, RHS>form data
      db.session.add(new_user)
      db.session.commit()
      return redirect("/login")
  return render_template("register.html")

@app.route("/manager")
def manager():
  this_user = User.query.filter_by(role='manager').first()
  all_tables = Table.query.all()
  return render_template("manager_dash.html", this_user=this_user, all_tables=all_tables)

@app.route("/home/<int:user_id>")
def home(user_id):
  # this_user = User.query.get(user_id)
  this_user = User.query.filter_by(id=user_id).first()
  all_tables = Table.query.filter_by(status='available').all()
  return render_template("user_dash.html", this_user= this_user, all_tables= all_tables)

@app.route("/create_table", methods=['GET', 'POST'])
def create_table():
  if request.method == "POST":
    table_number = request.form.get("table_number")
    capacity = request.form.get("capacity")
    location = request.form.get("location")
    new_table = Table(table_number=table_number, capacity=capacity, location=location)
    db.session.add(new_table)
    db.session.commit()
    return redirect("/manager")
  return render_template("create_table.html")

@app.route("/update_table/<int:table_id>", methods=['GET', 'POST'])
def update_table(table_id):
  tbl = Table.query.filter_by(id=table_id).first()
  if request.method == "POST":
    table_number = request.form.get("table_number")
    tbl.table_number = table_number
    tbl.capacity = request.form.get("capacity")
    tbl.location = request.form.get("location")
    tbl.status = request.form.get("status")
    db.session.commit()
    return redirect("/manager")
  return render_template("update_table.html", tbl=tbl)

@app.route("/delete_table/<int:table_id>")
def delete_table(table_id):
  tbl = Table.query.filter_by(id=table_id).first()
  if tbl:
    db.session.delete(tbl)
    db.session.commit()
  return redirect("/manager")

@app.route("/manager/requests")
def m_requests():
  this_user = User.query.filter_by(role='manager').first()
  # all_res = Reservation.query.filter_by(status='pending').all()
  all_res = Reservation.query.all()
  return render_template("manager_request.html", this_user=this_user, all_res=all_res)

@app.route("/user/requests/<int:user_id>")
def u_requests(user_id):
  this_user = User.query.filter_by(id=user_id).first()
  all_res = Reservation.query.filter_by(user_id=user_id).all()
  return render_template("user_request.html", this_user=this_user, all_res=all_res)

@app.route("/reserve/<int:table_id>/<int:user_id>", methods=['GET', 'POST'])
def reserve(table_id, user_id):
  tbl = Table.query.filter_by(id=table_id).first()
  user = User.query.get(user_id)
  if request.method == "POST":
    date = request.form.get("date")
    time_slot = request.form.get("time_slot")
    new_reservation = Reservation(user_id=user_id, table_id=table_id, date=date, time_slot=time_slot)
    db.session.add(new_reservation)
    db.session.commit()
    return redirect(f"/home/{user_id}")
  return render_template("reserve.html", tbl=tbl, user=user)

@app.route('/approve/<int:res_id>')
def approve(res_id):
    res = Reservation.query.filter_by(id=res_id).first()
    if not res:
        return '<h1>Reservation not found</h1>'
    conflict = Reservation.query.filter_by(table_id=res.table_id, date=res.date, time_slot=res.time_slot, status='approved').first()
    if conflict:
        return '<h1>Table already booked for this slot</h1>'
    res.status = 'approved'
    db.session.commit()
    return redirect('/manager/requests')

@app.route('/reject/<int:res_id>')
def reject(res_id):
    res = Reservation.query.filter_by(id=res_id).first()
    if res:
        res.status = 'rejected'
        db.session.commit()
    return redirect('/manager/requests')

@app.route('/cancel/<int:res_id>')
def cancel(res_id):
    res = Reservation.query.filter_by(id=res_id).first()
    if res and res.status == 'pending':
        res.status = 'cancelled'
        db.session.commit()
    return redirect(f"/user/requests/{res.user_id}")

@app.route('/search')
def search():
    search_word = request.args.get('search')#search input
    key = request.args.get('key')#dropdown
    if key == 'user':
        result = User.query.filter_by(username=search_word).first()
    else:
        result = Table.query.filter_by(table_number=search_word).first()
    return render_template('result.html', result=result, key=key)

@app.route('/summary')
def summary():
    pe = len(Reservation.query.filter_by(status='pending').all())
    ap = len(Reservation.query.filter_by(status='approved').all())
    re = len(Reservation.query.filter_by(status='rejected').all())

    labels = ['Pending', 'Approved', 'Rejected']
    sizes = [pe, ap, re]
    colors = ['blue', 'green', 'red']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title('Reservation Status')
    plt.savefig('static/pie.png')
    plt.clf()

    plt.bar(labels, sizes, color=colors)
    plt.title('Reservation Status Distribution')
    plt.savefig('static/bar.png')
    plt.clf()

    return render_template('summary.html', pe=pe, ap=ap, re=re)
