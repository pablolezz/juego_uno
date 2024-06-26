import pygame
import os
from moviepy.editor import *

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

class Button:
    def __init__(self, x, y, width, height, text, fontType="Arial", fontSize=20):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (255, 255, 255)  # Color blanco por defecto
        self.text = text
        self.font = pygame.font.SysFont(fontType, fontSize)
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        if self.text:
            text_surface = self.font.render(self.text, True, (0, 0, 0))  # Texto negro
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    def contains_point(self, point):
        return self.rect.collidepoint(point)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Text:
    def __init__(self, x, y, text):
        self.font = pygame.font.SysFont("Fixedsys Excelsior", 48)
        self.x = x
        self.y = y
        self.position = (self.x, self.y)
        self.text = self.font.render(text, True, (0, 0, 0))


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color(200, 200, 200)
        self.color_active = pygame.Color(255,255,255)
        self.color = self.color_inactive
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.placeholder = 'Escriba el nombre del jugador'
        self.placeholder_color = (100, 100, 100)
        self.border_radius = 40

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)  # Aquí podrías manejar el texto ingresado
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        # Render the text
        if self.text == '' and not self.active:
            # Draw placeholder if the box is empty and not active
            text_surface = self.font.render(self.placeholder, True, (100, 100, 100))
        else:
            # Draw current text if there is any
            text_surface = self.font.render(self.text, True, (0, 0, 0))

        # Adjust the position of the text
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center

        # Draw the rounded rectangle
        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, pygame.Color('black'), self.rect, 2, border_radius=self.border_radius)

        # Blit the text surface onto the screen
        screen.blit(text_surface, text_rect)

class Login_view:
    def __init__(self, screen):
        self.surface_color_1 = (19, 136, 8)
        self.surface_color_2 = (255, 0, 0)
        self.surface_color_3 = (0, 0, 255)

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
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Fixedsys Excelsior", 32)
        Type_name = Text(500, 100, "¿Cómo te llamas?")

        # Load and scale the logo once
        logo_path = os.path.join(parent_dir, 'UNO', 'login_uno.jpg')
        logo_surface = pygame.image.load(logo_path)
        logo_surface = pygame.transform.scale(logo_surface, (1280, 640))

        width = 800
        heigth = 80
        input_box = InputBox((1280 - width) // 2, (640 - heigth) // 2, 800, 80)

        start_button = Button(540, 500, 200, 50, "CONTINUAR")
        start_button.color = button_color = (255, 255, 255)

        running = True
        while running:
            for event in pygame.event.get():
                input_box.handle_event(event)
                if start_button.handle_event(event):
                    return input_box.text

            self.main_surface.fill(self.surface_color_2)  # Clear the screen
            self.main_surface.blit(logo_surface, (0, 0))  # Draw the logo image
            self.main_surface.blit(Type_name.text, Type_name.position)  # Draw the text

            input_box.draw(self.main_surface)  # Draw the input box
            start_button.draw(self.main_surface)  # Draw the button

            pygame.display.flip()
            self.clock.tick(30)

    def event_poll_QUIT(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


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
