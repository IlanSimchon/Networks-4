# import sys
# import socket
# import os
# import struct
# import time
# import statistics as stats
#
# ICMP_ECHO_REQUEST = 8
# ICMP_ECHO_CODE = 0
# ICMP_ECHO_REPLY = 0
# PACKET_SIZE = 64
#
# local_host = '127.0.0.1'
# timer_port = 3000
#
# TIMER_ON = "ON"
# TIMER_OFF = "OFF"
#
#
# def checksum(data):
#     sum = 0
#     count_to = (len(data) // 2) * 2
#     count = 0
#
#     while count < count_to:
#         this_val = data[count+1] * 256 + data[count]
#         sum += this_val
#         sum &= 0xffffffff
#         count += 2
#
#     if count_to < len(data):
#         sum += data[len(data) - 1]
#         sum &= 0xffffffff
#
#     sum = (sum >> 16) + (sum & 0xffff)
#     sum += (sum >> 16)
#     result = ~sum & 0xffff
#     result = socket.htons(result)
#
#     return result
#
#
# def receive_ping(sock, count, host_ip):
#     OK = False
#
#     count_rece = 0
#     start_time = time.time()
#
#     recv_packet, addr = sock.recvfrom(PACKET_SIZE + 28)
#     icmp_header = recv_packet[20:28]
#     icmp_type, code, checksum, packet_id, sequence = struct.unpack(
#         "bbHHh", icmp_header
#     )
#
#     finish_time = (time.time() - start_time) * 1000
#
#     len_of_packet = len(recv_packet[20:])
#     ip_addr = addr[0]
#     ttl = recv_packet[8]
#     if ip_addr == host_ip and packet_id == os.getgid():
#         count_rece += 1
#         if count == 1:
#             print(f"PING {host_ip} ({host_ip}) {len(recv_packet[28:])}({len(recv_packet)}) bytes of data.")
#         if icmp_type == ICMP_ECHO_REPLY:
#             OK = True
#             print(f"{len_of_packet} bytes from {ip_addr}: icmp_seq={count} ttl={ttl} time={finish_time:.3f} ms")
#
#     return finish_time , OK
#
# def send_ping(host_ip):
#     times = []
#
#     count = 0
#     count_recev = 0
#
#     sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
#
#     timer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#     timer_sock.connect((local_host, timer_port))
#
#
#     try:
#         while True:
#             count += 1
#             packet = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, ICMP_ECHO_CODE, 0, 0, count)
#             data = b"this is my massage"
#
#             calc_checksum = checksum(packet + data)
#
#             packet = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, ICMP_ECHO_CODE, calc_checksum, 0, count)
#
#             to_send = packet + data
#
#             sock.sendto(to_send, (host_ip, 1))
#
#             timer_sock.send(TIMER_ON.encode())
#
#             answer = receive_ping(sock,  count , host_ip)
#
#             if answer[1]:
#                 timer_sock.send(TIMER_OFF.encode())  # maybe need if
#
#             times.append(answer[0])
#             if answer[1]:
#                 count_recev += 1
#             time.sleep(1)
#
#
#     except KeyboardInterrupt:
#
#         print(f"\n--- {host_ip} ping statistics ---")
#         print(f"{count} packets transmitted, {count_recev} received, {int((1 - (count_recev / count)) * 100)}% packet loss, time {int(sum(times))}ms")
#         if count_recev != 0:
#             Min = min(times)
#             avg = stats.mean(times)
#             Max = max(times)
#             differences = [abs(time - avg) for time in times]
#             mdev = stats.mean(differences)
#             print(f"rtt min/avg/max/mdev ={Min:.3f}/{avg:.3f}/{Max:.3f}/{mdev:.3f} ms")
#
#         sock.close()
#         timer_sock.close()
#
#
# def main():
#     if len(sys.argv) != 2:
#         print('Correct your command :sudo python3 ping.py <ip_address>')
#         exit(1)
#
#     host_ip = sys.argv[1]
#
#     send_ping(host_ip)
#
#
#
# if __name__ == '__main__':
#     main()


