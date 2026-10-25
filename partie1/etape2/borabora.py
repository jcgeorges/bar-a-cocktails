##################################
# partie 1
# etape 2
##################################
# class accessoire herité de la class list 

import sys # permet de recuperer les arguments passés en ligne de commande
import time
import re # permet de faire des recherches dans une chaine de caractères avec des expressions régulières


class Accessoire(list):
    pass


class Pic(Accessoire):

    def embrocher(self, postit): # fonction qui recoit un postit contenant une commande et l'ajoute au pic
        self.append(postit)

    def liberer(self): # verifie si le pic contient un postit et le libere si c'est le cas
        if len(self) > 0:
            return self.pop() # avec pop() la derniere commande est retirée en premier

        return None


class Bar(Accessoire):

    def recevoir(self, commande):
        self.append(commande)

    def evacuer(self):
        if len(self) > 0:
            return self.pop() # on utilise pop() pour retirer la première commande ajoutée à la bar: FIFO(firt in first out)

        return None
    
# classe clients utilisé pour l'etape 2
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


class Employé:

    def __init__(self, pic, bar, clients):
        self.pic = pic
        self.bar = bar
        self.clients = clients

        print(f"{self.__class__.__name__}: prêt pour le service")



class Serveur(Employé):

    def prendre_commande(self):

        print("Serveur: prêt pour prendre une nouvelle commande...")

        commande = self.clients.commande()

        if commande is None:
            return False

        print(f"Serveur: j'ai la commande '{commande}'")
        print(f"Serveur: j'écris sur le post-it '{commande}'")

        self.pic.embrocher(commande)

        return True


    def servir(self):

        commande = self.bar.evacuer()

        if commande is not None:

            print(f"Serveur: j'apporte la commande '{commande}'")

            for cocktail in commande:
                print(f"Serveur: je sers '{cocktail}'")

            return True

        return False

    def run(self):

        while self.prendre_commande():
            pass

        while self.servir():
            pass


'''
question pour la partie 1:
L'énoncé indique initialement que le pic et le bar sont deux files FIFO. Pourtant, les exemples de la partie 1 utilisent pop() pour retirer les éléments, ce qui correspond à un fonctionnement LIFO.

je choisis de respecter les exemples d'exécution demandés par l'enoncé mais il me semble avir une contradiction.
'''

class Bariste(Employé):

    def preparer(self):

        commande = self.pic.liberer() # le bariste verifie si le pic contient un postit et le libere si c'est le cas

        if commande is not None:

            print(
                f"Bariste: je commence la fabrication de '{commande}'"
            )

            for cocktail in commande:
                print(f"Bariste: je prépare '{cocktail}'")

            print(f"Bariste: la commande {commande} est prête")

            self.bar.recevoir(commande) # dépose la commande prête sur la bar

            return True

        return False

    def run(self): # demande au bariste de preparer les commandes tant qu'il y en a sur le pic

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

    le_pic = Pic()
    le_bar = Bar()

    les_clients = Clients(fcommandes)

    bob = Bariste(le_pic, le_bar, les_clients)
    alice = Serveur(le_pic, le_bar, les_clients)

    # Prise des commandes
    while alice.prendre_commande():
        pass

    # Préparation des commandes
    bob.run()

    # Service des cocktails
    while alice.servir():
        pass


if __name__ == "__main__":
    main()

