import time

import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from pandas import DataFrame

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="BigData Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("BigData Analytics Dashboard")
st.markdown("Dashboard interactif alimenté par MongoDB via API FastAPI")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choisir une vue",
    ["Accueil", "Clients", "Produits", "Tendances", "Pays", "Performances"]
)


def fetch_api(endpoint: str, params: dict = None) -> dict:
    try:
        start_time = time.time()
        response = requests.get(f"{API_URL}{endpoint}", params=params, timeout=10)
        elapsed = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            return {
                "data": response.json(),
                "success": True,
                "response_time": elapsed
            }
        else:
            return {
                "data": None,
                "success": False,
                "error": f"Error {response.status_code}: {response.text}",
                "response_time": elapsed
            }
    except Exception as e:
        return {
            "data": None,
            "success": False,
            "error": str(e),
            "response_time": 0
        }


if page == "Accueil":
    st.header("Vue d'ensemble")
    
    result = fetch_api("/stats/summary")
    
    if result["success"]:
        data = result["data"]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Clients", f"{data.get('total_clients', 0):,}")
        with col2:
            st.metric("Total Produits", data.get('total_products', 0))
        with col3:
            st.metric("Chiffre d'Affaires", f"{data.get('total_revenue', 0):,.2f} €")
        with col4:
            st.metric("Commandes", f"{data.get('total_orders', 0):,}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Valeur Client Moyenne", f"{data.get('average_customer_value', 0):,.2f} €")
        with col2:
            st.metric("Pays Actifs", data.get('total_countries', 0))
        with col3:
            st.metric("Temps de Réponse API", f"{data.get('response_time_ms', 0):.2f} ms")
        
        st.success("API et MongoDB opérationnels")
    else:
        st.error(f"Erreur lors de la récupération des données: {result.get('error')}")


