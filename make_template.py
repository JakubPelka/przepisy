import re

with open('przepisy.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Header: Up to <div class="results-bar" id="results-bar"></div>\n</section>
part1_end = content.find('</section>', content.find('id="results-bar"')) + 10
header = content[:part1_end]

# Find where main starts
main_start = content.find('<main>')
if main_start != -1:
    header = content[:main_start]

# Find where script starts or end of file
script_start = content.find('<script>')
if script_start != -1:
    footer = content[script_start:]
else:
    # just find the end of the last section
    footer = "</div>\n</body>\n</html>"

template_content = header + """
<main>
<section class="panel hero">
<h1>Przepisy z archiwum Dieta.zip</h1>
<p class="category-meta">Liczba przepisów: <strong>{{ total_recipes }}</strong></p>
</section>
{{ recipes_html|safe }}
</main>
{{ ingredient_index_html|safe }}
""" + footer

with open('templates/base_przepisy.html', 'w', encoding='utf-8') as f:
    f.write(template_content)

print("Generated templates/base_przepisy.html")
