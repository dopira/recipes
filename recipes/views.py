from django.shortcuts import redirect, render

from recipes.models import Recipe


def home(request):
    if request.method == 'POST':
        return redirect('/users/ben/')
    return render(request, 'home.html')


def add(request):
    if request.method == 'POST':
        recipe = Recipe()
        recipe.title = request.POST.get('recipe_title', '')
        recipe.ingredients = request.POST.get('recipe_ingredients', '')
        recipe.directions = request.POST.get('recipe_directions', '')
        recipe.servings = request.POST.get('recipe_servings', '')
        recipe.save()
        return redirect('/users/ben/')

    return render(request, 'add.html')


def user(request):
    recipes = Recipe.objects.all()
    return render(request, 'user.html', {'recipes': recipes})