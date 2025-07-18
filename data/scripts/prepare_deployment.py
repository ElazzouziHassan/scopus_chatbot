#!/usr/bin/env python3
"""
Prepare files for deployment by splitting large files and creating compressed versions
"""

import json
import gzip
import os
import shutil
from typing import Dict, List

def compress_large_files():
    """Compress large files for GitHub releases"""
    
    search_index_dir = "data/search_index"
    release_dir = "release_files"
    
    # Create release directory
    os.makedirs(release_dir, exist_ok=True)
    
    # Compress papers_data.json
    papers_file = os.path.join(search_index_dir, "papers_data.json")
    if os.path.exists(papers_file):
        print(f"Compressing {papers_file}...")
        
        with open(papers_file, 'rb') as f_in:
            with gzip.open(f"{release_dir}/papers_data.json.gz", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Check compression ratio
        original_size = os.path.getsize(papers_file) / (1024*1024)  # MB
        compressed_size = os.path.getsize(f"{release_dir}/papers_data.json.gz") / (1024*1024)  # MB
        
        print(f"Original: {original_size:.1f}MB")
        print(f"Compressed: {compressed_size:.1f}MB")
        print(f"Compression ratio: {compressed_size/original_size:.1%}")
    
    # Copy other index files
    for file in ["metadata.json", "faiss_index.bin", "embeddings.npy"]:
        src = os.path.join(search_index_dir, file)
        dst = os.path.join(release_dir, file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            size_mb = os.path.getsize(src) / (1024*1024)
            print(f"Copied {file}: {size_mb:.1f}MB")

def create_sample_data():
    """Create a small sample dataset for immediate deployment"""
    
    papers_file = "data/search_index/papers_data.json"
    sample_file = "data/sample_papers.json"
    
    if os.path.exists(papers_file):
        print("Creating sample dataset...")
        
        with open(papers_file, 'r', encoding='utf-8') as f:
            all_papers = json.load(f)
        
        # Take a representative sample (50 papers from different categories)
        sample_papers = []
        categories_seen = set()
        
        for paper in all_papers:
            if len(sample_papers) >= 50:
                break
                
            # Get primary category
            primary_cat = paper.get('categories', {}).get('primary', '')
            
            # Include if we haven't seen this category or if we have < 50 papers
            if primary_cat not in categories_seen or len(sample_papers) < 20:
                sample_papers.append(paper)
                if primary_cat:
                    categories_seen.add(primary_cat)
        
        # Save sample
        with open(sample_file, 'w', encoding='utf-8') as f:
            json.dump(sample_papers, f, ensure_ascii=False, indent=2)
        
        sample_size = os.path.getsize(sample_file) / (1024*1024)
        print(f"Created sample with {len(sample_papers)} papers ({sample_size:.1f}MB)")
        print(f"Categories covered: {len(categories_seen)}")

if __name__ == "__main__":
    print("=== Preparing Deployment Files ===")
    compress_large_files()
    create_sample_data()
    print("=== Done ===")
