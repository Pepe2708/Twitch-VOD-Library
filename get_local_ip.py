import socket

ip = socket.gethostbyname(socket.gethostname())
print(ip)

f = "script.js"

lines = open(f, "r").readlines()
lines[-1] = f"var ip = '{ip}'"

open(f, 'w').writelines(lines)