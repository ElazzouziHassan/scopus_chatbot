# Chatbot de Recherche Sémantique arXiv

## Aperçu

Le **Chatbot de Recherche Sémantique arXiv** est une application web intelligente qui permet d'explorer et de rechercher dans une vaste collection d'articles scientifiques provenant d'arXiv. Utilisant des techniques avancées de traitement du langage naturel et de recherche sémantique, ce projet offre une interface conversationnelle intuitive pour découvrir des recherches pertinentes.

Ce projet résout le problème de la surcharge d'information dans la littérature scientifique en permettant aux chercheurs, étudiants et professionnels de poser des questions en langage naturel et d'obtenir des réponses synthétisées basées sur des milliers d'articles scientifiques. L'application combine la puissance des embeddings sémantiques, de l'indexation vectorielle FAISS et d'une interface utilisateur moderne construite avec Streamlit.

### Fonctionnalités Clés
- **Recherche Sémantique Avancée** : Recherche par similarité de sens plutôt que par mots-clés
- **Interface Conversationnelle** : Chat interactif avec réponses détaillées et contextualisées
- **Synthèse Intelligente** : Génération automatique de réponses complètes basées sur multiple articles
- **Visualisations Interactives** : Statistiques et analyses graphiques du dataset
- **Déploiement Cloud** : Application accessible via Streamlit Cloud

## Architecture du Système

Le système suit une architecture modulaire en plusieurs étapes :

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   arXiv API     │───▶│  Extraction &    │───▶│   Nettoyage     │
│                 │    │  Collecte        │    │   des Données   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Interface Web   │◀───│  Recherche       │◀───│  Génération     │
│ (Streamlit)     │    │  Sémantique      │    │  d'Embeddings   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Index FAISS    │◀───│  Sentence       │
                       │                  │    │  Transformers   │
                       └──────────────────┘    └─────────────────┘
```

## Structure du Projet

```
Scoupus-chatbot/
├── 📂 app/                       # Applications Streamlit
│   ├── beta_hatbot.py            # Application principale
│   └── pro_chatbot.py            # Version professionnelle
├── 📂 data/                      # Données et scripts
│   ├── 📂 scripts/               # Scripts de traitement
│   │   ├── arxiv_extractor.py    # Extraction des données arXiv
│   │   ├── data_cleaner.py       # Nettoyage des données
│   │   └── semantic_indexer.py   # Création de l'index sémantique
│   ├── 📂 data_source/           # Données brutes extraites
│   ├── 📂 processed/             # Données nettoyées
│   └── 📂 search_index/          # Index de recherche FAISS
├── 📂 config/                    # Configuration
│   └── config.py                 # Paramètres de configuration
├── 📄 requirements.txt           # Dépendances Python
├── 📄 .env                       # Variables d'environnement
├── 📄 .gitignore                 # Fichiers à ignorer par Git
└── 📄 README.md                  # Documentation du projet
```

## Installation et Configuration

### Prérequis
- **Python 3.8+** (recommandé : Python 3.9 ou 3.10)
- **Git** pour cloner le repository
- **Environnement virtuel** (venv ou conda)
- **8GB+ RAM** recommandés pour le traitement des embeddings

### Installation

1. **Cloner le repository**
```bash
  git clone https://github.com/ElazzouziHassan/scopus_chatbot.git
  cd scopus_chatbot
```

2. **Créer un environnement virtuel**
```bash
  # Avec venv
  python -m venv venv
  source venv/bin/activate  # Sur Windows: venv\Scripts\activate

  # Ou avec conda
  conda create -n arxiv-chatbot python=3.9
  conda activate arxiv-chatbot
```

3. **Installer les dépendances**
```bash
  pip install -r requirements.txt
```

4. **Configurer l'environnement**
```bash
  cp .env.example .env
  # Éditer le fichier .env avec vos paramètres
```

## Construction de l'Index Sémantique

### Étape 1 : Extraction des Données

```bash
  # Extraction automatique (recommandée)
  python data/scripts/arxiv_extractor.py

  # Ou extraction personnalisée
  python data/scripts/arxiv_extractor.py \
    --query "machine learning" \
    --max_results 1000 \
    --output data/data_source/ml_papers.json
```

### Étape 2 : Nettoyage des Données

```bash
  # Nettoyage automatique
  python data/scripts/data_cleaner.py --auto

  # Ou nettoyage personnalisé
  python data/scripts/data_cleaner.py \
    --input data/data_source/raw_data.json \
    --output data/processed/clean_data.json \
    --stats
