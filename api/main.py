import time
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel

MONGODB_URI = "mongodb://admin:admin123@localhost:27017/"
MONGODB_DATABASE = "bigdata"

app = FastAPI(
    title="BigData Analytics API",
    description="API pour accéder aux données analytics stockées dans MongoDB",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    client = MongoClient(MONGODB_URI)
    return client[MONGODB_DATABASE]


class ClientStats(BaseModel):
    id_client: int
    nom: str
    email: str
    date_inscription: str
    pays: str
    nombre_achats: int
    montant_total: float
    montant_moyen: float
    premier_achat: Optional[str] = None
    dernier_achat: Optional[str] = None


class ProductStats(BaseModel):
    produit: str
    nombre_ventes: int
    chiffre_affaires: float
    prix_moyen: float
    prix_min: float
    prix_max: float


class MonthlyStats(BaseModel):
    annee_mois: str
    nombre_achats: int
    chiffre_affaires: float
    panier_moyen: float
    nombre_clients_uniques: int


class CountryStats(BaseModel):
    pays: str
    nombre_clients: int
    nombre_achats: int
    chiffre_affaires: float
    panier_moyen: float


class APIStats(BaseModel):
    endpoint: str
    response_time_ms: float
    records_count: int


# === Endpoints ===

@app.get("/")
def root():
    return {
        "message": "BigData Analytics API",
        "version": "1.0.0",
        "endpoints": {
            "clients": "/clients",
            "products": "/products",
            "monthly": "/monthly",
            "countries": "/countries",
            "top_clients": "/top-clients",
            "health": "/health"
        }
    }


@app.get("/health")
def health_check():
    try:
        db = get_db()
        db.list_collection_names()
        return {
            "status": "healthy",
            "database": MONGODB_DATABASE,
            "collections": db.list_collection_names()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")


@app.get("/clients", response_model=List[ClientStats])
def get_clients(
    limit: int = Query(100, ge=1, le=1000, description="Nombre de clients à retourner"),
    skip: int = Query(0, ge=0, description="Nombre de clients à sauter"),
    pays: Optional[str] = Query(None, description="Filtrer par pays")
):
    start_time = time.time()
    
    db = get_db()
    collection = db["clients_stats"]
    
    filter_query = {}
    if pays:
        filter_query["pays"] = pays
    
    cursor = collection.find(filter_query, {"_id": 0}).skip(skip).limit(limit)
    results = list(cursor)
    
    elapsed = (time.time() - start_time) * 1000
    print(f"GET /clients - {len(results)} records in {elapsed:.2f}ms")
    
    return results


@app.get("/products", response_model=List[ProductStats])
def get_products():
    start_time = time.time()
    
    db = get_db()
    collection = db["product_stats"]
    
    cursor = collection.find({}, {"_id": 0})
    results = list(cursor)
    
    elapsed = (time.time() - start_time) * 1000
    print(f"GET /products - {len(results)} records in {elapsed:.2f}ms")
    
    return results


@app.get("/monthly", response_model=List[MonthlyStats])
def get_monthly_stats():
    start_time = time.time()
    
    db = get_db()
    collection = db["monthly_stats"]
    
    cursor = collection.find({}, {"_id": 0})
    results = list(cursor)
    
    elapsed = (time.time() - start_time) * 1000
    print(f"GET /monthly - {len(results)} records in {elapsed:.2f}ms")
    
    return results


@app.get("/countries", response_model=List[CountryStats])
def get_country_stats():
    start_time = time.time()
    
    db = get_db()
    collection = db["country_stats"]
    
    cursor = collection.find({}, {"_id": 0})
    results = list(cursor)
    
    elapsed = (time.time() - start_time) * 1000
    print(f"GET /countries - {len(results)} records in {elapsed:.2f}ms")
    
    return results


@app.get("/top-clients")
def get_top_clients(limit: int = Query(10, ge=1, le=100, description="Nombre de top clients")):
    start_time = time.time()
    
    db = get_db()
    collection = db["clients_stats"]
    
    cursor = collection.find(
        {}, 
        {"_id": 0}
    ).sort("montant_total", -1).limit(limit)
    
    results = list(cursor)
    
    elapsed = (time.time() - start_time) * 1000
    print(f"GET /top-clients - {len(results)} records in {elapsed:.2f}ms")
    
    return results


@app.get("/stats/summary")
def get_summary_stats():
    start_time = time.time()
    
    db = get_db()
    
    summary = {
        "total_clients": db["clients_stats"].count_documents({}),
        "total_products": db["product_stats"].count_documents({}),
        "total_months": db["monthly_stats"].count_documents({}),
        "total_countries": db["country_stats"].count_documents({}),
    }
    
    clients = list(db["clients_stats"].find({}, {"_id": 0, "montant_total": 1, "nombre_achats": 1}))
    if clients:
        summary["total_revenue"] = sum(c.get("montant_total", 0) for c in clients)
        summary["total_orders"] = sum(c.get("nombre_achats", 0) for c in clients)
        summary["average_customer_value"] = summary["total_revenue"] / len(clients) if clients else 0
    
    elapsed = (time.time() - start_time) * 1000
    summary["response_time_ms"] = round(elapsed, 2)
    
    print(f"GET /stats/summary - {elapsed:.2f}ms")
    
    return summary


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
