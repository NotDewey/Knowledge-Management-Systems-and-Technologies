# Nexo IT Services - Project Progress (Phase I)

This is the initial prototype for the project progress submission, due October 31, 2026. It uses the same fictional company and 30-document corpus as the later activities. Its implemented capabilities are supervised document classification and basic TF-IDF/cosine search. It includes a digital knowledge lifecycle map and a curated conceptual ontology. It does not claim to be the final integrated chatbot/recommendation system.

## Install and run

Use Python 3.12. The tested environment used NumPy 2.5.4 and scikit-learn 1.9.1.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python progress.py build
python progress.py search --query "Restore deleted customer files after a failed backup"
python progress.py classify --text "The analyst resolved a failed VPN connection after clearing cached credentials."
python -m http.server 8766 --bind 127.0.0.1 --directory site
```

Open http://127.0.0.1:8766/progress.html. The static browser model and diagrams are included, so the interface can be started without rebuilding evidence. On macOS/Linux use `source .venv/bin/activate`.

## Structure

- `corpus.csv`: original simulated corpus, including unique id, title, text, category, topic and concepts.
- `recommender.py`: reusable text normalization, TF-IDF vectorization and cosine retrieval.
- `classifier.py`: supervised logistic regression and isolated stratified holdout evaluation.
- `progress.py`: executable CLI, real evidence generation, ontology and validation checks.
- `site/`: functional Phase I classification/search interface and digital maps.
- `evidencias/`: exact input/output JSON, raw logs, ontology triples, screenshots and six applied practice records aligned with Topics 1-6.
- `test_progress.py`: behavioral checks, including model input validation and ontology constraints.
- `test_parity.mjs`: browser/Python ranking and classification consistency checks.

## Evidence and limitations

The package records two search queries and three new-text classification examples. A 21/9 stratified holdout fits its evaluation vocabulary only on the training partition. Macro precision and recall are both 0.222. The small simulated corpus is insufficient for automatic operational routing, so the proposed workflow requires human review.

TF-IDF implements the assignment's basic search requirement but measures lexical overlap rather than learned semantic equivalence. Similarity scores are not relevance labels or calibrated confidence. The ontology uses explicit directed triples and a diagram; no OWL reasoning or SPARQL execution is claimed.

The six exercise records are newly completed applied project practices aligned with the reviewed course topics. They do not claim historical course submissions, attendance or a handwritten artifact.

## Hosted resources

Phase I prototype: https://nexo-it-knowledge-lab-oct26.lushcorgi132.chatgpt.site/progress.html

Source repository equivalent: https://nexo-it-knowledge-lab-oct26.lushcorgi132.chatgpt.site/downloads/Progress_Source.zip

Portable Git repository: https://nexo-it-knowledge-lab-oct26.lushcorgi132.chatgpt.site/downloads/Progress_Source.bundle

To recover the repository with Git, download the bundle and run `git clone Progress_Source.bundle Nexo_Progress`.

Progress report: https://nexo-it-knowledge-lab-oct26.lushcorgi132.chatgpt.site/downloads/Project_Progress_Report.pdf

The site is public with the owner's approval. All organization data is fictional. The project materials were prepared with AI assistance and should be reviewed against course requirements before submission.