```

### Étape 3 : Génération de l'Index Sémantique

```bash
  # Création automatique de l'index
  python data/scripts/semantic_indexer.py --auto

  # Ou création personnalisée
  python data/scripts/semantic_indexer.py \
    --input data/processed/clean_data.json \
    --output data/search_index \
    --model all-MiniLM-L6-v2 \
    --test
```

**Modèles d'embeddings supportés :**
- `all-MiniLM-L6-v2` : Rapide, bonne qualité (384 dimensions)
- `all-mpnet-base-v2` : Meilleure qualité, plus lent (768 dimensions)
- `all-roberta-large-v1` : Qualité optimale, très lent (1024 dimensions)

## Lancement du Chatbot

### Exécution Locale

```bash
  # Lancer l'application principale
  streamlit run app/beta_chatbot.py

  # Ou la version professionnelle
  streamlit run app/pro_chatbot.py
```

### Comportement Attendu

1. **Interface de Chat** : Interface conversationnelle avec historique des messages
2. **Recherche Sémantique** : Recherche intelligente basée sur le sens des requêtes
3. **Réponses Synthétisées** : Réponses détaillées combinant plusieurs sources
4. **Résultats Détaillés** : Accès aux articles originaux avec scores de pertinence
5. **Statistiques** : Visualisations interactives du dataset

### Exemples de Requêtes

```
  "Qu'est-ce que l'apprentissage par renforcement ?"
  "Dernières avancées en vision par ordinateur"
  "Applications pratiques des transformers"
  "Méthodes d'optimisation en deep learning"
  "Recherches de Geoffrey Hinton sur les réseaux de neurones"
```

## Déploiement sur Streamlit Cloud

### Étapes de Déploiement

1. **Préparer le Repository**
```bash
  # S'assurer que les fichiers essentiels sont présents
  git add app/pro_chatbot.py requirements.txt README.md
  git commit -m "Prêt pour le déploiement"
  git push origin main
```

2. **Configurer Streamlit Cloud**
- Aller sur [share.streamlit.io](https://share.streamlit.io)
- Connecter votre repository GitHub
- Sélectionner `app/chatbot.py` comme fichier principal
- Déployer l'application

3. **Variables d'Environnement**
```toml
  # Dans .streamlit/secrets.toml
  [general]
  ARXIV_API_RATE_LIMIT = 3
  DEFAULT_MODEL = "all-MiniLM-L6-v2"
```

### Application Déployée
[Lien vers l'application déployée](https://votre-app.streamlit.app)

## Tests et Validation

### Tests de Performance

```bash
  # Test de l'extraction
  python data/scripts/arxiv_extractor.py --query "test" --max_results 10

  # Test de l'index sémantique
  python data/scripts/semantic_indexer.py --test
```

### Métriques de Validation

- **Temps de Réponse** : < 2 secondes pour les requêtes standard
- **Précision Sémantique** : Évaluée sur un ensemble de test de 100 requêtes
- **Couverture** : Plus de 30,000 articles scientifiques indexés
- **Satisfaction Utilisateur** : Interface intuitive et réponses pertinentes

## Métriques de Performance

| Métrique | Valeur | Description |
|----------|--------|-------------|
| **Articles Indexés** | 30,000+ | Nombre total d'articles dans la base |
| **Temps de Recherche** | < 100ms | Temps moyen de recherche sémantique |
| **Précision@10** | 85%+ | Pertinence des 10 premiers résultats |
| **Couverture Temporelle** | 2010-2024 | Période couverte par les articles |
| **Domaines** | 20+ | Nombre de domaines scientifiques |

## Mise à Jour de l'Index

### Actualisation Complète

```bash
  # Pipeline complet de mise à jour
  python data/scripts/arxiv_extractor.py --large_scale --target_size 2.0
  python data/scripts/data_cleaner.py --auto
  python data/scripts/semantic_indexer.py --auto
```

### Actualisation Incrémentale

```bash
  # Ajouter de nouveaux articles
  python data/scripts/arxiv_extractor.py \
    --query "submittedDate:[20240101 TO 20241231]" \
    --max_results 5000 \
    --output data/data_source/new_papers.json
```

## Sécurité et Confidentialité

### Gestion des Secrets

- **Variables d'environnement** : Utilisation de fichiers `.env` pour les configurations sensibles
- **Streamlit Secrets** : Configuration sécurisée pour le déploiement cloud
- **Données Publiques** : Utilisation exclusive de données publiques d'arXiv

### Bonnes Pratiques

- Ne jamais commiter de clés API dans le repository
- Utiliser des environnements virtuels isolés
- Respecter les limites de taux de l'API arXiv (3 requêtes/seconde)

## Dépannage

### Erreurs Communes

**1. Erreur d'importation de SemanticSearcher**
```bash
  # Solution : Vérifier que l'index est construit
  python data/scripts/semantic_indexer.py --auto
