from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CallbackContext
from datetime import datetime
from mix import *
import random
import sqlite3

# replace_first_name = ['Айрат, лучший бомбардир', 'СиРоЖа, второй из лучших бомбардиров', 'Темный, мутный',
# 'Перл Харбор, чернокожий', 'Потому что есть, Алёшка у тебя...', 'Светлый, бородач', 'Азатъ, сбивающий с ног',
# 'Леха Месси, в 2041 году', "Рустем I'm back, я буду возвращаться раз в 1-2 месяца", 'Данил, пропал', 'Тимур,
# костяная нога', 'Владик, пузатик', 'Андрэ, уже не тот, что был раньше', 'Володька, аллейкум', 'Альмир, закидон',
# 'Димоооон, на опыте', 'Макс, не помню тебя', 'Идир', 'Андрей', 'Рамис, тусовщик', 'Максим Серов,
# на ноги вставатель', 'Дмитрий', 'Никита, симулянт', 'Асыр, хрен знает кто ты', 'Мурад, до встречи в другой жизни',
# 'Иванушка, дурачок', 'Минтимер', 'Makc', 'Лысый из Brazzerz, типо умеет играть в футбол', 'Руслан, не смотрит
# когда, сдает назад', 'Айрат КАЗ, хитёр', 'Виктор, старается', 'АРамис, если вы проиграли, можете свалить все на
# меня']


you_not_list = ['Чувак, тебя нет в списке!', 'Ошибка, тебя нет в списке', "Опс, сначала добавься, а потом уже удаляйся",
                'Тебя нет', 'Тебя нет, но ты можешь добавиться', 'Кинули дважды , совести нет совсем…']
you_in_list = ["Ты уже в списке под именем: ", 'Эээ, сука, меня не проведешь, я тебя знаю, ты -  ', 'Какого ..уя '
                                                                                                    'ты творишь? ']

you_add_in_list = ['Ты в вписке чувак', 'Могучее ТЕЛО добавлено!', 'Крутяк!!!',
                   'Я знал, что ты придешь!', 'Ура, товарищи!!!', 'Ты сегодня за рыжих: ', 'За синих без бээээ',
                   'Я тебя обожаю!', 'Учти, с тебя минимум дубль сегодня!',
                   'Давай только без твоих выкрутасов в стиле Месси! окей?',
                   'Почитай сначала правила игры, а потом приходи!',
                   'На тебя поступила жалоба, что ты довольно часто забиваешь в свои ворота!', 'Ты сегодня в защите!',
                   'Ты добавлен, но будь добр, приходи трезвым!', 'Пузико решил растрясти?)',
                   'Так, смотри кто к нам пришел!',
                   'Сразу предупреждаю, у нас пеший футбол, тоесть пузико не исчезнет']

you_del_in_list = ['Бля, я так и знал, что ты это сделаешь!!!', 'Пацаны, нас кинули!', 'Бейте его!!!', 'Ты куда? ёмаё!',
                   'Даю тебе последний шанс вернуться!', 'Ну и съёбывай от сюда!', 'И как тебя назвать после этого?',
                   '...No comments...', 'Ты совершил ошибку!!', "Перепутал '+' c '-' ?", 'Пиздец конечно...']

you_add_friend_in_list = ['Могучее ТЕЛО добавлено!', 'Он точно придёт?', 'Если он не приедет, платишь за него тоже!',
                          'Это кто? Надеюсь Рональдиньо?',
                          'Неужели это Дзюба?', 'Он умеет играть?', 'Проинструктируй его, что у нас тут пеший футбол!',
                          'Пусть приходит!', 'Недеюсь он не хоккеист?', 'О, круто, оценим чувака!',
                          'Недеюсь это защитник? Нападающих тут и так дохуя!',
                          'Если это нападающий, то ему тут делать нехуй, конкуренция страшная!']

