__version__ = "1.1"
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
        ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from random import randint



gong = SoundLoader.load('audio/gong_fade_2.wav')

chop_1 = SoundLoader.load('audio/chop1.wav')
chop_3 = SoundLoader.load('audio/chop3.wav')
chop_4 = SoundLoader.load('audio/chop4.wav')
chop_7 = SoundLoader.load('audio/chop7.wav')
chop_9 = SoundLoader.load('audio/chop9.wav')

chops = [chop_1, chop_3, chop_4, chop_7, chop_9]

chops_len = len(chops)-1
def chop_now():
    chops[randint(0, chops_len)].play()

side_chop=SoundLoader.load('audio/chop_s.wav')
def chop_side():
    side_chop.play()

goal_1 = SoundLoader.load('audio/goal/goal1.wav')
goal_2 = SoundLoader.load('audio/goal/goal2.wav')
goal_3 = SoundLoader.load('audio/goal/goal3.wav')
goal_4 = SoundLoader.load('audio/goal/goal4.wav')
goal_5 = SoundLoader.load('audio/goal/goal5.wav')
goal_6 = SoundLoader.load('audio/goal/goal6.wav')
goal_7 = SoundLoader.load('audio/goal/goal7.wav')
goal_9 = SoundLoader.load('audio/goal/goal9.wav')
goal_10 = SoundLoader.load('audio/goal/goal10.wav')
goal_11 = SoundLoader.load('audio/goal/goal11.wav')
goal_12 = SoundLoader.load('audio/goal/goal12.wav')
goal_13 = SoundLoader.load('audio/goal/goal13.wav')
goal_15 = SoundLoader.load('audio/goal/goal15.wav')
goal_16 = SoundLoader.load('audio/goal/goal16.wav')
goal_17 = SoundLoader.load('audio/goal/goal17.wav')

goals = [goal_1, goal_2, goal_3, goal_4, goal_5, goal_6, goal_7, goal_9, goal_10, goal_11, goal_12, goal_13, goal_15, goal_16, goal_17]

goals_len = len(goals)-1
def goal_now():
    goals[randint(0, chops_len)].play()

break_1 = SoundLoader.load('audio/break/break1.wav')
break_2 = SoundLoader.load('audio/break/break2.wav')
break_3 = SoundLoader.load('audio/break/break3.wav')
break_4 = SoundLoader.load('audio/break/break4.wav')
break_5 = SoundLoader.load('audio/break/break5.wav')
break_6 = SoundLoader.load('audio/break/break6.wav')
break_7 = SoundLoader.load('audio/break/break7.wav')
break_8 = SoundLoader.load('audio/break/break8.wav')
break_9 = SoundLoader.load('audio/break/break9.wav')

breaks = [break_1, break_2, break_3, break_4, break_5, break_6, break_7, break_8, break_9] 

breaks_len = len(breaks)-1
def break_now():
    breaks[randint(0,breaks_len)].play()

class PongBall(Widget):
    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # paddle touch count
    touched = NumericProperty(0)

    # ball speed multiplyer
    speeder = NumericProperty(4)

    limiter = NumericProperty(40)
    limiter_y = NumericProperty(20)


    # ''move'' function will move the ball one step. this
    # will be called in equal intervals to animate the ball
    def move(self):
        if self.velocity_y < self.limiter_y*-1:
            self.velocity_y = self.limiter_y*-1
        if self.velocity_y > self.limiter_y:
            self.velocity_y = self.limiter_y
        if self.speeder > self.limiter:
            self.speeder=self.limiter
        if self.velocity_x > 0:
            self.velocity_x = self.speeder

        if self.velocity_x < 0:
            self.velocity_x = self.speeder*-1

        #print "velocity_x: %d" % self.velocity_x
        #print "touched: %d" % self.touched
        #print "speeder: %d" % self.speeder
        #print "velocity_y: %d" % self.velocity_y
        self.pos = Vector(*self.velocity) + self.pos

class TeamLeft(Widget):
    pass

class TeamRight(Widget):
    pass


class PongGame(Widget):

    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    team1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    team2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel
    
    def update(self, dt):
        # call ball.move and other stuff
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce off top and bottom
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            chop_side()
            self.ball.velocity_y *= -1

        # if touch goal area to score points
        if self.ball.x < self.x:
            self.serve_ball(vel=(4, 0))
            self.player2.score += 1
            self.ball.speeder = 4
            break_now()
            goal_now()
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))
            self.ball.speeder = 4
            break_now()
            goal_now()

        ## bounce off left and right
        #if (self.ball.x < 0) or (self.ball.right > self.width):
            #self.ball.velocity_x *= -1

    def on_touch_move(self, touch):
        if touch.x < self.width/3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width/3:
            self.player2.center_y = touch.y

class PongPaddle(Widget):

    score = NumericProperty(0)

    def bounce_ball(self, ball):

        if self.collide_widget(ball):
            if ball.touched >= 5:
                ball.speeder += 2
                ball.touched = 0

            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            chop_now()
            vel = bounced * ball.speeder
            ball.velocity = vel.x, vel.y + offset
            ball.touched += 1



class PongPaddleRight(PongPaddle):
    pass


class PongPaddleLeft(PongPaddle):
    pass



class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        gong.play()
        return game

if __name__ == '__main__':
    PongApp().run()
