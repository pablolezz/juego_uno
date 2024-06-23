import pygame
import os
import sys

main_dir = os.path.split(os.path.abspath(__file__))[0]

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
        self.text = self.font.render(text, True, (255, 255, 255))

class CardSprite:

    def __init__(self):
        self.sheet = pygame.image.load(os.path.join(main_dir, 'UNO', "Copia UNO.jpg"))
        self.x = self.sheet.get_width()  # 800
        self.y = self.sheet.get_height()  # 882

    def load_grid_images(self):
        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size
        sprite_rects = []
        cardheighty = 0
        cardwidthx = 0
        cardsizex = self.x // 10
        cardsizey = 125
        for card in range(56):
            card_coordinates = [cardwidthx, cardheighty, cardsizex, cardsizey]
            sprite_rects.append(card_coordinates)
            cardwidthx += cardsizex
            if cardwidthx >= self.x:
                cardwidthx = 0
                cardheighty += cardsizey
        return self.images_at(sprite_rects)

    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

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

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Game_view:
    # BOTNES,TEXTOS,FUNETES, SPRITES, EL BACKGROUND, TAMAÑO, SURFACE "FUNCIONES DE UPADATE DEL RENDERER",
    def __init__(self, main_surface):
        self.all_buttons = []
        self.main_surface = main_surface

        # Asignamos 3 colores para las 3 "fases"
        self.surface_color_1 = (19, 136, 8)
        self.surface_color_2 = (255, 0, 0)
        self.surface_color_3 = (0, 0, 255)

        self.play_area = (320, 264)
        self.colors = ([234, 26, 39], [248, 224, 0], [0, 164, 78], [2, 149, 216], [255, 165, 0], [0, 0, 0])

    def poll_event_QUIT(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def start_loop(self):
        self.main_surface.fill(self.surface_color_1)
        self.font = pygame.font.SysFont("Fixedsys Excelsior", 32)
        logo = pygame.image.load(os.path.join(main_dir, 'UNO', "UNO_logo_small.png"))
        h = logo.get_height()
        w = logo.get_width()
        welcome = Text(345, 580, "Pulsa cualquier tecla para continuar")
        surface_sizex = 1280  # Ancho del tablero, en píxeles
        surface_sizey = 640  # Alto del tablero, en píxeles
        self.main_surface.blit(logo, (surface_sizex // 2 - w // 2, surface_sizey // 2 - h // 2))
        self.main_surface.blit(welcome.text, welcome.position)

        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            return True

        pygame.display.flip()
    def login_loop(self):
        self.clock = pygame.time.Clock()
        self.main_surface.fill(self.surface_color_2)
        self.font = pygame.font.SysFont("Fixedsys Excelsior", 32)
        Type_name = Text(500, 100, "¿Cómo te llamas?")
        self.main_surface.blit(Type_name.text, Type_name.position)

        input_box = InputBox(500, 150, 280, 32)

        start_button = Button(540, 300, 200, 50, "CONTINUAR")
        start_button.color = button_color = (255, 255, 255)

        running = True
        while running:
            for event in pygame.event.get():
                input_box.handle_event(event)
                if start_button.handle_event(event):
                    return input_box.text

            input_box.update()

            self.main_surface.fill(self.surface_color_2)
            self.main_surface.blit(Type_name.text, Type_name.position)
            input_box.draw(self.main_surface)
            start_button.draw(self.main_surface)

            pygame.display.flip()
            self.clock.tick(30)
    def game_loop(self, game_model):
        self.main_surface.fill(self.surface_color_3)
        juego_text = Text(345, 580, "Fase de Juego")

        self._game_cards_update(game_model)
        self._game_buttons_update(game_model)

        self.main_surface.blit(juego_text.text, juego_text.position)

        pygame.display.flip()

    def game_start(self, game_model):
        self._game_buttons_init(game_model)
        self._game_cards_init(game_model)


    def _game_cards_init(self, game_model):
        # Definimos un patrón para pegar las cartas una junto a otra
        [paste_x, paste_y] = [64, 480]
        [paste_xAI, paste_yAI] = [64, 32]

        cardSprite = CardSprite()
        # Definimos la posición que ocuparán las cartas sobre el tablero al empezar la partida
        for player in game_model.players:
            for card in player.hand.cards:
                card.hidden = cardSprite.image_at([720 , 750, 80, 125])  # Para el atributo hidden usamos la carta con el signo de interrogación,
                # que anteriormente asignamos al atributo image del mazo
                if player.name == "AI":
                    card.position = [paste_xAI, paste_yAI]
                    paste_xAI += 85
                else:
                    card.position = [paste_x, paste_y]
                    paste_x += 85
    def _game_cards_update(self, game_model):
        # Ponemos las cartas sobre el tablero
        cardSprite = CardSprite()
        for player in game_model.players:
            for card in player.hand.cards:
                if player.name == "AI":
                    self.main_surface.blit(card.hidden, card.position)  # Si es una carta de la IA, elegimos la imagen del signo de interrogación
                else:
                    self.main_surface.blit(card.image, card.position)
        self.main_surface.blit(cardSprite.image_at([720, 750, 80, 125]), [650, 256])
        self.main_surface.blit(game_model.card_in_play.image, game_model.play_area)

    def _game_buttons_init(self, game_model):
        size = 45
        x = self.play_area[0]
        y = self.play_area[1]
        # Definimos los botones para elegir entre los cuatro colores, así como el botón de pasar turno y el del color en juego
        for n in range(4):
            self.all_buttons.append(Button(x - 55, y + 145, size, size, ""))
            x += 50

        coordinates = [850, 275, 125, 25], [750, 325, 330, 25], [225, 400, 175, 30], [575, 400, 175, 30]
        for c in coordinates:
            self.all_buttons.append(Button(c[0], c[1], c[2], c[3], ""))

        c = 0
        for button in self.all_buttons:
            button.color = self.colors[c]
            c += 1
            if c == 6:
                break

        self.all_buttons[4].text = self.font.render("Pasar turno".format(), True, (0, 0, 0))
        self.all_buttons[5].text = self.font.render("El color en juego es el {0}".format(game_model.card_in_play.suit), True,
                                                    (255, 255, 255))
        self.all_buttons[6].text = self.font.render("Volver a jugar".format(), True, (0, 0, 0))
        self.all_buttons[6].color = self.colors[0]
        self.all_buttons[7].text = self.font.render("Salir del juego".format(), True, (0, 0, 0))
        self.all_buttons[7].color = self.colors[3]
    def _game_buttons_update(self, game_model, i=0, j=6):
        for n in range(i, j):
            button_color = self.all_buttons[n].color
            button_rect = (self.all_buttons[n].x, self.all_buttons[n].y, self.all_buttons[n].width, self.all_buttons[n].height)
            if n == 5:
                self.all_buttons[n].text = self.font.render("El color en juego es el {0}".format(game_model.card_in_play.suit),
                                                            True, (255, 255, 255))
            button_text = self.all_buttons[n].text
            self.main_surface.fill(button_color, button_rect)
            try:
                self.main_surface.blit(button_text, button_rect)
            except:
                TypeError