you_del_friend_in_list = ['Бля, я так и знал что ты это сделаешь!!!', 'Пацаны, нас кинули!', 'Бейте его!!!',
                          'Куда он?', 'Чё происходит не пойму?', 'Предсказуемо конечно!',
                          'Он что вспомнил, что никогда не играл в футбол?',
                          'Скажи ему, что тут ребята огорчились!', 'То добавляешь, то удаляешь, давай посерьезнее?']

serega_list = ['Володя тоже умеет считать, так что со счетом не наебешь!!!',
               'Серега, давай без мата сегодня!!!', 'Опять за рыжих пойдешь? Не надоело проебывать?',
               'Если ты с другого конца поля судишь кто был прав в нарушении...пиздец, у тебя орлиный глаз!']

greate_player_list = ['О, великий', 'О, могучий', 'О, мастер', 'Сегодня ты НЕ платишь за футбол',
                      'Рональдиньо отдыхает, когда играет', 'С тебя сегодня 5 голов', 'Ты лучший на сегодня -',
                      'Леха Месси отдыхает, когда играет', 'Сегодня ты красавчик'
                      ]
loser_player_list = ['за тебя сегодня платит', 'отдает тебе свою жену на ночь, если жены нет, то находит ей замену',
                     'пришлет видео с 20 отжиманиями, иначе получит бан на 1 месяц',
                     'стирает манижки на этой неделе', 'с удовольствием постирает одежду лучшего',
                     'устроит '
                     'костюмированную '
                     'вечеринку в своей '
                     'гардеробной',
                     'переименует все свои растения и разговаривает с ними каждое утро',
                     'устроит шоу теневого театра с использованием своих рук',
                     'придумает историю для каждого предмета в своем холодильнике',
                     'посвятит день изучению танца живота и покажет нам свой прогресс',
                     'пригласить нас на виртуальную вечеринку и проведет мастер-класс по пению душевных песен',
                     'проведет день, выражая свои мысли только в виде характерных смайликов']


my_list = []
time_default = 0
LIMIT_HOUR = 10
LIMIT_HOUR_START = 8
LIMIT_HOUR_START2 = 9
GRATE_PLAYER = None
LOSER_PLAYER = None


def stat_create(db_name_: str):
    m = ''
    conn = sqlite3.connect('user_name.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT * from {db_name_}')
    records = cursor.fetchall()
    cursor.execute(f'SELECT COUNT(blue) FROM {db_name_} WHERE blue > redheads')
    blue_points = cursor.fetchone()[0] * 3
    cursor.execute(f'SELECT COUNT(blue) FROM {db_name_} WHERE blue < redheads')
    redheads_points = cursor.fetchone()[0] * 3
    cursor.execute(f'SELECT COUNT(blue) FROM {db_name_} WHERE blue = redheads')
    draw = cursor.fetchone()[0]
    blue_points += draw
    redheads_points += draw
    cursor.execute(f'SELECT SUM(blue) FROM {db_name_}')
    goals_blue = cursor.fetchone()[0]
    cursor.execute(f'SELECT SUM(redheads) FROM {db_name_}')
    goals_redheads = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    m += f'Общий счет по очкам:\nСиние {blue_points} : {redheads_points} Рыжие\n\nОбщий счет по голам:\nСиние' \
         f' {goals_blue} :' \
         f' {goals_redheads} ' \
         f'Рыжие\n\n'
    for i in records:
        m += f'{i[0]}... Синие {i[1]} : {i[2]} Рыжие\n'
    m += '\n'
    return m


def db_table(user_id: int, user_name: str):
    conn = sqlite3.connect('user_name.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users(id_ int, name varchar(50))')  # создаю
    # таблицу,
    # если ее нет
    cursor.execute(f'SELECT id_ FROM users WHERE id_ = {user_id}')  # выбираю один элемент с user_id
    id_tuple = cursor.fetchone()
    if id_tuple:
        cursor.execute(f'SELECT name FROM users WHERE id_ = {user_id}')
        name_tuple = cursor.fetchone()[0]
        id_u = id_tuple[0]
        cursor.execute(f"UPDATE users set name = ? WHERE id_ = ?", (user_name, id_u))
        conn.commit()
        cursor.close()
        conn.close()
        return name_tuple
    else:
        cursor.execute('INSERT INTO users(id_, name) VALUES(?, ?)', (user_id, user_name))
        conn.commit()
        cursor.close()
        conn.close()
        return None


