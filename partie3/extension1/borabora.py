"""Partie 3 - Extension 1: deux serveurs partagent les commandes.
Version reconstituée à partir du fichier final fourni par la collègue.
"""

import asyncio
import sys
import time
import re


##################################
# LOG
##################################

class Logable:

    def __init__(self, name, verbose):
        self.name = name
        self.verbose = verbose

    def log(self, msg):
        if self.verbose:
            print(f"[{self.name}] {msg}", file=logf, flush=True)


##################################
# ACCESSOIRES
##################################

class Accessoire(asyncio.Queue, Logable):

    def __init__(self, name, verbose):
        asyncio.Queue.__init__(self)
        Logable.__init__(self, name, verbose)


class Pic(Accessoire):

    async def embrocher(self, postit):

        await self.put(postit)

        self.log(
            f"post-it '{postit}' embroché, "
            f"{self.qsize()} post-it(s) à traiter"
        )

    async def liberer(self):

        postit = await self.get()

        if postit is None:
            return None

        self.log(
            f"post-it '{postit}' libéré, "
            f"{self.qsize()} post-it(s) à traiter"
        )

        return postit


class Bar(Accessoire):

    async def recevoir(self, commande):

        await self.put(commande)

        self.log(
            f"'{commande}' posée, "
            f"{self.qsize()} commande(s) à servir"
        )

    async def evacuer(self):

        commande = await self.get()

        if commande is None:
            return None

        self.log(
            f"'{commande}' évacuée, "
            f"{self.qsize()} commande(s) à servir"
        )

        return commande


##################################
# CLIENTS
##################################

class Clients:

    def __init__(self, fname):

        commandes = []

        start = time.time()
        fmt = re.compile(r"(\d+)\s+(.*)")

        with open(fname, "r", encoding="utf-8") as f:

            for line in f:

                found = fmt.search(line)

                if found:

                    when = int(found.group(1))
                    what = found.group(2)

                    start += when

                    commandes.append((start, what.split(",")))

        self.commandes = commandes[::-1]

        # Protection contre les accès simultanés
        # des deux serveurs aux commandes.
        self.lock = asyncio.Lock()

    async def commande(self):

        async with self.lock:

            if len(self.commandes) == 0:
                return None

            date_commande, cocktails = self.commandes[-1]

            attente = max(0, date_commande - time.time())

            await asyncio.sleep(attente)

            self.commandes.pop()

            return cocktails


##################################
# EMPLOYES
##################################

class Employé(Logable):

    def __init__(
        self, pic, bar, clients,
        name, verbose
    ):

        super().__init__(name, verbose)

        self.pic = pic
        self.bar = bar
        self.clients = clients

        self.step = 0

        self.log("prêt pour le service")


##################################
# SERVEURS
##################################

class Serveur(Employé):

    def __init__(
        self, pic, bar, clients,
        name, verbose
    ):

        super().__init__(
            pic, bar, clients,
            name, verbose
        )

        # Empêche un serveur de prendre une commande
        # pendant qu'il est en train d'en servir une.
        self.lock = asyncio.Lock()

    async def prendre_commande(self):

        commande = await self.clients.commande()

        if commande is None:
            return False

        async with self.lock:

            self.log("prêt pour prendre une nouvelle commande...")

            self.log(f"j'ai la commande '{commande}'")

            self.log(f"j'écris sur le post-it '{commande}'")

            await self.pic.embrocher(commande)

        return True

    async def servir(self):

        commande = await self.bar.evacuer()

        if commande is None:
            return False

        async with self.lock:

            self.log(f"j'apporte la commande '{commande}'")

            for cocktail in commande:

                self.log(f"je sers '{cocktail}'")

                await asyncio.sleep(0.2)

        return True


##################################
# BARISTE
##################################

class Bariste(Employé):

    async def preparer(self):

        commande = await self.pic.liberer()

        if commande is None:
            return False

        self.log(f"je commence la fabrication de '{commande}'")

        for cocktail in commande:
            self.log(f"je prépare '{cocktail}'")
            await asyncio.sleep(0.2)

        self.log(f"la commande {commande} est prête")
        await self.bar.recevoir(commande)
        return True


##################################
# TACHES ASYNCHRONES
##################################

# Chaque serveur prend les commandes des clients.
async def prendre_les_commandes(serveur):

    while await serveur.prendre_commande():
        pass


# Les deux serveurs partagent la même liste de clients.
# On attend qu'ils aient terminé avant de signaler
# au bariste la fin de la prise des commandes.
async def prendre_toutes_les_commandes(serveurs, pic):

    await asyncio.gather(
        *(prendre_les_commandes(s) for s in serveurs)
    )

    await pic.put(None)


# Le bariste prépare les commandes.
async def preparer_les_commandes(bariste, nb_serveurs):

    while await bariste.preparer():
        pass

    # Un signal de fin pour chaque serveur.
    for _ in range(nb_serveurs):
        await bariste.bar.recevoir(None)



# Chaque serveur sert les commandes disponibles.
async def servir_les_commandes(serveur):

    while await serveur.servir():
        pass


##################################
# PROGRAMME PRINCIPAL
##################################

def usage():

    print(f"Usage : python3 {sys.argv[0]} fichier")

    sys.exit(1)


async def main():

    if len(sys.argv) != 2:
        usage()

    fcommandes = sys.argv[1]

    global logf

    logfile = "/tmp/borabora.log"

    print(f"Logging in {logfile}...")

    with open(logfile, "w", encoding="utf-8") as logf:

        print("\n---", file=logf, flush=True)

        # Création des accessoires.
        le_pic = Pic(name="le_pic", verbose=True)

        le_bar = Bar(name="le_bar", verbose=True)

        les_clients = Clients(fcommandes)

        # Création du bariste.
        bob = Bariste(
            le_pic,
            le_bar,
            les_clients,
            name="bob",
            verbose=True,
            # Temporisation fixe à cette étape.
        )

        # Création du premier serveur.
        alice = Serveur(
            le_pic,
            le_bar,
            les_clients,
            name="alice",
            verbose=True,
            # Temporisation fixe à cette étape.
        )

        # Extension 1 : deuxième serveur.
        charlie = Serveur(
            le_pic,
            le_bar,
            les_clients,
            name="charlie",
            verbose=True,
            # Temporisation fixe à cette étape.
        )

        serveurs = [alice, charlie]

        # Lancement des tâches concurrentes.
        await asyncio.gather(

            # Les deux serveurs prennent les commandes.
            prendre_toutes_les_commandes(
                serveurs, le_pic
            ),

            # Le bariste prépare les commandes.
            preparer_les_commandes(
                bob, len(serveurs)
            ),

            # Les deux serveurs servent les commandes.
            *(servir_les_commandes(s) for s in serveurs)
        )


if __name__ == "__main__":

    asyncio.run(main())