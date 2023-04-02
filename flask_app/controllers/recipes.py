from flask import render_template, redirect, session, request
from flask_app import app 
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/recipe/dashboard')
def dashboard():
    data=User.find_by_id({"id":session["user_id"]})
    retreiving_all_recipes =Recipe.get_all()
    return render_template('dashboard.html',user=data, recipes =retreiving_all_recipes)

@app.route('/recipes/create')
def add_recipe():
    return render_template("add_recipe.html")


@app.route('/recipes/add_recipe',methods=["POST"])
def adding_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/create')
    Recipe.save(request.form)
    return redirect("/recipe/dashboard")


@app.route('/recipes/view_recipe/<int:id>')
def view_recipe(id):
    recipe_info= Recipe.find_by_id({"id":id})
    you = User.find_by_id({"id":session["user_id"]})
    return render_template("view_recipe.html",recipes=recipe_info, users=you)


@app.route('/recipes/edit_recipe/<int:id>')
def edit_recipe(id):
    recipe_info= Recipe.find_by_id({"id":id})
    you = User.find_by_id({"id":session["user_id"]})
    return render_template("edit_recipe.html",recipes=recipe_info, users=you)


@app.route('/recipes/editing_recipe',methods=["POST"])
def editing_recipe():
    print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",request.form)
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit_recipe/{request.form["id"]}')
    Recipe.update(request.form)

    return redirect("/recipe/dashboard")


@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    
    Recipe.delete({"id":id})
    return redirect("/recipe/dashboard")