def db_load(user_id: int):
    conn = sqlite3.connect('user_name.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users(id_ int, name varchar(50))')  # создаю таблицу, если ее нет
    cursor.execute(f'SELECT name FROM users WHERE id_ = {user_id}')  # выбираю один элемент с user_id
    name_tuple = cursor.fetchone()
    name_u = None
    if name_tuple:
        name_u = name_tuple[0]
        cursor.close()
        conn.close()
        return name_u
    else:
        cursor.close()
        conn.close()
        return name_u


def limit_player_loader():
    conn = sqlite3.connect('user_name.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT limit_player FROM limit_player')
    limit_pl = cursor.fetchall()[-1]
    # print(limit_pl)
    # print(len(limit_pl))
    return limit_pl


def log_name(update: Update):
    file = open('log6.txt', 'a', encoding='utf-8')
    file.write(f'{update.message.from_user.id}, '
               f'{update.message.from_user.first_name}, '
               f'{update.message.text}, '
               f'{update.message.date}, '
               f'{update.message.chat.id} '
               f'{update.message.chat.title}\n')
    file.close()


async def log(update: Update, context: ContextTypes):
    log_name(update)


def create_message(data, limit_player, number):
    message = ''.join(stat_create('goals_summer2024').splitlines(keepends=True)[:6])
    message += 'Основной список:\n'
    rezerv = ''
    message_random_data_01 = ''
    message_random_data_02 = ''

    if len(data) == 0:
        return 'Ау, люди вы где?'
    elif len(data) <= limit_player:
        if len(data) < limit_player:
            for i in range(len(data)):
                message += f'{i + 1}.  {data[i]}\n'
            return message
        elif len(data) == limit_player:
            global GRATE_PLAYER, LOSER_PLAYER
            players = data[:limit_player]
            if GRATE_PLAYER is None:
                GRATE_PLAYER = random.choices(players)[0]
                players.remove(GRATE_PLAYER)
                LOSER_PLAYER = random.choices(players[:limit_player - 1])[0]
            elif GRATE_PLAYER not in players and LOSER_PLAYER not in players:
                players = data[:limit_player]
                GRATE_PLAYER = random.choices(players)[0]
                players.remove(GRATE_PLAYER)
                LOSER_PLAYER = random.choices(players[:limit_player - 1])[0]
            elif GRATE_PLAYER not in players:
                players = data[:limit_player]
                players.remove(LOSER_PLAYER)
                GRATE_PLAYER = random.choices(players[:limit_player - 1])[0]
            elif LOSER_PLAYER not in players:
                players.remove(GRATE_PLAYER)
                LOSER_PLAYER = random.choices(players[:limit_player - 1])[0]
            if '+1' in GRATE_PLAYER:
                GRATE_PLAYER = GRATE_PLAYER.replace('+1', 'друг')
            if '+1' in LOSER_PLAYER:
                LOSER_PLAYER = LOSER_PLAYER.replace('+1', 'друг')
            # print(f'{type(GRATE_PLAYER)}: {GRATE_PLAYER=}')
            # print(f'{type(LOSER_PLAYER)}: {LOSER_PLAYER=}')
            for i in range(len(data)):
                message += f'{i + 1}.  {data[i]}\n'
            random_data = mix_list(data)

            len_random_data = len(random_data) // 2
            for i in range(len_random_data):
                message_random_data_01 += f'{i + 1}.  {random_data[i * 2]}\n'
            for i in range(len_random_data):
                message_random_data_02 += f'{i + 1}.  {random_data[i * 2 + 1]}\n'
            winning = random.randint(0, 1)
            if winning == 0:
                winner = 'Рыжие'
                loser = 'Синие'
            else:
                winner = 'Синие'
                loser = 'Рыжие'
            loser_num = random.randint(6, 12)
            winner_num = random.randint(loser_num, 20)
            message_random_data = f'_Набор закрыт.\n\n_' \
                                  f'{message}' \
                                  f'\n' \
                                  f'Рекомендую поделиться так:\n' \
                                  f'\n' \
                                  f'Синие:\n' \
                                  f'{message_random_data_01}' \
                                  f'\n' \
                                  f'Рыжие:\n' \
                                  f'{message_random_data_02}\n' \
                                  f'Судя по командам, мой прогноз:  {winner} {winner_num} : {loser_num} {loser}. ' \
                                  f'\n\n' \
                                  f'--------------------------------------------------------\n' \
                                  f'*{greate_player_list[random.randint(0, len(greate_player_list) - 1)]} *' \
                                  f'*{GRATE_PLAYER}.\n*' \
                                  f'*А {LOSER_PLAYER} *' \
                                  f'*{loser_player_list[random.randint(0, len(loser_player_list) - 1)]}.*'
            return message_random_data
    else:
        for i in range(limit_player):
            message += f'{i + 1}.  {data[i]}\n'
        data_rezerv = data[limit_player:]  # список резерва
        for i in range(len(data_rezerv)):
            rezerv += f'{i + 1}.  {data_rezerv[i]}\n'

        if number == 0:
            new_message = f'Ты в резерве!\n' \
                          f'\n' \
                          f'Резерв!\n' \
                          f'{rezerv}' \
                          f'\n' \
                          f'{message}'
            return new_message
        elif number == 1:
            new_message = f'Твой игрок в резерве!\n' \
                          f'\n' \
                          f'Резерв!\n' \
                          f'{rezerv}' \
                          f'\n' \
                          f'{message}'
            return new_message
        elif number == 2:
            new_message = f'Резерв!\n' \
                          f'{rezerv}' \
                          f'\n' \
                          f'{message}'

            return new_message


