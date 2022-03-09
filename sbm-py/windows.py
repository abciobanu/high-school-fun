from tkinter import Tk, Label, Button, Canvas, BOTH
from psutil import net_io_counters
from socket import gethostbyname, getfqdn
from sys import exit, platform
from urllib.request import urlopen

import graph


INTERNAL_IP = gethostbyname(getfqdn())
EXTERNAL_IP = urlopen('https://ident.me').read().decode('utf8')


class Main_window:
    def __init__(self, master):
        self.master = master

        if platform == "win32":
            master.iconbitmap('icon.ico')
        else:
            master.wm_iconbitmap(bitmap='@icon.xbm')

        master.title('sbm-py')
        master.geometry('256x256')
        master.resizable(0, 0)

        self.int_ip_label = Label(
            master, text='Internal IP:', font='TkDefaultFont 9 bold')
        self.int_ip_label.pack()

        self.int_ip = Label(master, text=INTERNAL_IP)
        self.int_ip.pack()

        self.ext_ip_label = Label(
            master, text='External IP:', font='TkDefaultFont 9 bold')
        self.ext_ip_label.pack(pady=(10, 0))

        self.ext_ip = Label(master, text=EXTERNAL_IP)
        self.ext_ip.pack()

        self.recv_label = Label(master, text='Receive:',
                                font='TkDefaultFont 9 bold')
        self.recv_label.pack(pady=(10, 0))

        self.recv_speed = Label(master, text='0 MB/s')
        self.recv_speed.pack()

        self.send_label = Label(master, text='Send:',
                                font='TkDefaultFont 9 bold')
        self.send_label.pack(pady=(10, 0))

        self.send_speed = Label(master, text='0 MB/s')
        self.send_speed.pack()

        self.recv_speed_list = []
        self.send_speed_list = []

        self.graphs = Button(master, text='Graphs',
                             command=self.create_graphs_window)
        self.graphs.pack(pady=(20, 0))

        self.master.bind('<Destroy>', lambda event: exit())

    def update_speed(self, recv_speed, send_speed):
        recv_speed = recv_speed / 1024. / 1024.
        recv_speed = round(recv_speed, 2)
        self.recv_speed.configure(text=str(recv_speed) + ' MB/s')

        if len(self.recv_speed_list) == 60:
            for i in range(0, 59):
                self.recv_speed_list[i] = self.recv_speed_list[i + 1]
            self.recv_speed_list[59] = recv_speed
        else:
            self.recv_speed_list.append(recv_speed)

        send_speed = send_speed / 1024. / 1024.
        send_speed = round(send_speed, 2)
        self.send_speed.configure(text=str(send_speed) + ' MB/s')

        if len(self.send_speed_list) == 60:
            for i in range(0, 59):
                self.send_speed_list[i] = self.send_speed_list[i + 1]
            self.send_speed_list[59] = send_speed
        else:
            self.send_speed_list.append(send_speed)

    def get_stats(self, recv=net_io_counters().bytes_recv, send=net_io_counters().bytes_sent):
        new_recv = net_io_counters().bytes_recv
        new_send = net_io_counters().bytes_sent

        self.update_speed(new_recv - recv, new_send - send)

        self.master.after(1000, lambda: self.get_stats(new_recv, new_send))

    def create_graphs_window(self):
        g_root = Tk()
        graphs_window = Graphs_window(
            g_root, self.recv_speed_list, self.send_speed_list)

        graphs_window.update()

        g_root.mainloop()


class Graphs_window:
    def __init__(self, master, recv_list, send_list):
        self.master = master

        if platform == "win32":
            master.iconbitmap('icon.ico')
        else:
            master.wm_iconbitmap(bitmap='@icon.xbm')

        master.title('sbm-py - Graphs')
        master.geometry('1024x832')
        master.resizable(0, 0)

        self.canvas = Canvas(self.master)
        self.canvas.pack(fill=BOTH, expand=1)

        self.create_separation_line()

        self.recv_list = recv_list
        self.send_list = send_list

        self.recv_graph = None
        self.send_graph = None

        self.draw_graphs()

        self.last_update = None
        self.master.bind(
            '<Destroy>', lambda event: self.master.after_cancel(self.last_update))

    def create_separation_line(self):
        x1 = 0
        y1 = self.master.winfo_height() / 2
        x2 = self.master.winfo_width()
        y2 = self.master.winfo_height() / 2
        line_width = 2

        self.canvas.create_line(x1, y1, x2, y2, width=line_width)
        self.canvas.update()

    def update(self):
        self.canvas.delete('graph_line', 'current_speed')

        self.recv_graph.update_points()
        self.send_graph.update_points()

        self.last_update = self.master.after(1000, self.update)

    def draw_graphs(self):
        master = self.master
        canvas = self.canvas

        x_left = 60
        y_down = master.winfo_height() / 2 - 25
        x_right = master.winfo_width() - 60
        y_up = 5

        self.recv_graph = graph.Graph(
            master, canvas, x_left, y_down, x_right, y_up, self.recv_list, 'red', 'RECEIVE')

        y_down = master.winfo_height() - 25
        y_up = master.winfo_height() / 2 + 5

        self.send_graph = graph.Graph(
            master, canvas, x_left, y_down, x_right, y_up, self.send_list, 'green', 'SEND')
