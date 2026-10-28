import asyncio
import importlib.util
import io
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FICHIER = ROOT / "partie2" / "etape2" / "borabora.py"

spec = importlib.util.spec_from_file_location(
    "borabora_partie2_etape2", FICHIER
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_pic():

    async def scenario():

        module.logf = io.StringIO()

        pic = module.Pic(name="le_pic", verbose=True)

        commande1 = ["mojito", "margarita"]
        commande2 = ["daiquiri", "piña colada"]

        await pic.embrocher(commande1)
        await pic.embrocher(commande2)

        assert pic.qsize() == 2

        # Vérification du comportement FIFO
        assert await pic.liberer() == commande1
        assert await pic.liberer() == commande2

        # Marqueur de fin
        await pic.embrocher(None)

        assert await pic.liberer() is None

    asyncio.run(scenario())


def test_bar():

    async def scenario():

        module.logf = io.StringIO()

        bar = module.Bar(name="le_bar", verbose=True)

        commande1 = ["mojito", "margarita"]
        commande2 = ["daiquiri", "piña colada"]

        await bar.recevoir(commande1)
        await bar.recevoir(commande2)

        assert bar.qsize() == 2

        # Vérification du comportement FIFO
        assert await bar.evacuer() == commande1
        assert await bar.evacuer() == commande2

        await bar.recevoir(None)

        assert await bar.evacuer() is None

    asyncio.run(scenario())


def test_simulation_complete():

    fichier_commandes = ROOT / "commandes" / "lundi.txt"

    resultat = subprocess.run(
        [
            sys.executable,
            str(FICHIER),
            str(fichier_commandes)
        ],
        capture_output=True,
        text=True,
        timeout=10
    )

    assert resultat.returncode == 0

    contenu = Path("/tmp/borabora.log").read_text(
        encoding="utf-8"
    )

    # Vérifier que tous les cocktails ont été servis
    assert "[alice] je sers 'tequila sunrise'" in contenu
    assert "[alice] je sers 'margarita'" in contenu
    assert "[alice] je sers 'daiquiri'" in contenu
    assert "[alice] je sers 'ti-punch'" in contenu

    # Vérifier que le bariste a préparé les commandes
    assert "[bob] je prépare 'tequila sunrise'" in contenu
    assert "[bob] je prépare 'ti-punch'" in contenu