import asyncio
import importlib.util
import io
from pathlib import Path

# Ici, Nous allons vérifier deux éléments :
# 1. Chaque serveur possède un verrou asyncio.Lock.
# 2. Alice ne peut pas prendre une commande pendant qu'elle sert un plateau.

ROOT = Path(__file__).resolve().parents[1]
FICHIER = ROOT / "partie2" / "etape4" / "borabora.py"

spec = importlib.util.spec_from_file_location(
    "borabora_partie2_etape4", FICHIER
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_verrou_serveur():

    async def scenario():

        module.logf = io.StringIO()

        pic = module.Pic(name="le_pic", verbose=False)
        bar = module.Bar(name="le_bar", verbose=False)

        alice = module.Serveur(
            pic, bar, None,
            name="alice", verbose=True
        )

        assert isinstance(alice.lock, asyncio.Lock)

    asyncio.run(scenario())


def test_synchronisation_serveur():

    async def scenario():

        module.logf = io.StringIO()

        pic = module.Pic(name="le_pic", verbose=False)
        bar = module.Bar(name="le_bar", verbose=False)

        # Client fictif qui retourne une commande immédiatement
        class FauxClients:

            async def commande(self):
                return ["daiquiri"]

        clients = FauxClients()

        alice = module.Serveur(
            pic, bar, clients,
            name="alice", verbose=True
        )

        # Une première commande est prête à être servie
        await bar.recevoir(["mojito", "margarita"])

        # Alice commence le service
        tache_service = asyncio.create_task(alice.servir())

        # Laisser le service commencer
        await asyncio.sleep(0.05)

        # Une nouvelle commande arrive pendant le service
        tache_commande = asyncio.create_task(
            alice.prendre_commande()
        )

        # Attendre la fin des deux activités
        await asyncio.wait_for(
            asyncio.gather(tache_service, tache_commande),
            timeout=5
        )

        logs = module.logf.getvalue()

        # Position des événements dans les logs
        position_margarita = logs.index("je sers 'margarita'")
        position_commande = logs.index("j'ai la commande")

        # Alice termine le service avant de prendre la commande
        assert position_margarita < position_commande

        # La nouvelle commande a bien été déposée sur le pic
        assert await pic.liberer() == ["daiquiri"]

    asyncio.run(scenario())