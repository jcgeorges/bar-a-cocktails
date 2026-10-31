"""
Partie 2 - Étape 3 : Tests de la coopération des tâches asynchrones.

Ce fichier vérifie :
- La transformation de Clients.commande() en coroutine.
- La lecture asynchrone des commandes contenues dans lundi.txt.
- Le respect de l'ordre de récupération des commandes.
- Le retour de None après la dernière commande.
- L'exécution complète de la simulation.
- La préparation de tous les cocktails par le bariste.
- Le service de tous les cocktails par le serveur.
- La terminaison du programme sans blocage.

Ces tests valident le fonctionnement général de la simulation.
La coopération effective entre les tâches est également
observée manuellement dans les logs du programme.
"""

import asyncio
import importlib.util
import inspect
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FICHIER = ROOT / "partie2" / "etape3" / "borabora.py"

spec = importlib.util.spec_from_file_location(
    "borabora_partie2_etape3", FICHIER
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_clients_asynchrone():

    assert inspect.iscoroutinefunction(
        module.Clients.commande
    )


def test_lecture_commandes():

    async def scenario():

        fichier = ROOT / "commandes" / "lundi.txt"
        clients = module.Clients(fichier)

        commande1 = await clients.commande()
        commande2 = await clients.commande()
        commande3 = await clients.commande()

        assert commande1 == ["tequila sunrise", "margarita"]
        assert commande2 == ["daiquiri", "ti-punch"]
        assert commande3 is None

    asyncio.run(scenario())


def test_simulation_complete():

    fichier = ROOT / "commandes" / "lundi.txt"

    resultat = subprocess.run(
        [
            sys.executable,
            str(FICHIER),
            str(fichier)
        ],
        capture_output=True,
        text=True,
        timeout=10
    )

    assert resultat.returncode == 0, resultat.stderr

    logs = Path("/tmp/borabora.log").read_text(
        encoding="utf-8"
    )

    cocktails = [
        "tequila sunrise",
        "margarita",
        "daiquiri",
        "ti-punch"
    ]

    for cocktail in cocktails:

        assert f"[bob] je prépare '{cocktail}'" in logs
        assert f"[alice] je sers '{cocktail}'" in logs