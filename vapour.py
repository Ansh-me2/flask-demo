from flask import Flask, url_for, render_template, g, request, redirect
import os
import sqlite3


app = Flask(__name__)
DATABASE = "vapour.db"

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
		db.row_factory = sqlite3.Row
	return db

def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv

def change_db(query,args=()):
	cur = get_db().execute(query, args)
	get_db().commit()
	cur.close()

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()


# FOR GAME TABLE
@app.route("/")
def index_game():
	game_list = query_db("SELECT * FROM GAME")
	return render_template("index_game.html", game_list=game_list)

@app.route('/create_game', methods=['GET', 'POST'])
def create_game():
	if request.method == "GET":
		return render_template("create.html",GAME=None)
	if request.method == "POST":
		GAME = request.form.to_dict()
		values = [GAME["GAME_ID"], GAME["GAME_NAME"], GAME["PUBLISHER"], GAME["SIZE"], GAME["PRICE"]]
		change_db("INSERT INTO GAME (GAME_ID, GAME_NAME, PUBLISHER, SIZE, PRICE) VALUES (?, ?, ?, ?, ?)", values)
		return redirect(url_for("index"))

@app.route('/update/<int:GAME_ID>', methods=['GET', 'POST'])
def update(GAME_ID):
	if request.method == "GET":
		GAME = query_db("SELECT * FROM GAME WHERE GAME_ID=?", [GAME_ID], one=True)
		return render_template("update.html", GAME=GAME)
	if request.method == "POST":
		GAME = request.form.to_dict()
		values = [GAME["GAME_ID"], GAME["GAME_NAME"], GAME["PUBLISHER"], GAME["SIZE"], GAME["PRICE"], GAME_ID]
		change_db("UPDATE GAME SET GAME_ID=?, GAME_NAME=?, PUBLISHER=?, SIZE=?, PRICE=? WHERE GAME_ID=?", values)
		return redirect(url_for("index"))

@app.route('/delete/<int:GAME_ID>', methods=['GET', 'POST'])
def delete(GAME_ID):
	if request.method == "GET":
		GAME = query_db("SELECT * FROM GAME WHERE GAME_ID=?", [GAME_ID], one=True)
		return render_template("delete.html", GAME=GAME)
	if request.method == "POST":
		change_db("DELETE FROM GAME where GAME_ID=?", [GAME_ID])
		return redirect(url_for("index"))

#FOR PUBLISHER TABLE

@app.route("/PUBLISHER")
def indexpub():
	pub_list = query_db("SELECT * FROM PUBLISHER")
	return render_template("indexpub.html", pub_list=pub_list)

@app.route('/createpub', methods=['GET', 'POST'])
def createpub():
	if request.method == "GET":
		return render_template("createpub.html",PUBLISHER=None)
	if request.method == "POST":
		PUBLISHER = request.form.to_dict()
		values = [PUBLISHER["PUB_ID"], PUBLISHER["PUB_NAME"], PUBLISHER["ADDRESS"], PUBLISHER["PHONE_NO"], PUBLISHER["COMMISSION"]]
		change_db("INSERT INTO PUBLISHER (PUB_ID, PUB_NAME, ADDRESS, PHONE_NO, COMMISSION) VALUES (?, ?, ?, ?, ?)", values)
		return redirect(url_for("indexpub"))

@app.route('/updatepub/<int:PUB_ID>', methods=['GET', 'POST'])
def updatepub(PUB_ID):
	if request.method == "GET":
		PUBLISHER = query_db("SELECT * FROM PUBLISHER WHERE PUB_ID=?", [PUB_ID], one=True)
		return render_template("updatepub.html", PUBLISHER=PUBLISHER)
	if request.method == "POST":
		PUBLISHER = request.form.to_dict()
		values = [PUBLISHER["PUB_ID"], PUBLISHER["PUB_NAME"], PUBLISHER["ADDRESS"], PUBLISHER["PHONE_NO"], PUBLISHER["COMMISSION"], PUB_ID]
		change_db("UPDATE PUBLISHER SET PUB_ID=?, PUB_NAME=?, ADDRESS=?, PHONE_NO=?, COMMISSION=? WHERE PUB_ID=?", values)
		return redirect(url_for("indexpub"))

