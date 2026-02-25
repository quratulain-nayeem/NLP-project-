# 🎯 Interview Prep — NLP Review Intelligence Pipeline

These are the questions recruiters and technical interviewers will most likely ask. Study the answers but reword them in your own voice.

---

## 🟢 Conceptual Questions (Non-Technical Interviewers / HR)

**Q: Can you explain your NLP project in simple terms?**

> I built a system that reads thousands of Amazon customer reviews and automatically organizes them into topics — like coffee, pet food, snacks — without anyone telling it what categories to look for. Then it writes a one-paragraph summary for each topic, so a business manager can understand what customers are saying without reading thousands of reviews themselves. It turns days of manual work into seconds.

---

**Q: What problem does this project solve?**

> Businesses collect huge amounts of customer feedback but don't have the bandwidth to read it all. My pipeline automates the discovery of what customers are talking about and surfaces key insights in plain English. It's essentially an automated analyst for unstructured text data.

---

**Q: Why did you choose Amazon reviews for this project?**

> Amazon reviews are a great proxy for real-world business data — they're messy, varied, and large scale (568k reviews). They also have a mix of short and long text, multiple product categories, and real human language including typos and slang, which makes the NLP challenges more realistic.

---

## 🔵 Technical Questions (Data Scientists / ML Engineers)

**Q: Walk me through your pipeline end to end.**

> Sure. First I clean the raw text — removing HTML tags, punctuation, and normalizing case. Then I generate sentence embeddings using `all-MiniLM-L6-v2` from sentence-transformers, which converts each review into a 384-dimensional vector that captures semantic meaning. Next, BERTopic runs UMAP to reduce those 384 dimensions down to around 5, making clustering feasible, then uses HDBSCAN to find natural groupings. BERTopic labels each cluster with representative keywords. Finally I use BART-large-CNN to generate a human-readable summary for each topic cluster.

---

**Q: What is an embedding and why do you need it?**

> An embedding is a numerical representation of text — a list of numbers that captures the meaning of a sentence, not just its words. You need it because machine learning models can't process raw text directly, they work with numbers. More importantly, good embeddings place semantically similar sentences close together in vector space, which is what enables meaningful clustering later.

---

**Q: Why did you use BERTopic instead of LDA?**

> LDA (Latent Dirichlet Allocation) is a classical topic model that works purely on word co-occurrence frequencies. It would treat "terrible delivery" and "package never arrived" as different topics because they share no words. BERTopic uses transformer embeddings, so it understands semantic similarity — both phrases mean the same thing and would be clustered together. BERTopic also produces more interpretable topics and integrates better with modern NLP workflows.

---

**Q: What is UMAP and why does BERTopic use it?**

> UMAP (Uniform Manifold Approximation and Projection) is a dimensionality reduction technique. We have 384 numbers per review after embedding, which is too high-dimensional for clustering algorithms to work efficiently — this is the "curse of dimensionality." UMAP compresses those 384 dimensions down to 5 while preserving the neighborhood structure, meaning reviews that were semantically similar in 384 dimensions are still close together in 5 dimensions. This makes HDBSCAN clustering much more effective.

---

**Q: What is HDBSCAN and how does it differ from K-Means?**

> HDBSCAN is a density-based clustering algorithm. Unlike K-Means, you don't need to specify the number of clusters in advance — it finds them automatically based on the density of points. It also handles outliers gracefully by assigning them to a "noise" cluster (Topic -1 in BERTopic), rather than forcing every point into a cluster. This is important for messy real-world text where not everything fits neatly into a category.

---

**Q: What does Topic -1 mean in your results?**

> Topic -1 is BERTopic's outlier bucket — reviews that didn't fit strongly into any discovered cluster. In my results, about 2,533 of 10,000 reviews landed there. This is normal and actually desirable — it means the model isn't forcing ambiguous reviews into topics where they don't belong. In a production system, you'd work to reduce this through hyperparameter tuning or by using BERTopic's outlier reduction features.

