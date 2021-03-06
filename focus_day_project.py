import pymunk
from pymunk.pyglet_util import DrawOptions
from pyglet.window import key
from InputGUI import user_input
from pyglet.gl import *
from playsound import playsound
import random

'''DO NOT RUN THIS PROGRAM! RUN OutputGUI.py INSTEAD!'''

# Assign user selected # of sections and if user wants to split each simulation into smaller simulations.
tests_num = user_input[2]
multi_mode = 0
if user_input[4]:
    multi_mode = 1

# Prompt user to enter Height and Width in pixels, radius of circles, and define mass and bounce/elasticity.
H = user_input[1]
W = user_input[0]
radius = user_input[3]
if user_input[4]:
    radius *= 4
mass = 1
bounce = 0

# Given H and W of gym define coordinates of corners.
Bottom_Left_Corner = ((18285 - W) // 2, 8571 - H)
Bottom_Right_Corner = ((18285 - W) // 2 + W, 8571 - H)
Top_Left_Corner = ((18285 - W) // 2, 8571)
Top_Right_Corner = ((18285 - W) // 2 + W, 8571)

# Create Pyglet Window
window = pyglet.window.Window(1280, 720, "Softballs in the Gym Simulation", resizable=False)
background = pyglet.image.load('Background.png')
background_sprite = pyglet.sprite.Sprite(background)
background_sprite.scale_y = 43
background_sprite.scale_x = 61
options = DrawOptions()
glScalef(0.07, 0.07, 0.07)

# Declare space to put bodies/shapes in, define gravity.
space = pymunk.Space()
space.gravity = 0, -7000

# Make gym base
segment_shape_base = pymunk.Segment(space.static_body, (0, 0), (W, 0), 50)
segment_shape_base.color = (118, 82, 19, 0.69)
segment_shape_base.body.position = Bottom_Left_Corner
segment_shape_base.elasticity = bounce
segment_shape_base.friction = 1.0

# Make gym left wall
segment_shape_left = pymunk.Segment(space.static_body, (0, H), (0, 0), 50)
segment_shape_left.color = (118, 82, 19, 0.69)
segment_shape_left.body.position = Bottom_Left_Corner
segment_shape_left.elasticity = bounce
segment_shape_left.friction = 1.0

# Make gym right wall
segment_body_right = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_body_right.position = Bottom_Right_Corner
segment_shape_right = pymunk.Segment(segment_body_right, (0, H), (0, 0), 50)
segment_shape_right.color = (118, 82, 19, 0.69)
segment_shape_right.elasticity = bounce
segment_shape_right.friction = 1.0

# Make gym top wall
segment_body_top = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_body_top.position = Top_Left_Corner
segment_shape_top = pymunk.Segment(segment_body_top, (0, 0), (W, 0), 50)
segment_shape_top.color = (118, 82, 19, 0.69)
segment_shape_top.elasticity = bounce
segment_shape_top.friction = 1.0

# Make left funnel
segment_body_left_fun = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_body_left_fun.position = 0, 0
segment_shape_left_fun = pymunk.Segment(segment_body_left_fun, (0, 10285), Top_Left_Corner, 50)
segment_shape_left_fun.color = (118, 82, 19, 0.69)
segment_shape_left_fun.elasticity = bounce
segment_shape_left_fun.friction = 1.0

# Make right funnel
segment_body_right_fun = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_body_right_fun.position = 0, 0
segment_shape_right_fun = pymunk.Segment(segment_body_right_fun, (18285, 10285), Top_Right_Corner, 50)
segment_shape_right_fun.color = (118, 82, 19, 0.69)
segment_shape_right_fun.elasticity = bounce
segment_shape_right_fun.friction = 1.0

# add gym walls to and funnel walls to wall shapes so they won't get counted multiple times or deleted.
wall_shapes = [segment_shape_base, segment_shape_left, segment_shape_right, segment_shape_top, segment_shape_right_fun,
               segment_shape_left_fun, segment_shape_top]
# Add gym walls and funnel walls to space.
space.add(segment_shape_base, segment_shape_left, segment_shape_right, segment_body_right, segment_shape_left_fun,
          segment_body_left_fun, segment_shape_right_fun, segment_body_right_fun)

# define variables used later.
checked_shapes = []
new_balls = []
previous_new_balls = []
tests = []
tests_completed = 0
ball_spawning = False
ball_cleanup = 0
auto = False
timer = 0
stop_time = 0
auto_auto = False
timer_length = 120
speedup = 0


def make_ball(x, y):  # Makes ball from given coordinates and adds it to space
    circle_moment = pymunk.moment_for_circle(mass, 0, radius)
    circle_body = pymunk.Body(mass, circle_moment)
    circle_body.position = x, y
    circle_shape = pymunk.Circle(circle_body, radius)
    circle_shape.color = (212, 255, 40, 1)
    circle_shape.elasticity = bounce
    circle_shape.friction = 1.0
    space.add(circle_body, circle_shape)


def random_ball(status):  # Generate a random ball between the specified coordinates.
    if status:
        make_ball(random.randint((18285 - W) // 2 + 200, (18285 - W) // 2 + W - 200), 11000)


def cleanup_tests():
    global tests
    tests_without_zeros = tests.copy()
    while 0 in tests_without_zeros:
        tests_without_zeros.remove(0)
    result = []
    if len(tests_without_zeros) > 1:
        average = tests_without_zeros[0]
        for i in range(len(tests_without_zeros)):
            if tests_without_zeros[i] / average >= 0.94:
                result.append(tests_without_zeros[i])
    return result


@window.event  # draw the space in window
def on_draw():
    window.clear()
    background_sprite.draw()
    space.debug_draw(options)


@window.event  # when the user closes the window stop the simulation
def on_close():
    window.close()


# noinspection PyUnusedLocal
@window.event
def on_mouse_press(x, y, button, modifiers):  # When the mouse is clicked, add a new shape to space at mouse coords.
    make_ball(x * 14.285, y * 14.285)


# noinspection PyUnusedLocal
@window.event
def on_key_press(symbol, modifiers):  # If a key is pressed...
    global ball_spawning, auto, new_balls, auto_auto, ball_cleanup, tests, speedup, timer_length

    if symbol == key.T and segment_shape_top not in space.shapes:  # If T, add the top wall if not already there.
        space.add(segment_shape_top, segment_body_top)
    elif symbol == key.T and segment_shape_top in space.shapes:  # If T, remove top wall if already there.
        space.remove(segment_shape_top.body, segment_shape_top)

    if symbol == key.B:  # If B, toggle ball_spawning variable (controls random_ball function called in update).
        ball_spawning = not ball_spawning

    if symbol == key.C:  # If C, clear all balls.
        for shape in space.shapes:
            if shape not in wall_shapes:
                space.remove(shape.body, shape)
        checked_shapes.clear()

    if symbol == key.Q:
        auto_auto = not auto_auto
        ball_cleanup = 0
        print("Auto Auto mode enabled")
        if segment_shape_top in space.shapes:
            space.remove(segment_shape_top, segment_body_top)
        ball_spawning = not ball_spawning
        auto = not auto

    if symbol == key.A:  # If A, activate auto mode, remove top wall if there, toggle on ball_spawning.
        print("Auto mode enabled")
        if segment_shape_top in space.shapes:
            space.remove(segment_shape_top, segment_body_top)
        ball_spawning = not ball_spawning
        auto = not auto

    if symbol == key.D:  # If D, clear all balls above top wall.
        for shape in space.shapes:
            if shape.body.position.y >= 8571 and shape not in wall_shapes:
                space.remove(shape.body, shape)
                new_balls.remove(shape)

    if symbol == key.R:  # if R, manually record number of balls in gym to tests.
        tests.append(len(checked_shapes))
        print("Manually recorded test: " + str(len(checked_shapes)))

    if symbol == key.F:  # If F, close window and print tests.
        auto_auto = False
        auto = False
        ball_spawning = False
        window.close()
        print("Final test results: " + str(tests))

    if symbol == key.S:
        if speedup == 0:
            speedup = 0.05
            timer_length = 60
        else:
            speedup = 0
            timer_length = 120

    if symbol == key.GRAVE:
        playsound("noise.mp3", False)


def update(dt):  # This function is called every 1/60 of a second.
    global checked_shapes, ball_spawning, previous_new_balls, new_balls, auto, timer, ball_cleanup, stop_time, \
        auto_auto, tests, tests_completed, multi_mode
    space.step(dt + speedup)  # Step forward the physics simulation, speedup simulation if user specified.
    changed_list = False  # Set changed_list to false (If true, print number of balls in checked_shapes).

    if len(tests) > 1:
        tests = cleanup_tests().copy()  # Remove outliers from tests.

    # If user specified number of tests and that number has been achieved, close the window and print results.
    if tests_completed == tests_num and tests_num != 0:
        window.close()
        auto_auto = False
        auto = False
        ball_spawning = False
        print("Final test results: " + str(tests))

    timer = (timer + 1) % timer_length  # Progress timer forward by one.

    for shape in space.shapes:  # for loop checks all balls and adds or removes them from lists.
        # if ball in gym add to checked_shapes
        if shape.body.position.y <= 8571 - radius and shape not in checked_shapes and shape not in wall_shapes:
            checked_shapes.append(shape)
            changed_list = True
        # If ball above gym height add to new_balls
        if shape.body.position.y > 8571 - radius and shape not in new_balls and shape not in wall_shapes:
            new_balls.append(shape)
        # If ball in new_balls and below gym height, remove from new_balls
        if shape.body.position.y < 8571 and shape in new_balls:
            new_balls.remove(shape)
        # If ball is below gym height remove from space and checked_shapes.
        if shape.body.position.y < (8571 - H) and shape not in wall_shapes:
            if shape in checked_shapes:
                checked_shapes.remove(shape)
            space.remove(shape.body, shape)
            changed_list = True
    if changed_list:  # If any balls were taken away or added to checked_shapes, print checked_shapes length.
        print(str(len(checked_shapes)) + " balls")

    random_ball(ball_spawning)  # Spawn a random_ball if ball_spawning is True.

    # If auto mode is active and 1 second has elapsed, check for overflow.
    if (timer % timer_length == 0 or timer % timer_length == 60) and auto and len(previous_new_balls) > 1:
        stop_time = timer
        print("checking for auto mode overflow...")
        # for loop checks balls from 2 seconds ago that are above top wall with current balls above top wall.
        for i in range(len(previous_new_balls)):
            # Check every ball from 2 seconds ago to see if still above and within 200px of previous coordinate.
            # Error: List index out of range
            current_previous_ball = (
                round(previous_new_balls[i].body.position.x), round(previous_new_balls[i].body.position.y))
            for j in range(len(new_balls)):
                current_new_ball = (round(new_balls[j].body.position.x), round(new_balls[j].body.position.y))
                if abs(current_new_ball[0] - current_previous_ball[0]) <= 200 and abs(
                        current_new_ball[1] - current_previous_ball[1]) <= 200 and auto:
                    # If so, deactivate ball_spawning, deactivate auto mode, clear new_balls, clear previous_new_balls.
                    print("Auto mode turning off...")
                    ball_spawning = False
                    auto = False
                    new_balls.clear()
                    previous_new_balls.clear()
                    for shape in space.shapes:  # Remove all balls above top wall.
                        if shape.body.position.y >= 8300 and shape not in wall_shapes:
                            space.remove(shape.body, shape)
                    space.add(segment_shape_top, segment_body_top)
                    ball_cleanup = 1  # Activate ball_cleanup.
                    break
            else:
                continue
            break
    # Every two seconds (right after checking for overflow) set previous_new_balls equal to new_balls
    if timer == 1 or timer % timer_length == 60:
        previous_new_balls = new_balls.copy()

    # after 0.5 seconds have passed since auto mode deactivation, remove top wall.
    if ball_cleanup == 1 and timer == (stop_time + 29) % timer_length:
        space.remove(segment_shape_top, segment_body_top)
        ball_cleanup += 1
    # after 2 seconds have passed, add top wall, remove balls above wall.
    if ball_cleanup == 2 and timer == (
            stop_time + 119) % timer_length:
        space.add(segment_shape_top, segment_body_top)
        for shape in space.shapes:
            if shape.body.position.y >= 8571 and shape not in wall_shapes:
                space.remove(shape.body, shape)
        ball_cleanup += 1
    # after 3.5(?) seconds have elapsed, log tests and restart auto if auto_auto.
    if ball_cleanup == 3 and timer == (stop_time - 30) % timer_length:
        if multi_mode > 0:
            tests_completed += 0.25
            if multi_mode == 1:
                tests.append(len(checked_shapes))
            if multi_mode > 1:
                tests[-1] += len(checked_shapes)
            multi_mode = multi_mode % 4 + 1
        else:
            tests_completed += 1
            tests.append(len(checked_shapes))
        print("Test results: " + str(tests) + "\nSection " + str(len(tests)) + "/" + str(tests_num))
        if multi_mode > 0:
            print("Simulation " + str(multi_mode - 1) + "/4")
        checked_shapes.clear()
        new_balls.clear()
        previous_new_balls.clear()
        if auto_auto:
            for shape in space.shapes:
                if shape not in wall_shapes or shape == segment_shape_top:
                    space.remove(shape, shape.body)
            ball_spawning = not ball_spawning
            auto = True
        ball_cleanup = 0


# Driver code to update simulation
pyglet.clock.schedule_interval(update, 1.0 / 60)
pyglet.app.run()
