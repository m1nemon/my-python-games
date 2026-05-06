import turtle, random, winsound, threading

def base10_base(base10, tobase):
    end = ""
    if base10 == 0:
        end = "0"
    while base10 != 0:
        end = base_key[base10 % tobase] + end
        base10 //= tobase
    return end


def base_base10(base, from_base):
    base = str(base)
    end = 0
    count = 0
    digits_list = []
    for c in base:
        digits_list.append(base_key.find(c))
    while len(digits_list) != 0:
        end += digits_list[-1] * (from_base ** count)
        count += 1
        digits_list = digits_list[:-1]
    return end


def hexa_to_rgb(hexa):
    return base_base10(hexa[:2], 16), base_base10(hexa[2:4], 16), base_base10(hexa[4:], 16)


def draw_rect(turtle, startx, starty, width, height):
    turtle.goto(startx, starty)
    turtle.begin_fill()
    turtle.setheading(0)
    turtle.fd(width)
    turtle.lt(90)
    turtle.fd(height)
    turtle.lt(90)
    turtle.fd(width)
    turtle.lt(90)
    turtle.fd(height)
    turtle.end_fill()

def draw_circ(turt,radius,angle = None,steps = None,x = 67,y = 67):
    if x == 67 and y == 67:
        x = turtle.xcor()
        y = turtle.ycor()
    turt.goto(x,y)
    turt.begin_fill()
    turt.circle(radius,angle,steps)
    turt.end_fill()

def create_button(turtle, room, next_room, next_room_function, startx, starty, width, height, shape, color):
    global buttons
    if color != "invis" and color != "invisible":
        turtle.color(color)
    if shape == "square" or shape.count("rect") != 0:
        draw_rect(turtle, startx, starty, width, height)
    if shape.count("circ") != 0:
        turtle.color("black")
        turtle.begin_fill()
        turtle.goto(startx, starty + height / 2)
        turtle.circle(width / 2)
        turtle.end_fill()
    buttons.append([room, next_room, next_room_function, startx, starty, startx + width, starty + height])


def on_button_click(new_room, room_function):
    global current_room
    current_room = new_room
    room_function()


def clear_room():
    global buttons, rolling_slots
    bg.clear()
    money.clear()
    if opened_slots:
        for turt in slot_turtles:
            turt.clear()
        slots_bg.clear()
        rolling_slots = False
    if opened_roulette:
        roulette.clear()
    buttons = []



def change_slot_image(turt, num):
    if num == 0:
        turt.shape("turtle")
        turt.color("green")
    elif num == 1:
        turt.shape("square")
        turt.color("red")
    elif num == 2:
        turt.shape("circle")
        turt.color("blue")







