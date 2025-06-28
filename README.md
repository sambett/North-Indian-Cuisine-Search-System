# Allergen Detection System for North Indian RAG

🛡️ **Safety-enhanced RAG system with comprehensive allergen detection for North Indian cuisine**

## 🚀 Quick Start

1. **Download allergen data:**
   ```bash
   python download_allergen_data.py
   ```

2. **Test the system:**
   ```bash
   python test_system.py
   ```

3. **Try the integration demo:**
   ```bash
   python rag_integration.py
   ```

## 📁 Project Structure

```
northindian_rag/
├── allergen_detection.py          # Core allergen detection engine
├── rag_integration.py             # RAG system integration example
├── download_allergen_data.py      # Data download and setup script
├── test_system.py                 # Basic test script
├── README.md                      # This file
└── allergen_data/                 # Generated allergen databases
    ├── swiss_eu_allergens.json    # EU 14 allergen categories
    ├── indian_allergens.json      # Indian cuisine specific allergens  
    ├── comprehensive_allergen_db.json # Combined database
    └── integration_config.json    # Configuration settings
```

## 🧬 Core Features

### ✅ Comprehensive Allergen Coverage
- **FDA Big 8** allergens (US standard)
- **EU 14** allergen categories (European standard)
- **Indian cuisine specific** allergens (hing, methi, etc.)
- **Regional language support** (Hindi terms included)

### ✅ Smart Detection
- **Rule-based pattern matching** with regex optimization
- **Confidence scoring** based on context and frequency
- **Negation handling** (detects "dairy-free", "no nuts", etc.)
- **Multi-language detection** (English + Hindi)

### ✅ Safety Classifications
- **🚨 CRITICAL**: Can cause anaphylaxis (peanuts, shellfish, tree nuts)
- **⚠️ HIGH**: Serious allergic reactions (milk, eggs, fish)
- **⚡ MODERATE**: Noticeable reactions (soy, mustard, celery)

### ✅ RAG Integration
- **Modular design** - wraps around your existing RAG system
- **Document analysis** - scans retrieved recipes for allergens
- **User profile support** - personalized warnings based on known allergies
- **Safety recommendations** - actionable advice and substitutions

## 🔧 Integration with Your RAG System

### Step 1: Basic Integration

```python
from allergen_detection import AllergenDatabase, RAGAllergenExtension
from rag_integration import SafetyEnhancedRAG

# Wrap your existing RAG system
existing_rag = YourRAGSystem()  # Your current system
safe_rag = SafetyEnhancedRAG(existing_rag)

# Use enhanced system
result = safe_rag.safe_query("butter chicken recipe", 
                            user_allergies=["dairy", "nuts"])

# Check safety
if result['safe_for_user']:
    print("✅ Safe to proceed!")
    # Show recipes
else:
    print("⚠️ Allergen warning detected!")
    # Show warnings and alternatives
```

### Step 2: Customize for Your System

1. **Modify document structure** in `allergen_detection.py`:
   ```python
   def _extract_text_from_document(self, document: Dict) -> str:
       # Update this method to match your document format
       return document['your_content_field']
   ```

2. **Update retrieval method** in `rag_integration.py`:
   ```python
   # Change this line to match your RAG system:
   retrieved_docs = self.rag_system.your_retrieve_method(query, **kwargs)
   ```

## 📊 Allergen Database Details

### Major Allergens (EU 14 + FDA 8)
| Allergen | Severity | Common in Indian Cuisine |
|----------|----------|-------------------------|
| **Milk/Dairy** | HIGH | ✅ Ghee, paneer, yogurt |
| **Tree Nuts** | CRITICAL | ✅ Cashews, almonds in gravies |
| **Peanuts** | CRITICAL | ✅ Groundnut oil, chutneys |
| **Wheat/Gluten** | HIGH | ✅ Roti, naan, thickeners |
| **Sesame** | HIGH | ✅ Til, sesame oil |
| **Mustard** | MODERATE | ✅ Mustard oil, tempering |
| **Eggs** | HIGH | ❌ Less common |
| **Fish** | HIGH | ❌ Regional dishes only |
| **Shellfish** | CRITICAL | ❌ Rare in North Indian |
| **Soy** | MODERATE | ❌ Modern additions |

### Indian-Specific Allergens
- **Asafoetida (Hing)** - Common in dal and vegetarian dishes
- **Fenugreek (Methi)** - Seeds and leaves in curries
- **Coconut** - South Indian influence in North Indian cooking
- **Tamarind (Imli)** - In chutneys and some curries

## 🧪 Testing & Validation

### Run Comprehensive Tests
```bash
# Basic functionality test
python test_system.py

# Full integration test with demo
python rag_integration.py
```

