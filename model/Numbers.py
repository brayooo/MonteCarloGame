import json
import random

with open('pseudoRandomNumbersForShots.json', 'r') as file:
    data = json.load(file)
    shot_numbers = data['numbers']

with open('pseudoRandomNumbersGender.json', 'r') as file:
    data = json.load(file)
    gender_numbers = data['numbers']

with open('pseudoRandomNumbers.json', 'r') as file:
    data = json.load(file)
    multi_purpose_numbers = data['numbers']

with open('uniformDistributionNumbers.json', 'r') as file:
    data = json.load(file)
    uniform_numbers = data['numbers']


class Numbers:
    """
        Una clase que utiliza números pseudoaleatorios pregenerados para diversos fines.

        Atributos:
            pseudo_random_shot (generador): Un generador que produce números pseudoaleatorios para tiros.
            pseudo_random_gender (generador): Un generador que produce números pseudoaleatorios para decidir el género.
            pseudo_random_numbers (generador): Un generador de propósito general que produce números pseudoaleatorios.
            uniform_pseudo_random_numbers (generador): Un generador que produce números de una distribución uniforme.
    """
    def __init__(self):
        """
        Inicializa la clase Numbers con números pseudoaleatorios pregenerados.
        """
        self.pseudo_random_shot = self.pseudo_random_generator(shot_numbers)
        self.pseudo_random_gender = self.pseudo_random_generator(gender_numbers)
        self.pseudo_random_numbers = self.pseudo_random_generator(multi_purpose_numbers)
        self.uniform_pseudo_random_numbers = self.pseudo_random_generator(uniform_numbers)

    def pseudo_random_generator(self, numbers):
        """
        Crea un generador que produce números de la lista dada.

        Args:
            numbers (list): Una lista de números pseudoaleatorios pregenerados.

        Returns:
            generator: Un generador que produce números de la lista.
        """
        for number in numbers:
            yield number

    def get_next_pseudo_random_shot(self):
        """
        Devuelve el siguiente número pseudoaleatorio para un tiro.

        Returns:
            int: El siguiente número pseudoaleatorio para un tiro.
        """
        try:
            return next(self.pseudo_random_shot)
        except StopIteration:
            # Reiniciar el generador
            self.pseudo_random_shot = self.pseudo_random_generator(shot_numbers)
            return next(self.pseudo_random_shot)

    def get_next_pseudo_random_gender(self):
        """
        Devuelve el siguiente número pseudoaleatorio para decidir el género.

        Returns:
            int: El siguiente número pseudoaleatorio para decidir el género.
        """
        try:
            return next(self.pseudo_random_gender)
        except StopIteration:
            self.pseudo_random_gender = self.pseudo_random_generator(gender_numbers)
            return next(self.pseudo_random_gender)

    def get_next_pseudo_random_number(self):
        """
        Devuelve el siguiente número pseudoaleatorio de propósito general.

        Returns:
            int: El siguiente número pseudoaleatorio de propósito general.
        """
        try:
            return next(self.pseudo_random_numbers)
        except StopIteration:
            self.pseudo_random_numbers = self.pseudo_random_generator(multi_purpose_numbers)
            return next(self.pseudo_random_numbers)

    def get_next_uniform_pseudo_random_number(self):
        """
        Devuelve el siguiente número pseudoaleatorio de una distribución uniforme.

        Returns:
            float: El siguiente número pseudoaleatorio de una distribución uniforme.
        """
        try:
            return next(self.uniform_pseudo_random_numbers)
        except StopIteration:
            self.uniform_pseudo_random_numbers = self.pseudo_random_generator(uniform_numbers)
            return next(self.uniform_pseudo_random_numbers)

    def decide_gender(self):
        """
        Devuelve 1 para masculino y 0 para femenino basado en un número pseudoaleatorio.

        Returns:
            int: 1 para masculino, 0 para femenino.
        """
        random.shuffle(gender_numbers)
        if self.get_next_pseudo_random_gender() > 50:
            return 1
        else:
            return 0

    def decide_shot(self):
        """
        Devuelve un número pseudoaleatorio para decidir el resultado de un tiro.

        Returns:
            int: Un número pseudoaleatorio para decidir el resultado de un tiro.
        """
        random.shuffle(multi_purpose_numbers)
        return self.get_next_pseudo_random_number()

    def get_random_number(self):
        """
        Devuelve un número pseudoaleatorio para decidir el genero del arquero.

        Returns:
            int: genero representado 0 (mujer) y 1 (hombre).
        """
        random.shuffle(multi_purpose_numbers)
        if self.get_next_pseudo_random_number() > 0.5:
            return 1
        else:
            return 2

    def get_random_uniform_number(self):
        """
        Devuelve un número pseudoaleatorio para establecer la suerte del jugador.

        Returns:
            int: Un número pseudoaleatorio uniforme entre 1 y 3.
        """
        random.shuffle(uniform_numbers)
        return self.get_next_uniform_pseudo_random_number()
