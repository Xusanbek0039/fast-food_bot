import sqlite3

from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from utils import build_inline_menu

# ReplyKeyboardMarkup - knopkala uchun karobka ochamiza va karobkani ichida royhat ochvolamiza
def generate_main_menu():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text='Make order ✅')],
        [KeyboardButton(text='History of orders 📜'), KeyboardButton(text='Cart 🛒')],
        [KeyboardButton(text='Help 🆘'), KeyboardButton(text='About us 🔤')],
        [KeyboardButton(text='Send Contact', request_contact=True)],
        [KeyboardButton(text='Send Location', request_location=True)]
    ], resize_keyboard=True)
    # resize_keyboard - text ga qarab knopkamizani kotta kichikligi ozgaradi digani



#Bu funksiyamiza Kategoriyalani menusini generatsiya qilib berish kere
def generate_category_menu():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='All menu', url='https://telegra.ph/Menu-FAST-FOOD-RESTAURANT-12-15')
    )

    # Kategoriyalarimizani malumotlar bazasidan qabul qilib olishimiza kere va kategoriyalarimizani qabul qilish uchun malumotlar bazasiga ulanishimiza kere
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT category_id, category_name FROM categories;
    ''')
    categories = cursor.fetchall()
    database.close()
    build_inline_menu(markup, categories, 'category')
    return markup


# Productlarimizani chiqarib beradigon funksiya
def generate_products_menu(category_id: int):
    markup = InlineKeyboardMarkup()
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_id, product_name FROM products WHERE category_id = ?;  
    ''', (category_id, ))
    products = cursor.fetchall()
    database.close()
    build_inline_menu(markup, products, 'product')
    return markup


def generate_product_detail_menu(product_id: int, category_id: int):
    markup = InlineKeyboardMarkup()
    number_list = [i for i in range(1, 9 + 1)]

    in_row = 3
    rows = len(number_list) // in_row
    if len(number_list) % in_row != 0:
        rows += 1

    start = 0
    end = in_row

    for i in range(rows):
        new_lst = []
        for number in number_list[start:end]:
            new_lst.append(
                InlineKeyboardButton(text=str(number), callback_data=f'cart_{product_id}_{number}')
            )
        markup.row(*new_lst)
        start = end
        end += in_row
    markup.row(
        InlineKeyboardButton(text='Back', callback_data=f'back_{category_id}')
    )

    return markup


# Karzinkani tegida chiqadigon knopkalani generatsiyasi  uchun  funksiya ochamiza
def generate_cart_menu(cart_id: int):
    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton(text='Checkout 🚀', callback_data=f'order_{cart_id}')
    )

    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()

    cursor.execute('''
    SELECT cart_product_id, product_name
    FROM cart_products
    WHERE cart_id = ?
    ''', (cart_id, ))

    cart_products = cursor.fetchall()
    database.close()

    for product_id, product_name in cart_products:
        markup.row(
            InlineKeyboardButton(text=f'❌ {product_name}', callback_data=f'delete_{product_id}')
        )
    return markup