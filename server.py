import socket

sock = socket.socket() # включаем сокет
sock.bind(('',9090)) # 1 - хост, 2 - порт
sock.listen(1) # арг - сколько "человек" в очереди (максимальное количество подключений в очереди)

conn, addr = sock.accept() # принимаем подлючение, получаем кортеж: новый сокет и адрес клиента

# связь с клиентом установлена

while True:
    data = conn.recv(1024) #recv - метод для чтения данных, принимает в арг получаемый размер данных
    if not data:
        break
    conn.send(data.upper())
    
conn.close()