
from flask import Flask, request, render_template, redirect, url_for, session

from database.create_table import create_user_table
from database.insert_data import register_user
from database.verification import verify_user, check_user_for_otp
from database.products import get_products

app = Flask(__name__)
app.secret_key = "my_secret_key"


# ---------------- HOME PAGE ----------------

@app.route("/")
def home():

    user = session.get("user")

    # Fetch fresh products from SQL
    fresh_products = get_products()

    return render_template(
        "index.html",
        user=user,
        products=fresh_products
    )


# ---------------- SIGNUP ----------------

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        Name = request.form.get('name')
        Surname = request.form.get('Surname')
        Contact = request.form.get('contact')
        Email = request.form.get('email')
        Password = request.form.get('password')
        Confirm_password = request.form.get('confirm_password')

        if Password != Confirm_password:
            return render_template(
                'signup.html',
                message="Password does not match!"
            )

        create_user_table()

        message = register_user(
            Name, Surname, Email, Contact, Password
        )

        return render_template('signup.html', message=message)

    return render_template("signup.html")


# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        login_type = request.form.get('login_type')
        identity = request.form.get('identity')
        password = request.form.get('password')
        otp = request.form.get('otp')

        if password:

            user = verify_user(login_type, identity, password)

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

                generated_otp = check_user_for_otp(
                    login_type, identity
                )

                if generated_otp:
                    session['login_otp'] = generated_otp
                    session['otp_identity'] = identity

                    return "OTP generated: " + generated_otp

                return "Email not registered!"

    return render_template("signin.html")


# ---------------- ACCOUNT ----------------

@app.route("/account")
def account():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "account.html",
        user=session["user"]
    )


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(url_for("home"))


# ---------------- PRODUCT CATEGORIES ----------------

@app.route("/fruits")
def fruits():

    return render_template(
        "fruits.html",
        # user=session.get("user")
    )


@app.route("/vegetables")
def vegetables():

    return render_template(
        "vegetables.html",
        user=session.get("user")
    )


@app.route("/groceries")
def groceries():

    return render_template(
        "groceries.html",
        user=session.get("user")
    )


@app.route("/dairy-products")
def dairy_products():

    return render_template(
        "dairy_products.html",
        user=session.get("user")
    )


@app.route("/special-offers")
def special_offers():

    return render_template(
        "special_offers.html",
        user=session.get("user")
    )


@app.route("/dry-fruits")
def dry_fruits():

    return render_template(
        "dry_fruits.html",
        user=session.get("user")
    )


# ---------------- ADD TO CART ----------------

@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):

    # TODO: Add cart logic here

    return redirect(url_for("home"))


# ---------------- RUN APPLICATION ----------------

if __name__ == '__main__':
    app.run(debug=True)
