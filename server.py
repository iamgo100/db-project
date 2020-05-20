import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
# включаем сокет,
# задамем семейство протоколов 'Интернет' (INET),
# задаем тип передачи данных 'потоковый' (TCP),
# выбираем протокол 'по умолчанию' для TCP, т.е. IP
sock.bind(('',9090)) # 1 - хост, 2 - порт
sock.listen(10) # арг - сколько "человек" в очереди (максимальное количество подключений в очереди)

while True:
    conn, addr = sock.accept() # принимаем подлючение, получаем кортеж: новый сокет и адрес клиента

    print('connected by',addr) # связь с клиентом установлена

    while True:
        data = conn.recv(1024) #recv - метод для чтения данных, принимает в арг получаемый размер данных
        if not data:
            break
        conn.sendall(data)
        
    conn.close()
