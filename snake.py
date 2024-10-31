import pygame  # pip install pygame
from pygame.math import Vector2
import random

# Definir dimensiones de la pantalla
ANCHO = 720
ALTO = 480

# Crear la pantalla del juego
pantalla = pygame.display.set_mode((ANCHO, ALTO))

# Definir la clase Snake (Serpiente)
class Snake():
    def __init__(self):
        # Inicializar el cuerpo de la serpiente con tres segmentos
        self.body = [Vector2(10, 100), Vector2(10, 110), Vector2(10, 120)]
        # Dirección inicial de la serpiente
        self.direccion = Vector2(10, 0)
        # Bandera para indicar si se debe agregar un segmento al cuerpo
        self.add = True

    def draw(self):
        # Dibujar cada segmento del cuerpo de la serpiente en la pantalla
        for i in self.body:
            pygame.draw.rect(pantalla, (0, 255, 0), pygame.Rect(i.x, i.y, 10, 10))

    def move(self):
        # Si se debe agregar un nuevo segmento al cuerpo
        if self.add:
            body_copy = self.body[:]  # Hacer una copia del cuerpo actual
            body_copy.insert(0, body_copy[0] + self.direccion)  # Insertar un nuevo segmento al frente
            self.body = body_copy[:]  # Actualizar el cuerpo con la copia modificada
            self.add = False  # Resetear la bandera
        else:
            body_copy = self.body[:-1]  # Hacer una copia del cuerpo excluyendo el último segmento
            body_copy.insert(0, body_copy[0] + self.direccion)  # Insertar un nuevo segmento al frente
            self.body = body_copy[:]  # Actualizar el cuerpo con la copia modificada

    def morir(self):
        # Verificar si la serpiente ha chocado con los límites de la pantalla
        if self.body[0].x >= ANCHO or self.body[0].x < 0 or self.body[0].y >= ALTO or self.body[0].y < 0:
            return True
        # Verificar si la serpiente ha chocado con su propio cuerpo
        for i in self.body[1:]:
            if self.body[0] == i:
                return True

# Definir la clase Manzana
class Manzana():
    def __init__(self):
        self.generar()  # Generar una nueva posición para la manzana al inicializar

    def generar(self):
        # Generar una nueva posición aleatoria para la manzana dentro de los límites de la pantalla
        x = random.randint(0, ANCHO // 10) * 10
        y = random.randint(0, ALTO // 10) * 10
        self.ubicacion = Vector2(x, y)

    def draw(self):
        # Dibujar la manzana en la pantalla
        pygame.draw.rect(pantalla, (255, 0, 0), pygame.Rect(self.ubicacion.x, self.ubicacion.y, 10, 10))

    def comprobar(self, snake):
        # Verificar si la serpiente ha comido la manzana
        if self.ubicacion == snake.body[0]:
            self.generar()  # Generar una nueva manzana en una posición aleatoria
            snake.add = True  # Indicar que se debe agregar un nuevo segmento al cuerpo de la serpiente

# Función principal del juego
def main():
    # Inicializar la serpiente y la manzana
    snake = Snake()
    manzana = Manzana()
    clock = pygame.time.Clock()
    puntaje = 0

    while True:
        clock.tick(30)  # Controlar la velocidad del juego (FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()  # Salir del juego si se cierra la ventana
            
            if event.type == pygame.KEYDOWN:
                # Cambiar la dirección de la serpiente basado en la tecla presionada
                if event.key == pygame.K_DOWN and snake.direccion != Vector2(0, -10):
                    snake.direccion = Vector2(0, 10)
                elif event.key == pygame.K_UP and snake.direccion != Vector2(0, 10):
                    snake.direccion = Vector2(0, -10)
                elif event.key == pygame.K_RIGHT and snake.direccion != Vector2(-10, 0):
                    snake.direccion = Vector2(10, 0)
                elif event.key == pygame.K_LEFT and snake.direccion != Vector2(10, 0):
                    snake.direccion = Vector2(-10, 0)

        if snake.morir():
            quit()  # Salir del juego si la serpiente muere
        
        pantalla.fill((0, 0, 0))  # Limpiar la pantalla
        
        snake.draw()  # Dibujar la serpiente
        manzana.draw()  # Dibujar la manzana
        snake.move()  # Mover la serpiente
        manzana.comprobar(snake)  # Comprobar si la serpiente ha comido la manzana

        if snake.add:
            puntaje += 1  # Incrementar el puntaje si se ha agregado un nuevo segmento al cuerpo
        
        pygame.display.set_caption(f"Puntaje: {puntaje}")  # Mostrar el puntaje en el título de la ventana
        pygame.display.update()  # Actualizar la pantalla

# Iniciar el juego
main()
