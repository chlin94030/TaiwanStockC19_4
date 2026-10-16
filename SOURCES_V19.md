# 資料來源與成本設定參考
查閱：2026-10-16。下列是來源文件，不代表已實測所有API可達、具有商業再散布授權或完整PIT保證。

- FinMind官方快速開始：https://finmind.github.io/quickstart/
- FinMind日線及資料集說明：https://finmind.github.io/tutor/TaiwanMarket/Technical/
- 證交所股票個股日成交資訊：https://www.twse.com.tw/zh/trading/historical/stock-day.html
- 本包21筆真實解析樣本：https://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20250901&response=json&stockNo=2330
- 證交所ETF交易規則（0050賣出稅設定參考）：https://www.twse.com.tw/zh/products/securities/etf/overview/rules.html

`v19_twse_sample.json`只作解析測試；來源回覆日期、價格及數量保留，不能據以計算十日期多股票研究。Yahoo備援為第三方日線資料，非證交所即時認證。個人研究請依資料供應商使用及授權條件；遇權限錯誤或限流，程式停止該來源，不嘗試繞過。


## V19.1驗證方法與本次輸入
- 使用者附件：`reference_validation_v190.md`（原摘要完整保留）。
- 時間序列切分與間隔：https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html
- 訓練、驗證及評估資料分開：https://scikit-learn.org/stable/modules/cross_validation.html
- 日線與還原股價資料：https://finmind.github.io/tutor/TaiwanMarket/Technical/

上述來源只用於核對方法及欄位語意。本版實作為自有Python程式，不需安裝scikit-learn。驗證區塊、權重收縮及通過門檻是研究治理偏好，並非文獻或附件證明的最佳數值。原摘要的十個日期已被查看，不再視為全新盲測。

## V19.2 checked references

- FinMind quick start and current access/rate-limit documentation:
  https://finmind.github.io/en/quickstart/
- FinMind technical price dataset schemas:
  https://finmind.github.io/tutor/TaiwanMarket/Technical/
- FinMind token/header example:
  https://finmind.github.io/login/
- Time-ordered validation and gap design (reference, not an imported estimator):
  https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html

Provider limits are not bypassed. These references do not establish this model's
out-of-sample returns. Current-source daily histories are not an immutable historical
membership/disclosure ledger.


## V19.3 implementation references

- Temporal ordering / gap: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html
- Optional fundamental dataset definitions: https://finmind.github.io/tutor/TaiwanMarket/Fundamental/
- Optional institutional / margin dataset definitions: https://finmind.github.io/tutor/TaiwanMarket/Chip/

These references define methods or datasets. They do not establish profitable factors. This replay uses the user-provided Yahoo_daily history; no claim of independently exchange-verified bars is made.


## V19.4 checked primary references (2026-10-16)

- Feature selection concepts: https://scikit-learn.org/stable/modules/feature_selection.html
- Sequential selection: https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SequentialFeatureSelector.html
- Chronological gap/purge reference: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html
- Financial dataset schemas: https://finmind.github.io/tutor/TaiwanMarket/Fundamental/
- FinMind corrections/updates: https://finmind.github.io/WhatIsNew/

The app implements its own bounded sparse search and nonnegative ridge; it does
not call these sklearn estimators. These references establish methods/schemas,
not optimal weights or this strategy's efficacy. Vendor correction histories
do not supply an immutable original-disclosure ledger.
