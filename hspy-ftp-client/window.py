import tkinter
import navigation


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title('ftp-client')
        self.master.geometry('1280x720')
        self.master.resizable(0, 0)

        self.canvas = tkinter.Canvas(self.master, height=50)
        self.canvas.pack(fill='x')

        self.canvas.create_text(25, 20, text='Host:')
        self.host_entry = tkinter.Entry(self.master, width=20)
        self.host_entry.place(x=50, y=9)

        self.canvas.create_text(280, 20, text='Username:')
        self.user_entry = tkinter.Entry(self.master, width=15)
        self.user_entry.place(x=324, y=9)

        self.canvas.create_text(512, 20, text='Password:')
        self.passwd_entry = tkinter.Entry(self.master, show='*', width=20)
        self.passwd_entry.place(x=553, y=9)

        self.canvas.create_text(763, 20, text='Port:')
        self.port_entry = tkinter.Entry(self.master, width=5)
        self.port_entry.place(x=786, y=9)

        self.connect_button = tkinter.Button(
            self.master, text='Connect', command=self.connect)
        self.connect_button.place(x=865, y=5)

        self.status = tkinter.Label(self.master, font='TkFixedFont 11')
        self.status.pack()

        self.transfer_log = navigation.TransferLog(self.master)
        self.local_navigation = navigation.LocalNavigation(
            self.master, self.status, self.transfer_log)
        self.remote_navigation = navigation.RemoteNavigation(
            self.master, self.status, self.local_navigation, self.transfer_log)

    def connect(self):
        host = self.host_entry.get()
        if host == '':
            return

        try:
            port = int(self.port_entry.get())
        except ValueError:
            port = 21

        user = self.user_entry.get()
        passwd = self.passwd_entry.get()

        ftp_args = [host, port, user, passwd]
        self.remote_navigation.connect(ftp_args)
