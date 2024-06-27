
from INPUTBOX import InputBox
import pygame
import os
import sys
from TEXT import Text
from BUTTON import Button


main_dir = os.path.split(os.path.abspath(__file__))[0]


def event_poll_QUIT(event):
	if event.type == pygame.QUIT:
		pygame.quit()
		sys.exit()


class GAME_VIEW:
    def __init__(self, main_surface):
        self.all_buttons = dict()
        self.main_surface = main_surface

        self.surface_color_1 = (19, 136, 8)
        self.surface_color_2 = (255, 0, 0)
        self.surface_color_3 = (0, 255, 255)

        self.play_area = (320, 264)
        self.colors = ([255, 0, 0], [0, 255, 2], [255, 255, 0], [0, 0, 255])

	#########################
    def start_update(self):
        self.main_surface.fill(self.surface_color_1)
        logo = pygame.image.load(os.path.join(main_dir, 'UNO', "UNO_logo_small.png"))

        welcome_text = Text(345, 580, "Pulsa cualquier tecla para continuar")

        self.main_surface.blit(logo, (1280 // 2 - logo.get_width() // 2, 640 // 2 - logo.get_height() // 2))
        welcome_text.draw(self.main_surface)

        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            return True

        pygame.display.flip()

    def login_update(self):
        self.main_surface.fill(self.surface_color_2)


        type_name_text = Text(175, 400, "¿Cómo te llamas?")
        many_cards = Text(175,150,"¿Con cuantas cartas quieres jugar?")

        input_box = InputBox(200, 450, 280, 32)
        cartas_input_box = InputBox(175, 200, 280, 32)

        start_button = Button(pygame.Rect(900, 300, 200, 50), (255, 255, 255), "CONTINUAR")

        while True:
            for event in pygame.event.get():
                input_box.handle_event(event)
                cartas_input_box.handle_event(event)

                if start_button.handle_event(event):
                    return [input_box.text, cartas_input_box.text]

            input_box.update()


            type_name_text.draw(self.main_surface)
            many_cards.draw(self.main_surface)
            input_box.draw(self.main_surface)
            cartas_input_box.draw(self.main_surface)

            start_button.draw(self.main_surface)

            pygame.display.flip()

    def game_start(self, game_model):
        self._define_game_buttons()

    def game_update(self, game_model):
        self.main_surface.fill(self.surface_color_3)

        player_turn_text = Text(300, 200, f"Player turn: {game_model.get_current_player().name}")
        player_turn_text.draw(self.main_surface)

        self._update_game_cards(game_model)
        self._render_game_cards(game_model)

        self._render_game_buttons()
        pygame.display.flip()

    def ending_view(self, winner):
        self.main_surface.fill(self.surface_color_1)

        if winner != "AI":

            final_text_vicoria = Text(200, 100, "Has ganado!!, quieres volver a jugar ?")
            final_text_vicoria.draw(self.main_surface)


        else:

            final_text_derrota = Text(200, 100, "Has perdido, quieres volver a jugar ?")
            final_text_derrota.draw(self.main_surface)

        self._render_game_buttons()

        pygame.display.flip()

    #########################

    def _define_game_buttons(self):
        x = self.play_area[0] - 55
        y = self.play_area[1]

        self.all_buttons["COLOR_0"] = Button(pygame.Rect(x, y + 145, 45, 45), self.colors[0])
        self.all_buttons["COLOR_1"] = Button(pygame.Rect(x + 50, y + 145, 45, 45), self.colors[1])
        self.all_buttons["COLOR_2"] = Button(pygame.Rect(x + 100, y + 145, 45, 45), self.colors[2])
        self.all_buttons["COLOR_3"] = Button(pygame.Rect(x + 150, y + 145, 45, 45), self.colors[3])

        self.all_buttons["ROBAR"] = Button(pygame.Rect(650, 245, 125, 25), (255, 255, 255), "Robar carta")
        self.all_buttons["VOLVER_A_JUGAR"] = Button(pygame.Rect(225, 400, 175, 30), self.colors[0], "Volver a jugar")
        self.all_buttons["SALIR"] = Button(pygame.Rect(575, 400, 175, 30), self.colors[3], "Salir del juego")

        self.diasable_all_butons()

    def poll_button(self, button_name, event):
        self.all_buttons[button_name].is_enabled = True
        if self.all_buttons[button_name].handle_event(event):
            self.all_buttons[button_name].is_enabled = False
            return True
        return False

    def _render_game_buttons(self):
        for button in self.all_buttons.values():
            if button.is_enabled:
                button.draw(self.main_surface)

    def diasable_all_butons(self):
        for button in self.all_buttons.values():
            button.is_enabled = False

    #########################

    def _update_game_cards(self, game_model):
        paste_x = 64
        paste_y = 480
        paste_x_AI = 64
        paste_y_AI = 32
        card_spacing_x = 85
        card_spacing_y = 75

        for player in game_model.players:
            for i, card in enumerate(player.hand.cards):
                card.hidden = game_model.deck.image

                if player.name == "AI":
                    if i <= 12:  # Primer fila de cartas AI
                        card.position = [paste_x_AI, paste_y_AI]
                        paste_x_AI += card_spacing_x
                    else:  # Segunda fila de cartas AI
                        card.position = [paste_x_AI - (400), paste_y_AI + (120)]
                        paste_x_AI += card_spacing_x

                else:  # Jugador humano
                    if i <= 12:  # Primer fila de cartas jugador humano
                        card.position = [paste_x, paste_y]
                        paste_x += card_spacing_x
                    else:  # Segunda fila de cartas jugador humano
                        card.position = [paste_x - (400), paste_y - (120)]
                        paste_x += card_spacing_x

    def _render_game_cards(self, game_model):
        for player in game_model.players:
            for card in player.hand.cards:
                if player.name == "AI":
                    self.main_surface.blit(card.hidden, card.position)
                else:
                    self.main_surface.blit(card.image, card.position)
        self.main_surface.blit(game_model.deck.image, game_model.deck.position)
        self.main_surface.blit(game_model.card_in_play.image, game_model.card_in_play.position)

    #########################
    def poll_cards(self, cards, event):
        for card in cards:
            rect = pygame.Rect([card.position[0], card.position[1], 80, 120])
            button = Button(rect)
            if button.handle_event(event):
                return card

    def poll_color(self, event):
        for color in range(0, 4):
            self.all_buttons[f"COLOR_{color}"].is_enabled = True
            if self.all_buttons[f"COLOR_{color}"].handle_event(event):
                for i in range(0, 4):
                    self.all_buttons[f"COLOR_{i}"].is_enabled = False
                return color
        return -1
