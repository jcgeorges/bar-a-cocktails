##################################
# partie 1
# etape 3
##################################
# class accessoire herité de la class list 

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

    def prendre_commande(self):

        self.log("prêt pour prendre une nouvelle commande...")

        commande = self.clients.commande()

        if commande is None:
            return False

        self.log(f"j'ai la commande '{commande}'")
        self.log(f"j'écris sur le post-it '{commande}'")

        self.pic.embrocher(commande)

        return True

    def servir(self):

        commande = self.bar.evacuer()

        if commande is not None:

            self.log(f"j'apporte la commande '{commande}'")

            for cocktail in commande:
                self.log(f"je sers '{cocktail}'")

            return True

        return False

    def run(self):

        while self.prendre_commande():
            pass

        while self.servir():
            pass


class Bariste(Employé):

    def preparer(self):

        commande = self.pic.liberer()

        if commande is not None:

            self.log(f"je commence la fabrication de '{commande}'")

            for cocktail in commande:
                self.log(f"je prépare '{cocktail}'")

            self.log(f"la commande {commande} est prête")

            self.bar.recevoir(commande)

            return True

        return False

    def run(self):

        while self.preparer():
            pass

# affichage de l'usage du programme si les arguments ne sont pas corrects
def usage():
    print(f"Usage : python3 {sys.argv[0]} fichier")
    sys.exit(1)

# fonction principale qui simule le fonctionnement du bar à cocktails
def main():

    if len(sys.argv) != 2:
        usage()

    fcommandes = sys.argv[1]

    global logf # permet de rendre la variable logf accessible dans toutes les fonctions et classes du programme

    logfile = "/tmp/borabora.log" # creation d'un fichier de log pour stocker les messages de log dans un fichier temporaire pour pouvoir les consulter après l'exécution du programme
    print(f"Logging in {logfile}...")

    with open(logfile, "w", encoding="utf-8") as logf: # ouverture du fichier de log en mode écriture (w) pour créer un nouveau fichier ou écraser le contenu existant

        print("\n---", file=logf, flush=True)

        le_pic = Pic(name="le_pic", verbose=False)
        le_bar = Bar(name="le_bar", verbose=False)

        les_clients = Clients(fcommandes)

         # initialisation des employés avec le nom et le mode verbose pour activer ou non l'affichage des messages de log
        bob = Bariste(
            le_pic, le_bar, les_clients,
            name="bob", verbose=True
        )

        # les messages du bariste sont desactivés pour ne pas surcharger la sortie standard, mais ils sont stockés dans le fichier de log
        # et les messages du serveur sont activés pour suivre l'exécution du programme en temps réel
        alice = Serveur(
            le_pic, le_bar, les_clients,
            name="alice", verbose=True
        )

        # Prise des commandes
        while alice.prendre_commande():
            pass

        # Préparation des cocktails
        bob.run()

        # Service des cocktails
        while alice.servir():
            pass


if __name__ == "__main__":
    main()

# tail -f /tmp/borabora.log : commande a mettre dans un autre terminal pour suivre 
# l'execution du programme en temps réel et voir les messages de log du bariste