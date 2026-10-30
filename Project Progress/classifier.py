"""TF-IDF logistic regression with an isolated stratified holdout evaluation."""
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
from recommender import make_vectorizer

def fit_classifier(docs,indices=None):
    selected=docs if indices is None else [docs[i] for i in indices]
    vec=make_vectorizer()
    x=vec.fit_transform([d['text'] for d in selected])
    model=LogisticRegression(C=4,max_iter=1500,random_state=42)
    model.fit(x,[d['category'] for d in selected])
    return vec,model

def evaluate_classifier(docs):
    train,test=train_test_split(list(range(len(docs))),test_size=.3,
        stratify=[d['category'] for d in docs],random_state=42)
    vec,model=fit_classifier(docs,train)
    truth=[docs[i]['category'] for i in test]
    pred=model.predict(vec.transform([docs[i]['text'] for i in test])).tolist()
    return {'train_ids':[docs[i]['id'] for i in train],
        'test_ids':[docs[i]['id'] for i in test],
        'rows':[dict(id=docs[i]['id'],truth=t,prediction=p) for i,t,p in zip(test,truth,pred)],
        'report':classification_report(truth,pred,zero_division=0,output_dict=True),
        'matrix':confusion_matrix(truth,pred,labels=model.classes_).tolist(),
        'classes':model.classes_.tolist()}
