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