---

**Q: Why did you use BART for summarization? Why not just extract sentences?**

> Extractive summarization (just pulling out sentences) is simpler but has limitations — you're limited to exact phrasing from the original text, which may not be the most coherent summary. BART is an abstractive summarization model, meaning it generates new text that captures the key points. This produces more natural, readable summaries. BART-large-CNN was specifically fine-tuned on news articles and CNN summaries, making it strong at condensing large bodies of text.

---

**Q: How did you handle the fact that reviews are noisy and messy?**

> Several ways. In preprocessing, I removed HTML tags (Amazon reviews often contain them), stripped punctuation, normalized to lowercase, and removed extra whitespace. At the modeling level, BERTopic's use of semantic embeddings is inherently more robust to noise than keyword-based approaches — minor spelling variations and informal language don't break the embeddings the way they would break regex or keyword matching.

---

**Q: How would you scale this to the full 568k reviews?**

> A few approaches. First, use GPU acceleration for embedding — it's the most expensive step. Second, use BERTopic's online learning mode which processes data in batches. Third, for summarization I'd switch to a lighter model or use the Hugging Face inference API to avoid running BART locally. The pipeline architecture is already modular so swapping components is straightforward.

---

## 🔴 Deep Dive Questions (Senior Engineers / Research)

**Q: What are the limitations of your current approach?**

> A few honest limitations. First, the summarization model (BART) wasn't fine-tuned on product reviews, so summaries sometimes read like news articles rather than consumer insights. Second, the topic labels are auto-generated keyword strings — they're readable but not always perfectly descriptive. Third, I'm not doing any temporal analysis, so I can't track how topics or sentiment shift over time. Fourth, Topic -1 (outliers) is large at ~25%, which suggests room for hyperparameter tuning.

---

**Q: How would you evaluate whether your topics are good?**

> Topic quality in unsupervised learning is tricky to evaluate. Quantitatively, I'd use topic coherence scores (like C_v or NPMI) which measure whether the top words in a topic actually co-occur frequently in real text. Qualitatively, I'd do a human evaluation — have people rate whether the top words and representative documents for each topic make sense together. BERTopic also has built-in visualization tools like intertopic distance maps that help assess topic separation.

---

**Q: What would you do differently if you were building this for production?**

> Several things. I'd build a proper data pipeline with Airflow or Prefect to continuously ingest new reviews. I'd store embeddings in a vector database like Pinecone or ChromaDB for fast similarity search. I'd add monitoring to track topic drift over time — as new products launch, new topics emerge. I'd also fine-tune the summarization model on domain-specific data and add a confidence score to each topic assignment. And I'd build proper unit tests for the preprocessing and embedding steps.

---

## 🟡 Behavioural / Portfolio Questions

**Q: What was the hardest part of this project?**

> The trickiest part was getting BERTopic to produce clean, meaningful topics rather than noisy clusters dominated by stopwords. The initial results had topics labeled with generic words like "the, and, to" because common words were drowning out the meaningful ones. I solved this by ensuring the text cleaning step was thorough and understanding that BERTopic's c-TF-IDF approach handles this at the representation level.

---

**Q: What would you add if you had more time?**

> I'd add a sentiment breakdown per topic — not just what people are talking about, but whether they're happy or unhappy about it. I'd also add time-series analysis using the review timestamps to show how topics evolve month over month. And I'd build a proper REST API around the pipeline so other systems could query it programmatically.

---

**Q: How does this project demonstrate skills relevant to a data science role?**

> It covers the full data science workflow — data acquisition, preprocessing, feature engineering (embeddings), unsupervised modeling, evaluation, and deployment. It uses modern NLP tools that are industry-standard. And importantly, it's framed around a real business problem with a tangible output, not just a notebook with accuracy metrics. That framing — from raw data to business insight — is what data scientists actually do day to day.
