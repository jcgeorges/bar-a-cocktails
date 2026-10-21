from borabora import Pic, Bar

'''
Ici l'instruction assert permet de verifier qu'une condition est vraie:
- Si la condition est vraie, le programme continue son execution normalement.
- Si la condition est fausse, une exception AssertionError est levée et le programme s'arrête.
'''
def test_pic():
    pic = Pic()

    commande1 = ["mojito", "margarita"]
    commande2 = ["daiquiri", "piña colada"]

    pic.embrocher(commande1)
    pic.embrocher(commande2)

    assert len(pic) == 2

    assert pic.liberer() == commande2
    assert pic.liberer() == commande1

    assert pic.liberer() is None


def test_bar():
    bar = Bar()

    commande1 = ["mojito", "margarita"]
    commande2 = ["daiquiri", "piña colada"]

    bar.recevoir(commande1)
    bar.recevoir(commande2)

    assert len(bar) == 2

    assert bar.evacuer() == commande1
    assert bar.evacuer() == commande2

    assert bar.evacuer() is None