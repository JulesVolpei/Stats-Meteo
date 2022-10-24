import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 8})

def main():
    tablLIEU = pd.read_csv("SYSTEM_LIEU.csv")
    tablALERTE = pd.read_csv("SYSTEM_ALERTE.csv")
    tablRELEVE = pd.read_csv("SYSTEM_RELEVE.csv")
    tablMESURE = pd.read_csv("SYSTEM_MESURE.csv")
    tablSTATION = pd.read_csv("SYSTEM_STATION.csv")


    # Études des données orientées vers les températures
    diagrammeBarTemperatureMoyenneRegionPACA(tablLIEU, tablSTATION, tablRELEVE, tablMESURE)
    diagrammeBarTemperatureMoyenneParRegion(tablLIEU, tablSTATION, tablRELEVE, tablMESURE)


    # Études des données orientées sur les alertes


    diagrammePieTotalAlertes(tablALERTE)

    diagrammePieLieuAvecAlerteOrange(tablALERTE, tablLIEU)
    diagrammePieLieuAvecAlerteRouge(tablLIEU, tablALERTE)
    diagrammePieAlerteOrange(tablALERTE)
    diagrammePieAlerteRouge(tablALERTE)

    # Alertes en fonction des dates

    diagrammePieAlerteEnFonctionDeLaDate(tablALERTE)
    diagrammeBarDureeMoyenneCatastrophe(tablALERTE)

    # Alertes en fonction des lieux

    catastropheParRegionAvecLeurDureeMoyenne(tablLIEU,  tablALERTE)
    provenanceDesCatastrohes(tablLIEU, tablALERTE)

def diagrammeBarTemperatureMoyenneParRegion(tablLIEU, tablSTATION, tablRELEVE, tablMESURE):
    """
    :param tablLIEU: Tableau de la table SYSTEM_LIEU.csv
    :param tablSTATION: Tableau de la table SYSTEM_STATION.csv
    :param tablRELEVE: Tableau de la table SYSTEM_RELEVE.csv
    :param tablMESURE: Tableau de la table SYSTEM_MESURE.csv
    """

    # Tableau avec tous les lieux avace comme IDLPERE celui de la France
    tablRegionFrance = tablLIEU.loc[tablLIEU["IDLPERE"] == 100]
    # Liste comportant le nom de chacune des régions obtenues plus haut
    listeNomRegion = [i for i in tablRegionFrance["NOML"]]
    # Liste comportant l'IDL de chacune des régions obtenues plus haut
    listeIDLRegion = [i for i in tablRegionFrance["IDL"]]


    listeDeMatricesTempératures = []
    for i in listeIDLRegion: # On commence par parcourir chaque IDL des régions
        # On prend ensuite les départements ayany comme IDLPERE celui de notre région
        tablRegionTemp = tablLIEU.loc[tablLIEU["IDLPERE"] == i]
        # On crée une liste regroupant nos nouveaux IDL (les IDL des départements)
        listeIDLTemp = [j for j in tablRegionTemp["IDL"]]

        matriceTemp = []
        for j in listeIDLTemp:  # On parcourt les IDL des départements
            # On prend ensuite une ville ayant comme IDLPERE celui de notre département (il y a une ville par département)
            tablTempVille = tablLIEU.loc[tablLIEU["IDLPERE"] == j]
            # On prend la station associée à cette ville à partir de IDL dans la table Station
            tablTempStationVille = tablSTATION.loc[tablSTATION["IDL"].isin(tablTempVille["IDL"])]
            # On y prend après le relevé lié à la station dans la table Releve
            tablTempReleveVille = tablRELEVE.loc[tablRELEVE["IDS"].isin(tablTempStationVille["IDS"])]
            # Enfin, on prend dans la table mesure les mesures associées au relevé
            tablTempMesureVille = tablMESURE.loc[tablMESURE["IDR"].isin(tablTempReleveVille["IDR"])]
            # On prend dans cette même table les températures
            tablDesTemperature = tablTempMesureVille.loc[tablTempMesureVille["NOMM"] == "Temperature"]
            # On regroupe les températures dans une liste
            listeTemperature = [k for k in tablDesTemperature["MESURE"]]
            if listeTemperature:    # Si notre liste n'est pas vide (car certaines villes n'ont pas de station)
                # On ajoute dans notre matrice la liste des températures
                matriceTemp.append(listeTemperature)
        # On ajoute après chaque tour de boucle notre matrice dans une liste de matrice
        listeDeMatricesTempératures.append(matriceTemp)

    matriceTemperatureMoyenne = []  #On va créer une matrice comportant une liste avec la moyenne de chaque température
    # Chaque indice de la matrice correspond à la région attribuée de la liste listeNomRegion
    for i in range(len(listeDeMatricesTempératures)):
        nouvelleListeTemperature = []
        for j in range(len(listeDeMatricesTempératures[i])):
            # On ajoute dans une liste la moyenne des températures de notre matrice
            nouvelleListeTemperature.append(np.mean(listeDeMatricesTempératures[i][j]))
        matriceTemperatureMoyenne.append(nouvelleListeTemperature)  # On ajoute notre liste dans une nouvelle matrice

    # On obtient une matrice avec dedans la moyenne des températures des villes d'une région associée
    listeFinale = []
    for i in matriceTemperatureMoyenne: # On parcourt notre nouvelle matrice
        # On ajoute dans une liste la moyenne des éléments de chaque liste de la matrice
        listeFinale.append(np.mean(i))
    listeFinale[9] = 0  # L'indice 0 correspond à la Bourgogne qui n'a pas de station, on lui attribue 0 pour éviter les erreurs
    listeNomRegion[0] = "PACA"  # On réduit le nom de la région par manque de lisibilité
    plt.close()
    plt.title('Moyenne des températures de chaque région pour les deux solstices')
    plt.text(-2, np.max(listeFinale) / 2, 'Degré celsius', rotation=90)
    # On fait correspondre l'indice d'une température moyenne avec sa région associée
    plt.bar(listeNomRegion, listeFinale, color='pink', align='center', width=0.8)
    plt.show()



