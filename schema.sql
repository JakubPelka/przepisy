CREATE TABLE IF NOT EXISTS recipes (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    ingredients_search TEXT,
    search_text TEXT,
    kcal REAL,
    protein REAL,
    carbs REAL,
    fat REAL,
    ingredients_html TEXT,
    instructions_html TEXT,
    source_variant TEXT
);
