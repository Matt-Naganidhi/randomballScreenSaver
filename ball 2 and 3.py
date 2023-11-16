import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Window dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Ball class
class Ball:
    def __init__(self):
        self.radius = random.randint(10, 30)
        self.position = [random.randint(self.radius, width - self.radius), random.randint(self.radius, height - self.radius)]
        self.velocity = [random.uniform(-5, 5), random.uniform(-5, 5)]
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # Mass is proportional to the area (pi*r^2)
        self.mass = math.pi * self.radius**2

    def move(self):
        # Update the position
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Bounce off the walls
        if self.position[0] + self.radius > width or self.position[0] - self.radius < 0:
            self.velocity[0] = -self.velocity[0]
        if self.position[1] + self.radius > height or self.position[1] - self.radius < 0:
            self.velocity[1] = -self.velocity[1]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius)

# Detect collision between two balls
def is_collision(ball1, ball2):
    distance = math.hypot(ball1.position[0] - ball2.position[0], ball1.position[1] - ball2.position[1])
    return distance < ball1.radius + ball2.radius

# Handle collision between two balls
def handle_collision(ball1, ball2):
    # Calculate the angle of the collision
    angle = math.atan2(ball2.position[1] - ball1.position[1], ball2.position[0] - ball1.position[0])
    # Decompose the velocities into perpendicular components
    v1 = rotate(ball1.velocity, -angle)
    v2 = rotate(ball2.velocity, -angle)
    # Conservation of momentum (elastic collision)
    v1_new = [((ball1.mass - ball2.mass) * v1[0] + 2 * ball2.mass * v2[0]) / (ball1.mass + ball2.mass), v1[1]]
    v2_new = [((ball2.mass - ball1.mass) * v2[0] + 2 * ball1.mass * v1[0]) / (ball1.mass + ball2.mass), v2[1]]
    # Rotate velocities back to the original coordinate system
    ball1.velocity = rotate(v1_new, angle)
    ball2.velocity = rotate(v2_new, angle)

# Rotate velocity vector by a given angle
def rotate(velocity, angle):
    vx, vy = velocity
    rotated_vx = vx * math.cos(angle) - vy * math.sin(angle)
    rotated_vy = vx * math.sin(angle) + vy * math.cos(angle)
    return [rotated_vx, rotated_vy]

# Randomize balls
num_balls = random.randint(5, 10)
balls = [Ball() for _ in range(num_balls)]

# ... (other parts of the code remain unchanged)

# Water wave simulation
def draw_water(screen, amplitude, frequency, phase_shift, water_level):
    water_color = (0, 105, 148)
    for x in range(0, width):
        # Sine wave for water surface
        y = int(amplitude * math.sin(frequency * x + phase_shift) + water_level)
        pygame.draw.line(screen, water_color, (x, y), (x, height))

# Shading for the balls
def add_shading(ball):
    light_source = (width // 2, height // 4)  # Static light source position
    gradient_color = calculate_gradient(ball, light_source)
    ball.color = gradient_color

def calculate_gradient(ball, light_source):
    # This function would calculate the gradient color based on ball position and light source
    # For simplicity, this is a placeholder that returns a shade of blue
    return (0, 0, 255)



# Main loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill((255, 255, 255))  # Fill the screen with white
    clock.tick(60)  # Limit the frame rate to 60 FPS

    # Move and draw the balls
    for ball in balls:
        ball.move()
        ball.draw(screen)

    # Check for collisions
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            if is_collision(balls[i], balls[j]):
                handle_collision(balls[i], balls[j])
    # Draw water waves
    amplitude = 10  # Amplitude of the waves
    frequency = 0.02  # Frequency of the waves
    phase_shift = pygame.time.get_ticks() / 1000  # Phase shift for animation
    water_level = height - 100  # Vertical position of the water level
    draw_water(screen, amplitude, frequency, phase_shift, water_level)

    # Apply shading to balls
    for ball in balls:
        add_shading(ball)
        ball.draw(screen)

    # Update the display
    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
# Quit Pygame
pygame.quit()

