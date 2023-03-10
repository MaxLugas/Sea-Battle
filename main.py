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

txt_len_middle = '* Human vs Computer'
size_font_x = 10
len_txt_x = len(txt_len_middle) * size_font_x
delta_menu_x = len_txt_x // step_x + 1
menu_x = step_x * delta_menu_x

menu_y = 40
ships = s_x // 2  # maximum number of ships
ship_len_1 = s_x // 5  # length of the first type of ship
ship_len_2 = s_x // 3  # length of the second type of ship
ship_len_3 = s_x // 2  # length of the third type of ship
enemy_ships1 = [[0 for i in range(s_y + 1)] for i in range(s_x + 1)]
enemy_ships2 = [[0 for i in range(s_y + 1)] for i in range(s_x + 1)]
list_ids = []  # list objects canvas

points1 = [[-1 for i in range(s_y)] for i in range(s_x)]  # push button list
points2 = [[-1 for i in range(s_y)] for i in range(s_x)]
boom = [[0 for i in range(s_y)] for i in range(s_x)]  # hit list

ships_list = []  # ships list player1 and player2

player_move = False  # if True then second player

computer_vs_human = False  # if True then play versus computer
if computer_vs_human:
    add_to_label = '(Computer)'
    player_move = False
else:
    add_to_label = ''
    player_move = False


def on_closing():
    global app_running
    if messagebox.askyesno('Exit', 'Are u sure?'):
        app_running = False
        tk.destroy()


tk.protocol('WM_DELETE_WINDOW', on_closing)
tk.title('SEA BATTLE')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
canvas = Canvas(tk, width=size_canvas_x + menu_x + size_canvas_x, height=size_canvas_y + menu_y, bd=0,
                highlightthickness=0)
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill='white')
canvas.create_rectangle(size_canvas_x + menu_x, 0, size_canvas_x + menu_x + size_canvas_x, size_canvas_y,
                        fill='lightyellow')
canvas.pack()
tk.update()


def draw_table(offset_x=0):
    for i in range(0, s_x + 1):
        canvas.create_line(offset_x + step_x * i, 0, offset_x + step_x * i, size_canvas_y)
    for i in range(0, s_y + 1):
        canvas.create_line(offset_x, step_y * i, offset_x + size_canvas_x, step_y * i)


draw_table()
draw_table(size_canvas_x + menu_x)

