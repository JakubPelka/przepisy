import sqlite3
import os
from bs4 import BeautifulSoup
import re

def extract_recipes():
    print("Reading przepisy.html...")
    with open('przepisy.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    recipes = soup.find_all('article', class_='recipe')
    print(f"Found {len(recipes)} recipes.")

    # Connect to db and create table
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    
    with open('schema.sql', 'r', encoding='utf-8') as schema_file:
        cursor.executescript(schema_file.read())

    for recipe in recipes:
        recipe_id = recipe.get('id', '')
        category = recipe.get('data-category', '')
        ingredients_search = recipe.get('data-ingredients', '')
        kcal_str = recipe.get('data-kcal', '0')
        search_text = recipe.get('data-search', '')

        try:
            kcal = float(kcal_str)
        except ValueError:
            kcal = 0.0

        title_tag = recipe.find('h3')
        title = title_tag.text.strip() if title_tag else "Brak tytułu"
        
        # Source variant (e.g. "Zachowany 1 wariant...")
        variant_tag = recipe.find('p', text=re.compile(r'Zachowany.*wariant'))
        source_variant = variant_tag.text.strip() if variant_tag else ""

        # Extract nutrition data from the grid
        protein = 0.0
        carbs = 0.0
        fat = 0.0
        nutrition_section = recipe.find('section', class_='nutrition')
        if nutrition_section:
            items = nutrition_section.find_all('div', class_='nutrition-item')
            for item in items:
                label = item.find('span', class_='nutrition-label').text.lower()
                value = item.find('span', class_='nutrition-value').text
                
                try:
                    num_val = float(value.replace('g', '').strip())
                    if 'białko' in label:
                        protein = num_val
                    elif 'węglowodany' in label:
                        carbs = num_val
                    elif 'tłuszcz' in label:
                        fat = num_val
                except Exception:
                    pass

        # Ingredients HTML
        ingredients_html = ""
        # The ingredients usually follow a <p><strong>Składniki</strong></p> and is a <ul>
        ul_tag = recipe.find('ul')
        if ul_tag:
            ingredients_html = str(ul_tag)
            
        # Instructions HTML
        instructions_html = ""
        # The instructions usually follow a <p><strong>Przygotowanie</strong></p> and is an <ol>
        ol_tag = recipe.find('ol')
        if ol_tag:
            instructions_html = str(ol_tag)

        # Insert into DB
        cursor.execute('''
            INSERT OR REPLACE INTO recipes 
            (id, title, category, ingredients_search, search_text, kcal, protein, carbs, fat, ingredients_html, instructions_html, source_variant)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (recipe_id, title, category, ingredients_search, search_text, kcal, protein, carbs, fat, ingredients_html, instructions_html, source_variant))

    conn.commit()
    conn.close()
    print("Extraction completed and saved to recipes.db.")

if __name__ == "__main__":
    extract_recipes()
