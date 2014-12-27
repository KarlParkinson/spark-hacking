# A python server that a Spark Core can communicate with. Inspired by the ruby and js servers here: https://github.com/spark/local-communication-example

import re
import socket
import sys

def help():
    print("Commands: <pin number><state>")
    print("      eg: 7h set pin D7 to high")
    print("      eg: 0l set pin D0 to low")
    print("          x  Exit")

def handleInput(inp, conn):
    if (re.match(r'^[0-7][lh]$', inp)):
        conn.sendall(bytes(inp.lower(), "ascii"))
    elif (inp == 'x'):
        conn.close()
        sys.exit()
    else:
        help()

def main():
    port = 9000
    ipAddress = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
    print("Listening on port " + str(port) + " at IP address " + ipAddress)
    print("In another window run curl https://api.spark.io/v1/devices/<DEVICE_ID>/connect -d access_token=<ACCESS_TOKEN> -d ip=" + ipAddress)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ipAddress, port))
    s.listen(1)
    conn, sparkAddr = s.accept()
    print("Connected from " + sparkAddr[0] + ":" + str(sparkAddr[1]))
    while True:
        print('>> ', end="")
        command = input()
        handleInput(command.rstrip(), conn)


if __name__ == "__main__":
    main()
    
