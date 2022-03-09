from tkinter import Canvas, Label


class Graph:
    def __init__(self, master, canvas, x_left, y_down, x_right, y_up, points_list, line_color, description):
        self.master = master
        self.canvas = canvas

        self.line_color = line_color
        self.description = description

        self.x_left = x_left
        self.y_down = y_down
        self.x_right = x_right
        self.y_up = y_up

        # x axis
        self.canvas.create_line(x_left, y_down, x_right, y_down)

        # y axis
        self.canvas.create_line(x_left, y_down, x_left, y_up)

        self.origin_label = Label(self.master, text='0')
        self.origin_label.place(x=x_left - 6, y=y_down + 1)

        self.xaxis_labels = [
            ('15', x_left + (x_right - x_left) / 4 - 5),
            ('30', x_left + (x_right - x_left) / 2 - 1),
            ('45', x_left + 3 * (x_right - x_left) / 4 + 1),
            ('59 seconds', x_right - 9)
        ]
        for label in self.xaxis_labels:
            Label(self.master, text=label[0]).place(x=label[1], y=y_down + 1)

        self.create_description_label()

        self.points_list = points_list
        self.lines = []

        self.current_speed = None

    def create_description_label(self):
        x = self.x_left + (self.x_right - self.x_left) / 2
        y = self.y_down - (self.y_down - self.y_up) / 2
        desc_font = 'TkDefaultFont 24 bold'
        desc_color = 'light gray'

        self.canvas.create_text(
            x, y, text=self.description, font=desc_font, fill=desc_color)

    def update_points(self):
        x_division = (self.x_right - self.x_left) / 59
        y_division = (self.y_down - self.y_up) / 125

        for i in range(len(self.points_list) - 1, 0, -1):
            x1 = self.x_left + x_division * (len(self.points_list) - 1 - i)
            y1 = self.y_down - y_division * self.points_list[i]
            x2 = self.x_left + x_division * (len(self.points_list) - 1 - i + 1)
            y2 = self.y_down - y_division * self.points_list[i - 1]

            self.canvas.create_line(
                x1, y1, x2, y2, width=2, fill=self.line_color, tags='graph_line')

        speed_x = self.x_left - 30
        speed_y = self.y_down - y_division * self.points_list[-1]
        speed_text = str(self.points_list[-1]) + ' MB/s'
        speed_font = 'TkDefaultFont 7 bold'

        self.canvas.create_text(
            speed_x, speed_y, text=speed_text, font=speed_font, tags='current_speed')
