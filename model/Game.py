import matplotlib.pyplot as plt

from model.Numbers import Numbers
from model.Player import Player
from model.Team import Team
from prettytable import PrettyTable
from colorama import init, Fore, Style


class Game:
    """
    Clase para representar un juego de arquería entre dos equipos.

    Atributos:
        numbers_instance (Numbers): Instancia de la clase Numbers para el manejo de las decisiones
        fig (matplotlib.figure.Figure): Figura para el gráfico de puntuaciones.
        lines (dict): Diccionario que mapea el ID de cada arquero a su línea en el gráfico.
        round_resistances (list): Lista de resistencias de los arqueros en la ronda actual.
        round_scores (list): Lista de puntuaciones de los arqueros en la ronda actual.
        game_number (int): Número del juego actual.
        team1 (Team): El primer equipo de arqueros.
        team2 (Team): El segundo equipo de arqueros.
    """
    def __init__(self, game):
        self.numbers_instance = Numbers()
        self.fig = None
        self.lines = {}
        plt.ion()  # Habilitar el modo interactivo
        plt.show(block=False)
        init()
        self.round_resistances = []
        self.round_scores = []
        self.game_number = 1
        self.team1 = Team()
        self.team2 = Team()
        self.init_teams()
        self.init_plot()
        self.game(game)

    def game(self, games):
        """
        Inicializa una instancia de la clase Game.

        Parámetros:
            game (int): Número de juegos a jugar.
        """
        for i in range(1, games+1):
            self.round()
            print("Partida:", i)

    def round(self):
        """
        Ejecuta una ronda de juego, donde se cumple con toda la logica propuesta por el docente.
        """
        number_round = 1
        print("Juego", self.game_number)
        while number_round <= 10:
            print("Numero de ronda: ", number_round)
            self.save_resistances()
            self.set_archer_luck()
            self.lucky_shot(self.team1)
            self.lucky_shot(self.team2)
            while not self.verify_resistence(self.team1) and not self.verify_resistence(self.team2):
                for archer in self.team1.get_team + self.team2.get_team:
                    while archer.resistance >= 5:
                        score = self.take_shot(archer)  # Obtener el puntaje del disparo
                        archer.score += score  # Acumular el puntaje total del arquero
                        self.reduce_endurance(archer)
            round_winner = self.round_winner()
            self.fill_archer_scores_per_round()
            self.round_won(round_winner)
            self.reduce_round_resistances()
            self.team_round_winner()
            self.archer_round_winner()
            self.reset_archer_score()
            number_round += 1
        self.table_stats()
        self.reset_original_resistance()
        self.update_plot(self.game_number)
        self.game_number += 1

    def init_plot(self):
        """
        Inicializa la figura y el eje para el gráfico de puntuaciones.
        """
        if self.fig is None:  # Solo crea la figura y el eje si no existen
            self.fig, self.ax = plt.subplots()
            self.ax.set_xlabel('Juegos')
            self.ax.set_ylabel('Puntos')
            self.ax.set_title('Puntos por Jugador vs Juego')
            # Crear las líneas del gráfico para cada arquero y almacenarlas en self.lines
            for team in [self.team1, self.team2]:
                for archer in team.get_team:
                    line, = self.ax.plot([], [], marker='o', linestyle='-', label=f'{archer.id} ({archer.team})')
                    self.lines[archer.id] = line
            self.ax.legend()

    def update_plot(self, game_number):
        """
        Actualiza el gráfico de puntuaciones con los datos de los arqueros.

        Parámetros:
            game_number (int): Número del juego actual.
        """
        for team in [self.team1, self.team2]:
            for archer in team.get_team:
                line = self.lines[archer.id]
                num_scores = len(archer.scores)
                # Evita un desbordamiento si hay más juegos que puntuaciones
                games_to_plot = min(game_number, num_scores)
                # Asegúra de que las puntuaciones se estén actualizando correctamente
                if games_to_plot > 0:
                    line.set_data(range(1, games_to_plot + 1), archer.scores[:games_to_plot])
        # Ajustar los límites del eje y redibujar el gráfico
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw_idle()
        plt.pause(0.02)

    def table_stats(self):
        """
        Muestra estadísticas finales del juego en forma de tablas.
        """
        self.gender_winner()
        self.game_player_winner()
        self.team_and_player_winner()

    def game_player_winner(self):
        """
         Muestra el jugador más afortunado y el más experimentado del juego.
         """
        most_lucky_archer = max(self.team1.team + self.team2.team, key=lambda archer: archer.accompanied_luck)
        most_experiences_archer = max(self.team1.team + self.team2.team, key=lambda archer: archer.experience)
        table = PrettyTable()
        table.field_names = ["Player", "Stats"]
        table.add_row(["Most Lucky Player", most_lucky_archer])
        table.add_row(["Most Experienced Player", most_experiences_archer])

        print(table)

    def team_and_player_winner(self):
        """
        Muestra el equipo ganador y el arquero ganador del juego.
        """
        team_winner = self.winner_team()
        player_winner = self.winner_archer()

        table = PrettyTable()
        table.field_names = ["Winner", "Stats"]
        table.add_row(["Player winner", player_winner])
        table.add_row(["Team winner", f"{team_winner.team_name} (Score: {team_winner.global_score})"])

        print(table)

    def winner_team(self):
        """
        Determina el equipo ganador del juego.

        Retorna:
            Team: El equipo ganador.
        """
        return self.team1 if self.team1.team_rounds_won > self.team2.team_rounds_won else self.team2

    def winner_archer(self):
        """
        Determina el arquero ganador del juego.

        Retorna:
            Player: El arquero ganador.
        """
        return max(self.team1.team + self.team2.team, key=lambda archer: archer.rounds_won)

    def gender_winner(self):
        """
        Muestra el total de victorias por género.
        """
        male_wins = self.team1.male_wins + self.team2.male_wins
        female_wins = self.team1.female_wins + self.team2.female_wins

        table = PrettyTable()
        table.field_names = [Fore.GREEN + "Gender" + Style.RESET_ALL, Fore.GREEN + "Total Wins" + Style.RESET_ALL]
        table.add_row([Fore.BLUE + "Male" + Style.RESET_ALL, str(male_wins)])
        table.add_row([Fore.BLUE + "Female" + Style.RESET_ALL, str(female_wins)])

        print(table)

    def clear_archer_scores(self):
        """
        Limpia las puntuaciones de todos los arqueros.
        """
        for archer in self.team1.get_team + self.team2.get_team:
            archer.scores.clear()

    def winner(self, team):
        """
        Determina el arquero con la puntuación más alta en un equipo.

        Parámetros:
            team (list): Lista de arqueros en el equipo.

        Retorna:
            tuple: La puntuación máxima y el arquero ganador.
        """
        winner = None
        max_score = 0
        for archer in team:
            if archer.score > max_score:
                max_score = archer.score
                winner = archer
        return max_score, winner

    def reset_archer_score(self):
        """
        Restablece la puntuación de todos los arqueros a cero.
        """
        for archer in self.team1.get_team + self.team2.get_team:
            archer.score = 0

    def fill_archer_scores_per_round(self):
        """
        Acumula las puntuaciones de cada arquero al final de cada ronda.
        """
        for archer in self.team1.get_team + self.team2.get_team:
            # Si la lista de scores está vacía, simplemente agregamos la puntuación actual
            if not archer.scores:
                archer.scores.append(archer.score)
            archer.scores.append(archer.scores[-1] + archer.score)

    def archer_round_winner(self):
        """
        Determina el arquero ganador de la ronda en cada equipo y actualiza las victorias por género.
        """
        archer_team_1 = max(self.team1.team, key=lambda archer: archer.score)
        archer_team_2 = max(self.team2.team, key=lambda archer: archer.score)
        archer_team_1.rounds_won += 1
        archer_team_2.rounds_won += 1
        self.gender_round_winner(archer_team_1, archer_team_2)

    def gender_round_winner(self, archer_team_1, archer_team_2):
        """
        Actualiza las victorias por género en función del arquero ganador de la ronda.

        Parámetros:
            archer_team_1 (Player): Arquero ganador del equipo 1.
            archer_team_2 (Player): Arquero ganador del equipo 2.
        """
        if archer_team_1.gender == 0:
            self.team1.female_wins += 1
        elif archer_team_1.gender == 1:
            self.team1.male_wins += 1
        elif archer_team_2.gender == 0:
            self.team2.female_wins += 1
        else:  # Si no es ninguno de los anteriores, entonces debe ser archer_team_2.gender == 1
            self.team2.male_wins += 1

    def round_won(self, archer):
        """
        Actualiza la experiencia del arquero ganador de la ronda.

        Parámetros:
            archer (Player): Arquero ganador de la ronda.
        """
        archer.experience_per_round += 3
        archer.experience += 3
        if archer.experience_per_round == 9:
            archer.reduced_resistance_rounds += 2  # Sumar 2 a las rondas de resistencia reducida

    def round_winner(self):
        """
        Determina el arquero ganador de la ronda entre los dos equipos.

        Retorna:
            Player: Arquero ganador de la ronda.
        """
        team1_archer_max_score, archer_team1_winner = self.winner(self.team1.get_team)
        team2_archer_max_score, archer_team2_winner = self.winner(self.team2.get_team)

        if team1_archer_max_score > team2_archer_max_score:
            return archer_team1_winner
        elif team1_archer_max_score > team2_archer_max_score:
            return archer_team2_winner
        else:
            # Empate, realizar lanzamientos extra hasta determinar un ganador
            return self.tiebreaker(archer_team1_winner, archer_team2_winner)

    def team_round_winner(self):
        """
        Determina el equipo ganador de la ronda y actualiza las puntuaciones globales.
        """
        score_team1 = sum(archer.score for archer in self.team1.team)
        score_team2 = sum(archer.score for archer in self.team2.team)
        self.team1.score = score_team1
        self.team2.score = score_team2
        self.team1.global_score += score_team1
        self.team2.global_score += score_team2
        if score_team1 > score_team2:
            self.team1.team_rounds_won += 1
        else:
            self.team2.team_rounds_won += 1

    def reduce_round_resistances(self):
        """
        Reduce la resistencia de los arqueros al final de cada ronda.
        """
        all_archers = self.team1.get_team + self.team2.get_team
        for i, resistence in enumerate(self.round_resistances):
            if i < len(all_archers):
                archer = all_archers[i]
                if archer.experience_per_round >= 9 and archer.reduced_resistance_rounds > 0:
                    archer.resistance = resistence - 1
                    archer.reduced_resistance_rounds -= 1
                else:
                    archer.resistance = resistence - self.numbers_instance.get_random_number()
                archer.experience_per_round = 0

    def take_shot(self, archer):
        """
        Simula un disparo de un arquero y retorna la puntuación obtenida.

        Parámetros:
            archer (Player): El arquero que realiza el disparo.

        Retorna:
            int: La puntuación obtenida en el disparo.
        """
        shot = self.numbers_instance.decide_shot()
        if archer.gender == 0:  # Mujeres
            if shot <= 0.30:
                return 10  # Central
            elif shot <= 0.30 + 0.38:
                return 9  # Intermedia
            elif shot <= 0.30 + 0.38 + 0.27:
                return 8  # Exterior
            else:
                return 0  # Error
        else:  # Hombres
            if shot <= 0.20:
                return 10  # Central
            elif shot <= 0.20 + 0.33:
                return 9  # Intermedia
            elif shot <= 0.20 + 0.33 + 0.40:
                return 8  # Exterior
            else:
                return 0  # Error

    def reduce_endurance(self, player):
        """
        Reduce la resistencia de un jugador después de realizar un disparo.

        Parámetros:
            player (Player): El jugador cuya resistencia se va a reducir.
        """
        if player.resistance >= 5:
            player.resistance -= 5
        else:
            print("El jugador no tiene suficiente resistencia para hacer el tiro.", player.id)

    def verify_resistence(self, team):
        """
        Verifica si todos los jugadores de un equipo tienen suficiente resistencia para disparar.

        Parámetros:
            team (Team): El equipo a verificar.

        Retorna:
            bool: Verdadero si todos los jugadores tienen resistencia insuficiente, falso en caso contrario.
        """
        return all(player.resistance < 5 for player in team.get_team)

    def save_resistances(self):
        """
        Guarda las resistencias actuales de todos los arqueros en la ronda.
        """
        self.round_resistances = [archer.resistance for archer in self.team1.get_team + self.team2.get_team]

    def tiebreaker(self, archer1, archer2):
        """
        Desempata entre dos arqueros mediante disparos adicionales.

        Parámetros:
            archer1 (Player): El primer arquero en el desempate.
            archer2 (Player): El segundo arquero en el desempate.

        Retorna:
            Player: El arquero ganador del desempate.
        """
        while True:
            score1 = self.take_shot(archer1)
            score2 = self.take_shot(archer2)
            if score1 > score2:
                return archer1
            elif score2 > score1:
                return archer2

    def lucky_shot(self, team):
        """
        Realiza un disparo afortunado para el arquero más afortunado del equipo.

        Parámetros:
            team (Team): El equipo que realiza el disparo afortunado.
        """
        max_luck = 0
        most_lucky_archer = None
        for archer in team.get_team:
            if archer.accompanied_luck > max_luck and archer.resistance > 0:
                max_luck = archer.accompanied_luck
                most_lucky_archer = archer
        team.score += self.take_shot(most_lucky_archer)
        most_lucky_archer.resistance -= 5
        self.verify_consecutive_lucky_shot(most_lucky_archer, team)

    def verify_consecutive_lucky_shot(self, archer, team):
        """
        Verifica si un arquero ha ganado tres lanzamientos de suerte seguidos y realiza un lanzamiento extra si es así.

        Parámetros:
            archer (Player): El arquero a verificar.
            team (Team): El equipo del arquero.
        """
        if archer is not None:
            archer.consecutive_lucky_wins += 1
            if archer.consecutive_lucky_wins == 3:  # Si ganó tres lanzamientos de suerte seguidos
                archer.consecutive_lucky_wins = 0  # Restablecer el contador
                team.score += self.take_shot(archer)  # Realizar el lanzamiento extra

    def set_initial_resistence(self):
        """
        Establece la resistencia inicial de todos los arqueros.
        """
        for archer in self.team1.get_team + self.team2.get_team:
            archer.resistance = archer.initial_resistence

    def set_archer_luck(self):
        """
        Asigna un valor de suerte a cada arquero y acumula su suerte acompañada.
        """
        for archer in self.team1.team + self.team2.team:
            archer.luck = self.numbers_instance.get_random_uniform_number()
            archer.accompanied_luck += archer.luck

    def reset_original_resistance(self):
        """
        Restablece la resistencia original de todos los arqueros y reinicia su experiencia por ronda.
        """
        all_archers = self.team1.get_team + self.team2.get_team
        for archer in all_archers:
            archer.resistance = archer.initial_resistance
            archer.experience_per_round = 0

    def init_teams(self):
        """
        Inicializa los equipos y asigna los arqueros a cada equipo.
        """
        for i in range(10):
            archer = Player(i)

            if i < 5:  # Primeros 5 jugadores van al equipo 1
                archer.team = "Team 1"
                self.team1.team_name = "Team 1"
            else:  # Siguientes 5 jugadores van al equipo 2
                archer.team = "Team 2"
                self.team2.team_name = "Team 2"
            if archer.team == "Team 1":
                self.team1.get_team.append(archer)
            else:
                self.team2.get_team.append(archer)