async def run(update: Update.message, context: ContextTypes):
    global time_default
    LIMIT_PLAYER = int(limit_player_loader()[0])
    log_name(update)
    dt_hour = datetime.now().hour
    dt_day_now = datetime.now().day
    mess = ''
    user_id = update.message.from_user.id
    user_name = db_load(user_id)
    if dt_hour < LIMIT_HOUR_START:
        mess = f'*Голосование начинается с 9 часов!*'
        await update.message.reply_text(f'{mess}', quote=True, parse_mode='Markdown')
    elif dt_hour < LIMIT_HOUR_START2 and update.message.from_user.id != 5157599418:
        mess = f'*Голосование начинается с 9 часов!*'
        await update.message.reply_text(f'{mess}', quote=True, parse_mode='Markdown')
    else:
        if int(dt_day_now) != time_default:
            my_list.clear()
            time_default = dt_day_now
            # my_list.append('Айрат')
        if update.message.text == '+':
            if user_name is None:
                user_name = update.message.from_user.first_name
            if user_name not in my_list:
                my_list.append(user_name)
                if update.message.from_user.id == 2063531206:
                    mess = f'{serega_list[random.randint(0, len(serega_list) - 1)]}\n' \
                           f'\n' \
                           f'{create_message(my_list, LIMIT_PLAYER, 0)}'
                else:
                    mess = f'{you_add_in_list[random.randint(0, len(you_add_in_list) - 1)]}\n' \
                           f'\n' \
                           f'{create_message(my_list, LIMIT_PLAYER, 0)}'
            else:
                mess = f'*{you_in_list[random.randint(0, len(you_in_list) - 1)]}{user_name}*'
        elif update.message.text == '-':
            if user_name is None:
                user_name = update.message.from_user.first_name

            if user_name in my_list:
                my_list.remove(user_name)
                mess = f'*{you_del_in_list[random.randint(0, len(you_del_in_list) - 1)]}*\n' \
                       f'\n' \
                       f'{create_message(my_list, LIMIT_PLAYER, 2)}'
            else:
                mess = f'*{you_not_list[random.randint(0, len(you_not_list) - 1)]}*'
        elif update.message.text == '+1':
            # print(f'время сейчас {dt_hour}')
            # print(f'Лимит времени {LIMIT_HOUR}')
            if dt_hour >= LIMIT_HOUR:
                if user_name is None:
                    user_name = update.message.from_user.first_name
                user_plus_1 = f'+1 от {user_name}'
                my_list.append(user_plus_1)
                mess = f'*{you_add_friend_in_list[random.randint(0, len(you_add_friend_in_list) - 1)]}*\n' \
                       f'\n' \
                       f'{create_message(my_list, LIMIT_PLAYER, 1)}'

            else:
                mess = f'*Добавить игрока можно после {LIMIT_HOUR} часов!*'
        elif update.message.text == '-1':
            if user_name is None:
                user_name = update.message.from_user.first_name
            user_plus_1 = f'+1 от {user_name}'
            if user_plus_1 in my_list:
                my_list.remove(user_plus_1)
                mess = f'*{you_del_friend_in_list[random.randint(0, len(you_del_friend_in_list) - 1)]}*\n' \
                       f'\n' \
                       f'{create_message(my_list, LIMIT_PLAYER, 2)}'
            else:
                mess = '*Твоего игрока нет в списке!*'

        await update.message.reply_text(f'{mess}', quote=True, parse_mode='Markdown')


