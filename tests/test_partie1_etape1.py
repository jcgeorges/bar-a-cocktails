'''
Ici l'instruction assert permet de verifier qu'une condition est vraie:
- Si la condition est vraie, le programme continue son execution normalement.
- Si la condition est fausse, une exception AssertionError est levée et le programme s'arrête.
'''
import importlib.util
from pathlib import Path


# Chemin vers le programme de l'étape 1
ROOT = Path(__file__).resolve().parents[1]
FICHIER = ROOT / "partie1" / "etape1" / "borabora.py"

# Charger le programme
spec = importlib.util.spec_from_file_location("borabora_etape1", FICHIER)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

Pic = module.Pic
Bar = module.Bar


def test_pic():

    pic = Pic()

    commande1 = ["mojito", "margarita"]
    commande2 = ["daiquiri", "piña colada"]

    pic.embrocher(commande1)
    pic.embrocher(commande2)

    assert len(pic) == 2

    # Le pic retire la dernière commande ajoutée
    assert pic.liberer() == commande2
    assert pic.liberer() == commande1

    # Le pic est maintenant vide
    assert pic.liberer() is None


def test_bar():

    bar = Bar()

    commande1 = ["mojito", "margarita"]
    commande2 = ["daiquiri", "piña colada"]

    bar.recevoir(commande1)
    bar.recevoir(commande2)

    assert len(bar) == 2

    # Comportement attendu à l'étape 1
    assert bar.evacuer() == commande2
    assert bar.evacuer() == commande1

    # Le bar est maintenant vide
    assert bar.evacuer() is None