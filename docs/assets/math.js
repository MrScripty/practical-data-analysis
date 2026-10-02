/* Pure numerical helpers used by the browser labs and node tests. */
(function(root){'use strict';
const mean=xs=>xs.reduce((a,b)=>a+b,0)/xs.length;
const sorted=xs=>[...xs].sort((a,b)=>a-b);
const median=xs=>{const a=sorted(xs),n=a.length;return n%2?a[(n-1)/2]:(a[n/2-1]+a[n/2])/2;};
const nearestRank=(xs,p)=>{if(!xs.length||p<0||p>1)throw Error('Invalid quantile input');return sorted(xs)[Math.max(0,Math.ceil(p*xs.length)-1)];};
const ecdf=(xs,x)=>xs.filter(v=>v<=x).length/xs.length;
const paired=(rows,key)=>{const d=rows.map(r=>r.proposed-r[key]);return {d,mean:mean(d),wins:d.filter(v=>v< -1e-9).length,ties:d.filter(v=>Math.abs(v)<=1e-9).length,n:d.length,ratio:mean(rows.map(r=>r.proposed/r[key])),ratioOfMeans:mean(rows.map(r=>r.proposed))/mean(rows.map(r=>r[key]))};};
const weighted=(easy,hard,share)=>easy*share+hard*(1-share);
const safeDivide=(a,b)=>b===0?null:a/b;
const confusion=(tp,fp,fn,tn)=>({agreement:safeDivide(tp+tn,tp+fp+fn+tn),falsePositive:safeDivide(fp,fp+tn),falseDiscovery:safeDivide(fp,tp+fp),precision:safeDivide(tp,tp+fp),recall:safeDivide(tp,tp+fn)});
const api={mean,median,nearestRank,ecdf,paired,weighted,confusion,sorted};
if(typeof module!=='undefined')module.exports=api;root.BookMath=api;
})(typeof window==='undefined'?globalThis:window);
