from flask import Flask, request, render_template, redirect, url_for, session
from database.create_table import create_user_table
from database.insert_data import register_user
from database.verification import verify_user,check_user_for_otp
from database.products import get_products

app=Flask(__name__)
app.secret_key = "my_secret_key"

@app.route("/")
def home():

    user = session.get("user")
    category = request.args.get("category")
    if category == "Fruits":
        return render_template("fruits.html")
    elif category=="Vegetables":
        return render_template('vegetables.html')
    elif category=='Groceries':
        return render_template('groceries.html')
    elif category=='Dairy':
        return render_template('dairy_products.html')
    elif category=='Special Offers':
            return render_template('special_offers.html') 
    elif category=='Dry Fruits':
        return render_template('dry_fruits.html')

    # Fresh products extract from sql 
    fresh_products=get_products() 
    print(fresh_products)

    return render_template(
        "index.html",
        user=user,products=fresh_products
    )

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        Name=request.form.get('name')
        Surname=request.form.get('Surname')
        Contact=request.form.get('contact')
        Email=request.form.get('email')
        Password=request.form.get('password')
        Confirm_password=request.form.get('confirm_password')
        print(Contact,len(Contact))
        if Password!=Confirm_password:
            return render_template('signup.html', message="Password does not match!")
        create_user_table()
        message=register_user(Name, Surname, Email, Contact, Password)
        return render_template('signup.html', message=message) 
         
    return render_template("signup.html")

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        login_type = request.form.get('login_type')
        identity = request.form.get('identity')
        password = request.form.get('password')
        otp = request.form.get('otp') 
        if password:
            user = verify_user(login_type, identity, password)
            print(user)
            if user:
                session["user"] = {
                    "id": user[0],
                    "name": user[1],
                    "surname": user[2],
                    "email": user[3],
                    "contact": user[4]
                }
                return redirect(url_for('home'))
        elif otp:

            if login_type == 'email':

                generated_otp = check_user_for_otp(login_type, identity)

                if generated_otp:
                    session['login_otp'] = generated_otp
                    session['otp_identity'] = identity

                    return "OTP generated: " + generated_otp

                return "Email not registered!"





    return render_template("signin.html")

@app.route("/account")
def account():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "account.html",
        user=session["user"]
    )
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(url_for("home"))

@app.route("/fruits")
def fruits():
    return render_template("fruits.html")

@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
  # TODO: Add cart logic here
  return redirect(url_for("home"))
if __name__=='__main__':
    app.run(debug=True)  