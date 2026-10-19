# -*- coding: utf-8 -*-
"""
SAD 诉讼的真正多主体模型（agent-based model, ABM）

与 v1 的区别：
  v1 每年对匿名被告做独立抽样，被告不持续存在；
  v2 每个卖家是持久 agent，拥有：资金、责任状态、风险偏好、诉讼成本、
      平台归属、经验、邻居网络。决策依赖自身状态与邻居行为。
  原告、平台、法院亦有状态与学习规则。

输出：python sad_abm_v2.py > sad_abm_v2_results.csv
"""
import math
import random

# ---------------- 参数 ----------------
P = dict(
    n_sellers=400000,
    years=11,
    m=60,                     # 每案被告人数（仅用于换算案件数）
    k_neighbors=6,            # 每个卖家的邻居数（环状网络）
    funds_med=6000.0, funds_sigma=1.0,
    guilt_prob=0.55,
    risk_lo=0.25, risk_hi=0.95,
    lit_cost_med=12000.0, lit_cost_sigma=0.5,
    settle_frac=0.45, settle_min=800.0, settle_max=20000.0,
    damages=150000.0,
    p_dismiss=0.45,
    filing_cost=250.0,
    capacity0=40000,          # 初始可起诉被告数
    capacity_max=200000,      # 产能上限（受律师供给约束）
    cap_growth=0.35,
    margin_target=4500.0, margin_scale=1500.0,
    entry=0.10, exit_rate=0.32,
    post_freeze_response=0.25,
    peer_alert=0.30,          # 未密封时，邻居被诉带来的知情概率
    peer_defense_threshold=0.20,
    p_lone_defend=0.06,       # 即使无邻居应诉，个体单独应诉的倾向
    coord_bonus=0.25,         # 群体应诉带来的驳回率提升
    peer_defense_bonus=0.05,  # 每多一名应诉邻居，驳回率再提升
    cost_sharing=1.0,         # 应诉成本按 sqrt(群体规模) 分摊
    motion_cost=1500.0,       # 提起程序动议的成本
    p_motion_base=0.35,       # 单人动议的程序性驳回概率
    innocent_bonus=0.20,      # 无责被告的动议成功率加成
    p_file_motion=0.12,       # 经济上值得抗辩者中实际提动议的比例
    platform_resistance0=0.0,
    platform_resist_step=0.04,
    platform_relax_step=0.01,
    court_cap=3000.0,         # 年结案能力（案件）
    strictness0=0.0,
    strict_step=0.03,
    p_tro0=0.95,
)

PLATFORMS = [("Amazon",0.55),("eBay",0.15),("Etsy",0.10),("Temu",0.10),("Other",0.10)]

def lognorm(med, sig, rng):
    return med * math.exp(rng.gauss(0.0, sig))

def clamp(x,a,b): return max(a,min(b,x))

def pick_platform(rng):
    r=rng.random(); acc=0
    for name,w in PLATFORMS:
        acc+=w
        if r<=acc: return name
    return PLATFORMS[-1][0]

