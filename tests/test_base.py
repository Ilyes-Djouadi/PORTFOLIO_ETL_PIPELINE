import pandas as pd

from etl_pipeline import nettoyer_donnees


def test_nettoyer_donnees():
    df_brouillon = pd.DataFrame([{"_id": "France", "total_clients": 150}])
    df_resultat = nettoyer_donnees(df_brouillon)
    
    assert "pays" in df_resultat.columns
    assert "_id" not in df_resultat.columns
    assert df_resultat["pays"].iloc[0] == "France"