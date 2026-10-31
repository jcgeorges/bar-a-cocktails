##################################
# partie 2
# etape 3
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




class Accessoire(asyncio.Queue, Logable): # file async capable d'enregistrer des messages de log

    def __init__(self, name, verbose):
        asyncio.Queue.__init__(self)
        Logable.__init__(self, name, verbose)



class Pic(Accessoire):

    async def embrocher(self, postit):

        await self.put(postit) # ajoute le post-it à la file d'attente de manière asynchrone

        self.log(
            f"post-it '{postit}' embroché, "
            f"{self.qsize()} post-it(s) à traiter"
        )

    async def liberer(self):

        postit = await self.get() # récupère le post-it de la file d'attente de manière asynchrone  

        if postit is None:
            return None

        self.log(
            f"post-it '{postit}' libéré, "
            f"{self.qsize()} post-it(s) à traiter"
        ) # self.qsize() retourne le nombre d'éléments dans la file d'attente

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

    async def commande(self):
        
        if len(self.commandes) == 0:
            return None 
        
        date_commande, cocktails = self.commandes[-1] # récupère la prochaine commande et sa date de disponibilité, sans encore la retirer.
        
        attente = max(0, date_commande - time.time()) # calcule la durée d'attente.
        # Par exemple, si une commande doit arriver dans quatre secondes : attente = 4
        # Nous utilisons max(0, ...) pour éviter une durée négative lorsque la date est déjà passée.
        
        await asyncio.sleep(attente) # suspend la coroutine jusqu'à la disponibilité de la commande.
        # Pendant ce temps, Bob peut préparer les cocktails et Alice peut servir des commandes déjà prêtes.
        
        self.commandes.pop() # retire la commande de la liste
        
        return cocktails



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

        commande = await self.clients.commande() # j'ajoute await ici car Clients.commande() est maintenant une coroutine
        
        if commande is None:
            return False
        
        self.log(f"j'ai la commande '{commande}'")
        self.log(f"j'écris sur le post-it '{commande}'")
        
        await self.pic.embrocher(commande) # ajoute le post-it à la file d'attente de manière asynchrone
        
        return True


# Ici, Alice laisse également la possibilité aux autres coroutines de progresser pendant qu'elle sert une commande.
    async def servir(self): 
        
        commande = await self.bar.evacuer() 
        
        if commande is None: 
            
            return False

        self.log(f"j'apporte la commande '{commande}'") 
        
        for cocktail in commande: 
            
            self.log(f"je sers '{cocktail}'")

            await asyncio.sleep(0.2)

        return True

        

    async def run(self):

        while await self.prendre_commande():
            pass

        while await self.servir():
            pass


class Bariste(Employé):

    async def preparer(self):
        
        commande = await self.pic.liberer()
        
        if commande is None:
            return False

        self.log(f"je commence la fabrication de '{commande}'")

        for cocktail in commande:
            
            self.log(f"je prépare '{cocktail}'")
            
            await asyncio.sleep(0.2) # représente une durée de préparation simplifiée de 0,2 seconde par cocktail
            
        self.log(f"la commande {commande} est prête") 
        
        await self.bar.recevoir(commande) 
        
        return True
        

    async def run(self):

        while await self.preparer():
            pass


# fonctions asynchrones qui permettent de prendre les commandes, de les préparer et de les servir en parallèle
async def prendre_les_commandes(serveur):

    while await serveur.prendre_commande():
        pass

    # Fin de la prise des commandes
    await serveur.pic.embrocher(None)


async def preparer_les_commandes(bariste):

    while await bariste.preparer():
        pass

    # Fin de la préparation
    await bariste.bar.recevoir(None)

    
async def servir_les_commandes(serveur): # fonction asynchrone qui permet de servir les commandes des clients et de les enlever du bar

    while await serveur.servir():
        pass


# affichage de l'usage du programme si les arguments ne sont pas corrects
def usage():
    print(f"Usage : python3 {sys.argv[0]} fichier")
    sys.exit(1)

# fonction principale qui simule le fonctionnement du bar à cocktails
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