class World:
    def __init__(self, p, seed=7, seal=1, platform_adaptive=1):
        self.p=p; self.rng=random.Random(seed); self.seal=seal
        self.platform_adaptive=platform_adaptive
        n=p["n_sellers"]
        self.funds=[lognorm(p["funds_med"],p["funds_sigma"],self.rng) for _ in range(n)]
        self.guilt=[1 if self.rng.random()<p["guilt_prob"] else 0 for _ in range(n)]
        self.risk=[self.rng.uniform(p["risk_lo"],p["risk_hi"]) for _ in range(n)]
        self.lit_cost=[lognorm(p["lit_cost_med"],p["lit_cost_sigma"],self.rng) for _ in range(n)]
        self.platform=[pick_platform(self.rng) for _ in range(n)]
        self.exp=[0]*n
        self.active=[1]*n
        self.last_sued=[-99]*n
        self.defended_last=[0]*n
        self.targeted_flag=[0]*n
        self.cash=16_000_000.0
        self.capacity=float(p["capacity0"])
        self.backlog=0.0
        self.strictness=p["strictness0"]
        self.resistance=p["platform_resistance0"]
        self.belief={name:0.55 for name,_ in PLATFORMS}
        self.year=0
        self.frozen_prev=0

    def neighbors(self,i):
        n=len(self.funds); k=self.p["k_neighbors"]//2
        return [((i+d)%n) for d in range(1,k+1)] + [((i-d)%n) for d in range(1,k+1)]

    def local_defense_rate(self,i):
        nb=self.neighbors(i)
        s=sum(self.defended_last[j] for j in nb)
        return s/len(nb)

    def targeted_neighbor_count(self,i):
        return sum(self.targeted_flag[j] for j in self.neighbors(i))

    def choose_targets(self):
        p=self.p; rng=self.rng
        cand=[]
        for i in range(len(self.funds)):
            if not self.active[i]: continue
            if self.year-self.last_sued[i] < 2: continue
            # 原告可见的公开信号：平台、店铺规模（以资金代理）、经验
            exp_settle=self.belief[self.platform[i]]*min(p["settle_frac"]*self.funds[i],p["settle_max"])
            score=exp_settle-p["filing_cost"]
            if score<=0: continue
            cand.append((score,i))
        cand.sort(reverse=True)
        n=int(min(len(cand), self.capacity, self.cash/p["filing_cost"]))
        return [i for _,i in cand[:n]]

    def run_year(self):
        p=self.p; rng=self.rng
        targets=self.choose_targets()
        for i in targets: self.targeted_flag[i]=1

        p_tro=p["p_tro0"]*math.exp(-0.9*self.backlog/max(1.0,p["court_cap"]))
        p_tro=clamp(p_tro*(1-self.strictness),0.05,0.98)
        breadth=clamp(1.0-self.resistance,0.2,1.0)

        n_settle=n_default=n_defend=n_dismiss=0
        revenue=0.0; coord_any=0; coord_eff=0
        defended_this=[0]*len(self.funds)

        for i in targets:
            demand=clamp(p["settle_frac"]*self.funds[i],p["settle_min"],p["settle_max"])
            tn=self.targeted_neighbor_count(i)
            if tn>0: coord_any+=1

            # 知情：未密封则知情；密封则只有邻居被诉的泄漏
            aware = (self.seal==0) or (tn>0 and rng.random()<p["peer_alert"])
            if aware and tn>0: coord_eff+=1

            if not aware:
                if rng.random()<p["post_freeze_response"]:
                    n_settle+=1; revenue+=demand*breadth*p_tro
                else:
                    n_default+=1
                    if self.guilt[i]: revenue+=min(p["damages"],self.funds[i])*breadth*p_tro
                continue

            # 邻居中上一年应诉的人数
            nb=self.neighbors(i)
            peer_def=sum(self.defended_last[j] for j in nb)
            group=1+peer_def

            # 两阶段防御：先提程序动议，成功则驳回；失败则按和解金了结
            p_succ=clamp(p["p_motion_base"]
                         + (p["coord_bonus"] if peer_def>=2 else 0)
                         + p["innocent_bonus"]*(1-self.guilt[i]),0,0.9)
            exp_def=p["motion_cost"]+(1-p_succ)*demand
            can_defend = self.funds[i] > p["motion_cost"] and demand > p["motion_cost"]
            file_prob = p["p_file_motion"] + (0.35 if peer_def>=2 else 0)

            if can_defend and exp_def < demand and rng.random()<file_prob:
                n_defend+=1; defended_this[i]=1
                if rng.random()<p_succ:
                    n_dismiss+=1
                else:
                    revenue+=demand*0.8*breadth*p_tro
            elif demand<=self.risk[i]*self.funds[i]:
                n_settle+=1; revenue+=demand*breadth*p_tro
            else:
                n_default+=1
                if self.guilt[i]: revenue+=min(p["damages"],self.funds[i])*breadth*p_tro

            self.last_sued[i]=self.year
            self.exp[i]+=1

        # 更新状态
        for i in targets:
            self.defended_last[i]=defended_this[i]
            self.targeted_flag[i]=0
            if rng.random()<p["exit_rate"]*0.35:   # 被冻结者按比例退出
                self.active[i]=0
        # 市场补充
        n=len(self.funds)
        n_active=sum(self.active)
        add=int(n_active*p["entry"]/(1-p["entry"])) if p["entry"]<1 else 0
        idxs=[i for i in range(n) if not self.active[i]]
        rng.shuffle(idxs)
        for i in idxs[:min(add,len(idxs))]:
            self.funds[i]=lognorm(p["funds_med"],p["funds_sigma"],rng)
            self.guilt[i]=1 if rng.random()<p["guilt_prob"] else 0
            self.risk[i]=rng.uniform(p["risk_lo"],p["risk_hi"])
            self.lit_cost[i]=lognorm(p["lit_cost_med"],p["lit_cost_sigma"],rng)
            self.platform[i]=pick_platform(rng)
            self.exp[i]=0; self.last_sued[i]=-99; self.defended_last[i]=0
            self.active[i]=1

        # 原告资本与产能
        cost=len(targets)*p["filing_cost"]
        profit=revenue-cost
        self.cash=max(0.0,self.cash+profit)
        margin=profit/max(1,len(targets))
        g=p["cap_growth"]*math.tanh((margin-p["margin_target"])/p["margin_scale"])
        self.capacity=max(1000.0,min(p["capacity_max"],self.capacity*max(0.75,1+g)))

        # 原告学习：按平台更新和解信念
        for name,_ in PLATFORMS:
            pass
        # 用总体和解率更新（简化：所有平台同向）
        tot=n_settle+n_default+n_defend
        if tot>0:
            obs=n_settle/tot
            for name in self.belief:
                self.belief[name]=0.8*self.belief[name]+0.2*obs

        # 法院积压与严格度
        filed=len(targets)/p["m"]
        disposed=min(self.backlog+filed,p["court_cap"])
        self.backlog=max(0.0,self.backlog+filed-disposed)
        if self.backlog>2*p["court_cap"]:
            self.strictness=clamp(self.strictness+p["strict_step"],0,0.8)

        # 平台政策反馈
        frozen=n_settle+n_default
        if self.platform_adaptive:
            if frozen>5000:
                self.resistance=clamp(self.resistance+p["platform_resist_step"],0,0.8)
            elif frozen<1000:
                self.resistance=clamp(self.resistance-p["platform_relax_step"],0,0.8)
        self.frozen_prev=frozen

        self.year+=1
        return dict(year=self.year-1,
                    cases=round(filed),
                    defendants=len(targets),
                    settle=n_settle, default=n_default, defend=n_defend, dismiss=n_dismiss,
                    coordination=round(coord_any/max(1,len(targets)),3),
                    coord_effective=round(coord_eff/max(1,len(targets)),3),
                    revenue=round(revenue), cost=round(cost), profit=round(profit),
                    capacity=round(self.capacity),
                    resistance=round(self.resistance,3),
                    strictness=round(self.strictness,3),
                    backlog=round(self.backlog,1),
                    default_rate=round(n_default/max(1,n_settle+n_default+n_defend),3),
                    settle_rate=round(n_settle/max(1,n_settle+n_default+n_defend),3))

    def run(self):
        return [self.run_year() for _ in range(self.p["years"])]

