"""Extension 3 : vérifie le service direct des commandes par Bob.

- Bob oriente une commande vers le service direct si le pic est vide.
- Bob dépose une commande sur le bar si des commandes restent sur le pic.
- Le service direct consomme la file et se termine au marqueur None.
- Le verrou empêche de préparer et servir simultanément.
"""
import asyncio
import importlib.util
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FICHIER = ROOT / "partie3" / "extension3" / "borabora.py"
spec = importlib.util.spec_from_file_location("borabora_p3_ext3", FICHIER)
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


def test_service_direct_pic_vide():
    async def scenario():
        module.logf = io.StringIO()
        pic, bar, directes = module.Pic("pic", False), module.Bar("bar", False), asyncio.Queue()
        bob = module.Bariste(pic, bar, FauxClients([]), directes, "bob", False, delai=0)
        await pic.embrocher(["mojito"])
        assert await bob.preparer()
        assert await directes.get() == ["mojito"]
        assert bar.empty()
    asyncio.run(scenario())


def test_pic_non_vide_passe_par_bar():
    async def scenario():
        module.logf = io.StringIO()
        pic, bar, directes = module.Pic("pic", False), module.Bar("bar", False), asyncio.Queue()
        bob = module.Bariste(pic, bar, FauxClients([]), directes, "bob", False, delai=0)
        await pic.embrocher(["mojito"])
        await pic.embrocher(["margarita"])
        assert await bob.preparer()
        assert await bar.evacuer() == ["mojito"]
        assert directes.empty()
    asyncio.run(scenario())


def test_tache_service_direct_et_fin():
    async def scenario():
        module.logf = io.StringIO()
        pic, bar, directes = module.Pic("pic", False), module.Bar("bar", False), asyncio.Queue()
        bob = module.Bariste(pic, bar, FauxClients([]), directes, "bob", True, delai=0)
        await directes.put(["mojito", "piña colada"])
        await directes.put(None)
        await asyncio.wait_for(bob.servir_directement(), timeout=2)
        assert directes.empty()
        logs = module.logf.getvalue()
        assert "[bob] je sers 'mojito'" in logs
        assert "[bob] je sers 'piña colada'" in logs
    asyncio.run(scenario())


def test_service_direct_attend_verrou():
    async def scenario():
        module.logf = io.StringIO()
        pic, bar, directes = module.Pic("pic", False), module.Bar("bar", False), asyncio.Queue()
        bob = module.Bariste(pic, bar, FauxClients([]), directes, "bob", False, delai=0)
        await directes.put(["mojito"])
        await directes.put(None)
        await bob.lock.acquire()
        tache = asyncio.create_task(bob.servir_directement())
        await asyncio.sleep(0.01)
        assert not tache.done()
        bob.lock.release()
        await asyncio.wait_for(tache, timeout=2)
    asyncio.run(scenario())