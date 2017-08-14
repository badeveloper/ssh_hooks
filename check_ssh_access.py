import paramiko
from os.path import expanduser
import socket
import string
import time
#RSA keys files
# key_file_1 = {"file_path": '/path/to/rsa_private/key1', "key_comment": 'Some private key 1'}
# key_file_2 = {"file_path": '/path/to/rsa_private/key2', "key_comment": 'Some private key 2'}
# #SSH credentials
# ssh_ports       = [22, 2210, 2232]
# ssh_users       = ['user1', 'user2', 'root']
# ssh_passwords   = ['password1', 'password2']
# ssh_keys        =  [key_file_1, key_file_2]


key_file_1 = {"file_path": expanduser('~') + '/.ssh/x5_support' , "key_comment": 'access-all'}
DEVNULL = '/dev/null'
ssh_ports       = [22, 3030]
ssh_users       = ['support', 'root']
ssh_keys        =  [key_file_1]
ssh_passwords = ['113525']

#Try ssh client connect and hand exeption, if connect success return True, if can't connect return False
def try_ssh(host, port, ssh_user, ssh_password=None, ssh_key=None):
    succes = True
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(policy=paramiko.AutoAddPolicy())
    paramiko.util.log_to_file(DEVNULL)

    try:
        ssh_client.connect(hostname=host, username=ssh_user, password=ssh_password, pkey=ssh_key, port=port,
                   timeout=5, look_for_keys=False)
    except paramiko.ssh_exception.AuthenticationException: succes=False
    except paramiko.ssh_exception.NoValidConnectionsError: succes=False
    except socket.timeout: succes=False
    try:
        stdin, stdout, stderr = ssh_client.exec_command('echo 1', timeout=2)
        cmd_out = stdout.read()
        c = cmd_out.strip('\n')
        if c != '1':
         succes = False
    except paramiko.ssh_exception.SSHException: succes = False
    except AttributeError: succes = False
    ssh_client.close()
    return succes

#Brute force credentials and return success combinations, or empty list
def brutforce_credentials(ssh_host=None, ssh_ports=[22], ssh_users=None, ssh_passwords=None, ssh_keys=None):
    true_credentils = {"password_access": None, "key_access": None }
    if ssh_users:
        for ssh_user in ssh_users:
            if ssh_passwords:
                for ssh_password in ssh_passwords:
                    if ssh_ports:
                        for ssh_port in ssh_ports:
                            ssh_access_pwd = try_ssh(host=ssh_host, port=ssh_port, ssh_user=ssh_user, ssh_password=ssh_password)
                            if ssh_access_pwd:
                               #true_credentils.append([ssh_user, ssh_password, ssh_port])
                                true_credentils.update({"password_access": {"user": ssh_user, "password": ssh_password, "port": ssh_port} })
            if ssh_keys:
                for ssh_key in ssh_keys:
                    if ssh_ports:
                        for ssh_port in ssh_ports:
                            key = paramiko.RSAKey.from_private_key(open(ssh_key['file_path'], 'ra'))
                            ssh_access_key = try_ssh(host=ssh_host, port=ssh_port, ssh_user=ssh_user, ssh_key=key)
                            if ssh_access_key:
                                #true_credentils.append([ssh_user, ssh_key['key_comment'], ssh_port])
                                true_credentils.update({"key_access": {"user": ssh_user, "key_file": ssh_key['key_comment'], "port": ssh_port} })
    return true_credentils


# key = paramiko.RSAKey.from_private_key(open(key_file_1['file_path'], 'ra'))
# #print brutforce_credentials(ssh_host='msk-dpro-ora083.x5.ru', ssh_users=ssh_users, ssh_passwords=ssh_passwords, ssh_keys=ssh_keys, ssh_ports=ssh_ports)
# print try_ssh(host='msk-dpro-ora083', port=22, ssh_user='suppot', ssh_key=key)