import sys
import socket
import os
import struct
import time
import statistics as stats

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_CODE = 0
ICMP_ECHO_REPLY = 0
PACKET_SIZE = 64

local_host = '127.0.0.1'
timer_port = 3000

TIMER_ON = "ON"
TIMER_OFF = "OFF"

def checksum(data):
    sum = 0
    count_to = (len(data) // 2) * 2
    count = 0

    while count < count_to:
        this_val = data[count+1] * 256 + data[count]
        sum += this_val
        sum &= 0xffffffff
        count += 2

    if count_to < len(data):
        sum += data[len(data) - 1]
        sum &= 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    result = ~sum & 0xffff
    result = socket.htons(result)

    return result


def receive_ping(sock, count, host_ip):
    OK = False

    count_rece = 0
    start_time = time.time()
    try:
        recv_packet, addr = sock.recvfrom(PACKET_SIZE + 28)
        icmp_header = recv_packet[20:28]
        icmp_type, code, checksum, packet_id, sequence = struct.unpack(
            "bbHHh", icmp_header
        )

        finish_time = (time.time() - start_time) * 1000

        len_of_packet = len(recv_packet[20:])
        ip_addr = addr[0]
        ttl = recv_packet[8]
        if ip_addr == host_ip and packet_id == os.getgid():
            count_rece += 1

            if icmp_type == ICMP_ECHO_REPLY:
                OK = True
                print(f"{len_of_packet} bytes from {ip_addr}: icmp_seq={count} ttl={ttl} time={finish_time:.3f} ms")
    except:
        OK = False
        finish_time = 0

    return finish_time , OK

def send_ping(host_ip):
    times = []

    count_cmp = 0
    count = 0
    count_recev = 0
    s_time = time.time()

    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    timer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    timer_sock.connect((local_host, timer_port))

    sock.setblocking(False)
    timer_sock.setblocking(False)

    try:
        while True:
            count_cmp += 1
            packet = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, ICMP_ECHO_CODE, 0, 0, count_cmp)
            data = b"this is my massage"

            calc_checksum = checksum(packet + data)

            packet = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, ICMP_ECHO_CODE, calc_checksum, 0, count_cmp)


            to_send = packet + data
            if count == 0:
                print(f"PING {host_ip} ({host_ip}) {len(packet)}({len(data)}) bytes of data.")

            time.sleep(1)

            sock.sendto(to_send, (host_ip, 1))

            timer_sock.send(TIMER_ON.encode())

            answer = receive_ping(sock,  count_cmp , host_ip)

            if answer[1]:
                timer_sock.send(TIMER_OFF.encode())

            timer = ""
            try:
                timer = timer_sock.recv(1024).decode()
            except:
                pass

            if timer == "overtime":
                print(f"server {host_ip} cannot be reached")
                sock.close()
                timer_sock.close()
                exit(1)

            count += 1
            if answer[1]:
                count_recev += 1
                times.append(answer[0])

    except KeyboardInterrupt:
        f_time = time.time() - s_time

        print(f"\n--- {host_ip} ping statistics ---")
        print(f"{count} packets transmitted, {count_recev} received, {int((1 - (count_recev / count)) * 100)}% packet loss, time {int(f_time * 1000)}ms")
        if count_recev != 0:
            Min = min(times)
            avg = stats.mean(times)
            Max = max(times)
            differences = [abs(time - avg) for time in times]
            mdev = stats.mean(differences)
            print(f"rtt min/avg/max/mdev = {Min:.3f}/{avg:.3f}/{Max:.3f}/{mdev:.3f} ms")

        sock.close()
        timer_sock.close()


def main():
    if len(sys.argv) != 2:
        print('Correct your command :sudo python3 ping.py <ip_address>')
        exit(1)

    host_ip = sys.argv[1]

    send_ping(host_ip)



if __name__ == '__main__':
    main()
