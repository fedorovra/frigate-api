import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
ip = s.getsockname()[0]
s.close()

bind = ip + ':1025'
daemon = True
reload = True
workers = 5
threads = 10
