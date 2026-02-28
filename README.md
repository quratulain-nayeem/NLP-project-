# Review Intelligence — NLP Topic Modeling & Summarization Pipeline

> Upload any CSV of customer reviews. The app automatically discovers what people are talking about, groups similar reviews together, and writes a plain-English summary for each group — turning thousands of unread reviews into actionable business insights in minutes.

---

## What Does This Actually Do?

Imagine you run an e-commerce store and you have 50,000 customer reviews sitting in a spreadsheet. You can't read them all. You don't know what people are complaining about, what they love, or what keeps coming up again and again.

This tool solves that. You drop in your CSV file, pick the column that has the review text, and within minutes you get:

- **Automatic topic groups** — the app figures out on its own that reviews are about "shipping and packaging", "product quality", "customer service" etc. You never tell it what to look for.
- **A plain-English summary per topic** — instead of reading 500 reviews about shipping, you read one paragraph.
- **Sample reviews per topic** — so you can drill down and read the actual feedback.
- **Search within reviews** — type any keyword and instantly see all reviews containing that word.

No machine learning knowledge required to use it. Just upload and read.

---

## Live Demo

The app comes with a pre-loaded demo using **568,454 real Amazon Fine Food Reviews**. Topics discovered automatically include coffee & K-cups, cat food, dog food, tea, chips, chocolate, hot sauce and more — with no manual labeling at any step.

Works best with:
- Product reviews (Amazon, eBay, Etsy)
- Restaurant or hotel reviews (Yelp, TripAdvisor)
- App store reviews (Google Play, App Store)
- Support tickets or customer feedback

---

## How It Works — The Pipeline

```
Your CSV (any size)
       │
       ▼
① Text Cleaning
  Remove HTML, URLs, punctuation, normalize case
       │
       ▼
② Sentence Embeddings
  all-MiniLM-L6-v2 → 384-dimensional vectors
  "Terrible shipping" and "package never arrived"
  are now mathematically close to each other
       │
       ▼
③ Dimensionality Reduction
  UMAP: 384 dims → 5 dims
  Keeps similar reviews close, makes clustering feasible
       │
       ▼
④ Clustering
  HDBSCAN finds natural groups automatically
  No need to specify number of clusters in advance
       │
       ▼
⑤ Topic Labeling
  BERTopic uses c-TF-IDF to find distinctive keywords per cluster
       │
       ▼
⑥ Summarization
  facebook/bart-large-cnn reads all reviews in a cluster
  Generates a concise paragraph summary
       │
       ▼
⑦ Interactive Dashboard
  Click any topic, read the summary,
  explore sample reviews, search by keyword
```

---

## Why This Is Better Than Simple Sentiment Analysis

Most basic NLP tools just tell you "positive" or "negative." That's not useful. A business needs to know *what specifically* people are positive or negative about.

This pipeline uses **semantic embeddings** — the model understands context, not just keywords. "The delivery was a disaster" and "my package took three weeks" get grouped together because they mean the same thing, even though they share zero words.

**Why BERTopic over LDA?**
LDA works on word co-occurrence frequency. BERTopic works on meaning. Reviews that are semantically similar cluster together regardless of exact wording — producing significantly cleaner, more interpretable topics.

---

## Results on Amazon Fine Food Reviews

| Metric | Value |
|--------|-------|
| Total reviews in dataset | 568,454 |
| Sample used for modeling | 10,000 |
| Topics discovered automatically | 121 |
| Embedding model | all-MiniLM-L6-v2 |
| Summarization model | facebook/bart-large-cnn |

**Sample topics discovered with zero manual labeling:**

| Topic | Keywords | Reviews |
|-------|----------|---------|
| Coffee & K-Cups | coffee, cup, roast, kcups | 1,143 |
| Cat Food | cat, cats, food, eat | 408 |
| Dog Food | dog, food, bones, teeth | 323 |
| Tea | tea, teas, mint, bags | 318 |
| Chips & Snacks | chips, potato, kettle | 299 |
| Hot Chocolate | chocolate, cocoa, dark, milk | 207 |
| Hot Sauce | sauce, hot, chili, spicy | 126 |

---

## Tech Stack

| Component | Tool | Purpose |
|-----------|------|---------|
| Data loading | `pandas` | Read and process CSV files |
| Text cleaning | `re` (regex) | Strip HTML, URLs, noise |
| Embeddings | `sentence-transformers` | Convert text to semantic vectors |
| Dim. reduction | `UMAP` | Compress 384 dims to 5 |
| Clustering | `HDBSCAN` | Find natural topic groups |
| Topic modeling | `BERTopic` | End-to-end topic pipeline |
| Summarization | `facebook/bart-large-cnn` | Generate plain-English summaries |
| Dashboard | `Streamlit` | Interactive web interface |
| Hosting | `Hugging Face Spaces` | Free deployment |

---

## Key Design Decisions

**Why sample 10k from 568k reviews?**
Generating embeddings for 568k reviews requires significant compute. 10k is large enough to discover meaningful topics while keeping runtime feasible on a standard machine.

**Why combine the review title and body text?**
Amazon reviews have a `Summary` field (short title) and a `Text` field (full review). The title often contains the most concentrated signal. Concatenating both gives the embedding model richer context per review.

**Why BART for summarization?**
BART is abstractive — it generates new text that captures the key points, producing more natural and readable summaries than extractive methods which just pull sentences directly from the source.

---

## Project Structure

```
NLP-project-/
│
├── app.py                          # Streamlit dashboard
├── requirements.txt                # All dependencies
│
├── data/
│   ├── reviews_with_topics.csv     # 10k reviews with assigned topic IDs
│   └── topic_summaries.csv         # Auto-generated summary per topic
│
├── models/
│   └── bertopic_model              # Saved BERTopic model
│
└── notebooks/
    └── exploration.ipynb           # Full step-by-step Colab notebook
```

---

## Run It Locally

```bash
git clone https://github.com/quratulain-nayeem/NLP-project-.git
cd NLP-project-
pip install -r requirements.txt
streamlit run app.py
```

---

## Limitations & Future Work

- Works best with English text and multi-category review data
- Upload mode uses TF-IDF + KMeans for speed — BERTopic would give better topic quality
- Sentiment breakdown per topic (planned)
- Time-series topic trend analysis (planned)
- Fine-tune summarization model on review-specific data (planned)

---

## Author

**Quratulain Nayeem**
[GitHub](https://github.com/quratulain-nayeem)
