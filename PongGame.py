import kivy
kivy.require('1.10.0')


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock
from random import randint

class PongGame(Widget):

    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

   

    def serve_ball(self, vel=(4,0)):
        self.ball.center = self.center

        ## Create array to regulate serve angles for SERVE_BALL()
        angles1 = []
        i = 0
        while i < 65:
            angles1.append(i)
            i += 1

        angles2 = []
        i = 115
        count = 0
        while i < 180:
            angles2.append(i)
            count += 1
            i += 1
        serveDir = []
        serveDir.append(angles1)
        serveDir.append(angles2)


        serveIndex = randint(0,1)
        self.ball.velocity = Vector(4,0).rotate(serveDir[serveIndex][randint(0, 64)])

    def update(self, dt):
        self.ball.move()

        # Bounce off the walls
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)



        # keep score
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4,0))


    def on_touch_move(self, touch):
        if touch.x < self.width /3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y



class PongBall(Widget):


    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)


    # Move function will move the ball one step. This will be called in equal intervals to animate the ball

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos



class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset




class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game




if __name__ == '__main__':
    PongApp().run()