elif page == "Clients":
    st.header("Statistiques Clients")
    
    col1, col2 = st.columns(2)
    with col1:
        limit = st.slider("Nombre de clients", 10, 500, 100)
    with col2:
        countries_result = fetch_api("/countries")
        if countries_result["success"]:
            countries = ["Tous"] + [c["pays"] for c in countries_result["data"]]
            selected_country = st.selectbox("Filtrer par pays", countries)
        else:
            selected_country = "Tous"
    
    params = {"limit": limit}
    if selected_country != "Tous":
        params["pays"] = selected_country
    
    result = fetch_api("/clients", params)
    
    if result["success"]:
        df = DataFrame(result["data"])
        
        st.metric("Temps de réponse API", f"{result['response_time']:.2f} ms")
        
        st.subheader("Top Clients par Chiffre d'Affaires")
        top_clients = df.nlargest(10, 'montant_total')
        
        fig = px.bar(
            top_clients,
            x='nom',
            y='montant_total',
            color='pays',
            title="Top 10 Clients",
            labels={'montant_total': 'CA Total (€)', 'nom': 'Client'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        if selected_country == "Tous":
            st.subheader("Distribution des Clients par Pays")
            country_counts = df['pays'].value_counts()
            fig = px.pie(values=country_counts.values, names=country_counts.index, title="Clients par Pays")
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Données Détaillées")
        st.dataframe(df, use_container_width=True)
    else:
        st.error(f"Erreur: {result.get('error')}")


elif page == "Produits":
    st.header("Statistiques Produits")
    
    result = fetch_api("/products")
    
    if result["success"]:
        df = DataFrame(result["data"])
        
        st.metric("Temps de réponse API", f"{result['response_time']:.2f} ms")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                df.sort_values('chiffre_affaires', ascending=False),
                x='produit',
                y='chiffre_affaires',
                title="Chiffre d'Affaires par Produit",
                labels={'chiffre_affaires': 'CA (€)', 'produit': 'Produit'},
                color='chiffre_affaires',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                df.sort_values('nombre_ventes', ascending=False),
                x='produit',
                y='nombre_ventes',
                title="Nombre de Ventes par Produit",
                labels={'nombre_ventes': 'Ventes', 'produit': 'Produit'},
                color='nombre_ventes',
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Analyse des Prix")
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Prix Moyen', x=df['produit'], y=df['prix_moyen']))
        fig.add_trace(go.Bar(name='Prix Min', x=df['produit'], y=df['prix_min']))
        fig.add_trace(go.Bar(name='Prix Max', x=df['produit'], y=df['prix_max']))
        fig.update_layout(barmode='group', title="Comparaison des Prix")
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df, use_container_width=True)
    else:
        st.error(f"Erreur: {result.get('error')}")


elif page == "Tendances":
    st.header("Tendances Mensuelles")
    
    result = fetch_api("/monthly")
    
    if result["success"]:
        df = DataFrame(result["data"])
        
        st.metric("Temps de réponse API", f"{result['response_time']:.2f} ms")
        
        fig = px.line(
            df,
            x='annee_mois',
            y='chiffre_affaires',
            title="Évolution du Chiffre d'Affaires",
            labels={'chiffre_affaires': 'CA (€)', 'annee_mois': 'Mois'},
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                df,
                x='annee_mois',
                y='nombre_achats',
                title="Nombre d'Achats par Mois",
                labels={'nombre_achats': 'Achats', 'annee_mois': 'Mois'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(
                df,
                x='annee_mois',
                y='panier_moyen',
                title="Évolution du Panier Moyen",
                labels={'panier_moyen': 'Panier Moyen (€)', 'annee_mois': 'Mois'},
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df, use_container_width=True)
    else:
        st.error(f"Erreur: {result.get('error')}")


elif page == "Pays":
    st.header("Statistiques par Pays")
    
    result = fetch_api("/countries")
    
    if result["success"]:
        df = DataFrame(result["data"])
        
        st.metric("Temps de réponse API", f"{result['response_time']:.2f} ms")
        
        fig = px.bar(
            df.sort_values('chiffre_affaires', ascending=False),
            x='pays',
            y='chiffre_affaires',
            title="Chiffre d'Affaires par Pays",
            labels={'chiffre_affaires': 'CA (€)', 'pays': 'Pays'},
            color='chiffre_affaires',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                df,
                values='nombre_clients',
                names='pays',
                title="Répartition des Clients par Pays"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                df.sort_values('panier_moyen', ascending=False),
                x='pays',
                y='panier_moyen',
                title="Panier Moyen par Pays",
                labels={'panier_moyen': 'Panier Moyen (€)', 'pays': 'Pays'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df, use_container_width=True)
    else:
        st.error(f"Erreur: {result.get('error')}")


elif page == "Performances":
    st.header("Mesures de Performance")
    
    st.markdown("""
    Cette page permet de comparer les temps de réponse des différents endpoints de l'API.
    """)
    
    if st.button("🔄 Lancer les tests de performance"):
        with st.spinner("Tests en cours..."):
            endpoints = [
                ("/clients", {"limit": 100}),
                ("/clients", {"limit": 500}),
                ("/products", None),
                ("/monthly", None),
                ("/countries", None),
                ("/stats/summary", None),
                ("/top-clients", {"limit": 10})
            ]
            
            results = []
            
            for endpoint, params in endpoints:
                result = fetch_api(endpoint, params)
                param_str = f"?{params}" if params else ""
                results.append({
                    "Endpoint": f"{endpoint}{param_str}",
                    "Temps (ms)": round(result["response_time"], 2),
                    "Statut": "OK" if result["success"] else "Erreur",
                    "Records": len(result["data"]) if result["success"] and isinstance(result["data"], list) else "-"
                })
            
            df = DataFrame(results)
            
            fig = px.bar(
                df,
                x='Endpoint',
                y='Temps (ms)',
                title="Temps de Réponse par Endpoint",
                labels={'Temps (ms)': 'Temps de Réponse (ms)'},
                color='Temps (ms)',
                color_continuous_scale='RdYlGn_r'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(df, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Temps Moyen", f"{df['Temps (ms)'].mean():.2f} ms")
            with col2:
                st.metric("Temps Min", f"{df['Temps (ms)'].min():.2f} ms")
            with col3:
                st.metric("Temps Max", f"{df['Temps (ms)'].max():.2f} ms")


st.sidebar.markdown("---")
st.sidebar.info(
    """
    **Architecture:**
    - MinIO (Data Lake)
    - MongoDB (NoSQL)
    - FastAPI (API)
    - Streamlit (Dashboard)
    """
)
