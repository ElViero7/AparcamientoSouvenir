import pygame
import sys

# Inicializa Pygame
pygame.init()

# Configuraciones básicas
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 6
CELL_SIZE = WIDTH // GRID_SIZE
FPS = 60

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Configura la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rush Hour")

# Clase para los vehículos
class Vehicle:
    def __init__(self, x, y, length, horizontal, color):
        self.x = x
        self.y = y
        self.length = length
        self.horizontal = horizontal
        self.color = color
        self.selected = False

    def draw(self):
        rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, 
                           (self.length * CELL_SIZE if self.horizontal else CELL_SIZE),
                           (CELL_SIZE if self.horizontal else self.length * CELL_SIZE))
        pygame.draw.rect(screen, self.color, rect)
        if self.selected:
            pygame.draw.rect(screen, BLACK, rect, 3)

    def move(self, dx, dy):
        if self.horizontal:
            self.x += dx
        else:
            self.y += dy

# Crear vehículos
vehicles = [
    Vehicle(2, 2, 2, True, RED),  # Coche rojo
    Vehicle(0, 0, 3, False, BLUE),
    Vehicle(4, 3, 2, True, GREEN)
]

selected_vehicle = None

# Función principal
def main():
    global selected_vehicle
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                for vehicle in vehicles:
                    if vehicle.horizontal and vehicle.y == grid_y and vehicle.x <= grid_x < vehicle.x + vehicle.length:
                        selected_vehicle = vehicle
                        vehicle.selected = True
                        break
                    elif not vehicle.horizontal and vehicle.x == grid_x and vehicle.y <= grid_y < vehicle.y + vehicle.length:
                        selected_vehicle = vehicle
                        vehicle.selected = True
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_vehicle:
                    selected_vehicle.selected = False
                    selected_vehicle = None
            elif event.type == pygame.KEYDOWN and selected_vehicle:
                if event.key == pygame.K_LEFT:
                    selected_vehicle.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    selected_vehicle.move(1, 0)
                elif event.key == pygame.K_UP:
                    selected_vehicle.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    selected_vehicle.move(0, 1)

        screen.fill(WHITE)
        
        # Dibujar la cuadrícula
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT))
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        
        # Dibujar vehículos
        for vehicle in vehicles:
            vehicle.draw()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
