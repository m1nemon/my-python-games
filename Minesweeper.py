import turtle, random, sys

def is_mine(cords):
    if real_grid[cords[1]][cords[0]][1] == "m":
        return True
    else:
        return False

def turt_set_color(turtle,number,colors):
    if number % 2 == 0:
        color = colors[0]
    else:
        color = colors[1]
    turtle.color(color)

def mines_around(x,y):
    return int(real_grid[y][x][0])

def win_lose_setup():
    global advait
    advait = turtle.Turtle()
    advait.shape("turtle")
    advait.goto(0,0)
    advait.ht()
    advait.penup()
    advait.speed(0)

def check_win_lose():
    count = 0
    if not won and not lost:
        for mine in mines:
            if is_broken(mine):
                lose()
                return
        for i in range(height):
            for j in range(width):
                if not is_mine((j,i)) and is_broken((j,i)):
                    count += 1
        if count == (height * width) - mine_count:
            win()

def lose():
    global lost
    lost = True
    advait.color("red")
    advait.write("You lose!", align="center", font=("Arial", 200, "bold"))

def win():
    global won
    won = True
    advait.color("green")
    advait.write("You win!!!", align="center", font=("Arial", 200, "bold"))

def is_broken(cords):
    x,y = cords
    if tile_grid[y][x] == 1:
        return True
    else:
        return False

def flood_break(start_x, start_y):
    global turtle_tiles
    window.tracer(0)
    if mines_around(start_x, start_y) > 0 or flood_grid[start_y][start_x] == 1:
        return
    else:
        for a in range(-1,2):
            for b in range(-1,2):
                if start_y + a >= height or start_y + a < 0 or start_x + b < 0 or start_x + b >= width:
                    continue
                elif flood_grid[start_y+a][start_x+b] == 1:
                    continue
                else:
                    break_tile(start_x, start_y)
                    flood_grid[start_y][start_x] = 1
                    break_tile(start_x+b, start_y+a)
                    flood_break(start_x+b, start_y+a)
    window.tracer(1)

def break_tile(x,y):
    global tile_grid, turtle_tiles, flood_grid, flag_grid
    if tile_grid[y][x] == 0 and flag_grid[y][x] == 0 and not won and not lost:
        tile.clearstamp(turtle_tiles[y][x])
        turtle_tiles[y][x] = 0
        tile_grid[y][x] = 1

def is_flagged(cords):
    x,y = cords
    return flag_grid[y][x] != 0

def check_flag_on_broken():
    for i in range(height):
        for j in range(width):
            if is_broken((j,i)) and is_flagged((j,i)):
                damon.clearstamp(flag_grid[i][j])
                flag_grid[i][j] = 0

def create_grid(grid):
    for i in range(height):
        row = []
        for j in range(width):
            row.append(0)
        grid.append(row)

def goto_cords(turtle,x,y):
    turtle.goto((x - (width - 1) / 2.0) * (window_height / width), (y - (height - 1) / 2.0) * (window_height / height))

def setup():
    global width, height, mine_count, real_grid, bg_color_1, bg_color_2, bg_colors,tile_colors, odd, moves, won, lost, shape_distortion
    size = chosen_size
    width = int(size)
    height = int(size)
    sys.setrecursionlimit(int(size*size)+100)
    mine_count = int(chosen_mines)
    odd = size % 2 == 1
    if mine_count > width * height:
        mine_count = width * height
    bg_color_1 = (170,214,81)
    bg_color_2 = (162,209,73)
    bg_colors = [bg_color_1, bg_color_2]
    tile_color_1 = (31,36,120)
    tile_color_2 = (10,15,107)
    tile_colors = [tile_color_1, tile_color_2]
    moves = 0
    lost = False
    won = False
    shape_distortion = window_height / height / 20

