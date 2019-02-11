import random
import string
import paramiko
import config

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


