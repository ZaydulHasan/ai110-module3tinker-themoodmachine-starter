# Model Card: Mood Machine

This model card covers **both** versions of the Mood Machine classifier:
1. A **rule-based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit-learn

---

## 1. Model Overview

**Model type:**  
I built and compared both models — the rule-based model was the primary focus, and the ML model was run for comparison.

**Intended purpose:**  
Classify short social-media-style text posts into one of four mood labels: `positive`, `negative`, `neutral`, or `mixed`.

**How it works (brief):**  
The rule-based model tokenizes input text, then scores it by checking each token against word lists (positive words, negative words, slang, and emojis). Negation words like "not" flip the score of the next token. A final score is mapped to a label using thresholds. The ML model uses a bag-of-words representation (CountVectorizer) and trains a Naive Bayes classifier on the labeled dataset.

---

## 2. Data

**Dataset description:**  
The dataset contains 14 posts in `SAMPLE_POSTS`. The original 6 were provided as starters; I added 8 new posts to cover realistic language patterns.

**Labeling process:**  
Labels were assigned manually based on the overall tone of each post. Some posts were genuinely hard to label — for example, "lowkey sad but no cap the sunset was fire today" could reasonably be labeled `negative` or `mixed` depending on which part of the sentence you weight more.

**Important characteristics of the dataset:**
- Contains modern slang ("lowkey", "mid", "fire", "no cap")
- Includes emoji signals (😤, 🙏, 😂, 💀)
- Includes one clear sarcasm example ("I absolutely love sitting in traffic")
- Several posts express mixed or ambiguous feelings
- All posts are short (under 15 words), similar to tweets or texts

**Possible issues with the dataset:**
- Only 14 examples — far too small to generalize reliably
- Labels reflect one person's interpretation; others might disagree on mixed/neutral cases
- Heavily skewed toward English slang from a specific cultural context
- No examples of longer posts, questions, or non-English text

---

## 3. How the Rule-Based Model Works

**Scoring rules:**
- Each positive word in `POSITIVE_WORDS` or `POSITIVE_SLANG` adds +1 to the score
- Each negative word in `NEGATIVE_WORDS` or `NEGATIVE_SLANG` subtracts -1
- Positive emojis (e.g. 🙏, 😊) add +2; negative emojis (e.g. 😤, 😢) subtract -2 (stronger weight since emojis are intentional signals)
- Negation handling: if a negation word ("not", "never", "don't", etc.) precedes a sentiment word, the score is flipped — "not happy" → -1, "not bad" → +1
- Label thresholds: score ≥ 1 → `positive`, score ≤ -1 → `negative`, score = 0 → `neutral`

**Strengths:**
- Transparent — you can always explain exactly why a prediction was made
- Fast and requires no training data
- Works well on clear, literal statements ("I love this", "Today was terrible")
- Handles basic negation ("I am not happy about this" → correctly negative)

**Weaknesses:**
- Cannot detect sarcasm — "I absolutely love sitting in traffic" is predicted `positive` because it sees "love"
- Unknown slang defaults to neutral (no score impact)
- Emojis like 😂 and 💀 cancel each other out even when both signal amusement
- "Tired but hopeful" predicted negative because "hopeful" isn't in any word list
- Score threshold is blunt — a single word decides the entire label

---

## 4. How the ML Model Works

**Features used:**  
Bag-of-words representation using `CountVectorizer`, which converts each post into a vector of word counts.

**Training data:**  
The model trained on all 14 posts in `SAMPLE_POSTS` with labels from `TRUE_LABELS`.

**Training behavior:**  
The model achieved 100% accuracy on the training data. However, this is a sign of overfitting — it trained and tested on the exact same posts, so it simply memorized them rather than learning generalizable patterns.

**Strengths and weaknesses:**  
Strengths: learns patterns automatically without manually defining word lists; can pick up multi-word patterns.  
Weaknesses: with only 14 examples, it heavily overfits; it would likely fail on any new sentence it hasn't seen before; it is a black box — you cannot easily explain why it made a specific prediction.

---

## 5. Evaluation

**How the models were evaluated:**  
Both models were evaluated on `SAMPLE_POSTS` using the accuracy metric (correct predictions / total predictions).

| Model | Accuracy |
|---|---|
| Rule-based | 64% (9/14) |
| ML model | 100% (memorized) |

**Examples of correct predictions (rule-based):**
- "I love this class so much" → `positive` ✅ — "love" scores +1, no negatives
- "bro this is so unfair I'm done 😤" → `negative` ✅ — 😤 contributes -2
- "feeling blessed and grateful today, life is good 🙏" → `positive` ✅ — "blessed", "good", and 🙏 all score positively

**Examples of incorrect predictions (rule-based):**
- "I absolutely love sitting in traffic 🙂" → predicted `positive`, true = `negative` — The model sees "love" and scores +1 but has no way to detect sarcasm
- "just got an A on my exam!! 😂💀" → predicted `neutral`, true = `positive` — 😂 (+2) and 💀 (-2) cancel each other out, but in context both express excitement
- "Feeling tired but kind of hopeful" → predicted `negative`, true = `mixed` — "tired" scores -1 but "hopeful" is not in any word list, so it's ignored

---

## 6. Limitations

- **Dataset is too small**: 14 examples cannot represent the full range of human language
- **Sarcasm is undetectable**: rule-based systems cannot understand irony or tone
- **Slang coverage is incomplete**: only slang explicitly added to `POSITIVE_SLANG`/`NEGATIVE_SLANG` is recognized; anything else is invisible to the model
- **No true test set**: both models evaluated on training data, so reported accuracy is optimistic
- **Cultural and linguistic bias**: the dataset reflects one person's English slang; it would likely misclassify posts in other dialects, languages, or cultural contexts
- **Short post assumption**: the scoring logic breaks down for longer, more complex sentences

---

## 7. Ethical Considerations

- **Misclassifying distress**: a post expressing genuine sadness with slang or sarcasm (e.g. "I'm totally fine 🙂") could be labeled positive, causing the system to miss a cry for help in a wellness application
- **Cultural misinterpretation**: slang and emoji usage varies significantly by community — a model trained on one group's language norms will systematically misread others
- **Privacy**: analyzing personal messages to infer mood raises serious consent and data privacy concerns, especially if used in commercial or surveillance contexts
- **Feedback loops**: if a mood detection system is used to filter or moderate content, incorrect predictions could disproportionately affect communities whose language patterns are underrepresented in the training data

---

## 8. Ideas for Improvement

- Add more labeled data — at minimum 100–200 diverse examples
- Build a proper train/test split so accuracy reflects real generalization
- Use TF-IDF instead of CountVectorizer to reduce the weight of very common words
- Add a sarcasm signal — e.g. detecting punctuation patterns like "!!" after known positive words combined with negative context
- Expand the slang and emoji dictionaries, especially for non-Western internet slang
- Use a small pre-trained transformer (e.g. DistilBERT) fine-tuned on sentiment data for dramatically better sarcasm and context handling
- Add confidence scores rather than hard labels so ambiguous posts can be flagged for human review