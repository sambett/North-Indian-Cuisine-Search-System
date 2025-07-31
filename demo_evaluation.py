"""
Demo: Advanced RAG Evaluation & Hindi Translation
Run this to see your enhanced system in action
"""

import time
import json
from rag_enhancer import SmartRAGEnhancer

def demo_evaluation_system():
    """Demonstrate the evaluation capabilities"""
    
    print("🧠 RAG System Enhancement Demo")
    print("=" * 50)
    
    # Initialize enhancer
    enhancer = SmartRAGEnhancer()
    
    # Test Hindi translation
    print("\n1. 📝 Hindi Translation Test")
    print("-" * 30)
    
    hindi_recipes = [
        "टमाटर पुलियोगरे रेसिपी - Spicy Tomato Rice (Recipe In Hindi)",
        "हल्दी और जीरा के साथ दाल रेसिपी",
        "Dal Makhani with Butter and Cream"  # Already English
    ]
    
    for recipe in hindi_recipes:
        translated = enhancer.translate_hindi_text(recipe)
        print(f"Original:   {recipe}")
        print(f"Translated: {translated}")
        print()
    
    # Test evaluation metrics
    print("2. 📊 Search Quality Evaluation")
    print("-" * 30)
    
    # Simulate search results
    mock_results = {
        'documents': [["Dal Makhani is a rich North Indian curry made with black lentils, butter, and cream"]],
        'metadatas': [[{
            'recipe_name': 'Dal Makhani Recipe',
            'cuisine': 'North Indian',
            'course': 'Main Course',
            'ingredient_count': 8
        }]],
        'distances': [[0.15]]  # Low distance = high confidence
    }
    
    query = "What ingredients are in Dal Makhani?"
    response_time = 0.8  # 800ms
    
    evaluation = enhancer.evaluate_search_results(query, mock_results, response_time)
    
    print(f"Query: {query}")
    print(f"Quality Score: {evaluation['quality_score']}/100")
    print(f"Confidence: {evaluation['avg_confidence']}%")
    print(f"Response Time: {evaluation['response_time']}ms")
    print(f"Assessment: {evaluation['summary']}")
    
    # Test result enhancement
    print("\n3. ✨ Result Enhancement")
    print("-" * 30)
    
    enhanced = enhancer.enhance_search_results(mock_results, query)
    
    for result in enhanced:
        print(f"Recipe: {result['metadata']['recipe_name']}")
        print(f"Confidence: {result['confidence']:.1%}")
        print(f"Match Reason: {result['match_reason']}")
        print(f"Quality: {', '.join(result['quality_indicators'])}")
        print()
    
    print("4. 🎯 Key Improvements Summary")
    print("-" * 30)
    print("✅ Hindi recipe names automatically translated")
    print("✅ Confidence scores with color coding")
    print("✅ Match explanations for transparency")
    print("✅ Quality indicators for each result")
    print("✅ Performance metrics tracking")
    print("✅ Response time optimization analysis")
    print("✅ Search pattern analytics")
    print()
    
    print("🚀 Your RAG system is now enterprise-grade!")

if __name__ == "__main__":
    demo_evaluation_system()
