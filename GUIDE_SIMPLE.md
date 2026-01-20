# 📊 Guide Simple du Projet BigData

## 🎯 C'est Quoi Ce Projet ?

Imagine que tu as un magasin en ligne. Tu as plein de clients qui achètent des produits. Ce projet transforme toutes ces informations en graphiques et statistiques faciles à comprendre !

## 🏪 L'Histoire en Simple

### 1. Les Données de Départ
Tu as deux fichiers Excel (en fait des CSV) :
- **clients.csv** : 1500 clients avec leur nom, email, pays
- **achats.csv** : 23,663 achats avec ce qu'ils ont acheté et combien ça coûte

### 2. Le Voyage des Données

#### Étape 1 : La Boîte Bronze 🥉
- On prend les fichiers Excel
- On les met dans une première boîte (MinIO) sans rien changer
- C'est comme faire une photocopie de tes factures

#### Étape 2 : La Boîte Silver 🥈
- On nettoie tout ça :
  - On enlève les doublons (si Marc apparaît 2 fois, on garde qu'un seul)
  - On corrige les erreurs (les dates bizarres, les prix négatifs)
  - On ajoute des infos utiles (l'année, le mois de l'achat)
- On range tout proprement

#### Étape 3 : La Boîte Gold 🥇
- On fait des calculs intelligents :
  - Quel client a dépensé le plus ?
  - Quel produit se vend le mieux ?
  - Quel mois on a fait le plus de ventes ?
  - Dans quel pays on vend le plus ?
- On crée 4 tableaux de résumés

#### Étape 4 : MongoDB 🗄️
- On met tous ces résumés dans une base de données spéciale
- C'est comme un classeur ultra rapide
- On peut chercher n'importe quelle info en une fraction de seconde

#### Étape 5 : L'API 🔌
- C'est comme un serveur au restaurant
- Tu lui demandes une info, il va la chercher et te la ramène
- Exemple : "Donne-moi les 10 meilleurs clients"

#### Étape 6 : Le Dashboard 📱
- C'est l'écran que tu vois
- Plein de graphiques colorés
- Tu peux cliquer partout pour explorer

## 🎮 Les 6 Pages du Dashboard

### Page 1 : 🏠 Accueil
**C'est quoi ?** La vue d'ensemble de ton magasin

**Ce que tu vois :**
- Combien de clients tu as
- Combien d'argent tu as gagné au total
- Combien de commandes ont été passées
- En moyenne, combien chaque client dépense

**Pourquoi c'est utile ?** D'un seul coup d'œil, tu sais si ton magasin marche bien !

### Page 2 : 👥 Clients
**C'est quoi ?** Tout sur tes clients

**Ce que tu vois :**
- Un graphique avec les clients qui dépensent le plus
- Les couleurs montrent de quel pays ils viennent
- Un camembert qui montre la répartition par pays
- Un grand tableau avec tous les détails

**Tu peux :**
- Choisir combien de clients voir (10, 50, 100...)
- Filtrer par pays (voir seulement les Français, par exemple)

**Pourquoi c'est utile ?** Pour savoir qui sont tes meilleurs clients et leur faire des offres spéciales !

### Page 3 : 📦 Produits
**C'est quoi ?** Les statistiques de vente de chaque produit

**Ce que tu vois :**
- Quel produit rapporte le plus d'argent
- Quel produit se vend le plus souvent
- Les prix min, max et moyen de chaque produit

**Pourquoi c'est utile ?** Pour savoir sur quels produits concentrer tes efforts de marketing !

### Page 4 : 📅 Tendances
**C'est quoi ?** L'évolution de tes ventes dans le temps

**Ce que tu vois :**
- Une courbe qui monte et descend chaque mois (ton chiffre d'affaires)
- Le nombre d'achats par mois
- Le panier moyen (combien les gens dépensent en moyenne)

**Pourquoi c'est utile ?** Pour voir si tes ventes augmentent ou diminuent, et prévoir l'avenir !

### Page 5 : 🌍 Pays
**C'est quoi ?** Où se trouvent tes clients et combien ils dépensent

**Ce que tu vois :**
- Un graphique par pays avec le chiffre d'affaires
- Un camembert avec le nombre de clients par pays
- Le panier moyen de chaque pays

**Pourquoi c'est utile ?** Pour savoir dans quels pays investir en publicité !

### Page 6 : ⚡ Performances
**C'est quoi ?** La vitesse du système

**Ce que tu vois :**
- Combien de temps prend chaque demande (en millisecondes)
- Un graphique qui compare les vitesses

**Pourquoi c'est utile ?** Pour vérifier que tout marche super vite !

## 🎨 Comment Ça Marche Techniquement (En Simple)

### Les Outils Utilisés

**MinIO** 📦
- C'est comme un disque dur géant dans le cloud
- Il stocke tous tes fichiers de données
- Organisé en 4 boîtes : sources, bronze, silver, gold

**MongoDB** 🗄️
- C'est une base de données rapide
- Elle range les infos comme dans des tiroirs
- Tu peux chercher n'importe quoi très vite

**FastAPI** 🚀
- C'est le serveur qui répond à tes questions
- Tu lui demandes "Donne-moi les clients français"
- Il va chercher et te répond en quelques millisecondes

**Streamlit** 🎨
- C'est ce qui crée les beaux graphiques que tu vois
- Il prend les données et les transforme en images colorées
- Facile à utiliser, tu cliques et ça marche !

**Prefect** 🤖
- C'est le chef d'orchestre
- Il lance tous les traitements dans le bon ordre
- Il vérifie que tout se passe bien

## 📊 Les Chiffres du Projet

- **1500 clients** dans la base
- **23,663 achats** enregistrés
- **10 produits** différents
- **9 pays** représentés
- **13 mois** de données
- **Temps de chargement** : Moins d'une seconde !

## 🎯 Les 4 Questions Principales Auxquelles Ce Projet Répond

### 1. "Qui sont mes meilleurs clients ?"
→ Page Clients : Tu vois le Top 10 qui dépensent le plus

### 2. "Quel produit marche le mieux ?"
→ Page Produits : Graphique qui montre le chiffre d'affaires par produit

### 3. "Mes ventes augmentent ou diminuent ?"
→ Page Tendances : Courbe qui monte/descend chaque mois

### 4. "Dans quel pays je devrais investir ?"
→ Page Pays : Graphique avec le CA par pays

## 💡 Cas d'Usage Concrets

### Exemple 1 : Préparer une Promo
1. Va sur la page Produits
2. Regarde quel produit se vend mal
3. Décide de faire -30% dessus
4. Résultat : Tu écoules ton stock !

### Exemple 2 : Fidéliser les Meilleurs Clients
1. Va sur la page Clients
2. Clique sur "Top clients"
3. Note les 10 premiers
4. Envoie-leur un code promo exclusif
5. Résultat : Ils restent fidèles !

### Exemple 3 : Expansion Internationale
1. Va sur la page Pays
2. Regarde quel pays a le panier moyen le plus élevé
3. Décide d'investir en pub dans ce pays
4. Résultat : Tes ventes explosent là-bas !

### Exemple 4 : Prévoir les Stocks
1. Va sur la page Tendances
2. Regarde les mois où tu vends le plus
3. Commande plus de stock avant ces mois
4. Résultat : Jamais en rupture !

## ⚡ Pourquoi C'est Rapide ?

### Architecture Intelligente
- **Parquet** : Format de fichier super compressé et rapide à lire
- **MongoDB** : Base de données NoSQL ultra-rapide pour les lectures
- **API** : Serveur optimisé qui garde les connexions ouvertes
- **Cache** : Les données souvent demandées restent en mémoire

### Les Temps Mesurés
- Charger 1500 clients : **~30 millisecondes**
- Charger les stats produits : **~10 millisecondes**
- Charger les stats pays : **~10 millisecondes**
- Résumé complet : **~50 millisecondes**

C'est **plus rapide qu'un clignement d'œil** (300 millisecondes) !

## 🔄 Comment Mettre À Jour les Données ?

### Étape par étape :

1. **Ajoute de nouvelles données** dans les fichiers CSV
2. **Lance le flow Bronze** :
   ```bash
   python flows/bronze_ingestion.py
   ```
3. **Lance le flow Silver** :
   ```bash
   python flows/silver_transformation.py
   ```
4. **Lance le flow Gold** :
   ```bash
   python flows/gold_aggregation.py
   ```
5. **Lance le flow MongoDB** :
   ```bash
   python flows/mongodb_ingestion.py
   ```
6. **Rafraîchis le dashboard** : Il se met à jour automatiquement !

**Temps total** : Environ 5 secondes pour tout mettre à jour !

## 🎓 Ce Que Tu Apprends Avec Ce Projet

### Concepts BigData
1. **Data Lake** : Stocker les données brutes avant de les traiter
2. **Architecture Medallion** : Bronze → Silver → Gold
3. **ETL/ELT** : Extract, Transform, Load (Extraire, Transformer, Charger)
4. **NoSQL** : Base de données flexible et rapide
5. **API REST** : Serveur qui répond à des requêtes
6. **Orchestration** : Automatiser les tâches
7. **Visualisation** : Transformer les chiffres en graphiques

### Compétences Techniques
- Python (langage de programmation)
- Pandas (manipulation de données)
- FastAPI (création d'API)
- Streamlit (dashboards)
- MongoDB (base NoSQL)
- Docker (conteneurs)
- Prefect (orchestration)

## 🚀 Pour Aller Plus Loin

### Améliorations Possibles
1. **Alertes** : Recevoir un email si les ventes baissent
2. **Prédictions** : Utiliser le machine learning pour prévoir les ventes futures
3. **Temps réel** : Mettre à jour les stats toutes les 5 minutes
4. **Plus de graphiques** : Ajouter des cartes géographiques
5. **Export PDF** : Générer des rapports automatiquement

## 📞 Besoin d'Aide ?

### Problème : Le dashboard ne s'affiche pas
**Solution** : Vérifie que l'API tourne avec `curl http://localhost:8000/health`

### Problème : Données vides
**Solution** : Lance d'abord tous les flows dans l'ordre

### Problème : Erreur MongoDB
**Solution** : Vérifie que Docker tourne avec `docker ps`

## 🎉 Conclusion

Ce projet transforme des fichiers Excel ennuyeux en un **dashboard interactif magnifique** qui t'aide à prendre de **meilleures décisions** pour ton business !

En quelques clics, tu peux :
- ✅ Voir qui sont tes meilleurs clients
- ✅ Savoir quels produits marchent
- ✅ Suivre l'évolution de tes ventes
- ✅ Identifier les pays les plus rentables
- ✅ Prendre des décisions basées sur des données réelles

**Tout ça en moins d'une seconde !** 🚀
