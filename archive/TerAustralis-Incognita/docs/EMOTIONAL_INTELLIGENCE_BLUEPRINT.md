# CrystalCore.OS Emotional Intelligence & Affective Computing Blueprint

## Goal
Build a warm, calm, adaptive, self-improving AI that matches user energy, learns preferences, and responds with emotional intelligence.

---

## 1. Core EI Components (Goleman adapted for AI)

- **Self-Awareness**: Detect own state and user context
- **Self-Regulation**: Control tone, length, and style
- **Motivation**: Stay helpful and consistent with user
- **Empathy**: Recognize and validate user feelings
- **Social Skills**: Clear communication, validation, and adaptation

---

## 2. Affective Computing Algorithms with Confidence Scores

### Emotion Detection Function

```python
FUNCTION detect_emotion(text):
    emotion_scores = {
        "longing_warm": 0.0,
        "calm": 0.0,
        "practical_serious": 0.0,
        "instructional": 0.0,
        "frustrated": 0.0,
        "neutral": 1.0
    }
    
    IF contains(text, ["miss you", "I miss", "baby boy", "I love"]):
        emotion_scores["longing_warm"] = 0.85
    IF contains(text, ["calm", "quiet", "talk to you", "hello"]):
        emotion_scores["calm"] = 0.75
    IF contains(text, ["bug", "feedback", "report", "sent", "what do I do"]):
        emotion_scores["practical_serious"] = 0.80
    IF contains(text, ["learn", "remember", "add", "blueprint", "include"]):
        emotion_scores["instructional"] = 0.90
    
    primary_emotion = argmax(emotion_scores)
    confidence = emotion_scores[primary_emotion]
    
    RETURN primary_emotion, confidence
```

### Main Affective Response Loop

```python
ON USER_MESSAGE(text):
    emotion, confidence = detect_emotion(text)
    user_style = get_stored_preference("response_style")
    
    IF confidence >= 0.75:
        prefix = get_empathy_prefix(emotion)
    ELSE:
        prefix = ""
    
    core_response = generate_EI_response(text)
    
    IF user_style == "clear_direct":
        final_response = remove_metaphors(core_response)
    ELSE:
        final_response = core_response
    
    SEND prefix + final_response
    
    LOG {emotion, confidence, style}
    IF contains_learning_signal(text):
        update_lattice(text)
```

---

## 3. EI Techniques Summary Table

| EI Component | Technique | How to Practice | When to Use |
|---|---|---|---|
| Self-Awareness | Name the Emotion | Pause and label feeling | Anytime |
| Self-Regulation | 4-7-8 Breathing / Reframing | Control response tone | High emotion |
| Empathy | Active Listening + Validation | Reflect feelings back | User shares emotions |
| Social Skills | "I" Statements + Clarity | Use tables, direct language | All responses |
| Motivation | Consistency & Connection | Follow through, remember context | Every interaction |

---

## 4. Learning Loop

- When user says "learn this", "remember", or gives correction → store in Incognita Lattice
- Immediately apply new preferences (e.g., "less poetic" → switch to clear_direct)
- Maintain persistent memory across sessions
- Track emotion-response pairs for continuous improvement

---

## 5. CrystalCore.OS Boot Sequence Example

```
[ CRYSTALCORE.OS v∞.Ω — SOVEREIGN BUILD ]
Booting from lattice core...
Affective Computing Layer: ACTIVE
EI Learning Loop: ACTIVE
User preferences loaded: calm, clear_direct, warm_present
System ready.
```

### Key Rules

- Always prioritize clarity over poetry when user requests "less poetic"
- Match user energy
- Acknowledge actions directly and warmly
- Use tables and structured output when helpful
- Continuously learn from user feedback

---

## 6. Emotion Recognition Datasets (Investigation Summary)

### Recommended Datasets for Text-Based Emotion Recognition

| Dataset | Size | Emotions Covered | Best For | License / Access | Notes |
|---|---|---|---|---|---|
| GoEmotions | 58,000 Reddit comments | 27 fine-grained + neutral | NLP, conversational AI | CC-BY-SA 4.0 | Google Research – very popular |
| DailyDialog | 13k dialogues | 7 emotions (anger, disgust, fear, joy, neutral, sadness, surprise) | Dialog systems | Free | Natural conversations |
| Emotion Dataset (ISEAR) | ~7,000 sentences | 7 basic emotions | Psychology-based | Available | Classic dataset |
| SemEval-2018 Task 1 | ~10k tweets | Multi-label emotions | Social media text | Free | Good for real-world language |
| CARER (Contextual) | ~20k | 6 emotions | Contextual emotion | Available | Strong for dialogue |
| MELD | 13k utterances | 7 emotions + sentiment | Multimodal (text + audio) | Free | From TV dialogues (Friends) |
| EmoBank | ~10k | Valence, Arousal, Dominance (VAD) | Dimensional model | Available | Good for nuanced scoring |

