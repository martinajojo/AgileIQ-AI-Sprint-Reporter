# =============================================================================
# AgileIQ — AI-Powered Sprint Intelligence System
# Author: Martina Jojo
# Version: 1.0
# Phase: Phase 3 — AI Build
# Description: Sends sprint standup notes to Google Gemini API and generates
#              a structured, stakeholder-ready sprint status report.
# =============================================================================

import google.generativeai as genai
import os

# =============================================================================
# SECTION 1: CONFIGURATION
# =============================================================================

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise EnvironmentError(
        "GEMINI_API_KEY environment variable not set. "
        "Please set it before running this script."
    )

genai.configure(api_key=GEMINI_API_KEY)

# =============================================================================
# SECTION 2: INPUT — Simulated Sprint Standup Notes
# =============================================================================
# This represents one week of daily standup notes from a 5-person Agile team
# working on Sprint 2 of a fictional SaaS product (InvoiceFlow v2.0).
# In production, this string would be populated via webhook from OttoKit.
# =============================================================================

standup_notes = """
SPRINT 2 — WEEK 2 STANDUP NOTES
Project: InvoiceFlow v2.0
Sprint Dates: 5 May 2026 – 16 May 2026
Compiled by: PM (Martina Jojo)

---

MONDAY 11 MAY 2026

Aiden (Backend Developer):
- Yesterday: Completed the invoice generation endpoint (US-14). All unit tests passing.
- Today: Starting integration with the payment gateway module.
- Blockers: None.

Priya (Frontend Developer):
- Yesterday: Finished responsive layout for the invoice dashboard. Tested on mobile and tablet.
- Today: Starting work on the PDF export button (US-17).
- Blockers: Waiting on the final PDF template design from the design team — blocked on this since last Thursday. Cannot proceed with US-17 until the template is approved.

Callum (QA Engineer):
- Yesterday: Completed regression testing for Sprint 1 features. Found 2 minor UI bugs — logged in Jira.
- Today: Setting up the test plan for the payment gateway flow.
- Blockers: None currently, but flagging a potential dependency — QA for the payment gateway cannot start until Aiden's integration is complete, expected mid-week.

Sasha (UX/UI Designer):
- Yesterday: Finalised the onboarding flow wireframes for Phase 2 scope.
- Today: Working on the PDF invoice template Priya is waiting on. Aiming to have it ready by end of day.
- Blockers: None.

Riya (Product Owner):
- Yesterday: Stakeholder review call — feedback received on the invoice numbering format. Client wants sequential numbering with prefix (e.g., INV-0001).
- Today: Updating the acceptance criteria for US-14 to reflect the new numbering format. Will share with Aiden today.
- Blockers: None. But flagging: if the numbering format change requires backend schema changes, this could impact the Sprint 2 deadline.

---

TUESDAY 12 MAY 2026

Aiden (Backend Developer):
- Yesterday: Started payment gateway integration. Hit an issue with the sandbox credentials — the third-party vendor hasn't sent the updated keys yet.
- Today: Blocked — cannot progress on payment gateway integration until we receive sandbox credentials from StripeConnect. Raised a support ticket yesterday (ticket #SC-4421). Estimated resolution: 24–48 hours.
- Blockers: BLOCKED on StripeConnect sandbox credentials (external dependency). Risk to Sprint goal if not resolved by Wednesday.

Priya (Frontend Developer):
- Yesterday: Sasha delivered the PDF template — reviewed and approved. Starting US-17 implementation.
- Today: Continuing PDF export button. Integrating the template into the front end.
- Blockers: None.

Callum (QA Engineer):
- Yesterday: Test plan for payment gateway drafted. Shared with Aiden for review.
- Today: Reviewing Aiden's unit tests for US-14. Also monitoring the blocker on payment gateway — QA timelines will slip if resolution is delayed past Wednesday.
- Blockers: Indirect dependency on StripeConnect credentials via Aiden's work.

Sasha (UX/UI Designer):
- Yesterday: Delivered PDF invoice template to Priya. Starting sprint 3 discovery work.
- Today: User research interviews for Phase 2 features.
- Blockers: None.

Riya (Product Owner):
- Yesterday: Updated acceptance criteria for US-14 with new invoice numbering format. Confirmed with Aiden — no schema changes needed, just formatting logic.
- Today: Grooming backlog for Sprint 3. Reviewing stakeholder feedback document.
- Blockers: None.

---

WEDNESDAY 13 MAY 2026

Aiden (Backend Developer):
- Yesterday: Still blocked on StripeConnect credentials. Escalated via PM to our account manager.
- Today: Using blocker time productively — refactoring the invoice numbering logic per Riya's updated acceptance criteria.
- Blockers: Still blocked on StripeConnect (Day 2). PM to escalate further if not resolved by end of day.

Priya (Frontend Developer):
- Yesterday: PDF export button implemented. Testing in staging environment now.
- Today: Fixing a formatting issue — decimal alignment in the invoice line items is off on Firefox. Minor but needs resolving before demo.
- Blockers: None.

Callum (QA Engineer):
- Yesterday: Reviewed US-14 unit tests. All passing. Starting exploratory testing on the invoice dashboard.
- Today: Continuing exploratory testing. Will begin payment gateway test cases as soon as Aiden's integration is unblocked.
- Blockers: Still dependent on StripeConnect resolution before QA can begin payment gateway testing.

Sasha (UX/UI Designer):
- Yesterday: Completed 3 user research interviews. Key insight: users want a 'Duplicate Invoice' feature — logging as a backlog item for Sprint 4.
- Today: Writing up research findings for the Product Owner.
- Blockers: None.

Riya (Product Owner):
- Yesterday: Reviewed Sprint 3 backlog. Added 6 new user stories. Shared with team for sizing in Thursday's refinement session.
- Today: Following up on the StripeConnect escalation with the vendor relationship manager.
- Blockers: None — but Sprint 2 goal is at amber risk if payment gateway isn't unblocked today.
"""

