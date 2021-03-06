import random
import string
import paramiko
import config
import csv
from telebot import types

def connect_vpn(): #### подключение к серверу по ssh
    global client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=config.host, username=config.user, password=config.secret, port=config.port)
    global channel
    channel = client.get_transport().open_session()
    channel.get_pty()
    channel.settimeout(5)

def local_connect(message): #### локальное подключение к станции
    channel.exec_command('ssh pi@192.168.78.{}'.format(message.text[6:]))
    channel.send(config.local_password+'\n')
    return channel.recv(1024)

def command_local(exe): #### функция выполнения присланной команды (не работает)
    stdin, stdout, stderr = channel.exec_command(exe)
    data = stdout.read() + stderr.read()
    return data

def buildblock(size): #### генерация защитного кода
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

def create_callback_data(action,number):
    """ Create the callback data associated to each button"""
    return ";".join([action,str(number)])

def create_stations():
    index = 0
    new_stations = []
    with open('stations.csv', 'r', encoding="utf8") as stations_spb:
        reader = csv.reader(stations_spb, dialect=csv.excel_tab)
        for row in reader:
            if index > 0:
                new_stations.append(row)
            index += 1
    # keyboard = []
    # row = []
    #for station in new_stations:
    #    row.append(types.InlineKeyboardButton(station[0], station[1],
    #                                          callback_data=create_callback_data("station", station[0]))
    # keyboard.append(row)
    return new_stations

