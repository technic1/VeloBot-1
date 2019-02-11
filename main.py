# -*- coding: utf-8 -*-
import telebot
import config
import json
import utils
import os
import paramiko
import time
from telebot import types

#### параметры ssh
host = config.host
user = config.user
secret = config.secret
port = 22

#### параметры локальные
local_host = config.local_host
local_user = config.local_user
local_password = config.local_password

#### параметры работы бота
bot = telebot.TeleBot(config.token)
login = config.login
pswd = config.pswd
auth_file = 'authorized.json'
pswd_file = 'password.txt'
worker_id = []
authorized_user = []

#### подключение по локальной сети

if os.stat(auth_file).st_size != 0: #### если файл не пустой, читаем из него id авторизованных юзеров
    with open (auth_file, 'r') as k:
        authorized_user = json.load(k)


@bot.message_handler(commands=['start'])
def start_msg(message):
    # markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    # btn_auth = types.KeyboardButton('/auth')
    # btn_connect = types.KeyboardButton('/con')
    # markup.add(btn_auth, btn_connect)
    # bot.send_message(message.chat.id, 'Authorization now', reply_markup=markup)
    bot.send_message(message.chat.id, 'Station number', reply_markup=utils.create_stations())

@bot.message_handler(commands=['auth'])
def welcome_msg(message):
    if message.chat.id not in authorized_user:
        msglog = bot.send_message(message.chat.id, "Введите логин")
        bot.register_next_step_handler(msglog, login_auth)
    else:
        check_code = str(utils.buildblock(6))
        with open (pswd_file, 'w') as c:
            json.dump(check_code, c)
        bot.send_message(43162157, check_code)
        msgauth = bot.send_message(message.chat.id, "Введите код подтверждения")
        bot.register_next_step_handler(msgauth, check_confirm)

def login_auth(message):
    if message.text != login:
        bot.send_message(message.chat.id, login)
    else:
        msgpswd = bot.send_message(message.chat.id, "Введите пароль")
        bot.register_next_step_handler(msgpswd, password_auth)

def password_auth(message):
    if message.text != pswd:
        return False
    else:
        check_code = str(utils.buildblock(6))
        with open (pswd_file, 'w') as f:
            json.dump(check_code, f)
        bot.send_message(43162157, check_code)
        accept = bot.send_message(message.chat.id, 'Введите код подтверждения.')
        bot.register_next_step_handler(accept, check_confirm)

def check_confirm(message):
    with open (pswd_file,'r') as f:
        check_code = f.read()
    if message.text in check_code:
        bot.send_message(message.chat.id, 'Всё окей. Ваш chat.id='+str(message.chat.id))
        if message.chat.id not in authorized_user:
            authorized_user.append(message.chat.id)
            with open (auth_file, 'w') as d:
                json.dump(authorized_user, d)
    else: 
        bot.send_message(message.chat.id, 'Неверный код')

@bot.message_handler(commands=['check'])
def test_command(message):
    bot.send_message(message.chat.id, message.text)

@bot.message_handler(commands=['connect'])
def connect(message):
    if 'local' in message.text:
        vpn.local_connect()
    else:
        vpn.connect_vpn()

@bot.message_handler(commands=['exit'])
def exit_usr(message):
    if message.chat.id in authorized_user:
        authorized_user.remove(message.chat.id)
        with open (auth_file, 'w') as j:
            json.dump(authorized_user, j)
        bot.send_message(message.chat.id, 'иди нахуй, Марина')

@bot.message_handler(commands=['close'])
def close_connection():
    channel.close()
    client.close()

@bot.message_handler(commands=['c'])
def command_consol(message):
    if message.chat.id in authorized_user:
        # channel.send(message.text[3:]+'\r\n')
        data = ''
        channel.send(message.text[3:]+'\n')
        while not data.endswith('# '):
            resp = channel.recv(9999)
            data += resp.decode()
        data = data[data.find(message.text[3:]) + len(message.text[3:]):data.find("root")]
        # data = channel.recv(9999)
        try:
            bot.send_message(message.chat.id, data)
        except:
            bot.send_message(message.chat.id, 'empty...')
    else:
        error = bot.send_message(message.chat.id, 'Вы не авторизованы')
        bot.register_next_step_handler(error, welcome_msg)

@bot.message_handler(commands=['con'], regexp="Connect")
def connection(message):
    if message.chat.id in authorized_user:
        bot.send_message(message.chat.id, 'Please wait about 20 seconds')
        global client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=config.host, username=config.user, password=config.secret, port=config.port)
        global channel
        # channel = client.get_transport().open_session()
        # channel.get_pty()
        # channel.settimeout(5)
        channel = client.invoke_shell()
        channel.send('ssh pi@192.168.78.{}'.format(message.text[:-2])+'\n')
        data = ''
        while not data.endswith('\'s password: '):
            resp = channel.recv(9999)
            data += resp.decode()
        time.sleep(3)
        channel.send(local_password + '\n')
        # bot.send_message(message.chat.id, data)
        while not data.endswith(':~$ '):
            resp = channel.recv(9999)
            data += resp.decode()
        time.sleep(3)
        # bot.send_message(message.chat.id, 'Ok')
        channel.send('sudo -s\n')
        while not data.endswith('pi# '):
            resp = channel.recv(9999)
            data += resp.decode()
        time.sleep(1)
        bot.send_message(message.chat.id, data)
        bot.send_message(message.chat.id, 'Ok\nNow u can write a command, for example: /c ls')
        # return channel.recv(1024)
    else:
        error = bot.send_message(message.chat.id, 'Вы не авторизованы')
        bot.register_next_step_handler(error, welcome_msg)


if __name__ == '__main__':
    bot.polling(none_stop=True)