##################################
# partie 2
# etape 1
##################################
# class accessoire herité de la class list 

import asyncio
import sys # permet de recuperer les arguments passés en ligne de commande
import time
import re # permet de faire des recherches dans une chaine de caractères avec des expressions régulières


# classe ajouté pour l'etape 3: permet d'activer ou non l'affichage des messages de log
class Logable:

    def __init__(self, name, verbose): # verbose permet d'activer ou non l'affichage des messages de log
        self.name = name
        self.verbose = verbose

    def log(self, msg): # fonction qui affiche un message de log si verbose est activé
        if self.verbose:
            print(f"[{self.name}] {msg}", file=logf, flush=True)




class Accessoire(list, Logable):

    def __init__(self, name, verbose):
        list.__init__(self)
        Logable.__init__(self, name, verbose)


class Pic(Accessoire):

    def embrocher(self, postit):
        self.append(postit)
        self.log(
            f"post-it '{postit}' embroché, {len(self)} post-it(s) à traiter"
        )

    def liberer(self):
        if len(self) > 0:
            postit = self.pop()
            self.log(
                f"post-it '{postit}' libéré, {len(self)} post-it(s) à traiter"
            )
            return postit

        return None


class Bar(Accessoire):

    def recevoir(self, commande):
        self.append(commande)
        self.log(
            f"'{commande}' posée, {len(self)} commande(s) à servir"
        )

    def evacuer(self):
        if len(self) > 0:
            commande = self.pop()
            self.log(
                f"'{commande}' évacuée, {len(self)} commande(s) à servir"
            )
            return commande

        return None

    
# classe utilisée pour simuler l'arrivée des clients et de leurs commandes à différents moments
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

                    start += when # permet de cumuler la durée d'attente entre chaque commande

                    commandes.append((start, what.split(","))) # what.split(",") transforme une chaine en liste

        self.commandes = commandes[::-1] # inverse la liste pour que la première commande soit en dernier (afin de respecter le fonctionnement LIFO du pic et du bar)

    def commande(self):

        if len(self.commandes) > 0:

            while True:

                if time.time() >= self.commandes[-1][0]:
                    return self.commandes.pop()[1]

                time.sleep(0.01) # permet de ne pas surcharger le processeur en attendant la prochaine commande

        return None



class Employé(Logable):

    def __init__(self, pic, bar, clients, name, verbose):
        super().__init__(name, verbose)

        self.pic = pic
        self.bar = bar
        self.clients = clients
        self.step = 0

        self.log("prêt pour le service")


class Serveur(Employé):

    async def prendre_commande(self):

        self.log("prêt pour prendre une nouvelle commande...")

        commande = self.clients.commande()

        if commande is None:
            return False

        self.log(f"j'ai la commande '{commande}'")
        self.log(f"j'écris sur le post-it '{commande}'")

        self.pic.embrocher(commande)

        return True

    async def servir(self):

        commande = self.bar.evacuer()

        if commande is not None:

            self.log(f"j'apporte la commande '{commande}'")

            for cocktail in commande:
                self.log(f"je sers '{cocktail}'")

            return True

        return False

    async def run(self):

        while await self.prendre_commande():
            pass

        while await self.servir():
            pass


class Bariste(Employé):

    async def preparer(self):

        commande = self.pic.liberer()

        if commande is not None:

            self.log(f"je commence la fabrication de '{commande}'")

            for cocktail in commande:
                self.log(f"je prépare '{cocktail}'")

            self.log(f"la commande {commande} est prête")

            self.bar.recevoir(commande)

            return True

        return False

    async def run(self):

        while await self.preparer():
            pass


# fonctions asynchrones qui permettent de prendre les commandes, de les préparer et de les servir en parallèle
async def prendre_les_commandes(serveur): # fonction asynchrone qui permet de prendre les commandes des clients et de les mettre sur le pic

    while await serveur.prendre_commande():
        pass


async def preparer_les_commandes(bariste): # fonction asynchrone qui permet de préparer les commandes des clients et de les mettre sur le bar

    while await bariste.preparer():
        pass


async def servir_les_commandes(serveur): # fonction asynchrone qui permet de servir les commandes des clients et de les enlever du bar

    while await serveur.servir():
        pass


# affichage de l'usage du programme si les arguments ne sont pas corrects
def usage():
    print(f"Usage : python3 {sys.argv[0]} fichier")
    sys.exit(1)

# fonction principale qui simule le fonctionnement du bar à cocktails
'''
Ici nous constatons que le programme fonctionne toujours de manière séquentielle.

Alice termine de prendre toutes les commandes avant que Bob commence à préparer les cocktails.

Bob termine ensuite toutes les préparations avant qu'Alice commence le service.

Car : 
dans la methode prendre_commande(), nous utilisons encore :
commande = self.clients.commande()

Cette méthode est synchrone et peut bloquer l'exécution.

De plus, nos coroutines ne contiennent pas encore d'instruction await permettant de céder effectivement le contrôle à la boucle d'événements.
Conséquence : chaque tâche s'exécute jusqu'à sa terminaison avant que la suivante puisse progresser.
'''
async def main():

    if len(sys.argv) != 2:
        usage()

    fcommandes = sys.argv[1]

    global logf

    logfile = "/tmp/borabora.log"
    print(f"Logging in {logfile}...")

    with open(logfile, "w", encoding="utf-8") as logf:

        print("\n---", file=logf, flush=True)

        le_pic = Pic(name="le_pic", verbose=True)
        le_bar = Bar(name="le_bar", verbose=True)

        les_clients = Clients(fcommandes)

        bob = Bariste(
            le_pic, le_bar, les_clients,
            name="bob", verbose=True
        )

        alice = Serveur(
            le_pic, le_bar, les_clients,
            name="alice", verbose=True
        )

        await asyncio.gather(
            prendre_les_commandes(alice),
            preparer_les_commandes(bob),
            servir_les_commandes(alice)
        )


if __name__ == "__main__":
    asyncio.run(main())

# tail -f /tmp/borabora.log : commande a mettre dans un autre terminal pour suivre 
# l'execution du programme en temps réel et voir les messages de log du bariste