import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import numpy as np

# Initialize pygame
pygame.init()

# Get the current screen resolution
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

# Set up the display with OpenGL in a fullscreen window
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL | FULLSCREEN | NOFRAME)
pygame.display.set_caption("Pong Game with OpenGL")

# Set up the projection
gluPerspective(45, (screen_width / screen_height), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Paddle properties
paddle_width = 0.1
paddle_height = 1.0
paddle_speed = 0.1

# Ball properties
ball_radius = 0.1
ball_speed = [0.03, 0.03]

# Paddle positions
left_paddle_pos = [-3.5, 0]
right_paddle_pos = [3.5, 0]

# Ball position
ball_pos = [0, 0]

# Function to draw a paddle
def draw_paddle(position):
    glBegin(GL_QUADS)
    glVertex2f(position[0] - paddle_width / 2, position[1] - paddle_height / 2)
    glVertex2f(position[0] + paddle_width / 2, position[1] - paddle_height / 2)
    glVertex2f(position[0] + paddle_width / 2, position[1] + paddle_height / 2)
    glVertex2f(position[0] - paddle_width / 2, position[1] + paddle_height / 2)
    glEnd()

# Function to draw the ball
def draw_ball(position):
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(1.0, 0.0, 0.0)  # Red color
    glVertex2f(position[0], position[1])  # Center of circle
    for angle in np.linspace(0, 2 * np.pi, 100):
        x = ball_radius * np.cos(angle)
        y = ball_radius * np.sin(angle)
        glVertex2f(position[0] + x, position[1] + y)
    glEnd()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    # Handle paddle movement with arrow keys
    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        left_paddle_pos[1] += paddle_speed
        right_paddle_pos[1] += paddle_speed
    if keys[K_DOWN]:
        left_paddle_pos[1] -= paddle_speed
        right_paddle_pos[1] -= paddle_speed

    # Clamp paddle positions to stay within the window
    left_paddle_pos[1] = max(-3 + paddle_height / 2, min(3 - paddle_height / 2, left_paddle_pos[1]))
    right_paddle_pos[1] = max(-3 + paddle_height / 2, min(3 - paddle_height / 2, right_paddle_pos[1]))

    # Update ball position
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Ball collision with top and bottom
    if ball_pos[1] > 3 or ball_pos[1] < -3:
        ball_speed[1] = -ball_speed[1]

    # Ball collision with paddles
    if (ball_pos[0] <= left_paddle_pos[0] + paddle_width / 2 and
        left_paddle_pos[1] - paddle_height / 2 <= ball_pos[1] <= left_paddle_pos[1] + paddle_height / 2):
        ball_speed[0] = -ball_speed[0]

    if (ball_pos[0] >= right_paddle_pos[0] - paddle_width / 2 and
        right_paddle_pos[1] - paddle_height / 2 <= ball_pos[1] <= right_paddle_pos[1] + paddle_height / 2):
        ball_speed[0] = -ball_speed[0]

    # Reset ball if it goes out of bounds
    if ball_pos[0] < -4 or ball_pos[0] > 4:
        ball_pos = [0, 0]

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw paddles and ball
    glColor3f(0.0, 0.0, 1.0)  # Blue color for paddles
    draw_paddle(left_paddle_pos)
    draw_paddle(right_paddle_pos)

    glColor3f(1.0, 0.0, 0.0)  # Red color for ball
    draw_ball(ball_pos)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate to 30 FPS
    pygame.time.Clock().tick(30)

# Quit pygame
pygame.quit()
sys.exit()
