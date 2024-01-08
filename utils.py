from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

# markup - argument sifatida va markup ni malumotlar turi InlineKeyboardMarkup
# lst - argument sifatida va lst ni malumotlar turi list
# prefix - argument sifatida va prefix ni  malumotlar turi str
# in_row - argument sifatida va in_row ni malumotlar turi int va defoult holadida 2 ga teng boladi
def build_inline_menu(markup: InlineKeyboardMarkup, lst: list, prefix: str, in_row: int = 2):
    in_row = in_row   # in_row = in_row kak to 2 = 2 oxshash qilib qoyilgande Har bitta sozdat qilingandan keyin abnuleniye yani sbrasivaniye bolishi uchun
    rows = len(lst) // in_row
    if len(lst) % in_row != 0:
        rows += 1

    start = 0
    end = in_row

    for i in range(rows):
        new_lst = []
        for pk, name in lst[start:end]:
            new_lst.append(
                InlineKeyboardButton(text=name, callback_data=f'{prefix}_{pk}')   # callback_data - qanaka qilib abrabotka qilish
            )
        markup.row(*new_lst)
        start = end
        end += in_row

    if prefix == 'product':
        markup.row(
            InlineKeyboardButton(text='Back', callback_data='main_menu')
        )

# prefix - bu bizada categoriyamizani nomi, pk - categoriyamizani id - si hisoblanadi

