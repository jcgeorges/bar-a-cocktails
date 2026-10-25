import importlib.util
from pathlib import Path


# Chemin vers le programme de l'étape 2
ROOT = Path(__file__).resolve().parents[1]
FICHIER = ROOT / "partie1" / "etape2" / "borabora.py"

# Charger le programme
spec = importlib.util.spec_from_file_location("borabora_etape2", FICHIER)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

Pic = module.Pic
Bar = module.Bar
Clients = module.Clients


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
    assert bar.evacuer() == commande2
    assert bar.evacuer() == commande1
    assert bar.evacuer() is None


def test_clients_lundi():

    fichier = ROOT / "commandes" / "lundi.txt"

    clients = Clients(fichier)

    commande1 = clients.commande()
    commande2 = clients.commande()
    commande3 = clients.commande()

    assert commande1 == ["tequila sunrise", "margarita"]
    assert commande2 == ["daiquiri", "ti-punch"]
    assert commande3 is None