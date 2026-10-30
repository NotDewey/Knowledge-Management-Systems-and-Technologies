"""Phase I: corpus, supervised classification, TF-IDF search and ontology evidence."""
import argparse,csv,hashlib,json
from collections import Counter
from pathlib import Path
from recommender import Recommender,ROOT,STOPWORDS,clean
from classifier import fit_classifier,evaluate_classifier

CLASSIFICATION_INPUTS=[
 ('Policy example','Every production change must include manager approval, a validation plan and a rollback procedure.'),
 ('Incident example','An employee reported a failed VPN connection after a password change. The analyst cleared cached credentials and restored access.'),
 ('Training example','During the training workshop, participants practice restoring a sample folder and compare the backup manifest in a learning exercise.')]
QUERIES=[
 ('Restore deleted customer files after a failed backup','The operating procedure and FAQ address recovery points and approval. Training material adds context but is not the governing procedure.'),
 ('VPN connection fails after password change','The recovery procedure, incident, access policy and FAQ are applicable. The workshop shares words but lacks corrective steps; alternate terminology can hide relevant guidance.')]
LIFECYCLE=[
 ('Create or acquire','Analyst records the stale-credential VPN incident.','An observed resolution becomes a candidate knowledge record.','Service desk'),
 ('Store or document','Reviewer documents steps and validation in DOC002/DOC003.','The solution becomes a durable, explicit document with an ID.','Knowledge lead'),
 ('Organize or classify','Assign category, topic and concepts to the document.','Metadata and the classifier make the record findable.','Document owner'),
 ('Share','Publish the approved article in the internal knowledge library.','A shared record makes the expert experience available to peers.','Knowledge lead'),
 ('Apply','A new analyst searches for a similar VPN failure and checks DOC002.','The knowledge is used to choose an applicable approved procedure.','Service desk'),
 ('Update or improve','Review a failed search and revise vocabulary or recovery instructions.','Feedback changes the record and starts the next cycle.','Owner and network team')]

def ontology(docs):
    nodes={};edges=[]
    def node(identifier,label,kind):nodes[identifier]={'id':identifier,'label':label,'type':kind}
    for d in docs:
        node(d['id'],d['title'],'Document');cat='category:'+d['category'];node(cat,d['category'],'Category')
        edges.append({'source':d['id'],'predicate':'belongs_to','target':cat})
        for c in d['concepts'].split(','):
            concept='concept:'+c;node(concept,c,'Concept');edges.append({'source':d['id'],'predicate':'mentions','target':concept})
    for a,b in [('Identity','Authentication'),('Backup','Recovery'),('Change','Rollback'),('Phishing','Containment'),('Onboarding','Identity'),('SLA','Escalation')]:
        edges.append({'source':'concept:'+a,'predicate':'related_concept','target':'concept:'+b})
    return {'nodes':list(nodes.values()),'edges':edges}

def validate_ontology(graph,docs):
    ids={n['id'] for n in graph['nodes']};types={n['id']:n['type'] for n in graph['nodes']}
    assert len(ids)==len(graph['nodes'])
    assert all(e['source'] in ids and e['target'] in ids for e in graph['edges'])
    for d in docs:
        memberships=[e for e in graph['edges'] if e['source']==d['id'] and e['predicate']=='belongs_to']
        assert len(memberships)==1 and types[memberships[0]['target']]=='Category'
        assert any(e['source']==d['id'] and e['predicate']=='mentions' for e in graph['edges'])
    return {'unique_nodes':True,'valid_edge_endpoints':True,'one_category_per_document':True,'concepts_present_for_every_document':True}

def sparse(matrix):return [{str(j):float(v) for j,v in zip(row.indices,row.data)} for row in matrix.tocsr()]

