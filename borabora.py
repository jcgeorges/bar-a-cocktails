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
