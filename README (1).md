# 🧠 NLP Review Intelligence Pipeline

> An end-to-end NLP system that ingests 500k+ Amazon product reviews, automatically discovers topics using transformer-based embeddings, and generates human-readable business summaries — turning days of manual analysis into seconds.

---

## 🎯 Project Overview

Businesses receive thousands of customer reviews daily but lack the bandwidth to read them all. This pipeline solves that by automatically:

1. **Clustering** reviews into meaningful topics (e.g. coffee, pet food, snacks) — with zero manual labeling
2. **Summarizing** each topic cluster into a concise, actionable paragraph
3. **Surfacing** insights a non-technical business stakeholder can immediately act on

---

## 🏗️ System Architecture

```
Raw Reviews (568k)
       │
       ▼
 Text Cleaning
 (regex, lowercasing)
       │
       ▼
 Sentence Embeddings
 (all-MiniLM-L6-v2)
 384-dimensional vectors
       │
       ▼
 Dimensionality Reduction
 (UMAP: 384 → 5 dims)
       │
       ▼
 Clustering
 (HDBSCAN)
       │
       ▼
 Topic Labeling
 (BERTopic: 121 topics found)
       │
       ▼
 Summarization per Topic
 (BART-large-CNN)
       │
       ▼
 Business Insights Dashboard
 (Streamlit)
```

---

## 📊 Results

| Metric | Value |
|--------|-------|
| Total reviews processed | 568,454 |
| Sample used for modeling | 10,000 |
| Topics discovered | 121 |
| Summarization model | facebook/bart-large-cnn |
| Embedding model | all-MiniLM-L6-v2 |

**Sample topics discovered automatically:**

| Topic | Keywords | Review Count |
|-------|----------|-------------|
| Coffee & K-Cups | coffee, cup, roast, kcups | 1,143 |
| Cat Food | cat, cats, food, eat | 408 |
| Dog Food | dog, food, bones, teeth | 323 |
| Tea | tea, teas, mint, bags | 318 |
| Chips & Snacks | chips, potato, kettle | 299 |
| Hot Chocolate | chocolate, cocoa, dark, milk | 207 |
| Hot Sauce | sauce, hot, chili, spicy | 126 |

---

## 🛠️ Tech Stack

| Component | Tool | Why |
|-----------|------|-----|
| Data | Amazon Fine Food Reviews (Kaggle) | 568k real, messy reviews |
| Embeddings | `sentence-transformers` (MiniLM-L6-v2) | Fast, free, semantically powerful |
| Topic Modeling | `BERTopic` | State-of-the-art, no manual labels needed |
| Summarization | `facebook/bart-large-cnn` | Fine-tuned for summarization tasks |
| Dashboard | `Streamlit` | Fast to build, easy to demo |
| Hosting | Hugging Face Spaces | Free deployment |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/quratulain-nayeem/NLP-project-.git
cd NLP-project-
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the pipeline
```bash
python pipeline.py
```

### 4. Launch the dashboard
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
NLP-project-/
│
├── pipeline.py           # Full end-to-end pipeline
├── app.py                # Streamlit dashboard
├── requirements.txt      # Dependencies
│
├── data/
│   ├── reviews_with_topics.csv    # Reviews + assigned topics
│   └── topic_summaries.csv        # Auto-generated summaries per topic
│
├── models/
│   └── bertopic_model/            # Saved BERTopic model
│
└── notebooks/
    └── exploration.ipynb          # Step-by-step Colab notebook
```

---

## 💡 Key Design Decisions

**Why BERTopic over LDA?**
Traditional topic modeling (LDA) works on word frequency alone — it would treat "terrible delivery" and "package arrived damaged" as different topics because they share no words. BERTopic uses semantic embeddings, so it understands these mean the same thing.

**Why sample 10k from 568k?**
Embeddings and clustering are computationally expensive. 10k reviews is sufficient to discover meaningful topics and demonstrates the pipeline effectively. The system is designed to scale to the full dataset with a GPU.

**Why combine Summary + Text fields?**
The review title (`Summary`) often contains the most concentrated signal ("Not as advertised", "Great product!"). Combining it with the full text gives the embedding model richer context.

---

## 📈 Business Value

This pipeline reduces the time to understand customer feedback from **days → minutes**. A product manager can instantly answer:
- "What are customers complaining about in our coffee category?"
- "What do dog food buyers love vs. hate?"
- "Which product categories have the most negative sentiment?"

---

## 🔮 Future Improvements

- Add sentiment scoring per topic (positive/negative breakdown)
- Build topic trend analysis over time using the `Time` column
- Extend to other review datasets (Yelp, Steam, Trustpilot)
- Fine-tune summarization model on domain-specific data
- Add interactive filtering by rating score in dashboard

---

## 👩‍💻 Author

**Qurat ul Ain Nayeem**
[GitHub](https://github.com/quratulain-nayeem)