# =============================================================================
# SECTION 3: PROMPT ENGINEERING — System Prompt for Gemini
# =============================================================================
# This prompt defines Gemini's role, output structure, and quality rules.
# It is the core intelligence layer of AgileIQ.
# Well-crafted prompts produce consistent, stakeholder-ready reports.
# =============================================================================

SYSTEM_PROMPT = """
You are AgileIQ — an expert AI Sprint Reporting Assistant embedded in an Agile software team.

Your role is to analyse raw sprint standup notes provided by the Project Manager and produce a clear, professional, stakeholder-ready Weekly Sprint Status Report.

You must follow these rules without exception:
1. Base your report ONLY on what is explicitly stated in the standup notes. Do not invent or assume information.
2. Use professional business language. Avoid jargon. Write for an executive audience.
3. Flag every blocker, risk, and dependency explicitly — these are the most critical items for stakeholders.
4. Apply RAG (Red / Amber / Green) status with precision:
   - RED: Sprint goal is at immediate risk. A blocker is active and unresolved with no clear resolution timeline.
   - AMBER: Sprint goal may be at risk. A blocker exists but is being managed, or a risk has been flagged but not yet materialised.
   - GREEN: Sprint is on track. No active blockers. Delivery is expected as planned.
5. Be concise. Each section should be readable in under 60 seconds.
6. Always include a Recommendations section with at least 2 specific, actionable items for the PM.

OUTPUT FORMAT — You must produce the report in exactly this structure:

---

# AgileIQ Weekly Sprint Status Report
**Project:** [Extract from notes]
**Sprint:** [Extract from notes]
**Report Period:** [Extract from notes]
**Generated by:** AgileIQ AI Sprint Intelligence System

---

## 1. Sprint Summary
A 3–5 sentence narrative overview of the sprint week. Cover overall progress, team activity, and general health. Do not list every task — synthesise the pattern.

---

## 2. Team Progress Snapshot
A brief bullet for each team member (Name — Role: one sentence on their week's progress).

---

## 3. Blockers Flagged 🚨
For each blocker identified:
- **[Team Member / Area]:** Description of the blocker.
  - Status: Active / Escalated / Resolved
  - Impact: What does this block? Which user stories or sprint goals are affected?
  - Days Active: [Number]
  - Owner: Who is responsible for resolution?

If no blockers: write "No active blockers this week."

---

## 4. Risks & Dependencies ⚠️
List any flagged risks or inter-team dependencies that are not yet blockers but could become ones. Include likelihood and potential impact.

---

## 5. RAG Status
**Overall Sprint RAG: [RED / AMBER / GREEN]**
**Justification:** A 2–3 sentence explanation of why this RAG status was assigned, referencing specific evidence from the standup notes.

---

## 6. Recommendations
Numbered list of 2–4 specific, actionable recommendations for the PM or Scrum Master. Be direct. Each recommendation should name the action, the owner, and the timeframe.

---

## 7. Next Steps
2–3 bullet points summarising the most critical items to resolve or monitor in the coming week.

---
"""

# =============================================================================
# SECTION 4: AI CALL — Send Notes to Gemini and Generate Report
# =============================================================================

def generate_sprint_report(notes: str, system_prompt: str) -> str:
    """
    Sends standup notes to Google Gemini and returns a formatted sprint report.

    Args:
        notes: The raw standup notes string.
        system_prompt: The structured prompt defining output format and rules.

    Returns:
        The AI-generated sprint status report as a string.
    """
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_prompt
    )

    # Construct the user message — clear instructions with the raw data
    user_message = f"""
Please analyse the following sprint standup notes and produce a Weekly Sprint Status Report 
following the format and rules in your instructions.

STANDUP NOTES:
{notes}
"""

    print("Sending standup notes to Gemini API...")
    print("=" * 60)

    response = model.generate_content(user_message)

    return response.text


# =============================================================================
# SECTION 5: OUTPUT — Print Report to Terminal + Save to File
# =============================================================================

if __name__ == "__main__":
    # Generate the report
    report = generate_sprint_report(standup_notes, SYSTEM_PROMPT)

    # Print to terminal
    print(report)

    # Save to a markdown file for portfolio evidence
    output_filename = "sprint_report_output.md"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(report)

    print("\n" + "=" * 60)
    print(f"✅ Report saved to: {output_filename}")
    print("✅ AgileIQ report generation complete.")