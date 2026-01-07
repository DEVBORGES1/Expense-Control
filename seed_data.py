
import sys
import os
import datetime
import random

# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.database import db

def seed_data():
    username = "bg"
    password = "123"
    
    print(f"Checking user {username}...")
    success, user_id = db.login_user(username, password)
    
    if not success:
        print("User not found or password incorrect. Attempting to register...")
        reg_success, msg = db.register_user(username, password)
        if reg_success:
            print("User registered.")
            success, user_id = db.login_user(username, password)
        else:
            print(f"Failed to register: {msg}")
            return

    print(f"Seeding data for User ID: {user_id}")
    
    today = datetime.date.today()
    
    # 2. Add Income - High enough to level up
    incomes = [
        ("Salario", 5000.00, today.replace(day=5)),
        ("Freelance", 1200.00, today.replace(day=15)),
        ("Investimentos", 350.50, today.replace(day=20)),
    ]
    
    print("Adding Income...")
    for cat, val, date in incomes:
        db.add_income(user_id, cat, str(date), val)

    # 3. Add Expenses
    categories = db.get_categories()
    moods = ["Normal", "Ansioso 😰", "Feliz 🤩", "Triste 😢", "Entediado 😐", "Estressado 🤯"]
    
    print("Adding Expenses...")
    for i in range(15):
        cat = random.choice( categories )
        val = round(random.uniform(20.0, 300.0), 2)
        day = random.randint(1, 28)
        date = today.replace(day=day)
        mood = random.choice(moods)
        
        db.add_expense(user_id, cat, str(date), val, mood)
        
    # 4. Add Budgets
    print("Setting Budgets...")
    db.set_budget(user_id, "Comida", 800.00)
    db.set_budget(user_id, "Lazer", 400.00)
    db.set_budget(user_id, "Transporte", 300.00)
    
    # 5. Add Wishlist Items
    print("Adding Wishlist...")
    db.add_wishlist_item(user_id, "Novo Headset", 450.00, 24) 
    db.add_wishlist_item(user_id, "Viagem Fim de Ano", 2500.00, 168)
    
    print("Data seeded successfully!")

if __name__ == "__main__":
    seed_data()
