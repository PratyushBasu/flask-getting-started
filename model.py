import json

# Load data from file
def load_db():
    with open('flashcards_db.json') as f:
        return json.load(f)

# Write data to file
def save_db():
    with open('flashcards_db.json', 'w') as f:
        return json.dump(db, f)

db = load_db()