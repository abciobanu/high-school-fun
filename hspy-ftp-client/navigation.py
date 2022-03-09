import tkinter
import os
from pathlib import Path
from ftplib import FTP


def get_formatted_size(size):
    for unit in ['B', 'K', 'M', 'G', 'T', 'P']:
        if size < 1024:
            return f'{size:.2f}{unit}'
        size /= 1024


class LocalNavigation:
    def __init__(self, master, status_out, transfer_log):
        self.master = master
        self.status = status_out
        self.transfer_log = transfer_log

        self.frame = tkinter.Frame(self.master)
        self.frame.pack(side='left', anchor='n', padx=(10, 0), pady=(50, 0))

        self.subframe = tkinter.Frame(self.frame)
        self.subframe.pack(side='bottom')

        self.current_path = tkinter.Label(self.frame, font='TkFixedFont 9')
        self.current_path.pack(side='top', anchor='w')

        self.dir_box = tkinter.Listbox(
            self.subframe, width=75, height=15, selectmode='single', font='TkFixedFont')
        self.dir_box.pack(side='left')

        self.scrollbar = tkinter.Scrollbar(self.subframe)
        self.scrollbar.pack(side='right', fill='both')

        self.dir_box.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.dir_box.yview)

        self.show_hidden = False
        self.hide_button = tkinter.Button(
            self.master, text='Show hidden files', command=self.button_click)
        self.hide_button.place(x=10, y=425)

        self.listing = []

        os.chdir(str(Path.home()))
        self.update_directory()

        self.dir_box.bind('<Double-1>', lambda event: self.access_file())

        self.remote_navigation = None

    def update_directory(self):
        self.listing.clear()
        self.dir_box.delete(0, 'end')

        self.dir_box.insert('end', '..')
        self.listing.append(['..', '-'])

        for _, directories, files in os.walk('.'):
            if not self.show_hidden:
                directories = [d for d in directories if d[0] != '.']
                files = [f for f in files if f[0] != '.']

            directories.sort()
            files.sort()

            for name in directories:
                if len(name) > 60:
                    name = name[:58] + '...'
                text = f"{name:65}-"

                self.listing.append([name, '-'])
                self.dir_box.insert('end', text)

            for name in files:
                size = get_formatted_size(os.path.getsize(name))

                if len(name) > 60:
                    name = name[:58] + '...'
                text = f"{name:65}{size}"

                self.listing.append([name, size])
                self.dir_box.insert('end', text)

            break

        self.current_path.configure(text='LOCAL: ' + os.getcwd())

    def button_click(self):
        if self.show_hidden:
            self.hide_button.configure(underline=-1)
            self.show_hidden = False
        else:
            self.hide_button.configure(underline=0)
            self.show_hidden = True

        self.update_directory()

    def access_file(self):
        if self.dir_box.curselection():
            selection = self.dir_box.curselection()[0]
            if self.listing[selection][1] == '-':
                os.chdir(self.listing[selection][0])
                self.update_directory()
            elif self.remote_navigation.ftp is not None:
                self.remote_navigation.store_file(self.listing[selection][0])
            else:
                self.status.configure(
                    text='You are not connected to a server!')


