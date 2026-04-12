import turtle
import random
not_done = False
begginginging_length = 5
length = begginginging_length
moves = 0
locations = []
distance = 50
snake_thick = 21
not_dead = True
# setup stuff
window = turtle.Screen()
window.cv._rootwindow.resizable(False, False)
# no resize window
bg_color = "black"
window.bgcolor("black")
window.title("Snake")
window.setup(width=1200, height=1000)
window.colormode(255)
window.tracer(0)
bg_color_1 = "grey20"
bg_color_2 = "grey30"
bg = turtle.Turtle()
bg.color(bg_color_1)
bg.shape("square")
bg.speed(0)
bg.shapesize(2.5)
bg.penup()
# background turtle

window.tracer(0)
bg.goto(-575,475)
bg.stamp()
for i in range(20):
    bg.goto(-575,475 - i * 50)
    for j in range(24):
        if j % 2 == 0:
            if i % 2 == 0:
                bg.color(bg_color_1)
            else:
                bg.color(bg_color_2)
        else:
            if i % 2 == 0:
                bg.color(bg_color_2)
            else:
                bg.color(bg_color_1)
        bg.goto(-575 + 50 * j,bg.ycor())
        bg.stamp()
bg.goto(625,-475)
# sets up bg

apple = turtle.Turtle()
apple.color("red")
apple.shape("circle")
apple.speed(0)
apple.hideturtle()
# apple turtle

snake = turtle.Turtle()
snake.shape("circle")
snake.color("green")
snake.pencolor("green")
snake.pensize(snake_thick)
snake.speed(0)
snake.penup()
snake.goto(25,25)
snake.pendown()
# snake turtle

window.tracer(1)

def shadows():
    window.tracer(0)
    if moves == begginginging_length:
        bg.color(bg_color_2)
        bg.goto(25,25)
        bg.stamp()
        # covers your starting point cuz one below don't do that
    if len(locations) >= length:
        bg.goto(locations[-length])
        if length % 2 == 0:
            if moves % 2 == 0:
                bg.color(bg_color_1)
            else:
                bg.color(bg_color_2)
        else:
            if moves % 2 == 0:
                bg.color(bg_color_2)
            else:
                bg.color(bg_color_1)
        bg.stamp()
    # covers the end of your tail

def right():
    global not_done, length, moves, locations, not_dead
    if not_done or snake.heading() == 180:
        return
    if not not_dead:
        return
    not_done = True
    snake.setheading(0)
    everything()
    not_done = False
def left():
    global not_done, length, moves, locations, not_dead
    if not_done or snake.heading() == 0:
        return
    if not not_dead:
        return
    not_done = True
    snake.setheading(180)
    everything()
    not_done = False
def up():
    global not_done, length, moves, locations, not_dead
    if not_done or snake.heading() == 270:
        return
    if not not_dead:
        return
    not_done = True
    snake.setheading(90)
    everything()
    not_done = False
def down():
    global not_done, length, moves, locations, not_dead
    if not_done or snake.heading() == 90:
        return
    if not not_dead:
        return
    not_done = True
    snake.setheading(270)
    everything()
    not_done = False

def spawn_apple():
    y = random.randrange(-10,10)
    x = random.randrange(-12,12)
    apple.penup()
    apple.goto(x * 50 + 25,y * 50 + 25)
    apple.showturtle()
    #spawns apple
def everything():
    # happens every tick or in this case whenever you move because I don't like time thingy and didn't want to do it
    global length, moves, not_done, locations, not_dead
    shadows()
    if moves == 0: spawn_apple()
    # beginning apple
    if len(locations) >= length:
        locations.pop(0)
    window.tracer(1)
    snake.fd(distance)
    locations.append((round(snake.xcor(),1), round(snake.ycor(),1)))
    # since they are floats the thing where num is close but not exact happened, so I just round
    if (round(snake.xcor(),1) == (round(apple.xcor(),1))) and (round(snake.ycor(),1) == (round(apple.ycor(),1))):
        spawn_apple()
        length += 1
        # when eat apple spawn new one and get longer
    if snake.xcor() >= 600 or snake.xcor() <= -600 or snake.ycor() >= 500 or snake.ycor() <= -500:
        not_dead = False
        # checks if out of bounce

    snake_location = (round(snake.xcor(),1), round(snake.ycor(),1))
    for i in range(len(locations) - 1):
        if snake_location == locations[i]:
            not_dead = False
    # checks if it hits itself

    moves += 1

window.onkeypress(down, "Down")
window.onkeypress(left, "Left")
window.onkeypress(right, "Right")
window.onkeypress(up, "Up")
window.listen()

window.listen()
turtle.done()