```

**2. Fichiers trop volumineux pour GitHub**
```bash
  # Solution : Utiliser Git LFS ou exclure les gros fichiers
  git rm --cached data/search_index/papers_data.json
  echo "data/search_index/papers_data.json" >> .gitignore
```

**3. Mémoire insuffisante**
```bash
  # Solution : Réduire la taille du batch ou utiliser un modèle plus petit
  # Modifier batch_size=16 dans semantic_indexer.py
```

**4. Erreur de connexion à l'API arXiv**
```bash
  # Solution : Vérifier la connexion internet et respecter les limites de taux
  # Attendre 3 secondes entre les requêtes
```

## Travaux Futurs / Feuille de Route

### Améliorations Prévues

- [ ] **Intégration Multi-Sources** : Ajout de PubMed, IEEE Xplore
- [ ] **Recherche Multimodale** : Support des images et graphiques
- [ ] **Personnalisation** : Profils utilisateur et recommandations
- [ ] **API REST** : Interface programmatique pour développeurs
- [ ] **Analyse de Citations** : Graphe de citations et impact des articles
- [ ] **Support Multilingue** : Interface en plusieurs langues
- [ ] **Collaboration** : Partage de collections et annotations

### Cas d'Usage Potentiels

- **Recherche Académique** : Aide à la revue de littérature
- **Veille Technologique** : Suivi des dernières innovations
- **Éducation** : Support pédagogique pour étudiants
- **R&D Industrielle** : Exploration de nouvelles technologies

## Contributeurs

### Équipe Principale

- **Groupe 2IAD (H. Elazzouzi, K. Ettalbi & O. Rochdi)** 
  - Développeurs Principal
  - Architecture du système
  - Implémentation des algorithmes de recherche
  - Interface utilisateur Streamlit

### Contributions Bienvenues

Nous accueillons les contributions de la communauté ! Voici comment contribuer :

1. **Fork** le repository
2. **Créer** une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. **Commiter** vos changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. **Pousser** vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. **Créer** une Pull Request

### Types de Contributions Recherchées

- 🐛 Correction de bugs
- ✨ Nouvelles fonctionnalités
- 📚 Amélioration de la documentation
- 🧪 Tests et validation
- 🌐 Traductions
- 🎨 Améliorations de l'interface

## Licence

Ce projet est sous licence **MIT License**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

```
MIT License

Copyright (c) 2025 2IAD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## Références et Remerciements

### Technologies Utilisées

- **[arXiv API](https://arxiv.org/help/api)** - Source des données scientifiques
- **[Sentence Transformers](https://www.sbert.net/)** - Génération d'embeddings sémantiques
- **[FAISS](https://faiss.ai/)** - Indexation et recherche vectorielle rapide
- **[Streamlit](https://streamlit.io/)** - Framework d'interface web
- **[Plotly](https://plotly.com/)** - Visualisations interactives
- **[Pandas](https://pandas.pydata.org/)** - Manipulation de données

### Bibliographie Scientifique

1. Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. *EMNLP 2019*.
2. Johnson, J., Douze, M., & Jégou, H. (2019). Billion-scale similarity search with GPUs. *IEEE Transactions on Big Data*.
3. Karpukhin, V., et al. (2020). Dense Passage Retrieval for Open-Domain Question Answering. *EMNLP 2020*.

### Remerciements Spéciaux

- **arXiv.org** pour l'accès libre aux publications scientifiques
- **Hugging Face** pour les modèles de transformers pré-entraînés
- **La communauté open-source** pour les outils et bibliothèques utilisés

---

## Démarrage Rapide

```bash
  # Installation rapide
  git clone https://github.com/ElazzouziHassan/scopus_chatbot.git
  cd scopus_chatbot
  python -m venv venv && source venv/bin/activate
  pip install -r requirements.txt

  # Construction de l'index (peut prendre 30-60 minutes)
  python data/scripts/arxiv_extractor.py
  python data/scripts/data_cleaner.py --auto
  python data/scripts/semantic_indexer.py --auto

  # Lancement de l'application
  streamlit run app/pro_chatbot.py
```

** Votre chatbot de recherche sémantique arXiv est maintenant prêt ! 🎉**

---

*Pour toute question ou support, n'hésitez pas à ouvrir une issue sur GitHub ou à nous contacter directement.*
