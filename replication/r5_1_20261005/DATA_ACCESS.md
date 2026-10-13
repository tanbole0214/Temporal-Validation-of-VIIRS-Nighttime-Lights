# Data access

The public package contains author-written statistical code and aggregate results. It excludes the compiled 296-prefecture GDP workbook, row-level GDP panels, predictions, individual losses, bootstrap draws and acquired source publications. The public runner can replay summaries and Table 3 without these inputs; model and bootstrap refitting require the exact separate inputs in RESTRICTED_INPUT_SHA256.csv.

The underlying prefecture GDP source data are the *China City Statistical Yearbook* (中国城市统计年鉴; relevant editions through 2025) and municipal/provincial statistical-bureau publications. The compiled workbook is treated only as an intermediary extraction/harmonization file, not as an original statistical source. Official observations independently retrieved from upstream statistical publications take precedence whenever available.

The intermediary compiled workbook was supplied by Markdata (马克集数), operated by 重庆马禾锐信息科技有限公司, https://s.macrodatas.cn/. Its compilation is a third-party processing stage. The provider's current GDP-growth product page is https://s.macrodatas.cn/article/indicator/city-e895d581e72b4d-gdpzengsu-b52ac5 (indicator 108252). It advertises a VIP download requiring the provider's account/access process. The current online series can change and is not certified as byte-identical to the archived workbook used in this study. Reproduction must use the frozen identities, transformations and input hashes, not substitute a later download without checking.

## Restrictions and access requests

The membership agreement inspected on 13 October 2026 (displayed update date 22 September 2026) limits platform-data use to mainland-China research/teaching/internal research, prohibits supplying platform data to third parties, and requires written permission for overseas use or provision. See https://s.macrodatas.cn/membership-agreement and https://s.macrodatas.cn/agreement. These are the publicly displayed terms, not evidence of an individual author's acquisition agreement or a separate permission.

Provider permission requests can be directed to macrodatas@163.com. The provider must determine any permitted peer-review access, cross-border access, post-publication verification, charges, restrictions and availability of the exact historical version. The authors cannot guarantee these permissions or waive provider terms. Public website availability and an ordinary paid account do not establish permission to supply the study's restricted inputs to reviewers.

Zhong Li (lizhong@caas.cn) is the corresponding-author contact for author-controlled code, processing rules, source locators, version/hash matching and verification documentation. Requests involving third-party observations or derivatives require the applicable permission. No unconditional third-party-data redistribution or reviewer-access guarantee is asserted. A written arrangement for necessary restricted-input verification remains an outstanding submission condition.

Seven predeclared verification observations remain unresolved; the verified-enhanced panel retains 298 compiled entries. These qualifications are unchanged by public packaging. The 98 completed sampled verifications must not be conflated with the 108 total new official entries.
