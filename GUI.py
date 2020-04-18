import socket, threading, datetime
from tkinter import *
# 创建客户端对象
def outdatas(*args):
    #while True:
        # 输入要发给服务器的信息
    outdata = (Input.get('1.0', END)).replace('\n', '').replace('\r', '')
    cur=datetime.datetime.now().strftime('%F %T')
    cur=datetime.datetime.now().strftime('%F %T')
    # print()
    if outdata=='enter':
        Output.insert(END, '已离线')
        Output.yview_moveto(1)
        client.send(f'{cur}\n{name}下线了'.encode('utf-8'))
        root.destroy()
        return
    if outdata=='list':
        client.send(outdata.encode('utf-8'))
        Input.delete('1.0', END)
        return
    # 发送给服务器
    client.send(f'{cur}\n{name}:{outdata}'.encode('utf-8'))
    Output.insert(END, f'{cur}\n')
    Output.insert(END, '%s:%s\n'% (name, outdata))
    Output.yview_moveto(1)
    Input.delete('1.0', END)
def indatas():
    while True:
        # 接受来自服务器的信息
        indata = client.recv(1024).decode('utf-8')
        # print(indata.decode('utf-8'))
        Output.insert(END, f'{indata}\n')
        Output.yview_moveto(1)
def conti(*args):
    global host
    host=h.get()
    global name
    name=n.get()
    # print(type(host))
    if not name:
        messagebox.showerror('Name type error', message='用户名不能为空')
    else:
        #host='39.67.75.130'
        window.destroy()
        #print(host)
window=Tk()
window.title('登录')
sw = window.winfo_screenwidth()
sh = window.winfo_screenheight()
window.geometry('+{}+{}'.format((sw-430)//2, (sh-340)//2))
window['height'] = 110
window['width'] = 270
window.resizable(0, 0)
h=StringVar()
n=StringVar()
Label(window,text='输入目标ip:').place(x=20, y=10, width=100, height=20)
Entry1=Entry(window,textvariable=h).place(x=120, y=10, width=130, height=20)
Label(window,text='输入个人昵称:').place(x=30, y=40, width=80, height=20)
Entry2=Entry(window,textvariable=n).place(x=120, y=40, width=130, height=20)
Button(window,text='确定',command=conti).place(x=100, y=70, width=70, height=30)
window.bind('<Return>', conti)
window.mainloop()
root=Tk()
root.title('聊天室')
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
root.geometry('+{}+{}'.format((sw-430)//2, (sh-340)//2))
ww=root.winfo_width()
wh=root.winfo_height()
# root.resizable(0, 0)
#alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
frameT = Frame(root, width=460, height=320)
frameB = Frame(root, width=460, height=80)
frameT.pack(expand='yes', fill='both')
frameB.pack(expand='yes', fill='both')
Input = Text(frameB, height=6,font=('微软雅黑', 12, 'normal'))
Output = Text(frameT,font=('微软雅黑', 12, 'normal'))
Input.pack(expand='yes', fill='both')
Output.pack(expand='yes', fill='both')
btnFrame = Frame(frameB, height=24, background='White')
btnFrame.pack(expand='yes', fill='both')
Button(btnFrame, text='发送', width=8, bg='DodgerBlue', fg='White', command=outdatas).pack(side=RIGHT)
root.bind('<Return>', outdatas)
# 目标主机
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 目标端口
port = 45543
# 连接客户端
#host='39.67.75.130'
#name='li0201'
client.connect((host, port))
client.send(f'{name}'.encode('utf-8'))
Output.insert(END, '-'*5+'已连接到服务器'+'-'*5+'\n')
Output.insert(END, '-'*5+'输入enter关闭与服务器的连接'+'-'*5+'\n')
Output.yview_moveto(1)
cur=datetime.datetime.now().strftime('%F %T')
client.send(f'{cur}\n{name}上线了'.encode('utf-8'))
# 建立多线程
# 建立接受信息，线程对象
t1 = threading.Thread(target=indatas, name='input')
t1.daemon = True
# 建立输出信息，线程对象
# t2 = threading.Thread(target=outdatas, name='out')
# 启动多线程
t1.start()
# t2.start()
# 阻塞线程，直到子线程执行结束，主线程才能结束。
# t1.join()
# t2.join()
# 关闭连接
# Output.insert(END, '-'*5+'服务器断开连接'+'-'*5)
# client.close()
# root.protocol("WM_DELETE_WINDOW", onClosing)
root.mainloop()
client.close()