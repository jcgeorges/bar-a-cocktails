"""
Partie 1 - Étape 3 : Tests du système de journalisation.

Ce fichier vérifie :
- Le fonctionnement des accessoires Pic et Bar.
- L'enregistrement des actions du pic : ajout et retrait des post-it.
- L'enregistrement des actions du bar : dépôt et retrait des commandes.
- La présence du nom de chaque objet dans les messages de log.
- L'activation des messages lorsque verbose=True.
- La désactivation des messages lorsque verbose=False.

Les logs sont enregistrés en mémoire avec io.StringIO()
pour éviter de créer un fichier pendant les tests.
"""


import importlib.util
import io
from pathlib import Path


# Chargement du programme de l'étape 3
ROOT = Path(__file__).resolve().parents[1]
FICHIER = ROOT / "partie1" / "etape3" / "borabora.py"

spec = importlib.util.spec_from_file_location(
    "borabora_etape3", FICHIER
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

Pic = module.Pic
Bar = module.Bar
Bariste = module.Bariste
Serveur = module.Serveur


def test_pic():

    module.logf = io.StringIO()

    pic = Pic(name="le_pic", verbose=True)

    commande = ["mojito", "margarita"]

    pic.embrocher(commande)

    assert len(pic) == 1
    assert pic.liberer() == commande
    assert pic.liberer() is None

    logs = module.logf.getvalue()

    assert "[le_pic]" in logs
    assert "embroché" in logs
    assert "libéré" in logs


def test_bar():

    module.logf = io.StringIO()

    bar = Bar(name="le_bar", verbose=True)

    commande = ["mojito", "margarita"]

    bar.recevoir(commande)

    assert len(bar) == 1
    assert bar.evacuer() == commande
    assert bar.evacuer() is None

    logs = module.logf.getvalue()

    assert "[le_bar]" in logs
    assert "posée" in logs
    assert "évacuée" in logs


def test_verbose():

    module.logf = io.StringIO()

    pic = Pic(name="le_pic", verbose=False)
    bar = Bar(name="le_bar", verbose=False)

    bob = Bariste(
        pic, bar, None,
        name="bob", verbose=False
    )

    alice = Serveur(
        pic, bar, None,
        name="alice", verbose=True
    )

    logs = module.logf.getvalue()

    assert "[alice] prêt pour le service" in logs
    assert "[bob]" not in logs
    assert "[le_pic]" not in logs
    assert "[le_bar]" not in logs