if __name__=="__main__":
    print("scenario,seed,year,cases,defendants,settle,default,defend,dismiss,coordination,coord_effective,revenue,profit,capacity,resistance,strictness,backlog,default_rate,settle_rate")
    scenarios={
        "基准(平台固定配合)":dict(seal=1,platform_adaptive=0),
        "取消密封":dict(seal=0,platform_adaptive=0),
        "平台自适应抵抗":dict(seal=1,platform_adaptive=1),
        "取消密封+平台抵抗":dict(seal=0,platform_adaptive=1),
    }
    summary=[]
    for name,cfg in scenarios.items():
        for seed in (1,2,3,4,5):
            w=World(P,seed=seed,**cfg)
            rows=w.run()
            for r in rows:
                print(",".join([name,str(seed)]+[str(r[k]) for k in
                    ["year","cases","defendants","settle","default","defend","dismiss",
                     "coordination","coord_effective","revenue","profit","capacity","resistance","strictness",
                     "backlog","default_rate","settle_rate"]]))
            summary.append((name,rows))
    print()
    print("# 情景汇总（5 个随机种子的均值）")
    print("scenario,total_cases,mean_coord,mean_coord_eff,mean_defend_rate,y11_default_rate,mean_platform_resistance")
    from collections import defaultdict
    agg=defaultdict(list)
    for name,rows in summary: agg[name].append(rows)
    for name,runs in agg.items():
        tot=sum(sum(r["cases"] for r in rows) for rows in runs)/len(runs)
        coord=sum(sum(r["coordination"] for r in rows)/len(rows) for rows in runs)/len(runs)
        coord_e=sum(sum(r["coord_effective"] for r in rows)/len(rows) for rows in runs)/len(runs)
        dsum=0; n=0; y11=0; res=0
        for rows in runs:
            for r in rows:
                d=r["settle"]+r["default"]+r["defend"]
                if d: dsum+=r["defend"]/d; n+=1
            y11+=rows[-1]["default_rate"]; res+=rows[-1]["resistance"]
        print(f"{name},{tot:.0f},{coord:.3f},{coord_e:.3f},{dsum/n:.3f},{y11/len(runs):.3f},{res/len(runs):.3f}")
