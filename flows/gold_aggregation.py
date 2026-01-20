from io import BytesIO

import pandas as pd
from prefect import flow, task

from config import BUCKET_GOLD, BUCKET_SILVER, get_minio_client


@task(name="read_silver_parquet", retries=2)
def read_silver_data(object_name: str) -> pd.DataFrame:

    client = get_minio_client()
    
    response = client.get_object(BUCKET_SILVER, object_name)
    data = response.read()
    response.close()
    response.release_conn()
    
    df = pd.read_parquet(BytesIO(data))
    print(f"Read {len(df)} rows from silver/{object_name}")
    return df


@task(name="aggregate_clients_stats", retries=2)
def create_clients_stats(clients_df: pd.DataFrame, achats_df: pd.DataFrame) -> pd.DataFrame:
    stats = achats_df.groupby('id_client').agg(
        nombre_achats=('id_achat', 'count'),
        montant_total=('montant', 'sum'),
        montant_moyen=('montant', 'mean'),
        premier_achat=('date_achat', 'min'),
        dernier_achat=('date_achat', 'max')
    ).reset_index()
    
    result = clients_df.merge(stats, on='id_client', how='left')
    
    result['nombre_achats'] = result['nombre_achats'].fillna(0).astype(int)
    result['montant_total'] = result['montant_total'].fillna(0)
    result['montant_moyen'] = result['montant_moyen'].fillna(0)
    
    print(f"Created stats for {len(result)} clients")
    return result


@task(name="aggregate_sales_by_product", retries=2)
def create_product_stats(achats_df: pd.DataFrame) -> pd.DataFrame:
    stats = achats_df.groupby('produit').agg(
        nombre_ventes=('id_achat', 'count'),
        chiffre_affaires=('montant', 'sum'),
        prix_moyen=('montant', 'mean'),
        prix_min=('montant', 'min'),
        prix_max=('montant', 'max')
    ).reset_index()
    
    # Tri par chiffre d'affaires décroissant
    stats = stats.sort_values('chiffre_affaires', ascending=False)
    
    print(f"Created stats for {len(stats)} products")
    return stats


@task(name="aggregate_sales_by_month", retries=2)
def create_monthly_stats(achats_df: pd.DataFrame) -> pd.DataFrame:
    achats_df['annee_mois'] = achats_df['date_achat'].dt.to_period('M').astype(str)
    
    stats = achats_df.groupby('annee_mois').agg(
        nombre_achats=('id_achat', 'count'),
        chiffre_affaires=('montant', 'sum'),
        panier_moyen=('montant', 'mean'),
        nombre_clients_uniques=('id_client', 'nunique')
    ).reset_index()
    
    print(f"Created monthly stats for {len(stats)} months")
    return stats


@task(name="aggregate_sales_by_country", retries=2)
def create_country_stats(clients_df: pd.DataFrame, achats_df: pd.DataFrame) -> pd.DataFrame:
    data = achats_df.merge(clients_df[['id_client', 'pays']], on='id_client', how='left')
    
    stats = data.groupby('pays').agg(
        nombre_clients=('id_client', 'nunique'),
        nombre_achats=('id_achat', 'count'),
        chiffre_affaires=('montant', 'sum'),
        panier_moyen=('montant', 'mean')
    ).reset_index()
    
    stats = stats.sort_values('chiffre_affaires', ascending=False)
    
    print(f"Created stats for {len(stats)} countries")
    return stats


@task(name="write_to_gold", retries=2)
def write_to_gold(df: pd.DataFrame, object_name: str) -> str:

    client = get_minio_client()
    
    if not client.bucket_exists(BUCKET_GOLD):
        client.make_bucket(BUCKET_GOLD)
    
    buffer = BytesIO()
    df.to_parquet(buffer, index=False, engine='pyarrow')
    buffer.seek(0)
    
    client.put_object(
        BUCKET_GOLD,
        object_name,
        buffer,
        length=buffer.getbuffer().nbytes,
        content_type='application/octet-stream'
    )
    
    print(f"Wrote {len(df)} rows to gold/{object_name}")
    return object_name


@flow(name="Gold Aggregation Flow")
def gold_aggregation_flow() -> dict:
    clients_df = read_silver_data("clients.parquet")
    achats_df = read_silver_data("achats.parquet")
    
    clients_stats = create_clients_stats(clients_df, achats_df)
    product_stats = create_product_stats(achats_df)
    monthly_stats = create_monthly_stats(achats_df)
    country_stats = create_country_stats(clients_df, achats_df)
    
    gold_clients = write_to_gold(clients_stats, "clients_stats.parquet")
    gold_products = write_to_gold(product_stats, "product_stats.parquet")
    gold_monthly = write_to_gold(monthly_stats, "monthly_stats.parquet")
    gold_country = write_to_gold(country_stats, "country_stats.parquet")
    
    return {
        "clients_stats": gold_clients,
        "product_stats": gold_products,
        "monthly_stats": gold_monthly,
        "country_stats": gold_country
    }


if __name__ == "__main__":
    result = gold_aggregation_flow()
    print(f"Gold aggregation complete: {result}")
