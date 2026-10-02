# Final Demo Script (Target: 5–6 minutes)

The instructor asks for a 5 ± 3 minute video with the presenter’s face and the computer or mobile screen visible. Keep the camera and screen visible together. Do not show or read the API key. Rehearse once with the PDFs already indexed; use a question that produces a clear source citation.

| Time | Show | Suggested narration |
|---|---|---|
| 0:00–0:35 | Face on camera, then app title | “I built a PE6201 course-materials assistant for a student who remembers a concept but not which lecture or exercise page explains it. Its goal is to return evidence the student can check, not to act autonomously.” |
| 0:35–1:05 | Library count and indexed-material list | “The current local corpus has nine PDFs and 221 searchable passages. PDFs are parsed locally; scanned content and complex diagrams remain limitations.” |
| 1:05–2:15 | Select `Week 4 Exercise.pdf`; ask: “What three request types does the appointment-email exercise handle?” | “The source filter narrows retrieval to a known exercise file. The answer summarizes the exercise wording and points to a source ID.” |
| 2:15–2:50 | Scroll to `[S1]` and inspect its source page | “I can verify the answer against the original passage and page. When all files are searched, lecture notes may use different but related wording, so source choice can affect the phrasing.” |
| 2:50–3:40 | Ask a question and leave the model consent box unchecked; show a local answer or an abstention | “The default mode stays local. If the passages do not provide enough evidence, the assistant can abstain instead of guessing.” |
| 3:40–4:20 | Optional: ask one question with consent checked, only if the API key is configured and the course material may be sent | “The LLM is an optional synthesis layer. The student explicitly authorizes sending the question and retrieved excerpts; the app records spend and enforces its own budget stop.” |
| 4:20–5:10 | Briefly show evaluation guide / result table | “I compare local retrieval with the optional model. The test set is small, answerability accuracy is not factual correctness, and token F1 is only a lexical proxy. Citation and answer judgments need a larger, independently checked set.” |
| 5:10–5:40 | Face on camera for closing | “The project’s difference from a generic agent is course-specific retrieval, visible evidence, and an abstention path. The next improvement is stronger human-checked answer and citation evaluation.” |

## Recording checklist

- Keep face and screen visible at the same time; ensure text and citations are readable.
- Use a steady pace and explain one complete question-to-evidence path.
- If using OpenRouter, check course-material permissions first and show consent only for that demonstration. Never reveal the key or unrelated account details.
- State the scope honestly: nine PDFs indexed, not the full 500+ slide course corpus.
- Keep the final video between 2 and 8 minutes; target approximately 5½ minutes.
- Confirm the video file is included in the submission location. The recording itself must be made by the student.
