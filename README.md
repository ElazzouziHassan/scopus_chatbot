# arXiv Semantic Search Chatbot

## Overview

The **arXiv Semantic Search Chatbot** is an intelligent web application that lets you explore and search a large collection of scientific papers from arXiv. Using advanced natural language processing and semantic search techniques, this project provides an intuitive conversational interface for discovering relevant research.

It addresses the problem of information overload in scientific literature by letting researchers, students, and professionals ask questions in natural language and get synthesized answers drawn from thousands of scientific articles. The application combines semantic embeddings, FAISS vector indexing, and a modern user interface built with Streamlit.

This project is described in the accompanying research paper: *"Development of an Intelligent Conversational Assistant for Semantic Exploration of Scientific Articles"* — see [Citation](#citation) below.

### Key Features

- **Advanced Semantic Search** — search by meaning rather than exact keywords
- **Conversational Interface** — interactive chat with detailed, contextualized answers
- **Intelligent Synthesis** — automatic generation of comprehensive answers drawn from multiple articles
- **Interactive Visualizations** — statistics and graphical analysis of the dataset
- **Cloud Deployment** — accessible via Streamlit Cloud

## System Architecture

The system follows a modular, multi-stage architecture:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   arXiv API      │───▶│  Extraction &    │───▶│   Data          │
│                   │    │  Collection      │    │   Cleaning      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Web Interface     │◀───│  Semantic        │◀───│  Embedding      │
│ (Streamlit)       │    │  Search          │    │  Generation     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                       ┌──────────────────┐    ┌─────────────────┐
                       │   FAISS Index     │◀───│  Sentence       │
                       │                    │    │  Transformers   │
                       └──────────────────┘    └─────────────────┘
```

## Project Structure

```
scopus_chatbot/
├── 📂 app/                       # Streamlit applications
│   ├── beta_chatbot.py           # Main application
│   └── pro_chatbot.py            # Production-ready version
├── 📂 data/                      # Data and scripts
│   ├── 📂 scripts/               # Processing scripts
│   │   ├── arxiv_extractor.py    # arXiv data extraction
│   │   ├── data_cleaner.py       # Data cleaning
│   │   └── semantic_indexer.py   # Semantic index creation
│   ├── 📂 data_source/           # Raw extracted data
│   ├── 📂 processed/             # Cleaned data
│   └── 📂 search_index/          # FAISS search index
├── 📂 config/                    # Configuration
│   └── config.py                 # Configuration parameters
├── 📄 requirements.txt           # Python dependencies
├── 📄 .env                       # Environment variables
├── 📄 .gitignore                 # Git-ignored files
├── 📄 CITATION.cff               # Citation metadata
└── 📄 README.md                  # Project documentation
```

## Installation and Setup

### Prerequisites

- **Python 3.8+** (recommended: Python 3.9 or 3.10)
- **Git** to clone the repository
- **Virtual environment** (venv or conda)
- **8GB+ RAM** recommended for embedding processing

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/ElazzouziHassan/scopus_chatbot.git
cd scopus_chatbot
```

2. **Create a virtual environment**

```bash
# With venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or with conda
conda create -n arxiv-chatbot python=3.9
conda activate arxiv-chatbot
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure the environment**

```bash
cp .env.example .env
# Edit the .env file with your settings
```

## Building the Semantic Index

### Step 1: Data Extraction

```bash
# Automatic extraction (recommended)
python data/scripts/arxiv_extractor.py

# Or custom extraction
python data/scripts/arxiv_extractor.py \
  --query "machine learning" \
  --max_results 1000 \
  --output data/data_source/ml_papers.json
```

### Step 2: Data Cleaning

```bash
# Automatic cleaning
python data/scripts/data_cleaner.py --auto

# Or custom cleaning
python data/scripts/data_cleaner.py \
  --input data/data_source/raw_data.json \
  --output data/processed/clean_data.json \
  --stats
```

### Step 3: Semantic Index Generation

```bash
# Automatic index creation
python data/scripts/semantic_indexer.py --auto

# Or custom index creation
python data/scripts/semantic_indexer.py \
  --input data/processed/clean_data.json \
  --output data/search_index \
  --model all-MiniLM-L6-v2 \
  --test
```

**Supported embedding models:**

- `all-MiniLM-L6-v2` — fast, good quality (384 dimensions)
- `all-mpnet-base-v2` — better quality, slower (768 dimensions)
- `all-roberta-large-v1` — best quality, very slow (1024 dimensions)

## Running the Chatbot

### Local Execution

```bash
# Launch the main application
streamlit run app/beta_chatbot.py

# Or the production version
streamlit run app/pro_chatbot.py
```

### Expected Behavior

1. **Chat Interface** — conversational interface with message history
2. **Semantic Search** — intelligent search based on the meaning of queries
3. **Synthesized Answers** — detailed responses combining multiple sources
4. **Detailed Results** — access to original articles with relevance scores
5. **Statistics** — interactive dataset visualizations

### Example Queries

```
"What is reinforcement learning?"
"Latest advances in computer vision"
"Practical applications of transformers"
"Optimization methods in deep learning"
"Geoffrey Hinton's research on neural networks"
```

## Deployment on Streamlit Cloud

### Deployment Steps

1. **Prepare the repository**

```bash
# Make sure the essential files are present
git add app/pro_chatbot.py requirements.txt README.md
git commit -m "Ready for deployment"
git push origin main
```

2. **Configure Streamlit Cloud**

- Go to [share.streamlit.io](https://share.streamlit.io)
- Connect your GitHub repository
- Select `app/pro_chatbot.py` as the main file
- Deploy the application

3. **Environment Variables**

```toml
# In .streamlit/secrets.toml
[general]
ARXIV_API_RATE_LIMIT = 3
DEFAULT_MODEL = "all-MiniLM-L6-v2"
```

## Testing and Validation

### Performance Tests

```bash
# Test extraction
python data/scripts/arxiv_extractor.py --query "test" --max_results 10

# Test the semantic index
python data/scripts/semantic_indexer.py --test
```

### Validation Metrics

- **Response Time**: < 2 seconds for standard queries
- **Semantic Precision**: evaluated on a test set of 100 queries
- **Coverage**: over 30,000 scientific articles indexed
- **User Satisfaction**: intuitive interface and relevant answers

## Performance Metrics

| Metric                 | Value      | Description                             |
| ----------------------- | ---------- | ---------------------------------------- |
| **Indexed Articles**    | 30,000+    | Total number of articles in the database |
| **Search Time**         | < 100ms    | Average semantic search time             |
| **Precision@10**        | 85%+       | Relevance of the top 10 results          |
| **Time Coverage**       | 2010–2024  | Period covered by the articles           |
| **Domains**             | 20+        | Number of scientific domains             |

## Updating the Index

### Full Refresh

```bash
# Complete update pipeline
python data/scripts/arxiv_extractor.py --large_scale --target_size 2.0
python data/scripts/data_cleaner.py --auto
python data/scripts/semantic_indexer.py --auto
```

### Incremental Update

```bash
# Add new articles
python data/scripts/arxiv_extractor.py \
  --query "submittedDate:[20240101 TO 20241231]" \
  --max_results 5000 \
  --output data/data_source/new_papers.json
```

## Security and Privacy

### Secrets Management

- **Environment variables**: `.env` files for sensitive configuration
- **Streamlit Secrets**: secure configuration for cloud deployment
- **Public Data**: uses exclusively public arXiv data

### Best Practices

- Never commit API keys to the repository
- Use isolated virtual environments
- Respect arXiv API rate limits (3 requests/second)

## Troubleshooting

### Common Errors

**1. SemanticSearcher import error**

```bash
# Solution: make sure the index has been built
python data/scripts/semantic_indexer.py --auto
```

**2. Files too large for GitHub**

```bash
# Solution: use Git LFS or exclude large files
git rm --cached data/search_index/papers_data.json
echo "data/search_index/papers_data.json" >> .gitignore
```

**3. Insufficient memory**

```bash
# Solution: reduce batch size or use a smaller model
# Set batch_size=16 in semantic_indexer.py
```

**4. arXiv API connection error**

```bash
# Solution: check your internet connection and respect rate limits
# Wait 3 seconds between requests
```

## Future Work / Roadmap

### Planned Improvements

- [ ] **Multi-Source Integration**: add PubMed, IEEE Xplore
- [ ] **Multimodal Search**: support for images and figures
- [ ] **Personalization**: user profiles and recommendations
- [ ] **REST API**: programmatic interface for developers
- [ ] **Citation Analysis**: citation graph and article impact
- [ ] **Multilingual Support**: interface in multiple languages
- [ ] **Collaboration**: shared collections and annotations

### Potential Use Cases

- **Academic Research**: literature review assistance
- **Technology Watch**: tracking the latest innovations
- **Education**: teaching support for students
- **Industrial R&D**: exploring new technologies

## Contributors

### Core Team

- **Group 2IAD (H. El Azzouzi, K. Ettalbi & O. Rochdi)**
  - Lead developers
  - System architecture
  - Search algorithm implementation
  - Streamlit user interface

### Contributions Welcome

Community contributions are welcome! Here's how to contribute:

1. **Fork** the repository
2. **Create** a branch for your feature (`git checkout -b feature/new-feature`)
3. **Commit** your changes (`git commit -am 'Add new feature'`)
4. **Push** to the branch (`git push origin feature/new-feature`)
5. **Open** a Pull Request

### Types of Contributions Wanted

- 🐛 Bug fixes
- ✨ New features
- 📚 Documentation improvements
- 🧪 Tests and validation
- 🌐 Translations
- 🎨 UI improvements

## Citation

If you use this project or refer to it in your own work, please cite the associated paper:

> El Azzouzi, H., Ettalbi, K., & Rochdi, O. (2026). *Development of an Intelligent Conversational Assistant for Semantic Exploration of Scientific Articles*. Zenodo. https://doi.org/10.5281/zenodo.22033431

BibTeX:

```bibtex
@misc{elazzouzi2026scopuschatbot,
  author       = {El Azzouzi, Hassan and Ettalbi, Kabira and Rochdi, Oumayma},
  title        = {Development of an Intelligent Conversational Assistant for Semantic Exploration of Scientific Articles},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.22033431},
  url          = {https://doi.org/10.5281/zenodo.22033431}
}
```

See also [`CITATION.cff`](./CITATION.cff), which GitHub uses to generate a "Cite this repository" button automatically.

## License

This project is licensed under the **MIT License**. See the [LICENSE](https://github.com/ElazzouziHassan/scopus_chatbot/blob/main/LICENSE) file for details.

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

## References and Acknowledgments

### Technologies Used

- **[arXiv API](https://arxiv.org/help/api)** — source of scientific data
- **[Sentence Transformers](https://www.sbert.net/)** — semantic embedding generation
- **[FAISS](https://faiss.ai/)** — fast vector indexing and search
- **[Streamlit](https://streamlit.io/)** — web interface framework
- **[Plotly](https://plotly.com/)** — interactive visualizations
- **[Pandas](https://pandas.pydata.org/)** — data manipulation

### Scientific Bibliography

1. Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. *EMNLP 2019*.
2. Johnson, J., Douze, M., & Jégou, H. (2019). Billion-scale similarity search with GPUs. *IEEE Transactions on Big Data*.
3. Karpukhin, V., et al. (2020). Dense Passage Retrieval for Open-Domain Question Answering. *EMNLP 2020*.

### Special Thanks

- **arXiv.org** for open access to scientific publications
- **Hugging Face** for pretrained transformer models
- **The open-source community** for the tools and libraries used

---

## Quick Start

```bash
# Quick installation
git clone https://github.com/ElazzouziHassan/scopus_chatbot.git
cd scopus_chatbot
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Build the index (may take 30-60 minutes)
python data/scripts/arxiv_extractor.py
python data/scripts/data_cleaner.py --auto
python data/scripts/semantic_indexer.py --auto

# Launch the application
streamlit run app/pro_chatbot.py
```

**Your arXiv semantic search chatbot is now ready! 🎉**

---

*For questions or support, feel free to open an issue on GitHub or reach out directly.*