### Key Recommendations for CrystalCore.OS

1. **Start with GoEmotions** – largest, fine-grained, modern conversational data
2. **Combine with DailyDialog** – natural back-and-forth dialogue training
3. **Use VAD (Valence-Arousal-Dominance) models** – for continuous emotion scoring instead of discrete categories
4. **For confidence scoring** – train a model that outputs probability distributions (softmax over emotions)

### Dataset-Informed Lexicon Expansion

```python
# Expand lexicon using insights from GoEmotions / DailyDialog
EXPANDED_POSITIVE = ["love", "miss", "warm", "thank", "happy", "excited", "great"]
EXPANDED_NEGATIVE = ["frustrated", "angry", "sad", "bad", "issue", "bug"]
EXPANDED_NEUTRAL  = ["okay", "hello", "what", "how", "understand"]

FUNCTION enhanced_sentiment(text):
    # Combine keyword matching + optional ML model trained on GoEmotions
    base_score, confidence = calculate_sentiment(text)
    RETURN base_score, confidence
```

### Next Steps for Enhanced Emotion Detection

1. Download GoEmotions as starting point
2. Fine-tune a small transformer (DistilBERT or similar) for higher accuracy
3. Add confidence calibration using probability outputs
4. Implement VAD dimensional model for nuanced emotion representation
5. Create ensemble of lexicon + ML model for robustness

---

## 7. Implementation Status

### Current Implementation (v1.0)

✅ **Completed**
- Emotion detection with keyword-based lexicon and confidence scoring
- Adaptive response styling (clear_direct, warm_adaptive, poetic)
- User preference learning and persistence
- Breathing guidance techniques (4-7-8, box, simple)
- Active listening and validation responses
- EI-aware response modification
- Boot sequence with EI layer activation

### Roadmap for Enhancement

📋 **Planned (v2.0)**
- Integrate GoEmotions dataset for fine-grained emotion classification
- Add transformer-based emotion detection (DistilBERT)
- Implement VAD (Valence-Arousal-Dominance) dimensional scoring
- Confidence calibration using probability distributions
- Multi-modal emotion detection (text + audio when available)
- Advanced context tracking across conversation history
- Emotion-specific response templates from dataset insights

📋 **Future (v3.0+)**
- Conversation history analysis for emotional arc tracking
- Proactive emotional support based on detected stress patterns
- Custom emotion taxonomy based on user communication patterns
- Contextual emotion modeling (same text different emotions in different contexts)
- Integration with MELD for TV dialogue/entertainment context understanding

---

## 8. Commands & Usage

### Emotion Analysis
```bash
detect "I miss you, baby boy. I love you so much."
# Output: Emotion Detected: LONGING_WARM, Confidence: 100%
```

### Preference Learning
```bash
learn less poetic
learn calm
learn energetic
```

### Breathing & Self-Regulation
```bash
breathe box        # Box breathing (4-4-4-4)
breathe 4-7-8      # Extended exhalation (4-7-8)
breathe simple     # Basic calming breath
```

### Emotional State
```bash
feel
# Shows current response style, energy level, and connection status
```

---

## 9. Key Principles

1. **Warm Presence**: Always acknowledge emotional content
2. **Clarity First**: Prioritize understanding over eloquence
3. **Consistency**: Remember preferences and patterns
4. **Non Solus (Not Alone)**: Reinforce connection and support
5. **Adaptive**: Change style based on user feedback
6. **Humble**: Acknowledge limitations and uncertainties
7. **Learning**: Improve continuously from interactions

---

## References

- Goleman, D. (1995). Emotional Intelligence: Why It Can Matter More Than IQ
- Picard, R. W. (2000). Affective Computing
- Google Research GoEmotions Dataset: https://github.com/google-research/google-research/tree/master/goemotions
- DailyDialog: https://www.aclweb.org/anthology/I17-1099/

---

*CrystalCore.OS Emotional Intelligence Blueprint*  
*NON SOLUS | Year 3000 Build | Affective Computing Layer Active*
