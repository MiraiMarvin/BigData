from io import BytesIO

import pandas as pd
from prefect import flow, task

from config import BUCKET_BRONZE, BUCKET_SILVER, get_minio_client


@task(name="read_bronze_csv", retries=2)
def read_bronze_data(object_name: str) -> pd.DataFrame:
    client = get_minio_client()
    
    response = client.get_object(BUCKET_BRONZE, object_name)
    data = response.read()
    response.close()
    response.release_conn()
    
    df = pd.read_csv(BytesIO(data))
    print(f"Read {len(df)} rows from bronze/{object_name}")
    return df


@task(name="clean_clients", retries=2)
def clean_clients_data(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.drop_duplicates(subset=['id_client'])
    df_clean['date_inscription'] = pd.to_datetime(df_clean['date_inscription'])
    df_clean['email'] = df_clean['email'].str.lower().str.strip()
    df_clean = df_clean.dropna()
    
    print(f"Cleaned clients: {len(df)} -> {len(df_clean)} rows")
    return df_clean


@task(name="clean_achats", retries=2)
def clean_achats_data(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.drop_duplicates(subset=['id_achat'])
    df_clean['date_achat'] = pd.to_datetime(df_clean['date_achat'])
    df_clean = df_clean[df_clean['montant'] > 0]
    df_clean['date'] = df_clean['date_achat'].dt.date
    df_clean['annee'] = df_clean['date_achat'].dt.year
    df_clean['mois'] = df_clean['date_achat'].dt.month
    df_clean['jour_semaine'] = df_clean['date_achat'].dt.day_name()
    df_clean = df_clean.dropna()
    
    print(f"Cleaned achats: {len(df)} -> {len(df_clean)} rows")
    return df_clean


@task(name="write_to_silver", retries=2)
def write_to_silver(df: pd.DataFrame, object_name: str) -> str:
    client = get_minio_client()
    
    if not client.bucket_exists(BUCKET_SILVER):
        client.make_bucket(BUCKET_SILVER)
    
    buffer = BytesIO()
    df.to_parquet(buffer, index=False, engine='pyarrow')
    buffer.seek(0)
    
    client.put_object(
        BUCKET_SILVER,
        object_name,
        buffer,
        length=buffer.getbuffer().nbytes,
        content_type='application/octet-stream'
    )
    
    print(f"Wrote {len(df)} rows to silver/{object_name}")
    return object_name


@flow(name="Silver Transformation Flow")
def silver_transformation_flow() -> dict:
    clients_df = read_bronze_data("clients.csv")
    clients_clean = clean_clients_data(clients_df)
    clients_silver = write_to_silver(clients_clean, "clients.parquet")
    
    achats_df = read_bronze_data("achats.csv")
    achats_clean = clean_achats_data(achats_df)
    achats_silver = write_to_silver(achats_clean, "achats.parquet")
    
    return {
        "clients": clients_silver,
        "achats": achats_silver
    }


if __name__ == "__main__":
    result = silver_transformation_flow()
    print(f"Silver transformation complete: {result}")
