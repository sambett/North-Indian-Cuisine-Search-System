"""
Indian Food RAG Data Processor - CLEAN VERSION
Processes only high-quality Kaggle Indian Food Dataset
Focuses on ingredient identification for North Indian cuisine

DECISION LOG:
- Date: June 23, 2025
- Decision: Use only Kaggle dataset (3,406 recipes)
- Reason: INDB dataset structure incompatible (only yielded 20 usable recipes)
- Result: Clean, focused dataset with 4,368 ingredients from verified sources
"""
import pandas as pd
import json
import re
import os
from typing import Dict, List, Set

class CleanIndianFoodProcessor:
    def __init__(self, data_folder: str):
        self.data_folder = data_folder
        self.kaggle_csv_path = os.path.join(data_folder, "archive", "IndianFoodDatasetCSV.csv")
        
        # North Indian cuisine filters - comprehensive list
        self.north_indian_cuisines = {
            'Indian', 'North Indian', 'Punjabi', 'Delhi', 'Haryana', 
            'Chandigarh', 'Himachal Pradesh', 'Rajasthani', 'Mughlai'
        }
        
        # North Indian dish indicators - expanded list
        self.priority_dishes = {
            'chole', 'bhature', 'dal', 'makhani', 'butter chicken', 'paneer',
            'naan', 'roti', 'paratha', 'biryani', 'korma', 'tandoori',
            'aloo', 'gobi', 'rajma', 'kadhi', 'sarson', 'makki', 'tikka',
            'samosa', 'pakora', 'kulcha', 'lassi', 'raita', 'kebab', 'masala'
        }

    def clean_ingredient_text(self, ingredient_text: str) -> List[str]:
        """
        Clean and extract individual ingredients from comma-separated text
        
        Input: "2 cups rice, 1 tsp salt, ghee - as required"
        Output: ["rice", "salt", "ghee"]
        """
        if not ingredient_text or pd.isna(ingredient_text):
            return []
        
        # Remove quantities and measurements (numbers + units)
        cleaned = re.sub(r'\d+\s*(cups?|tbsp|tsp|tablespoons?|teaspoons?|grams?|kg|lbs?|ml|liters?|pieces?)', '', ingredient_text)
        
        # Split by commas and clean each ingredient
        ingredients = []
        for item in cleaned.split(','):
            # Remove everything after hyphen (descriptions like "- chopped", "- as required")
            clean_item = re.sub(r'\s*-\s*.*$', '', item.strip())
            # Remove parenthetical descriptions like "(chopped)" or "(Bitter Gourd)"
            clean_item = re.sub(r'\s*\([^)]*\)', '', clean_item)
            # Remove common cooking instructions
            clean_item = re.sub(r'\s*(to taste|as required|as needed|chopped|sliced|diced)', '', clean_item, flags=re.IGNORECASE)
            # Remove extra whitespace
            clean_item = clean_item.strip()
            
            # Only keep meaningful ingredients (longer than 2 chars, not just numbers)
            if clean_item and len(clean_item) > 2 and not clean_item.isdigit():
                ingredients.append(clean_item)
        
        return ingredients

    def is_north_indian_dish(self, recipe_name: str, cuisine: str) -> bool:
        """
        Determine if a dish belongs to North Indian cuisine
        
        Logic:
        1. Check cuisine field for North Indian indicators
        2. Check recipe name for characteristic dish names
        """
        # Check cuisine column first
        if cuisine and any(nc.lower() in cuisine.lower() for nc in self.north_indian_cuisines):
            return True
        
        # Check recipe name for North Indian dish indicators
        recipe_lower = recipe_name.lower()
        return any(dish in recipe_lower for dish in self.priority_dishes)

    def process_kaggle_dataset(self) -> List[Dict]:
        """
        Process Kaggle Indian Food Dataset CSV file
        
        Source: 6,871 total recipes from Archana's Kitchen
        Filter: North Indian cuisine only
        Output: Clean recipe data with ingredient lists
        """
        print("📊 Processing Kaggle Indian Food Dataset...")
        print(f"   Source: {self.kaggle_csv_path}")
        
        processed_recipes = []
        total_processed = 0
        
        try:
            # Process in chunks to handle large file efficiently
            chunk_size = 1000
            
            for chunk_num, chunk in enumerate(pd.read_csv(self.kaggle_csv_path, chunksize=chunk_size)):
                print(f"   Processing chunk {chunk_num + 1}...")
                
                for _, row in chunk.iterrows():
                    total_processed += 1
                    
                    # Extract data from row
                    recipe_name = str(row.get('RecipeName', '')).strip()
                    cuisine = str(row.get('Cuisine', '')).strip()
                    course = str(row.get('Course', '')).strip()
                    ingredients_text = str(row.get('Ingredients', '')).strip()
                    
                    # Skip if missing essential data
                    if not recipe_name or not ingredients_text:
                        continue
                    
                    # Filter for North Indian dishes only
                    if not self.is_north_indian_dish(recipe_name, cuisine):
                        continue
                    
                    # Clean and extract ingredients
                    ingredients = self.clean_ingredient_text(ingredients_text)
                    
                    # Only keep recipes with meaningful ingredient lists (3+ ingredients)
                    if len(ingredients) >= 3:
                        recipe_data = {
                            'id': f"recipe_{len(processed_recipes) + 1:04d}",
                            'name': recipe_name,
                            'cuisine': cuisine if cuisine and cuisine != 'nan' else 'North Indian',
                            'course': course if course and course != 'nan' else 'unknown',
                            'ingredients': ingredients,
                            'ingredient_count': len(ingredients),
                            'source': 'kaggle_archanas_kitchen',
                            'region': 'north_india',
                            'original_ingredients_text': ingredients_text  # Keep for reference
                        }
                        processed_recipes.append(recipe_data)
            
            print(f"✅ Successfully processed:")
            print(f"   • Total rows examined: {total_processed}")
            print(f"   • North Indian recipes found: {len(processed_recipes)}")
            print(f"   • Success rate: {len(processed_recipes)/total_processed*100:.1f}%")
            
            return processed_recipes
            
        except Exception as e:
            print(f"❌ Error processing Kaggle dataset: {e}")
            return []

    def create_ingredient_analysis(self, all_recipes: List[Dict]) -> Dict:
        """
        Create comprehensive ingredient analysis for RAG optimization
        """
        print("📈 Creating ingredient analysis...")
        
        ingredient_freq = {}
        ingredient_to_recipes = {}
        
        for recipe in all_recipes:
            for ingredient in recipe['ingredients']:
                # Normalize ingredient name (lowercase, strip)
                normalized = ingredient.lower().strip()
                
                # Count frequency across all recipes
                ingredient_freq[normalized] = ingredient_freq.get(normalized, 0) + 1
                
                # Map ingredient to recipe IDs
                if normalized not in ingredient_to_recipes:
                    ingredient_to_recipes[normalized] = []
                ingredient_to_recipes[normalized].append(recipe['id'])
        
        # Sort ingredients by frequency
        sorted_ingredients = sorted(ingredient_freq.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'frequency_map': ingredient_freq,
            'recipe_mapping': ingredient_to_recipes,
            'total_unique_ingredients': len(ingredient_freq),
            'most_common_50': sorted_ingredients[:50],
            'statistics': {
                'total_ingredients': sum(ingredient_freq.values()),
                'average_per_recipe': sum(ingredient_freq.values()) / len(all_recipes),
                'ingredients_used_once': len([i for i in ingredient_freq.values() if i == 1]),
                'ingredients_used_10plus': len([i for i in ingredient_freq.values() if i >= 10])
            }
        }

    def generate_rag_documents(self, all_recipes: List[Dict]) -> List[Dict]:
        """
        Generate optimized documents for RAG vector search
        
        Creates two types of documents:
        1. Recipe documents: Full recipe with all ingredients
        2. Ingredient documents: Individual ingredient usage patterns
        """
        print("🔄 Generating RAG documents...")
        
        rag_documents = []
        
        for recipe in all_recipes:
            ingredients_text = ", ".join(recipe['ingredients'])
            
            # 1. Main recipe document
            content = f"Recipe: {recipe['name']} is a {recipe['cuisine']} {recipe['course']} dish from North Indian cuisine. "
            content += f"This recipe uses {recipe['ingredient_count']} main ingredients: {ingredients_text}. "
            content += f"This dish is typically served as a {recipe['course']} and represents authentic North Indian cooking."
            
            recipe_doc = {
                'id': recipe['id'],
                'type': 'recipe',
                'content': content,
                'metadata': {
                    'recipe_name': recipe['name'],
                    'cuisine': recipe['cuisine'],
                    'course': recipe['course'],
                    'region': recipe['region'],
                    'ingredient_count': recipe['ingredient_count'],
                    'all_ingredients': ingredients_text,
                    'source': recipe['source']
                }
            }
            rag_documents.append(recipe_doc)
            
            # 2. Individual ingredient documents for better search granularity
            for i, ingredient in enumerate(recipe['ingredients']):
                ingredient_doc = {
                    'id': f"{recipe['id']}_ing_{i+1:02d}",
                    'type': 'ingredient_usage',
                    'content': f"Ingredient: {ingredient} is used in {recipe['name']}, a popular {recipe['cuisine']} dish. This ingredient is essential for authentic North Indian flavor and is commonly found in {recipe['course']} preparations.",
                    'metadata': {
                        'ingredient_name': ingredient,
                        'recipe_name': recipe['name'],
                        'cuisine': recipe['cuisine'],
                        'course': recipe['course'],
                        'region': recipe['region'],
                        'source': recipe['source']
                    }
                }
                rag_documents.append(ingredient_doc)
        
        print(f"✅ Generated {len(rag_documents)} RAG documents")
        print(f"   • Recipe documents: {len(all_recipes)}")
        print(f"   • Ingredient documents: {len(rag_documents) - len(all_recipes)}")
        
        return rag_documents

    def process_and_export(self, output_file: str = "clean_north_indian_rag_data.json"):
        """
        Main processing pipeline - clean and focused approach
        """
        print("=" * 60)
        print("🍛 CLEAN INDIAN FOOD RAG DATA PROCESSOR")
        print("=" * 60)
        print(f"📁 Data source: {self.data_folder}")
        print(f"🎯 Target: North Indian cuisine ingredients")
        print("📝 Approach: Quality over quantity - Kaggle dataset only")
        print()
        
        # Step 1: Process Kaggle dataset
        recipes = self.process_kaggle_dataset()
        if not recipes:
            print("❌ No recipes processed. Exiting.")
            return None
        
        # Step 2: Create ingredient analysis
        ingredient_analysis = self.create_ingredient_analysis(recipes)
        
        # Step 3: Generate RAG documents
        rag_documents = self.generate_rag_documents(recipes)
        
        # Step 4: Create final clean dataset
        clean_dataset = {
            'metadata': {
                'dataset_name': 'Clean North Indian RAG Data',
                'creation_date': pd.Timestamp.now().isoformat(),
                'version': '1.0_clean',
                'total_recipes': len(recipes),
                'total_rag_documents': len(rag_documents),
                'total_unique_ingredients': ingredient_analysis['total_unique_ingredients'],
                'data_sources': ['kaggle_archanas_kitchen'],
                'geographic_focus': 'North India (Punjab, Chandigarh, Delhi, Haryana)',
                'quality_notes': 'Focused on high-quality ingredient lists only',
                'processing_decisions': [
                    'INDB dataset excluded due to structural incompatibility',
                    'Minimum 3 ingredients per recipe required',
                    'North Indian cuisine filtering applied',
                    'Ingredient text cleaning and normalization performed'
                ]
            },
            'recipes': recipes,
            'ingredient_analysis': ingredient_analysis,
            'rag_documents': rag_documents
        }
        
        # Step 5: Save to JSON file
        output_path = os.path.join(self.data_folder, output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(clean_dataset, f, indent=2, ensure_ascii=False)
        
        # Step 6: Print comprehensive summary
        print("=" * 60)
        print("✅ PROCESSING COMPLETE - CLEAN DATASET READY")
        print("=" * 60)
        print(f"📊 Final Dataset Statistics:")
        print(f"   • Total recipes: {len(recipes)}")
        print(f"   • Unique ingredients: {ingredient_analysis['total_unique_ingredients']}")
        print(f"   • RAG documents: {len(rag_documents)}")
        print(f"   • Average ingredients per recipe: {ingredient_analysis['statistics']['average_per_recipe']:.1f}")
        print()
        print(f"🏆 Top 10 Most Common Ingredients:")
        for ingredient, count in ingredient_analysis['most_common_50'][:10]:
            print(f"   • {ingredient}: {count} recipes")
        print()
        print(f"💾 Output file: {output_path}")
        print(f"🎯 Ready for RAG system integration")
        print("=" * 60)
        
        return output_path

# Usage
if __name__ == "__main__":
    print("Starting Clean Indian Food RAG Data Processing...")
    
    # Initialize with data folder (use current directory)
    data_folder = os.getcwd()  # This will use the current working directory
    processor = CleanIndianFoodProcessor(data_folder)
    
    # Process and create clean dataset
    output_file = processor.process_and_export()
    
    if output_file:
        print(f"\n🎉 SUCCESS! Clean RAG dataset ready at: {output_file}")
        print("\n📋 NEXT STEPS:")
        print("   1. Review the generated JSON file")
        print("   2. Build RAG system using this clean data")
        print("   3. Test with North Indian dish queries")
    else:
        print("\n❌ Processing failed. Please check the data and try again.")
