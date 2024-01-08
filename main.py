from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery, LabeledPrice
import os
import sqlite3
from keyboards import *



# Dispatcher - bot da eshitib turadigon yani bot da qilinvotgan ishlani kuzatib turuvchi yani dispecher
# executor - bot ni ishga tushuruvchi vosita hiusoblanadi
# Bot - bot ni elon qilish uchun kere boladi

"""
Malumot turlari python 1)integer 2) float 3)list 4) tuple 5)string 6)dictionary 7) set 8)boolean
"""

TOKEN = '6849473588:AAEEt5wy0Mq3Dja3yJ--GXzRcavWqoev7_A'
bot = Bot(TOKEN, parse_mode='HTML')

dp = Dispatcher(bot)  # botimizaga biita dispecher tayillab qoyamiza buni esa Dispatcher orqali tayillimiza


# Start kamandasini ushlab olishimiza kere buning uchun dispecherga murojat qilamiza  / # Meesage obyektidan olingan sms boladi
@dp.message_handler(commands=['start'])
async def start(message: Message):  # Meesage obyektidan olingan sms boladi
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Bu yetkazib berish boti !!!')
    await register_user(message)
    await show_main_menu(message)


@dp.message_handler(commands=['start'])
async def start(message: Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'This is test bot of delivery !!!')
    await register_user(message)
    await show_main_menu(message)




'''
await режим считается

Как работает await async?
Async await позволяет писать асинхронный код, так как будто он является синхронным. 
Для использования async await нужно указать, что наша функция будет содержать асинхронный код, путем добавления слова async. 
Далее, внутри функции нужно отметить словом await  те строчки, в которых содержится асинхронный код.
'''

