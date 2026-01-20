# 🚀 Guide d'Accès au Projet BigData

## ✅ Projet Lancé !

Tous les services sont maintenant actifs. Voici où accéder à chaque partie du projet et à quoi ça sert.

---

## 🌐 Les 5 Interfaces Web Disponibles

### 1. 📊 **Dashboard Streamlit** - LE PRINCIPAL !
**URL :** http://localhost:8501

**C'est quoi ?**
C'est **TON ÉCRAN PRINCIPAL** - l'interface graphique pour visualiser toutes tes données !

**À quoi ça sert ?**
- 📈 Voir des **graphiques colorés** de tes ventes
- 👥 Explorer tes **meilleurs clients**
- 📦 Analyser tes **produits qui marchent**
- 🌍 Comparer les **performances par pays**
- 📅 Suivre l'**évolution mensuelle** de ton business

**Les 6 pages disponibles :**
1. **🏠 Accueil** : Vue d'ensemble avec chiffres clés
2. **👥 Clients** : Top clients, filtres par pays
3. **📦 Produits** : Ventes et CA par produit
4. **📅 Tendances** : Courbes d'évolution dans le temps
5. **🌍 Pays** : Statistiques géographiques
6. **⚡ Performances** : Vitesse de l'API

**Comment l'utiliser ?**
1. Ouvre http://localhost:8501 dans ton navigateur
2. Clique sur les onglets dans la barre latérale
3. Utilise les filtres (choix du pays, nombre de clients, etc.)
4. Explore les graphiques interactifs (tu peux zoomer, survoler)

---

### 2. 🔌 **API Documentation** - Pour les Développeurs
**URL :** http://localhost:8000/docs

**C'est quoi ?**
Une interface pour **tester l'API** directement dans le navigateur.

**À quoi ça sert ?**
- Tester les **requêtes API** sans coder
- Voir tous les **endpoints disponibles**
- Comprendre quelles **données tu peux récupérer**
- Tester différents **filtres et paramètres**

**Exemples de requêtes que tu peux faire :**
- `GET /clients` : Récupérer la liste des clients
- `GET /products` : Obtenir les stats produits
- `GET /stats/summary` : Avoir un résumé complet
- `GET /top-clients` : Les meilleurs clients

**Comment l'utiliser ?**
1. Ouvre http://localhost:8000/docs
2. Clique sur un endpoint (par exemple "GET /clients")
3. Clique sur "Try it out"
4. Clique sur "Execute"
5. Vois le résultat JSON apparaître

---

### 3. 🗄️ **Mongo Express** - Base de Données MongoDB
**URL :** http://localhost:8081

**C'est quoi ?**
Une interface web pour **voir directement dans MongoDB** (ta base de données NoSQL).

**À quoi ça sert ?**
- Voir les **4 collections** de données
- Explorer les **documents** (comme des lignes dans Excel)
- Vérifier que les **données sont bien stockées**
- Faire des **requêtes directes** sur la base

**Les 4 collections que tu verras :**
1. **clients_stats** : 1500 clients avec leurs statistiques
2. **product_stats** : 10 produits avec leurs ventes
3. **monthly_stats** : 13 mois de statistiques
4. **country_stats** : 9 pays avec leurs performances

**Comment l'utiliser ?**
1. Ouvre http://localhost:8081
2. Clique sur "bigdata" (le nom de la base)
3. Clique sur une collection (par exemple "clients_stats")
4. Tu vois tous les documents stockés

---

### 4. 📦 **MinIO Console** - Data Lake
**URL :** http://localhost:9001
**Identifiants :** minioadmin / minioadmin

**C'est quoi ?**
C'est ton **entrepôt de données** - comme un Google Drive pour tes fichiers de données.

**À quoi ça sert ?**
- Voir les **4 boîtes** de données (sources, bronze, silver, gold)
- Télécharger les **fichiers Parquet**
- Vérifier la **taille des fichiers**
- Naviguer dans ton **data lake**

**Les 4 buckets (boîtes) :**
1. **sources** : Fichiers CSV originaux (clients.csv, achats.csv)
2. **bronze** : Copies brutes (2 fichiers CSV)
3. **silver** : Données nettoyées (2 fichiers Parquet)
4. **gold** : Agrégations (4 fichiers Parquet)

**Comment l'utiliser ?**
1. Ouvre http://localhost:9001
2. Login : `minioadmin` / `minioadmin`
3. Clique sur "Buckets" dans le menu
4. Explore les 4 buckets
5. Tu peux télécharger les fichiers si besoin

---

### 5. 🤖 **Prefect Server** - Orchestration
**URL :** http://localhost:4200

**C'est quoi ?**
L'interface pour voir l'**historique des traitements** (flows).

**À quoi ça sert ?**
- Voir les **4 flows** qui ont été exécutés
- Consulter les **logs** de chaque étape
- Vérifier que **tout s'est bien passé**
- Voir les **temps d'exécution**

