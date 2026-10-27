import importlib.util
import inspect
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FICHIER = ROOT / "partie2" / "etape1" / "borabora.py"

spec = importlib.util.spec_from_file_location(
    "borabora_partie2_etape1", FICHIER
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_coroutines():

    assert inspect.iscoroutinefunction(
        module.Serveur.prendre_commande
    )

    assert inspect.iscoroutinefunction(
        module.Serveur.servir
    )

    assert inspect.iscoroutinefunction(
        module.Bariste.preparer
    )


def test_main_asynchrone():

    assert inspect.iscoroutinefunction(module.main)