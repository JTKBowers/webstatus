import os

def is_up(host='8.8.8.8'):
    return os.system("ping -c 1 -w2 " + host + " > /dev/null 2>&1") == 0

if __name__ == '__main__':
    hostname = "8.8.8.8"
    print (is_up(hostname))
