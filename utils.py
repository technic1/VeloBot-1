import random
import string
import paramiko

def connect_vpn(): #### подключение к серверу по ssh
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
    stdin, stdout, stderr = client.exec_command('ls')
    data = stdout.read() + stderr.read()
    print(data[:10])
    client.close()
    return data

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