# Foydalanuvchilarni registratsiya qilamiza
async def register_user(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name

    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()


    try:
        cursor.execute('''
        INSERT INTO users (full_name, telegram_id) VALUES (?, ?)
        ''', (full_name, chat_id))
        database.commit()  # Kortej korinishida bervomiza
        await bot.send_message(chat_id, "Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!!!")
    except:  # Foydalanuvchi bizani malumotlar bazamizaga oldin kirgan bosa
        await bot.send_message(chat_id, f"Avtorizatsiya muvaffaqiyatli bo'ldi!!!")
    database.close()
    await create_cart(message)

#Foydalanuvchi uchun alohida karzinka yaratilinishi
async def create_cart(message: Message):    # 1 chi message - bu foydalanuvchidam keladigon message, 2 chi Message biza kutvotgan malumotlar turi bu 2 chi Message boladi
    chat_id = message.chat.id
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    try:
        cursor.execute('''
        INSERT INTO carts(user_id) VALUES
        (
        (SELECT user_id FROM users WHERE telegram_id = ?)
        )
        
        ''', (chat_id,))   # ? orniga Kortej korinishida malumot bervorishimiza kere bu malumot chat_id
        database.commit()
    except:
        pass
    database.close()
# telegram_id - orqali malumot qoshamiza va telegram_id chat_id ga teglashadi

# Kategoriyalani ichidigi productlani korish uchun funksiya
@dp.callback_query_handler(lambda call: 'category' in call.data)   # call bu yerda argument sifatida
async def show_products(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, category_id = call.data.split('_')    # _  dasturlashda keremas hisoblanadi yani keremas ozgaruvchi agarda nijniy defis bilan nomlangan bosa
    category_id = int(category_id)
    await bot.edit_message_text('Please choose product: ', chat_id, message_id,
                                reply_markup=generate_products_menu(category_id))

    # edit_message_reply_markup - redaktirovaniye yani markup ni tahrirlash ozgartirish kiritish digani

# Mahsulot button ni bosilganda shu mahsulot haqida malumot chiqarib berish jarayoni
@dp.callback_query_handler(lambda call: 'product' in call.data)
async def show_detail_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    _, product_id = call.data.split('_')
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()

    cursor.execute('''
    SELECT product_id, product_name, price, ingredients, category_id, image
    FROM products
    WHERE product_id = ?;
    ''', (product_id,))

    product = cursor.fetchone()
    print(product)
    database.close()

    await bot.delete_message(chat_id, message_id)  # Bot jonatgan message ni ochirib tashimiza chat_id dan
    with open(product[5], mode='rb') as img:
        await bot.send_photo(chat_id,
                             photo=img,
                             caption=f'''<strong>{product[1]}</strong>
<strong>Ingredients: </strong> {product[3]}
<strong>Price: </strong> {product[2]}
    ''', reply_markup=generate_product_detail_menu(product_id=product_id, category_id=product[4]))

# Kolichestvo product dobavlenniy v karzinku uchun funksiya
@dp.callback_query_handler(lambda call: call.data.startswith('cart'))
async def add_product_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, product_id, quantity = call.data.split('_')   # 3 ta ozgaruvchiga saxranit qivoldik , 1 chi - card sozi 2 chi product_id 3 chiproductlani soni

    product_id, quantity = int(product_id), int(quantity)

    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()

    cursor.execute('''
    SELECT cart_id FROM carts
    WHERE user_id = (SELECT user_id FROM users WHERE telegram_id = ?)
    ''', (chat_id,))
    cart_id = cursor.fetchone()[0]
    print(cart_id)
# product_name - orqali karzinkaga qoshamiza, price orqali obshiy summani chiqarvolamiza
    cursor.execute('''
    SELECT product_name, price FROM products
    WHERE product_id = ?;
    ''', (product_id,))

    product_name, price = cursor.fetchone()   # Ozlashtirib ketvomiza product_name=product_name ga, price=price ga

    final_price = quantity * price

    try:
        cursor.execute('''
        INSERT INTO cart_products(cart_id, product_name, quantity, final_price)
        VALUES (?,?,?,?)
        ''', (cart_id, product_name, quantity, final_price))
        database.commit()
        await bot.answer_callback_query(call.id, text='Product added successfully !')
    except:
        cursor.execute('''
        UPDATE cart_products
        SET quantity = ?,
        final_price = ?
        WHERE product_name = ? AND cart_id = ?
        ''', (quantity, final_price, product_name, cart_id))
        database.commit()
        await bot.answer_callback_query(call.id, text='Quantity changed successfully !')   # Bizaga kevotgan har bil call ni ozini id - si bor

    finally:
        database.close()


@dp.callback_query_handler(lambda call: 'back' in call.data)  # back_1 # back_2  Obrabotka qilish jarayoni dp orqali 
async def return_to_category(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, category_id = call.data.split('_')   # Kevotgan callback_data ni split qilishimiza kere
    await bot.delete_message(chat_id, message_id)

    await bot.send_message(chat_id=chat_id,
                           text='Choose the product: ',
                           reply_markup=generate_products_menu(category_id))

@dp.callback_query_handler(lambda call: 'main_menu' in call.data)
async def return_to_main_menu(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text='Choose the category: ',
                                reply_markup=generate_category_menu())


@dp.message_handler(lambda message: 'Cart 🛒' in message.text)
async def show_cart(message: Message, edit_message: bool = False):
    chat_id = message.chat.id

    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()

    # Malumotlar bazasidan Foydalanuvchiga tegishli bogan karzinkani ovolishimiza kere va Foydalanuvchini user_id orqali karzinkani cart_id ni ovolamiza
    cursor.execute('''
    SELECT cart_id FROM carts WHERE user_id = 
    (
    SELECT user_id FROM users WHERE telegram_id = ?
    )
    ''', (chat_id, ))
    cart_id = cursor.fetchone()[0]
    try:
        cursor.execute('''
        UPDATE carts
        SET total_products = (
            SELECT SUM(quantity) FROM cart_products
            WHERE cart_id = :cart_id
        ),
        total_price = (
            SELECT SUM(final_price) FROM cart_products
            WHERE cart_id = :cart_id
        )
        WHERE cart_id = :cart_id
        ''', {'cart_id': cart_id})
        database.commit()
    except:
        await bot.send_message(chat_id, f'Cart is unavailable !')
        database.close()
        return
# Cards jadvalidan total_products bilan total_price ovolishimiza kere
    cursor.execute('''
    SELECT total_products, total_price FROM carts
    WHERE user_id = 
    (
    SELECT user_id FROM users
    WHERE telegram_id = ?
    )
    ''', (chat_id, ))
    total_products, total_price = cursor.fetchone()

    cursor.execute('''
    SELECT product_name, quantity, final_price
    FROM cart_products
    WHERE cart_id = ?
    ''', (cart_id, ))
    cart_products = cursor.fetchall()

    # Foydalanuvchiga sms habar jonatish
    text = 'Your cart: \n\n'

    i = 0

    for product_name, quantity, final_price in cart_products:
        i += 1
        text += f'''{i}. {product_name}
Quantity: {quantity}
Total price: {final_price}\n\n'''
    text += f'''Total products: {0 if total_products == None else total_products}
Total price: {0 if total_price == None else total_price}'''
    if edit_message:
        await bot.edit_message_text(text, chat_id, message.message_id, reply_markup=generate_cart_menu(cart_id))
    else:
        await bot.send_message(chat_id, text, reply_markup=generate_cart_menu(cart_id))


@dp.callback_query_handler(lambda call: 'delete' in call.data)  # delete_1
async def delete_product_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    message = call.message

    _, cart_product_id = call.data.split('_')
    cart_product_id = int(cart_product_id)

    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()

    cursor.execute('''
    DELETE FROM cart_products
    WHERE cart_product_id = ?
    ''', (cart_product_id, ))
    database.commit()
    database.close()

    await bot.answer_callback_query(call.id, 'Product deleted successfull !!!')
    await show_cart(message, edit_message=True)

@dp.callback_query_handler(lambda call: 'order' in call.data)
async def create_order(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, cart_id = call.data.split('_')
    cart_id = int(cart_id)

    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()

    cursor.execute('''
        SELECT product_name, quantity, final_price
        FROM cart_products
        WHERE cart_id = ?
        ''', (cart_id,))
    cart_products = cursor.fetchall()

    cursor.execute('''
        SELECT total_products, total_price FROM carts
        WHERE user_id = 
        (
        SELECT user_id FROM users
        WHERE telegram_id = ?
        )
        ''', (chat_id,))
    total_products, total_price = cursor.fetchone()

    text = 'Your check:\n\n'
    i = 0
    for product_name, quantity, final_price in cart_products:
        i += 1
        text += f'''{i}. {product_name}
Quantity: {quantity}
Total price: {final_price}\n\n'''
    text += f'''Total products: {0 if total_products == None else total_products}
Total price of check: {0 if total_price == None else total_price}'''

# send_invoice - tolov uchun jonatilinadigon sms hisoblanadi
    if total_price is None:
        total_price = 0

    await bot.send_invoice(
        chat_id=chat_id,
        title=f'Check №{cart_id}',
        description=text,
        payload='bot-defined invoice payload',
        provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
        currency='UZS',
        prices=[
            LabeledPrice(label='Total priice', amount=int(str(total_price) + '00')),
            LabeledPrice(label='Delivery', amount=900000)
        ]
    )
    # LabeledPrice - narxlar bilan ishlash uchun ishlatilinadigon biblioteka hisoblanadi
    # Uzb da hamma trazaksiyala tin korinishida amalga oshiriladi 1 som 100 tin

    await bot.send_message(chat_id, 'Order has been paid !')



# lambda - funksiya, message - argument
@dp.message_handler(lambda message: 'Buyurtma berish ✅' in message.text)    # knopkani ichidi kevotgan habarni yani text ni ushlab ovomiza
async def make_order(message: Message):
    chat_id = message.chat.id
    group_id = -000000000000000
    full_name = message.from_user.full_name

    await bot.send_message(chat_id, 'Please choose category - Пожалуйста, выберите категорию: ', reply_markup=generate_category_menu())
    await bot.send_message(group_id, f'Foydalanuvchi {full_name} Buyurtma berishni bosdi!')

# Foydalanuvchiga menu chiqarib berish jarayoni
async def show_main_menu(message: Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "O'zingiz xohlagan narsani tanlang: ", reply_markup=generate_main_menu())   # reply_markup - knopkalani qaytarib berish kere

executor.start_polling(dp, skip_updates=True)  # Botimiza pastoyanno ishlab turishi uchun executor obyektiga murojat qilib  start_polling ni ishga tushurib, va executor bu botimizani ishga tushuradigon obyekt va executor yordamida botimizani ishga tushuramiza
# skip_updates=True argument - biza betda qaytadan botni ishga tushurmimiza yani start qaytadan bosish shart bomidi kod ishga tushurse shuni ozi yetadi