import time
from io import BytesIO

import pandas as pd
from prefect import flow, task
from pymongo import MongoClient

from config import BUCKET_GOLD, get_minio_client


# Configuration MongoDB
MONGODB_URI = "mongodb://admin:admin123@localhost:27017/"
MONGODB_DATABASE = "bigdata"


def get_mongodb_client():
    """Get MongoDB client connection."""
    return MongoClient(MONGODB_URI)


@task(name="read_gold_parquet", retries=2)
def read_gold_data(object_name: str) -> pd.DataFrame:

    client = get_minio_client()
    
    response = client.get_object(BUCKET_GOLD, object_name)
    data = response.read()
    response.close()
    response.release_conn()
    
    df = pd.read_parquet(BytesIO(data))
    print(f"Read {len(df)} rows from gold/{object_name}")
    return df


@task(name="write_to_mongodb", retries=2)
def write_to_mongodb(df: pd.DataFrame, collection_name: str) -> dict:
    start_time = time.time()
    
    mongo_client = get_mongodb_client()
    db = mongo_client[MONGODB_DATABASE]
    collection = db[collection_name]
    
    collection.drop()
    
    df_copy = df.copy()
    for col in df_copy.columns:
        if pd.api.types.is_datetime64_any_dtype(df_copy[col]):
            df_copy[col] = df_copy[col].astype(str)
    
    records = df_copy.to_dict('records')
    result = collection.insert_many(records)
    
    elapsed_time = time.time() - start_time
    
    stats = {
        "collection": collection_name,
        "rows_inserted": len(result.inserted_ids),
        "time_seconds": round(elapsed_time, 3)
    }
    
    print(f"Inserted {stats['rows_inserted']} rows into {collection_name} in {stats['time_seconds']}s")
    
    mongo_client.close()
    return stats


@flow(name="MongoDB Ingestion Flow")
def mongodb_ingestion_flow() -> dict:
    start_time = time.time()
    
    # Liste des fichiers gold à charger
    gold_files = {
        "clients_stats": "clients_stats.parquet",
        "product_stats": "product_stats.parquet",
        "monthly_stats": "monthly_stats.parquet",
        "country_stats": "country_stats.parquet"
    }
    
    results = {}
    
    for collection_name, file_name in gold_files.items():
        df = read_gold_data(file_name)
        
        stats = write_to_mongodb(df, collection_name)
        results[collection_name] = stats
    
    total_time = time.time() - start_time
    
    summary = {
        "collections": results,
        "total_time_seconds": round(total_time, 3),
        "total_rows": sum(r['rows_inserted'] for r in results.values())
    }
    
    print(f"\n=== MongoDB Ingestion Summary ===")
    print(f"Total rows: {summary['total_rows']}")
    print(f"Total time: {summary['total_time_seconds']}s")
    
    return summary


if __name__ == "__main__":
    result = mongodb_ingestion_flow()
    print(f"\nMongoDB ingestion complete: {result}")