@app.route('/deletepub/<int:PUB_ID>', methods=['GET', 'POST'])
def deletepub(PUB_ID):
	if request.method == "GET":
		PUBLISHER = query_db("SELECT * FROM PUBLISHER WHERE PUB_ID=?", [PUB_ID], one=True)
		return render_template("deletepub.html", PUBLISHER=PUBLISHER)
	if request.method == "POST":
		change_db("DELETE FROM PUBLISHER where PUB_ID=?", [PUB_ID])
		return redirect(url_for("indexpub"))


#FOR USER TABLE
@app.route("/USER")
def index_user():
	user_list = query_db("SELECT * FROM USER")
	return render_template("index_user.html", user_list=user_list)

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
	if request.method == "GET":
		return render_template("create_user.html",USER=None)
	if request.method == "POST":
		USER = request.form.to_dict()
		values = [USER["USER_ID"], USER["USER_NAME"], USER["AGE"]]
		change_db("INSERT INTO USER (USER_ID, USER_NAME, AGE) VALUES (?, ?, ?)", values)
		return redirect(url_for("index_user"))

# TODO: update not updating in the form
@app.route('/update_user/<int:USER_ID>', methods=['GET', 'POST'])
def update_user(USER_ID):
	if request.method == "GET":
		USER = query_db("SELECT * FROM USER WHERE USER_ID=?", [USER_ID], one=True)
		return render_template("update_user.html", USER=USER_ID)
	if request.method == "POST":
		USER = request.form.to_dict()
		values = [USER["USER_ID"], USER["USER_NAME"], USER["AGE"], USER_ID]
		change_db("UPDATE USER SET USER_ID=?, USER_NAME=?, AGE=? WHERE USER_ID=?", values)
		return redirect(url_for("index_user"))

@app.route('/delete_user/<int:USER_ID>', methods=['GET', 'POST'])
def delete_user(USER_ID):
	if request.method == "GET":
		USER = query_db("SELECT * FROM USER WHERE USER_ID=?", [USER_ID], one=True)
		return render_template("delete_user.html", USER=USER)
	if request.method == "POST":
		change_db("DELETE FROM USER where USER_ID=?", [USER_ID])
		return redirect(url_for("index_user"))


#for PAYMENT TABLE
@app.route("/PAYMENT")
def index_pay():
	pay_list = query_db("SELECT * FROM PAYMENT")
	return render_template("index_pay.html", pay_list=pay_list)

@app.route('/create_pay', methods=['GET', 'POST'])
def create_pay():
	if request.method == "GET":
		return render_template("create_pay.html",PAYMENT=None)
	if request.method == "POST":
		PAYMENT = request.form.to_dict()
		values = [PAYMENT["PAY_ID"], PAYMENT["GAME_NAME"], GAME["PUBLISHER"], GAME["SIZE"], GAME["PRICE"]]
		change_db("INSERT INTO GAME (GAME_ID, GAME_NAME, PUBLISHER, SIZE, PRICE) VALUES (?, ?, ?, ?, ?)", values)
		return redirect(url_for("index"))

@app.route('/update/<int:GAME_ID>', methods=['GET', 'POST'])
def update(GAME_ID):
	if request.method == "GET":
		GAME = query_db("SELECT * FROM GAME WHERE GAME_ID=?", [GAME_ID], one=True)
		return render_template("update.html", GAME=GAME)
	if request.method == "POST":
		GAME = request.form.to_dict()
		values = [GAME["GAME_ID"], GAME["GAME_NAME"], GAME["PUBLISHER"], GAME["SIZE"], GAME["PRICE"], GAME_ID]
		change_db("UPDATE GAME SET GAME_ID=?, GAME_NAME=?, PUBLISHER=?, SIZE=?, PRICE=? WHERE GAME_ID=?", values)
		return redirect(url_for("index"))

@app.route('/delete/<int:GAME_ID>', methods=['GET', 'POST'])
def delete(GAME_ID):
	if request.method == "GET":
		GAME = query_db("SELECT * FROM GAME WHERE GAME_ID=?", [GAME_ID], one=True)
		return render_template("delete.html", GAME=GAME)
	if request.method == "POST":
		change_db("DELETE FROM GAME where GAME_ID=?", [GAME_ID])
		return redirect(url_for("index"))


if __name__ == '__main__':
	app.run(host="0.0.0.0",port=5010, debug=True)
