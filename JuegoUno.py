import random
import time


colores = ('ROJO', 'VERDE', 'AZUL', 'AMARILLO')
rangos = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Saltar', 'Invertir', 'Robar2', 'Robar4')
tipo_carta = {'0': 'numero', '1': 'numero', '2': 'numero', '3': 'numero', '4': 'numero', '5': 'numero', '6': 'numero',
              '7': 'numero', '8': 'numero', '9': 'numero', 'Saltar': 'accion', 'Invertir': 'accion', 'Robar2': 'accion',
              'Robar4': 'accion_sincolor'}

class Carta:

    def __init__(self, color, rango):
        self.rango = rango
        if tipo_carta[rango] == 'numero':
            self.color = color
            self.tipo_carta = 'numero'
        elif tipo_carta[rango] == 'accion':
            self.color = color
            self.tipo_carta = 'accion'
        else:
            self.color = None
            self.tipo_carta = 'accion_sincolor'

    def __str__(self):
        if self.color is None:
            return self.rango
        else:
            return self.color + " " + self.rango


class Baraja:

    def __init__(self):
        self.baraja = []
        for clr in colores:
            for ran in rangos:
                if tipo_carta[ran] != 'accion_sincolor':
                    self.baraja.append(Carta(clr, ran))
                    self.baraja.append(Carta(clr, ran))
                else:
                    self.baraja.append(Carta(clr, ran))

    def __str__(self):
        comp_baraja = ''
        for carta in self.baraja:
            comp_baraja += '\n' + carta.__str__()
        return 'La baraja tiene ' + comp_baraja

    def barajar(self):
        random.shuffle(self.baraja)

    def repartir(self):
        return self.baraja.pop()


class Mano:

    def __init__(self):
        self.cartas = []
        self.cartas_str = []
        self.cartas_numero = 0
        self.cartas_accion = 0

    def agregar_carta(self, carta):
        self.cartas.append(carta)
        self.cartas_str.append(str(carta))
        if carta.tipo_carta == 'numero':
            self.cartas_numero += 1
        else:
            self.cartas_accion += 1

    def remover_carta(self, posicion):
        self.cartas_str.pop(posicion - 1)
        return self.cartas.pop(posicion - 1)

    def cartas_en_mano(self):
        for i in range(len(self.cartas_str)):
            print(f' {i + 1}.{self.cartas_str[i]}')

    def una_carta(self, posicion):
        return self.cartas[posicion - 1]

    def numero_de_cartas(self):
        return len(self.cartas)


# Función para seleccionar aleatoriamente quién empieza primero
def elegir_primero():
    if random.randint(0, 1) == 0:
        return 'Jugador'
    else:
        return 'PC'


# Función para verificar si la carta jugada por el Jugador/PC es válida comparándola con la carta superior
def verificar_carta_unica(carta_superior, carta):
    if carta.color == carta_superior.color or carta_superior.rango == carta.rango or carta.tipo_carta == 'accion_sincolor':
        return True
    else:
        return False


# PARA PC SOLAMENTE
# Para verificar si la PC tiene alguna carta válida para jugar
def revisar_mano_completa(mano, carta_superior):
    for c in mano.cartas:
        if c.color == carta_superior.color or c.rango == carta_superior.rango or c.tipo_carta == 'accion_sincolor':
            return mano.remover_carta(mano.cartas_str.index(str(c)) + 1)
    else:
        return 'sin carta'


# Función para verificar si alguno gana
def verificar_ganador(mano):
    if len(mano.cartas) == 0:
        return True
    else:
        return False


# Función para verificar si la última carta es una carta de acción (EL JUEGO DEBE TERMINAR CON UNA CARTA NUMÉRICA)
def verificar_ultima_carta(mano):
    for c in mano.cartas:
        if c.tipo_carta != 'numero':
            return True
    else:
        return False


