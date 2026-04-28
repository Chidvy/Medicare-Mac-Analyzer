# Medicare MAC Letter Analyzer

An LLM-powered healthcare compliance triage assistant that classifies Medicare MAC correspondence, extracts structured deadlines and risk fields, generates prioritized action checklists, and drafts response letters for human review.

---

## Privacy & Compliance Note

This project uses 100% synthetic sample letters only. No real patient data, beneficiary information, PHI, or provider-identifiable records are included in this repository.

The tool is designed as a compliance triage assistant to support human review, not as a substitute for legal, clinical, billing, or regulatory judgment.

---

## Problem → Solution → Impact

**Problem:** Medicare provider and supplier organizations receive 20–30+ MAC letters monthly. Each letter can carry time-sensitive deadlines, such as 30–45 calendar days for documentation requests or 30-day overpayment response windows, depending on the contractor, letter type, and regulatory context. Missing deadlines can trigger claim denials, regulatory exposure, interest accrual, or financial penalties. Teams manually read each letter, determine priority, pull records, and draft responses.

**Solution:** This automated triage system classifies the letter type, extracts key deadlines and dollar amounts at risk, generates a prioritized action checklist, and drafts a response letter from raw letter text.

**Impact:** Work that previously took about 45 minutes of manual review can be completed in approximately 30 seconds for first-pass triage. High-risk letters are surfaced immediately, and checklists help teams manage time-sensitive deadlines more systematically.

---

## Why This Matters

Medicare MAC correspondence includes complaints, ADRs, overpayment demands, audit notices, and denials, each with distinct workflows, documentation requirements, and time-sensitive deadlines. Manual triage is error-prone and time-consuming. Automated classification and priority scoring help compliance teams focus on high-risk cases, standardize response workflows, and manage deadlines more consistently.

---

## Demo

```bash
python analyzer.py
```

```text
============================================================
MEDICARE MAC LETTER ANALYZER
============================================================

Choose input method:
1. Use a synthetic sample letter (demo)
2. Paste your own letter text

Enter 1 or 2: 1

Using: Overpayment Demand Letter

Analyzing letter...

============================================================
MEDICARE MAC LETTER ANALYSIS
============================================================

LETTER TYPE:    OVERPAYMENT
MAC/CONTRACTOR: CGS DME MAC
JURISDICTION:   Jurisdiction B
DCN:            SYNTH-2025-1204
AMOUNT AT RISK: $12,450
DEADLINE:       30 days from receipt

*** HIGH PRIORITY ***
Time-sensitive repayment window with potential interest accrual if unresolved.

ACTION CHECKLIST:
  [ ] Review overpayment notice and identify billing errors
  [ ] Determine repayment method or response strategy
  [ ] Review repayment, rebuttal, appeal, or extended repayment options based on the demand letter
  [ ] Document all supporting evidence if requesting redetermination
  [ ] Log case status in compliance tracker

DOCUMENTS TO PULL:
  [ ] Original claim details for flagged claims
  [ ] Billing records for dates of service
  [ ] Prior authorization records
  [ ] Provider appeal history

CONTACT INFO:
  Phone: [CONTACT PHONE]

============================================================
DRAFT RESPONSE LETTER
============================================================

[PROVIDER NAME]
[DATE]

[MAC CONTRACTOR / RECOVERY UNIT]
[ADDRESS LINE 1]
[ADDRESS LINE 2]

Re: Overpayment Response — DCN SYNTH-2025-1204
Amount: $12,450.00

Dear Recovery Unit,

We acknowledge receipt of your overpayment notice dated December 1, 2025. 
We have reviewed the identified discrepancies and are taking the following 
actions:

1. Billing Review — reviewing the claims identified in the notice
2. Corrective Action Review — assessing documentation and billing controls
3. Response Planning — evaluating repayment, appeal, or extended repayment options

We will submit our response according to the instructions and timeline included 
in the demand letter.

Sincerely,
[SIGNATURE]
[PROVIDER NAME]

============================================================

Save analysis to JSON file? (y/n): y
Saved to: analysis_20260428_162106.json
```

*Example output shown for demonstration purposes.*

---

## What This Demonstrates

