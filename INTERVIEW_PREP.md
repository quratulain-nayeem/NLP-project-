# Interview Prep — Review Intelligence NLP Pipeline
## Brutal Question Bank — Every Possible Angle

---

## PART 1 — EXPLAIN IT SIMPLY (HR / Non-Technical)

**Q: Tell me about this project in one sentence.**
> I built a web app that takes any spreadsheet of customer reviews and automatically groups them into topics, then writes a one-paragraph summary for each group — so a business can understand what thousands of customers are saying without reading a single review manually.

**Q: What problem does it solve?**
> Companies collect huge amounts of customer feedback but nobody has time to read it all. This tool automates the analysis — you go from 50,000 unread reviews to 10-20 clear, actionable summaries in minutes.

**Q: Who would actually use this?**
> Product managers who want to know what features customers complain about. Customer support leads who want to spot recurring issues before they become crises. E-commerce businesses that sell many product categories and need to monitor feedback at scale.

**Q: What makes it different from just doing a Google search on reviews?**
> Google search requires you to know what you're looking for. This tool tells you what's there even when you don't know what to search for. You don't tell it "find complaints about shipping" — it finds that pattern on its own.

---

## PART 2 — TECHNICAL WALKTHROUGH (Data Scientists / ML Engineers)

**Q: Walk me through your pipeline end to end.**
> First I clean the raw text — lowercasing, removing HTML tags, URLs, and punctuation. Then I generate sentence embeddings using all-MiniLM-L6-v2 from sentence-transformers, which converts each review into a 384-dimensional vector capturing semantic meaning. BERTopic then runs UMAP to compress those 384 dimensions down to 5, making clustering feasible, then HDBSCAN finds natural groupings. BERTopic labels each cluster with representative keywords using c-TF-IDF. Finally BART-large-CNN generates a human-readable summary for each topic cluster by reading the combined text of all reviews in that group.

**Q: What is an embedding and why do you need it?**
> An embedding is a numerical representation of text — a list of numbers capturing the meaning of a sentence, not just its words. You need it because ML models can't process raw text. More importantly, good embeddings place semantically similar sentences close together in vector space — "terrible delivery" and "package never arrived" end up near each other even though they share no words. That proximity is what enables meaningful clustering.

**Q: Why BERTopic over LDA?**
> LDA is a classical topic model that works purely on word co-occurrence frequencies. It treats "terrible delivery" and "package never arrived" as completely unrelated because they share no words. BERTopic uses transformer embeddings, so it understands semantic similarity — both phrases mean the same thing and get clustered together. BERTopic also doesn't require you to specify the number of topics in advance, handles outliers gracefully with Topic -1, and produces more interpretable results on short informal text like reviews.

**Q: What is UMAP and why does BERTopic use it?**
> UMAP stands for Uniform Manifold Approximation and Projection. It's a dimensionality reduction technique. We have 384 numbers per review after embedding — clustering in 384 dimensions is computationally expensive and suffers from the curse of dimensionality where everything appears equally distant. UMAP compresses those 384 dimensions down to 5 while preserving neighborhood structure — reviews that were semantically similar in 384 dimensions stay close together in 5 dimensions. This makes HDBSCAN clustering much more effective and faster.

**Q: What is HDBSCAN and how is it different from K-Means?**
> HDBSCAN is a density-based clustering algorithm. Unlike K-Means you don't need to specify the number of clusters — it finds them automatically based on data density. It also handles outliers gracefully by assigning ambiguous points to a noise cluster (Topic -1 in BERTopic) rather than forcing everything into a cluster. For messy real-world text where not every review fits neatly into a category, this is significantly better than K-Means.

**Q: What does Topic -1 mean?**
> Topic -1 is BERTopic's outlier bucket — reviews that didn't fit confidently into any discovered cluster. In my results about 25% of reviews landed there. This is actually desirable — it means the model isn't forcing ambiguous reviews into topics where they don't belong. In production you'd tune HDBSCAN's min_cluster_size and min_samples parameters to reduce this.

