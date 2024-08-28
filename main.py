from tkinter import *
import random

# Constants
GAME_WIDTH = 700
GAME_HEIGHT = 600
SPEED = 150  # Slower speed
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "green"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"

# Snake class
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
            self.squares.append(square)

    def move(self, x, y):
        self.coordinates = [[x, y]] + self.coordinates[:-1]

        for i in range(len(self.squares)):
            x, y = self.coordinates[i]
            canvas.coords(self.squares[i], x, y, x + SPACE_SIZE, y + SPACE_SIZE)

    def grow(self):
        self.coordinates.append(self.coordinates[-1])
        square = canvas.create_rectangle(self.coordinates[-1][0], self.coordinates[-1][1], 
                                         self.coordinates[-1][0] + SPACE_SIZE, 
                                         self.coordinates[-1][1] + SPACE_SIZE, 
                                         fill=SNAKE_COLOR, tags="snake")
        self.squares.append(square)

# Food class
class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags="food")

# Game functions
def start_game():
    global score, direction, snake, food
    score = 0
    direction = "down"
    label.config(text=f"Score: {score}")
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    next_turn(snake, food)

def next_turn(snake, food):
    global score

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.move(x, y)

    if snake.coordinates[0] == food.coordinates:
        score += 1
        label.config(text=f"Score: {score}")
        snake.grow()
        canvas.delete("food")
        food = Food()

    if check_collision(snake):
        game_over()
    else:
        Window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction

def check_collision(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2, font=('consolas', 70), text="GAME OVER", fill="red")

# Main game window setup
Window = Tk()
Window.title("Snake Game")
Window.resizable(False, False)

score = 0
direction = "down"

label = Label(Window, text=f"Score: {score}", font=("consolas", 40))
label.pack()

canvas = Canvas(Window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

start_button = Button(Window, text="Start Game", command=start_game, font=("consolas", 20))
start_button.pack()

Window.update()

Window_width = Window.winfo_width()
Window_height = Window.winfo_height()
screen_width = Window.winfo_screenwidth()
screen_height = Window.winfo_screenheight()

x = (screen_width / 2) - (Window_width / 2)
y = (screen_height / 2) - (Window_height / 2)

Window.geometry(f"{Window_width}x{Window_height}+{int(x)}+{int(y)}")

# Controls
Window.bind("<Left>", lambda event: change_direction("left"))
Window.bind("<Right>", lambda event: change_direction("right"))
Window.bind("<Up>", lambda event: change_direction("up"))
Window.bind("<Down>", lambda event: change_direction("down"))

Window.mainloop()