class RemoteNavigation:
    def __init__(self, master, status_out, local_navigation, transfer_log):
        self.master = master
        self.status = status_out
        self.local_navigation = local_navigation
        self.transfer_log = transfer_log

        self.frame = tkinter.Frame(self.master)
        self.frame.pack(side='right', anchor='n', padx=(0, 10), pady=(50, 0))

        self.subframe = tkinter.Frame(self.frame)
        self.subframe.pack(side='bottom')

        self.current_path = tkinter.Label(self.frame, font='TkFixedFont 9')
        self.current_path.pack(side='top', anchor='w')

        self.dir_box = tkinter.Listbox(
            self.subframe, width=75, height=15, selectmode='single', font='TkFixedFont')
        self.dir_box.pack(side='left')

        self.scrollbar = tkinter.Scrollbar(self.subframe)
        self.scrollbar.pack(side='right', fill='both')

        self.dir_box.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.dir_box.yview)

        self.ftp = None
        self.listing = []

        self.local_navigation.remote_navigation = self

    def connect(self, args):
        host = args[0]
        port = args[1]
        user = args[2]
        passwd = args[3]

        self.status.configure(text='Connecting...')
        self.status.update()

        try:
            self.ftp = FTP()
            self.ftp.connect(host, port)
            self.ftp.login(user, passwd)

            self.status.configure(text='Connected.')
            self.status.update()
        except Exception as e:
            self.ftp = None
            self.status.configure(text=e)
            return

        self.cut_button = tkinter.Button(
            self.master, text='Cut', width=7, command=self.cut_click)
        self.cut_button.place(x=653, y=425)

        self.paste_button = tkinter.Button(
            self.master, text='Paste', width=7, command=self.paste_click)
        self.paste_button.place(x=753, y=425)

        self.delete_button = tkinter.Button(
            self.master, text='Delete', width=7, command=self.delete_click)
        self.delete_button.place(x=853, y=425)

        self.rename_button = tkinter.Button(
            self.master, text='Rename', width=7, command=self.rename_click)
        self.rename_button.place(x=953, y=425)

        self.rename_entry = tkinter.Entry(
            self.master, width=25, state='disabled')
        self.rename_entry.place(x=1050, y=430)

        self.cut_source_path = ''
        self.cut_filename = ''

        self.dir_box.configure(state='normal')

        self.transfer_log.log_connection(host)
        self.update_directory()
        self.dir_box.bind('<Double-1>', lambda event: self.access_file())

    def update_directory(self):
        self.status.configure(text='')

        self.listing.clear()
        self.dir_box.delete(0, 'end')

        self.listing.append(['..', '-'])
        self.dir_box.insert('end', '..')

        files = []
        try:
            files = self.ftp.nlst()
        except Exception as e:
            self.status.configure(text=e)

        dirs_i = 1
        for file_name in files:
            file_size = '-'
            try:
                self.ftp.cwd(file_name)
                self.ftp.cwd('..')
            except:
                self.ftp.voidcmd('TYPE I')
                try:
                    file_size = get_formatted_size(self.ftp.size(file_name))
                except Exception as e:
                    self.status.configure(text=e)
                    continue

            text = f"{file_name:65}{file_size}"
            if file_size == '-':
                self.listing.insert(dirs_i, [file_name, file_size])
                self.dir_box.insert(dirs_i, text)
                dirs_i += 1
            else:
                self.listing.append([file_name, file_size])
                self.dir_box.insert('end', text)

        self.current_path.configure(text='REMOTE: ' + self.ftp.pwd())

    def retrieve_file(self, file_name):
        try:
            self.ftp.retrbinary('RETR ' + file_name,
                                open(file_name, 'wb').write)

            local_path = os.getcwd()
            if local_path == '/':
                local_path += file_name
            else:
                local_path += '/' + file_name

            remote_path = self.ftp.pwd()
            if remote_path == '/':
                remote_path += file_name
            else:
                remote_path += '/' + file_name

            direction = 'retrieve'

            file_size = '-'
            for name, size in self.listing:
                if name == file_name:
                    file_size = size

            self.transfer_log.log(local_path, remote_path,
                                  direction, file_size)

            self.local_navigation.update_directory()
            self.status.configure(
                text='The file has been downloaded successfully!')
        except Exception as e:
            os.remove(file_name)
            self.status.configure(text=e)

    def access_file(self):
        if self.dir_box.curselection():
            selection = self.dir_box.curselection()[0]
            if self.listing[selection][1] == '-':
                try:
                    self.ftp.cwd(self.listing[selection][0])
                    self.update_directory()
                except Exception as e:
                    self.status.configure(text=e)
                    return
            else:
                self.retrieve_file(self.listing[selection][0])

    def store_file(self, file_name):
        try:
            self.ftp.storbinary('STOR ' + file_name, open(file_name, 'rb'))

            local_path = os.getcwd()
            if local_path == '/':
                local_path += file_name
            else:
                local_path += '/' + file_name

            remote_path = self.ftp.pwd()
            if remote_path == '/':
                remote_path += file_name
            else:
                remote_path += '/' + file_name

            direction = 'store'

            file_size = '-'
            for name, size in self.local_navigation.listing:
                if name == file_name:
                    file_size = size

            self.transfer_log.log(local_path, remote_path,
                                  direction, file_size)

            self.update_directory()
            self.status.configure(
                text='The file has been uploaded successfully!')
        except Exception as e:
            self.status.configure(text=e)

    def cut_click(self):
        if self.dir_box.curselection():
            selection = self.dir_box.curselection()[0]
            if self.listing[selection][1] == '-':
                pass
            else:
                self.cut_source_path = self.ftp.pwd()
                self.cut_filename = self.listing[selection][0]

    def paste_click(self):
        if self.ftp.pwd() == self.cut_source_path:
            self.cut_source_path = ''
            self.cut_filename = ''
        elif self.cut_source_path == '':
            pass
        else:
            if self.cut_source_path == '/':
                self.cut_source_path += self.cut_filename
            else:
                self.cut_source_path += '/' + self.cut_filename

            try:
                self.ftp.rename(self.cut_filename, self.cut_source_path)
                self.status.configure(
                    text='The file has been moved successfully!')
            except Exception as e:
                self.status.configure(text=e)

            self.cut_source_path = ''
            self.cut_filename = ''

    def delete_click(self):
        if self.dir_box.curselection():
            selection = self.dir_box.curselection()[0]
            if self.listing[selection][1] == '-':
                pass
            else:
                try:
                    self.ftp.delete(self.listing[selection][0])
                    self.status.configure(
                        text='The file has been deleted successfully!')
                except Exception as e:
                    self.status.configure(text=e)

    def rename_click(self):
        if self.dir_box.curselection():
            selection = self.dir_box.curselection()[0]
            if self.listing[selection][1] == '-':
                pass
            else:
                if self.rename_entry['state'] == 'disabled':
                    self.rename_entry.configure(state='normal')
                    self.dir_box.configure(state='disabled')
                else:
                    new_filename = self.rename_entry.get()

                    self.rename_entry.delete(0, 'end')
                    self.rename_entry.configure(state='disabled')
                    self.dir_box.configure(state='normal')

                    if len(new_filename) > 0:
                        try:
                            self.ftp.rename(
                                self.listing[selection][0], new_filename)
                            self.update_directory()
                            self.status.configure(
                                text='The file has been renamed successfully!')
                        except Exception as e:
                            self.status.configure(text=e)
                            return


