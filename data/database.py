
import sqlite3
import bcrypt
import os

DB_NAME = "DATA.db"

class Database:
    def __init__(self):
        self.conn = None
        self.create_tables()

    def connect(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn

    def create_tables(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            
            # Users Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')

            # Categories Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL
                )
            ''')
            
            # Income Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Income (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    categoria TEXT,
                    adicionado_em DATE,
                    valor DECIMAL,
                    FOREIGN KEY(user_id) REFERENCES Users(id)
                )
            ''')

            # Expenses Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    categoria TEXT,
                    retirado_em DATE,
                    valor DECIMAL,
                    FOREIGN KEY(user_id) REFERENCES Users(id)
                )
            ''')
            
            # Budgets Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    categoria TEXT,
                    limit_value DECIMAL,
                    FOREIGN KEY(user_id) REFERENCES Users(id),
                    UNIQUE(user_id, categoria)
                )
            ''')

            # Wishlist Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Wishlist (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT,
                    value DECIMAL,
                    added_at DATETIME,
                    cooldown_end DATETIME,
                    status TEXT, -- 'LOCKED', 'AVAILABLE', 'PURCHASED', 'CANCELLED'
                    FOREIGN KEY(user_id) REFERENCES Users(id)
                )
            ''')
            
            # Initial Categories if empty
            cursor.execute("SELECT count(*) FROM Categories")
            if cursor.fetchone()[0] == 0:
                categories = ['Salario', 'Freelance', 'Investimentos', 'Aluguel', 'Comida', 'Transporte', 'Lazer', 'Outros']
                for cat in categories:
                    cursor.execute("INSERT INTO Categories (nome) VALUES (?)", (cat,))
            
            conn.commit()
            
        self.check_and_migrate()

    def check_and_migrate(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            
            # Check Income
            cursor.execute("PRAGMA table_info(Income)")
            columns = [info[1] for info in cursor.fetchall()]
            if 'user_id' not in columns:
                cursor.execute("ALTER TABLE Income ADD COLUMN user_id INTEGER REFERENCES Users(id)")
                # Assign existing records to a default user (orphaned) or NULL
                print("Migrated Income table")

            # Check Expenses
            cursor.execute("PRAGMA table_info(Expenses)")
            columns = [info[1] for info in cursor.fetchall()]
            if 'user_id' not in columns:
                cursor.execute("ALTER TABLE Expenses ADD COLUMN user_id INTEGER REFERENCES Users(id)")
                print("Migrated Expenses table")
            
            # Check Budgets (New Table check)
            cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Budgets'")
            if cursor.fetchone()[0] == 0:
                print("Creating Budgets table...")
                cursor.execute('''
                    CREATE TABLE Budgets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        categoria TEXT,
                        limit_value DECIMAL,
                        FOREIGN KEY(user_id) REFERENCES Users(id),
                        UNIQUE(user_id, categoria)
                    )
                ''')

            # Check Wishlist
            cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Wishlist'")
            if cursor.fetchone()[0] == 0:
                print("Creating Wishlist table...")
                cursor.execute('''
                    CREATE TABLE Wishlist (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        name TEXT,
                        value DECIMAL,
                        added_at DATETIME,
                        cooldown_end DATETIME,
                        status TEXT,
                        FOREIGN KEY(user_id) REFERENCES Users(id)
                    )
                ''')

            # Check Mood Column in Expenses
            cursor.execute("PRAGMA table_info(Expenses)")
            columns = [info[1] for info in cursor.fetchall()]
            if 'mood' not in columns:
                cursor.execute("ALTER TABLE Expenses ADD COLUMN mood TEXT")
                print("Migrated Expenses table (Added mood)")
                
            conn.commit()

    # User Auth
    def register_user(self, username, password):
        try:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, hashed))
                conn.commit()
                return True, "User registered successfully"
        except sqlite3.IntegrityError:
            return False, "Username already exists"
        except Exception as e:
            return False, str(e)

    def login_user(self, username, password):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, password FROM Users WHERE username=?", (username,))
            user = cursor.fetchone()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user[1]):
                return True, user[0] # Returns user_id
            return False, None

    # Categories
    def get_categories(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM Categories")
            return [row[0] for row in cursor.fetchall()]

    def add_category(self, name):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Categories (nome) VALUES (?)", (name,))
            conn.commit()

    # Transactions (Unified Interface)
    def add_income(self, user_id, category, date, amount):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Income (user_id, categoria, adicionado_em, valor) VALUES (?, ?, ?, ?)", 
                           (user_id, category, date, amount))
            conn.commit()

    def add_expense(self, user_id, category, date, amount, mood=None):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Expenses (user_id, categoria, retirado_em, valor, mood) VALUES (?, ?, ?, ?, ?)", 
                           (user_id, category, date, amount, mood))
            conn.commit()

    def update_transaction(self, trans_id, trans_type, category, date, amount):
        table = "Income" if trans_type == "Receita" else "Expenses"
        date_col = "adicionado_em" if trans_type == "Receita" else "retirado_em"
        
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {table} SET categoria=?, {date_col}=?, valor=? WHERE id=?", 
                           (category, date, amount, trans_id))
            conn.commit()

    def get_user_balance_filtered(self, user_id, month=None, year=None):
        with self.connect() as conn:
            cursor = conn.cursor()
            
            date_filter = ""
            params = [user_id]
            
            if month and year:
                # SQLite strftime format: %Y-%m
                date_str = f"{year}-{month}"
                date_filter = f"AND strftime('%Y-%m', date_col) = ?"
                params.append(date_str)
            
            # Total Income
            cursor.execute(f"SELECT SUM(valor) FROM Income WHERE user_id=? {date_filter.replace('date_col', 'adicionado_em')}", params)
            income = cursor.fetchone()[0] or 0.0
            
            # Total Expenses
            cursor.execute(f"SELECT SUM(valor) FROM Expenses WHERE user_id=? {date_filter.replace('date_col', 'retirado_em')}", params)
            expenses = cursor.fetchone()[0] or 0.0
            
            return income, expenses, (income - expenses)

    def get_transactions_filtered(self, user_id, month=None, year=None):
        with self.connect() as conn:
            cursor = conn.cursor()
            
            filter_inc = ""
            filter_exp = ""
            params_inc = [user_id]
            params_exp = [user_id]
            
            if month and year:
                date_str = f"{year}-{month}"
                filter_inc = "AND strftime('%Y-%m', adicionado_em) = ?"
                filter_exp = "AND strftime('%Y-%m', retirado_em) = ?"
                params_inc.append(date_str)
                params_exp.append(date_str)

            query = f'''
                SELECT id, 'Receita' as tipo, categoria, adicionado_em as data, valor FROM Income WHERE user_id=? {filter_inc}
                UNION ALL
                SELECT id, 'Despesa' as tipo, categoria, retirado_em as data, valor FROM Expenses WHERE user_id=? {filter_exp}
                ORDER BY data DESC
            '''
            # Flatten params: [user_id, date, user_id, date]
            cursor.execute(query, params_inc + params_exp)
            return cursor.fetchall()

    def delete_transaction(self, trans_id, trans_type):
        table = "Income" if trans_type == "Receita" else "Expenses"
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table} WHERE id=?", (trans_id,))
            conn.commit()

    # Budget Logic
    def set_budget(self, user_id, category, value):
        with self.connect() as conn:
            cursor = conn.cursor()
            # UPSERT logic (Insert or Replace)
            cursor.execute("INSERT OR REPLACE INTO Budgets (user_id, categoria, limit_value) VALUES (?, ?, ?)", 
                           (user_id, category, value))
            conn.commit()
            
    def get_budgets(self, user_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT categoria, limit_value FROM Budgets WHERE user_id=?", (user_id,))
            return {row[0]: row[1] for row in cursor.fetchall()}

    def get_category_spending(self, user_id, month, year):
        # Get total spending per category for specific month
        with self.connect() as conn:
            cursor = conn.cursor()
            date_str = f"{year}-{month}"
            cursor.execute('''
                SELECT categoria, SUM(valor) FROM Expenses 
                WHERE user_id=? AND strftime('%Y-%m', retirado_em) = ?
                GROUP BY categoria
            ''', (user_id, date_str))
            return {row[0]: row[1] for row in cursor.fetchall()}

    # Wishlist Logic
    def add_wishlist_item(self, user_id, name, value, duration_hours):
        import datetime
        now = datetime.datetime.now()
        cooldown = now + datetime.timedelta(hours=duration_hours)
        
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Wishlist (user_id, name, value, added_at, cooldown_end, status) VALUES (?, ?, ?, ?, ?, ?)", 
                           (user_id, name, value, now, cooldown, 'LOCKED'))
            conn.commit()

    def get_wishlist(self, user_id):
        import datetime
        now = datetime.datetime.now()
        
        with self.connect() as conn:
            cursor = conn.cursor()
            
            # Auto-update status if cooldown passed
            cursor.execute("UPDATE Wishlist SET status='AVAILABLE' WHERE user_id=? AND status='LOCKED' AND cooldown_end <= ?", (user_id, now))
            conn.commit()
            
            cursor.execute("SELECT id, name, value, cooldown_end, status FROM Wishlist WHERE user_id=? AND status IN ('LOCKED', 'AVAILABLE') ORDER BY cooldown_end", (user_id,))
            return cursor.fetchall()

    def update_wishlist_status(self, item_id, status):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE Wishlist SET status=? WHERE id=?", (status, item_id))
            conn.commit()

db = Database()
