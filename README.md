An LLM-powered compliance triage system that automates the analysis of 
Medicare Administrative Contractor (MAC) correspondence — classifying 
letter type, extracting structured compliance data, generating prioritized 
action checklists, and drafting response letters.

Built to eliminate manual triage bottlenecks in DME and home health 
provider workflows, where missed deadlines carry direct financial and 
regulatory consequences.

## The Problem This Solves

Medicare Home health providers receive dozens of MAC letters monthly — complaints, ADRs, overpayment demands, audit notices. Each has different deadlines, required documentation, and response strategies. Providers manually read each letter, decide priority, pull records, and draft responses.

Miss a 30-day complaint deadline → compliance violation.  
Miss a 45-day ADR window → automatic claim denial.  
Miss an overpayment response → interest accrual at ~11% annually.

This tool triages letters in seconds, not hours.

---

## What It Does

Given any MAC/CMS letter (pasted as text), the tool:

1. **Classifies** the letter type: Complaint, ADR, Overpayment, Audit, Denial, or General
2. **Extracts** structured fields: MAC contractor, DCN, HCPCS code, dollar amount at risk, deadline
3. **Prioritizes** HIGH / MEDIUM / LOW with a one-line reason
4. **Generates** a step-by-step action checklist specific to that letter type
5. **Drafts** a professional response letter ready for compliance team review
6. **Saves** structured JSON output for downstream tracking or dashboard use

---

## Sample Output

```
============================================================
  MEDICARE MAC LETTER ANALYSIS
============================================================

LETTER TYPE:    COMPLAINT
MAC/CONTRACTOR: CGS DME MAC
JURISDICTION:   Jurisdiction B
DCN:            SYNTH-2025-0042
HCPCS CODE:     XXXXX (Orthotic Equipment)
DEADLINE:       30 days from receipt

** MEDIUM PRIORITY **
  30-day hard deadline for equipment pickup and fax confirmation required.

ACTION CHECKLIST:
  [ ] Contact beneficiary within 5 business days
  [ ] Schedule equipment pickup appointment
  [ ] Obtain beneficiary signature on pickup confirmation
  [ ] Fax pickup documentation to Complaint Screening department
  [ ] Log case closure in compliance tracker

DOCUMENTS TO PULL:
  [ ] Original delivery documentation
  [ ] Beneficiary signature on delivery
  [ ] Equipment serial number record

CONTACT INFO:
  Phone: XXXXXXX

============================================================
  DRAFT RESPONSE LETTER
============================================================
[PROVIDER NAME]
[DATE]

CGS DME MAC Jurisdiction B
Complaint Screening Department

Re: DCN SYNTH-2025-0042 — Beneficiary Equipment Pickup Request

Dear CGS Complaint Screening Team,

We are writing to acknowledge receipt of your correspondence dated MM/DD/YYYY
regarding the above-referenced beneficiary and DCN.

We have initiated the equipment pickup process and are coordinating directly with
the beneficiary to schedule retrieval of the L0651 orthotic equipment.

Please contact [CONTACT NAME] at [PHONE] with any questions.

Sincerely,
[SIGNATURE]
[PROVIDER NAME]
============================================================
```

---

## Setup

**Requirements:** Python 3.9+, Anthropic API key ([get one here](https://console.anthropic.com))

```bash
# Clone the repo
git clone  https://github.com/Chidvy/Medicare-Mac-Analyzer.git
cd medicare-mac-analyzer

# Install dependencies
pip install -r requirements.txt

# Set your API key (Windows)
set ANTHROPIC_API_KEY=your_key_here

# Set your API key (Mac/Linux)
export ANTHROPIC_API_KEY=your_key_here
```

---

## Usage

```bash
python analyzer.py
```

You will be prompted to either:
- Select one of 3 built-in synthetic sample letters (complaint, ADR, overpayment demand)
- Paste your own letter text

Output prints to terminal and optionally saves to a timestamped JSON file.

---

## Letter Types Supported

| Type | Description |
|---|---|
| COMPLAINT | Beneficiary complaint — equipment pickup, billing dispute |
| ADR | Additional Documentation Request — records to support claim |
| OVERPAYMENT | Payer demanding repayment with interest timeline |
| AUDIT | Pre/post-payment audit — records review required |
| DENIAL | Claim denial with appeal window |
| GENERAL | Informational correspondence |

---

## Design Decisions

| Choice | Rationale |
|---|---|

| JSON-first extraction | Enables downstream use: dashboards, trackers, alerts |
| Two-pass architecture | Separate extraction from response generation for cleaner outputs |
| Synthetic samples built-in | Enables live demo without any real provider data |
| Priority classification | Mirrors real compliance triage logic (deadline + dollar amount) |

---

## Potential Extensions

- **Batch processing** — analyze a folder of letters, output summary dashboard
- **Deadline tracker** — parse dates, calculate days remaining, sort by urgency
- **Streamlit UI** — drag-and-drop letter upload with visual priority queue
- **Appeal letter generator** — extend to full ADR appeal with medical necessity arguments
- **Multi-payer support** — extend beyond Medicare to Medicaid MACs and commercial payers

---

## Tech Stack

- Python 3.9+
- [Anthropic Python SDK](https://github.com/anthropic/anthropic-sdk-python)


---

## Author

**Durga Meduri** — Business Analytics Manager | MS Business Analytics, UMass Boston  
Built from direct observation of compliance workflows in healthcare operations.  
[LinkedIn](https://www.linkedin.com/in/durga-c-meduri/) | [GitHub](https://github.com/Chidvy)