def diagrammeBarTemperatureMoyenneRegionPACA(tablLIEU, tablSTATION, tablRELEVE, tablMESURE):
    """
    :param tablLIEU: Tableau de la table SYSTEM_LIEU.csv
    :param tablSTATION: Tableau de la table SYSTEM_STATION.csv
    :param tablRELEVE: Tableau de la table SYSTEM_RELEVE.csv
    :param tablMESURE: Tableau de la table SYSTEM_MESURE.csv
    """
    tablRegionPACA = tablLIEU.loc[tablLIEU["IDLPERE"] == 101]   # On prend l'IDL de la région PACA
    listeIDLPEREPACA = []
    for i in tablRegionPACA["IDL"]:
        listeIDLPEREPACA.append(i)
    # On prend ensuite toutes les départements de la région PACA
    matriceTemperatureVille = []
    listeNomVille = []
    for i in listeIDLPEREPACA:
        tablTempVille = tablLIEU.loc[tablLIEU["IDLPERE"] == i]
        listeNomVille.append([i for i in tablTempVille["NOML"]])    # Seul manière que j'ai trouvé pour avoir les noms des villes (indice [i][0] --> nom ville)
        tablTempStationVille = tablSTATION.loc[tablSTATION["IDL"].isin(tablTempVille["IDL"])]
        tablTempReleveVille = tablRELEVE.loc[tablRELEVE["IDS"].isin(tablTempStationVille["IDS"])]
        tablTempMesureVille = tablMESURE.loc[tablMESURE["IDR"].isin(tablTempReleveVille["IDR"])]
        tablDesTemperature = tablTempMesureVille.loc[tablTempMesureVille["NOMM"] == "Temperature"]
        matriceTemperatureVille.append([i for i in tablDesTemperature["MESURE"]])
    # Calcul moyenne des températures des villes
    listeMoyenneTemperatureVille = []
    for i in matriceTemperatureVille:
        listeMoyenneTemperatureVille.append(np.mean(i))
    vraiNomVille = []   # Pour n'avoir que les noms de villes, pas la liste
    for i in listeNomVille:
        vraiNomVille.append(i[0])
    plt.close()
    plt.title('Moyenne des températures des villes de la région PACA')
    plt.text(-1.25, np.max(listeMoyenneTemperatureVille) / 2, 'Degré celsius', rotation=90)
    plt.bar(vraiNomVille, listeMoyenneTemperatureVille, align='center', color='pink')
    plt.show()





