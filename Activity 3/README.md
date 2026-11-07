# Activity 3 — Top-K Document Recommender with Cosine Similarity

**Course:** Knowledge Management Systems and Technologies  
**Fictional company:** Nexo IT Services  
**Project:** Document Recommendation System

## Overview

This activity implements a small document recommender for **Nexo IT Services**, a fictional IT support company. The goal is to help team members find relevant policies, support incidents, and knowledge articles without having to search the entire repository manually.

The prototype uses **TF-IDF** and **cosine similarity** to return the five most similar documents for either an existing document ID or a short free-text query. It is a lexical recommender, not an embedding-based semantic search system.

## Dataset

The `corpus.csv` file contains **30 simulated documents** covering three areas:

- Policy/Process
- Support/Incidents
- Knowledge/Training

Each document has an `id`, `title`, `text`, and `category`, along with additional metadata such as topic, concepts, owner, version, and review date.

## How it works

1. Load and validate the CSV dataset.
2. Clean text by converting to lowercase, normalizing accents, and removing special characters.
3. Build TF-IDF vectors using unigrams and bigrams and an English stopword list.
4. Calculate cosine similarity between the selected input and the document corpus.
5. Return the **Top-5** documents with their similarity scores. When using a document ID, the original document is excluded.

The script also handles invalid document IDs, empty queries, missing files, missing columns, and duplicate identifiers.

## Requirements

- Python 3
- `numpy`
- `scikit-learn`

Install the dependencies with:

```bash
python3 -m pip install numpy scikit-learn
```

## Running the recommender

Open a terminal in the `Activity-3-KM` folder and run one of the following examples.

**Search using a Policy/Process document:**

```bash
python3 recommender.py --id DOC002
```

**Search using a Support/Incidents document:**

```bash
python3 recommender.py --id DOC008
```

**Search using a free-text query:**

```bash
python3 recommender.py --query "restore deleted customer files after a failed backup"
```

The output includes the input and five recommendations with document IDs, titles, and cosine similarity scores. To obtain machine-readable results, add the `--json` option.

## Validation and evidence

Three test cases were documented:

| Test | Input | Purpose |
| --- | --- | --- |
| 1 | `DOC002` | Policy/Process document recommendation |
| 2 | `DOC008` | Support/Incidents document recommendation |
| 3 | `restore deleted customer files after a failed backup` | Free-text recommendation |

The results, Top-5 similarity scores, and short comments on their relevance are included in `Activity3_Report.pdf`. Additional execution logs and screenshots are stored in the `evidencias/` folder.

## Repository structure

```text
Activity-3-KM/
├── README.md
├── Activity3_Report.pdf
├── corpus.csv
├── recommender.py
├── Guion_video.txt
├── Activity3_Reflection.mp4
└── evidencias/
```

*The video filename above is the suggested location/name; adjust it if your actual MP4 has a different name or is hosted externally.*

## Organizational value and limitations

A recommender like this can reduce repeated work by making related procedures and previous incident records easier to find. It may also help support analysts identify useful documentation before deciding how to address an issue.

However, TF-IDF depends on shared vocabulary. It can miss relevant documents that use different terms, and high similarity does not mean that a document is correct, current, or approved for a specific user. The corpus is also small and simulated.

Future improvements could include synonym handling, embedding-based retrieval, metadata filters, access permissions, document version checks, and ongoing evaluation with reviewed relevance labels.

## Report and reflection

- **Report:** [Activity3_Report.pdf](./Activity3_Report.pdf)
- **Reflection video:** [Activity3_Reflection.mp4](./Activity3_Reflection.mp4) (if uploaded under this filename)

The reflection discusses how document recommendations can reduce rework, the limitations of lexical similarity, and improvements needed for a real organizational environment.

---

*Academic project developed for the Knowledge Management Systems and Technologies course at Tecmilenio.*
