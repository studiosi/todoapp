from app import app, db
from models.List import List
from models.Item import Item


@app.cli.command("seed-database", help="Seed the database for testing purposes.")
def seed_database():
    # List with three items
    seeded_list_items = List("Example list #0")
    seeded_list_items.add_item(Item("Example content #0", 0))
    seeded_list_items.add_item(Item("Example content #1", 1))
    seeded_list_items.add_item(Item("Example content #2", 2))
    db.session.add(seeded_list_items)
    # List without items
    seeded_list_empty = List("Example list #1")
    db.session.add(seeded_list_empty)
    # Commit the changes to the database
    db.session.commit()
    print("Database seeded")