t0 = Label(tk, text='Player ???1', font=('Helvetica', 10))
t0.place(x=size_canvas_x // 2 - t0.winfo_reqwidth() // 2, y=size_canvas_y + 3)
t1 = Label(tk, text='Player ???2' + add_to_label, font=('Helvetica', 10))
t1.place(x=size_canvas_x + menu_x + size_canvas_x // 2 - t1.winfo_reqwidth() // 2, y=size_canvas_y + 3)
t3 = Label(tk, text='@@@@@@', font=('Helvetica', 9))
t3.place(x=size_canvas_x + menu_x // 2 - t3.winfo_reqwidth() // 2, y=size_canvas_y)

t0.configure(bg='red')
t0.configure(bg='#f0f0f0')


def change_rb():
    global computer_vs_human, add_to_label
    if rb_var.get():
        computer_vs_human = True
        add_to_label = '(Computer)'
    else:
        computer_vs_human = False
        add_to_label = ''


rb_var = BooleanVar()
rb_1 = Radiobutton(tk, text='Human vs Computer', variable=rb_var, value=1, command=change_rb)
rb_2 = Radiobutton(tk, text='Human vs Human', variable=rb_var, value=0, command=change_rb)

rb_1.place(x=size_canvas_x + 100 - rb_1.winfo_reqwidth() // 2, y=150)
rb_2.place(x=size_canvas_x + 100 - rb_2.winfo_reqwidth() // 2, y=170)

if computer_vs_human:
    rb_1.select()


# t0 for first player, t1 for second player
def mark_player(player_mark):
    if player_mark:
        t1.configure(bg='red')
        t0.configure(bg='#f0f0f0')
        t3.configure(text='Player ???2 move')
        t1.configure(text='Player ???2' + add_to_label)
        t3.place(x=size_canvas_x + menu_x // 2 - t3.winfo_reqwidth() // 2, y=size_canvas_y)
    else:
        t0.configure(bg='red')
        t1.configure(bg='#f0f0f0')
        t3.configure(text='Player ???1 move')


mark_player(player_move)


def button_show_enemy1():
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships1[j][i] > 0:
                color = 'red'
                if points1[j][i] != -1:
                    color = 'black'
                _id = canvas.create_rectangle(i * step_x, j * step_y, i * step_x + step_x, j * step_y + step_y,
                                              fill=color)
                list_ids.append(_id)


def button_show_enemy2():
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships2[j][i] > 0:
                color = 'red'
                if points2[j][i] != -1:
                    color = 'black'
                _id = canvas.create_rectangle(size_canvas_x + menu_x + i * step_x, j * step_y,
                                              size_canvas_x + menu_x + i * step_x + step_x, j * step_y + step_y,
                                              fill=color)
                list_ids.append(_id)


def button_begin_again():
    global list_ids
    global points1, points2
    global boom
    global enemy_ships1, enemy_ships2
    for el in list_ids:
        canvas.delete(el)
    list_ids = []
    generate_ships_list()
    enemy_ships1 = generate_enemy_ships()
    enemy_ships2 = generate_enemy_ships()
    points1 = [[-1 for i in range(s_y)] for i in range(s_x)]
    points2 = [[-1 for i in range(s_y)] for i in range(s_x)]
    boom = [[0 for i in range(s_y)] for i in range(s_x)]


b0 = Button(tk, text='Show player \n ???1 ships', command=button_show_enemy1)
b0.place(x=size_canvas_x + menu_x // 2 - b0.winfo_reqwidth() // 2, y=10)

b1 = Button(tk, text='Show player \n ???2 ships', command=button_show_enemy2)
b1.place(x=size_canvas_x + menu_x // 2 - b1.winfo_reqwidth() // 2, y=60)

b2 = Button(tk, text='Restart game', command=button_begin_again)
b2.place(x=size_canvas_x + menu_x // 2 - b2.winfo_reqwidth() // 2, y=110)


def draw_point(x, y):
    if enemy_ships1[y][x] == 0:
        color = "red"
        id1 = canvas.create_oval(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y, fill=color)
        id2 = canvas.create_oval(x * step_x + step_x // 3, y * step_y + step_y // 3, x * step_x + step_x - step_x // 3,
                                 y * step_y + step_y - step_y // 3, fill="white")
        list_ids.append(id1)
        list_ids.append(id2)

    if enemy_ships1[y][x] > 0:
        color = "green"
        id1 = canvas.create_rectangle(x * step_x, y * step_y + step_y // 2 - step_y // 10, x * step_x + step_x,
                                      y * step_y + step_y // 2 + step_y // 10, fill=color)
        id2 = canvas.create_rectangle(x * step_x + step_x // 2 - step_x // 10, y * step_y,
                                      x * step_x + step_x // 2 + step_x // 10, y * step_y + step_y, fill=color)
        list_ids.append(id1)
        list_ids.append(id2)


def draw_point2(x, y, offset_x=size_canvas_x + menu_x):
    if enemy_ships2[y][x] == 0:
        color = "red"
        id1 = canvas.create_oval(offset_x + x * step_x, y * step_y, offset_x + x * step_x + step_x, y * step_y + step_y,
                                 fill=color)
        id2 = canvas.create_oval(offset_x + x * step_x + step_x // 3, y * step_y + step_y // 3,
                                 offset_x + x * step_x + step_x - step_x // 3,
                                 y * step_y + step_y - step_y // 3, fill="white")
        list_ids.append(id1)
        list_ids.append(id2)

    if enemy_ships2[y][x] > 0:
        color = "green"
        id1 = canvas.create_rectangle(offset_x + x * step_x, y * step_y + step_y // 2 - step_y // 10,
                                      offset_x + x * step_x + step_x,
                                      y * step_y + step_y // 2 + step_y // 10, fill=color)
        id2 = canvas.create_rectangle(offset_x + x * step_x + step_x // 2 - step_x // 10, y * step_y,
                                      offset_x + x * step_x + step_x // 2 + step_x // 10, y * step_y + step_y,
                                      fill=color)
        list_ids.append(id1)
        list_ids.append(id2)


def check_winner(x, y):
    win = False
    if enemy_ships1[y][x] > 0:
        boom[y][x] = enemy_ships1[y][x]
    sum_enemy_ships1 = sum(sum(i) for i in zip(*enemy_ships1))
    sum_boom = sum(sum(i) for i in zip(*boom))
    if sum_enemy_ships1 == sum_boom:
        win = True
    return win


def check_winner2():
    win = True
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships1[j][i] > 0:
                if points1[j][i] == -1:
                    win = False
    return win


def check_winner2_player2():
    win = True
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships2[j][i] > 0:
                if points2[j][i] == -1:
                    win = False
    return win


def computer_move():
    global points1, points2, player_move
    tk.update()
    time.sleep(1)
    player_move = False
    ip_x = random.randint(0, s_x - 1)
    ip_y = random.randint(0, s_y - 1)
    while not points1[ip_y][ip_x] == -1:
        ip_x = random.randint(0, s_x - 1)
        ip_y = random.randint(0, s_y - 1)
    points1[ip_y][ip_x] = 7
    draw_point(ip_x, ip_y)
    if check_winner2():
        messagebox.showinfo('SEA BATTLE', "Player ???2 win!!!!" + add_to_label)
        points1 = [[10 for i in range(s_y)] for i in range(s_x)]
        points2 = [[10 for i in range(s_y)] for i in range(s_x)]


def add_to_all(event):
    global points1, points2, player_move
    _type = 0  # left mouse button
    if event.num == 3:
        _type = 1  # right mouse button
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    ip_x = mouse_x // step_x
    ip_y = mouse_y // step_y

    # first game field
    if ip_x < s_x and ip_y < s_y and player_move:
        if points1[ip_y][ip_x] == -1:
            points1[ip_y][ip_x] = _type
            player_move = False
            draw_point(ip_x, ip_y)
            if check_winner2():
                player_move = True
                messagebox.showinfo('SEA BATTLE', "Player ???2 win!!!!")
                points1 = [[10 for i in range(s_y)] for i in range(s_x)]
                points2 = [[10 for i in range(s_y)] for i in range(s_x)]

    # second game field
    if ip_x >= s_x + delta_menu_x and ip_x <= s_x + s_x + delta_menu_x and ip_y < s_y and not player_move:
        if points2[ip_y][ip_x - s_x - delta_menu_x] == -1:
            points2[ip_y][ip_x - s_x - delta_menu_x] = _type
            player_move = True
            draw_point2(ip_x - s_x - delta_menu_x, ip_y)
            if check_winner2_player2():
                player_move = False
                messagebox.showinfo('SEA BATTLE', "Player ???1 win!!!!")
                points1 = [[10 for i in range(s_y)] for i in range(s_x)]
                points2 = [[10 for i in range(s_y)] for i in range(s_x)]
            elif computer_vs_human:
                mark_player(player_move)
                computer_move()
    mark_player(player_move)


canvas.bind_all('<Button-1>', add_to_all)  # left mouse button
canvas.bind_all('<Button-3>', add_to_all)  # right mouse button


def generate_ships_list():
    global ships_list
    ships_list = []
    for i in range(0, ships):  # generating a list of random ship lengths
        ships_list.append(random.choice([ship_len_1, ship_len_2, ship_len_3]))


def generate_enemy_ships():
    global ships_list
    enemy_ships = []

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

            approximately_x = random.randrange(0, s_x)
            if approximately_x + len > s_x:
                approximately_x = approximately_x - len

            approximately_y = random.randrange(0, s_y)
            if approximately_y + len > s_y:
                approximately_y = approximately_y - len

            if horizont_vertikal == 1:
                if approximately_x + len <= s_x:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[approximately_y][approximately_x - 1] + \
                                               enemy_ships[approximately_y][approximately_x + j] + \
                                               enemy_ships[approximately_y][approximately_x + j + 1] + \
                                               enemy_ships[approximately_y + 1][approximately_x + j + 1] + \
                                               enemy_ships[approximately_y - 1][approximately_x + j + 1] + \
                                               enemy_ships[approximately_y + 1][approximately_x + j] + \
                                               enemy_ships[approximately_y - 1][approximately_x + j]

                            if check_near_ships == 0:  # write it down if there is nothing nearby
                                enemy_ships[approximately_y][
                                    approximately_x + j] = i + 1  # write down the number of the ship
                        except Exception:
                            pass
            if horizont_vertikal == 2:
                if approximately_y + len <= s_y:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[approximately_y - 1][approximately_x] + \
                                               enemy_ships[approximately_y + j][approximately_x] + \
                                               enemy_ships[approximately_y + j + 1][approximately_x] + \
                                               enemy_ships[approximately_y + j + 1][approximately_x + 1] + \
                                               enemy_ships[approximately_y + j + 1][approximately_x - 1] + \
                                               enemy_ships[approximately_y + j][approximately_x + 1] + \
                                               enemy_ships[approximately_y + j][approximately_x - 1]

                            if check_near_ships == 0:  # write it down if there is nothing nearby
                                enemy_ships[approximately_y + j][
                                    approximately_x] = i + 1  # write down the number of the ship
                        except Exception:
                            pass

        sum_1_enemy = 0
        for i in range(0, s_x):
            for j in range(0, s_y):
                if enemy_ships[j][i] > 0:
                    sum_1_enemy = sum_1_enemy + 1

    return enemy_ships


generate_ships_list()
enemy_ships1 = generate_enemy_ships()
enemy_ships2 = generate_enemy_ships()
# print('***************************')
# print(enemy_ships1)
# print('***************************')
# print(enemy_ships2)
# print('***************************')

while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)
