# BigData Analytics - MongoDB Integration

## 📊 Projet Réalisé

Architecture complète ELT avec MongoDB, API et Dashboard.

## 🏗️ Architecture

```
Data Sources (CSV)
    ↓
Bronze Layer (MinIO) - Données brutes
    ↓
Silver Layer (MinIO) - Données nettoyées (Parquet)
    ↓
Gold Layer (MinIO) - Agrégations (Parquet)
    ↓
MongoDB - Base NoSQL
    ↓
FastAPI - API REST
    ↓
Streamlit - Dashboard
```

## 🚀 Services Déployés

- **MinIO**: http://localhost:9001 (minioadmin/minioadmin)
- **MongoDB**: localhost:27017 (admin/admin123)
- **Mongo Express**: http://localhost:8081
- **Prefect Server**: http://localhost:4200
- **FastAPI**: http://localhost:8000
- **Streamlit Dashboard**: http://localhost:8501

## 📁 Structure du Projet

```
flows/
  ├── bronze_ingestion.py      # Ingestion CSV → Bronze
  ├── silver_transformation.py # Bronze → Silver (nettoyage)
  ├── gold_aggregation.py      # Silver → Gold (agrégations)
  └── mongodb_ingestion.py     # Gold → MongoDB
api/
  └── main.py                   # API FastAPI
dashboard.py                    # Dashboard Streamlit
```

## 🎯 Flows Prefect Créés

### 1. Bronze Ingestion
- Upload CSV vers MinIO bucket `sources`
- Copie vers bucket `bronze`

### 2. Silver Transformation
- Lecture depuis `bronze`
- Nettoyage des données:
  - Suppression doublons
  - Conversion des dates
  - Validation des montants
  - Enrichissement (année, mois, jour de semaine)
- Écriture en Parquet vers `silver`

### 3. Gold Aggregation
- Lecture depuis `silver`
- Création de 4 agrégations:
  - **clients_stats**: Statistiques par client
  - **product_stats**: Ventes par produit
  - **monthly_stats**: Tendances mensuelles
  - **country_stats**: Performance par pays
- Écriture en Parquet vers `gold`

### 4. MongoDB Ingestion
- Lecture Parquet depuis `gold`
- Ingestion dans MongoDB (4 collections)
- Mesure du temps d'ingestion

## 📊 Collections MongoDB

1. **clients_stats** (1500 docs) - Stats clients
2. **product_stats** (10 docs) - Stats produits
3. **monthly_stats** (13 docs) - Stats mensuelles
4. **country_stats** (9 docs) - Stats pays

## 🔌 API Endpoints

- `GET /` - Info API
- `GET /health` - Health check
- `GET /clients` - Liste clients (avec filtres)
- `GET /products` - Stats produits
- `GET /monthly` - Stats mensuelles
- `GET /countries` - Stats pays
- `GET /top-clients` - Top clients
- `GET /stats/summary` - Résumé global

## 📈 Dashboard Streamlit

6 pages interactives:
- 🏠 **Accueil**: Vue d'ensemble
- 👥 **Clients**: Statistiques clients avec filtres
- 📦 **Produits**: Analyse des ventes
- 📅 **Tendances**: Évolution temporelle
- 🌍 **Pays**: Performance géographique
- ⚡ **Performances**: Benchmarks API

## ⚡ Performances Mesurées

### MongoDB Ingestion
- **Total rows**: 1532
- **Temps total**: 0.213s
- **Détail**:
  - clients_stats: 1500 rows en 0.058s
  - product_stats: 10 rows en 0.019s
  - monthly_stats: 13 rows en 0.019s
  - country_stats: 9 rows en 0.019s

### API Response Times
Les temps de réponse sont mesurables via la page Performances du dashboard.

## 🎮 Commandes Utiles

### Lancer tous les flows
```bash
source .venv/bin/activate
python flows/bronze_ingestion.py
python flows/silver_transformation.py
python flows/gold_aggregation.py
python flows/mongodb_ingestion.py
```

### Lancer l'API
```bash
source .venv/bin/activate
python api/main.py
```

### Lancer le Dashboard
```bash
source .venv/bin/activate
streamlit run dashboard.py
```

### Docker
```bash
# Démarrer l'infrastructure
docker compose up -d

# Voir les logs
docker compose logs -f mongodb

# Arrêter
docker compose down
```

## 📊 Données Traitées

- **Clients**: 1500
- **Achats**: 23,663
- **Produits**: 10
- **Pays**: 9
- **Période**: 13 mois

## 🎓 Concepts BigData Utilisés

1. **Architecture Medallion** (Bronze/Silver/Gold)
2. **Data Lake** (MinIO S3)
3. **NoSQL Database** (MongoDB)
4. **REST API** (FastAPI)
5. **Data Orchestration** (Prefect)
6. **Interactive Dashboard** (Streamlit)
7. **Format Parquet** (optimisé pour analytics)

## ✅ Consigne Réalisée

**Base NoSQL opérationnelle avec MongoDB**:
- ✅ Pipeline qui lit Gold (Parquet) et écrit dans MongoDB
- ✅ API Flask/FastAPI qui expose les données MongoDB
- ✅ Dashboard Streamlit qui interroge l'API
- ✅ Calcul du temps de refresh mesuré
- ⏳ Bonus Metabase (optionnel)
