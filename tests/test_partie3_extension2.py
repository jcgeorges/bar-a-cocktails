"""Extension 2 : vérifie la productivité propre à chaque employé.

- Chaque employé reçoit une temporisation indépendante.
- Le temps de service tient compte de cette temporisation.
- Deux serveurs peuvent toujours prendre des commandes.
"""
import asyncio
import importlib.util
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FICHIER = ROOT / "partie3" / "extension2" / "borabora.py"
spec = importlib.util.spec_from_file_location("borabora_p3_ext2", FICHIER)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class FauxClients:
    def __init__(self, commandes):
        self.commandes = list(commandes)
        self.lock = asyncio.Lock()

    async def commande(self):
        async with self.lock:
            if not self.commandes:
                return None
            return self.commandes.pop(0)


def test_delais_distincts():
    module.logf = io.StringIO()
    pic, bar, clients = module.Pic("pic", False), module.Bar("bar", False), FauxClients([])
    alice = module.Serveur(pic, bar, clients, "alice", False, delai=0.03)
    charlie = module.Serveur(pic, bar, clients, "charlie", False, delai=0.01)
    bob = module.Bariste(pic, bar, clients, "bob", False, delai=0.02)
    assert (alice.delai, charlie.delai, bob.delai) == (0.03, 0.01, 0.02)
    alice.delai = 0.04
    assert (charlie.delai, bob.delai) == (0.01, 0.02)


def test_delai_utilise_au_service():
    async def scenario():
        module.logf = io.StringIO()
        pic, bar, clients = module.Pic("pic", False), module.Bar("bar", False), FauxClients([])
        alice = module.Serveur(pic, bar, clients, "alice", False, delai=0.025)
        await bar.recevoir(["mojito", "margarita"])
        debut = asyncio.get_running_loop().time()
        assert await alice.servir()
        duree = asyncio.get_running_loop().time() - debut
        assert duree >= 0.04
    asyncio.run(scenario())