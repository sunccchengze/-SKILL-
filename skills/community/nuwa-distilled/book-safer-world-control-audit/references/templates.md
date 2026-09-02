# *Engineering a Safer World* 操作模板

> 每条链保持 `L → H → SC → controller/CA → UCA → LS → requirement → verification → indicator`；候选不是验证。

## S1 Loss inventory
| L-ID | Unacceptable loss | Affected party | Severity basis | Rights/duties | Excluded loss challenger |
|---|---|---|---|---|---|

## S2 Hazard / system constraint
| H-ID | System state/condition | Worst-case environment | L links | SC-ID | Observable constraint |
|---|---|---|---|---|---|

## S3 Boundary and environment
| In boundary | External controller/dependency | Lifecycle stage | Assumed interface | Feedback | Boundary risk owner |
|---|---|---|---|---|---|

## S4 Controller card
| Controller | Responsibility | Authority/resources | Process-model variables | Algorithm/procedure | Input | CA | Feedback/delay |
|---|---|---|---|---|---|---|---|

## S5 Coordination/interface table
| Controller A | Controller B | Shared responsibility | Conflicting goals | Handoff | Missing/late feedback | Resolution owner |
|---|---|---|---|---|---|---|

## S6 Four-category UCA table
| UCA-ID | Controller | Control action | Type | Actual hazardous context | H link | Controller constraint |
|---|---|---|---|---|---|---|
| | | | not provided | | | |
| | | | provided | | | |
| | | | wrong timing/order | | | |
| | | | wrong duration | | | |

## S7 Loss scenario walk
| LS-ID | UCA/H | Controller/algorithm | Process-model flaw | Input/feedback/delay | Action path/actuator | Process/environment | Org pressure/coordination |
|---|---|---|---|---|---|---|---|

## S8 Safety requirement / verification case
| R-ID | Trace IDs | Required behavior/context | Owner | Design implementation | Analysis | Test/simulation | Operational evidence | Residual |
|---|---|---|---|---|---|---|---|---|

## S9 Migration and leading indicators
| Assumption/constraint | Leading indicator | Source | Threshold | Lag | Owner | Response | Stop/rollback |
|---|---|---|---|---|---|---|---|

## S10 Change-control impact
| Change | Controllers/actions/feedback affected | New/changed H/UCA/LS | Regression evidence | Training/procedure update | Approval | Rollback |
|---|---|---|---|---|---|---|

## S11 CAST learning card
- loss/hazard/violated constraint；
- physical process and proximal events（not root-cause stop）；
- actual control structure vs assumed；
- each controller’s context/process model/feedback；
- coordination and change history；
- systemic corrections + verification + owner；
- individual accountability kept separate from system learning。

## S12 Independent assurance gate
- SME disciplines and affected operators/users；
- competing method (FMEA/FTA/HAZOP/PRA/etc.) interface；
- completeness challenge and excluded scope；
- duplicate/conflicting requirements；
- real-impact evidence / owner / independent reviewer；
- appeal / stop / rollback；
- status：`hazard_analysis_not_safety_certification`。
