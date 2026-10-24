from abc import ABC, abstractmethod


def entero_valido(valor, minimo, maximo=None):
    if type(valor) is not int:
        return False
    if valor < minimo:
        return False
    if maximo is not None and valor > maximo:
        return False
    return True


class Personaje(ABC):
    def __init__(self, nombre, vida, ataque, defensa):
        self.set_nombre(nombre)
        self.set_vida(vida)
        self.set_ataque(ataque)
        self.set_defensa(defensa)

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        if type(nombre) is not str or nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacío")
        self.__nombre = nombre.strip()

    def get_vida(self):
        return self.__vida

    def set_vida(self, vida):
        if not entero_valido(vida, 0, 100):
            raise ValueError("La vida debe ser un entero entre 0 y 100")
        self.__vida = vida

    def get_ataque(self):
        return self.__ataque

    def set_ataque(self, ataque):
        if not entero_valido(ataque, 1):
            raise ValueError("El ataque debe ser un entero positivo")
        self.__ataque = ataque

    def get_defensa(self):
        return self.__defensa

    def set_defensa(self, defensa):
        if not entero_valido(defensa, 0):
            raise ValueError("La defensa debe ser un entero no negativo")
        self.__defensa = defensa

    def recibir_danio(self, cantidad):
        if not entero_valido(cantidad, 0):
            raise ValueError("El daño debe ser un entero no negativo")
        recibido = cantidad
        if cantidad > self.__vida:  # la vida no puede quedar negativa
            recibido = self.__vida
        self.__vida = self.__vida - recibido
        return recibido

    def esta_vivo(self):
        return self.__vida > 0

    def mostrar_estado(self):
        return f"{type(self).__name__} {self.__nombre}: vida {self.__vida}, ataque {self.__ataque}, defensa {self.__defensa}"

    def validar_ataque(self, objetivo):
        if not isinstance(objetivo, Personaje) or objetivo is self:
            raise ValueError("Objetivo inválido")
        if not self.esta_vivo():
            raise ValueError(f"{self.get_nombre()} está derrotado y no puede atacar")
        if not objetivo.esta_vivo():
            raise ValueError(f"{objetivo.get_nombre()} ya está derrotado")

    @abstractmethod
    def atacar(self, objetivo):
        pass


class Guerrero(Personaje):
    def atacar(self, objetivo):
        self.validar_ataque(objetivo)
        ataque_potenciado = self.get_ataque() * 120 // 100  # +20 % sin decimales (redondea hacia abajo)
        danio = ataque_potenciado - objetivo.get_defensa()
        if danio < 0:
            danio = 0
        return objetivo.recibir_danio(danio)


class Mago(Personaje):
    def atacar(self, objetivo):
        self.validar_ataque(objetivo)
        return objetivo.recibir_danio(self.get_ataque())


class Arquero(Personaje):
    def atacar(self, objetivo):
        self.validar_ataque(objetivo)
        danio = 0
        if self.get_ataque() > objetivo.get_defensa():
            danio = (self.get_ataque() - objetivo.get_defensa()) * 2
        return objetivo.recibir_danio(danio)


class Combate:
    def __init__(self, personaje1, personaje2):
        if not isinstance(personaje1, Personaje) or not isinstance(personaje2, Personaje):
            raise ValueError("Los participantes deben ser personajes")
        if personaje1 is personaje2:
            raise ValueError("Los participantes deben ser distintos")
        if not personaje1.esta_vivo() or not personaje2.esta_vivo():
            raise ValueError("Los participantes deben estar vivos")
        self.atacante = personaje1
        self.defensor = personaje2
        self.rondas = 0
        self.ganador = None
        self.resultado = ""

    def cambiar_turno(self):
        temporal = self.atacante
        self.atacante = self.defensor
        self.defensor = temporal

    def verificar_ganador(self):
        if not self.defensor.esta_vivo():
            return self.atacante
        if not self.atacante.esta_vivo():
            return self.defensor
        return None

    def iniciar(self):
        while self.resultado == "" and self.rondas < 50:
            self.rondas += 1
            danio_ronda = 0
            for turno in range(2):  # cada personaje ataca una vez por ronda
                danio = self.atacante.atacar(self.defensor)
                danio_ronda += danio
                print(f"Ronda {self.rondas}: {self.atacante.get_nombre()} ataca a {self.defensor.get_nombre()} y causa {danio}")
                print("  " + self.atacante.mostrar_estado())
                print("  " + self.defensor.mostrar_estado())
                self.ganador = self.verificar_ganador()
                if self.ganador is not None:
                    self.resultado = "Ganador: " + self.ganador.get_nombre()
                    break
                self.cambiar_turno()
            if self.resultado == "" and danio_ronda == 0:
                self.resultado = "Empate técnico: ronda sin daño"
        if self.resultado == "":
            self.resultado = "Empate: 50 rondas sin ganador"
        self.mostrar_resultado()
        return self.ganador

    def mostrar_resultado(self):
        print(f">>> {self.resultado} (rondas: {self.rondas})")