def diagrammePieTotalAlertes(tablALERTE):
    """
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    """
    # On prend une table avec uniquement les alertes orange
    tablAlerteOrange = tablALERTE.loc[tablALERTE["NIVEAU"] == "orange"]
    # On prend une table avec uniquement les alertes rouges
    tablAlerteRouge = tablALERTE.loc[tablALERTE["NIVEAU"] == "rouge"]

    plt.close()
    plt.title('Diagramme des différents types d\'alertes ')
    # On compare ensuite le nombre d'alertes orange et le nombre d'alertes rouge
    plt.pie([len([i for i in tablAlerteRouge["IDA"]]), len([i for i in tablAlerteOrange["IDA"]])],
            labels=['Rouge', 'Orange'],
            colors=['red', 'orange'],
            autopct= lambda z : str(round(z, 2)) + "%",
            explode=[0, 0.3])
    plt.show()

def diagrammePieLieuAvecAlerteOrange(tablALERTE, tablLIEU):
    """
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    :param tablLIEU: Tableau de la table SYSTEM_LIEU.csv
    """
    # On prend un tableau avec les alertes de niveaux orange
    tablAlerteOrange = tablALERTE.loc[tablALERTE["NIVEAU"] == "orange"]
    # On prend les lieux ayant au moins une alerte orange recensée
    tablLieuAvecAlerteOrange = tablLIEU.loc[tablLIEU["IDL"].isin(tablAlerteOrange["IDL"])]

    dictLieuAvecAlerteOrange = {}
    # On crée une liste avec tous les IDL des lieux avec une ou plusieurs alerte orange
    listeIDL = [i for i in tablLieuAvecAlerteOrange["IDL"]]
    for i in listeIDL:  # On parcourt cette liste
        # On y associe dans un dictionnaire l'IDL du lieu avec son nombre d'alertes (pour l'instant initialisé à 0)
        dictLieuAvecAlerteOrange[i] = 0

    for i in [j for j in tablAlerteOrange["IDL"]]:
        if i in listeIDL:
            # On compte le nombre de fois que notre IDL est dans la liste
            dictLieuAvecAlerteOrange[i] += 1

    # On crée une matrice avec les IDL correspondant aux noms
    matriceTest = [[i for i in tablLieuAvecAlerteOrange["IDL"]], [i for i in tablLieuAvecAlerteOrange["NOML"]]]
    dictNomLieuAlertesOrange = {}

    for i in range(len(matriceTest[0])):    # On parcourt les IDL
        for key in dictLieuAvecAlerteOrange.keys():
            # Si une des clés du dictionnaire correspond à un IDL dans la liste
            if key == matriceTest[0][i]:
                # On crée une variable valeur qui a prendre le nombre de catastrophe de cet IDL
                valeur = dictLieuAvecAlerteOrange[key]
        # On fait ensuite correspondre dans un dictionnaire le nom du lieu avec le nombre de catastrophe
        dictNomLieuAlertesOrange[matriceTest[1][i]] = valeur

    listeExplode = []
    for i in range(len([j for j in dictNomLieuAlertesOrange.keys()])):
        # Par lisibilié, on va faire en sorte de légèrement faire ressortir chaque part du diagramme
        listeExplode.append(i / len([k for k in dictNomLieuAlertesOrange.keys()]))
    plt.close()
    plt.pie([i for i in dictNomLieuAlertesOrange.values()],
            labels=[i for i in dictNomLieuAlertesOrange.keys()],
            autopct=lambda z : str(round(z, 2)) + "%",
            pctdistance=0.8,
            explode=listeExplode)
    plt.show()

