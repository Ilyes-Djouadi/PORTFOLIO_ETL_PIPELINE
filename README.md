# Pipeline ETL Hybride : MongoDB Atlas vers DuckDB via Pandas

## L'Objectif Métier
Ce projet est un pipeline d'ingénierie de données (ETL) conçu pour extraire des données clients depuis une base NoSQL Cloud, les transformer, et les charger dans un entrepôt analytique local pour des requêtes haute performance.

## Architecture Technique

1. **Extract (Cloud NoSQL)** : Connexion sécurisée (protocole TLS via certifi) à un cluster MongoDB Atlas.
2. **Transform (Serveur distant & Local)** : 
   - Exploitation du pipeline d'agrégation MongoDB ($match, $group) pour filtrer les données à la source et minimiser l'empreinte mémoire.
   - Nettoyage final et formatage des structures de données via Pandas.
3. **Load (Stockage Analytique)** : Chargement du DataFrame formaté dans DuckDB, générant une table SQL (top_pays_premium) optimisée pour la Business Intelligence.

## Qualité & Intégration Continue (CI/CD)
Ce dépôt respecte les standards de production via l'automatisation GitHub Actions :
- **Formatage & Linting** : Contrôle continu via Ruff.
- **Tests Automatisés** : Validation de la logique de transformation via Pytest.
- **Sécurité** : Exclusion stricte des bases de données locales (.db) et des fichiers de configuration (.env) du contrôle de version.