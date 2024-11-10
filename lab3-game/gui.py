import tkinter as tk
from board import Board
from player import Player


class GameGUI:
    def __init__(self, root, rows=5, cols=5, obstacle_ratio=0.2, cell_size=50):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.obstacle_ratio = obstacle_ratio
        self.board = Board(rows, cols, obstacle_ratio)
        self.player = Player(self.board.start, self.board)
        self.path = [self.player.get_position()]

        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.canvas.pack()

        self.draw_board()
        self.draw_player()

        control_frame = tk.Frame(root)
        control_frame.pack()

        btn_up = tk.Button(control_frame, text="Góra", command=lambda: self.move_player('up'))
        btn_up.grid(row=0, column=1)

        btn_left = tk.Button(control_frame, text="Lewo", command=lambda: self.move_player('left'))
        btn_left.grid(row=1, column=0)

        btn_down = tk.Button(control_frame, text="Dół", command=lambda: self.move_player('down'))
        btn_down.grid(row=1, column=1)

        btn_right = tk.Button(control_frame, text="Prawo", command=lambda: self.move_player('right'))
        btn_right.grid(row=1, column=2)

        btn_reset = tk.Button(control_frame, text="Reset", command=self.reset_game)
        btn_reset.grid(row=2, column=1)

        self.status_label = tk.Label(root, text="Ruch: ")
        self.status_label.pack()

        self.root.bind("<Up>", lambda event: self.move_player('up'))
        self.root.bind("<Down>", lambda event: self.move_player('down'))
        self.root.bind("<Left>", lambda event: self.move_player('left'))
        self.root.bind("<Right>", lambda event: self.move_player('right'))

        self.root.focus_set()

    def draw_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                cell = self.board.grid[r][c]
                if cell == 'A':
                    color = 'green'
                elif cell == 'B':
                    color = 'red'
                elif cell == 'X':
                    color = 'black'
                else:
                    color = 'white'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')

    def draw_player(self):
        r, c = self.player.get_position()
        x1 = c * self.cell_size + 5
        y1 = r * self.cell_size + 5
        x2 = x1 + self.cell_size - 10
        y2 = y1 + self.cell_size - 10
        self.player_icon = self.canvas.create_oval(x1, y1, x2, y2, fill='blue')

    def update_player_position(self):
        r, c = self.player.get_position()
        x1 = c * self.cell_size + 5
        y1 = r * self.cell_size + 5
        x2 = x1 + self.cell_size - 10
        y2 = y1 + self.cell_size - 10
        self.canvas.coords(self.player_icon, x1, y1, x2, y2)

    def move_player(self, direction):
        success, message = self.player.move(direction)
        self.status_label.config(text=message)
        if success:
            self.path.append(self.player.get_position())
            self.update_player_position()
            if self.player.get_position() == self.board.stop:
                self.status_label.config(text="Dotarłeś do celu!")

    def reset_game(self):
        self.canvas.delete("all")
        self.board = Board(self.rows, self.cols, self.obstacle_ratio)
        self.player = Player(self.board.start, self.board)
        self.path = [self.player.get_position()]
        self.draw_board()
        self.draw_player()
        self.status_label.config(text="Gra zresetowana.")


def main():
    root = tk.Tk()
    root.title("TAU - Gra Planszowa")
    gui = GameGUI(root, rows=9, cols=9, obstacle_ratio=0.2)
    root.mainloop()


if __name__ == "__main__":
    main()