def setup():
    global base_key, buttons, current_room, title_font, money_font, moneys, opened_slots, opened_roulette
    base_key = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()-=_+{}[]|:;<>,.?/~`"
    buttons = []
    current_room = "title"
    title_font = ("Old English Text MT", 100, "normal")
    money_font = ("Cambria", 65, "normal")
    #Algerian  Verdana  Times New Roman  Rockwell  Garamond  Cambria  Century  Bookman Old Style
    moneys = 10000
    opened_slots = False
    opened_roulette = False


def mouse_setup():
    global mouse
    mouse = turtle.Turtle()
    mouse.penup()
    mouse.shape("turtle")
    mouse.shapesize(0.5)
    mouse.hideturtle()
    mouse.up()
    mouse.speed(0)


def mouse_click(xx, yy):
    global x, y
    x = xx
    y = yy
    mouse.goto(xx, yy)
    for i in range(len(buttons)):
        if (not (i >= len(buttons))) and current_room == buttons[i][0] and buttons[i][3] <= x <= buttons[i][5] and buttons[i][4] <= y <= buttons[i][6]:
            on_button_click(buttons[i][1], buttons[i][2])


def create_window():
    global window
    window = turtle.Screen()
    window.colormode(255)
    bg_color = hexa_to_rgb("394053")
    window.bgcolor(bg_color)
    window.title("Investment Simulator")
    window.setup(1920, 1080)


def create_bg_turtle():
    global bg
    window.tracer(0)
    bg = turtle.Turtle()
    bg.penup()
    bg.speed(0)
    bg.hideturtle()
    bg.shape("turtle")
    bg.color("black")
    window.tracer(1)


def create_title_screen():
    window.tracer(0)
    clear_room()
    create_button(bg, "title", "hub", create_hub, 400, 100, 500, 75, "rect", "black")
    create_button(bg, "title", "title", enter_save, 400, 0, 500, 75, "rect", "grey4")
    create_button(bg, "title", "options", options_menu, 400, -100, 500, 75, "rect", "grey")
    create_button(bg, "title", "quit", quit, 400, -200, 500, 75, "rect", "white")
    bg.goto(0, 350)
    bg.write("Investment Simulator", False, "center", title_font)
    window.tracer(1)


def create_hub():
    window.tracer(0)
    clear_room()
    create_button(bg, "hub", "title", create_title_screen, -910, 390, 100, 100, "rect", "black")
    create_button(bg, "hub", "hub", save_code, 710, -490, 200, 100, "rect", "black")
    create_button(bg, "hub", "slots", open_slots, 610, 90, 200, 300, "rect", "red")
    create_button(bg, "hub", "roll", open_roulette, -200, -200, 400, 400, "rectcirc", "grey")
    update_money()
    window.tracer(1)

def enter_save():
    save_code = window.textinput("Save game", "Enter the code last time you saved or just leave blank")
    if save_code != "":
        pass  # ill do this later

def save_code():
    save_code = "67"
    window.textinput("Save code",
                     save_code + "\nPut this in next time you play to save your progress\nJust put anything")

def options_menu():
    window.tracer(0)
    clear_room()
    create_button(bg, "options", "title", create_title_screen, -910, 390, 100, 100, "rect", "black")
    window.tracer(1)

def quit():
    window.bye()

def money_turtle_setup():
    global money
    money = turtle.Turtle()
    money.penup()
    money.speed(0)
    money.hideturtle()
    money.shape("turtle")

def update_money():
    window.tracer(0)
    money.clear()
    money_width = (len("{:,}".format(int(moneys))) + 1) * 50 + 10
    if len("{:,}".format(int(moneys))) // 4 > 0:
        money_width -= (len("{:,}".format(int(moneys))) // 4) * 36
    money.color("black")
    draw_rect(money, -910, -490, money_width, 100)
    money.goto(-900, -490)
    money.color("white")
    money.write("$" + "{:,}".format(int(moneys)), False, "left", money_font)
    window.tracer(1)


def open_slots():
    window.tracer(0)
    clear_room()
    create_button(bg, "slots", "hub", create_hub, -910, 390, 100, 100, "rect", "black")
    create_button(bg, "slots", "slots", roll_slots, 500, 25, 300, 100, "rect", "grey")
    create_button(bg, "slots", "slots", change_slot_bet, 500, -125, 300, 100, "rect", "black")
    update_money()
    if not opened_slots:
        setup_slots()
    left_slot.goto(-150, 300)
    middle_slot.goto(0, 300)
    right_slot.goto(150, 300)
    window.tracer(1)

def setup_slots():
    global left_slot, middle_slot, right_slot, slot_turtles, opened_slots, rolling_slots,current_slots, slots_bg, slot_bet
    window.tracer(0)
    left_slot = turtle.Turtle()
    left_slot.penup()
    change_slot_image(left_slot, 0)
    left_slot.speed(0)
    left_slot.shapesize(5)
    left_slot.setheading(270)
    left_slot.hideturtle()
    middle_slot = left_slot.clone()
    right_slot = left_slot.clone()
    slot_turtles = [left_slot, middle_slot, right_slot]
    for i in range(3):
        slot_turtles[i].goto(slot_turtles[i].xcor(), 150)
    slots_bg = turtle.Turtle()
    slots_bg.penup()
    slots_bg.hideturtle()
    slots_bg.speed(0)
    opened_slots = True
    rolling_slots = False
    current_slots = []
    slot_bet = 5
    for turt in slot_turtles:
        thing = random.randint(0, 2)
        change_slot_image(turt,thing)
        current_slots.append(thing)
    window.tracer(1)

def change_slot_bet():
    global slot_bet
    slot_bet = window.numinput("Slot bet", "Enter the slot bet:",int(moneys),1,moneys)

def roll_slots():
    global rolling_slots, moneys
    if rolling_slots or (current_room != "slots"):
        return
    speed = 5
    spins = 5000
    moneys -= slot_bet
    update_money()
    rolling_slots = True
    slot_1 = random.randint(0, 2)
    slot_2 = random.randint(0, 2)
    slot_3 = random.randint(0, 2)
    slots = [slot_1, slot_2, slot_3]
    #0 = turtle, 1 = square, 2 = circle
    for i in range(3):
        slot_turtles[i].goto(slot_turtles[i].xcor(), 300)
    for i in range(spins):
        if current_room != "slots": return
        window.tracer(0)
        for j in range(3):
            slot_turtles[j].clear()
            slot_turtles[j].goto(slot_turtles[j].xcor(), slot_turtles[j].ycor() - speed)
            if slot_turtles[j].ycor() <= 0:
                slot_turtles[j].goto(slot_turtles[j].xcor(), 300)
                thing = random.randint(0, 2)
                while current_slots[j] == thing:
                    thing = random.randint(0, 2)
                change_slot_image(slot_turtles[j], thing)
                current_slots[j] = thing
        if i == spins-1:
            if slot_turtles[0].ycor() > 150:
                while slot_turtles[0].ycor() >= 150:
                    window.tracer(0)
                    for w in range(3):
                        slot_turtles[w].clear()
                        slot_turtles[w].goto(slot_turtles[w].xcor(), slot_turtles[w].ycor() - speed)
                        slot_turtles[w].stamp()
                    slots_bg.clear()
                    draw_rect(slots_bg, -250, -100, 500, 100)
                    draw_rect(slots_bg, -250, 300, 500, 100)
                    window.tracer(1)
                window.tracer(0)
            else:
                while round(slot_turtles[0].ycor(),1) != 150.0:
                    window.tracer(0)
                    for l in range(3):
                        slot_turtles[l].clear()
                        slot_turtles[l].goto(slot_turtles[l].xcor(), slot_turtles[l].ycor() - speed)
                        slot_turtles[l].stamp()
                        if slot_turtles[l].ycor() <= 0:
                            slot_turtles[l].goto(slot_turtles[l].xcor(), 300)
                            thing = random.randint(0, 2)
                            while current_slots[l] == thing:
                                thing = random.randint(0, 2)
                            change_slot_image(slot_turtles[l], thing)
                            current_slots[l] = thing
                    slots_bg.clear()
                    draw_rect(slots_bg, -250, -100, 500, 100)
                    draw_rect(slots_bg, -250, 300, 500, 100)
                    window.tracer(1)
                window.tracer(0)
        for r in range(3):
            slot_turtles[r].stamp()
        slots_bg.clear()
        draw_rect(slots_bg, -250, -100, 500, 100)
        draw_rect(slots_bg, -250, 300, 500, 100)
        window.tracer(1)
    window.tracer(0)
    for r in range(3):
        slot_turtles[r].clear()
        slot_turtles[r].goto(slot_turtles[r].xcor(), 150)
        slot_turtles[r].stamp()
    window.tracer(1)
    rolling_slots = False
    if current_slots[0] == current_slots[1] == current_slots[2] == 0:
        moneys += slot_bet * 100
        update_money()
    elif current_slots[0] == current_slots[1] == current_slots[2]:
        moneys += slot_bet * 20
        update_money()

def setup_roulette():
    global roulette, opened_roulette, spinning_roulette, roll_bet, chosen_roulette_number, chosen_roulette_color, has_chosen_roulette_num, has_chosen_roulette_color
    window.tracer(0)
    roulette = turtle.Turtle()
    roulette.penup()
    roulette.hideturtle()
    window.tracer(1)
    draw_bg_roulette()
    opened_roulette = True
    spinning_roulette = False
    roll_bet = 5
    chosen_roulette_number = -1
    chosen_roulette_color = ""
    has_chosen_roulette_num = False
    has_chosen_roulette_color = False

def draw_bg_roulette():
    window.tracer(0)
    bg.color("black")
    bg.setheading(0)
    draw_circ(bg,450,None,None,0,-450)
    roulette.color("red")
    roulette.setheading(0)
    for i in range(18):
        roulette.goto(0, 0)
        roulette.begin_fill()
        roulette.fd(450)
        roulette.lt(90)
        roulette.circle(450, 10)
        roulette.setheading(roulette.towards(0, 0))
        roulette.fd(450)
        roulette.end_fill()
        roulette.lt(180)
        roulette.lt(10)
    roulette.color("white")
    roulette.goto(-503, 30)
    roulette.begin_fill()
    roulette.goto(-390, 0)
    roulette.goto(-503, -30)
    roulette.end_fill()
    roulette.color("black")
    roulette.goto(-500, 25)
    roulette.begin_fill()
    roulette.goto(-400, 0)
    roulette.goto(-500, -25)
    roulette.end_fill()
    window.tracer(1)

def open_roulette():
    window.tracer(0)
    clear_room()
    create_button(bg, "roll", "hub", create_hub, -910, 390, 100, 100, "rect", "black")
    create_button(bg, "roll", "roll", spin_roulette, 500, 175, 300, 100, "rect", "white")
    create_button(bg, "roll", "roll", chose_roulette_color, 500, 25, 300, 100, "rect", "gray")
    create_button(bg, "roll", "roll", chose_roulette_num, 500, -125, 300, 100, "rect", "dim gray")
    create_button(bg, "roll", "roll", change_roulette_bet, 500, -275, 300, 100, "rect", "black")
    update_money()
    if not opened_roulette:
        setup_roulette()
    else:
        draw_bg_roulette()
    window.tracer(1)

def spin_roulette():
    global spinning_roulette, has_chosen_roulette_color, has_chosen_roulette_num, moneys
    if spinning_roulette or current_room != "roll":
        return
    if has_chosen_roulette_num or has_chosen_roulette_color:
        moneys -= roll_bet
        update_money()
    speed = 1
    #spins = 1000
    #spins_num = random.randint(5,35)
    #spins_num = 1
    #spins = (spins_num * 10) * (1 / speed)
    #spins = (spins_num * 10) * (1/speed)  + random.randint(2,6) * 360
    spins = random.randrange(720,1260)
    spinning_roulette = True
    window.tracer(0)
    roulette.setheading(0)
    for j in range(int(spins)):
        if current_room != "roll": return
        if j>0 and int(round(roulette.heading(), 0) // 10)%10==0: a.join()
        window.tracer(0)
        roulette.clear()
        roulette.lt(speed)
        roulette.color("red")
        for i in range(18):
            roulette.goto(0,0)
            roulette.begin_fill()
            roulette.fd(450)
            roulette.lt(90)
            roulette.circle(450,10)
            roulette.setheading(roulette.towards(0,0))
            roulette.fd(450)
            roulette.end_fill()
            roulette.lt(180)
            roulette.lt(10)
        roulette.color("white")
        roulette.goto(-503, 30)
        roulette.begin_fill()
        roulette.goto(-390, 0)
        roulette.goto(-503, -30)
        roulette.end_fill()
        roulette.color("black")
        roulette.goto(-500,25)
        roulette.begin_fill()
        roulette.goto(-400,0)
        roulette.goto(-500,-25)
        roulette.end_fill()
        window.tracer(1)
        if int(round(roulette.heading(), 0) // 10)%10==0:
            a = threading.Thread(target=winsound.Beep, args=[450,50], daemon=True)
            a.start()
    wheel_heading = round(roulette.heading(),0)
    if wheel_heading//10 % 2 == 0:
        color = "black"
    else:
        color = "red"
    if has_chosen_roulette_color and chosen_roulette_color[0] == color[0]:
        moneys+=roll_bet * 3
        update_money()
    if has_chosen_roulette_num and chosen_roulette_num == int(wheel_heading//10):
        moneys+=roll_bet * 72
        update_money()
    #has_chosen_roulette_num = False
    #has_chosen_roulette_color = False
    spinning_roulette = False

def change_roulette_bet():
    global roll_bet
    roll_bet = window.numinput("Slot bet", "Enter the roulette bet:",int(moneys), 1, moneys)

def chose_roulette_num():
    global chosen_roulette_num, has_chosen_roulette_num
    chosen_roulette_num = window.numinput("Chose Number","Enter the number you want to bet on",0,-1,35)
    if chosen_roulette_num == -1:
        has_chosen_roulette_num = False
        return
    has_chosen_roulette_num = True

def chose_roulette_color():
    global chosen_roulette_color, has_chosen_roulette_color
    chosen_roulette_color = window.textinput("Chose Color","Enter the color you want to bet on:")
    acceptable_answers = ["r","b","red","black",""]
    while not chosen_roulette_color in acceptable_answers:
        chosen_roulette_color = window.textinput("Chose Color", "Invalid answer\nEnter the color you want to bet on:")
    if chosen_roulette_color == "":
        has_chosen_roulette_color = False
        return
    has_chosen_roulette_color = True

def main():
    setup()
    create_window()
    create_bg_turtle()
    window.tracer(0)
    mouse_setup()
    money_turtle_setup()
    window.tracer(1)
    create_title_screen()
    window.onclick(mouse_click, 1)


if __name__ == '__main__':
    main()
    turtle.done()
