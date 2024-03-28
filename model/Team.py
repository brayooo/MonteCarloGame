class Team:
    """
    Clase para representar un equipo de arqueros en el juego de arquería.

    Atributos:
        team (str): Nombre del equipo.
        team (list): Lista de objetos Player que representan los arqueros del equipo.
        global_score (int): Puntuación global acumulada del equipo en todos los juegos.
        score (int): Puntuación del equipo en el juego actual.
        team_rounds_won (int): Número de rondas ganadas por el equipo en el juego actual.
        male_wins (int): Número de victorias masculinas en el equipo.
        female_wins (int): Número de victorias femeninas en el equipo.
    """
    def __init__(self):
        """
        Inicializa una instancia de la clase Team.
        """
        self.team_name = ""
        self.team = []
        self.global_score = 0
        self.score = 0
        self.team_rounds_won = 0
        self.male_wins = 0
        self.female_wins = 0

    @property
    def get_team(self):
        """
        Devuelve la lista de arqueros del equipo.

        Retorna:
            list: Lista de objetos Player que representan los arqueros del equipo.
        """
        return self.team

    def __str__(self):
        """
        Devuelve una representación en cadena de la instancia del equipo.

        Retorna:
            str: Una cadena que representa al equipo y sus arqueros.
        """
        players_str = ", ".join([str(player) for player in self.team])
        return (f"Team(Rounds Won: {self.team_rounds_won},"
                f"Team Score: {self.score},"
                f"Global Score: {self.global_score},"
                f"Players: [{players_str}])")
