"""
Medicare MAC Letter Analyzer
Analyzes CMS/MAC correspondence letters and generates structured triage + response drafts.
Built using the Anthropic Claude API.

IMPORTANT: This tool is for demonstration purposes only.
Use only with synthetic or de-identified data. Never input real PHI.
"""

import anthropic
import os
import json
import sys
from datetime import datetime


LETTER_TYPES = {
    "COMPLAINT": "Beneficiary or third-party complaint requiring pickup, correction, or response",
    "ADR": "Additional Documentation Request — payer requesting medical records to support a claim",
    "OVERPAYMENT": "Payer identified overpayment and is requesting repayment",
    "AUDIT": "Pre or post-payment audit of claims — records review required",
    "DENIAL": "Claim denied — appeal window open",
    "GENERAL": "General correspondence or informational notice"
}


SYNTHETIC_SAMPLES = {
    "1": {
        "name": "Beneficiary Complaint (DME Equipment)",
        "text": """CGS
Jurisdiction B
P.O. Box 20007
Nashville, TN 37202

MEDICARE DME

October 9, 2025

Sunrise Medical Supply Corp
400 Commerce Drive
Providence, RI 02903

John D. Sample / XXXXXXXXXNA99
DCN: SYNTH-2025-0042

Dear Sunrise Medical Supply Corp:

Correspondence was received by CGS, the Jurisdiction B Durable Medical Equipment Medicare
Administrative Contractor (DME MAC) from the above-mentioned Medicare beneficiary.
According to the beneficiary, your company provided a L0651 (orthotic equipment) on June 10th, 2025.
The beneficiary requested that your company pick up the item. We request that you comply
with the beneficiary's request and pick up the equipment within 30 calendar days of receipt of this
letter. Once the item has been obtained, please fax a copy of the pick-up documentation along with
this letter to the attention of the Complaint Screening department at 615-782-4624.

Your cooperation and prompt reply are appreciated. If you have any questions, please contact our
Customer Service department at 866-590-6727.

Sincerely,
CGS DME MAC Jurisdiction B"""
    },
    "2": {
        "name": "Additional Documentation Request (ADR)",
        "text": """Novitas Solutions
Medicare Administrative Contractor
P.O. Box 3000
Mechanicsburg, PA 17055

ADDITIONAL DOCUMENTATION REQUEST

November 14, 2025

Sunrise Medical Supply Corp
400 Commerce Drive
Providence, RI 02903

Beneficiary: Mary T. Example / XXXXXXXXXMB12
DCN: SYNTH-2025-0891
Claim Number: SYNTH-CLM-20251101
Date of Service: October 1, 2025
HCPCS Code: E1390 (Oxygen Concentrator)
Amount at Risk: $1,847.20

Dear Provider:

We are requesting medical documentation to support the above referenced claim.
Please submit the following records within 45 days of this letter:

- Physician certificate of medical necessity (CMN)
- Most recent qualifying blood gas study or oximetry results
- Office notes supporting medical necessity from the treating physician
- Delivery confirmation and beneficiary signature

Failure to respond within 45 days will result in claim denial.
Submit records to: ADR Processing, P.O. Box 3000, Mechanicsburg, PA 17055

Questions: 1-855-609-9960

Sincerely,
Novitas Solutions Medicare ADR Department"""
    },
    "3": {
        "name": "Overpayment Demand Letter",
        "text": """CGS
Jurisdiction B
P.O. Box 20007
Nashville, TN 37202

MEDICARE OVERPAYMENT NOTICE

December 1, 2025

Sunrise Medical Supply Corp
400 Commerce Drive
Providence, RI 02903

DCN: SYNTH-2025-1204
Overpayment Reference: OVP-2025-00334
Claims Period: January 1, 2025 – June 30, 2025
Total Overpayment Amount: $12,450.00

Dear Provider:

A review of your Medicare claims has identified an overpayment of $12,450.00
for the period referenced above. The overpayment was identified due to:

- Claims billed for HCPCS E0601 (CPAP) without required prior authorization
- Duplicate billing identified on 3 claims (dates of service: Feb 4, Mar 17, May 22)

You must repay this amount within 30 days to avoid interest accrual under
31 U.S.C. 3717 at the current rate of 10.875% per annum.

Options:
1. Submit voluntary repayment via check payable to: CGS Medicare
2. Request an extended repayment plan (ERP) for amounts over $3,000
3. File a redetermination request if you disagree with this finding

Questions: 866-590-6727

Sincerely,
CGS Overpayment Recovery Unit"""
    }
}


def analyze_letter(client: anthropic.Anthropic, letter_text: str) -> dict:
    """Send letter to Claude for structured extraction and classification."""

    prompt = f"""You are a Medicare compliance specialist at a DME/home health provider.
Analyze the following Medicare MAC correspondence letter and return ONLY valid JSON with no markdown formatting.

Return this exact structure:
{{
  "letter_type": "COMPLAINT | ADR | OVERPAYMENT | AUDIT | DENIAL | GENERAL",
  "mac_contractor": "Name of the MAC/contractor who sent the letter",
  "jurisdiction": "Jurisdiction letter if mentioned",
  "dcn": "Document Control Number if present",
  "beneficiary_id": "Masked or partial ID only — do not extract full IDs",
  "hcpcs_code": "HCPCS code and description if mentioned",
  "date_of_service": "Date of service if mentioned",
  "amount_at_risk": "Dollar amount at risk if mentioned, else null",
  "response_deadline_days": "Number of days to respond as integer, else null",
  "required_actions": ["action 1", "action 2", "action 3"],
  "documents_needed": ["document 1", "document 2"],
  "priority": "HIGH | MEDIUM | LOW",
  "priority_reason": "One sentence explaining the priority level",
  "fax_number": "Fax number to send response to if mentioned",
  "contact_phone": "Contact phone number if mentioned"
}}

Priority rules:
- HIGH: Overpayment demand, deadline under 30 days, claim denial with appeal window
- MEDIUM: ADR with 45-day window, complaint with 30-day window
- LOW: General correspondence, informational notices

Letter text:
{letter_text}"""

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip().rstrip("```").strip()

    return json.loads(raw)


