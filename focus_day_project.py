import pymunk
import pyglet
from pymunk.pyglet_util import DrawOptions
from pyglet.window import key

# Create Pyglet Window
window = pyglet.window.Window(1280, 720, "Pymunk Testing", resizable=False)
options = DrawOptions()
# Declare space to put bodies/shapes in
space = pymunk.Space()
space.gravity = 0, -1000
# Set mass and radius of circle
mass = 1
radius = 30
# Make segment
segment_shape_base = pymunk.Segment(space.static_body, (0, 0), (800, 0), 2)
segment_shape_base.body.position = 200, 70
segment_shape_base.elasticity = 0
segment_shape_base.friction = 1.0

segment_shape_left = pymunk.Segment(space.static_body, (0, 500), (0, 0), 2)
segment_shape_left.body.position = 200, 70
segment_shape_left.elasticity = 0
segment_shape_left.friction = 1.0

segment_body_right = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_body_right.position = 1000, 70
segment_shape_right = pymunk.Segment(segment_body_right, (0, 500), (0, 0), 2)
segment_shape_right.elasticity = 0
segment_shape_right.friction = 1.0

segment_body_top = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_body_top.position = 200, 570
segment_shape_top = pymunk.Segment(segment_body_top, (0, 0), (800, 0), 2)
segment_shape_top.elasticity = 0
segment_shape_top.friction = 1.0

checked_shapes = [segment_shape_base, segment_shape_left, segment_shape_right, segment_shape_top]
# Add shapes/bodies to space
space.add(segment_shape_base, segment_shape_left, segment_shape_right, segment_body_right)


@window.event  # draw the space when window opens (I think)
def on_draw():
    window.clear()
    space.debug_draw(options)


@window.event
def on_mouse_press(x, y, button, modifiers):
    circle_moment = pymunk.moment_for_circle(mass, 0, radius)
    circle_body = pymunk.Body(mass, circle_moment)
    circle_body.position = x, y
    circle_shape = pymunk.Circle(circle_body, radius)
    circle_shape.elasticity = 0
    circle_shape.friction = 1.0
    space.add(circle_body, circle_shape)


@window.event
def on_key_press(symbol, modifiers):
    t_press = False
    if symbol == key.T and segment_shape_top not in space.shapes:
        print("Top segment added")
        space.add(segment_shape_top, segment_body_top)
    elif symbol == key.T and segment_shape_top in space.shapes:
        space.remove(segment_shape_top.body, segment_shape_top)


def update(dt):  # Increase physics simulation by one, check if object is below y = 100, if so remove it.
    global checked_shapes
    space.step(dt)
    for shape in space.shapes:
        if shape.body.position.y < 470 and shape not in checked_shapes:
            checked_shapes.append(shape)
    print(len(checked_shapes)-3)


if __name__ == "__main__":  # Driver code to update simulation
    pyglet.clock.schedule_interval(update, 1.0 / 60)
    pyglet.app.run()