async def help_command(update: Update.message, context: CallbackContext):
    await update.message.reply_text(f"Добавиться в список: отправь ' + ' \n"
                                    f"Удалиться из списка: отправь ' - ' \n"
                                    f"Добавить одного игрока в список: отправь ' +1 ' \n"
                                    f"Удалить одного игрока из списка: отправь ' -1 '\n"
                                    f"/del - обнулить список\n"
                                    f"/stat - посмотреть статистику\n\n"
                                    f"'/add 3 3' - добавить статистику.\n "
                                    f"'команда''пробел''число''пробел''число'.\n "
                                    f"Первое число количество голов синих, второе число количество голов рыжих.\n\n"
                                    f"'/chg_name Иван' - изменить имя в списке. Имя может состоять из 1 или 2 слов.\n"
                                    f"'команда''пробел''имя'\nили\n'команда''пробел''первая часть "
                                    f"имени''пробел''вторая часть имени'\n\n"
                                    f"'/chg_limit_pl 14' - Изменить лимит игроков.\n"
                                    f"'команда' 'пробел' 'число'.\n"
                                    f"Число - это лимит игроков. Например 12, если играем в манеже.\n"
                                    f"\n"
                                    f"", quote=True)


async def change_command(update: Update.message, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(text='Да', callback_data='yes'), InlineKeyboardButton(text='Нет',
                                                                                            callback_data='no')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text='Хочешь изменить имя?', reply_markup=reply_markup)


async def change_limit_player(update: Update.message, context: CallbackContext):
    if len(context.args) == 1:
        limit_players = context.args[0]
        if int(limit_players) % 2 != 0:
            await update.message.reply_text(f'<u>Ошибка. Лимит игроков должен быть кратный двум.</u>\n', quote=True,
                                            parse_mode='html')
        else:
            LIMIT_PLAYER = int(limit_player_loader()[0])
            date_game = str(datetime.now())[:10]
            conn = sqlite3.connect('user_name.db')
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS limit_player(dategame varchar(20), limit_player int)')
            cursor.execute('INSERT INTO limit_player(dategame, limit_player) VALUES(?, ?)', (date_game, limit_players,))
            conn.commit()
            cursor.close()
            conn.close()
            await update.message.reply_text(f'<u>Лимит игроков изменен на {limit_players}.</u>\n'
                                            f'{create_message(my_list, LIMIT_PLAYER, 0)}', quote=True,
                                            parse_mode='html')
    else:
        await update.message.reply_text(f'<u>Ошибка при изменении лимита игроков. Введи /help для помощи.</u>',
                                        quote=True,
                                        parse_mode='html')