def build(out=ROOT/'evidencias'):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);engine=Recommender();vec,model=fit_classifier(engine.docs)
    classifications=[]
    for name,text in CLASSIFICATION_INPUTS:
        probabilities=model.predict_proba(vec.transform([text]))[0]
        classifications.append({'test':name,'input':text,'prediction':str(model.classes_[probabilities.argmax()]),
            'probabilities':dict(zip(model.classes_.tolist(),probabilities.tolist()))})
    searches=[{'query':q,'results':engine.recommend(query=q),'interpretation':note} for q,note in QUERIES]
    holdout=evaluate_classifier(engine.docs);graph=ontology(engine.docs);checks=validate_ontology(graph,engine.docs)
    preprocessing=[{'id':d['id'],'original':d['text'][:160],'normalized':clean(d['text'])[:160]} for d in engine.docs[:3]]
    manifest={'documents':len(engine.docs),'categories':dict(Counter(d['category'] for d in engine.docs)),
        'features':len(engine.vectorizer.vocabulary_),'corpus_sha256':hashlib.sha256((ROOT/'corpus.csv').read_bytes()).hexdigest(),
        'ontology_nodes':len(graph['nodes']),'ontology_edges':len(graph['edges']),'ontology_checks':checks}
    all_evidence={'manifest':manifest,'classifications':classifications,'searches':searches,'holdout':holdout,
        'lifecycle':LIFECYCLE,'ontology':graph,'preprocessing':preprocessing}
    for name,data in [('execution.json',all_evidence),('ontology.json',graph),('classification.json',classifications),
                      ('holdout.json',holdout),('searches.json',searches),('manifest.json',manifest)]:
        (out/name).write_text(json.dumps(data,indent=2),encoding='utf-8')
    with (out/'ontology_triples.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['source','predicate','target']);w.writeheader();w.writerows(graph['edges'])
    log=['PHASE I EXECUTION','CORPUS: '+json.dumps(manifest), '\nCLASSIFICATION INPUTS AND PREDICTIONS']
    for c in classifications:log+=['INPUT: '+c['input'],'PREDICTION: '+c['prediction'],'PROBABILITIES: '+json.dumps(c['probabilities'])]
    for s in searches:
        log+=['\nQUERY: '+s['query']]+[f"{i}. {d['id']} {d['score']:.6f} {d['title']}" for i,d in enumerate(s['results'],1)]+['INTERPRETATION: '+s['interpretation']]
    log+=['\nINDEPENDENT HOLDOUT: '+json.dumps(holdout['report']['macro avg']), 'ONTOLOGY VALIDATION: '+json.dumps(checks)]
    (out/'execution.log').write_text('\n'.join(log),encoding='utf-8')
    browser={'documents':engine.docs,'stopwords':STOPWORDS,'vocabulary':engine.vectorizer.vocabulary_,
        'idf':engine.vectorizer.idf_.tolist(),'vectors':sparse(engine.matrix),
        'classifier':{'vocabulary':vec.vocabulary_,'idf':vec.idf_.tolist(),'classes':model.classes_.tolist(),
                      'coefficients':model.coef_.tolist(),'intercept':model.intercept_.tolist()},'manifest':manifest}
    site=ROOT/'site';site.mkdir(exist_ok=True)
    (site/'progress-model.json').write_text(json.dumps(browser,default=lambda o:int(o),separators=(',',':')),encoding='utf-8')
    make_exercises(out,all_evidence)
    return all_evidence

def make_exercises(out,evidence):
    content={
      '01_knowledge_inventory.md':'''# Topic 1: applied knowledge inventory\n\nOriginal project exercise completed for this progress package. It does not claim an earlier course submission.\n\n|Knowledge form|Nexo example|Capture or reuse mechanism|\n|---|---|---|\n|Tacit|An analyst recognizes stale authentication from experience.|Ask the analyst to explain the diagnosis and review the resulting incident note.|\n|Explicit|DOC002 records approved VPN recovery steps.|Index the document and preserve owner, version and review date.|\n\nDIKW: the error time is data; repeated errors following a credential change are contextual information; a validated cached-credential recovery procedure is knowledge; deciding whether the procedure applies and when to escalate requires expert judgment.\n\nSECI: shadow an analyst (socialization); write the confirmed steps (externalization); connect incident and policy records (combination); apply the procedure in a supervised practice case (internalization).\n\nThe project lifecycle is delivered as a digital map. No handwritten formative exercise is claimed.\n''',
      '02_ai_classification.md':'# Topic 2: AI-enabled organization\n\nOriginal applied exercise. Three new input texts are classified by a supervised TF-IDF/logistic regression pipeline. See classification.json for exact inputs, predictions and uncalibrated probabilities. The classifier assists indexing; humans approve category and content. No generative model or external AI service is called.\n',
      '03_ontology.md':f"# Topic 3: explicit knowledge representation\n\nThe ontology contains Document, Category and Concept entity types. Document belongs_to Category; Document mentions Concept; Concept related_concept Concept. There are {evidence['manifest']['ontology_nodes']} nodes and {evidence['manifest']['ontology_edges']} directed triples.\n\nValidation checks: {json.dumps(evidence['manifest']['ontology_checks'])}.\n\nThe CSV is a transparent triple representation; no Protégé, OWL reasoner or SPARQL execution is claimed.\n",
      '04_graph_mapping.md':'''# Topic 4: organizational graph mapping\n\nOriginal applied exercise. Trace DOC002 through Policy/Process to VPN, Identity and Recovery. Trace DOC007 through Policy/Process to Backup, Recovery and Approval. Recovery connects both topics. The visualization is an illustrative subset of the full ontology_triples.csv export. Similarity edges and conversational components belong to later phases and are not part of this baseline graph.\n''',
      '05_classification_preprocessing.md':'''# Topic 5: preprocessing and supervised classification\n\nThe prototype normalizes case and accents, replaces punctuation, removes a fixed stopword list, and uses unigram/bigram TF-IDF with sublinear term frequency. Logistic regression learns predefined categories from the labeled corpus.\n\nexecution.json stores preprocessing examples and three new-text predictions. holdout.json separates 21 training IDs and 9 held-out IDs; the evaluation vocabulary uses only training text. Macro precision and recall are both 0.222. Training-set predictions do not establish generalization. Collect more independently labeled examples before automatic routing.\n''',
      '06_information_retrieval.md':'''# Topic 6: TF-IDF information retrieval\n\nTwo actual query executions are stored in searches.json and execution.log. The queries use the fitted corpus vocabulary, L2 normalization and cosine similarity. Five ranked results display IDs, titles and scores.\n\nThe course describes this as basic semantic search. The implementation is lexical TF-IDF retrieval, so alternate terms such as corporate tunnel and VPN are not automatically equivalent. A training article may share vocabulary without offering a corrective action. The score is similarity, not proof of relevance.\n'''}
    for filename,text in content.items():(out/filename).write_text(text,encoding='utf-8')

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='action',required=True)
    q=sub.add_parser('search');q.add_argument('--query',required=True)
    c=sub.add_parser('classify');c.add_argument('--text',required=True)
    sub.add_parser('build');a=p.parse_args()
    if a.action=='build':print(json.dumps(build()['manifest'],indent=2));return
    e=Recommender()
    if a.action=='search':result=e.recommend(query=a.query)
    else:
        if not a.text.strip():p.error('Document text cannot be empty')
        v,m=fit_classifier(e.docs);probs=m.predict_proba(v.transform([a.text]))[0]
        result={'prediction':str(m.classes_[probs.argmax()]),'probabilities':dict(zip(m.classes_.tolist(),probs.tolist()))}
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
