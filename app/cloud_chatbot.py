#!/usr/bin/env python3
"""
Cloud-Compatible arXiv Chatbot for Streamlit Deployment

This version works without pre-built indexes and handles data loading gracefully.
"""

import streamlit as st
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Any
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from collections import Counter
import time

# Import our cloud data manager
from cloud_data_manager import get_cloud_chatbot

def render_chat_page(chatbot):
    """Render the main chat page with cloud compatibility"""
    st.title("🔬 arXiv Scientific Papers Chatbot")
    
    # Show data source information
    stats = chatbot.get_paper_statistics()
    data_source = stats.get('data_source', 'unknown')
    search_method = stats.get('search_method', 'keyword')
    
    # Data source indicator
    if data_source == 'demo':
        st.info("📋 **Demo Mode**: Using sample data for demonstration. Full dataset available in production.")
    else:
        st.success(f"📊 **Active**: {stats.get('total_papers', 0)} papers loaded with {search_method} search")
    
    st.markdown("Ask me anything about scientific papers from arXiv!")
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        welcome_message = """Hello! I'm your arXiv papers assistant. 

🎯 **What I can help you with:**
- **Search** for research papers on any topic
- **Analyze** trends and research patterns  
- **Discover** key researchers and institutions
- **Explore** connections between different fields

💡 **Try asking:**
- "What are the latest developments in quantum computing?"
- "Show me research on machine learning applications"
- "Find papers about natural language processing"
- "What's new in computer vision?"

Let's explore the world of scientific research together! 🚀"""
        
        st.session_state.messages = [
            {"role": "assistant", "content": welcome_message}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about scientific papers..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            with st.spinner("🔍 Searching research papers..."):
                # Search for papers
                search_results = chatbot.search_papers(prompt, k=10)
                
                # Generate response
                full_response = chatbot.generate_response(prompt, search_results)
            
            # Stream the response
            streamed_response = ""
            for char in full_response:
                streamed_response += char
                response_placeholder.markdown(streamed_response + "▌")
                time.sleep(0.01)
            
            # Final response without cursor
            response_placeholder.markdown(full_response)
            
            # Display detailed results if found
            if search_results:
                st.subheader("📄 Detailed Results")
                
                for i, paper in enumerate(search_results, 1):
                    with st.expander(f"{i}. {paper['title'][:80]}..." + ("" if len(paper['title']) <= 80 else "...")):
                        col_a, col_b = st.columns([3, 1])
                        
                        with col_a:
                            st.write("**Abstract:**")
                            summary = paper['summary']
                            if len(summary) > 400:
                                st.write(summary[:400] + "...")
                                if st.button(f"Show full abstract", key=f"full_{i}"):
                                    st.write(summary)
                            else:
                                st.write(summary)
                            
                            st.write("**Authors:**")
                            authors = paper.get('authors', {}).get('names', [])
                            st.write(', '.join(authors))
                            
                            if paper.get('categories', {}).get('terms'):
                                st.write("**Categories:**")
                                st.write(', '.join(paper['categories']['terms']))
                            
                            if paper.get('keywords'):
                                st.write("**Keywords:**")
                                keywords = paper['keywords'][:8]
                                st.write(', '.join(keywords))
                        
                        with col_b:
                            relevance = paper.get('similarity_score', 0)
                            st.metric("🎯 Relevance", f"{relevance:.1%}")
                            
                            if paper.get('publication_year'):
                                st.metric("📅 Year", paper['publication_year'])
                            
                            author_count = len(paper.get('authors', {}).get('names', []))
                            st.metric("👥 Authors", author_count)
                            
                            if paper.get('pdf_url'):
                                st.link_button("📄 View PDF", paper['pdf_url'])
                            
                            if paper.get('abstract_url'):
                                st.link_button("🔗 arXiv Page", paper['abstract_url'])

        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

def render_statistics_page(chatbot):
    """Render the dataset statistics page"""
    st.title("📊 Dataset Statistics")
    
    stats = chatbot.get_paper_statistics()
    
    if stats:
        # Header with data source info
        data_source = stats.get('data_source', 'unknown')
        search_method = stats.get('search_method', 'keyword')
        
        st.markdown(f"""
        **Data Source:** {data_source.title()} | **Search Method:** {search_method.title()}
        """)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📚 Total Papers", f"{stats['total_papers']:,}")
        
        with col2:
            st.metric("👥 Unique Authors", f"{stats['total_authors']:,}")
        
        with col3:
            st.metric("🆕 Recent Papers", f"{stats['recent_papers']:,}")
        
        with col4:
            st.metric("📈 Avg Authors/Paper", f"{stats['avg_authors_per_paper']:.1f}")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Category distribution
            if stats['categories']:
                st.subheader("🏷️ Research Categories")
                cat_df = pd.DataFrame(
                    list(stats['categories'].items()),
                    columns=['Category', 'Papers']
                )
                fig = px.bar(
                    cat_df, 
                    x='Papers', 
                    y='Category', 
                    orientation='h',
                    title="Papers by Category",
                    color='Papers',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Publication timeline
            if stats['years']:
                st.subheader("📅 Publication Timeline")
                year_df = pd.DataFrame(
                    list(stats['years'].items()),
                    columns=['Year', 'Papers']
                )
                year_df['Year'] = year_df['Year'].astype(int)
                year_df = year_df.sort_values('Year')
                
                fig = px.line(
                    year_df, 
                    x='Year', 
                    y='Papers', 
                    markers=True,
                    title="Publications Over Time"
                )
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        # Additional insights
        st.markdown("---")
        st.subheader("📈 Research Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            recent_pct = (stats['recent_papers'] / stats['total_papers'] * 100) if stats['total_papers'] > 0 else 0
            st.info(f"**Research Velocity**: {recent_pct:.1f}% of papers are from 2020+")
        
        with col2:
            st.info(f"**Collaboration Index**: Average of {stats['avg_authors_per_paper']:.1f} authors indicates {'high' if stats['avg_authors_per_paper'] > 2 else 'moderate'} collaboration")
        
        with col3:
            st.info(f"**Research Diversity**: {len(stats['categories'])} different research categories")
    
    else:
        st.error("No statistics available. Please check data loading.")

def main():
    """Main Streamlit application with cloud compatibility"""
    st.set_page_config(
        page_title="arXiv Scientific Papers Chatbot",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize page state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'chat'
    
    # Sidebar navigation
    st.sidebar.header("🧭 Navigation")
    
    # Navigation buttons
    if st.sidebar.button("💬 Chat Assistant", use_container_width=True, 
                        type="primary" if st.session_state.current_page == 'chat' else "secondary"):
        st.session_state.current_page = 'chat'
        st.rerun()
    
    if st.sidebar.button("📊 Dataset Statistics", use_container_width=True,
                        type="primary" if st.session_state.current_page == 'stats' else "secondary"):
        st.session_state.current_page = 'stats'
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Initialize chatbot with error handling
    try:
        chatbot = get_cloud_chatbot()
        
        if not chatbot.is_ready:
            st.sidebar.error("⚠️ Chatbot initialization incomplete")
            st.sidebar.info("Using fallback demo mode")
        else:
            st.sidebar.success("✅ Chatbot ready")
            stats = chatbot.get_paper_statistics()
            st.sidebar.info(f"📊 {stats.get('total_papers', 0)} papers loaded")
            
    except Exception as e:
        st.sidebar.error(f"❌ Initialization error: {e}")
        st.error("Failed to initialize chatbot. Please refresh the page.")
        return
    
    # Quick search section
    if st.session_state.current_page == 'chat':
        st.sidebar.markdown("---")
        st.sidebar.header("🚀 Quick Searches")
        
        quick_searches = [
            "quantum computing",
            "machine learning", 
            "computer vision",
            "natural language processing",
            "reinforcement learning",
            "blockchain technology",
            "neural networks",
            "artificial intelligence"
        ]
        
        for search_term in quick_searches:
            if st.sidebar.button(search_term, key=f"quick_{search_term}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": search_term})
                st.rerun()
        
        # Search tips
        st.sidebar.markdown("---")
        st.sidebar.subheader("💡 Search Tips")
        st.sidebar.markdown("""
        **Effective strategies:**
        - Use specific technical terms
        - Try different phrasings  
        - Combine multiple concepts
        - Include methodology terms
        - Specify application domains
        """)
    
    # Render appropriate page
    if st.session_state.current_page == 'chat':
        render_chat_page(chatbot)
    elif st.session_state.current_page == 'stats':
        render_statistics_page(chatbot)
    
    # Footer with system info
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🔬 System Info**")
        if chatbot.is_ready:
            stats = chatbot.get_paper_statistics()
            st.markdown(f"Papers: {stats.get('total_papers', 0):,}")
            st.markdown(f"Search: {stats.get('search_method', 'keyword').title()}")
        
    with col2:
        st.markdown("**🧠 AI Technology**")
        st.markdown("Embeddings: Sentence Transformers")
        st.markdown("Fallback: Keyword Search")
    
    with col3:
        st.markdown("**☁️ Cloud Deployment**")
        st.markdown("Platform: Streamlit Cloud")
        st.markdown("Status: Production Ready")

if __name__ == "__main__":
    main()