class TransferLog:
    def __init__(self, master):
        self.master = master

        self.frame = tkinter.Frame(self.master)
        self.frame.pack(side='bottom', pady=(0, 10))

        self.log_box = tkinter.Listbox(
            self.frame, width=155, height=12, selectmode='single', font='TkFixedFont')
        self.log_box.grid(row=0, column=0)

        self.yscrollbar = tkinter.Scrollbar(self.frame)
        self.yscrollbar.grid(row=0, column=1, sticky='ns')

        self.log_box.configure(yscrollcommand=self.yscrollbar.set)
        self.yscrollbar.configure(command=self.log_box.yview)

        self.xscrollbar = tkinter.Scrollbar(self.frame, orient='horizontal')
        self.xscrollbar.grid(row=1, sticky='we')

        self.log_box.configure(xscrollcommand=self.xscrollbar.set)
        self.xscrollbar.configure(command=self.log_box.xview)

        self.directions = {
            'retrieve': '<--',
            'store': '-->'
        }

        self.data = []

    def log_connection(self, host):
        if self.log_box.size() > 0:
            self.log_box.insert('end', '')
        self.log_box.insert('end', host + ':')

    def log(self, local_path, remote_path, direction, size):
        self.data.append([local_path, remote_path, direction, size])
        self.log_box.insert(
            'end', f'{local_path} {self.directions[direction]} {remote_path} {size}')