def diagrammePieLieuAvecAlerteRouge(tablLIEU, tablALERTE):
    """
    :param tablLIEU: Tableau de la table SYSTEM_LIEU.csv
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    """
    # On prend dans notre table les alertes rouge
    tablAlerteRouge = tablALERTE.loc[tablALERTE["NIVEAU"] == "rouge"]
    # On prend dans notre table les lieux avec les alertes rouge
    tablLieuAvecAlerteRouge = tablLIEU.loc[tablLIEU["IDL"].isin(tablAlerteRouge["IDL"])]

    dictLieuAvecAlerteRouge = {}
    # On crée ensuite une listea avec les IDL des lieux avec au moins une alerte rouge
    listeIDL = [i for i in tablLieuAvecAlerteRouge["IDL"]]
    for i in listeIDL:
        # On parcourt cette liste pour créer le dictionnaire associé
        dictLieuAvecAlerteRouge[i] = 0

    for i in [j for j in tablAlerteRouge["IDL"]]:
        if i in listeIDL:
            # On compte le nombre de fois que notre IDL est dans la liste
            dictLieuAvecAlerteRouge[i] += 1

    # On crée une matrice avec les IDL correspondant aux noms
    matriceTest = [[i for i in tablLieuAvecAlerteRouge["IDL"]], [i for i in tablLieuAvecAlerteRouge["NOML"]]]

    dictTest = {}

    for i in range(len(matriceTest[0])):
        for key in dictLieuAvecAlerteRouge.keys():
            # Si une des clés du dictionnaire correspond à un IDL dans la liste
            if key == matriceTest[0][i]:
                # On crée une variable valeur qui a prendre le nombre de catastrophe de cet IDL
                valeur = dictLieuAvecAlerteRouge[key]
        # On fait ensuite correspondre dans un dictionnaire le nom du lieu avec le nombre de catastrophe
        dictTest[matriceTest[1][i]] = valeur

    plt.close()
    plt.title('Provenance des alertes rouges')
    plt.pie([i for i in dictTest.values()],
            labels=[i for i in dictTest.keys()],
            autopct=lambda z: str(round(z, 2)) + "%",
            pctdistance=0.8,)
    plt.show()


def diagrammePieAlerteOrange(tablALERTE):
    """
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    """
    # On prend dans la table les alertes orange
    tablAlerteOrange = tablALERTE.loc[tablALERTE["NIVEAU"] == "orange"]
    # On parcourt les noms des alertes que l'on prend une seule fois avec la fonction np.unique()
    nomCatastrophe = np.unique([i for i in tablAlerteOrange["CATEGORIE"]])

    dictAlerteOrange = {}
    for i in nomCatastrophe:
        # On initialise chaque nom de catastrophe à 0 dans un dictionnaire
        dictAlerteOrange[i] = 0
    for i in tablAlerteOrange["CATEGORIE"]:
        # On compte le nombre de fois qu'une cataqtrophe est présent dans les alertes oranges
        dictAlerteOrange[i] += 1
    plt.close()
    plt.title('Pourcentage du type d\'alertes oranges')
    plt.pie([i for i in dictAlerteOrange.values()],
            labels=nomCatastrophe,
            autopct='%1.1f%%')
    plt.show()

def diagrammePieAlerteRouge(tablALERTE):
    """
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    """
    # On prend dans la table les alertes rouge
    tablAlerteRouge = tablALERTE.loc[tablALERTE["NIVEAU"] == "rouge"]
    # On parcourt les noms des alertes que l'on prend une seule fois avec la fonction np.unique()
    nomCatastrophe = np.unique([i for i in tablAlerteRouge["CATEGORIE"]])

    dictAlerteRouge = {}
    for i in nomCatastrophe:
        # On initialise chaque nom de catastrophe à 0 dans un dictionnaire
        dictAlerteRouge[i] = 0
    for i in tablAlerteRouge["CATEGORIE"]:
        # On compte le nombre de fois qu'une cataqtrophe est présent dans les alertes rouge
        dictAlerteRouge[i] += 1
    plt.close()
    plt.title('Pourcentage du type d\'alertes rouges')
    plt.pie([i for i in dictAlerteRouge.values()],
            labels=nomCatastrophe,
            autopct='%1.1f%%')
    plt.show()

