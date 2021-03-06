from django.shortcuts import redirect, render, get_object_or_404
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.utils.html import escape

from .models import User, Recipe
from .forms import RecipeForm
from .tools.bas.scraper import scrape

import os
import shutil
import logging


def home(request):
    if request.method == 'POST':
        user_ = User()
        user_.display_name = request.POST.get('user_name', '')
        user_.name = user_.display_name.lower()
        user_.save()
        return redirect('/users/%s/' % user_.name, {'user': user_})
    users = User.objects.all()
    return render(request, 'home.html', {'users': users})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def add_recipe(request, user_name):
    if request.method == 'POST':
        import_url = request.POST.get('import_url', '')
        if import_url:
            data = scrape(import_url)
            data['ingredients'] = '\n'.join(data['ingredients'])
            data['directions'] = '\n'.join(data['directions'])
            form = RecipeForm(data=data)
            return render(request, 'add.html', {'form': form})
        form = RecipeForm(data=request.POST)
        if form.is_valid():
            user_ = User.objects.get(name=user_name)
            recipe = Recipe()
            recipe.title = request.POST.get('title', '')
            recipe.ingredients = request.POST.get('ingredients', '')
            recipe.directions = request.POST.get('directions', '')
            recipe.servings = request.POST.get('servings', '')
            recipe.source = request.POST.get('source', '')
            recipe.source_url = request.POST.get('source_url', '')
            recipe.img_url = request.POST.get('img_url', '')
            recipe.cooking_time = request.POST.get('cooking_time', '')
            recipe.total_time = request.POST.get('total_time', '')
            recipe.notes = request.POST.get('notes', '')
            recipe.user = user_
            recipe.url_name = recipe.title.lower().replace(' ', '-')
            recipe.url = '/users/%s/recipe/%s' % (user_name, recipe.url_name)
            recipe.save()
            return redirect('/users/%s/' % user_.name)
        else:
            return render(request, 'add.html', {'form': form})
    else:
        return render(request, 'add.html', {'form': RecipeForm()})


def user(request, user_name):
    user_ = User.objects.get(name=user_name)
    return render(request, 'user.html', {'user': user_})


def view_recipe(request, user_name, recipe_url_name):
    user_ = User.objects.get(name=user_name)
    recipe_ = get_object_or_404(Recipe, url_name=recipe_url_name, user=user_)
    ingredients = recipe_.ingredients.split('\n')
    directions = recipe_.directions.split('\n')
    return render(request, 'recipe.html', {'user_name': user_name,
                                           'recipe': recipe_,
                                           'ingredients': ingredients,
                                           'directions': directions})


def edit_recipe(request, user_name, recipe_url_name):
    user_ = User.objects.get(name=user_name)
    recipe = get_object_or_404(Recipe, url_name=recipe_url_name, user=user_)
    if request.method == 'POST':
        recipe.title = request.POST.get('title', '')
        recipe.ingredients = request.POST.get('ingredients', '')
        recipe.directions = request.POST.get('directions', '')
        recipe.servings = request.POST.get('servings', '')
        recipe.source = request.POST.get('source', '')
        recipe.source_url = request.POST.get('source_url', '')
        recipe.img_url = request.POST.get('img_url', '')
        recipe.cooking_time = request.POST.get('cooking_time', '')
        recipe.total_time = request.POST.get('total_time', '')
        recipe.notes = request.POST.get('notes', '')
        recipe.save()
        return redirect('/users/%s/recipe/%s' % (user_.name, recipe.url_name))
    form = RecipeForm(instance=recipe)
    return render(request, 'edit.html', {'user_name': user_name,
                                         'form': form})


def export(request, username):
    logging.info('received request to export %s' % username)
    zipdir = os.path.join('/tmp', username, 'recipes')
    try:
        os.makedirs(zipdir)
        logging.debug('made directory %s' % zipdir)
        user_ = User.objects.get(name=username)
        for recipe in user_.recipe_set.all():
            filename = os.path.join(zipdir, recipe.url_name)
            with open(filename, 'wt', encoding='utf-8') as f:
                logging.debug('writing %s to %s' % (recipe.title, filename))
                f.write(recipe.title)
                f.write('\n\nIngredients:\n')
                f.write(recipe.ingredients)
                f.write('\n\nDirections:\n')
                f.write(recipe.directions)
                if recipe.servings:
                    f.write('\n\nServings:\n')
                    f.write(recipe.servings)
                if recipe.source:
                    f.write('\n\nSource:\n')
                    f.write(recipe.source)
                if recipe.source_url:
                    f.write('\n\nSource URL:\n')
                    f.write(recipe.source_url)
                if recipe.img_url:
                    f.write('\n\nImage URL:\n')
                    f.write(recipe.img_url)
                if recipe.cooking_time:
                    f.write('\n\nCooking Time:\n')
                    f.write(recipe.cooking_time)
                if recipe.total_time:
                    f.write('\n\nTotal Time:\n')
                    f.write(recipe.total_time)
                if recipe.notes:
                    f.write('\n\nNotes:\n')
                    f.write(recipe.notes)
        shutil.make_archive('recipes', 'zip', os.path.join('/tmp', username), 'recipes')
        shutil.rmtree(zipdir)
        filename = 'recipes.zip'
        wrapper = FileWrapper(open(filename, 'rb'))
        response = HttpResponse(wrapper, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=recipes.zip'
        response['Content-Length'] = os.path.getsize(filename)
        os.remove(filename)
        logging.debug('removing %s' % filename)
    except:
        logging.exception('failed to export')
        shutil.rmtree(zipdir)
        response = None
    return response
