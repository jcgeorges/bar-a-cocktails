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
            return self.pop(0) # on utilise pop(0) pour retirer la première commande ajoutée à la bar: FIFO(firt in first out)

        return None


# test
if __name__ == "__main__":

    pic = Pic()
    bar = Bar()

    commande1 = ["mojito", "margarita"]
    commande2 = ["daiquiri", "piña colada"]

    # Le serveur dépose deux commandes
    pic.embrocher(commande1)
    pic.embrocher(commande2)

    print("Commandes sur le pic :", pic)

    # Le bariste récupère une commande
    commande = pic.liberer()

    print("Commande récupérée :", commande)

    # Le bariste dépose la commande préparée
    bar.recevoir(commande)

    print("Commandes sur le bar :", bar)

    # Le serveur récupère la commande
    commande_servie = bar.evacuer()

    print("Commande servie :", commande_servie)