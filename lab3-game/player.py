class Player:
    def __init__(self, start_position, board):
        self.position = start_position
        self.board = board

    def move(self, direction):
        direction_map = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }

        if direction not in direction_map:
            return False, "Nieznany kierunek ruchu."

        delta = direction_map[direction]
        new_position = (self.position[0] + delta[0], self.position[1] + delta[1])

        if not self.board.is_within_bounds(new_position):
            return False, "Wyjście poza planszę."
        if self.board.is_obstacle(new_position):
            return False, "Napotkano przeszkodę."

        self.position = new_position
        return True, "Ruch wykonany."

    def get_position(self):
        return self.position
