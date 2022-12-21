from tkinter import *
from tkinter import messagebox
import time

tk = Tk()
app_running = True

size_canvas_x = 600
size_canvas_y = 600
s_x = s_y = 10  # game size field
step_x = size_canvas_x // s_x  # horizontal step
step_y = size_canvas_y // s_y  # vertical step
size_canvas_x = step_x * s_x
size_canvas_y = step_y * s_y

menu_x = 250


def on_closing():
    global app_running
    if messagebox.askokcancel('Exit', 'Are u sure?'):
        app_running = False
        tk.destroy()


tk.protocol('WM_DELETE_WINDOW', on_closing)
tk.title('BATTLE SEA')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
canvas = Canvas(tk, width=size_canvas_x + menu_x, height=size_canvas_y, bd=0, highlightthickness=0)
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill='white')
canvas.pack()
tk.update()


def draw_table():
    for i in range(0, s_x + 1):
        canvas.create_line(step_x * i, 0, step_x * i, size_canvas_y)
    for i in range(0, s_y + 1):
        canvas.create_line(0, step_y * i, size_canvas_x, step_y * i)


draw_table()


def button_show_enemy():
    pass


def button_begin_again():
    pass


b0 = Button(tk, text='Show enemy ships', command=button_show_enemy)
b0.place(x=size_canvas_x + 20, y=30)

b1 = Button(tk, text='Restart game', command=button_begin_again)
b1.place(x=size_canvas_x + 20, y=70)

while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)
