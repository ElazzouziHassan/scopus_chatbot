#!/bin/bash
# Deployment script for Streamlit Cloud

echo "🚀 Preparing for Streamlit Cloud deployment..."

# 1. Create sample data
echo "📊 Creating sample dataset..."
python scripts/prepare_deployment.py

# 2. Update .gitignore to exclude large files
echo "📝 Updating .gitignore..."
cat >> .gitignore << EOF

# Large data files (use GitHub Releases instead)
data/search_index/papers_data.json
data/search_index/embeddings.npy
data/search_index/faiss_index.bin
data/data_source/*.json
data/processed/*.json

# Keep small files
!data/sample_papers.json
!data/search_index/metadata.json
EOF

# 3. Add files to git
echo "📁 Adding files to git..."
git add data/sample_papers.json
git add data/search_index/metadata.json
git add app/
git add requirements.txt
git add .streamlit/
git add README.md

# 4. Commit
echo "💾 Committing changes..."
git commit -m "Add Streamlit Cloud compatible chatbot with sample data

- Added cloud-compatible data manager
- Created sample dataset (50 papers, <5MB)
- Excluded large files from git
- Ready for immediate deployment"

# 5. Push
echo "🌐 Pushing to GitHub..."
git push origin main

echo "✅ Ready for Streamlit Cloud deployment!"
echo "📋 Deploy settings:"
echo "   Repository: $(git remote get-url origin)"
echo "   Branch: main"
echo "   Main file: app/cloud_chatbot.py"