def diagrammePieAlerteEnFonctionDeLaDate(tablALERTE):
    """
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    """
    # On crée une table à partir des dates délimitant les quatre saisons
    # Hiver
    tablDateHiver = tablALERTE.loc[((tablALERTE["DATEDEB"] >= "2021-12-21") & (tablALERTE["DATEDEB"] <= "2021-12-31")) | ((tablALERTE["DATEDEB"] >= "2021-01-01") & (tablALERTE["DATEDEB"] <= "2021-03-22"))]
    # Été
    tablDateEte = tablALERTE.loc[(tablALERTE["DATEDEB"] >= "2021-06-21") & (tablALERTE["DATEDEB"] <= "2021-09-23")]
    # Automne
    tablDateAutomne = tablALERTE.loc[(tablALERTE["DATEDEB"] >= "2021-09-23") & (tablALERTE["DATEDEB"] <= "2021-12-21")]
    # Printemps
    tablDatePrintemps = tablALERTE.loc[(tablALERTE["DATEDEB"] >= "2021-03-22") & (tablALERTE["DATEDEB"] <= "2021-06-21")]

    # On prend ensuite chacune des catastrophes présentent dans nos quatre tables que l'on stocke dans des listes
    # Hiver
    nomCatastropheHiver = np.unique([i for i in tablDateHiver["CATEGORIE"]])
    # Été
    nomCatastropheEte = np.unique([i for i in tablDateEte["CATEGORIE"]])
    # Printemps
    nomCatastrophePrintemps = np.unique([i for i in tablDatePrintemps["CATEGORIE"]])
    # Automne
    nomCatastropheAutomne = np.unique([i for i in tablDateAutomne["CATEGORIE"]])

    # On crée des dictionnaires dans lesquels la clé va correspondre à la catastrophe et la valeur au nombre de fois que
    # celle-ci est présente dans la table
    dictHiver = {}
    dictEte = {}
    dictAutomne = {}
    dictPrintemps = {}

    # On remplit les dictionnaires à l'aide d'une fonction crée
    dictEte = creerDictPourAlerte(dictEte, nomCatastropheEte, tablDateEte)
    dictHiver = creerDictPourAlerte(dictHiver, nomCatastropheHiver, tablDateHiver)
    dictAutomne = creerDictPourAlerte(dictAutomne, nomCatastropheAutomne, tablDateAutomne)
    dictPrintemps = creerDictPourAlerte(dictPrintemps, nomCatastrophePrintemps, tablDatePrintemps)

    plt.close()
    plt.title('Catastrophes en été')
    plt.pie([i for i in dictEte.values()],
            labels=nomCatastropheEte,
            autopct='%1.1f%%')
    plt.show()
    plt.close()
    plt.title('Catastrophes en automne')
    plt.pie([i for i in dictAutomne.values()],
            labels=nomCatastropheAutomne,
            autopct='%1.1f%%')
    plt.show()
    plt.close()
    plt.title('Catastrophes en hiver')
    plt.pie([i for i in dictHiver.values()],
            labels=nomCatastropheHiver,
            autopct='%1.1f%%')
    plt.show()
    plt.close()
    plt.title('Catastrophes au printemps')
    plt.pie([i for i in dictPrintemps.values()],
            labels=nomCatastrophePrintemps,
            autopct='%1.1f%%')
    plt.show()
    plt.close()

def creerDictPourAlerte(dictSaison, nomCatastrophe, tablSaison):
    """
    :param dictSaison: Dictionnaire attitré à la saison
    :param nomCatastrophe: Liste comportant les noms des catastrophes pour cette saison
    :param tablSaison: Tableau de la table SYSTEM_ALERTE.csv avec des dates correspondant à la saison donnée
    :return: Un dictionnaire avec comme clé le nom de la catastrophe et en valeur le nombre de fois que cette catastrophe
     a lieu pendant cette saison
    """
    for i in nomCatastrophe:    # On parcourt la liste des noms des catastrophes
        # On initialise chaque catastrophe avec une valeur de 0
        dictSaison[i] = 0
    for i in tablSaison["CATEGORIE"]:   # On parcourt les différentes alertes de la saison
        # On incrémente la valeur à chaque fois que l'on rencontre la catastrophe dans la table
        dictSaison[i] += 1
    return dictSaison


