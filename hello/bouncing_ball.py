import pygame
import sys
import math
import numpy as np

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball in Rotating Hexagon Simulation")

# Colors
BACKGROUND = (10, 10, 40)
HEXAGON_COLOR = (0, 200, 255)
BALL_COLOR = (255, 215, 0)
TEXT_COLOR = (200, 220, 255)

# Physics constants
GRAVITY = 0.5
FRICTION = 0.99
ELASTICITY = 0.8
AIR_RESISTANCE = 0.999

class Hexagon:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        self.angle = 0
        self.rotation_speed = 0.5
        self.vertices = self.calculate_vertices()
        
    def calculate_vertices(self):
        vertices = []
        for i in range(6):
            angle_rad = math.radians(self.angle + 60 * i)
            x = self.center[0] + self.radius * math.cos(angle_rad)
            y = self.center[1] + self.radius * math.sin(angle_rad)
            vertices.append((x, y))
        return vertices
        
    def rotate(self):
        self.angle += self.rotation_speed
        self.vertices = self.calculate_vertices()
        
    def draw(self, surface):
        pygame.draw.polygon(surface, HEXAGON_COLOR, self.vertices, 2)

class Ball:
    def __init__(self, position, radius=15):
        self.position = list(position)
        self.velocity = [0, 0]
        self.radius = radius
        self.trail = []
        self.max_trail = 20
        
    def update(self):
        # Apply gravity
        self.velocity[1] += GRAVITY
        
        # Apply air resistance
        self.velocity[0] *= AIR_RESISTANCE
        self.velocity[1] *= AIR_RESISTANCE
        
        # Apply friction (when colliding)
        # self.velocity[0] *= FRICTION
        # self.velocity[1] *= FRICTION
        
        # Update position
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        # Store trail for visual effect
        self.trail.append((int(self.position[0]), int(self.position[1])))
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)
            
    def draw(self, surface):
        # Draw trail
        for i, pos in enumerate(self.trail):
            alpha = int(255 * i / len(self.trail))
            color = (255, 215, 0, alpha)
            pygame.draw.circle(surface, color, pos, int(self.radius * i / len(self.trail)), 1)
        
        # Draw ball
        pygame.draw.circle(surface, BALL_COLOR, (int(self.position[0]), int(self.position[1])), self.radius)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.position[0]), int(self.position[1])), self.radius, 1)

def distance_point_to_line(point, line_start, line_end):
    # Convert to numpy arrays for vector operations
    point = np.array(point)
    line_start = np.array(line_start)
    line_end = np.array(line_end)
    
    line_vec = line_end - line_start
    line_len = np.linalg.norm(line_vec)
    line_unitvec = line_vec / line_len
    point_vec = point - line_start
    
    # Project point onto line
    projection = np.dot(point_vec, line_unitvec)
    
    if projection < 0:
        closest = line_start
    elif projection > line_len:
        closest = line_end
    else:
        closest = line_start + projection * line_unitvec
        
    distance = np.linalg.norm(point - closest)
    return distance, closest

def check_collision(ball, hexagon):
    collision_occurred = False
    for i in range(6):
        start = hexagon.vertices[i]
        end = hexagon.vertices[(i + 1) % 6]
        
        distance, closest = distance_point_to_line(ball.position, start, end)
        
        if distance < ball.radius:
            # Calculate collision normal
            normal = np.array([ball.position[0] - closest[0], 
                              ball.position[1] - closest[1]])
            normal_length = np.linalg.norm(normal)
            if normal_length == 0:
                continue
            normal = normal / normal_length
            
            # Reflect velocity with elasticity
            dot_product = np.dot(ball.velocity, normal)
            ball.velocity[0] = ball.velocity[0] - (1 + ELASTICITY) * dot_product * normal[0]
            ball.velocity[1] = ball.velocity[1] - (1 + ELASTICITY) * dot_product * normal[1]
            
            # Apply friction on collision
            ball.velocity[0] *= FRICTION
            ball.velocity[1] *= FRICTION
            
            # Position correction
            overlap = ball.radius - distance
            ball.position[0] += overlap * normal[0]
            ball.position[1] += overlap * normal[1]
            
            collision_occurred = True
    
    return collision_occurred

def main():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    
    # Create hexagon
    hexagon = Hexagon((WIDTH//2, HEIGHT//2), 200)
    
    # Create ball
    ball = Ball((WIDTH//2, HEIGHT//2 - 120))
    
    # Add initial velocity
    ball.velocity = [3, -2]
    
    # Game state
    paused = False
    show_trail = True
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Pause/Resume
                elif event.key == pygame.K_p:
                    paused = not paused
                # Speed controls
                elif event.key == pygame.K_UP:
                    hexagon.rotation_speed *= 1.2
                elif event.key == pygame.K_DOWN:
                    hexagon.rotation_speed *= 0.8
                elif event.key == pygame.K_LEFT:
                    hexagon.rotation_speed = -abs(hexagon.rotation_speed)
                elif event.key == pygame.K_RIGHT:
                    hexagon.rotation_speed = abs(hexagon.rotation_speed)
                # Reset ball position
                elif event.key == pygame.K_SPACE:
                    ball.position = [WIDTH//2, HEIGHT//2 - 120]
                    ball.velocity = [3, -2]
                    ball.trail = []
                # Toggle trail
                elif event.key == pygame.K_t:
                    show_trail = not show_trail
                # Change gravity
                elif event.key == pygame.K_g:
                    global GRAVITY
                    GRAVITY = 0.2 if GRAVITY == 0.5 else 0.5
                # Change elasticity
                elif event.key == pygame.K_e:
                    global ELASTICITY
                    ELASTICITY = 0.6 if ELASTICITY == 0.8 else 0.8
        
        # Update
        if not paused:
            hexagon.rotate()
            ball.update()
            check_collision(ball, hexagon)
        
        # Draw
        screen.fill(BACKGROUND)
        hexagon.draw(screen)
        
        # Draw trail if enabled
        if show_trail:
            ball.draw(screen)
        else:
            # Draw ball without trail
            pygame.draw.circle(screen, BALL_COLOR, (int(ball.position[0]), int(ball.position[1])), ball.radius)
            pygame.draw.circle(screen, (255, 255, 255), (int(ball.position[0]), int(ball.position[1])), ball.radius, 1)
        
        # Draw info
        info_text = [
            f"Rotation Speed: {hexagon.rotation_speed:.2f} rad/s (↑↓←→ to adjust)",
            f"Ball Velocity: ({ball.velocity[0]:.2f}, {ball.velocity[1]:.2f})",
            f"Gravity: {GRAVITY:.1f} (G to toggle), Elasticity: {ELASTICITY:.1f} (E to toggle)",
            "SPACE: Reset | P: Pause | T: Toggle trail",
            f"Status: {'PAUSED' if paused else 'RUNNING'}"
        ]
        
        for i, text in enumerate(info_text):
            text_surface = font.render(text, True, TEXT_COLOR)
            screen.blit(text_surface, (10, 10 + i * 25))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
