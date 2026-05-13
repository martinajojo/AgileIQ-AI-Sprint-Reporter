# AgileIQ — AI-Powered Sprint Reporter

A Python tool that converts raw daily standup notes into a 
formatted sprint status report using the Google Gemini API.

Built as a portfolio project by Martina Jojo to demonstrate 
end-to-end PM/BA and AI automation skills.

---

## What It Does

Paste your team's standup notes in → get a structured sprint 
report out.

The tool:
- Generates a weekly sprint summary in seconds
- Flags blockers automatically (keywords: blocked, delay, 
  dependency, waiting on)
- Outputs a RAG status (Red / Amber / Green) ready for 
  stakeholders
- Reduces manual reporting time from ~60 minutes to ~8 minutes

---

## How It Works

1. You paste standup notes into the script
2. The script scans for blockers using keyword detection
3. It sends the notes + a structured prompt to the Gemini API
4. Gemini returns a formatted report with: Sprint Summary, 
   Blockers Flagged, RAG Status, and Recommendations
5. Output is printed to terminal (and optionally sent to Slack 
   via OttoKit automation)

---

## Tech Stack

| Tool        | Purpose                        |
|-------------|--------------------------------|
| Python      | Core scripting                 |
| Gemini API  | AI report generation           |
| OttoKit     | Automation / webhook trigger   |
| Slack       | Report delivery channel        |
| GitHub      | Version control + portfolio    |

---

## Project Status

🔄 In Progress — Phase 3 of 4 (AI Build)

Phase 1: BA Discovery ✅  
Phase 2: PM Planning ✅  
Phase 3: AI Build 🔄  
Phase 4: Metrics & Portfolio ⬜  

---

## Portfolio

This project is part of a full PM/BA portfolio.  
Full documentation, process maps, Jira boards, and a live 
demo are available at: [Portfolio link coming soon]

---

*Built by Martina Jojo | Associate PM / BA — Software & Tech*
