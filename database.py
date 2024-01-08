# Bu faylda botimizani malumotlar bazasini shakillantiramiza
# Biza malumotlar bazasini script da yaratmimiza, malumotlar bazasini funksiyalada yaratamiza bugalgisida
# Funksiyala qaysidur jadvalni yaratishi uchun javob beradi

import sqlite3

database = sqlite3.connect('fastfood.db')
cursor = database.cursor()

# Har bir foydalanuvchini telegram_id boladi va Kanalga ulanganini telegram_id orqali tekshiriladi
def create_users_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name VARCHAR(50) NOT NULL,
        telegram_id INTEGER NOT NULL UNIQUE
    )
    ''')

# Kategoriyalarimizani saqlash uchun alohida bitta jadval yaratamiza
def create_categories():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name VARCHAR(20) NOT NULL UNIQUE
        
    )''')

# Product qaysi categoriyaga tegishli bolishi kere va Product qaysi categoriyaga tegishliligini category_id INTEGER NOT NULL orqali taminlab beramiza
# Kategoriyalarimizda saqlanvotgan mahsulotlarimiza uchun jadval
# DECIMAL - malumotlar turi bu float malumotlar turi digani yani verguli son vergulgacha 12 ta son, verguldan keyin 2 ta son shunaka agranicheniye berse boladi
def create_products_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products(
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        product_name VARCHAR(20) NOT NULL UNIQUE,
        price DECIMAL(12, 2) NOT NULL,
        ingredients VARCHAR(50),
        image TEXT,
        FOREIGN KEY(category_id) REFERENCES categories(category_id)
        
    )''')
# products jadvalini  categories ga ulab qoyishimiza kere

# user_id - ushbu karzinka foydalanuvchiga tegishli bolishi uchun
# Karzinka uchun alohida jadval yaratamiza zakaz jarayonida shakilanadigon jadval boladi
def create_cart_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carts(
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(user_id) UNIQUE,
        total_products INTEGER DEFAULT 0,
        total_price DECIMAL(12, 2) DEFAULT 0
    )''')


# Karzinkani ichidigi saqlanvotgan productlarimiz uchun jadval yaratamiza
def create_cart_products_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart_products(
        cart_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER REFERENCES carts(cart_id),
        product_name VARCHAR(20) NOT NULL,
        quantity INTEGER NOT NULL,
        final_price DECIMAL(12, 2) NOT NULL,

        UNIQUE(cart_id, product_name)
    )''')


# Buyurtma uchun jadval boladi , time_create buyurtmani ochilgan vaqti
def create_orders_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders(
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(user_id) UNIQUE,
        time_create DATETIME,
        total_products INTEGER DEFAULT 0
    )''')


# Bu jadval Buyurtmani ichidigi  mahsulotla uchun jadval boladi
def create_order_products_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_products(
        order_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER REFERENCES orders(order_id),
        product_name VARCHAR(20) NOT NULL,
        final_price DECIMAL(12, 2) NOT NULL,

        UNIQUE(order_id, product_name)
        )''')

# Malumotlar bazasi yaratilinishi uchun bu funksiyala ishga tushishi kere
# create_users_table()
# create_cart_table()
# create_cart_products_table()
# create_categories()
# create_products_table()
# create_orders_table()
# create_order_products_table()

def insert_categories():
    cursor.execute('''
    INSERT INTO categories(category_name) VALUES
    ('LAVASH'),('DONAR'),('BURGER'),('HOT-DOG'),('DESSERT'),('DRINKS'),('SAUCE')
    ''')

# insert_categories()


# Malumotlar bazasiga malumot qoshishimiza kere yani productla
def insert_products():
    cursor.execute('''
    INSERT INTO products(category_id, product_name, price, ingredients, image) VALUES
    (1, 'Mini Lavash Beef', 20000, 'Meat Beaf, Lavash, Tomato, Cucumber, Chips, Tomato Sauce, Mayonnaise', 'media/Mini Lavash Beef.jpg'),
    (1, 'Mini Lavash Chicken', 18000, 'Meat Chicken, Lavash, Tomato, Cucumber, Chips, Tomato Sauce, Mayonnaise', 'media/Mini Lavash Chicken.jpg'),
    (1, 'Lavash Beef', 25000, 'Meat Beaf, Lavash, Tomato, Cucumber, Chips, Tomato Sauce, Mayonnaise', 'media/Lavash Beef.png'),
    (1, 'Lavash Chicken', 23000, 'Meat Chicken, Lavash, Tomato, Cucumber, Chips, Tomato Sauce, Mayonnaise', 'media/Lavash Chicken.png'),
    (1, 'Lavash Beef Cheese', 27000, 'Meat Beaf, Lavash, Tomato, Cucumber, Chips, Tomato Sauce, Mayonnaise, Cheese', 'media/Lavash Beef Cheese.png'),
    (1, 'Lavash Chicken Cheese', 20000, 'Meat Chicken, Lavash, Tomato, Cucumber, Chips, Tomato Sauce, Mayonnaise', 'media/Lavash Chicken Cheese.png')
    ''')

# insert_products()


database.commit()
database.close()
