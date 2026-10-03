# Final Demo Video Script (Target: about 6½ minutes)

## Instructor requirements

- Target length: **5 minutes, with a ±3 minute allowance**. Keep the submitted video under 8 minutes; the instructor will review at most the first 8 minutes.
- Keep **your face and your computer or mobile screen visible together** while explaining the relevant parts of the demo.
- Be precise, articulate, and succinct. Demonstrate the product, explain the reasoning behind its design, and critique the results honestly.
- Show the app and evidence clearly. Do not reveal the API key, private account details, or unrelated personal information.
- The presenter must record the video and check the video file into the submission location.

## Before recording

1. Start the app and confirm the indexed files and quiz page load. Keep the nine PDFs indexed so the demo does not spend time uploading.
2. Arrange the camera and screen side by side or in a picture-in-picture layout. Check that the presenter’s face is visible and that citations and text on the screen can be read.
3. Rehearse the Week 4 question once: **“What three request types does the appointment-email exercise handle?”** Select `Week 4 Exercise.pdf` before asking it.
4. Prepare to show the answer, its citation, and the matching source excerpt/page. Have a separate local-only question ready in case the optional model call fails.
5. Only demonstrate the OpenRouter option if the key is configured and course-material sharing is permitted. The key itself must never appear in the recording.

## Narration and screen plan

| Time | What to show | Suggested narration |
|---|---|---|
| 0:00–0:35 | Face and app title, with both visible | “Hello, I’m presenting my PE6201 Course Materials Q&A Assistant. I built it for a student who remembers a topic but not which lecture or exercise page explains it. The goal is to reduce the time spent searching and make the evidence easy to check. I have not yet measured whether it improves grades or learning outcomes, so I will focus on what the prototype demonstrates.” |
| 0:35–1:15 | App overview and indexed-material counts | “The current local index contains nine course PDFs, 215 pages, and 221 searchable passages. The app extracts text locally, organizes it by file and page, and lets the student search across the corpus or restrict a question to a known PDF. This source filter is useful because lecture notes and exercises can describe the same topic in different ways.” |
| 1:15–2:35 | Select `Week 4 Exercise.pdf`; ask the prepared question; show answer and citation | “I’ll limit the search to the Week 4 exercise and ask: ‘What three request types does the appointment-email exercise handle?’ The app retrieves passages from the selected file and returns the answer with a source reference. The answer shown here is confirm, cancel, and reschedule. I can inspect the cited excerpt and page, so I can check whether those words are actually supported by the course material. The citation matters because a fluent answer alone is not enough evidence.” |
| 2:35–3:15 | Scroll to the cited passage; optionally switch to all PDFs | “If I search all files, the system may retrieve lecture notes that use related wording. Restricting the source is helpful when I know where the answer should be, while all-course search is useful when I do not. A citation points me to the evidence, but it does not guarantee that every generated sentence is correct; the student still needs to verify the passage.” |
| 3:15–3:55 | Show the local-only path or an unanswerable query; keep consent unchecked | “By default, the app works locally and selects extractive text from the retrieved passages. If there is not enough evidence, its answer path can abstain rather than inventing a course fact. This is a deliberate design choice: the tool should help locate material, not pretend that every question has a supported answer.” |
| 3:55–4:35 | Generate a quiz; show the course, direction, scenario, focus, and question | “The quiz is designed for active recall, but a broad prompt like ‘What is the main idea?’ gives too little guidance. Each item now shows the week and material type, the question direction, the operation scenario, and the exact knowledge point. For example, a Week 4 appointment-automation question is framed around reading a customer email, checking appointment records, and preparing a reply. The student knows which process and concept the question refers to before answering.” |
| 4:35–5:15 | If permitted, demonstrate the separate OpenRouter consent option; otherwise show its explanation without sending | “There is also an optional OpenRouter path. It is separate from the local mode and only runs after the student checks this consent box. The app sends the question and selected excerpts, not the original PDF files. I would only use this option when sharing the course text is permitted. The app tracks its own API spend and stops requests at its configured limit. I will not show the API key.” |
| 5:15–6:10 | Show the evaluation guide or evaluation results | “I evaluated the system on 68 questions: 46 development cases and 22 held-out test cases. On the test split, the local answerability gate had 0.88 precision and 0.94 recall, and evidence-page Hit at 4 was 1.00. In the optional model comparison, 22 of 22 answerability decisions matched the labels, 15 of 16 answerable questions cited the exact gold page, and mean reference-token F1 was 0.548 compared with 0.224 for the local baseline. These numbers have important limits: 22 test questions are a small sample; answerability accuracy is not factual correctness; token F1 measures word overlap, not meaning; and a valid supporting page can differ from the single gold page.” |
| 6:10–6:50 | Briefly show product architecture/report, then return to face and app | “The project differs from a generic agent by keeping the workflow focused on course materials: local indexing, retrieval, source filtering, citations, abstention, and a context-rich revision quiz. The main rough edges are PDF extraction for tables and diagrams, keyword-based retrieval and self-checking, and the small evaluation set. My next steps would be to add independently written questions, allow multiple acceptable evidence pages, and have a human review whether each answer is actually supported. Thank you.” |

## Recording checklist

- [ ] Face and screen remain visible together during the explanation.
- [ ] Face is clearly visible; app text and source citations are readable.
- [ ] The video is concise and under 8 minutes; aim for roughly 6–7 minutes.
- [ ] Show one complete question → retrieval → cited evidence path.
- [ ] Explain the quiz’s course/topic/scenario context.
- [ ] Report metrics with their caveats; do not claim measured learning gains.
- [ ] Do not expose API keys or unrelated account information.
- [ ] Confirm the final video file is included in the submission location.