def map_maker():
    global width, height, mines, mine_count, real_grid, unique_mines, unique_mines, moves
    mines = []
    moves = 0
    unique_mines = 0
    real_grid = []
    create_grid(real_grid)
    for i in range(mine_count):
        random_row = random.randint(0, width-1)
        random_column = random.randint(0, height-1)
        mines.append((random_row,random_column))
    while unique_mines < mine_count:
        unique_mines = 0
        for mine in mines:
            if mines.count(mine) > 1:
                mines.remove(mine)
                random_row = random.randint(0, (width - 1))
                random_column = random.randint(0, (height - 1))
                mines.append((random_row, random_column))
            elif mines.count(mine) == 1:
                unique_mines += 1
    for i in range(height):
        for j in range(width):
            cord = (j,i)
            if mines.count(cord) == 1:
                real_grid[i][j] = "0m"
            else:
                real_grid[i][j] = "0n"
    for i in range(len(real_grid)):
        for j in range(len(real_grid[i])):
            around = 0
            for a in range(-1,2):
                for b in range(-1,2):
                    cord = (j+a,i+b)
                    if cord[0] < 0 or cord[0] >= width or cord[1] < 0 or cord[1] >= height:
                        pass
                    else:
                        if is_mine(cord):
                            around += 1
            real_grid[i][j] = str(around) + real_grid[i][j][1]

def screen_turtle():
    global window, window_height, window_width, chosen_size, chosen_mines
    window_height = 800
    window_width = 1280
    window = turtle.Screen()
    window.colormode(255)
    bg_color = (75,117,45)
    window.bgcolor(bg_color)
    window.title("Minesweeper")
    window.setup(window_width, window_height)
    chosen_size = 10

def ask_size_and_mine():
    global chosen_size, chosen_mines
    chosen_size = window.numinput("Choose a size","Please choose the size of your board",10,1,10000)
    estimated = int((chosen_size ** 2) / 4)
    chosen_mines = window.numinput("Choose how many mines you want", "Please choose how many mines you want. Probably:" + str(int(estimated)), estimated, 1, chosen_size*chosen_size)

def bg_tiles():
    global bg_tile
    bg_tile = turtle.Turtle()
    bg_tile.shape("square")
    bg_tile.hideturtle()
    bg_tile.up()
    bg_tile.speed(0)
    bg_tile.shapesize(shape_distortion)
    c = 0
    for i in range(height):
        if not odd:
            c += 1
        for j in range(width):
            goto_cords(bg_tile, j, i)
            turt_set_color(bg_tile, c, bg_colors)
            bg_tile.stamp()
            c += 1

def numbers_and_mines():
    global efaz
    font = ("Verdana",int(shape_distortion * 7),"normal")
    possible_numbers = ["","1","2","3","4","5","6","7","8","9"]
    number_colors = ["black",(25,117,209),(56,143,60),(212,47,47),(124,31,168),(255,145,0),(0,158,176),(59,69,74),(196,191,171)]
    efaz = turtle.Turtle()
    efaz.shape("circle")
    efaz.color("black")
    efaz.shapesize(shape_distortion/2)
    efaz.ht() #hide turtle
    efaz.up()
    efaz.speed(0)
    c = 1
    for i in range(height):
        if not odd:
            c += 1
        for j in range(width):
            c += 1
            if is_mine((j,i)):
                goto_cords(efaz,j,i)
                efaz.color("black")
                efaz.stamp()
            else:
                efaz.goto((j - (width - 1) / 2.0) * (window_height / width),(i - (height - 1) / 2.0) * (window_height / height) - (window_height / height / 5))
                efaz.color(number_colors[mines_around(j,i)])
                if height > 40 or width > 40:
                    efaz.setheading(90)
                    efaz.fd((window_height / height / 5))
                    if mines_around(j,i) == 0:
                        turt_set_color(efaz,c,bg_colors)
                    efaz.stamp()
                else:
                    efaz.write(possible_numbers[mines_around(j,i)],False,"center",font)
def tile_turtles():
    global turtle_tiles, tile
    tile = turtle.Turtle()
    tile.hideturtle()
    tile.up()
    tile.speed(0)
    tile.shape("square")
    # Normal square is 20 px * 20 px
    tile.showturtle()

def create_tile_grid():
    global tile
    tile.shapesize(shape_distortion)
    c = 0
    for i in range(height):
        if not odd:
            c += 1
        for j in range(width):
            turt_set_color(tile, c, tile_colors)
            goto_cords(tile,j,i)
            turtle_tiles[i][j] = tile.stamp()
            c += 1
    tile.hideturtle()