**Les 4 flows que tu verras :**
1. **Bronze Ingestion** : Upload des CSV
2. **Silver Transformation** : Nettoyage
3. **Gold Aggregation** : Calculs
4. **MongoDB Ingestion** : Stockage en base

**Comment l'utiliser ?**
1. Ouvre http://localhost:4200
2. Clique sur "Flow Runs" dans le menu
3. Tu vois l'historique de tous les traitements
4. Clique sur un flow pour voir les détails

---

## 🎯 Quelle Interface Pour Quel Usage ?

### Tu veux VOIR tes données ? 
→ **Dashboard Streamlit** (http://localhost:8501)
- **Pour :** Analyser, explorer, prendre des décisions
- **Public :** Toi, ton boss, l'équipe business

### Tu veux TESTER l'API ?
→ **API Documentation** (http://localhost:8000/docs)
- **Pour :** Développer, intégrer avec d'autres apps
- **Public :** Développeurs

### Tu veux VÉRIFIER la base de données ?
→ **Mongo Express** (http://localhost:8081)
- **Pour :** Débugger, voir les données brutes
- **Public :** Admins base de données

### Tu veux NAVIGUER dans les fichiers ?
→ **MinIO Console** (http://localhost:9001)
- **Pour :** Gérer les fichiers, télécharger des exports
- **Public :** Data engineers

### Tu veux VOIR l'historique des traitements ?
→ **Prefect Server** (http://localhost:4200)
- **Pour :** Vérifier que les jobs tournent bien
- **Public :** DevOps, Data engineers

---

## 📊 Cas d'Usage Pratiques

### Scénario 1 : "Je veux voir mes meilleurs clients"
1. Va sur **Dashboard** → http://localhost:8501
2. Clique sur "👥 Clients" dans la barre latérale
3. Regarde le graphique "Top 10 Clients"
4. Tu vois les noms et combien ils ont dépensé

### Scénario 2 : "Je veux récupérer les données pour Excel"
1. Va sur **API Docs** → http://localhost:8000/docs
2. Clique sur "GET /clients"
3. "Try it out" → "Execute"
4. Copie le JSON qui s'affiche
5. Colle dans un convertisseur JSON → Excel

### Scénario 3 : "Je veux vérifier que mes données sont à jour"
1. Va sur **Mongo Express** → http://localhost:8081
2. Clique sur "bigdata" → "clients_stats"
3. Regarde le nombre de documents
4. Vérifie les dates

### Scénario 4 : "Je veux télécharger les fichiers Parquet"
1. Va sur **MinIO** → http://localhost:9001
2. Login : minioadmin/minioadmin
3. Clique sur le bucket "gold"
4. Télécharge "clients_stats.parquet"

### Scénario 5 : "Je veux voir si les traitements ont réussi"
1. Va sur **Prefect** → http://localhost:4200
2. Clique sur "Flow Runs"
3. Vérifie que tout est en vert (Completed)
4. Clique sur un flow pour voir les logs

---

## 🔄 Comment Rafraîchir les Données ?

Si tu ajoutes de nouvelles ventes dans tes fichiers CSV :

```bash
# 1. Active l'environnement
source .venv/bin/activate

# 2. Lance les 4 flows dans l'ordre
python flows/bronze_ingestion.py
python flows/silver_transformation.py
python flows/gold_aggregation.py
python flows/mongodb_ingestion.py

# 3. Le dashboard se met à jour automatiquement !
```

**Temps total :** ~5 secondes

---

## 📈 Résumé des Données Disponibles

| Donnée | Où la voir | Interface |
|--------|-----------|-----------|
| **Graphiques business** | Dashboard | http://localhost:8501 |
| **JSON API** | API Docs | http://localhost:8000/docs |
| **Documents MongoDB** | Mongo Express | http://localhost:8081 |
| **Fichiers Parquet** | MinIO | http://localhost:9001 |
| **Logs des jobs** | Prefect | http://localhost:4200 |

---

## 🎓 Ce Que Chaque Niveau Apporte

### 🥉 Bronze (CSV brut)
- **Taille :** 1.1 MB
- **Format :** CSV (lisible dans Excel)
- **Utilité :** Sauvegarde originale, traçabilité

### 🥈 Silver (Nettoyé)
- **Taille :** 627 KB (43% plus petit !)
- **Format :** Parquet (optimisé)
- **Utilité :** Prêt pour l'analyse, pas d'erreurs

### 🥇 Gold (Agrégations)
- **Taille :** 120 KB (90% plus petit !)
- **Format :** Parquet
- **Utilité :** Réponses directes aux questions business

### 🗄️ MongoDB (Requêtable)
- **Taille :** 1532 documents
- **Format :** NoSQL
- **Utilité :** Requêtes ultra-rapides (<20ms)

---

## 🚀 Prêt à Explorer !

**Commence par ici :** http://localhost:8501

C'est le dashboard principal, tout y est ! 

Les autres interfaces sont pour des usages plus techniques ou de vérification.

**Bon voyage dans tes données !** 📊✨