# El bucle del juego
while True:

    print('¡Bienvenido a UNO! Termina tus cartas primero para ganar')

    baraja = Baraja()
    baraja.barajar()

    mano_jugador = Mano()
    for i in range(7):
        mano_jugador.agregar_carta(baraja.repartir())

    mano_pc = Mano()
    for i in range(7):
        mano_pc.agregar_carta(baraja.repartir())

    carta_superior = baraja.repartir()
    if carta_superior.tipo_carta != 'numero':
        while carta_superior.tipo_carta != 'numero':
            carta_superior = baraja.repartir()
    print('\nLa carta inicial es: {}'.format(carta_superior))
    time.sleep(1)
    jugando = True

    turno = elegir_primero()
    print(turno + ' irá primero')

    while jugando:

        if turno == 'Jugador':
            print('\nLa carta superior es: ' + str(carta_superior))
            print('Tus cartas: ')
            mano_jugador.cartas_en_mano()
            if mano_jugador.numero_de_cartas() == 1:
                if verificar_ultima_carta(mano_jugador):
                    print('La última carta no puede ser una carta de acción \nAgregando una carta de la baraja')
                    mano_jugador.agregar_carta(baraja.repartir())
                    print('Tus cartas: ')
                    mano_jugador.cartas_en_mano()
            eleccion = input("\n¿Jugar o Sacar una carta? (j/s): ")
            if eleccion == 'j':
                pos = int(input('Ingrese el índice de la carta: '))
                temp_carta = mano_jugador.una_carta(pos)
                if verificar_carta_unica(carta_superior, temp_carta):
                    if temp_carta.tipo_carta == 'numero':
                        carta_superior = mano_jugador.remover_carta(pos)
                        turno = 'PC'
                    else:
                        if temp_carta.rango == 'Saltar':
                            turno = 'Jugador'
                            carta_superior = mano_jugador.remover_carta(pos)
                        if temp_carta.rango == 'Saltar':
                            turno = 'Jugador'
                            carta_superior = mano_jugador.remover_carta(pos)
                        elif temp_carta.rango == 'Invertir':
                            turno = 'Jugador'
                            carta_superior = mano_jugador.remover_carta(pos)
                        elif temp_carta.rango == 'Robar2':
                            mano_pc.agregar_carta(baraja.repartir())
                            mano_pc.agregar_carta(baraja.repartir())
                            carta_superior = mano_jugador.remover_carta(pos)
                            turno = 'Jugador'
                        elif temp_carta.rango == 'Robar4':
                            for i in range(4):
                                mano_pc.agregar_carta(baraja.repartir())
                            carta_superior = mano_jugador.remover_carta(pos)
                            color_cambio = input('Cambiar color a (ingrese en mayúsculas): ')
                            if color_cambio != color_cambio.upper():
                                color_cambio = color_cambio.upper()
                            carta_superior.color = color_cambio
                            turno = 'Jugador'

                else:
                    print('Esta carta no se puede usar')
            elif eleccion == 's':
                temp_carta = baraja.repartir()
                print('Has obtenido: ' + str(temp_carta))
                time.sleep(1)
                if verificar_carta_unica(carta_superior, temp_carta):
                    mano_jugador.agregar_carta(temp_carta)
                else:
                    print('No se puede usar esta carta')
                    mano_jugador.agregar_carta(temp_carta)
                    turno = 'PC'
            if verificar_ganador(mano_jugador):
                print('\n¡JUGADOR GANÓ!')
                jugando = False
                break

        if turno == 'PC':
            if mano_pc.numero_de_cartas() == 1:
                if verificar_ultima_carta(mano_pc):
                    time.sleep(1)
                    print('Agregando una carta a la mano de la PC')
                    mano_pc.agregar_carta(baraja.repartir())
            temp_carta = revisar_mano_completa(mano_pc, carta_superior)
            time.sleep(1)
            if temp_carta != 'sin carta':
                print(f'\nLa PC tira: {temp_carta}')
                time.sleep(1)
                if temp_carta.tipo_carta == 'numero':
                    carta_superior = temp_carta
                    turno = 'Jugador'
                else:
                    if temp_carta.rango == 'Saltar':
                        turno = 'PC'
                        carta_superior = temp_carta
                    elif temp_carta.rango == 'Invertir':
                        turno = 'PC'
                        carta_superior = temp_carta
                    elif temp_carta.rango == 'Robar2':
                        mano_jugador.agregar_carta(baraja.repartir())
                        mano_jugador.agregar_carta(baraja.repartir())
                        carta_superior = temp_carta
                        turno = 'PC'
                    elif temp_carta.rango == 'Robar4':
                        for i in range(4):
                            mano_jugador.agregar_carta(baraja.repartir())
                        carta_superior = temp_carta
                        color_cambio = mano_pc.cartas[0].color
                        print('El color cambia a', color_cambio)
                        carta_superior.color = color_cambio
                        turno = 'PC'

            else:
                print('\nLa PC toma una carta de la baraja')
                time.sleep(1)
                temp_carta = baraja.repartir()
                if verificar_carta_unica(carta_superior, temp_carta):
                    print(f'La PC tira: {temp_carta}')
                    time.sleep(1)
                    if temp_carta.tipo_carta == 'numero':
                        carta_superior = temp_carta
                        turno = 'Jugador'
                    else:
                        if temp_carta.rango == 'Saltar':
                            turno = 'PC'
                            carta_superior = temp_carta
                        elif temp_carta.rango == 'Invertir':
                            turno = 'PC'
                            carta_superior = temp_carta
                        elif temp_carta.rango == 'Robar2':
                            mano_jugador.agregar_carta(baraja.repartir())
                            mano_jugador.agregar_carta(baraja.repartir())
                            carta_superior = temp_carta
                            turno = 'PC'
                        elif temp_carta.rango == 'Robar4':
                            for i in range(4):
                                mano_jugador.agregar_carta(baraja.repartir())
                            carta_superior = temp_carta
                            color_cambio = mano_pc.cartas[0].color
                            print('El color cambia a', color_cambio)
                            carta_superior.color = color_cambio
                            turno = 'PC'

                else:
                    print('La PC no tiene una carta')
                    time.sleep(1)
                    mano_pc.agregar_carta(temp_carta)
                    turno = 'Jugador'
            print('\nLa PC tiene {} cartas restantes'.format(mano_pc.numero_de_cartas()))
            time.sleep(1)
            if verificar_ganador(mano_pc):
                print('\n¡PC GANÓ!')
                jugando = False

    nuevo_juego = input('¿Te gustaría jugar de nuevo? (s/n)')
    if nuevo_juego == 's':
        continue
    else:
        print('\n¡Gracias por jugar!')
        break