async def button(update: Update.message, context: CallbackContext):
    query = update.callback_query
    choice = query.data
    await query.answer()
    if choice == 'no':
        await query.edit_message_text(text=f"Какого хрена ты меня отвлекаешь?")
    else:
        user_id_ = update.callback_query.from_user.id
        # await query.register_next_step_handler(user_id_)

        # for i in range(len(user_id)):
        #     if user_id_ == user_id[i]:
        #         old = replace_first_name[i]
        #         replace_first_name[i] = "Айратттт"
        #         new = replace_first_name[i]
        #         await query.edit_message_text(text=f"{old} изменено на {new}")


async def add_goals(update: Update.message, context: CallbackContext):
    if len(context.args) == 2 and context.args[0].isdigit() and context.args[1].isdigit():
        m = ''
        blue = context.args[0]  # голы синих
        redheads = context.args[1]  # голы рыжих
        date_game = str(datetime.now())[:10]
        conn = sqlite3.connect('user_name.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS goals_summer2024(date_game char(20), blue int, redheads int)')
        cursor.execute('INSERT INTO goals_summer2024(date_game, blue, redheads) VALUES(?, ?, ?)',
                       (date_game, blue, redheads))
        conn.commit()
        cursor.close()
        conn.close()
        m = stat_create('goals_summer2024')
        await update.message.reply_text(m, quote=True)
    else:
        await update.message.reply_text(f'<u>Ошибка при добавлении статистики. Введи /help для помощи.</u>', quote=True,
                                        parse_mode='html')


async def change_name(update: Update.message, context: CallbackContext):
    global my_list
    if 3 > len(context.args) > 0:
        new_name = context.args[0].title()
        if len(context.args) == 2:
            new_name += ' ' + context.args[1]
        # print(type(new_name))
        user_id_ = update.message.from_user.id
        value = db_table(user_id_, new_name)
        if value:
            if len(my_list) > 0:
                my_list = [new_name if x == value else x for x in my_list]
                my_list = [f'+1 от {new_name}' if x == f'+1 от {value}' else x for x in my_list]
            await update.message.reply_text(f'<u>Имя {value} изменено на {new_name}.</u>', quote=True,
                                            parse_mode='html')
        else:
            await update.message.reply_text(f'<u>Имя {update.message.from_user.first_name} изменено на {new_name}.</u>',
                                            quote=True,
                                            parse_mode='html')
    else:
        await update.message.reply_text(f'<u>Ошибка при добавлении имени. Введи /help для помощи</u>', quote=True,
                                        parse_mode='html')


async def del_command(update: Update.message, context: ContextTypes):
    global my_list
    my_list = []
    await update.message.reply_text(f"Эээ, список кто-то ёбнул", quote=True)


async def tela_tela(context: CallbackContext):
    global my_list
    LIMIT_PLAYER = int(limit_player_loader()[0])
    if len(my_list) < LIMIT_PLAYER:
        await context.bot.send_message(chat_id=-630322479, text='*Тела, тела, тела, тела, тела, тела....*',
                                       parse_mode='Markdown')


async def stat_command(update: Update.message, context: ContextTypes):
    await update.message.reply_text(stat_create('goals_summer2024'), quote=True)

# if __name__ == '__main__':
#     # date_game = str(datetime.now())[:10]
#     # conn = sqlite3.connect('user_name.db')
#     # cursor = conn.cursor()
#     # cursor.execute('CREATE TABLE IF NOT EXISTS seasons(date_game char(20), blue_point int, redheads_point int, '
#     #                'blue_win int, '
#     #                'redhead_win int)')
#     # cursor.execute('INSERT INTO seasons(date_game, blue_point, redheads_point, blue_win, redhead_win)'
#     #                ' VALUES(?, ?, ?, ?, ?)', (date_game, 12, 15, 0, 1))
#     # # cursor.execute('INSERT INTO goals(date_game, blue, redheads) VALUES(?, ?, ?)', (date_game, blue, redheads))
#     # conn.commit()
#     # cursor.close()
#     # conn.close()
