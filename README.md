# Stats-Meteo

Ce dépôt est le résultat d'un projet universitaire portant sur june étude statistique de données météo melant deux matières (les bases de données ainsi que les statistiques).

Pour ce faire, nous avons décidé de regrouper de vrais données météo trouvées sur Internet afin de générer plusieurs graphiques.

Ce document markdown a pour but de répertorier toutes les fonctions présentent dans le programme permettant de générer des graphiques (ces dernières étant déjà commenté dans le programme pour leur compréhension).

## Bibliothèques et modification

```py
import numpy as np              # Importer NumPy
import pandas as pd             # Importer Pandas
import matplotlib.pyplot as plt # Importer pyplot de Matplotlib

plt.rcParams.update({'font.size': 8})   # Changer la taille de la police sur les graphiques
```

## Fonctions

### Études des données orientées vers les températures

* diagrammeBarTemperatureMoyenneRegionPACA

```py
def diagrammeBarTemperatureMoyenneRegionPACA(tablLIEU, tablSTATION, tablRELEVE, tablMESURE):
    """
    :param tablLIEU: Tableau de la table SYSTEM_LIEU.csv
    :param tablSTATION: Tableau de la table SYSTEM_STATION.csv
    :param tablRELEVE: Tableau de la table SYSTEM_RELEVE.csv
    :param tablMESURE: Tableau de la table SYSTEM_MESURE.csv
    """
```

* diagrammeBarTemperatureMoyenneParRegion

```py
def diagrammeBarTemperatureMoyenneParRegion(tablLIEU, tablSTATION, tablRELEVE, tablMESURE):
    """
    :param tablLIEU: Tableau de la table SYSTEM_LIEU.csv
    :param tablSTATION: Tableau de la table SYSTEM_STATION.csv
    :param tablRELEVE: Tableau de la table SYSTEM_RELEVE.csv
    :param tablMESURE: Tableau de la table SYSTEM_MESURE.csv
    """
```

### Études des données orientées sur les alertes

* diagrammePieTotalAlertes

```py
def diagrammePieTotalAlertes(tablALERTE):
    """
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    """
```

*  diagrammePieLieuAvecAlerteOrange

```py
def diagrammePieLieuAvecAlerteOrange(tablALERTE, tablLIEU):
    """
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    :param tablLIEU: Tableau de la table SYSTEM_LIEU.csv
    """
```

* diagrammePieLieuAvecAlerteRouge

```py
def diagrammePieLieuAvecAlerteRouge(tablLIEU, tablALERTE):
    """
    :param tablLIEU: Tableau de la table SYSTEM_LIEU.csv
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    """
```

* diagrammePieAlerteOrange

```py
def diagrammePieAlerteOrange(tablALERTE):
    """
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    """
```

* diagrammePieAlerteRouge

```py
def diagrammePieAlerteRouge(tablALERTE):
    """
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    """
```

### Alertes en fonction des dates

* diagrammePieAlerteEnFonctionDeLaDate

```py
def diagrammePieAlerteEnFonctionDeLaDate(tablALERTE):
    """
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    """
```

* creerDictPourAlerte

```py
def creerDictPourAlerte(dictSaison, nomCatastrophe, tablSaison):
    """
    :param dictSaison: Dictionnaire attitré à la saison
    :param nomCatastrophe: Liste comportant les noms des catastrophes pour cette saison
    :param tablSaison: Tableau de la table SYSTEM_ALERTE.csv avec des dates correspondant à la saison donnée
    :return: Un dictionnaire avec comme clé le nom de la catastrophe et en valeur le nombre de fois que cette catastrophe
     a lieu pendant cette saison
    """
```

* diagrammeBarDureeMoyenneCatastrophe

```py
def diagrammeBarDureeMoyenneCatastrophe(tablALERTE):
    """
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    """
```

* tempMoyenCatastrophe

```py
def tempMoyenCatastrophe(tablALERTE, nomCatastrophe):
    """
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    :param nomCatastrophe: Liste comportant les noms des catastrophes
    :return: La durée moyenne de chaque catastrophe
    """ 
```

### Alertes en fonction des lieux

* catastropheParRegionAvecLeurDureeMoyenne

```py
def catastropheParRegionAvecLeurDureeMoyenne(tablLIEU, tablALERTE):
    """
    :param tablLIEU: Tableau de la table SYSTEM_LIEU.csv
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    """
```

* provenanceDesCatastrohes

```py
def provenanceDesCatastrohes(tablLIEU, tablALERTE):
    """
    :param tablLIEU: Tableau de la table SYSTEM_LIEU.csv
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    """
```
