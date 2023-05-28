import socket
import time

local_host = '127.0.0.1'
timer_port = 3000

TIMER_ON = "ON"
TIMER_OFF = "OFF"

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((local_host, timer_port))

        sock.listen(1)

        timer_sock, timer_addr = sock.accept()

        sock.setblocking(False)
        timer_sock.setblocking(False)
        status = ""
        s_time = None
        timer_on = False
        while True:
            try:
                status = timer_sock.recv(1024).decode()
            except:
                pass
            if timer_on is False and status == TIMER_ON:
                s_time = time.time()
                timer_on = True
            elif status == TIMER_OFF:
                timer_on = False
            if timer_on and time.time() - s_time > 10:
                timer_sock.send("overtime".encode())
                sock.close()
                timer_sock.close()
                exit(1)


            status = ""

    except KeyboardInterrupt:
        sock.close()
        timer_sock.close()
        exit(1)


if __name__ == '__main__':
    main()