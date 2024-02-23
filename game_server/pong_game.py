class PongGame:
    def __init__(self):
        # settings
        self.map_width = 720
        self.map_height = 480
        self.ball_speed = 5
        self.move_speed = 5
        self.winning_score = 5
        self.paddle_length = 50
        self.paddle_speed = 5

        self.player1_id = ''
        self.player2_id = ''

        self.ball_coords = [0, 0]  # x, y
        self.ball_dir = [1, 1]  # x, y

        self.player1_coords = [-1 * self.map_width // 2, 0]
        self.player2_coords = [self.map_width // 2, 0]

        self.score = [0, 0]  # p1, p2

    def move_player(self, player_id, direction):
        if player_id == self.player1_id:
            self.player1_coords[1] += direction * self.move_speed
        elif player_id == self.player2_id:
            self.player2_coords[1] += direction * self.move_speed

    def next_frame(self) -> dict:
        self.check_wall_collision()
        self.ball_coords[0] += self.ball_speed * self.ball_dir[0]
        self.ball_coords[1] += self.ball_speed * self.ball_dir[1]

        return {
            "ball_coords": self.ball_coords,
            "player1_coords": self.player1_coords,
            "player2_coords": self.player2_coords,
        }

    def check_wall_collision(self):
        if self.ball_coords[0] <= -1 * self.map_width // 2 or self.ball_coords[0] >= self.map_width // 2:
            self.ball_dir[0] *= -1
        if self.ball_coords[1] <= -1 * self.map_height // 2 or self.ball_coords[1] >= self.map_height // 2:
            self.ball_dir[1] *= -1

    def goal(self, player):
        self.ball_coords = [0, 0]  # x, y

        self.player1_coords = [-1 * self.map_width // 2, 0]
        self.player2_coords = [self.map_width // 2, 0]

        if player == 1:
            self.score[0] += 1
        elif player == 2:
            self.score[1] += 1

        if self.score[0] > self.winning_score:
            pass
        elif self.score[1] > self.winning_score:
            pass

