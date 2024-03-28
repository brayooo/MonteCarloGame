import random

from model.Numbers import Numbers


class Player:
    """
    Clase para representar a un arquero en el juego de arquería.

    Atributos:
        gender (int): Género del arquero, 0 para mujer y 1 para hombre.
        id (int): Identificador único del arquero.
        team (str): Nombre del equipo al que pertenece el arquero.
        initial_resistance (int): Resistencia inicial del arquero, un valor aleatorio entre 25 y 45.
        resistance (int): Resistencia actual del arquero.
        experience (int): Experiencia acumulada del arquero.
        experience_per_round (int): Experiencia acumulada por ronda del arquero.
        luck (float): Valor de suerte actual del arquero.
        accompanied_luck (float): Valor acumulado de suerte del arquero.
        score (int): Puntuación actual del arquero en el juego.
        scores (list): Lista de puntuaciones acumuladas del arquero en cada juego.
        rounds_won (int): Número de rondas ganadas por el arquero.
        lucky_shots (int): Número de tiros afortunados realizados por el arquero.
        reduced_resistance_rounds (int): Número de rondas restantes con resistencia reducida.
        consecutive_lucky_wins (int): Número de tiros afortunados consecutivos ganados por el arquero.
    """
    def __init__(self, id):
        """
        Inicializa una instancia de la clase Player.

        Parámetros:
            id (int): Identificador único del arquero.
        """
        numbers_instance = Numbers()
        self.gender = numbers_instance.decide_gender()
        self.id = id
        self.team = ""
        self.initial_resistance = random.randint(25, 45)
        self.resistance = self.initial_resistance
        self.experience = 10
        self.experience_per_round = 0
        self.luck = 0
        self.accompanied_luck = 0
        self.score = 0
        self.scores = []
        self.rounds_won = 0
        self.lucky_shots = 0
        self.reduced_resistance_rounds = 2
        self.consecutive_lucky_wins = 0

    def __str__(self):
        """
        Devuelve una representación en cadena de la instancia del arquero.

        Retorna:
            str: Una cadena que representa al arquero.
        """
        return (f"Player(Gender: {self.gender}, "
                # f"Initial Resistance: {self.initial_resistance}, "
                f"Resistance: {self.resistance}, "
                f"Experience: {self.experience}, "
                f"Lucky: {self.luck}, "
                f"Score: {self.score}, "
                f"accompanied_luck: {self.accompanied_luck}, "
                f"lucky_wins: {self.consecutive_lucky_wins}, "
                f"id: {self.id}, "
                f"Rounds Won: {self.rounds_won})"
                )