def tempMoyenCatastrophe(tablALERTE, nomCatastrophe):
    """
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    :param nomCatastrophe: Liste comportant les noms des catastrophes
    :return: La durée moyenne de chaque catastrophe
    """
    # On prend une table comportant toutes les alertes d'une catastrophe en particulier
    tablCatastrophe = tablALERTE.loc[tablALERTE["CATEGORIE"] == nomCatastrophe]

    # On stocke les date de début dans une liste
    dateDebCatastrophe = [i for i in tablCatastrophe["DATEDEB"]]
    # On stocke les date de fin dans une liste
    dateFinCatastrophe = [i for i in tablCatastrophe["DATEFIN"]]

    jourDebCatastrophe = []
    jourFinCatastrophe = []
    # On va ensuite stocker les jours de fin et de début de chaque catastrophe
    for i in range(len(dateDebCatastrophe)):
        jourDebCatastrophe.append(int(dateDebCatastrophe[i][8:]))
        jourFinCatastrophe.append(int(dateFinCatastrophe[i][8:]))
    listeDuree = []

    # On crée un dictionnaire avec en clé un mois et en valeur un entier correspondant à son dernier jour
    dictFinMois = {'01': 31, '02': 28, '03': 31, '04': 30, '05': 31, '06': 30, '07': 31, '08': 31, '09': 30, '10': 31, '11': 30, '12': 31}
    for i in range(len(jourDebCatastrophe)):
        # On initialise un compteur pour pouvoir compter les jours
        cmpt = 0
        while jourDebCatastrophe[i] != jourFinCatastrophe[i]:   # Tant que notre jour de début n'est pas celui de fin
            # Si le jour de début n'est pas le jour de la fin du mois
            if not jourDebCatastrophe[i] == dictFinMois[dateDebCatastrophe[i][5:7]]:
                # On incrémente les deux variables
                jourDebCatastrophe[i] += 1
                cmpt += 1
            else:   # Sinon
                # On initialise le jour de début à 1 pour correspondre au début du mois
                jourDebCatastrophe[i] = 1
                # On incrémente toujours le compteur
                cmpt += 1
        # On ajoute le compteur dans une liste crée au préalable
        listeDuree.append(cmpt)
    return np.mean(listeDuree)  # On renvoie la moyenne des valeurs de cette liste

def diagrammeBarDureeMoyenneCatastrophe(tablALERTE):
    """
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    """
    # On crée une liste avec toutes les catastrophes
    listeCatastrophe = np.unique([i for i in tablALERTE["CATEGORIE"]])
    dictCatastropheDureeMoyenne = {}
    for i in listeCatastrophe:  # On parcourt notre liste
        # Pour chaque catastrophe, on y associe son temps moyen
        dictCatastropheDureeMoyenne[i] = tempMoyenCatastrophe(tablALERTE, i)
    plt.close()
    plt.title('Durée moyenne de chaque catastrophe')
    plt.text(-1.5, np.max([i for i in dictCatastropheDureeMoyenne.values()]) / 2, 'Durée en jour', rotation=90)
    plt.bar([i for i in dictCatastropheDureeMoyenne.keys()], [i for i in dictCatastropheDureeMoyenne.values()], color='pink')
    plt.show()

