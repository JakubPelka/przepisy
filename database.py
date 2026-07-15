import sqlite3

DATABASE = 'recipes.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_recipes():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM recipes ORDER BY title')
    recipes = cursor.fetchall()
    db.close()
    return recipes

def get_recipe_by_id(recipe_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,))
    recipe = cursor.fetchone()
    db.close()
    return recipe

def insert_recipe(data):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO recipes (id, title, category, ingredients_search, search_text, kcal, protein, carbs, fat, ingredients_html, instructions_html, source_variant)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['id'], data['title'], data['category'], data['ingredients_search'], data['search_text'], 
          data['kcal'], data['protein'], data['carbs'], data['fat'], 
          data['ingredients_html'], data['instructions_html'], data['source_variant']))
    db.commit()
    db.close()

def update_recipe(recipe_id, data):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        UPDATE recipes SET 
            title = ?, category = ?, ingredients_search = ?, search_text = ?, 
            kcal = ?, protein = ?, carbs = ?, fat = ?, 
            ingredients_html = ?, instructions_html = ?, source_variant = ?,
            id = ?
        WHERE id = ?
    ''', (data['title'], data['category'], data['ingredients_search'], data['search_text'], 
          data['kcal'], data['protein'], data['carbs'], data['fat'], 
          data['ingredients_html'], data['instructions_html'], data['source_variant'], 
          data['id'], recipe_id))
    db.commit()
    db.close()

def delete_recipe(recipe_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
    db.commit()
    db.close()
