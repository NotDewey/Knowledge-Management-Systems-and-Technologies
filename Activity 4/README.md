
# Activity 4 — Evaluation of an Intelligent Information Retrieval System

**Course:** Knowledge Management Systems and Technologies  
**Project:** Nexo IT Services — Document Recommendation System

## Overview

In Activity 3, we developed a document recommender using **TF-IDF and cosine similarity**. For Activity 4, we kept the same recommender and the same corpus of 30 simulated IT support documents. Our goal was to evaluate how well the system retrieves information that is actually useful for a specific support request, rather than change the recommendation algorithm.

We tested the following query:

> VPN connection fails after password change

The system returns the five documents with the highest cosine similarity. We compared those results with relevance labels defined for the query: a document counts as relevant if it contains corrective steps or an applicable policy for the credential-related VPN issue.

## Results

| Metric | Score |
| --- | ---: |
| Precision@5 | 0.80 |
| Recall@5 | 0.80 |
| F1@5 | 0.80 |

| Outcome | Number of documents |
| --- | ---: |
| True positives (TP) | 4 |
| False positives (FP) | 1 |
| False negatives (FN) | 1 |
| True negatives (TN) | 24 |

The system retrieved **4 of the 5 relevant documents**. It also retrieved one document that was not useful for solving the incident (**DOC005**, a training workshop) and missed one relevant recovery document (**DOC026**, which describes the problem using different terms).

These results are from **one query and a simulated 30-document corpus**, so they are a useful starting point, not a claim about performance in a real organization.

## How to run the project

**Requirements:** Python 3 and the packages NumPy, scikit-learn, and Matplotlib.

1. Keep `recommender.py`, `evaluate.py`, and `corpus.csv` in the same folder.
2. Install the dependencies:

   ```bash
   python -m pip install numpy scikit-learn matplotlib
   ```

3. Run the evaluation:

   ```bash
   python evaluate.py
   ```

To test the original recommender separately:

```bash
python recommender.py --query "VPN connection fails after password change"
python recommender.py --id DOC002
```

## Project files

```text
Activity 4/
├── README.md
├── Activity4_Report.pdf
├── corpus.csv
├── recommender.py
├── evaluate.py
└── evidencias/
    └── activity4/
        ├── validation.csv
        ├── evaluation.json
        ├── execution.log
        ├── confusion_matrix.png
        └── performance.png
```

The files in `evidencias/activity4/` are generated automatically when `evaluate.py` runs:

- `validation.csv`: ground-truth labels, system predictions, and outcomes for all 30 documents.
- `evaluation.json`: query, retrieved results, evaluation metrics, and confusion matrix.
- `execution.log`: printed labels, predictions, and metric results.
- `confusion_matrix.png`: visualization of TP, FP, FN, and TN.
- `performance.png`: bar chart comparing Precision, Recall, and F1-score.

The report contains the evaluation scenario, validation table, metric calculations, analysis, and organizational-value infographic.

## What we learned

The recommender performs reasonably well on this example, but shared keywords do not always mean that a document answers the user's question. DOC005 includes terms related to VPN access but does not provide a recovery procedure. Meanwhile, DOC026 contains useful instructions that the system misses because its wording differs from the query.

Two possible improvements would be to **support synonyms or semantic similarity** and to **prioritize approved recovery procedures over general training material** for incident-related searches. These are proposals for future testing; the original Activity 3 recommender was not changed for this evaluation.

## Evaluation method

The Python script uses `precision_score`, `recall_score`, `f1_score`, and `confusion_matrix` from **scikit-learn**, with Matplotlib for the charts. Relevance labels were assigned by one author according to the specific support need. A larger evaluation with multiple queries and independent reviewers would be needed before drawing broader conclusions.
