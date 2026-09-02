# *What If* 操作模板

> 所有制品写 `claim IDs / source IDs / layer / version / owner / status`。TODO 不等于通过；不得删除失败项。

## T1 Causal question / estimand card
| Target population | Strategy A | Strategy B | Outcome | Time zero / horizon | Contrast | Measure |
|---|---|---|---|---|---|---|
|  |  |  |  |  | ITT / per-protocol / other | RD/RR/mean/etc. |

## T2 七项目标试验—emulation 双协议
| Component | Ideal target trial | Observational emulation | Data gap | Bias if gap | Decision |
|---|---|---|---|---|---|
| Eligibility | | | | | |
| Strategies | | | | | |
| Assignment | random | | | confounding | |
| Follow-up/time zero | | | | immortal/selection | |
| Outcome | | | | measurement | |
| Causal contrast | | | | target shift | |
| Analysis plan | | | | researcher freedom | |

## T3 Strategy version / consistency card
| Label | Start | Dose/intensity | Duration | Switching | Co-intervention | Versions in data | Relevance |
|---|---|---|---|---|---|---|---|

## T4 Identification assumption ledger
| Assumption | Formal/ordinary statement | Why plausible | Why not | Observable implication | Sensitivity/falsifier | Owner | Status |
|---|---|---|---|---|---|---|---|
| Consistency | | | | | | | asserted_not_verified |
| Exchangeability/alternative | | | | | | | |
| Positivity | | | | | | | |
| Measurement/missingness | | | | | | | |
| Interference | | | | | | | |

## T5 Time-indexed variable role table
| Variable@time | Common cause | Outcome predictor | Mediator | Collider/selection | Instrument | Proxy | Adjust? why |
|---|---:|---:|---:|---:|---:|---:|---|

## T6 Competing DAG record
| Arrow / omitted U | Domain basis | Alternative direction | Data implication | Effect of being wrong | Adjudication |
|---|---|---|---|---|---|

## T7 Positivity / overlap diagnostic
| Target stratum | Strategy support | Structural zero or sparse | Weight/influence | Target change proposed | Scientific cost |
|---|---|---|---|---|---|

## T8 Longitudinal strategy table
| Decision time | History available | Treatment rule | Time-varying confounder | Prior-treatment effect | Adherence/censoring | Sequential assumption |
|---|---|---|---|---|---|---|

## T9 Estimate—diagnostic—sensitivity release table
| Estimand | Estimator | Estimate/uncertainty | Failed diagnostic | Negative control | Unmeasured confounding sensitivity | Alternative version | Target boundary |
|---|---|---|---|---|---|---|---|

## T10 High-impact causal evidence packet
- real-world impact evidence + verification status：
- affected groups / differential harm：
- accountable owner / authority：
- applicable rules / IRB / professional review：
- appeal / correction：
- stop / rollback / incident response：
- status 固定：`governance_review_required`；分析不触发行动。

## T11 Claim/source release footer
```text
A locked book claims:
B author later work:
C independent evidence/critique:
D TARGET operationalization:
Unverified assumptions:
Failed diagnostics:
Not authorized:
```
