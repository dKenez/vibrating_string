from graphics import *
from Chord import Chord
import time

my_chord = Chord(10, 1, 0.1, 1000, 20, (2, 2), (5, 3), (7, 1.5))

win_width = 800
win_height = 800
t_inc = 0.1
sim_speed = 1

win = GraphWin("Rezgő húr", win_width, win_height, autoflush=False)
win.setBackground("black")

win.setCoords(-my_chord.length * (1 / 8), -my_chord.length * (5 / 8), my_chord.length * (9 / 8), my_chord.length * (5 / 8))

# my_chord.refresh()

sim_start_t = time.time()
curr_t = sim_start_t
t = 0
print(my_chord.fx)
print()
print(my_chord.E_k)
print(my_chord.alpha_k)

while win.checkMouse() is None:  # main program loop
    dt = time.time() - curr_t
    if dt > t_inc:
        curr_t = time.time()
        dt = t_inc * sim_speed
        t += dt

        win.delete("all")

        prev_point = Point(*next(my_chord.shape))
        for i in range(my_chord.res - 1):

            point = Point(*next(my_chord.shape))
            line = Line(prev_point, point)
            line.setFill("white")
            line.setWidth(1)
            line.draw(win)
            prev_point = point
        my_chord.refresh(t)


# win.getMouse() # Pause to view result
win.close()  # Close window when done
