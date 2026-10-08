"""Unchanged complete-province-history refit bootstrap functions from R5."""
import numpy as np
import pandas as pd

def by_province(a,pidx,G):return np.bincount(pidx,weights=np.asarray(a,float),minlength=G)


def pack(d,provinces,x,y,raw=None):
    pi=pd.Index(provinces).get_indexer(d.province_code)
    assert (pi>=0).all()
    a=np.asarray(d[x],float);b=np.asarray(d[y],float);G=len(provinces)
    st={k:by_province(v,pi,G) for k,v in {'n':np.ones(len(d)),'x':a,'xx':a*a,'y':b,'yy':b*b,'xy':a*b}.items()}
    if raw is not None:
        for bench in ['B1','B2','B3']:
            r=b-np.asarray(raw['predicted_'+bench],float)
            for key,v in [('r',r),('rr',r*r),('xr',a*r)]:st[bench+'_'+key]=by_province(v,pi,G)
    return st


def evaluate(panel,m,W):
    provinces=sorted(panel.province_code.unique());results={};detail={}
    for product,lv in m.PRODUCTS.items():
        valid=panel.dropna(subset=['transformed_log_growth_extended',lv]);stats={};hist={}
        for yr in range(2015,2025):
            d=valid[valid.year.eq(yr)].reset_index(drop=True)
            raw=m.benchmark_predictions(panel,d,yr,lv)
            stats[yr]=pack(d,provinces,lv,'transformed_log_growth_extended',raw)
            h=valid[valid.year.lt(yr)]
            hi=pd.Index(provinces).get_indexer(h.province_code)
            hist[yr]=(W@by_province(h.transformed_log_growth_extended,hi,len(provinces)))/(W@by_province(np.ones(len(h)),hi,len(provinces)))
        # Every sum is a province multiplicity-weighted sum, not a fixed-fit loss bootstrap.
        z={yr:{key:W@v for key,v in st.items()} for yr,st in stats.items()}
        for bench in m.BENCHMARKS:
            pooled0=np.zeros(len(W));pooled1=np.zeros(len(W));pooledN=np.zeros(len(W))
            for yr in [2022,2023,2024]:
                prior=list(range(2015,yr));n=sum(z[j]['n'] for j in prior);sx=sum(z[j]['x'] for j in prior);sxx=sum(z[j]['xx'] for j in prior)
                if bench=='B0':
                    sr=sum(z[j]['y']-hist[j]*z[j]['n'] for j in prior)
                    sxr=sum(z[j]['xy']-hist[j]*z[j]['x'] for j in prior)
                else:
                    sr=sum(z[j][bench+'_r'] for j in prior);sxr=sum(z[j][bench+'_xr'] for j in prior)
                den=sxx-sx*sx/n;assert np.all(den>1e-12)
                a0=sr/n;g=(sxr-sx*sr/n)/den;a1=a0-g*sx/n
                zz=z[yr];nn=zz['n'];xx=zz['x'];xxx=zz['xx']
                if bench=='B0':
                    d=zz['y']-hist[yr]*nn;xd=zz['xy']-hist[yr]*xx
                    dd=zz['yy']-2*hist[yr]*zz['y']+hist[yr]**2*nn
                else:d=zz[bench+'_r'];xd=zz[bench+'_xr'];dd=zz[bench+'_rr']
                ss0=dd-2*a0*d+a0*a0*nn
                ss1=dd-2*a1*d-2*g*xd+a1*a1*nn+2*a1*g*xx+g*g*xxx
                assert np.all(ss0>=-1e-12) and np.all(ss1>=-1e-12)
                pooled0+=ss0;pooled1+=ss1;pooledN+=nn
                detail[(product,bench,yr)]=dict(SSE_M0=ss0,SSE_M1=ss1,alpha_M0=a0,alpha_M1=a1,gamma_M1=g,N=nn)
            results[(product,bench)]=dict(SSE_M0=pooled0,SSE_M1=pooled1,N=pooledN,mean_delta_loss=(pooled1-pooled0)/pooledN,skill=1-pooled1/pooled0)
    for b in m.BENCHMARKS:
        e=results[('EOG',b)];bm=results[('Black Marble',b)]
        assert np.max(np.abs(e['N']-bm['N']))==0
        assert np.max(np.abs(e['SSE_M0']-bm['SSE_M0']))<1e-10,'Common M0 bootstrap mismatch'
        results[('paired_EOG_minus_BM',b)]=dict(N=e['N'],mean_delta_loss=(e['SSE_M1']-bm['SSE_M1'])/e['N'],mean_incremental_contrast=e['mean_delta_loss']-bm['mean_delta_loss'])
    return results,detail


def literal_duplicate(panel,weights):
    parts=[]
    for prov,count in zip(sorted(panel.province_code.unique()),weights):
        for k in range(int(count)):
            q=panel[panel.province_code.eq(prov)].copy()
            q['city_code']=q.city_code+'__block'+str(k);q['province_code']=q.province_code+'__block'+str(k);parts.append(q)
    return pd.concat(parts,ignore_index=True)
