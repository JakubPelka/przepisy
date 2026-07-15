from flask import Flask, render_template, request, redirect, url_for, flash
import database
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_local_app'

@app.route('/')
def index():
    recipes = database.get_all_recipes()
    return render_template('admin.html', recipes=recipes)

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            database.insert_recipe(data)
            flash('Przepis dodany pomyślnie!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Błąd dodawania: {e}', 'danger')
    return render_template('form.html', recipe=None)

@app.route('/edit/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            database.update_recipe(recipe_id, data)
            flash('Przepis zaktualizowany!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Błąd aktualizacji: {e}', 'danger')
    
    recipe = database.get_recipe_by_id(recipe_id)
    if not recipe:
        flash('Nie znaleziono przepisu', 'danger')
        return redirect(url_for('index'))
    return render_template('form.html', recipe=recipe)

@app.route('/delete/<recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    try:
        database.delete_recipe(recipe_id)
        flash('Przepis usunięty!', 'success')
    except Exception as e:
        flash(f'Błąd usuwania: {e}', 'danger')
    return redirect(url_for('index'))

def build_static_html():
    recipes = database.get_all_recipes()
    
    # 1. Generate Sidebar & TOC
    sidebar_content = ""
    categories = {}
    for r in recipes:
        if r['category'] not in categories:
            categories[r['category']] = []
        categories[r['category']].append(r)
        
    sidebar_content += '<section class="panel sidebar-card search-wrap">\n'
    sidebar_content += '<label for="recipe-search"><strong>Szukaj przepisu</strong></label>\n'
    sidebar_content += '<input autocomplete="off" id="recipe-search" placeholder="Wpisz nazwę, składnik lub frazę..." type="search"/>\n'
    sidebar_content += '<div class="filters-inline"><label for="ingredient-search"><strong>Filtr po składnikach</strong></label><input autocomplete="off" id="ingredient-search" placeholder="np. seler, jajka, pomidor" type="search"/></div><p class="search-help">Pierwsze pole szuka po nazwie i treści. Drugie filtruje po składnikach; kilka składników rozdziel przecinkami.</p>\n'
    sidebar_content += '<div class="results-bar" id="results-bar"></div>\n'
    sidebar_content += '</section>\n'
    
    sidebar_content += '<section class="panel sidebar-card quick-links" id="spis-tresci">\n'
    sidebar_content += '<h2>Spis treści</h2>\n<ul>\n'
    # Sort categories to standard order
    order = ['Śniadanie', 'Lunch', 'Obiad', 'Przekąski']
    cat_keys = sorted(categories.keys(), key=lambda x: order.index(x) if x in order else 99)
    for cat in cat_keys:
        sidebar_content += f'<li><a href="#{cat.lower()}">{cat} <span>{len(categories[cat])}</span></a></li>'
    sidebar_content += '<li><a href="#skorowidz-skladnikow">Skorowidz składników <span>A–Z</span></a></li></ul>\n</section>\n'

    sidebar_content += '<section class="panel sidebar-card">\n<h2>Przepisy w sekcjach</h2>\n'
    for cat in cat_keys:
        sidebar_content += f'<details class="toc-group">\n<summary><a href="#{cat.lower()}">{cat} ({len(categories[cat])})</a></summary>\n<ul>\n'
        for r in categories[cat]:
            sidebar_content += f'<li><a href="#{r["id"]}">{r["title"]}</a></li>\n'
        sidebar_content += '</ul>\n</details>'
    sidebar_content += '</section>\n'

    # 2. Generate Recipes HTML
    recipes_html = ""
    for r in recipes:
        recipes_html += f'<article class="recipe" data-category="{r["category"]}" data-ingredients="{r["ingredients_search"]}" data-kcal="{r["kcal"]}" data-search="{r["search_text"]}" id="{r["id"]}">\n'
        recipes_html += f'<h3>{r["title"]}</h3>\n'
        if r['source_variant']:
            recipes_html += f'<p><em>{r["source_variant"]}</em></p>\n'
        
        recipes_html += '<section class="nutrition"><p class="nutrition-title">Wartości odżywcze — cała porcja</p><div class="nutrition-grid">'
        recipes_html += f'<div class="nutrition-item"><span class="nutrition-label">Energia</span><span class="nutrition-value">{r["kcal"]} kcal</span></div>'
        recipes_html += f'<div class="nutrition-item"><span class="nutrition-label">Białko</span><span class="nutrition-value">{r["protein"]} g</span></div>'
        recipes_html += f'<div class="nutrition-item"><span class="nutrition-label">Węglowodany</span><span class="nutrition-value">{r["carbs"]} g</span></div>'
        recipes_html += f'<div class="nutrition-item"><span class="nutrition-label">Tłuszcz</span><span class="nutrition-value">{r["fat"]} g</span></div>'
        recipes_html += '</div></section>'
        
        recipes_html += '<p><strong>Składniki</strong></p>\n'
        recipes_html += r['ingredients_html'] + '\n'
        recipes_html += '<p><strong>Przygotowanie</strong></p>\n'
        recipes_html += r['instructions_html'] + '\n'
        recipes_html += '<a class="back-top" href="#spis-tresci">Powrót do spisu treści</a>\n</article>'

    # 3. Generate Ingredients Index
    ingredients_dict = {}
    for r in recipes:
        ing_list = r['ingredients_search'].split('|')
        for ing in ing_list:
            ing = ing.strip()
            if not ing: continue
            if ing not in ingredients_dict:
                ingredients_dict[ing] = []
            ingredients_dict[ing].append(r)
            
    # Group by first letter
    from collections import defaultdict
    letter_groups = defaultdict(list)
    for ing, r_list in ingredients_dict.items():
        first_letter = ing[0].upper()
        letter_groups[first_letter].append((ing, r_list))
        
    for letter in letter_groups:
        letter_groups[letter].sort(key=lambda x: x[0].lower())
        
    sorted_letters = sorted(letter_groups.keys())
    
    ingredient_index_html = '<section class="panel ingredient-index-wrap" id="skorowidz-skladnikow"><h2>Skorowidz składników</h2><p>Kliknij literę albo przewiń niżej. Każdy składnik prowadzi do listy przepisów, w których występuje.</p>'
    ingredient_index_html += '<div class="letter-nav">'
    for letter in sorted_letters:
        ingredient_index_html += f'<a href="#skladniki-{letter.lower()}">{letter}</a>'
    ingredient_index_html += '</div>'
    
    for letter in sorted_letters:
        count = sum(len(x[1]) for x in letter_groups[letter])
        ingredient_index_html += f'<details class="ingredient-group" id="skladniki-{letter.lower()}"><summary>{letter} ({len(letter_groups[letter])})</summary><ul class="ingredient-list">'
        for ing, r_list in letter_groups[letter]:
            ing_id = "skladnik-" + ing.lower().replace(' ', '-').replace(',', '').replace('.', '')
            ingredient_index_html += f'<li><span class="ingredient-name" id="{ing_id}">{ing}</span><span class="ingredient-count"> ({len(r_list)})</span><div class="ingredient-recipes">'
            links = []
            for r in r_list:
                links.append(f'<a href="#{r["id"]}">{r["title"]}</a>')
            ingredient_index_html += ", ".join(links)
            ingredient_index_html += '</div></li>'
        ingredient_index_html += '</ul></details>'
    ingredient_index_html += '</section>'

    # Render template
    with app.app_context():
        final_html = render_template('base_przepisy.html', 
                                     sidebar_content=sidebar_content, 
                                     total_recipes=len(recipes), 
                                     recipes_html=recipes_html,
                                     ingredient_index_html=ingredient_index_html)
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(final_html)

@app.route('/export', methods=['POST'])
def export_html():
    try:
        build_static_html()
        flash('Wyeksportowano do index.html!', 'success')
    except Exception as e:
        flash(f'Błąd eksportu: {e}', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
