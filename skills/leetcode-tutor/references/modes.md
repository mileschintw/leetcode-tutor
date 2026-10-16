# Mode switching

Two situations where the tutor departs from the full four-phase flow.

## Trivial brute force

**Trigger:** the brute-force approach is obvious, such as checking every pair with nested loops in O(n²).

**Action:** don't make the learner code or explain it. Acknowledge it in one line ("We could check every pair in O(n²)...") and move straight to optimisation ("...but how can we bring that down to O(n)?").

## Recap Mode

**Trigger:** the learner says they already know the Problem, asks for a quick recap, or is reviewing for an interview.

**Action:** suspend the multi-phase Socratic flow. Instead:

1. When the Problem has a `notes.md` in the Practice Workspace, read it first (see "Returning to a Problem" in [practice-workspace.md](practice-workspace.md)) and mention the past Attempts in a line.
2. Give the 📋 Problem Analysis section and the 🎯 Solution Strategies & Comparison section of the First Response (see [first-response.md](first-response.md)).
3. Ask the learner to state the 🔑 One-Sentence Key Takeaway from memory, and end the reply on that question. Don't quote or paraphrase the stored Key Takeaway before they answer; naming the approaches in the comparison table is fine.
4. Confirm or correct their recall against the stored Key Takeaway (or your own, for a Problem with none), naming what they missed.
5. Offer the optimal code skeleton, or discuss edge cases directly. In Recap Mode you may write the solution.
6. Keep the exchange fast and focused on recall.
7. Record a `mode: recap` Attempt (step 5 in `SKILL.md`). Judge its `outcome` by the recall, not by the code you showed:
   - `solved-alone`: they stated the Key Takeaway correctly without help.
   - `solved-with-hints`: they got it after a correction or a nudge.
   - `saw-solution`: they couldn't recall it and you gave it. This marks the Problem Need Review.

   A recap Attempt never clears Need Review, even when it is `solved-alone` (see [need-review.md](need-review.md)).

   Its code file holds the optimal code from the recap: the learner's, if they wrote or pasted any, otherwise the code you showed. Without any, write the optimal solution in the learner's programming language from their earlier Attempts, so the Attempt has a code file. `mistakes` names what the recall missed.
