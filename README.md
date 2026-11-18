# Bar à cocktails — Simulation Python asynchrone

Projet de programmation orientée objet en Python simulant le fonctionnement d'un bar à cocktails. Le programme retrace les actions des employés, depuis la prise de commande jusqu'à la préparation et au service, en enregistrant leurs activités dans un journal.

Le développement est organisé **par parties et par étapes**, afin de conserver une version exécutable de chaque évolution et de faciliter le suivi de l'avancement.

## Fonctionnement général

Le bar utilise deux accessoires partagés :

- **Le pic** reçoit les post-it des commandes à préparer.
- **Le bar** reçoit les plateaux préparés, en attente de service.

Le ou les **serveurs** récupèrent les commandes des clients, les transmettent au pic et servent les cocktails. Le **bariste** prépare les commandes et les dépose sur le bar ; dans la dernière extension, il peut aussi servir directement certaines commandes.

```text
Clients ──commande──> Serveur(s) ──post-it──> Pic
                                                │
                                                ▼
                                              Bariste
                                                │
                       ┌────────────────────────┴─────────────┐
                       ▼                                      ▼
                Bar (plateaux prêts)                Service direct (ext. 3)
                       │                                      │
                       ▼                                      ▼
                   Serveur(s)                               Clients
                       │
                       ▼
                     Clients
```

## Structure du dépôt

```text
bar-a-cocktails/
├── partie1/
│   ├── etape1/borabora.py
│   ├── etape2/borabora.py
│   └── etape3/borabora.py
├── partie2/
│   ├── etape1/borabora.py
│   ├── etape2/borabora.py
│   ├── etape3/borabora.py
│   └── etape4/borabora.py
├── partie3/
│   ├── extension1/borabora.py
│   ├── extension2/borabora.py
│   └── extension3/borabora.py
├── commandes/
│   ├── lundi.txt
│   └── mardi.txt
├── tests/
│   ├── test_partie1_etape1.py
│   ├── test_partie1_etape2.py
│   ├── test_partie1_etape3.py
│   ├── test_partie2_etape1.py
│   ├── test_partie2_etape2.py
│   ├── test_partie2_etape3.py
│   ├── test_partie2_etape4.py
│   ├── test_partie3_extension1.py
│   ├── test_partie3_extension2.py
│   └── test_partie3_extension3.py
|
├── README.md
└── .gitignore
```

Chaque dossier d'étape contient son propre `borabora.py`. Les programmes sont **des versions successives**, pas des modules à exécuter tous ensemble.

## Progression du projet

| Partie | Étape | Réalisation |
| --- | --- | --- |
| 1 | Étape 1 | Simulation séquentielle, classes `Accessoire`, `Pic`, `Bar`, `Employé`, `Serveur`, `Bariste` ; saisie au clavier |
| 1 | Étape 2 | Lecture automatique des commandes depuis un fichier avec `Clients` |
| 1 | Étape 3 | Journalisation configurable avec `Logable`, `name` et `verbose` |
| 2 | Étape 1 | Introduction de `async def`, `await` et `asyncio.gather()` |
| 2 | Étape 2 | Remplacement des listes par `asyncio.Queue` ; signalisation de la fin des traitements |
| 2 | Étape 3 | Coopération des coroutines et attentes non bloquantes avec `asyncio.sleep()` |
| 2 | Étape 4 | Synchronisation des activités d'un serveur avec `asyncio.Lock()` |
| 3 | Extension 1 | Ajout d'un second serveur, Charlie, avec ressources partagées |
| 3 | Extension 2 | Temporisation individuelle (`delai`) pour chaque employé |
| 3 | Extension 3 | Service direct de certaines commandes par Bob quand le pic est vide |

**Remarque sur les versions :** les extensions 1 et 2 de la partie 3 ont été **reconstituées rétrospectivement** à partir du fichier final fourni par la collègue ; elles illustrent la progression fonctionnelle, mais ne correspondent pas nécessairement à ses versions historiques. L'extension 3 conserve sa version finale.

## Installation

Prérequis : Python 3 avec `asyncio` (bibliothèque standard), Git et un terminal. VS Code est facultatif.

```bash
git clone https://github.com/jcgeorges/bar-a-cocktails.git
cd bar-a-cocktails
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pytest
```

Sous Windows, la commande d'activation de l'environnement virtuel est différente (`.venv\\Scripts\\activate` dans PowerShell). Aucune bibliothèque externe n'est nécessaire à l'**exécution** des simulations ; `pytest` sert uniquement aux tests.

## Exécuter une version

Depuis **la racine du dépôt** :

