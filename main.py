import telebot
from telebot import types
from datetime import datetime, date
import psycopg2

token = "2122712412:AAEmixIWC_hhbxxkpknvOl3BSz_3-3GA1p4"
bot = telebot.TeleBot(token)
bottom = 'Нижняя'
top = 'Верхняя'
type_of_week = bottom
DATE = datetime(2021, 8, 30)

"DATABASE"
conn = psycopg2.connect(database="timetablebfi",
                        user="postgres",
                        password="09fiveva",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


def Type_of_week():
    global type_of_week
    date_ = datetime.now()
    d = int((str(date_ - DATE)).split()[0])
    if (d // 7 + 1) % 2 == 0:
        type_of_week = bottom
    else:
        type_of_week = top


def print_timetable(day):
    cursor.execute("SELECT subject, room_numb, start_time FROM tables.timetable WHERE day=%s ", str(day))
    mass = list(cursor.fetchall())
    massage = ''
    for i in range(len(mass)):
        local_line = '<' + mass[i][0] + '>' + ' <' + mass[i][1] + '> < ' + mass[i][2] + '>' + '\n'
        massage += local_line
    return massage


def GetFullName(day):
    cursor.execute("SELECT subject FROM tables.timetable WHERE day=%s ", str(day))
    mass = list(cursor)
    if day == 0:
        cursor.execute("SELECT teacher FROM tables.timetable WHERE day=%s ", str(day))


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Приступим", "Пары - это не для меня")
    bot.send_message(message.chat.id,
                     'Здравствуйте! Этот бот поможет Вам узнать расписние вашей группы(БФИ2102, если Вы ,вдруг, забыли)',
                     reply_markup=keyboard)


@bot.message_handler(commands=['mtuci'])
def mtuci(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Понедельник", "Вторник", "Среда")
    keyboard.row("Четверг", "Пятница")
    keyboard.row("Расписание на текущую неделю")
    keyboard.row("Расписание на следующую неделю")
    keyboard.row("Назад")
    bot.send_message(message.chat.id, 'https://mtuci.ru/', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'О боте: подскажет Вам расписание на эту или следующую неделю' + '\n' + 'Список '
                                                                                                              'команд:' + '\n' +
                     '/week - подскажет вам какая сейчас неделя: верхняя или нижняя' + '\n' +
                     '/mtuci - https://mtuci.ru/' + '\n' +
                     'Назад - вернёт Вас назад)')


@bot.message_handler(commands=['week'])
def start(message):
    global type_of_week
    date_ = datetime.now()
    d = int((str(date_ - DATE)).split()[0])
    if (d // 7 + 1) % 2 == 0:
        bot.send_message(message.chat.id, bottom)
    else:
        bot.send_message(message.chat.id, top)


@bot.message_handler(content_types=['text'])
def answer(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Понедельник", "Вторник", "Среда")
    keyboard.row("Четверг", "Пятница")
    keyboard.row("Расписание на текущую неделю")
    keyboard.row("Расписание на следующую неделю")
    keyboard.row("Назад")
    if message.text.lower() == "приступим":
        bot.send_message(message.chat.id,
                         "Ну что ж, приступаю! " + '\n' + "Для получения информации о боте и списке команд введите /help",
                         reply_markup=keyboard)
    elif message.text.lower() == 'пары - это не для меня':
        keyboard2 = types.ReplyKeyboardMarkup()
        keyboard2.row('Назад')
        bot.send_message(message.chat.id, ':(', reply_markup=keyboard2)
    elif message.text.lower() == 'назад':
        keyboard_first = types.ReplyKeyboardMarkup()
        keyboard_first.row("Приступим", "Пары - это не для меня")
        bot.send_message(message.chat.id, "Ну чтож, приступаю! ", reply_markup=keyboard_first)
    elif message.text.lower() == 'понедельник' and type_of_week == top:
        bot.send_message(message.chat.id, "Понедельник" + '\n' + print_timetable(0), reply_markup=keyboard)
    elif message.text.lower() == 'вторник' and type_of_week == top:
        bot.send_message(message.chat.id, "Вторник" + '\n' + print_timetable(1), reply_markup=keyboard)
    elif message.text.lower() == 'среда' and type_of_week == top:
        bot.send_message(message.chat.id, "Среда" + '\n' + print_timetable(2), reply_markup=keyboard)
    elif message.text.lower() == 'четверг' and type_of_week == top:
        bot.send_message(message.chat.id, "Четверг" + '\n' + print_timetable(3), reply_markup=keyboard)
    elif message.text.lower() == 'пятница':
        bot.send_message(message.chat.id, "Пятница" + '\n' + print_timetable(4), reply_markup=keyboard)
    elif message.text.lower() == 'расписание на текущую неделю':
        if type_of_week == top:
            result = "Понедельник" + '\n' + print_timetable(0) + '\n' + "Вторник" + '\n' + print_timetable(
                1) + '\n' + "Среда" + '\n' + print_timetable(2) + '\n' + "Четверг" + '\n' + print_timetable(
                3) + '\n' + "Пятница" + '\n' + print_timetable(4)
            bot.send_message(message.chat.id, "Расписание на текущую неделю" + '\n' + result, reply_markup=keyboard)
        else:
            result = "Понедельник" + '\n' + print_timetable(5) + '\n' + "Вторник" + '\n' + print_timetable(
                6) + '\n' "Среда" + '\n' + print_timetable(
                7) + "\n" + "Четерг" + "\n" + "Chill day" + " " + "\n" + '\n' + "Пятница" + '\n' + print_timetable(4)
            bot.send_message(message.chat.id, "Расписание на следующую неделю" + '\n' + result, reply_markup=keyboard)
    elif message.text.lower() == 'понедельник' and type_of_week == bottom:
        bot.send_message(message.chat.id, "Понедельник" + '\n' + print_timetable(5), reply_markup=keyboard)
    elif message.text.lower() == 'вторник' and type_of_week == bottom:
        bot.send_message(message.chat.id, "Вторник" + '\n' + print_timetable(6), reply_markup=keyboard)
    elif message.text.lower() == 'среда' and type_of_week == bottom:
        bot.send_message(message.chat.id, "Среда" + '\n' + print_timetable(7), reply_markup=keyboard)
    elif message.text.lower() == 'четверг' and type_of_week == bottom:
        bot.send_message(message.chat.id, "Chill day", reply_markup=keyboard)
    elif message.text.lower() == 'расписание на следующую неделю':
        if type_of_week == top:
            result = "Понедельник" + '\n' + print_timetable(5) + '\n' + "Вторник" + '\n' + print_timetable(
                6) + '\n' "Среда" + '\n' + print_timetable(
                7) + "\n" + "Четерг" + "\n" + "Chill day" + '\n' + " " + "\n" + "Пятница" + '\n' + print_timetable(4)
            bot.send_message(message.chat.id, "Расписание на следующую неделю" + '\n' + result, reply_markup=keyboard)
        else:
            result = "Понедельник" + '\n' + print_timetable(0) + '\n' + "Вторник" + '\n' + print_timetable(
                1) + '\n' + "Среда" + '\n' + print_timetable(2) + '\n' + "Четверг" + '\n' + print_timetable(
                3) + '\n' + "Пятница" + '\n' + print_timetable(4)
            bot.send_message(message.chat.id, "Расписание на текущую неделю" + '\n' + result, reply_markup=keyboard)
    else:
        commands = ["help", "mtuci", "week", "start"]
        if message.text not in commands:
            bot.send_message(message.chat.id, "Простите, я Вас не понимаю")


if __name__ == '__main__':
    Type_of_week()
    bot.polling(none_stop=True)