### Test Your Own Recipes
```python
from allergen_detection import AllergenDetector, AllergenDatabase

detector = AllergenDetector(AllergenDatabase())

recipe = "Your recipe text here..."
detections = detector.detect_allergens(recipe)

for detection in detections:
    print(f"⚠️ {detection.warning_message}")
```

## ⚙️ Configuration

Customize behavior in `allergen_data/integration_config.json`:

```json
{
  "allergen_detection": {
    "confidence_threshold": 0.6,
    "severity_filter": ["critical", "high", "moderate"],
    "include_regional_names": true
  },
  "safety_settings": {
    "block_critical_results": false,
    "warn_on_all_detections": true,
    "require_confirmation": true
  }
}
```

## 🎯 Usage Examples

### Example 1: Basic Query
```python
result = safe_rag.safe_query("show me creamy north indian curries")

# Result includes:
# - retrieved_documents: Your normal RAG results
# - allergen_analysis: Detected allergens with confidence scores
# - safety_assessment: Overall safety status
# - recommendations: Actionable safety advice
```

### Example 2: User with Allergies
```python
result = safe_rag.safe_query(
    "butter chicken recipe", 
    user_allergies=["dairy", "tree nuts"]
)

# Will detect dairy in butter chicken and warn about user's allergy
# Provides personalized safety recommendations
```

### Example 3: Document Analysis
```python
extension = RAGAllergenExtension()
analysis = extension.analyze_retrieved_documents(documents, query)

print(f"Status: {analysis['safety_assessment']['status']}")
print(f"Found allergens: {analysis['unique_allergens']}")
```

## 🔄 Extending the System

### Add New Allergens
```python
# In allergen_detection.py, add to _load_default_allergens():
"turmeric": AllergenInfo(
    name="Turmeric",
    aliases=["turmeric", "haldi", "curcumin"],
    severity=AllergenSeverity.MILD,
    description="Can cause skin reactions in sensitive individuals",
    common_sources=["curry powder", "golden milk"],
    regional_names=["हल्दी"]
)
```

### Add New Languages
```python
# Add regional terms to existing allergens:
regional_names=["दूध", "دودھ", "ಹಾಲು"]  # Hindi, Urdu, Kannada
```

## 🚨 Safety Disclaimers

⚠️ **IMPORTANT SAFETY INFORMATION:**

1. **This system is for guidance only** - always verify ingredients manually
2. **Not a substitute for medical advice** - consult healthcare providers for severe allergies
3. **Keep emergency medication accessible** - EpiPen for anaphylactic allergies
4. **Cross-contamination awareness** - kitchen equipment may contain traces
5. **Recipe variations** - actual ingredients may differ from database entries

## 📈 Performance & Scaling

- **Fast pattern matching** with pre-compiled regex
- **Memory efficient** database loading
- **Scales to large document sets** - tested with 1000+ recipes
- **Concurrent processing ready** - thread-safe design

## 🤝 Contributing

### Add More Indian Allergens
1. Research traditional Indian ingredients that cause allergies
2. Add to `indian_allergens.json` with proper Hindi names
3. Include common dishes and regional variations

### Improve Detection Accuracy
1. Add more aliases and regional terms
2. Improve negation detection patterns
3. Add context-aware confidence scoring

### Language Support
1. Add support for more Indian languages (Tamil, Bengali, etc.)
2. Improve transliteration handling
3. Add regional cuisine variations

## 📚 Technical Details

### Architecture
```
User Query → RAG Retrieval → Document Analysis → Allergen Detection → Safety Assessment → Enhanced Response
```

### Core Components
- **AllergenDatabase**: Stores allergen information and mappings
- **AllergenDetector**: Pattern matching and confidence scoring
- **RAGAllergenExtension**: Integration layer for RAG systems
- **SafetyEnhancedRAG**: Complete enhanced RAG wrapper

### Data Sources
- Swiss Food Allergen Legislation (EU 14 categories)
- FDA Big 8 Allergen Guidelines
- Indian cuisine research and traditional knowledge
- OpenFoodFacts sample data for validation

## 🛠️ Troubleshooting

### Common Issues

**No allergens detected:**
- Check if text contains recognizable ingredient names
- Verify database loaded correctly
- Ensure confidence threshold isn't too high

**False positives:**
- Improve negation detection patterns
- Add more context-aware rules
- Adjust confidence thresholds

**Performance issues:**
- Use pre-compiled patterns (already implemented)
- Process documents in batches
- Consider caching frequent queries

## 📞 Support

For issues or questions:
1. Check the test scripts work correctly
2. Verify your document structure matches expected format
3. Review configuration settings
4. Test with simple examples first

---

**Built for the North Indian RAG project** 🇮🇳  
*Making food information safer and more accessible*
