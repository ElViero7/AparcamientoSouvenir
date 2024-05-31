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
LIGHTGREEN = (171, 235, 198)
ORANGE = (230, 126, 34)
LIGHTBLUE = (174, 214, 241)
PINK = (255, 51, 227)
DARKBLUE = (54, 51, 255)
CYAN = (55, 213, 158)
GREY = (171, 178, 185)
BEIGE = (241, 172, 99)
LEMON = (255, 250, 105)
BROWN = (135, 97, 38)
DARKGREEN = (36, 128, 38)
YELLOW = (255, 255, 0)
PURPLE = (85, 36, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
FONDO = (79, 75, 82)


# Configura la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aparcamiento Souvenir")

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
            new_x = self.x + dx
            if 0 <= new_x <= GRID_SIZE - self.length and not is_collision(new_x, self.y, self.length, self.horizontal):
                self.x = new_x
        else:
            new_y = self.y + dy
            if 0 <= new_y <= GRID_SIZE - self.length and not is_collision(self.x, new_y, self.length, self.horizontal):
                self.y = new_y

# Definir niveles
levels = [
    [  # Nivel 1
        Vehicle(2, 2, 2, True, RED),
        Vehicle(0, 0, 3, False, PURPLE),
        Vehicle(1, 0, 2, True, DARKGREEN),
        Vehicle(4, 2, 3, False, DARKBLUE),
        Vehicle(0, 3, 2, False, ORANGE),
        Vehicle(2, 4, 2, True, LIGHTBLUE),
        Vehicle(2, 5, 3, True, CYAN),
        Vehicle(5, 3, 3, False, YELLOW)
    ],
     [  # Nivel 2
        Vehicle(2, 2, 2, True, RED),  # Coche rojo
        Vehicle(0, 0, 2, True, GREY),
        Vehicle(3, 0, 2, False, BEIGE),
        Vehicle(4, 1, 2, False, LEMON),
        Vehicle(0, 3, 3, True, BROWN),
        Vehicle(0, 4, 2, True, DARKGREEN),
        Vehicle(3, 3, 2, False, PURPLE),
    ],
    [  # Nivel 3
        Vehicle(2, 2, 2, True, RED),  # Coche rojo
        Vehicle(0, 0, 2, True, LIGHTBLUE),
        Vehicle(0, 1, 3, False, PINK),
        Vehicle(1, 0, 2, False, ORANGE),
        Vehicle(3, 3, 3, False, BLUE),
        Vehicle(4, 0, 2, True, GREEN),
        Vehicle(1, 5, 2, True, CYAN),
    ],
    [  # Nivel 4
        Vehicle(2, 2, 2, True, RED),  # Coche rojo
        Vehicle(0, 0, 2, True, YELLOW),
        Vehicle(1, 0, 2, False, PURPLE),
        Vehicle(3, 0, 2, False, LIGHTGREEN),
        Vehicle(4, 1, 2, False, GREY),
        Vehicle(0, 3, 2, True, ORANGE),
        Vehicle(4, 4, 2, False, DARKBLUE),
    ],
    [  # Nivel 5
        Vehicle(0, 2, 2, True, RED),  # Coche rojo
        Vehicle(2, 1, 2, False, LIGHTGREEN),
        Vehicle(4, 1, 2, False, YELLOW),
        Vehicle(5, 2, 2, False, ORANGE),
        Vehicle(0, 3, 3, True, PURPLE),
        Vehicle(0, 4, 2, False, LIGHTBLUE),
        Vehicle(1, 4, 2, False, PINK),
        Vehicle(2, 4, 2, False, DARKBLUE),
        Vehicle(4, 4, 2, True, GREEN),
        Vehicle(4, 5, 2, True, WHITE),
    ],
    [  # Nivel 6
        Vehicle(1, 2, 2, True, RED),  # Coche rojo
        Vehicle(1, 0, 2, False, LIGHTGREEN),
        Vehicle(0, 3, 3, False, BLUE),
        Vehicle(3, 0, 2, False, GREEN),
        Vehicle(5, 0, 2, False, DARKGREEN),
        Vehicle(4, 0, 3, False, LEMON),
        Vehicle(3, 2, 2, False, PINK),
        Vehicle(1, 3, 2, True, LIGHTBLUE),
        Vehicle(5, 2, 2, False, ORANGE),
        Vehicle(4, 4, 2, True, BEIGE),
        Vehicle(3, 5, 3, True, PURPLE),
    ],
    [  # Nivel 7 DIFICIL
        Vehicle(0, 2, 2, True, RED),  # Coche rojo
        Vehicle(0, 0, 3, True, YELLOW),
        Vehicle(3, 0, 2, True, LIGHTGREEN),
        Vehicle(5, 0, 2, False, ORANGE),
        Vehicle(0, 1, 2, True, LIGHTBLUE),
        Vehicle(2, 1, 2, False, PINK),
        Vehicle(3, 1, 2, True, DARKBLUE),
        Vehicle(3, 2, 3, False, PURPLE),
        Vehicle(0, 4, 2, False, BEIGE),
        Vehicle(4, 3, 2, False, WHITE),
        Vehicle(1, 5, 3, True, BLUE),
        Vehicle(1, 4, 2, True, LEMON),
        Vehicle(4, 5, 2, True, BROWN),
        Vehicle(5, 2, 2, False, CYAN)
    ],
    
]

current_level = 0

def load_level(level):
    global vehicles
    vehicles = levels[level]

selected_vehicle = None

# Meta (posición de salida)
goal_x, goal_y = GRID_SIZE, 2  # Fuera del tablero

# Verificar colisiones
def is_collision(new_x, new_y, length, horizontal):
    for vehicle in vehicles:
        if vehicle != selected_vehicle:  # No comparar con el vehículo actual
            if horizontal:  # Verificar colisiones para vehículos horizontales
                for i in range(length):
                    if vehicle.horizontal:
                        for j in range(vehicle.length):
                            if new_x + i == vehicle.x + j and new_y == vehicle.y:
                                return True
                    else:
                        for j in range(vehicle.length):
                            if new_x + i == vehicle.x and new_y == vehicle.y + j:
                                return True
            else:  # Verificar colisiones para vehículos verticales
                for i in range(length):
                    if vehicle.horizontal:
                        for j in range(vehicle.length):
                            if new_x == vehicle.x + j and new_y + i == vehicle.y:
                                return True
                    else:
                        for j in range(vehicle.length):
                            if new_x == vehicle.x and new_y + i == vehicle.y + j:
                                return True
    return False

# Función principal
def main():
    global selected_vehicle, current_level
    clock = pygame.time.Clock()
    level_completed = False
    
    load_level(current_level)
    
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

        screen.fill(FONDO)
        
        # Dibujar la cuadrícula
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT))
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        
        # Dibujar la meta fuera del tablero
        goal_rect = pygame.Rect(WIDTH - CELL_SIZE // 2, goal_y * CELL_SIZE, CELL_SIZE // 2, CELL_SIZE)
        pygame.draw.rect(screen, RED, goal_rect)
        
        # Dibujar vehículos
        for vehicle in vehicles:
            vehicle.draw()

        # Verificar si el coche rojo ha alcanzado la meta
        if vehicles[0].x + vehicles[0].length == GRID_SIZE:
            level_completed = True
            font = pygame.font.SysFont(None, 74)
            text = font.render('Nivel Superado!', True, BLACK)
            screen.blit(text, (WIDTH // 4, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)  # Esperar 2 segundos antes de cargar el próximo nivel
            
            # Avanzar al siguiente nivel
            if current_level < len(levels) - 1:
                current_level += 1
                load_level(current_level)
                level_completed = False
            else:
                font = pygame.font.SysFont(None, 54)
                text = font.render('¡Todos los niveles completados!', True, BLACK)
                screen.blit(text, (WIDTH // 4, HEIGHT // 2 + 100))
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
