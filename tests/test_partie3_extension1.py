"""Extension 1 : teste les deux serveurs, les files partagées et la fin du service.

- Deux serveurs peuvent récupérer des commandes distinctes.
- Les commandes passent par le pic, le bar et le service sans perte.
- Les marqueurs None arrêtent correctement les tâches de service.
"""
import asyncio
import importlib.util
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FICHIER = ROOT / "partie3" / "extension1" / "borabora.py"
spec = importlib.util.spec_from_file_location("borabora_p3_ext1", FICHIER)
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


def test_deux_serveurs_prennent_les_commandes():
    async def scenario():
        module.logf = io.StringIO()
        pic = module.Pic("pic", False)
        bar = module.Bar("bar", False)
        clients = FauxClients([["mojito"], ["margarita"]])
        alice = module.Serveur(pic, bar, clients, "alice", False)
        charlie = module.Serveur(pic, bar, clients, "charlie", False)
        resultats = await asyncio.gather(alice.prendre_commande(), charlie.prendre_commande())
        assert resultats == [True, True]
        assert await pic.liberer() == ["mojito"]
        assert await pic.liberer() == ["margarita"]
    asyncio.run(scenario())


def test_traitement_complet_deux_serveurs():
    async def scenario():
        module.logf = io.StringIO()
        pic = module.Pic("pic", False)
        bar = module.Bar("bar", False)
        clients = FauxClients([["mojito"], ["margarita"]])
        alice = module.Serveur(pic, bar, clients, "alice", True)
        charlie = module.Serveur(pic, bar, clients, "charlie", True)
        bob = module.Bariste(pic, bar, clients, "bob", True)
        await asyncio.wait_for(asyncio.gather(
            module.prendre_toutes_les_commandes([alice, charlie], pic),
            module.preparer_les_commandes(bob, 2),
            module.servir_les_commandes(alice),
            module.servir_les_commandes(charlie),
        ), timeout=5)
        logs = module.logf.getvalue()
        for cocktail in ("mojito", "margarita"):
            assert logs.count(f"je prépare '{cocktail}'") == 1
            assert logs.count(f"je sers '{cocktail}'") == 1
    asyncio.run(scenario())