- Applied GenAI to automate healthcare compliance triage workflows
- Built Python pipelines for classifying Medicare correspondence and extracting structured compliance fields
- Designed priority logic based on deadlines, documentation requirements, and financial risk
- Generated action checklists and draft response letters for compliance team review
- Created JSON outputs that can support dashboards, trackers, and deadline monitoring

---

## Architecture

```text
MAC / CMS Letter Text
        ↓
Letter Type Classification
        ↓
Structured Field Extraction
        ↓
Deadline & Risk Prioritization
        ↓
Action Checklist Generation
        ↓
Draft Response Letter
        ↓
JSON Output for Tracker / Dashboard
```

---

## Setup

**Requirements:** Python 3.9+, Anthropic API key

```bash
git clone https://github.com/Chidvy/Medicare-Mac-Analyzer.git
cd Medicare-Mac-Analyzer

pip install -r requirements.txt
```

Set your API key:

```bash
# Windows
set ANTHROPIC_API_KEY=your_key_here

# Mac/Linux
export ANTHROPIC_API_KEY=your_key_here
```

---

## Usage

```bash
python analyzer.py
```

You will be prompted to either:

1. Select one of 3 built-in synthetic sample letters: complaint, ADR, or overpayment
2. Paste your own letter text

Output prints to the terminal and can optionally be saved to a timestamped JSON file.

---

## Letter Types Supported

| Type | Description |
|---|---|
| COMPLAINT | Beneficiary complaint requiring equipment pickup, service review, or billing correction |
| ADR | Additional Documentation Request requiring records to support a claim |
| OVERPAYMENT | Payer demand involving repayment, financial exposure, or response timeline |
| AUDIT | Pre-payment or post-payment audit requiring records review |
| DENIAL | Claim denial with potential appeal or redetermination workflow |
| GENERAL | Informational correspondence or non-urgent communication |

---

## Design Decisions

| Choice | Why It Matters |
|---|---|
| Two-pass extraction and response | Separates compliance field extraction from letter generation for accuracy and review clarity |
| Priority classification logic | Uses deadline urgency, documentation burden, and dollar amount at risk to mirror real triage workflows |
| JSON output for tracking | Extracted data is structured for downstream case management systems, trackers, and dashboards |
| Synthetic samples built in | Enables live demo without real provider data, beneficiary information, or PHI |
| LLM-based extraction | Handles varied letter formats, MAC jurisdictions, and claim types without hardcoded parsing rules |
| Human-review framing | Keeps the tool positioned as decision support, not automated compliance judgment |

---

## Limitations & Future Work

**Current limitations:**

- Uses synthetic sample letters only
- Does not replace compliance, legal, billing, clinical, or regulatory review
- Deadline rules may vary by contractor, letter type, payer, and regulatory context
- Does not yet validate extracted fields against page-level source citations
- Does not calculate exact calendar deadlines from receipt dates
- Does not yet integrate with a case tracker, EHR, billing system, or document management platform

**Future improvements:**

- Batch processing to analyze all open MAC letters and create a priority queue
- Deadline tracking with automatic reminders and escalation alerts
- Streamlit UI for drag-and-drop letter upload with visual priority dashboard
- Appeal letter generator with medical necessity arguments for ADR and denial cases
- Multi-payer support extending beyond Medicare to Medicaid and commercial payers
- Case status tracking tied to compliance reporting
- Page-level source citations and validation checks for audit trails
- Dashboard integration for compliance queues, aging reports, and open-case monitoring

---

## Note on Compliance Outputs

Extracted outputs should be reviewed by compliance, legal, billing, and operational teams before submission or action. This project is designed to accelerate first-pass triage and documentation review, not to make final compliance decisions.

Future versions will add source citations and validation checks to support audit trails for every extracted field and generated recommendation.

---

## Repository Structure

```text
Medicare-Mac-Analyzer/
├── analyzer.py
├── requirements.txt
└── README.md
```

---

## Tech Stack

- Python 3.9+
- Anthropic Python SDK
- Large Language Model API, Claude / OpenAI compatible
- JSON output generation
- Terminal-based workflow
- Synthetic healthcare compliance sample data

---

## Author

**Durga Meduri**  
Business Analytics Manager | MS Business Analytics, UMass Boston

Built from direct observation of compliance workflows in healthcare operations.

[LinkedIn](https://www.linkedin.com/in/durga-c-meduri/) | [GitHub](https://github.com/Chidvy)
