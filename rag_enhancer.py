"""
Quick Integration: Add this to your streamlit_rag_app_fixed.py
Smart RAG Evaluation & Hindi Translation Module
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import re
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Add this class to your streamlit app
class SmartRAGEnhancer:
    def __init__(self):
        # Hindi ingredient translations
        self.hindi_to_english = {
            'हल्दी': 'turmeric', 'जीरा': 'cumin', 'धनिया': 'coriander',
            'अदरक': 'ginger', 'लहसुन': 'garlic', 'प्याज': 'onion',
            'टमाटर': 'tomato', 'मिर्च': 'chili', 'नमक': 'salt',
            'तेल': 'oil', 'घी': 'ghee', 'दूध': 'milk', 'दही': 'yogurt',
            'पनीर': 'paneer', 'आलू': 'potato', 'चावल': 'rice',
            'आटा': 'flour', 'दाल': 'lentils', 'रेसिपी': 'recipe'
        }
        
        # Performance tracking
        if 'rag_metrics' not in st.session_state:
            st.session_state.rag_metrics = {
                'queries': [], 'response_times': [], 'confidences': []
            }
    
    def translate_hindi_text(self, text):
        """Smart Hindi to English translation"""
        if not text:
            return text
            
        # Check for Hindi characters
        if not re.search(r'[\u0900-\u097F]', text):
            return text
        
        translated = text
        for hindi, english in self.hindi_to_english.items():
            translated = translated.replace(hindi, english)
        
        # Clean common patterns
        translated = re.sub(r'रेसिपी.*?-\s*', '', translated)  # Remove "रेसिपी - "
        translated = re.sub(r'\(Recipe In Hindi\)', '', translated, flags=re.IGNORECASE)
        
        return translated.strip()
    
    def evaluate_search_results(self, query, results, response_time):
        """Professional search evaluation"""
        if not results:
            return {'quality_score': 0, 'summary': 'No results found'}
        
        # Extract confidence scores
        confidences = []
        for result_group in results['documents']:
            for i, distance in enumerate(results.get('distances', [[]])[0]):
                confidence = 1 - distance  # Convert distance to confidence
                confidences.append(confidence)
        
        # Calculate metrics
        avg_confidence = np.mean(confidences) if confidences else 0
        quality_score = min(avg_confidence * 100, 100)
        
        # Performance assessment
        time_score = 100 if response_time < 1 else max(50, 100 - (response_time - 1) * 20)
        overall_score = (quality_score + time_score) / 2
        
        # Generate summary
        if overall_score >= 80:
            summary = "🎯 Excellent: High-quality, fast results"
        elif overall_score >= 60:
            summary = "✅ Good: Solid performance with relevant results"
        else:
            summary = "⚠️ Fair: Results found but could be improved"
        
        # Store metrics
        st.session_state.rag_metrics['queries'].append(query)
        st.session_state.rag_metrics['response_times'].append(response_time)
        st.session_state.rag_metrics['confidences'].append(avg_confidence)
        
        return {
            'quality_score': round(overall_score, 1),
            'avg_confidence': round(avg_confidence * 100, 1),
            'response_time': round(response_time * 1000, 1),  # ms
            'summary': summary,
            'confidence_scores': confidences
        }
    
    def enhance_search_results(self, results, query):
        """Enhance results with translations and smart features"""
        enhanced_results = []
        
        if not results['documents'] or not results['documents'][0]:
            return enhanced_results
        
        documents = results['documents'][0]
        metadatas = results['metadatas'][0] if results.get('metadatas') else [{}] * len(documents)
        distances = results['distances'][0] if results.get('distances') else [0] * len(documents)
        
        for i, (doc, metadata, distance) in enumerate(zip(documents, metadatas, distances)):
            enhanced = {
                'content': doc,
                'metadata': metadata,
                'confidence': 1 - distance,
                'rank': i + 1
            }
            
            # Translate Hindi content
            recipe_name = metadata.get('recipe_name', '')
            if recipe_name:
                translated_name = self.translate_hindi_text(recipe_name)
                enhanced['translated_name'] = translated_name
                enhanced['is_translated'] = translated_name != recipe_name
            
            # Add smart explanations
            enhanced['match_reason'] = self._generate_match_explanation(doc, metadata, query)
            enhanced['quality_indicators'] = self._assess_quality(metadata, enhanced['confidence'])
            
            enhanced_results.append(enhanced)
        
        return enhanced_results
    
    def _generate_match_explanation(self, doc, metadata, query):
        """Generate why this result matched"""
        query_words = query.lower().split()
        recipe_name = metadata.get('recipe_name', '').lower()
        
        reasons = []
        for word in query_words[:2]:  # Check first 2 words
            if word in recipe_name:
                reasons.append(f"Recipe contains '{word}'")
            elif word in doc.lower():
                reasons.append(f"Ingredients include '{word}'")
        
        if not reasons:
            reasons.append("Semantic similarity with recipe content")
        
        return " • ".join(reasons)
    
    def _assess_quality(self, metadata, confidence):
        """Assess result quality"""
        indicators = []
        
        if confidence > 0.8:
            indicators.append("🎯 High confidence match")
        elif confidence > 0.6:
            indicators.append("✅ Good match")
        
        if metadata.get('cuisine'):
            indicators.append(f"🌍 {metadata['cuisine']} cuisine")
        
        if metadata.get('ingredient_count', 0) > 5:
            indicators.append("📋 Detailed ingredients")
        
        return indicators
    
    def show_performance_dashboard(self):
        """Display performance metrics dashboard"""
        st.markdown("## 📊 RAG System Performance Dashboard")
        
        metrics = st.session_state.rag_metrics
        
        if not metrics['queries']:
            st.info("🔍 No search data yet. Try some searches to see metrics!")
            return
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Searches", len(metrics['queries']))
        
        with col2:
            avg_time = np.mean(metrics['response_times']) * 1000
            st.metric("Avg Response Time", f"{avg_time:.0f}ms")
        
        with col3:
            avg_conf = np.mean(metrics['confidences']) * 100
            st.metric("Avg Confidence", f"{avg_conf:.0f}%")
        
        with col4:
            health_score = 100 if avg_time < 1000 and avg_conf > 70 else 80
            st.metric("System Health", f"{'🟢' if health_score > 85 else '🟡'} {health_score}%")
        
        # Performance Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Response Time Trend
            if len(metrics['response_times']) > 1:
                fig = px.line(
                    y=[t*1000 for t in metrics['response_times']],
                    title="Response Time Trend (ms)",
                    labels={'x': 'Search Number', 'y': 'Response Time (ms)'}
                )
                fig.update_traces(line_color='#FF6B35')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Confidence Distribution
            fig = px.histogram(
                x=[c*100 for c in metrics['confidences']],
                nbins=10,
                title="Confidence Score Distribution",
                labels={'x': 'Confidence %', 'y': 'Count'}
            )
            fig.update_traces(marker_color='#FF6B35')
            st.plotly_chart(fig, use_container_width=True)
        
        # Popular Queries
        if len(metrics['queries']) > 0:
            st.markdown("### 🔍 Recent Searches")
            recent_queries = metrics['queries'][-10:]  # Last 10
            query_df = pd.DataFrame({
                'Query': recent_queries,
                'Response Time (ms)': [t*1000 for t in metrics['response_times'][-10:]],
                'Confidence %': [c*100 for c in metrics['confidences'][-10:]]
            })
            st.dataframe(query_df, use_container_width=True)

# Add this to your main search function
def enhanced_display_search_results(collection, query, model, num_results, min_confidence, enhancer):
    """Enhanced search with evaluation and translation"""
    
    with st.spinner("🔍 Searching with AI evaluation..."):
        start_time = time.time()
        
        # Perform search
        results = collection.query(
            query_texts=[query],
            n_results=num_results,
            include=['documents', 'metadatas', 'distances']
        )
        
        response_time = time.time() - start_time
        
        # Evaluate search quality
        evaluation = enhancer.evaluate_search_results(query, results, response_time)
        
        # Enhance results
        enhanced_results = enhancer.enhance_search_results(results, query)
        
        # Filter by confidence
        filtered_results = [r for r in enhanced_results if r['confidence'] >= min_confidence]
        
        if not filtered_results:
            st.warning(f"No results found with confidence ≥ {min_confidence:.1%}")
            return
        
        # Show evaluation metrics
        st.markdown("### 📊 Search Quality Assessment")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            score = evaluation['quality_score']
            color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
            st.metric("Quality Score", f"{color} {score}/100")
        
        with col2:
            st.metric("Avg Confidence", f"{evaluation['avg_confidence']:.0f}%")
        
        with col3:
            st.metric("Response Time", f"{evaluation['response_time']:.0f}ms")
        
        with col4:
            st.metric("Results Found", len(filtered_results))
        
        st.info(evaluation['summary'])
        
        # Display results
        st.markdown(f"### 🎯 Search Results for '{query}'")
        
        for i, result in enumerate(filtered_results):
            confidence = result['confidence']
            
            # Confidence styling
            if confidence >= 0.8:
                conf_color, conf_emoji = "#28a745", "🟢"
            elif confidence >= 0.6:
                conf_color, conf_emoji = "#ffc107", "🟡"
            else:
                conf_color, conf_emoji = "#dc3545", "🔴"
            
            with st.container():
                st.markdown(f"""
                <div style="border-left: 4px solid {conf_color}; padding: 1rem; margin: 1rem 0; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h4>{conf_emoji} Result {i+1} - {confidence:.1%} Confidence</h4>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Recipe name with translation
                    recipe_name = result['metadata'].get('recipe_name', 'Unknown Recipe')
                    if result.get('is_translated'):
                        st.markdown(f"**🍛 Recipe:** {result['translated_name']}")
                        with st.expander("View Original Name"):
                            st.write(f"Original: {recipe_name}")
                    else:
                        st.markdown(f"**🍛 Recipe:** {recipe_name}")
                    
                    # Content
                    st.markdown("**📝 Content:**")
                    content = result['content'][:300] + "..." if len(result['content']) > 300 else result['content']
                    st.write(content)
                    
                    # Match explanation
                    st.info(f"🎯 **Why this matched:** {result['match_reason']}")
                
                with col2:
                    # Metadata
                    metadata = result['metadata']
                    if metadata.get('cuisine'):
                        st.write(f"🌍 **Cuisine:** {metadata['cuisine']}")
                    if metadata.get('course'):
                        st.write(f"🍴 **Course:** {metadata['course']}")
                    if metadata.get('ingredient_count'):
                        st.write(f"📊 **Ingredients:** {metadata['ingredient_count']}")
                    
                    # Quality indicators
                    if result['quality_indicators']:
                        st.markdown("**✨ Quality:**")
                        for indicator in result['quality_indicators']:
                            st.caption(indicator)
                
                st.markdown("---")

# Integration Instructions:
"""
TO INTEGRATE INTO YOUR EXISTING APP:

1. Add this import at the top of streamlit_rag_app_fixed.py:
   from rag_enhancer import SmartRAGEnhancer, enhanced_display_search_results

2. Initialize the enhancer in your main function:
   if 'enhancer' not in st.session_state:
       st.session_state.enhancer = SmartRAGEnhancer()

3. Replace your display_search_results function call with:
   enhanced_display_search_results(collection, query, model, num_results, min_confidence, st.session_state.enhancer)

4. Add performance dashboard to your sidebar:
   with st.sidebar:
       if st.button("📊 Performance Dashboard"):
           st.session_state.enhancer.show_performance_dashboard()
"""
