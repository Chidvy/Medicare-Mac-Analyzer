\# Earnings Report Analyzer



A command-line tool that uses \*\*Claude (Anthropic)\*\* to extract structured financial metrics and generate analyst-style narratives from earnings report PDFs — with an interactive Q\&A interface.



Built as a practical exploration of LLM-powered document analysis applied to financial data.



\---



\## What It Does



Given any earnings report or earnings call transcript (PDF or raw text), the tool:



1\. \*\*Extracts structured metrics\*\* — revenue, EPS, YoY changes, beats/misses vs estimates, guidance, key themes, risks

2\. \*\*Writes an analyst narrative\*\* — 3-paragraph sell-side style summary with specific figures

3\. \*\*Opens interactive Q\&A\*\* — ask natural language questions about the document, with multi-turn conversation memory



All powered by Claude's `claude-haiku-4-5` model via the Anthropic API.



\---



\## Demo



```

$ python earnings\_analyzer.py apple\_q4\_2024.pdf



============================================================

&#x20; EARNINGS REPORT ANALYZER  |  Powered by Claude

============================================================



&#x20; Loading PDF: apple\_q4\_2024.pdf

&#x20; Extracted 42,891 characters from 18 pages.



\[1/2] Extracting structured metrics...

\[2/2] Writing analyst narrative summary...



============================================================

STRUCTURED EXTRACTION

============================================================

Company:    Apple Inc.

Period:     Q4 FY2024

Revenue:    $94.9B

&#x20; YoY:      +6.1%

&#x20; vs Est:   Beat by \~$1.2B



EPS:        $1.64

&#x20; YoY:      +12%

&#x20; vs Est:   Beat



Key Metrics:

&#x20; • Services Revenue: $24.97B — Record quarter, up 12% YoY

&#x20; • iPhone Revenue: $46.2B — Up 6% YoY

&#x20; • Mac Revenue: $7.7B — Up 2% YoY



Guidance:

&#x20; Next Q:   Revenue in the range of $89B–$93B



Key Themes: Services growth | AI integration | Emerging markets

Risks:      China competition | Regulatory pressure

Mgmt Tone:  Bullish — Management emphasized record Services performance and AI-driven product roadmap



============================================================

ANALYST SUMMARY

============================================================

Apple reported strong fourth-quarter results, with revenue of $94.9B exceeding consensus by approximately 

$1.2B and EPS of $1.64 beating estimates by $0.08...



\[continues...]



============================================================

Q\&A Mode — Ask anything about Apple's earnings

Type 'exit' or 'quit' to stop.



You: What drove the Services beat?

Analyst: Services revenue of $24.97B, a record quarter, was driven by growth across the App Store,

Apple Music, iCloud, and AppleCare. Management cited 1B+ paid subscriptions globally...

```



\---



\## Setup



\*\*Requirements:\*\* Python 3.9+, Anthropic API key (\[get one here](https://console.anthropic.com))



```bash

\# Clone the repo

git clone https://github.com/yourusername/earnings-analyzer.git

cd earnings-analyzer



\# Install dependencies

pip install -r requirements.txt



\# Set your API key

export ANTHROPIC\_API\_KEY=your\_key\_here

\# Or copy .env.example to .env and fill it in

```



\---



\## Usage



```bash

\# Analyze a PDF (full workflow: extract + summarize + Q\&A)

python earnings\_analyzer.py report.pdf



\# Skip the interactive Q\&A

python earnings\_analyzer.py report.pdf --no-qa



\# Save structured JSON output

python earnings\_analyzer.py report.pdf --output results.json



\# Analyze raw text instead of a PDF

python earnings\_analyzer.py --text "Revenue was $5.2B, up 12% YoY..."

```



\*\*Where to get earnings PDFs:\*\*

\- \[SEC EDGAR](https://www.sec.gov/cgi-bin/browse-edgar) — search any public company, look for 10-Q/10-K filings

\- Company investor relations pages (e.g. Apple, Microsoft, J\&J, CVS Health)

\- Earnings call transcripts from \[Motley Fool](https://www.fool.com/earnings-call-transcripts/) (copy/paste text)



\---



\## Example JSON Output



```json

{

&#x20; "structured\_metrics": {

&#x20;   "company": "Apple Inc.",

&#x20;   "period": "Q4 FY2024",

&#x20;   "revenue": {

&#x20;     "actual": "$94.9B",

&#x20;     "yoy\_change": "+6.1%",

&#x20;     "vs\_estimate": "Beat by \~$1.2B"

&#x20;   },

&#x20;   "earnings\_per\_share": {

&#x20;     "actual": "$1.64",

&#x20;     "yoy\_change": "+12%",

&#x20;     "vs\_estimate": "Beat"

&#x20;   },

&#x20;   "key\_metrics": \[...],

&#x20;   "guidance": {...},

&#x20;   "key\_themes": \[...],

&#x20;   "management\_tone": "Bullish — ..."

&#x20; },

&#x20; "narrative\_summary": "Apple reported strong fourth-quarter results..."

}

```



\---



\## Design Decisions



| Choice | Rationale |

|---|---|

| `claude-haiku-4-5` model | Fast and cost-effective for document extraction tasks |

| Two-pass architecture | Separate structured extraction from narrative generation for cleaner outputs |

| 80K char truncation | Stays safely within context limits while covering most earnings docs |

| Multi-turn Q\&A | Maintains conversation history to support follow-up questions |

| JSON-first extraction | Structured output enables downstream use (dashboards, alerts, comparisons) |



\---



\## Potential Extensions



\- \*\*Batch processing\*\* — run across multiple quarters and track metric trends over time

\- \*\*Comparison mode\*\* — compare two companies' earnings side-by-side

\- \*\*Alerts\*\* — flag when guidance misses consensus by a threshold

\- \*\*Healthcare variant\*\* — adapt extraction schema for clinical trial readouts or hospital earnings (CMS reporting)

\- \*\*Streamlit UI\*\* — drag-and-drop PDF interface with charts



\---



\## Tech Stack



\- Python 3.9+

\- \[Anthropic Python SDK](https://github.com/anthropic/anthropic-sdk-python)

\- \[pypdf](https://github.com/py-pdf/pypdf) for PDF text extraction



\---



\## Author



\*\*Durga Meduri\*\* — Business Analytics Manager | MS Business Analytics, UMass Boston  



