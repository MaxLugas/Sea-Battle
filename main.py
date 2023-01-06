from tkinter import *
from tkinter import messagebox
import time, random

tk = Tk()
app_running = True

size_canvas_x = size_canvas_y = 400
s_x = s_y = 10  # game size field
step_x = size_canvas_x // s_x  # horizontal step
step_y = size_canvas_y // s_y  # vertical step
size_canvas_x = step_x * s_x
size_canvas_y = step_y * s_y
menu_x = 250
ships = s_x // 2  # maximum number of ships
ship_len_1 = s_x // 5  # length of the first type of ship
ship_len_2 = s_x // 3  # length of the second type of ship
ship_len_3 = s_x // 2  # length of the third type of ship
enemy_ships = [[0 for i in range(s_y + 1)] for i in range(s_x + 1)]
list_ids = []  # list objects canvas
points = [[-1 for i in range(s_y)] for i in range(s_x)]  # push button list
boom = [[0 for i in range(s_y)] for i in range(s_x)]  # hit list


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
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships[j][i] > 0:
                color = 'red'
                if points[j][i] != -1:
                    color = 'green'
                _id = canvas.create_rectangle(i * step_x, j * step_y, i * step_x + step_x, j * step_y + step_y,
                                              fill=color)
                list_ids.append(_id)


def button_begin_again():
    global list_ids
    global points
    global boom
    for el in list_ids:
        canvas.delete(el)
    list_ids = []
    generate_enemy_ships()
    points = [[-1 for i in range(s_y)] for i in range(s_x)]
    boom = [[0 for i in range(s_y)] for i in range(s_x)]


b0 = Button(tk, text='Show enemy ships', command=button_show_enemy)
b0.place(x=size_canvas_x + 20, y=30)

b1 = Button(tk, text='Restart game', command=button_begin_again)
b1.place(x=size_canvas_x + 20, y=70)


def draw_point(x, y):
    if enemy_ships[y][x] == 0:
        color = "red"
        id1 = canvas.create_oval(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y, fill=color)
        id2 = canvas.create_oval(x * step_x + step_x // 3, y * step_y + step_y // 3, x * step_x + step_x - step_x // 3,
                                 y * step_y + step_y - step_y // 3, fill="white")
        list_ids.append(id1)
        list_ids.append(id2)
    if enemy_ships[y][x] > 0:
        color = "black"
        id1 = canvas.create_rectangle(x * step_x, y * step_y + step_y // 2 - step_y // 10, x * step_x + step_x,
                                      y * step_y + step_y // 2 + step_y // 10, fill=color)
        id2 = canvas.create_rectangle(x * step_x + step_x // 2 - step_x // 10, y * step_y,
                                      x * step_x + step_x // 2 + step_x // 10, y * step_y + step_y, fill=color)
        list_ids.append(id1)
        list_ids.append(id2)


def check_winner(x, y):
    win = False
    if enemy_ships[y][x] > 0:
        boom[y][x] = enemy_ships[y][x]
    sum_enemy_ships = sum(sum(i) for i in zip(*enemy_ships))
    sum_boom = sum(sum(i) for i in zip(*boom))
    if sum_enemy_ships == sum_boom:
        win = True
    return win


def check_winner2():
    win = True
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships[j][i] > 0:
                if points[j][i] == -1:
                    win = False
    return win


def add_to_all(event):
    global points
    _type = 0  # left mouse button
    if event.num == 3:
        _type = 1  # right mouse button
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    ip_x = mouse_x // step_x
    ip_y = mouse_y // step_y
    if ip_x < s_x and ip_y < s_y:
        if points[ip_y][ip_x] == -1:
            points[ip_y][ip_x] = _type
            draw_point(ip_x, ip_y)
            if check_winner(ip_x, ip_y):
                print("You're winner!!")
                points = [[10 for i in range(s_y)] for i in range(s_x)]
        print(len(list_ids))


canvas.bind_all('<Button-1>', add_to_all)  # left mouse button
canvas.bind_all('<Button-3>', add_to_all)  # right mouse button


def generate_enemy_ships():
    global enemy_ships
    ships_list = []
    for i in range(0, ships):  # generating a list of random ship lengths
        ships_list.append(random.choice([ship_len_1, ship_len_2, ship_len_3]))

    sum_1_all_ships = sum(ships_list)  # calculating the total length of ships
    sum_1_enemy = 0
    while sum_1_enemy != sum_1_all_ships:
        # reset the array of enemy ships
        enemy_ships = [[0 for i in range(s_y + 1)] for i in
                       range(
                           s_x + 1)]  # +1 for additional lines on the right and bottom, for successful enemy generation checks

        for i in range(0, ships):
            len = ships_list[i]
            horizont_vertikal = random.randrange(1, 3)  # 1- horizontal 2 - vertical

            primerno_x = random.randrange(0, s_x)
            if primerno_x + len > s_x:
                primerno_x = primerno_x - len

            primerno_y = random.randrange(0, s_y)
            if primerno_y + len > s_y:
                primerno_y = primerno_y - len

            if horizont_vertikal == 1:
                if primerno_x + len <= s_x:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y][primerno_x - 1] + \
                                               enemy_ships[primerno_y][primerno_x + j] + \
                                               enemy_ships[primerno_y][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j]

                            if check_near_ships == 0:  # write it down if there is nothing nearby
                                enemy_ships[primerno_y][primerno_x + j] = i + 1  # write down the number of the ship
                        except Exception:
                            pass
            if horizont_vertikal == 2:
                if primerno_y + len <= s_y:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y - 1][primerno_x] + \
                                               enemy_ships[primerno_y + j][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x - 1] + \
                                               enemy_ships[primerno_y + j][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j][primerno_x - 1]

                            if check_near_ships == 0:  # write it down if there is nothing nearby
                                enemy_ships[primerno_y + j][primerno_x] = i + 1  # write down the number of the ship
                        except Exception:
                            pass

        sum_1_enemy = 0
        for i in range(0, s_x):
            for j in range(0, s_y):
                if enemy_ships[j][i] > 0:
                    sum_1_enemy = sum_1_enemy + 1


generate_enemy_ships()

while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)