def catastropheParRegionAvecLeurDureeMoyenne(tablLIEU, tablALERTE):
    """
    :param tablLIEU: Tableau de la table SYSTEM_LIEU.csv
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    """

    listeDepartementParRegion = []
    listeNomDepartementParRegion = []
    listeTotaleDepartement = [i for i in tablLIEU["IDL"].loc[tablLIEU["IDLPERE"] == 100]]   # IDL des régions
    listeTotaleNomRegion = [i for i in tablLIEU["NOML"].loc[tablLIEU["IDLPERE"] == 100]]    # Nom des régions

    for i in range(len(listeTotaleDepartement)):
        # On ajoute dans chacune des listes l'IDL et le NOML associée à un département
        listeDepartementParRegion.append([j for j in tablLIEU["IDL"].loc[tablLIEU["IDLPERE"] == listeTotaleDepartement[i]]])
        listeNomDepartementParRegion.append([j for j in tablLIEU["NOML"].loc[tablLIEU["IDLPERE"] == listeTotaleDepartement[i]]])

    for i in range(len(listeDepartementParRegion)):     # On parcourt la liste des IDL de départements
        # On initialise un dictionnaire pour chacune des régions
        dictCatastropheRegion = {}
        for j in np.unique([k for k in tablALERTE["CATEGORIE"]]):   # On parcourt l'ensemble des catastrophes
            # On initialise toutes les catastrophes à 0
            dictCatastropheRegion[j] = 0
        for j in range(len(listeDepartementParRegion[i])):      # On parcourt un IDL de département
            # On associe dans une liste les différentes IDA des catastrophes
            listeCatastrophe = [k for k in tablALERTE["IDA"].loc[tablALERTE["IDL"] == listeDepartementParRegion[i][j]]]
            if listeCatastrophe:    # Si il y a des catastrophes
                # On stocke ces catastrophes dans un tableau
                tablCatastrophe = tablALERTE.loc[tablALERTE["IDL"] == listeDepartementParRegion[i][j]]
                for k in tablCatastrophe["CATEGORIE"]:  # On parcourt les catastrophes de ce nouveau tableau
                    # On incrémente notre dictionnaire à la catastrophe correspondante
                    dictCatastropheRegion[k] += 1
        # On crée le titre du diagramme en fonction de la région étudiée
        titre = "Catastrophes enregistrées dans la région " + listeTotaleNomRegion[i]
        plt.close()
        plt.title(titre)
        plt.text(-1.5, np.max([j for j in dictCatastropheRegion.values()]) / 2, 'Nombre de catastrophes', rotation=90)
        plt.bar([j for j in dictCatastropheRegion.keys()], [j for j in dictCatastropheRegion.values()], color='pink')
        plt.show()

def provenanceDesCatastrohes(tablLIEU, tablALERTE):
    """
    :param tablLIEU: Tableau de la table SYSTEM_LIEU.csv
    :param tablALERTE: Tableau de la table SYSTEM_ALERTE.csv
    """
    # On liste chaque nom de catastrophe dans une liste
    nomCatastrophe = np.unique([i for i in tablALERTE["CATEGORIE"]])
    for i in nomCatastrophe:    # On parcourt cette liste
        dictCatastrophe = {}    # On initialise un dictionnaire
        # On crée une table comportant toutes les alertes d'une certaine catastrophe
        tablCatastrophe = tablALERTE.loc[tablALERTE["CATEGORIE"] == i]
        # On prend ensuite les IDL de ces alertes pour en retrouver les lieux
        tablLieuAvecCatastrophe = tablLIEU.loc[tablLIEU["IDL"].isin(tablCatastrophe["IDL"])]
        # On stocke ensuite dans une liste les IDL de ces lieux
        IDLDepartementCatastrophe = [j for j in tablCatastrophe["IDL"]]
        for j in IDLDepartementCatastrophe:     # On parcourt cette nouvelle liste
            # On initialise chaque IDL à 0 dans le dictionnaire
            dictCatastrophe[j] = 0

        for j in tablCatastrophe["IDL"]:    # On parcourt les IDL de la table d'alerte pour une certaine catastrophe
            # On incrémente la valeur pour chaque IDL rencontré
            dictCatastrophe[j] += 1
        # On crée le titre du diagramme en fonction de la catastrophe
        titre = "Proportion de département ayant la catastrophe : " + i
        plt.close()
        plt.title(titre)
        plt.pie([j for j in dictCatastrophe.values()],
                labels=[j for j in tablLieuAvecCatastrophe["NOML"]],
                autopct='%1.1f%%')
        plt.show()

if __name__ == "__main__":
    main()

