class PongGame:
    def __init__(self):
        # settings
        self.map_width = 720
        self.map_height = 480
        self.ball_speed = 5
        self.ball_radius = 10
        self.move_speed = 5
        self.winning_score = 5
        self.paddle_height = 50
        self.paddle_speed = 5
        self.paddle_width = 10

        self.player1_id = ''
        self.player2_id = ''

        self.player1_dy = 0
        self.player2_dy = 0

        self.ball_dir = [1, 1]  # x, y
        self.init_position()

        self.score = [0, 0]  # p1,p2

    def move_player(self, player_id, direction):
        if player_id == self.player1_id:
            self.player1_dy = direction
        elif player_id == self.player2_id:
            self.player2_dy = direction

    def stop_player(self, player_id):
        if player_id == self.player1_id:
            self.player1_dy = 0
        elif player_id == self.player2_id:
            self.player2_dy = 0

    def next_frame(self) -> dict:
        self.check_paddle_collision()
        self.check_wall_collision()

        self.ball_coords[0] += self.ball_speed * self.ball_dir[0]
        self.ball_coords[1] += self.ball_speed * self.ball_dir[1]

        self.player1_coords[1] += self.move_speed * self.player1_dy
        self.player2_coords[1] += self.move_speed * self.player2_dy

        return {
            "ball_coords": self.ball_coords,
            "player1_coords": self.player1_coords,
            "player2_coords": self.player2_coords,
            "score": self.score,
        }

    def check_wall_collision(self):
        if self.ball_coords[0] <= -1 * self.map_width // 2:
            self.goal(2)
        if self.ball_coords[0] >= self.map_width // 2:
            self.goal(1)
        if self.ball_coords[1] <= -1 * self.map_height // 2 or self.ball_coords[1] >= self.map_height // 2:
            self.ball_dir[1] *= -1

    def check_paddle_collision(self):
        if self.player1_coords[0] - self.paddle_width // 2 - self.ball_radius <= self.ball_coords[0] <= self.player1_coords[0] + self.paddle_width // 2 + self.ball_radius \
                and self.player1_coords[1] - self.paddle_height // 2 - self.ball_radius <= self.ball_coords[1] <= self.player1_coords[1] + self.paddle_height // 2 + self.ball_radius:
            self.ball_dir[0] *= -1
        if self.player2_coords[0] - self.paddle_width // 2 - self.ball_radius <= self.ball_coords[0] <= self.player2_coords[0] + self.paddle_width // 2 + self.ball_radius \
                and self.player2_coords[1] - self.paddle_height // 2 - self.ball_radius <= self.ball_coords[1] <= self.player2_coords[1] + self.paddle_height // 2 + self.ball_radius:
            self.ball_dir[0] *= -1

    def goal(self, player):
        self.init_position()

        if player == 1:
            self.score[0] += 1
        elif player == 2:
            self.score[1] += 1

        if self.score[0] > self.winning_score:
            pass
        elif self.score[1] > self.winning_score:
            pass


    def init_position(self):
        self.ball_coords = [0, 0]  # x, y

        self.player1_coords = [-1 * self.map_width // 2 + 20, 0]
        self.player2_coords = [self.map_width // 2 - 20, 0]