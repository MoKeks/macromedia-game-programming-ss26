#gamestate.py
# state machine for game states

#4 Game states
class Game:
    STATES = {"title", "playing", "shop", "gameover"}

    def __init__ (self):
        self.state = "title"
    
    def update(self, dt):
        if   self.state == "title":    self._update_title(dt)
        elif self.state == "playing":  self._update_playing(dt)
        elif self.state == "shop":     self._update_shop(dt)
        elif self.state == "gameover": self._update_gameover(dt)

    def change_state(self, new):
        assert new in self.STATES, f"unknown state: {new}"   # Unit 8
        print(f"[state] {self.state} -> {new}")              # free log
        self.state = new

