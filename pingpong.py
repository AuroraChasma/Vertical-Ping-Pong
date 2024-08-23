#Ping Pong Game
import pygame as pg
import time


pg.init()
pg.font.init()


screen_width = 800
screen_height = 500
win = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Ping Pong')

fps = 60

WHITE = (255,255,255)
BLACK = (0,0,0)


ball_width = 20
ball_height = 20
screen_middle = (screen_width//2-ball_width//2, screen_height//2 - ball_height//2)

paddle_width = 20
paddle_height = 100

player_left_score = 0
player_right_score = 0

player_left_score_font = pg.font.SysFont('comicsans', 50)
player_right_score_font = pg.font.SysFont('comicsans', 50)

winner_font = pg.font.SysFont('comicsans', 70)
# winner = None





class Ball(pg.sprite.Sprite):
    
    def __init__(self, x, y,  velocity):
        pg.sprite.Sprite.__init__(self)
        self.vel = [velocity, velocity] # x and y velocities are the same
        self.ball_surface = pg.Surface((ball_width, ball_height))
        self.ball_surface.fill(WHITE)
        self.ball_rect = self.ball_surface.get_rect(topleft=(x, y))
        
    def update(self, player_left_score, player_right_score):
        self.ball_rect.x += self.vel[0]
        self.ball_rect.y += self.vel[1]
        
        if self.ball_rect.right >= screen_width:
            player_left_score += 1
            self.ball_rect.x = screen_middle[0]
            self.ball_rect.y = screen_middle[1]

        elif self.ball_rect.left <= 0:
            player_right_score += 1
            self.ball_rect.x = screen_middle[0]
            self.ball_rect.y = screen_middle[1]
            
        elif self.ball_rect.top <= 0:
            self.vel[1] = -self.vel[1]
            
        elif self.ball_rect.bottom >= screen_height:
            self.vel[1] = -self.vel[1]
            
        return player_left_score, player_right_score
        
        
        
        
class Paddle(pg.sprite.Sprite):
    
    def __init__(self, x, y, velocity, identity):
        pg.sprite.Sprite.__init__(self)
        self.vel = velocity
        self.identity = identity
        self.paddle_surface = pg.Surface((paddle_width, paddle_height))
        self.paddle_surface.fill(WHITE)
        self.paddle_rect = self.paddle_surface.get_rect(topleft=(x, y))
        
        
    def update(self, key_pressed, ball):
        
        if key_pressed[pg.K_w] and self.paddle_rect.top > 0 and self.identity == 'left':
            self.paddle_rect.y -= self.vel
            
        elif key_pressed[pg.K_s] and self.paddle_rect.bottom < screen_height and self.identity == 'left':
            self.paddle_rect.y += self.vel
            
        elif key_pressed[pg.K_UP] and self.paddle_rect.top > 0 and self.identity == 'right':
            self.paddle_rect.y -= self.vel
            
        elif key_pressed[pg.K_DOWN] and self.paddle_rect.bottom < screen_height and self.identity == 'right':
            self.paddle_rect.y += self.vel
            
            
            
        if self.paddle_rect.colliderect(ball.ball_rect):
            ball.vel[0] = -ball.vel[0]
            

            
            

def draw_on_window(win, ball, paddle_left, paddle_right, player_left_score, player_right_score, winner=None,time_sleep=0):
    player_left_score_text = player_left_score_font.render(f"{player_left_score}", 1, WHITE)
    player_right_score_text = player_right_score_font.render(f"{player_right_score}", 1, WHITE)
    winner_text = winner_font.render(f"{winner}", 1, WHITE)
    
    win.fill(BLACK)
    win.blit(ball.ball_surface, (ball.ball_rect.x, ball.ball_rect.y))
    win.blit(paddle_left.paddle_surface, (paddle_left.paddle_rect.x,paddle_left.paddle_rect.y))
    win.blit(paddle_right.paddle_surface, (paddle_right.paddle_rect.x,paddle_right.paddle_rect.y))
    pg.draw.line(win, WHITE, (screen_width//2, 0), (screen_width//2, screen_height))
    win.blit(player_left_score_text, (80, 20))
    win.blit(player_right_score_text, (720, 20))
    
    if winner != None:
        win.blit(winner_text, (screen_width//2 - winner_text.get_width()//2, screen_height//2 - winner_text.get_height()//2))
        
    pg.display.update()
    

def reset_game(ball, paddle_left, paddle_right, player_left_score, player_right_score):
    ball.ball_rect.x = screen_middle[0]
    ball.ball_rect.y = screen_middle[1]
    paddle_left.paddle_rect.x = 50
    paddle_left.paddle_rect.y = screen_height//2-paddle_height//2
    paddle_right.paddle_rect.x = 750
    paddle_right.paddle_rect.y = screen_height//2-paddle_height//2
    player_left_score = 0
    player_right_score = 0
    game_over = False
    winner = None
    return ball.ball_rect.x, ball.ball_rect.y, paddle_left.paddle_rect.x, paddle_left.paddle_rect.y, paddle_right.paddle_rect.x, paddle_right.paddle_rect.y, player_left_score, player_right_score, game_over, winner
    


def main(player_left_score, player_right_score):
    
    ball = Ball(screen_width//2-ball_width//2, screen_height//2-ball_height//2, 5)
    paddle_left = Paddle(50, screen_height//2-paddle_height//2, 10, 'left')
    paddle_right = Paddle(750, screen_height//2-paddle_height//2, 10, 'right')
    clock = pg.time.Clock()
    is_updating = False
    game_over = False
    run = True
    
    
    
    while run:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    is_updating = True
     
        
        if is_updating != False and game_over != True:
            key_pressed = pg.key.get_pressed()
            
            paddle_left.update(key_pressed, ball)
            paddle_right.update(key_pressed, ball)
            
            player_left_score, player_right_score = ball.update(player_left_score, player_right_score)
            
            
            if player_left_score == 5:
                winner = "Left Player Wins"
                is_updating = False
                game_over = True
            elif player_right_score == 5:
                winner = 'Right Player Wins'
                is_updating = False
                game_over = True
            
            if game_over == True:
                ball.ball_rect.x, ball.ball_rect.y, paddle_left.paddle_rect.x,paddle_left.paddle_rect.y,paddle_right.paddle_rect.x, paddle_right.paddle_rect.y, player_left_score, player_right_score, game_over, winner = reset_game(ball, paddle_left, paddle_right, player_left_score,player_right_score)
            
            
                
            
        draw_on_window(win, ball, paddle_left, paddle_right, player_left_score, player_right_score)
        

if __name__ == '__main__':
    main(player_left_score, player_right_score)

pg.quit()