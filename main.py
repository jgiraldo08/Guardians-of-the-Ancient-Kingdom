import pytest
from personajes import Personaje, Guerrero, Mago, Arquero, Combate


def test_crear_guerrero():
    p = Guerrero("Arthas", 100, 30, 20)
    assert isinstance(p, Personaje)
    assert (p.get_nombre(), p.get_vida(), p.get_ataque(), p.get_defensa()) == ("Arthas", 100, 30, 20)


def test_crear_mago():
    p = Mago("Gandalf", 80, 40, 10)
    assert isinstance(p, Personaje)
    assert (p.get_nombre(), p.get_vida(), p.get_ataque(), p.get_defensa()) == ("Gandalf", 80, 40, 10)


def test_crear_arquero():
    p = Arquero("Legolas", 90, 35, 15)
    assert isinstance(p, Personaje)
    assert (p.get_nombre(), p.get_vida(), p.get_ataque(), p.get_defensa()) == ("Legolas", 90, 35, 15)


def test_personaje_es_abstracto():
    with pytest.raises(TypeError):
        Personaje("X", 100, 10, 10)


def test_vida_mayor_a_100():
    with pytest.raises(ValueError):
        Guerrero("X", 101, 10, 10)


def test_vida_negativa():
    with pytest.raises(ValueError):
        Guerrero("X", -1, 10, 10)


def test_nombre_vacio():
    with pytest.raises(ValueError):
        Mago("", 100, 10, 10)
    with pytest.raises(ValueError):
        Mago("   ", 100, 10, 10)


def test_ataque_invalido():
    with pytest.raises(ValueError):
        Arquero("X", 100, 0, 10)
    with pytest.raises(ValueError):
        Arquero("X", 100, -5, 10)
    with pytest.raises(ValueError):
        Arquero("X", 100, "a", 10)


def test_defensa_invalida():
    with pytest.raises(ValueError):
        Arquero("X", 100, 10, -1)
    with pytest.raises(ValueError):
        Arquero("X", 100, 10, "a")


def test_setters():
    p = Guerrero("X", 50, 10, 10)
    p.set_vida(80)
    assert p.get_vida() == 80
    with pytest.raises(ValueError):
        p.set_vida(101)


def test_habilidad_guerrero():
    objetivo = Guerrero("B", 100, 10, 10)
    assert Guerrero("A", 100, 30, 20).atacar(objetivo) == 26
    assert objetivo.get_vida() == 74


def test_habilidad_mago_ignora_defensa():
    objetivo = Guerrero("B", 100, 10, 20)
    assert Mago("A", 100, 40, 5).atacar(objetivo) == 40
    assert objetivo.get_vida() == 60


def test_habilidad_arquero_critico():
    objetivo = Guerrero("B", 100, 10, 15)
    assert Arquero("A", 100, 35, 5).atacar(objetivo) == 40


def test_arquero_sin_superar_defensa():
    objetivo = Guerrero("B", 100, 10, 15)
    assert Arquero("A", 100, 10, 5).atacar(objetivo) == 0
    assert objetivo.get_vida() == 100


def test_vida_no_negativa():
    p = Guerrero("X", 20, 10, 10)
    assert p.recibir_danio(50) == 20
    assert p.get_vida() == 0
    assert not p.esta_vivo()


def test_danio_negativo():
    with pytest.raises(ValueError):
        Guerrero("X", 20, 10, 10).recibir_danio(-1)


def test_derrotado_no_ataca():
    objetivo = Guerrero("B", 100, 10, 10)
    with pytest.raises(ValueError):
        Guerrero("A", 0, 10, 10).atacar(objetivo)
    with pytest.raises(ValueError):
        Mago("A", 0, 10, 10).atacar(objetivo)
    with pytest.raises(ValueError):
        Arquero("A", 0, 10, 10).atacar(objetivo)


def test_objetivo_invalido():
    atacante = Mago("A", 100, 10, 10)
    with pytest.raises(ValueError):
        atacante.atacar(Guerrero("B", 0, 10, 10))
    with pytest.raises(ValueError):
        atacante.atacar("no soy personaje")


def test_combate_completo_y_ganador():
    arthas = Guerrero("Arthas", 100, 30, 20)
    gandalf = Mago("Gandalf", 80, 40, 10)
    combate = Combate(arthas, gandalf)
    assert combate.iniciar() is gandalf
    assert arthas.get_vida() == 0
    assert gandalf.get_vida() == 2
    assert combate.rondas == 3


def test_empate_tecnico():
    combate = Combate(Guerrero("A", 100, 1, 100), Guerrero("B", 100, 1, 100))
    assert combate.iniciar() is None
    assert "técnico" in combate.resultado
    assert combate.rondas == 1


def test_empate_50_rondas():
    a = Mago("A", 100, 1, 0)
    b = Mago("B", 100, 1, 0)
    combate = Combate(a, b)
    assert combate.iniciar() is None
    assert combate.rondas == 50
    assert a.get_vida() == 50 and b.get_vida() == 50


def test_combate_invalido():
    with pytest.raises(ValueError):
        Combate(Guerrero("A", 100, 10, 10), "x")
    with pytest.raises(ValueError):
        Combate(Guerrero("A", 100, 10, 10), Mago("B", 0, 10, 10))


def demostracion():
    print("##### PERSONAJES #####")
    arthas = Guerrero("Arthas", 100, 30, 20)
    gandalf = Mago("Gandalf", 80, 40, 10)
    legolas = Arquero("Legolas", 90, 35, 15)
    print(arthas.mostrar_estado())
    print(gandalf.mostrar_estado())
    print(legolas.mostrar_estado())

    print("\n##### HABILIDADES (contra un muñeco de defensa 15) #####")
    print("Guerrero causa:", arthas.atacar(Guerrero("Muñeco", 100, 10, 15)))
    print("Mago causa:", gandalf.atacar(Guerrero("Muñeco", 100, 10, 15)))
    print("Arquero causa:", legolas.atacar(Guerrero("Muñeco", 100, 10, 15)))

    print("\n##### VALIDACIONES #####")
    try:
        Guerrero("", 100, 10, 10)
    except ValueError as error:
        print("Error:", error)
    try:
        Mago("X", 150, 10, 10)
    except ValueError as error:
        print("Error:", error)

    print("\n##### COMBATE DE EJEMPLO #####")
    Combate(Guerrero("Arthas", 100, 30, 20), Mago("Gandalf", 80, 40, 10)).iniciar()


if __name__ == "__main__":
    demostracion()
    print("\n##### CASOS DE PRUEBA #####")
    pytest.main([__file__, "-v"])