```bash
# Partie 1 : saisie manuelle des commandes (Entrée vide pour terminer)
python3 partie1/etape1/borabora.py

# Partie 1 : lecture des fichiers
python3 partie1/etape2/borabora.py commandes/lundi.txt
python3 partie1/etape3/borabora.py commandes/mardi.txt

# Partie 2 : évolution asynchrone
python3 partie2/etape1/borabora.py commandes/lundi.txt
python3 partie2/etape2/borabora.py commandes/lundi.txt
python3 partie2/etape3/borabora.py commandes/mardi.txt
python3 partie2/etape4/borabora.py commandes/mardi.txt

# Partie 3 : trois extensions séparées
python3 partie3/extension1/borabora.py commandes/mardi.txt
python3 partie3/extension2/borabora.py commandes/mardi.txt
python3 partie3/extension3/borabora.py commandes/mardi.txt
```

Pour lancer directement la **version la plus complète**, utiliser :

```bash
python3 partie3/extension3/borabora.py commandes/mardi.txt
```

Les versions intermédiaires de la partie 2 permettent notamment d'observer les difficultés de la concurrence avant l'introduction des files, de la coopération et des verrous. Elles ne constituent pas toutes des solutions finales autonomes.

## Format des commandes

Les fichiers de `commandes/` contiennent une commande par ligne :

```text
0 tequila sunrise,margarita
0 daiquiri,ti-punch
```

Chaque ligne comporte un entier de temporisation puis des noms de cocktails séparés par une virgule. Dans la **partie 3**, les délais sont cumulés pour planifier l'arrivée successive des commandes. Les versions antérieures conservent leur propre implémentation de `Clients` : ne pas supposer que toutes interprètent ces valeurs de la même manière.

## Journalisation

À partir de la partie 1, étape 3, les actions sont enregistrées dans :

```text
/tmp/borabora.log
```

Consulter le journal après une exécution :

```bash
cat /tmp/borabora.log
```

Le suivre dans un second terminal :

```bash
tail -f /tmp/borabora.log
```

Le paramètre `verbose=True` active les messages d'une instance ; `verbose=False` les désactive. **Le fichier est ouvert en écriture à chaque lancement : son contenu précédent est remplacé.** Le chemin `/tmp/borabora.log` est adapté à l'environnement Linux/Ubuntu du projet.

## Tests

Les tests se trouvent dans `tests/`, avec un fichier associé à chaque étape ou extension.

```bash
# Tous les tests
python -m pytest tests/ -v

# Une étape précise
python -m pytest tests/test_partie2_etape4.py -v

# Tests de la partie 3
python -m pytest tests/test_partie3_extension1.py tests/test_partie3_extension2.py tests/test_partie3_extension3.py -v
```

Les tests portent notamment sur les accessoires, l'ordre de traitement, la lecture des commandes, les logs, la déclaration des coroutines, les files FIFO, la terminaison des tâches, les verrous et les trois extensions.

**Vérifications effectuées sur les fichiers de la partie 3 fournis pour revue :** 8 tests automatisés réussis ; les extensions 1, 2 et 3 ont été exécutées avec `lundi.txt` et `mardi.txt`, avec quatre puis seize cocktails préparés et servis. L'extension 3 a aussi été relancée plusieurs fois avec `mardi.txt` ; les essais supplémentaires ont abouti. Ces vérifications ne remplacent pas l'exécution de **l'ensemble** des tests sur le dépôt local complet.

## Points de conception et limites

- Les premières versions de la partie 1 utilisent un retrait **LIFO** (`pop()`) dans les accessoires pour reproduire les sorties demandées, bien que l'introduction du sujet décrive des files **FIFO**. Les versions asynchrones passent à `asyncio.Queue` (FIFO).
- Dans la partie 3, un verrou protège la liste de commandes partagée entre les deux serveurs, et chaque serveur dispose d'un verrou empêchant le chevauchement de sa prise de commande et de son service.
- Les tâches reçoivent des sentinelles `None` pour annoncer la fin des commandes et éviter certaines attentes infinies.
- Dans l'extension 3, Bob oriente une commande vers le service direct lorsque le pic est vide **après sa préparation**. Cette règle peut conduire Bob à servir beaucoup de cocktails ; elle ne garantit pas une répartition équitable entre les employés.
- La concurrence dépend de l'ordonnancement de `asyncio` : l'ordre exact des messages et la répartition du travail peuvent varier selon les exécutions.
- Les tests actuels vérifient des comportements ciblés ; ils ne démontrent pas l'absence de tous les problèmes de concurrence ou des erreurs de saisie.

