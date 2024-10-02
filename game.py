import tkinter as tk
import random

# Constants
WIDTH = 600
HEIGHT = 400
SEGMENT_SIZE = 20
INITIAL_SNAKE_LENGTH = 3

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")

        # Initialize score and high score
        self.score = 0
        self.high_score = 0
        self.is_game_over = False
        
        # Create UI components
        self.score_label = tk.Label(master, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.pack()
        
        self.high_score_label = tk.Label(master, text=f"High Score: {self.high_score}", font=("Arial", 16))
        self.high_score_label.pack()

        self.restart_button = tk.Button(master, text="Restart", command=self.restart_game, font=("Arial", 16))
        self.restart_button.pack()

        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.snake = []
        self.direction = "Right"

        self.create_snake()
        self.food = self.create_food()
        
        # Bind keyboard events
        self.master.bind("<KeyPress>", self.change_direction)

        # Start game loop
        self.move_snake()

    def create_snake(self):
        self.snake.clear()
        self.direction = "Right"
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")

        for i in range(INITIAL_SNAKE_LENGTH):
            self.add_segment()

        self.is_game_over = False

    def add_segment(self):
        if len(self.snake) == 0:
            x = SEGMENT_SIZE
            y = HEIGHT // 2
        else:
            x, y = self.get_segment_coordinates(self.snake[-1])
        segment = self.canvas.create_oval(x, y, x + SEGMENT_SIZE, y + SEGMENT_SIZE, fill="green")
        self.snake.append(segment)

    def create_food(self):
        while True:
            x = random.randint(0, (WIDTH - SEGMENT_SIZE) // SEGMENT_SIZE) * SEGMENT_SIZE
            y = random.randint(0, (HEIGHT - SEGMENT_SIZE) // SEGMENT_SIZE) * SEGMENT_SIZE
            if not any(self.get_segment_coordinates(segment) == (x, y) for segment in self.snake):
                break
        return self.draw_mouse(x, y)

    def draw_mouse(self, x, y):
        # Draw a simple mouse shape using circles and a triangle
        body = self.canvas.create_oval(x, y, x + SEGMENT_SIZE, y + SEGMENT_SIZE, fill="gray", tags="food")
        ear1 = self.canvas.create_oval(x - SEGMENT_SIZE // 4, y, x, y + SEGMENT_SIZE // 2, fill="pink", tags="food")
        ear2 = self.canvas.create_oval(x + SEGMENT_SIZE, y, x + SEGMENT_SIZE + SEGMENT_SIZE // 4, y + SEGMENT_SIZE // 2, fill="pink", tags="food")
        return (body, ear1, ear2)

    def change_direction(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            if (self.direction == "Up" and event.keysym != "Down") or \
               (self.direction == "Down" and event.keysym != "Up") or \
               (self.direction == "Left" and event.keysym != "Right") or \
               (self.direction == "Right" and event.keysym != "Left"):
                self.direction = event.keysym

    def move_snake(self):
        if self.is_game_over:
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over", fill="white", font=("Arial", 24))
            return

        # Move the snake
        head_x, head_y = self.get_segment_coordinates(self.snake[0])
        if self.direction == "Up":
            head_y -= SEGMENT_SIZE
        elif self.direction == "Down":
            head_y += SEGMENT_SIZE
        elif self.direction == "Left":
            head_x -= SEGMENT_SIZE
        elif self.direction == "Right":
            head_x += SEGMENT_SIZE

        # Check for collision with walls
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or self.check_collision(head_x, head_y):
            self.is_game_over = True
            self.move_snake()
            return

        # Move the snake segments
        new_head = self.canvas.create_oval(head_x, head_y, head_x + SEGMENT_SIZE, head_y + SEGMENT_SIZE, fill="green")
        self.snake.insert(0, new_head)

        # Check for food collision
        if self.check_food_collision(head_x, head_y):
            self.canvas.delete("food")  # Clear the mouse shape
            self.food = self.create_food()
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")

            # Update high score
            if self.score > self.high_score:
                self.high_score = self.score
                self.high_score_label.config(text=f"High Score: {self.high_score}")
        else:
            tail = self.snake.pop()
            self.canvas.delete(tail)

        self.master.after(100, self.move_snake)

    def check_food_collision(self, head_x, head_y):
        food_coords = self.canvas.coords(self.food[0])  # Check the first part of the mouse shape
        return head_x == food_coords[0] and head_y == food_coords[1]

    def check_collision(self, head_x, head_y):
        for segment in self.snake[1:]:
            segment_coords = self.canvas.coords(segment)
            if head_x == segment_coords[0] and head_y == segment_coords[1]:
                return True
        return False

    def get_segment_coordinates(self, segment):
        return self.canvas.coords(segment)[0], self.canvas.coords(segment)[1]

    def restart_game(self):
        self.canvas.delete("all")  # Clear the canvas
        self.create_snake()         # Reset snake and food
        self.food = self.create_food()
        self.move_snake()           # Start moving the snake again

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
