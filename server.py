import socket,threading
from request import server

# settings

HOST = '192.168.155.1'
PORT = 8000
File_Dir = 'files'

def solve(conn,addr):
    sv = server()
    sv.File_Dir = File_Dir
    try:
        conn.settimeout(500)
        sv.read(str(conn.recv(1024), 'gbk'))
    except socket.timeout:
        print ('time out')
    except:
        print('连接出错')
    else:
        print('Connect by: ', addr)
        print('Request is:\n', sv)
        conn.sendall(sv.response())
    conn.close()

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(100)
    # infinite loop
    while True:
        conn, addr = sock.accept()
        thread = threading.Thread(target=solve, args=(conn, addr))
        solve(conn,addr)