def generate_response_letter(client: anthropic.Anthropic, letter_text: str, extracted: dict) -> str:
    """Generate a draft response letter based on the analysis."""

    prompt = f"""You are a Medicare compliance officer writing a professional response letter.

Based on this MAC letter analysis:
{json.dumps(extracted, indent=2)}

And the original letter:
{letter_text}

Write a professional, concise draft response letter that:
- Acknowledges receipt of the correspondence
- States the provider's intent to comply / respond
- Lists specific actions being taken
- Includes placeholder brackets for dates, signatures, and any specific details
- Is appropriately formal for Medicare correspondence

Use [PROVIDER NAME], [DATE], [CONTACT NAME], [SIGNATURE] as placeholders.
Keep it under 200 words. This is a draft — the compliance team will finalize it."""

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()


def print_analysis(extracted: dict, draft_response: str):
    """Print structured analysis to terminal."""

    priority_colors = {
        "HIGH": "*** HIGH PRIORITY ***",
        "MEDIUM": "** MEDIUM PRIORITY **",
        "LOW": "* LOW PRIORITY *"
    }

    print(f"\n{'='*60}")
    print("  MEDICARE MAC LETTER ANALYSIS")
    print(f"{'='*60}")

    print(f"\nLETTER TYPE:    {extracted.get('letter_type', 'UNKNOWN')}")
    print(f"MAC/CONTRACTOR: {extracted.get('mac_contractor', 'N/A')}")
    print(f"JURISDICTION:   {extracted.get('jurisdiction', 'N/A')}")
    print(f"DCN:            {extracted.get('dcn', 'N/A')}")
    print(f"HCPCS CODE:     {extracted.get('hcpcs_code', 'N/A')}")
    print(f"DATE OF SVC:    {extracted.get('date_of_service', 'N/A')}")

    amount = extracted.get('amount_at_risk')
    if amount:
        print(f"AMOUNT AT RISK: {amount}")

    deadline = extracted.get('response_deadline_days')
    if deadline:
        print(f"DEADLINE:       {deadline} days from receipt")

    print(f"\n{priority_colors.get(extracted.get('priority', 'LOW'), '')}")
    print(f"  {extracted.get('priority_reason', '')}")

    actions = extracted.get('required_actions', [])
    if actions:
        print(f"\nACTION CHECKLIST:")
        for action in actions:
            print(f"  [ ] {action}")

    docs = extracted.get('documents_needed', [])
    if docs:
        print(f"\nDOCUMENTS TO PULL:")
        for doc in docs:
            print(f"  [ ] {doc}")

    fax = extracted.get('fax_number')
    phone = extracted.get('contact_phone')
    if fax or phone:
        print(f"\nCONTACT INFO:")
        if fax:
            print(f"  Fax:   {fax}")
        if phone:
            print(f"  Phone: {phone}")

    print(f"\n{'='*60}")
    print("  DRAFT RESPONSE LETTER")
    print(f"{'='*60}")
    print(draft_response)
    print(f"{'='*60}\n")


def save_output(extracted: dict, draft_response: str, filename: str = None):
    """Save analysis to JSON file."""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_{timestamp}.json"

    output = {
        "analyzed_at": datetime.now().isoformat(),
        "extracted_data": extracted,
        "draft_response": draft_response
    }

    with open(filename, "w") as f:
        json.dump(output, f, indent=2)

    print(f"  Saved to: {filename}")


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\nERROR: ANTHROPIC_API_KEY not set.")
        print("  Run: set ANTHROPIC_API_KEY=your_key_here  (Windows)")
        print("  Run: export ANTHROPIC_API_KEY=your_key_here  (Mac/Linux)")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    print(f"\n{'='*60}")
    print("  MEDICARE MAC LETTER ANALYZER  |  Powered by Claude")
    print("  NOTE: Use synthetic/demo data only. No real PHI.")
    print(f"{'='*60}\n")

    print("Choose input method:")
    print("  1. Use a synthetic sample letter (demo)")
    print("  2. Paste your own letter text")
    print()

    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        print("\nAvailable sample letters:")
        for key, sample in SYNTHETIC_SAMPLES.items():
            print(f"  {key}. {sample['name']}")
        print()
        sample_choice = input("Choose sample (1/2/3): ").strip()
        if sample_choice not in SYNTHETIC_SAMPLES:
            print("Invalid choice. Using sample 1.")
            sample_choice = "1"
        letter_text = SYNTHETIC_SAMPLES[sample_choice]["text"]
        print(f"\nUsing: {SYNTHETIC_SAMPLES[sample_choice]['name']}\n")

    elif choice == "2":
        print("\nPaste your letter text below.")
        print("Type END on a new line when done:\n")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        letter_text = "\n".join(lines)

    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

    print("Analyzing letter...\n")

    extracted = analyze_letter(client, letter_text)
    draft = generate_response_letter(client, letter_text, extracted)

    print_analysis(extracted, draft)

    save_choice = input("Save analysis to JSON file? (y/n): ").strip().lower()
    if save_choice == "y":
        save_output(extracted, draft)

    print("\nDone.")


if __name__ == "__main__":
    main()