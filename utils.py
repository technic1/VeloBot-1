import random
import string
import paramiko
import config

def connect_vpn(): #### подключение к серверу по ssh
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=config.host, username=config.user, password=config.secret, port=config.port)
    channel = client.get_transport().open_session()
    channel.get_pty()
    channel.settimeout(5)

def local_connect(): #### локальное подключение к станции
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=local_host, username=local_user, password=local_password, port=port)
    stdin, stdout, stderr = client.exec_command('ls -l')
    data = stdout.read() + stderr.read()
    return data

def command_local(exe): #### функция выполнения присланной команды (не работает)
    stdin, stdout, stderr = channel.exec_command(exe)
    data = stdout.read() + stderr.read()
    return data

def buildblock(size): #### генерация защитного кода
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))



