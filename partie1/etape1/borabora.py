##################################
# partie 1
# etape 1
##################################
# class accessoire herité de la class list 
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

class Employé:

    def __init__(self, pic, bar, clients):
        self.pic = pic
        self.bar = bar
        self.clients = clients

        print(f"{self.__class__.__name__}: prêt pour le service")



class Serveur(Employé):

    def prendre_commande(self):

        commande = input(
            "Serveur: prêt pour prendre une commande : "
        )

        if commande == "":
            return False

        print(f"Serveur: j'ai la commande '{commande}'")

        postit = commande.split(",") # transforme une chaine en liste

        print(f"Serveur: j'écris sur le post-it '{postit}'")

        self.pic.embrocher(postit) # depose cette commande(liste) sur le pic

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


# fonction principale qui simule le fonctionnement du bar à cocktails
def main():

    le_pic = Pic()
    le_bar = Bar()

    bob = Bariste(le_pic, le_bar, None)
    alice = Serveur(le_pic, le_bar, None)

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
