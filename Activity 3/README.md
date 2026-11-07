# Activity 3 — Top-K Document Recommender with Cosine Similarity

**Course:** Knowledge Management Systems and Technologies  
**University:** Tecmilenio  
**Fictional Company:** Nexo IT Services  
**Project:** Document Recommendation System

## Overview

This activity focuses on developing a document recommendation system for **Nexo IT Services**, a fictional IT support company.

The objective is to help employees find relevant organizational documents, such as policies, procedures, support incidents, and training materials, without having to search through the entire repository manually.

The system uses **TF-IDF vectorization and cosine similarity** to identify and recommend the five most similar documents based on an existing document ID or a free-text query.

## Dataset

The repository contains `corpus.csv`, a dataset of **30 simulated organizational documents** divided into three categories:

- Policy/Process
- Support/Incidents
- Knowledge/Training

Each document includes the required fields:

- `id` — Unique document identifier
- `title` — Document title
- `text` — Document content
- `category` — Organizational category

Additional metadata includes topics, concepts, owners, versions, and review dates.

## How the Recommender Works

The recommendation process follows these steps:

1. Loads and validates the document dataset.
2. Cleans the text by converting it to lowercase, normalizing accents, and removing special characters.
3. Converts the documents into numerical vectors using `TfidfVectorizer`.
4. Calculates cosine similarity between the input and the documents.
5. Returns the **Top-5 most similar documents**, including their similarity scores.

When searching by document ID, the original document is excluded from the recommendations.

The implementation also handles invalid IDs, empty queries, missing files, and duplicate identifiers.

## Technologies and Dependencies

- Python 3
- NumPy
- Scikit-learn
- TF-IDF
- Cosine Similarity

### Installation

Clone the repository:

```bash
git clone https://github.com/NotDewey/Knowledge-Management-Systems-and-Technologies.git
```

Navigate to the activity directory:

```bash
cd "Knowledge-Management-Systems-and-Technologies/Activity 3"
```

Install the required dependencies:

```bash
python3 -m pip install numpy scikit-learn
```

## Running the Recommender

The system can be executed directly from the terminal.

### Test 1 — Policy/Process Document

```bash
python3 recommender.py --id DOC002
```

### Test 2 — Support/Incidents Document

```bash
python3 recommender.py --id DOC008
```

### Test 3 — Free-Text Query

```bash
python3 recommender.py --query "restore deleted customer files after a failed backup"
```

Each test returns five recommended documents with their IDs, titles, and cosine similarity scores.

## Test Results and Evidence

The recommender was evaluated using three different test cases:

| Test | Input | Expected Behavior |
|---|---|---|
| 1 | `DOC002` | Recommend documents related to remote access policies and VPN troubleshooting |
| 2 | `DOC008` | Recommend documents related to backup failures and recovery procedures |
| 3 | Free-text backup recovery query | Identify relevant restoration procedures and support documentation |

The results demonstrate that the system can identify documents with related terminology and organizational topics.

Execution screenshots and console logs are available in the [Evidences folder](./Evidences/).

### Evidence Files

| Test | Screenshot | Execution Log |
|---|---|---|
| Test 1 | [browser_test1.png](./Evidences/browser_test1.png) | [test1.log](./Evidences/test1.log) |
| Test 2 | [browser_test2.png](./Evidences/browser_test2.png) | [test2.log](./Evidences/test2.log) |
| Test 3 | [browser_test3.png](./Evidences/browser_test3.png) | [test3.log](./Evidences/test3.log) |

The complete results, similarity scores, and explanations are also included in the activity report.

## Organizational Value

A document recommendation system can help reduce repeated work by allowing employees to find existing solutions instead of solving the same problems multiple times.

For example, when a support analyst encounters a backup failure, the system can recommend previous incident reports, recovery procedures, and relevant policies.

This can support faster decision-making and improve access to organizational knowledge.

## Limitations and Future Improvements

Although the system produces relevant recommendations, TF-IDF has certain limitations:

- It depends on shared vocabulary and may miss documents that use synonyms.
- Similarity scores do not guarantee that a recommendation is correct or useful.
- Short or ambiguous queries may produce less accurate results.
- The dataset contains only 30 simulated documents.

Future improvements could include semantic embeddings, document metadata filters, role-based access controls, security measures, and continuous evaluation.

## Repository Structure

```text
Activity-3-KM/
│
├── README.md
├── Activity3_Report.pdf
├── Conclusion.mp4
├── corpus.csv
├── recommender.py
│
└── Evidences/
    ├── README.md
    ├── browser_test1.png
    ├── browser_test2.png
    ├── browser_test3.png
    ├── test1.log
    ├── test2.log
    └── test3.log
```

## Report and Reflection

**Activity Report:** [Activity3_Report.pdf](./Activity3_Report.pdf)

**Organizational Reflection Video:** [Conclusion.mp4](./Conclusion.mp4)

The reflection addresses how document recommendations can reduce rework, their limitations, and potential improvements for real-world organizational use.

If the video does not play directly on GitHub, download the MP4 file to watch it locally.

## Academic Information

**Institution:** Tecmilenio  
**Course:** Knowledge Management Systems and Technologies  
**Instructor:** Alfredo Paul Aguirre Torres

---

*This project was developed for academic purposes to demonstrate the application of information retrieval and knowledge management technologies in an organizational environment.*
