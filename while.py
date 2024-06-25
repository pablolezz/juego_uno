

while True:
    # Comenzamos el bucle estableciendo los efectos en función de la carta en juego (self.card_in_play):



    # Actualizamos las cartas
    self.place_cards()
    self.update_surface()

    # Los efectos ya están consolidados (esperemos). Ahora hay que definir el cambio de turno
    turn += 1
    i = (turn + pierdeturno) % len(
        self.hands)  # 0 en el primer turno, salvo que la primera carta en juego sea pierdeturno
    self.playable_cards = []
    suits_in_hand = []
    hand = self.hands[i].cards  # Llamamos hand a la mano que está jugando, para que el código sea más legible

    # Comienza el siguiente turno, propiamente dicho
    # Determinamos si tenemos cartas en la mano que podamos jugar:
    for card in hand:
        suits_in_hand.append(
            card.suit)  # Anotamos el color de cada carta, para comprobar después si podemos usar el comodín robacuatro
        if card.suit == self.color or card.rank == self.card_in_play.rank or card.rank == 13:  # "eligecolor":
            # Si la carta comparte color o número con la que está en juego, o si es el comodín de elegir color
            self.playable_cards.append(card)

    if self.color not in suits_in_hand:  # Si no tenemos ninguna carta del mismo color que la que está en el área de juego
        for card in hand:
            if card.rank == 14:  # "robacuatro":
                self.playable_cards.append(card)  # Lo añadimos a las cartas que podemos jugar

    if self.hands[i].status == 1:  # si el jugador es IA
        self.AI_plays(hand)

    else:  # si el jugador es humano
        self.human_plays(hand)

    # Consideraciones de final de turno, a continuación

    self.color = self.card_in_play.suit
    self.color_in_play = self.card_in_play.suits[self.color]

    if self.deck.is_empty():  # Si no quedan cartas en el mazo
        self.play_discard()

    self.place_cards()
    self.update_surface()

    if self.hands[i].is_empty():  # Si no quedan cartas en la mano
        end_game = 0
        self.main_surface.fill(self.surface_color)
        if self.hands[i].name == self.player_name:  # Ha ganado el jugador humano
            pygame.mixer.music.load(os.path.join(main_dir, 'UNO', "win.mp3"))
            pygame.mixer.music.play(-1)
            win = Text(100, 300, "¡Enhorabuena, " + self.player_name + "! Has ganado la partida")
            self.main_surface.blit(win.text, win.position)
        else:  # Ha ganado la IA
            pygame.mixer.music.load(os.path.join(main_dir, 'UNO', "loss.mp3"))
            pygame.mixer.music.play(-1)
            loss = Text(100, 300, "¡Lo sentimos, " + self.player_name + "! El ordenador ha ganado la partida")
            self.main_surface.blit(loss.text, loss.position)
        self.blit_buttons(6, 8)
        pygame.display.flip()
        while end_game == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Hemos hecho click
                    place_of_click = event.dict["pos"]
                    for button in self.all_buttons[6:8]:
                        if button.contains_point(place_of_click):
                            if button == self.all_buttons[6]:
                                end_game = 1
                                self.deck = Deck()
                                self.deck.shuffle()
                                self.play_UNO()
                            else:
                                pygame.quit()
                                sys.exit()

    pygame.display.flip()


def AI_plays(self, hand):
    if not self.playable_cards:  # No podemos jugar ninguna carta, tenemos que robar
        drawn_card = self.deck.pop()
        if drawn_card.suit == self.color or drawn_card.rank == self.card_in_play.rank or drawn_card.suit == 4:  # "Comodín":
            # Si la carta robada comparte color o número con la que está en juego, o si es un comodín
            self.card_in_play = drawn_card  # Jugamos la carta robada
            self.has_drawn = 0
            # hand.remove(drawn_card) ¡No es necesario, porque no llega a añadir la carta a la mano! Dará error
            self.discard_deck.cards.append(drawn_card)
        else:
            hand.append(drawn_card)  # Añadimos la carta robada a nuestra mano

    else:  # No nos hace falta robar, porque tenemos en la mano cartas que podemos jugar
        rng = random.Random()
        selected_card = self.playable_cards[
            rng.randrange(0, len(self.playable_cards))]  # La IA elige la carta que jugar
        self.card_in_play = selected_card  # La carta elegida será la próxima carta en juego
        self.has_drawn = 0
        self.card_in_play.position = self.play_area  # Adjudicamos a la carta elegida la zona de juego
        hand.remove(selected_card)
        self.discard_deck.cards.append(selected_card)


def human_plays(self, hand):
    self.has_drawn = 0
    has_played = 0
    has_playable_cards = 0
    while self.has_drawn == 0:
        if not self.playable_cards:  # No podemos jugar ninguna carta, tenemos que robar
            for event in pygame.event.get():  # event = pygame.event.poll()  # Buscar eventos y asignárselos a la variable event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Hemos hecho click
                    place_of_click = event.dict["pos"]
                    if self.deck.contains_point(place_of_click):
                        drawn_card = self.deck.pop()
                        if drawn_card.suit == self.color or drawn_card.rank == self.card_in_play.rank or drawn_card.suit == 4:  # "Comodín":
                            self.playable_cards.append(drawn_card)
                            has_playable_cards = 1
                        else:
                            pygame.display.flip()
                        self.has_drawn = 1
                        hand.append(drawn_card)
                        # Actualizamos las cartas
                        self.place_cards()
                        self.update_surface()
        else:
            has_playable_cards = 1
            self.has_drawn = 1

    while has_played == 0:
        if has_playable_cards == 1:  # Podemos jugar
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Hemos hecho click
                    place_of_click = event.dict["pos"]
                    for card in self.playable_cards:
                        if card.contains_point(place_of_click):
                            self.card_in_play = card
                            hand.remove(card)
                            self.discard_deck.cards.append(card)
                            has_played = 1
                            self.has_drawn = 0

        else:  # Tenemos que pasar turno
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Hemos hecho click
                    place_of_click = event.dict["pos"]
                    if self.all_buttons[4].contains_point(place_of_click):
                        has_played = 1

