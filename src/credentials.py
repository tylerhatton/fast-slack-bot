import json


def get_hosts(filename):
    with open(filename) as cred_file:
        hosts = []
        for host in json.load(cred_file).keys():
            hosts.append(host)
        return hosts


def get_username(filename, host):
    with open(filename) as cred_file:
        username = json.load(cred_file)[host]['username']
        return username


def get_password(filename, host):
    with open(filename) as cred_file:
        password = json.load(cred_file)[host]['password']
        return password
