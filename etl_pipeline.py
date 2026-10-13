import os

import certifi
import duckdb
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

def nettoyer_donnees(df: pd.DataFrame) -> pd.DataFrame:
    """Transformation : normalisation de la colonne d'identification."""
    if "_id" in df.columns:
        df = df.rename(columns={"_id": "pays"})
    return df

def run_pipeline() -> None:
    print("[ETAPE 1] EXTRACT (NoSQL) : Connexion a MongoDB Atlas...")
    uri = os.environ["MONGODB_URI"]
    
    try:
        client: MongoClient = MongoClient(uri, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=2000)
        base_clients = client["mon_entreprise"]["base_clients"]

        print("[ETAPE 2] TRANSFORM (Serveur) : Agregation MongoDB...")
        pipeline = [
            {"$match": {"statut": "Premium"}},
            {"$group": {"_id": "$pays", "total_clients": {"$sum": 1}}},
            {"$sort": {"total_clients": -1}},
            {"$limit": 3}
        ]
        curseur_nosql = base_clients.aggregate(pipeline)

        print("[ETAPE 3] TRANSFORM (Local) : Hybridation avec Pandas...")
        df = pd.DataFrame(list(curseur_nosql))
        df_propre = nettoyer_donnees(df)
        print(df_propre)

        print("[ETAPE 4] LOAD (SQL) : Chargement vers DuckDB...")
        con = duckdb.connect(database='mon_entrepot_analytique.db')
        con.execute("CREATE OR REPLACE TABLE top_pays_premium AS SELECT * FROM df_propre")
        
        print("[SUCCES] Pipeline execute avec succes.")
        
    except Exception as e:  # noqa: BLE001
        print(f"[ALERTE] Execution bloquee (Normal en CI/CD) : {e}")
        raise

if __name__ == "__main__":
    run_pipeline()