import fs from 'node:fs';
import assert from 'node:assert/strict';
const root=new URL('./',import.meta.url);
const M=JSON.parse(fs.readFileSync(new URL('site/progress-model.json',root),'utf8'));
const js=fs.readFileSync(new URL('site/progress-engine.js',root),'utf8');
const core=js.slice(js.indexOf('function normalize'),js.indexOf('// END SHARED MODEL FUNCTIONS'));
const api=new Function('M',core+';return {recommend,classify};')(M);
for(const s of JSON.parse(fs.readFileSync(new URL('evidencias/searches.json',root),'utf8'))){const actual=api.recommend({query:s.query});assert.deepEqual(actual.map(d=>d.id),s.results.map(d=>d.id));actual.forEach((d,i)=>assert.ok(Math.abs(d.score-s.results[i].score)<1e-12));console.log('PASS search:',s.query);}
for(const c of JSON.parse(fs.readFileSync(new URL('evidencias/classification.json',root),'utf8'))){const actual=api.classify(c.input);assert.equal(actual[0].category,c.prediction);for(const p of actual)assert.ok(Math.abs(p.probability-c.probabilities[p.category])<1e-12);console.log('PASS classification:',c.test);}
