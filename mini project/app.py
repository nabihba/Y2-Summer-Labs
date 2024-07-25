from flask import Flask, render_template, request, redirect, url_for, session as login_session
import pyrebase

Config = {
    "apiKey": "AIzaSyBQC2B3oJmSiOFUPjjI--xwMk6yj4BafXE",
    "authDomain": "recipe-web-a4e1d.firebaseapp.com",
    "databaseURL": "https://recipe-web-a4e1d-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "recipe-web-a4e1d",
    "storageBucket": "recipe-web-a4e1d.appspot.com",
    "messagingSenderId": "970348308619",
    "appId": "1:970348308619:web:9019c1ae5282c9223a4c8e",
    "measurementId": "G-4MQNBJ8P99"
}

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['SECRET_KEY'] = 'Your_secret_string'

firebase = pyrebase.initialize_app(Config)
db = firebase.database()
auth = firebase.auth()



@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.create_user_with_email_and_password(email, password)
            login_session['user'] = user
            user_data = {"email": email, "password": password}
            UID = login_session['user']['localId']
            db.child("users").child(UID).set(user_data)
            return redirect(url_for('home'))
        except Exception as e:
            print(e)
            return "Registration failed, please try again."

    return render_template('register.html')

@app.route('/recipe/<recipe_id>', methods=['GET', 'POST'])
def recipe_detail(recipe_id):
    if 'user' not in login_session:
        return redirect(url_for('login'))
    
    recipe = db.child("recipes").child(recipe_id).get().val()
    comments = db.child("comments").order_by_child("recipe_id").equal_to(recipe_id).get().val()

    if request.method == 'POST':
        comment_text = request.form['comment']
        user_id = login_session['user']['localId']
        comment = {
            "recipe_id": recipe_id,
            "user_id": user_id,
            "email": login_session['user']['email'],
            "comment": comment_text
        }
        db.child("comments").push(comment)
        return redirect(url_for('recipe_detail', recipe_id=recipe_id))
    
    return render_template('recipe_detail.html', recipe=recipe, comments=comments)
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        all_recipes = db.child("recipes").get().val()
        filtered_recipes = {k: v for k, v in all_recipes.items() if query.lower() in v['title'].lower() or query.lower() in v['ingredients'].lower() or query.lower() in v['instructions'].lower()}
        return render_template('home.html', recipes=filtered_recipes)
    else:
        return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            login_session['user'] = user
            return redirect(url_for('home'))
        except Exception as e:
            print(e)
            return render_template('login.html')
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user' not in login_session:
        return redirect(url_for('login'))
    
    recipes = db.child("recipes").get().val()

    print(recipes)
    return render_template('home.html', recipes=recipes)




@app.route('/profile')
def profile():
    if 'user' not in login_session:
        return redirect(url_for('login'))
    
    user_id = login_session['user']['localId']
    user_data = db.child("users").child(user_id).get().val()
    user_recipes = db.child("recipes").order_by_child("user_id").equal_to(user_id).get().val()
    print(user_recipes)
    
    return render_template('profile.html', user=user_data, recipes=user_recipes)


@app.route('/logout')
def logout():
    login_session.pop('user', None)
    return redirect(url_for('login'))
    
    return render_template('recipe_detail.html', recipe=recipe, comments=comments)

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if 'user' not in login_session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        
        if not title or not ingredients or not instructions:
            error = "All fields are required."
            return render_template('add_recipe.html', error=error)

        UID = login_session['user']['localId']

        recipe = {
            "title": title,
            "ingredients": ingredients,
            "instructions": instructions,
            "user_id": UID
        }
        
        db.child("recipes").push(recipe)
        return redirect(url_for('home'))
    
    return render_template('add_recipe.html')
@app.route('/update_recipe/<recipe_id>', methods=['GET', 'POST'])
def update_recipe(recipe_id):
    if 'user' not in login_session:
        return redirect(url_for('login'))
    
    recipe = db.child("recipes").child(recipe_id).get().val()
    
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        
        updated_recipe = {
            "title": title,
            "ingredients": ingredients,
            "instructions": instructions,
            "user_id": recipe['user_id']
        }
        
        db.child("recipes").child(recipe_id).update(updated_recipe)
        return redirect(url_for('home'))
    
    return render_template('update_recipe.html', recipe=recipe)


@app.route('/delete_recipe/<recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    if 'user' not in login_session:
        return redirect(url_for('login'))
    
    db.child("recipes").child(recipe_id).remove()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
