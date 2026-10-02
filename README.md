# TSC Workforce Automation & Payroll Processing Engine

An automated data pipeline architecture designed to manage structural employee files, execute evaluation rules, filter promotion eligibility parameters, and compute statutory deductions. The workflow incorporates raw file stream filtering, logical state assignments, and memory-optimized table structures.

## System Workflow Pipeline

The processing system operates as an analytical assembly line distributed across two primary modular operational stages:

1. **Core Processing and Promotion Module (`TSC_PANDAS_PAYROLL_ENGINE.py`)**
   * **Data Normalization:** Ingests the initial raw teacher records, addresses string formatting artifacts, and strips out nested double-quotes from text rows to normalize input formats.
   * **Service Computations:** Evaluates service tenures based on historical entry dates relative to the active target operational year (2026).
   * **Automated Scaling Rules:** Validates organizational groups against an operational dictionary matrix map. Active accounts passing institutional checkpoints are systematically elevated to their prospective grading scales (e.g., `B5` to `C1`), while unselected profiles are marked as `RETAIN ACTIVE`.
   * **Vectorized Financial Mapping:** Cross-references upgraded criteria directly with organizational scale guidelines using indexed lookup maps to overwrite structural values (Basic Salary, Commuter, and House Allowances) in place.
   * **Inter-process Hand-off:** Bypasses horizontal merge joins by utilizing explicit data filtering (`items=filter`) to isolate, thin out, and serialize clean incremental records as an optimized bridge layout for secondary accounting layers.

2. **Deductions and Net Accounting Module (`TSC_ENDMONTH_PAY.py`)**
   * **Memory-Optimized Ingestion:** Sources the clean intermediate records directly into the calculation space.
   * **Statutory Calculations:** Parses individual line rows to compute progressive local income taxes (PAYE), statutory social security protections, and specialized local welfare levies.
   * **Disbursement Verification:** Constructs the final localized terminal summaries indicating absolute gross, total aggregate deductions, and true monthly take-home payouts.

## Tech Stack & Data Tools

* **Operating System environment:** Windows Platform
* **Engine Core:** Python 3 (Pandas DataFrames with clean column extraction)
* **Query Execution Interface:** SQL (SQLite / `pandasql` environment integration hooks)
* **Version Control Framework:** Git & GitHub Cloud Management

## Configuration Guardrails
To prevent local administrative datasets, temporary cache models, or physical payroll calculation spreadsheets from leaking into public code repositories, a targeted rule file is tracked locally:

```text
# .gitignore profile configuration
*.csv
*.xlsx
*.db
```
﻿
