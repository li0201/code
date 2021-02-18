# 导入socket包
import socket, threading, datetime
import tkinter as tk
from tkinter.messagebox import *
# import win32api,win32con
# 创建一个socket对象
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# 获取本地ip
host = ""
final = 0
names={}
filename = 'data.txt'
# 给定端口
port = 45543
 
# 给服务器IP和端口
server.bind((host, port))
 
# 最大连接数
server.listen(10)
 
print('输入enter退出服务器')

# 创建一个客户端列表
clients = list()
# 存放已经创建线程的客户端
end = list()
 
 
# 阻塞式等待客户端连接，返回连接对象，与间接对象地址
def accept():
 
    while True:
        client, addr = server.accept()
        clients.append(client)
        name=client.recv(1024).decode('utf-8')
        names[client]=name
        with open(filename,'a') as w:
            w.write('-----'+f'服务器被{name}连接: 当前连接数：-----{len(clients)}'+'-'*5+'\n')
        print('\r'+'-'*5+f'服务器被{name}连接: 当前连接数：-----{len(clients)}'+'-'*5+'\n', end='')
        root=tk.Tk()
        root.withdraw()
        # tk.messagebox.showinfo('上线提醒',f'{name}上线了')
        root.destroy()
        # win32api.MessageBox(0, f'{name}上线了', "提醒",win32con.MB_OK)

def recv_data(client):
    while True:
        if final == 1:
            break
        # 接受来自客户端的信息
        # cur = datetime.datetime.now().strftime('%F %T')
        try:
            indata = client.recv(1024)
        except Exception as e:
            outname=names[client]
            sum=len(clients)-1
            with open(filename,'a') as w:
                w.write('-' * 5 + f'服务器被{outname}断开: 当前连接数：-----{sum}' + '-' * 5+'\n')                
            print('\r' + '-' * 5 + f'服务器被{outname}断开: 当前连接数：-----{sum}' + '-' * 5+'\n', end='')
            root=tk.Tk()
            root.withdraw()
            # tk.messagebox.showinfo('下线提醒',f'{outname}下线了')
            root.destroy()
            # win32api.MessageBox(0, f'{outname}下线了', "提醒",win32con.MB_OK)
            del names[client]
            end.remove(client)
            clients.remove(client)
            break
        indat=indata.decode('utf-8')
        if indat=='list':
            for i in names:
                client.send(names[i].encode('utf-8'))
            continue
        with open(filename,'a') as f:
            f.write(f'{indat}\n')
        print(indat)
        for clien in clients:
            # 转发来自客户端的信息，发给其他客户端
            if clien != client:
                clien.send(indata)
 
def outdatas():
    while True:
        # 输入要给客户端的信息
        # print('')
        cur = datetime.datetime.now().strftime('%F %T')
        cur = datetime.datetime.now().strftime('%F %T')
        outdata = input('')
        # print()
        if outdata=='enter':
            global final
            final = 1
            break
        if outdata=='list':
            list(names)
            continue
        print(cur)
        print('服务器:%s'% outdata)
        with open(filename,'a') as w:
            w.write(f"{cur}\n服务器:{outdata}\n")
        # 给每个客户端发信息
        for client in clients:
            client.send(f"{cur}\n服务器:{outdata}".encode('utf-8)'))
 
def list(w):
    for i in w:
        print(w[i])
 
def indatas():
    while True:
        # 循环出连接的客户端，并创建相应线程
        if final == 1:
            break
        for clien in clients:
            # 若是线程已经存在则跳过
            if clien in end:
                continue
            index = threading.Thread(target = recv_data,args = (clien,))
            index.start()
            end.append(clien)
 
def main():
    t1 = threading.Thread(target = indatas, name = 'input')
    t1.start()
    t2 = threading.Thread(target = outdatas, name = 'out')
    t2.start()
    t3 = threading.Thread(target = accept, name = 'accept')
    t3.daemon = True
    t3.start()
    while True:
        if final == 1:
            t2.join()
            for client in clients:
                client.close()
            print('-'*5+'服务器断开连接'+'-'*5)
            exit(0)
if __name__ == "__main__":
    main()