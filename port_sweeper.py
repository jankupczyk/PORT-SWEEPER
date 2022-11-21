from tracemalloc import start
from pyfiglet import Figlet
from datetime import datetime
import threading
import socket
import sys
import os
import time
import subprocess


def generalFont(gfont):print("\033[95m {}\033[00m" .format(gfont))
def yellow(general_yell):print("\033[93m {}\033[00m" .format(general_yell))
def green(general_green):print("\033[92m {}\033[00m" .format(general_green))
def err_msg(general_err):print("\033[91m {}\033[00m" .format(general_err))


mmx_ports_to_use=1
min_ports_to_use=0
max_ports_to_use=65535
open_ports = []


def scan_ports(thread_name, ps_start_port_input, max_port):
    try:
        for port in range(ps_start_port_input, max_port):
            if (port - 1) == max_port - 1:
                print(thread_name, "currently is busy!")
            socketRaddr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = socketRaddr.connect_ex((ps_ip_input, port))
            if result == 0:
                print("\n\033[92mPORT_SWEEPER Thread_{} found open port at ${}\033[00m".format(i, port))
                open_ports.append(port)
            socketRaddr.close()
    except KeyboardInterrupt:
        err_msg("ERROR:: Keyboard interrupt")
        sys.exit()
    except ConnectionError:
        err_msg("ERROR:: Connection error")
        sys.exit()
    except socket.gaierror:
        err_msg("ERROR:: Hostname could not be resolved")
        sys.exit()
    except socket.error:
        err_msg("ERROR:: Could not connect to server")
        sys.exit()


if __name__ == '__main__':
    banner = Figlet(font='slant')
    err_msg(banner.renderText('PORT_SWEEPER'))
    err_msg("PORT_SWEEPER is a script used to determine which ports are open and which are not in a specific IP address.")
    err_msg("Be aware that the program is in its alpha version, so there may be bugs!")
    err_msg("DISCLAIMER: Remember that you use the script at your own risk, the author of script is not responsible for any potential damage and will not be liable!\n")

    ps_ip_input = input('Provide IP: ')
    print("\033[92mPORT_SWEEPER will start listening at remote host {} \033[00m".format(ps_ip_input))
    ps_start_port_input = int(input('Provide start port: '))
    if min_ports_to_use <= ps_start_port_input <= max_ports_to_use:
        ps_start_port_input = ps_start_port_input
        print("\033[92mPORT_SWEEPER will start sweeping at port {} \033[00m".format(ps_start_port_input))
    else:
        err_msg("ERROR:: Could not find port")
        sys.exit()
    ps_end_port_input = int(input('Provide end port: '))
    if mmx_ports_to_use <= ps_end_port_input <= max_ports_to_use:
        ps_end_port_input = ps_end_port_input
        print("\033[92mPORT_SWEEPER will end sweeping at port {} \033[00m".format(ps_end_port_input))
    else:
        err_msg("ERROR:: Could not find port")
        sys.exit()
    thread_count = int(input('Provide amount of threads: '))
    print("\033[92mPORT_SWEEPER will dirtibute tasks for {} threads\033[00m\n".format(thread_count))

    threads = []

    i = 0
    next_max = ps_start_port_input
    min_port = ps_start_port_input
    while i < thread_count:
        i += 1
        next_max += ((ps_end_port_input - ps_start_port_input) // thread_count)
        if i == thread_count:
            next_max = ps_end_port_input
        generalFont("Thread_{} sheduled {} tasks - from port {} to port {}".format(i, next_max-min_port, min_port, next_max))
        threads.append(threading.Thread(target=scan_ports, args=("Thread{}".format(i), min_port, next_max)))
        min_port = next_max

    print("\n\nScanning for open ports in {}:{}-{}".format(ps_ip_input, ps_start_port_input, ps_end_port_input))
    print("Time started: " + str(datetime.now()))
    print("Please standby...")
    print("*" * 80)

    for var in threads:
        var.start()

    for var in threads:
        var.join()

    if len(open_ports) == 0:
        print("\nSCANNING SUMMARY: "+str(datetime.now()))
        print("#" * 80)
        print("\033[91mUnfortunately there is no open ports in {}:{}-{}\033[00m".format(ps_ip_input, ps_start_port_input, ps_end_port_input))
        print("#" * 80)
    else:
        print("\nSCANNING SUMMARY: "+str(datetime.now()))
        print("#" * 80)
        for port in open_ports:
            print("\033[92m {} \033[00m".format(port))
        print("#" * 80)

    input("\n\nPress RETURN to exit...")
    
    