def no_one_hears_a_word_they_say():
    global solid_snake, tile_grid, flood_grid
    solid_snake = turtle.Turtle()
    solid_snake.penup()
    solid_snake.shape("turtle")
    solid_snake.shapesize(0.5)
    solid_snake.hideturtle()
    solid_snake.up()
    solid_snake.speed(0)

def flag_turtle():
    global damon, flag_grid
    damon = turtle.Turtle()
    damon.penup()
    damon.shape("circle")
    damon.color("red")
    damon.ht()
    damon.up()
    damon.speed(0)

def on_flag_click(x, y):
    global flag_x, flag_y, damon
    damon.shapesize(shape_distortion / 3)
    flag_x, flag_y = 0, 0
    flag_x, flag_y = center_on_cords_and_give_mouse_cords(x, y, damon)
    if not lost and not won:
        if flag_grid[flag_y][flag_x] == 0 and tile_grid[flag_y][flag_x] == 0:
            flag_grid[flag_y][flag_x] = damon.stamp()
        else:
            damon.clearstamp(flag_grid[flag_y][flag_x])
            flag_grid[flag_y][flag_x] = 0
    check_win_lose()
    check_flag_on_broken()

def center_on_cords_and_give_mouse_cords(x,y,turtle):
    if not odd:
        end_mouse_x = x // round(window_height / width, 0) + (width // 2)
        end_mouse_y = y // round(window_height / width, 0) + (height // 2)
    else:
        end_mouse_x = round(x / round(window_height / width, 0), 0) + (width // 2)
        end_mouse_y = round(y / round(window_height / width, 0), 0) + (height // 2)
    goto_cords(turtle, end_mouse_x, end_mouse_y)
    return int(end_mouse_x), int(end_mouse_y)

def solid_snake_sneaking_around(x,y):
    global mouse_x, mouse_y, moves
    mouse_x , mouse_y = 0,0
    mouse_x,mouse_y = center_on_cords_and_give_mouse_cords(x,y,solid_snake)
    if moves == 0 and mines_around(mouse_x,mouse_y) != 0:
        window.tracer(0)
        while True:
            if moves == 0 and mines_around(mouse_x,mouse_y) != 0:
                map_maker()
            else:
                break
        numbers_and_mines()
        tile.clear()
        create_tile_grid()
        window.tracer(1)
    elif moves == 0:
        window.tracer(0)
        numbers_and_mines()
        tile.clear()
        create_tile_grid()
        window.tracer(1)
    moves += 1
    if tile_grid[mouse_y][mouse_x] == 0 and flag_grid[mouse_y][mouse_x] == 0 and not won and not lost and mines_around(mouse_x, mouse_y) == 0:
        flood_break(mouse_x, mouse_y)
    break_tile(mouse_x, mouse_y)
    check_win_lose()
    check_flag_on_broken()

def grid_setups():
    global flag_grid, tile_grid, flood_grid, turtle_tiles
    flag_grid = []
    create_grid(flag_grid)
    tile_grid = []
    create_grid(tile_grid)
    flood_grid = []
    create_grid(flood_grid)
    turtle_tiles = []
    create_grid(turtle_tiles)

def restart():
    global efaz,damon, bg_tile
    window.tracer(0)
    efaz.clear()
    damon.clear()
    tile.clear()
    bg_tile.clear()
    advait.clear()
    ask_size_and_mine()
    setup()
    map_maker()
    grid_setups()
    bg_tiles()
    create_tile_grid()
    window.tracer(1)

def main():
    screen_turtle()
    ask_size_and_mine()
    setup()
    grid_setups()
    map_maker()
    window.tracer(0)
    bg_tiles()
    tile_turtles()
    create_tile_grid()
    no_one_hears_a_word_they_say()
    flag_turtle()
    win_lose_setup()
    window.tracer(1)
    check_win_lose()
    window.onclick(solid_snake_sneaking_around, 1)
    window.onclick(on_flag_click, 3)
    window.onkeypress(restart, "r")
    window.listen()

if __name__ == '__main__':
    main()

turtle.done()