**Q: Why did you use BART for summarization instead of just extracting sentences?**
> Extractive summarization just pulls sentences directly from the original text — you're limited to exact phrasing. BART is abstractive, meaning it generates new text capturing the key points. This produces more natural, readable summaries. BART-large-CNN was specifically fine-tuned on news articles and CNN summaries, making it strong at condensing large bodies of text into coherent paragraphs.

**Q: What is c-TF-IDF and how does BERTopic use it?**
> c-TF-IDF stands for class-based TF-IDF. Regular TF-IDF finds words that are frequent in one document but rare overall. c-TF-IDF applies the same logic at the cluster level — it finds words that are frequent within a topic cluster but rare across all other clusters. This is how BERTopic generates topic labels. If reviews about coffee frequently mention "roast", "kcups", "brew" and those words rarely appear in other topic clusters, they become the representative keywords for that coffee topic.

---

## PART 3 — DESIGN DECISIONS (Senior Engineers)

**Q: Why did you sample 10k instead of using all 568k reviews?**
> Generating embeddings for 568k reviews on a CPU takes hours. 10k gives a representative sample that's large enough to discover meaningful topics. In production with GPU acceleration and a distributed setup, you'd process the full dataset. The pipeline architecture is modular — swapping in the full dataset is straightforward.

**Q: How would you scale this to millions of reviews?**
> Several ways. First, use GPU for embedding — it's the bottleneck. Second, use BERTopic's online learning mode which processes data in batches without loading everything into memory. Third, store embeddings in a vector database like Pinecone or ChromaDB so you don't re-embed on every run. Fourth, use a message queue like Celery to process new reviews asynchronously as they come in. Fifth, for summarization, use a lighter model or distilled version of BART.

**Q: Why combine the Summary and Text fields?**
> Amazon reviews have both a short title (Summary) and full review body (Text). The title contains highly concentrated signal — "Terrible quality", "Best purchase ever" — while the body has context. Concatenating both gives the embedding model the most complete representation of the reviewer's opinion. Just using the title misses detail; just using the body sometimes buries the main sentiment.

**Q: How would you evaluate whether your topics are good?**
> Several approaches. Quantitatively, topic coherence scores like C_v or NPMI measure whether the top words in a topic co-occur frequently in real text — high coherence means the topic makes semantic sense. Qualitatively, human evaluation where you ask people to rate whether the top words and representative documents for each topic belong together. BERTopic also has built-in visualization tools like intertopic distance maps that show how distinct and well-separated topics are.

**Q: What are the actual limitations of your approach?**
> Honest answer — four main ones. First, BART wasn't fine-tuned on product reviews so summaries sometimes have a news-article tone rather than consumer language. Second, Topic -1 outlier bucket is around 25% which suggests room for hyperparameter tuning. Third, the topic labels are auto-generated keyword strings — readable but not always perfectly descriptive. Fourth, the upload mode uses TF-IDF + KMeans instead of the full BERTopic pipeline for speed, so upload topic quality is lower than the demo.

**Q: What would you build differently for production?**
> I'd build a proper ingestion pipeline with Airflow for continuous review processing. Store embeddings in ChromaDB or Pinecone for fast similarity search. Add topic drift monitoring — as new products launch, new topics emerge and the model should adapt. Proper unit tests for preprocessing and embedding steps. A REST API around the pipeline so other systems can query it. And I'd fine-tune the summarization model on review-specific data.

---

## PART 4 — TRICKY / GOTCHA QUESTIONS

**Q: Your topic names look weird — "Cat Cats Food She" — why?**
> Good catch. The topic name comes from the most distinctive words in that cluster according to c-TF-IDF. "She" and "cats" appearing alongside "cat" suggests the reviews in that cluster often describe cat behaviour using feminine pronouns and plural forms. In production I'd add a deduplication step to remove near-duplicate words and filter pronouns from topic labels.

