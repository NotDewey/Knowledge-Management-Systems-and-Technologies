import json,unittest
from pathlib import Path
from recommender import Recommender,load_corpus
from classifier import fit_classifier
from progress import ontology,validate_ontology
ROOT=Path(__file__).resolve().parent

class ProgressTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.engine=Recommender()
    def test_corpus_matches_later_phases(self):
        self.assertEqual(len(self.engine.docs),30)
        self.assertEqual(len(self.engine.by_id),30)
        self.assertEqual({d['category'] for d in self.engine.docs},{'Policy/Process','Support/Incidents','Knowledge/Training'})
    def test_actual_search_evidence(self):
        evidence=json.loads((ROOT/'evidencias/searches.json').read_text())
        for case in evidence:
            hits=self.engine.recommend(query=case['query'])
            self.assertEqual([d['id'] for d in hits],[d['id'] for d in case['results']])
            self.assertEqual(len(hits),5)
            for actual,stored in zip(hits,case['results']):self.assertAlmostEqual(actual['score'],stored['score'],places=12)
    def test_new_text_classification(self):
        vec,model=fit_classifier(self.engine.docs)
        for case in json.loads((ROOT/'evidencias/classification.json').read_text()):
            p=model.predict_proba(vec.transform([case['input']]))[0]
            self.assertEqual(str(model.classes_[p.argmax()]),case['prediction'])
            self.assertAlmostEqual(float(p.sum()),1,places=12)
    def test_ontology_constraints(self):
        graph=ontology(self.engine.docs)
        self.assertTrue(all(validate_ontology(graph,self.engine.docs).values()))
        self.assertEqual(len(graph['nodes']),60);self.assertEqual(len(graph['edges']),126)
    def test_holdout_is_separate(self):
        h=json.loads((ROOT/'evidencias/holdout.json').read_text())
        self.assertFalse(set(h['train_ids'])&set(h['test_ids']))
        self.assertEqual(len(h['test_ids']),9)
    def test_empty_and_invalid_inputs(self):
        with self.assertRaises(ValueError):self.engine.recommend(query=' ')
        with self.assertRaises(ValueError):self.engine.recommend(doc_id='DOC999')

if __name__=='__main__':unittest.main(verbosity=2)
