# Activity 3 — Execution Evidence

**Course:** Knowledge Management Systems and Technologies  
**Company:** Nexo IT Services  
**Activity:** Top-K Document Recommender with Cosine Similarity

## Overview

This folder contains the execution evidence for the document recommendation system developed in Activity 3.

The purpose of these tests is to demonstrate that the Python recommender correctly processes document IDs and free-text queries, calculates cosine similarity using TF-IDF, and returns the five most relevant documents.

## Test Cases

### Test 1 — Policy/Process

**Input:** `DOC002`

This test uses a document from the Policy/Process category to identify related information about remote access and VPN troubleshooting.

The recommender returns five related documents with their similarity scores, excluding the original document.

**Result:** The recommendations include relevant access policies, troubleshooting guides, and support incidents.

### Test 2 — Support/Incidents

**Input:** `DOC008`

This test uses a Support/Incidents document related to a failed backup operation.

The objective is to determine whether the system can identify relevant recovery procedures, backup policies, and troubleshooting documentation.

**Result:** The system retrieves restoration procedures and recovery guidance that could help an analyst investigate the incident.

### Test 3 — Free-Text Query

**Input:**

```text
restore deleted customer files after a failed backup
```

This test demonstrates the system's ability to recommend documents based on a natural-language query instead of an existing document ID.

**Result:** The highest-ranked recommendations include file restoration procedures, deleted-file recovery guidance, and backup-related documentation.

## Evidence Provided

The evidence folder contains supporting materials for the three test cases, including:

- Console execution logs showing the input and Top-5 recommendations.
- Cosine similarity scores for each recommended document.
- Screenshots demonstrating successful execution.

The full results and explanations are documented in the main activity report.

## How to Reproduce the Tests

From the `Activity-3-KM` directory, run:

**Test 1:**

```bash
python3 recommender.py --id DOC002
```

**Test 2:**

```bash
python3 recommender.py --id DOC008
```

**Test 3:**

```bash
python3 recommender.py --query "restore deleted customer files after a failed backup"
```

Each command returns the five most similar documents with their respective cosine similarity scores.

## Observations

The tests demonstrate that the recommender can identify documents with related terminology and organizational topics.

However, TF-IDF is based on lexical similarity, meaning that documents using different terminology may not always be identified as relevant.

These limitations are discussed further in the main report, along with possible improvements such as semantic embeddings, metadata filtering, and continuous evaluation.

---

*These materials support the validation and reproducibility requirements of Activity 3 — Knowledge Management Systems and Technologies.*