**Q: If BERTopic is so good, why does your upload mode use TF-IDF + KMeans?**
> BERTopic requires downloading the sentence-transformers model (~80MB) and running UMAP + HDBSCAN which takes several minutes on CPU for even moderate datasets. Running this inside a Streamlit app would timeout and create a terrible user experience. TF-IDF + KMeans runs in seconds. The tradeoff is topic quality vs speed. In a production system I'd use async processing — the user uploads, gets notified when done, and comes back to results.

**Q: How do you know your summaries are accurate?**
> Honestly, I don't have a formal evaluation metric for this — it's a limitation. BART generates fluent, coherent text but I'm relying on the pre-training quality rather than domain-specific validation. To properly evaluate, I'd use ROUGE scores comparing generated summaries against human-written summaries of the same review clusters, or run a human evaluation study where annotators rate summary quality on accuracy and completeness.

**Q: What if someone uploads non-English reviews?**
> The pipeline would still run but results would be poor. The embedding model all-MiniLM-L6-v2 is primarily trained on English text, so non-English reviews won't embed as meaningfully. BART-large-CNN is English-only for summarization. To support multilingual reviews I'd switch to a multilingual embedding model like paraphrase-multilingual-MiniLM-L12-v2 and use mBART or mT5 for multilingual summarization.

**Q: Your search filters reviews within the currently selected topic. Shouldn't it search across all topics?**
> That's a valid design question. I made it topic-scoped intentionally — the user has already drilled into a specific topic category, so searching within that context is more useful than global search. If you searched "terrible" globally you'd get reviews from every category mixed together. Within the "Shipping" topic, "terrible" specifically shows you shipping complaints. For a future version I'd add a global search mode as well.

**Q: Why Streamlit and not a proper React frontend?**
> For a portfolio project demonstrating NLP capabilities, Streamlit lets me ship a working product in a fraction of the time. The value of this project is the ML pipeline, not the frontend framework. In a production setting I'd separate the backend pipeline into a FastAPI service and build a React frontend that consumes it — but that's an engineering decision based on team skills and scaling needs, not a reflection of the ML work.

**Q: Could this be gamed? What if someone floods the reviews with fake reviews?**
> Yes — adversarial or spam reviews would pollute the topic clusters. Mitigations include adding a review authenticity score before clustering, detecting duplicate or near-duplicate reviews using cosine similarity on embeddings, and filtering reviews below a minimum length threshold. This is a known challenge in e-commerce review systems generally.

---

## PART 5 — BEHAVIOURAL QUESTIONS

**Q: What was the hardest technical challenge?**
> Getting BERTopic to produce clean, meaningful topics rather than clusters dominated by stopwords. Initially topics were labeled with generic words like "the, and, to" because common words were drowning out meaningful signal. I solved this by ensuring thorough text cleaning before embedding and understanding that BERTopic's c-TF-IDF handles this at the representation level — the key was trusting the pipeline rather than over-engineering the preprocessing.

**Q: What would you add with more time?**
> First priority would be sentiment breakdown per topic — not just what people talk about but whether they're positive or negative about it. Second, time-series analysis using the review timestamps to show how topics evolve month over month. Third, replacing the upload mode's TF-IDF pipeline with proper async BERTopic processing so quality matches the demo. Fourth, a confidence score on each topic assignment.

**Q: What did you learn from this project?**
> The gap between a working notebook and a working product is enormous. Getting BERTopic to run in Colab was straightforward. Building a multi-mode Streamlit app with proper state management, good UX, and clean deployment took significantly more thought. I also learned that model quality is only half the story — the business framing of what insights you surface and how you present them matters just as much to the people who would actually use the tool.

**Q: How does this demonstrate skills relevant to a data science role?**
> It covers the full workflow — data acquisition, preprocessing, feature engineering via embeddings, unsupervised modeling, evaluation thinking, and deployment. It uses modern NLP tools that are industry standard. And it's framed around a real business problem with a tangible output. Most importantly, the "How It Works" page and this conversation show I can explain complex technical decisions clearly to both technical and non-technical audiences — which is what data scientists actually do day to day.
