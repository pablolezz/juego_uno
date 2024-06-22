import pygame
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
class Login_view:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 32)
        self.input_box = pygame.Rect(400, 240, 400, 40)  # Rectángulo para el campo de entrada del nombre
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.placeholder = 'Escriba el nombre del jugador'
        self.placeholder_color = (100, 100, 100)
        self.done = False
        self.main_surface = pygame.display.set_mode((1280, 640))

    def start_view(self):
        # Inicialización de la vista del login
        pass

    def game_view(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Activa/desactiva el campo de entrada al hacer clic en él
                    if self.input_box.collidepoint(event.pos):
                        self.active = not self.active
                    else:
                        self.active = False
                    self.color = self.color_active if self.active else self.color_inactive
                if event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_RETURN:
                            return self.text
                        elif event.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            self.text += event.unicode

            # Dibujar elementos en la pantalla
            self.screen.fill((30, 30, 30))
            """ self.draw_card()  # Dibuja la tarjeta central """
            self.insert_image()
            self.draw_text_input()  # Dibuja el campo de entrada de texto
            self.draw_continue_message()  # Dibuja el mensaje de continuar

            pygame.display.flip()

        return None

    def insert_image(self):
        logo_path = os.path.join(parent_dir, 'UNO', 'login_uno.jpg')
        logo_surface = pygame.image.load(logo_path)
        logo_surface = pygame.transform.scale(logo_surface, (1280, 640))  # Escala la imagen al tamaño de la pantalla
        self.main_surface.blit(logo_surface, (0, 0))

    def draw_card(self):
        card_width = 820
        card_height = 320
        card_x = (self.screen.get_width() - card_width) // 2
        card_y = (self.screen.get_height() - card_height) // 2

        card_surface = pygame.Surface((card_width, card_height))
        card_surface.fill((255, 255, 255))  # Color de fondo de la tarjeta
        card_rect = card_surface.get_rect()
        card_rect.topleft = (card_x, card_y)

        # Dibujar borde de la tarjeta
        pygame.draw.rect(card_surface, (0, 0, 0), (0, 0, card_width, card_height), 2)

        # Dibujar texto "Escriba su nombre"
        label_text = self.font.render("Escriba su nombre:", True, (0, 0, 0))
        label_rect = label_text.get_rect()
        label_rect.centerx = card_width // 2
        label_rect.y = 30
        card_surface.blit(label_text, label_rect)

        # Dibujar la tarjeta en la pantalla principal
        self.screen.blit(card_surface, card_rect.topleft)

    def draw_text_input(self):
        txt_surface = self.font.render(self.text, True, self.color)
        width = 800
        self.input_box.w = width
        height = 80
        self.input_box.h = height

        input_box_x = (self.screen.get_width() - width) // 2
        input_box_y = (self.screen.get_height() - height) // 2
        self.input_box.topleft = (input_box_x, input_box_y)

        pygame.draw.rect(self.screen, (255, 255, 255), self.input_box, border_radius=height//2)

        if self.text == '':
            txt_surface = self.font.render(self.placeholder, True, self.placeholder_color)
        else:
            txt_surface = self.font.render(self.text, True, (0, 0, 0))

        text_rect = txt_surface.get_rect()
        text_rect.center = self.input_box.center
        self.screen.blit(txt_surface, text_rect)

    def draw_continue_message(self):
        continue_text = self.font.render("Pulse enter para continuar con el juego", True, (0, 0, 0))
        continue_rect = continue_text.get_rect()
        continue_rect.centerx = self.screen.get_width() // 2
        continue_rect.y = self.screen.get_height() - 50
        self.screen.blit(continue_text, continue_rect)
