from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class Goal(Widget):
    pass


class Wall(Widget):
    def bounce_off(self, player):
        if self.collide_widget(player):
            vx, vy = player.velocity
            offset = (player.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            player.velocity = vel.x, vel.y + offset


class Floor(Widget):
    def bounce_off(self, player):
        if self.collide_widget(player):
            vx, vy = player.velocity
            offset = (player.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1
            player.velocity = vel.x, vel.y + offset


class Player(Widget):
    score = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    can_double_jump = False

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def jump(self):
        self.velocity_y += 15


class JumpGame(Widget):
    player = ObjectProperty(None)
    floor1 = ObjectProperty(None)
    floor2 = ObjectProperty(None)
    goal = ObjectProperty(None)
    wall = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        self.player.center = self.center
        self.player.velocity = vel

    def update(self, dt):
        self.player.move()
        if self.player.y > self.y:
            self.gravity()

        # bounce ball off top bottom
        if self.player.y < 0:
            self.player.y += 1
            self.player.velocity_y = 0

        if self.player.top > self.top:
            self.player.y = self.top - 1
            self.player.velocity *= -1

        if self.player.x < self.x:
            self.player.velocity_x *= -1

        if self.player.right > self.width - 100:
            self.floor1.center_x -= self.player.velocity_x
            self.floor2.center_x -= self.player.velocity_x
            self.player.center_x -= self.player.velocity_x
            self.player.score += self.player.velocity_x
            self.goal.center_x -= self.player.velocity_x
            self.wall.center_x -= self.player.velocity_x

        if self.goal.center_x < self.player.center_x:
            self.player.velocity_x = 0

        if self.player.collide_widget(self.wall):
            self.player.velocity_x = 0
            self.wall.bounce_off(self.player)

    def on_touch_down(self, touch):
        if touch.button == "left":
            if self.player.center_y - self.player.height / 2 <= self.y + 5:
                self.player.jump()
                self.player.can_double_jump = True
            elif self.player.can_double_jump:
                self.player.velocity_y = 0
                self.player.jump()
                self.player.can_double_jump = False

    def gravity(self):
        self.player.velocity_y -= 0.5


class JumpApp(App):
    def build(self):
        game = JumpGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    JumpApp().run()
