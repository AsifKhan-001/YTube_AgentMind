# Lecture Notes


---

# AI Agent Definition and Tool-Use Capabilities

## What is it?

**G-Eval** is a research-backed technique (2023 paper) for reliable **LLM-as-a-Judge** evaluation. It solves the high-variance problem of naive LLM judging by introducing two core innovations:

1. **Chain-of-Thought (CoT) decomposition** – Converts a high-level evaluation criterion into a detailed, step-by-step **evaluation constitution** (rule book) with explicit scoring rubrics.
2. **Probability-weighted scoring** – Instead of taking the single output token (e.g., "8"), it extracts log-probabilities of the top-k score tokens, normalizes them, and computes a weighted average (e.g., 7.84), yielding stable, deterministic scores across runs.

> The lecture focuses on **RAG application-quality evaluation** (correctness, completeness, style) using G-Eval via the DeepEval library. Previous sessions covered count-based metrics (recall, precision, faithfulness, answer relevance, context relevance); this session moves to judgment-based metrics.

## Why do we need it?

- **Count-based metrics fail for judgment tasks** – Style, correctness, completeness cannot be measured by breaking answers into claims and counting matches. They require holistic judgment.
- **Naive LLM-as-Judge is unreliable** – Two flaws:
  1. **Loose criteria** → LLM interprets the criterion differently each call → high score variance.
  2. **Direct token output** → Probabilistic token selection causes jumpy scores (e.g., 6 → 8 → 7) even with identical inputs.
- **G-Eval provides deterministic, repeatable evaluations** essential for regression testing and production monitoring.

## How does it work?

### G-Eval Pipeline (Step-by-Step)

1. **Define metric name & high-level criterion**  
   e.g., *Correctness*: "Compare actual answer against expected answer and decide factual correctness."
2. **CoT decomposition (auto or manual)**  
   LLM (preferably GPT-4) breaks the criterion into **evaluation steps** + **scoring rubric** (0–4, 5–8, 9–10 bands).
3. **Build judge prompt**  
   System prompt includes: role, evaluation steps, rubric, question, expected answer, actual answer.
4. **Extract log-probabilities**  
   Request top-k token log-probs for score tokens (0–10) from the judge model.
5. **Compute weighted score**  
   - Filter non-numeric tokens.  
   - Normalize probabilities of remaining numeric tokens to sum to 1.  
   - Calculate weighted average: Σ(score × probability).  
   - Divide by 10 → final 0–1 score.
6. **Threshold comparison**  
   Compare against threshold (e.g., 0.7) → PASS/FAIL.

### DeepEval Implementation Pattern

```python
# Define metric with explicit evaluation_steps and rubric
correctness = GEval(
    name="correctness",
    evaluation_steps=[...],  # detailed steps
    rubric={...},            # scoring bands
    model="gpt-4o-mini",
    threshold=0.7,
    strict_mode=False        # enables probability-weighted scoring
)

# Run evaluation loop
for q, expected in golden_dataset:
    actual = rag_pipeline(q)
    test_case = LLMTestCase(input=q, actual_output=actual, expected_output=expected)
    evaluate(test_cases=[test_case], metrics=[correctness])
```

### Iterative Refinement Loop

1. Run evaluation → analyze failures.
2. **Tighten evaluation steps** (e.g., "don't penalize brevity/omitted points").
3. **Add/Adjust rubric** (explicit score bands).
4. **Prompt-engineer generator** (e.g., "cover every distinct part of the question").
5. Re-run → scores stabilize and improve.

## Real World Example

**Scenario**: Evaluate a CampusX-style RAG chatbot on 15 golden questions.

| Metric       | Initial Score | After Refinement | Key Fix Applied |
|--------------|---------------|------------------|-----------------|
| Correctness  | 66%           | 84%              | Rubric: "don't deduct for brevity/omitted points" |
| Completeness | 68% (5 pass)  | 75% (14 pass)    | Generator prompt: "address all parts of multi-part questions" |
| Style        | 54%           | 74%              | Generator prompt: "conversational tone, intuition first"; Rubric: "analogy is bonus, not required" |

> **Insight**: Small, targeted prompt/rubric changes yield large metric gains. Prompt engineering directly improves evaluation scores.

## Important Points

- **Evaluation steps vs. Criterion**: Start with high-level criterion + CoT; once stable, **lock in explicit steps** to eliminate inter-call variance.
- **Rubric is control**: Explicit score bands (0–4, 5–8, 9–10) remove scoring discretion from the judge.
- **strict_mode=False** enables probability-weighted scoring; `True` reverts to unstable single-token output.
- **Golden dataset**: Human-expert written, universally correct answers (not limited to course content).
- **Faithfulness ≠ Correctness**: Faithful = grounded in context; Correct = factually true in the world. Ideal = both.
- **G-Eval works for any judgment metric**: Helpfulness, safety, tone, coherence, etc.

## Common Mistakes

- Using count-based logic (claims + ratio) for style/correctness/completeness.
- Providing only a one-line criterion → high variance.
- Omitting rubric → judge invents inconsistent scoring bands.
- Using `strict_mode=True` (direct token) → jumpy, unreliable scores.
- Not analyzing failure reasons before refining prompts/rubrics.
- Expecting 100% on all metrics; trade-offs exist (e.g., style vs. faithfulness).

## Interview Questions

1. **Why can't faithfulness/recall/precision methods evaluate "style" or "correctness"?**  
   They rely on claim-level counting; style/correctness are holistic judgments requiring whole-answer assessment.

2. **What are the two failure modes of naive LLM-as-a-Judge?**  
   (a) Loose criteria → inconsistent interpretation per call. (b) Direct token output → probabilistic score jitter.

3. **How does G-Eval's probability-weighted scoring reduce variance?**  
   It normalizes top-k score-token probabilities and computes a weighted average, smoothing token-level uncertainty.

4. **When should you supply explicit evaluation_steps vs. letting G-Eval generate them via CoT?**  
   Early exploration → use CoT on criterion. After 2–3 runs with clarity → lock in manual steps for determinism.

5. **Explain the rubric's role in G-Eval.**  
   It maps qualitative descriptions to numeric bands, removing scoring discretion and stabilizing output.

## Revision Notes

- **Count-based metrics**: Recall, Precision, Faithfulness, Answer Relevance, Context Relevance → claim breakdown + ratio.
- **Judgment-based metrics**: Correctness, Completeness, Style, Helpfulness, Safety → need LLM-as-Judge.
- **G-Eval innovations**: (1) CoT → evaluation constitution + rubric. (2) Log-prob weighted score → stable 0–1 output.
- **DeepEval GEval class**: `name`, `evaluation_steps`, `rubric`, `model`, `threshold`, `strict_mode=False`.
- **Refinement loop**: Run → read failure reasons → tighten steps/rubric → prompt-engineer generator → re-run.
- **Determinism goal**: Same inputs → same scores (±1–2%) across runs.


---

# Single-Agent vs Multi-Agent System Architecture

## What is it?

The lecture transcript provided does **not** cover Single-Agent vs Multi-Agent System Architecture. Instead, it focuses on **RAG Application Evaluation using G-Eval** for quality metrics (Correctness, Completeness, Style). The notes below reflect the actual transcript content.

## Why do we need it?

- **Problem**: Count-based metrics (Recall, Precision, Faithfulness, Answer Relevance, Context Relevance) work by breaking answers into claims and counting matches. This fails for **judgment-based metrics** like Correctness, Completeness, and Style where holistic assessment is needed.
- **LLM-as-a-Judge Issues**: Direct scoring (0-10) has high variance — same input yields different scores across runs due to:
  1. Loose criteria interpretation (LLM "thinks" differently each call)
  2. Token probability fluctuations (e.g., 7 vs 8 token probabilities shift)
- **Solution**: G-Eval provides **stable, deterministic evaluations** via two core innovations.

## How does it work?

### G-Eval Two Core Innovations

1. **Chain-of-Thought Evaluation Steps**  
   - Convert high-level criteria into a **structured rulebook** (evaluation steps + rubric) using CoT.
   - Removes ambiguity — same strict instructions sent every API call.

2. **Probability-Weighted Scoring**  
   - Instead of taking the max-probability token (e.g., "8"), extract top-k token log-probabilities (e.g., 7, 8, 9).
   - Normalize probabilities → compute weighted average → divide by 10 for 0-1 score.
   - Result: Scores vary minimally across runs (e.g., 7.84 → 7.79, not 6 → 8).

### Implementation Flow (DeepEval Library)

1. **Prepare Golden Dataset** — 15 Q&A pairs with universally correct answers.
2. **Run RAG Pipeline** — Generate actual answers for each question.
3. **Define G-Eval Metric** (e.g., `Correctness`):
   - Name, Criteria/Steps, Rubric, Judge Model (GPT-4o-mini), Threshold (0.7)
   - Optionally provide **pre-written evaluation steps + rubric** (skip CoT step for more determinism).
4. **Evaluate** — DeepEval builds judge prompt, calls model, extracts log-probs, computes weighted score, compares to threshold.
5. **Iterate** — Analyze failures → refine criteria/rubric or RAG prompts → re-run.

### Metric Examples from Transcript

| Metric | Purpose | Key Adjustment |
|--------|---------|----------------|
| **Correctness** | Factual accuracy vs gold answer | Rubric: Penalize only false claims; ignore brevity/omissions |
| **Completeness** | Covers all question parts | Generator prompt tweaked: "Address every distinct part of the question" |
| **Style** | Matches CampusX teaching tone | Rubric: Reward intuition-first, conversational, analogy-rich explanations; penalize robotic/jargon-heavy tone |

## Real World Example

> **Analogy**: Traditional LLM-as-a-Judge = Asking a grader "Rate this essay 0-10." They might give 7 today, 8 tomorrow.  
> **G-Eval** = Giving the grader a detailed rubric (step-by-step checks + score bands) AND asking for their confidence on each score bucket, then averaging. Grades become consistent.

## Important Points

- **Count-based vs Judgment-based**: Faithfulness/Recall = counting claims; Correctness/Style = holistic judgment.
- **G-Eval = Better LLM-as-a-Judge**: Adds structure (CoT steps) + statistical stability (log-prob weighting).
- **DeepEval Implementation**: `GEval` class accepts `evaluation_steps` + `rubric` for full control; `strict_mode=False` enables weighted scoring.
- **Prompt Engineering Matters**: Small generator prompt tweaks (e.g., "cover all parts") significantly boost Completeness/Style scores.
- **Threshold Tuning**: Default 0.7 may be harsh; adjust based on metric behavior.

## Common Mistakes

- Using raw LLM-as-a-Judge without CoT steps or rubric → high variance, unreliable scores.
- Expecting perfect scores on all metrics simultaneously — trade-offs exist (e.g., Style ↑ may hurt Faithfulness).
- Not analyzing failure reasons before refining criteria/rubric.
- Skipping log-prob weighted scoring (`strict_mode=True`) → back to unstable integer scores.

## Interview Questions

1. **Why do count-based metrics fail for Style or Correctness evaluation?**  
   Style/holistic correctness cannot be decomposed into independent claims; requires whole-answer judgment.

2. **What are the two core innovations of G-Eval?**  
   (1) CoT-generated evaluation steps/rubric for deterministic criteria. (2) Probability-weighted scoring using token log-probs instead of argmax token.

3. **How does G-Eval reduce score variance across runs?**  
   Fixed rulebook removes interpretation drift; weighted averaging smooths token probability noise.

4. **When should you provide custom `evaluation_steps` vs just a `criteria` string in G-Eval?**  
   After 2-3 pilot runs when you understand failure patterns; custom steps lock in the exact logic.

5. **How did the lecturer improve Completeness and Style scores?**  
   Completeness: Updated generator prompt to explicitly address all question parts. Style: Refined rubric to treat analogies as bonus (not mandatory) + adjusted generator tone instructions.

## Revision Notes

- **G-Eval** = Structured LLM-as-a-Judge for judgment-based metrics.
- **Two fixes**: (1) CoT → Evaluation Steps + Rubric (deterministic logic). (2) Log-prob weighted average (stable scoring).
- **DeepEval `GEval`**: Pass `evaluation_steps`, `rubric`, `model`, `threshold`. Set `strict_mode=False`.
- **Iterate**: Run → Analyze failures → Refine rubric/steps or RAG prompts → Re-run.
- **Metrics covered**: Correctness (factual), Completeness (coverage), Style (tone/pedagogy).
- **Key insight**: Prompt engineering on generator + evaluator both move metric scores.


---

# Multi-Agent System Benefits: Parallelization Specialization Scalability

## What is it?

**Note:** The provided transcript does not cover multi-agent systems, parallelization, specialization, or scalability. The lecture focuses on **RAG application evaluation** using **G-Eval** for judgment-based metrics (correctness, completeness, style). Below notes reflect the actual lecture content.

- **RAG Evaluation Pipeline**: Three-level offline evaluation suite (component, pipeline, application level)
- **G-Eval**: A research-backed technique (2023) that improves LLM-as-a-judge reliability using Chain-of-Thought evaluation steps and probability-weighted scoring
- **Judgment-based Metrics**: Metrics requiring holistic assessment (correctness, completeness, style, helpfulness, safety) rather than claim counting

## Why do we need it?

- **Count-based metrics fail** for style, correctness, completeness: Cannot break answers into independent claims (e.g., analogies only make sense in context)
- **Naive LLM-as-a-judge has high variance**: Same input yields different scores (6→8→7) due to:
  1. Loose criteria → inconsistent interpretation across calls
  2. Direct token scoring → probability fluctuations between adjacent scores
- **Need reliable, deterministic evaluation** for regression testing and production monitoring

## How does it work?

### G-Eval Two Core Innovations

1. **Criteria → Evaluation Steps (via Chain-of-Thought)**
   - Input: High-level criterion (e.g., "compare actual vs expected for factual correctness")
   - LLM (GPT-4) breaks it into **deterministic evaluation steps** (rubric/constitution)
   - Same steps used for every evaluation call → reduces interpretation variance

2. **Probability-Weighted Scoring (not direct token output)**
   - Extract top-k token log-probabilities for score tokens (0-10)
   - Filter non-numeric, normalize probabilities, compute weighted average
   - Example: P(8)=0.73, P(7)=0.21, P(9)=0.05 → Score = 7.84
   - Stable across runs (7.84 → 7.9, not 6→8)

### Implementation Flow (DeepEval)

1. Prepare **golden dataset**: Questions + universally correct answers
2. Run RAG pipeline → collect generated answers
3. Configure **GEval metric**:
   - Name, evaluation steps (or criteria), rubric, judge model (GPT-4o-mini), threshold
4. Evaluate → get weighted score, compare to threshold (pass/fail)
5. Iterate: Analyze failures → refine evaluation steps/rubric OR improve RAG prompts

### Metric Examples from Lecture

| Metric | Purpose | Key Configuration |
|--------|---------|-------------------|
| **Correctness** | Factual accuracy vs golden answer | Strict rubric: 0-4 (errors), 5-8 (minor issues), 9-10 (fully correct) |
| **Completeness** | Covers all question parts | Generator prompt tuned: "address every distinct part" |
| **Style** | Matches CampusX teaching voice | Rubric: conversational, intuition-first, analogies as bonus |

## Real World Example

**Correctness Evaluation:**
- Golden Q: "What is offline eval?"
- Golden A: Detailed 3-level definition
- Generated A: Covers 70% but misses pipeline level
- Naive judge: "Incomplete → score 5"
- G-Eval with rubric: "Factually accurate though shorter → score 9" (rubric: "do not deduct for brevity")

**Style Improvement:**
- Initial style score: 54/100
- Added generator prompt: "Explain intuition first, use analogies for abstract concepts"
- Fixed rubric over-correction: "Analogies are bonus, not required"
- Final style score: 74/100

## Important Points

- **Evaluation steps > criteria**: Pre-defined steps eliminate inter-call variance
- **Rubric controls scoring**: Explicit bands (0-4, 5-8, 9-10) prevent arbitrary scoring
- **Weighted scoring stabilizes**: Uses model's internal uncertainty (log-probs)
- **Iterative refinement**: Analyze failure reasons → adjust rubric/steps OR RAG prompts
- **Threshold matters**: 0.7 default; adjust per metric (style may need lower)

## Common Mistakes

- Using high-level criteria only → high score variance across runs
- Taking raw LLM token output (8, 7, 9) instead of probability-weighted average
- Over-constraining rubric (e.g., requiring analogies for every answer)
- Not analyzing failure reasons before tweaking prompts/rubrics
- Expecting 100% on all metrics → trade-offs exist (style vs faithfulness)

## Revision Notes

- **Count-based metrics**: Recall, Precision, Faithfulness, Answer Relevance, Context Relevance → claim counting + ratios
- **Judgment-based metrics**: Correctness, Completeness, Style, Helpfulness, Safety → holistic LLM assessment
- **G-Eval = CoT steps + probability-weighted scoring**
- **DeepEval GEval class**: name, criteria/steps, rubric, model, threshold, strict_mode=False
- **Improvement loop**: Evaluate → read failure reasons → refine rubric/steps OR RAG prompts → re-evaluate
- **Stability check**: Re-run 3-4 times; scores should vary <2 points (e.g., 83→84, not 75→85)


---

# Orchestrator-Worker Design Pattern

## What is it?
- **The provided transcript does not cover the Orchestrator-Worker Design Pattern.**
- The transcript focuses entirely on **G-Eval (Generalized Evaluation)** — a technique for **judgment-based evaluation of RAG applications** using LLMs as judges with Chain-of-Thought reasoning and probability-weighted scoring.
- Key metrics discussed: **Correctness, Completeness, Style** (all judgment-based, not count-based).

## Why do we need it?
- **Not covered in this transcript.**
- The transcript explains the need for **G-Eval** because:
  - Count-based metrics (Recall, Precision, Faithfulness, Answer Relevance, Context Relevance) fail for subjective metrics like style, correctness, completeness.
  - Naive LLM-as-a-Judge produces **high variance** (scores jump between runs) due to:
    1. Loose criteria → inconsistent interpretation per call.
    2. Direct integer scoring → token probability ties cause instability (e.g., 7 vs 8 flip-flop).

## How does it work?
- **Not covered for Orchestrator-Worker.**
- **G-Eval workflow (from transcript):**
  1. **Define metric name & high-level criteria** (e.g., "Correctness: compare actual vs expected answer for factual accuracy").
  2. **LLM (GPT-4) uses Chain-of-Thought to convert criteria into detailed Evaluation Steps (rubric).**
  3. **Build System Prompt** with evaluation steps, scoring rubric (e.g., 9–10 = fully correct, 5–8 = minor issues, 0–4 = factual errors), and inputs (question, expected, actual).
  4. **Extract top-k token log-probabilities** for numeric scores (0–10) from the judge LLM.
  5. **Normalize probabilities** over numeric tokens only.
  6. **Compute probability-weighted average** → stable continuous score (e.g., 7.84).
  7. **Divide by 10, apply threshold** (e.g., 0.7) → Pass/Fail.
  8. **Average across dataset** for final metric score.

## Real World Example
- **Not covered for Orchestrator-Worker.**
- **G-Eval example from transcript:**
  - **Correctness**: Golden dataset of 15 Q&A pairs. RAG pipeline answers each question. G-Eval judge scores each (0–10 weighted). Average = 84% pass.
  - **Completeness**: Same dataset. Judge checks if all parts of multi-part questions are covered. Initial 68% → after generator prompt tweak ("address all parts") → 75%.
  - **Style**: Judge uses rubric (conversational, intuition-first, analogies for abstract concepts). Initial 54% → after generator prompt tweak (teacher-like tone) + rubric fix (analogy = bonus, not required) → 74%.

## Important Points
- **Count-based vs Judgment-based metrics**: Count-based = claim breakdown + ratio (Faithfulness, Recall). Judgment-based = holistic LLM scoring (Correctness, Style).
- **G-Eval two core innovations**:
  1. **CoT-derived Evaluation Steps** → deterministic "constitution" replaces loose criteria.
  2. **Probability-weighted scoring** → stable continuous scores replace brittle argmax token.
- **DeepEval library** implements G-Eval: provide `name`, `criteria`/`evaluation_steps`, `rubric`, `model`, `threshold`.
- **Iterative refinement**: Run → analyze failures → tighten evaluation steps/rubric → tighten generator prompts → re-run.
- **Strict mode off** enables weighted scoring; **on** forces direct integer output (defeats G-Eval purpose).

## Common Mistakes
- Using naive LLM-as-a-Judge (single-line prompt + direct integer score) → high variance, unreliable.
- Overly strict rubrics (e.g., penalizing missing analogies in every answer) → false failures.
- Not providing evaluation steps/rubric explicitly → leaves interpretation to LLM each call.
- Expecting 100% on all metrics; trade-offs exist (e.g., style vs faithfulness).

## Interview Questions
1. **Why do count-based metrics (e.g., Faithfulness) fail for Correctness or Style evaluation?**
2. **What are the two main sources of variance in naive LLM-as-a-Judge scoring?**
3. **How does G-Eval’s probability-weighted scoring reduce run-to-run variance compared to argmax token selection?**
4. **When should you provide `criteria` vs explicit `evaluation_steps` to G-Eval?**
5. **How would you iteratively improve a low Completeness score using G-Eval failure analysis?**

## Revision Notes
- **G-Eval = LLM-as-a-Judge + CoT rubric generation + log-prob weighted scoring.**
- **Solves**: High variance in judgment-based metrics (Correctness, Completeness, Style, Safety, Helpfulness).
- **Flow**: Criteria → CoT → Evaluation Steps → System Prompt + Rubric → Log-probs (top-k numeric) → Normalize → Weighted Avg → Threshold.
- **DeepEval**: `GEval(name, criteria/evaluation_steps, rubric, model, threshold)`.
- **Refine loop**: Run → Read failure reasons → Tighten rubric/steps → Tighten generator prompts → Re-run.
- **Golden Dataset**: Human-expert Q&A (universally correct, not course-specific).


---

# Hierarchical Multi-Agent Design Pattern

## What is it?

- A **hierarchical evaluation framework** (G-Eval) that replaces simple LLM-as-a-judge with a structured, deterministic scoring pipeline
- Uses **Chain-of-Thought (CoT)** to break high-level criteria into explicit evaluation steps (a "constitution" or rule book)
- Replaces single-token score output with **probability-weighted scoring** over top-k tokens for stability
- Implemented via **DeepEval library** for RAG application quality assessment (correctness, completeness, style)

## Why do we need it?

- **Count-based metrics** (recall, precision, faithfulness, answer relevance, context relevance) fail for judgment-based metrics like style, correctness, completeness
- Naive **LLM-as-a-judge** produces high variance: same input yields different scores (6→8→7) due to:
  1. Loose criteria → LLM interprets differently each call
  2. Single integer output → token probability ties cause flip-flopping (e.g., 7 vs 8)
- Need **reliable, deterministic, repeatable** evaluation scores across runs

## How does it work?

1. **Define high-level criterion** (e.g., "compare actual vs expected answer for factual correctness")
2. **CoT breakdown**: LLM judge (GPT-4) converts criterion into 4–5 explicit **evaluation steps** (rule book)
3. **Build judge prompt** with:
   - Evaluation steps
   - Scoring **rubric** (e.g., 9–10: fully correct; 5–8: minor inaccuracies; 0–4: clear factual errors)
   - Question, expected answer, generated answer
4. **Extract log-probabilities** of top-k numeric tokens (0–10) from judge model
5. **Normalize & compute weighted average** → stable score (e.g., 7.84 instead of 8)
6. **Threshold** (e.g., 0.7) → pass/fail per test case
7. **Aggregate** across golden dataset (15 questions) for final metric score

## Real World Example

- **Correctness**: Golden dataset has 15 Q/A pairs. RAG pipeline answers each. G-Eval scores each 0–10. Average = 84% pass rate.
- **Completeness**: Same dataset. Ideal answer covers points A, B, C. Generated covers A, B only → score ~7.5. Improved by refining generator prompt to "address every distinct part of the question."
- **Style**: No expected answer. Rubric defines "CampusX teaching voice" (intuitive first, conversational, analogies as bonus). Initial score 54 → after prompt tweaks (generator + rubric) → 74.

## Important Points

- **Two core innovations**: (1) CoT-derived evaluation steps replace loose criteria; (2) probability-weighted scoring replaces argmax token
- **Start with criteria**, let LLM generate steps. Once stable, **hard-code steps + rubric** for maximum determinism
- **Prompt engineering matters**: Small generator/rubric tweaks yield measurable metric improvements
- **Threshold tuning**: 0.7 may be harsh; adjust per metric (e.g., 0.6 for style)
- **Trade-offs**: Over-optimizing one metric (style) can hurt others (faithfulness)

## Common Mistakes

- Using raw LLM-as-judge without CoT breakdown → high variance, unreliable scores
- Asking judge for single integer score → token probability ties cause run-to-run jumps
- Not providing rubric → scoring logic drifts across calls
- Expecting perfect scores; 70–80% is realistic for style/completeness with constrained generator
- Ignoring failed-case analysis; root-cause patterns (e.g., missing question parts) drive targeted fixes

## Interview Questions

1. **Why does naive LLM-as-a-judge produce high variance in scores?**
2. **Explain the two core innovations of G-Eval and how each reduces variance.**
3. **When should you provide criteria vs. hard-coded evaluation steps in G-Eval?**
4. **How does probability-weighted scoring work, and why is it more stable than argmax?**
5. **Describe the flow from golden dataset to final metric score using DeepEval's G-Eval.**

## Revision Notes

- **Count-based metrics**: Break answer → claims → count matches → ratio (recall, precision, faithfulness, relevance)
- **Judgment-based metrics**: Need LLM judge (correctness, completeness, style, helpfulness, safety)
- **G-Eval = CoT steps + probability-weighted scoring**
- **CoT steps** = deterministic "constitution" for evaluation
- **Weighted score** = Σ(score_i × P(token_i)) / ΣP(token_i) over top-k numeric tokens
- **DeepEval usage**: `GEval(name, criteria/steps, rubric, model, threshold)` + `evaluate(test_cases, metrics)`
- **Iterate**: Run → analyze failures → tighten steps/rubric/generator prompt → re-run


---

# Peer-to-Peer Agent Network Pattern

## What is it?

- The lecture covers **RAG Application Quality Evaluation** using **GEval (G-Eval)**, not peer-to-peer agent networks.
- **GEval** is a research paper (2023) that improves **LLM-as-a-Judge** evaluation for **judgment-based metrics** (correctness, completeness, style, helpfulness, safety).
- It solves high variance in LLM judge scores by introducing two core innovations:
  1. **Chain-of-Thought (CoT) decomposition** of high-level criteria into detailed evaluation steps (a "constitution" or rule book).
  2. **Probability-weighted scoring** using log probabilities of top-k output tokens instead of taking the single generated integer score.

## Why do we need it?

- **Count-based metrics** (recall, precision, faithfulness, answer relevance, context relevance) work by breaking answers into claims and counting matches. They fail for **judgment-based metrics** like:
  - **Correctness**: Is the answer factually right? (Cannot verify claim-by-claim; analogies/context matter).
  - **Completeness**: Does the answer cover all parts of a multi-part question?
  - **Style/Tone**: Does it match a specific brand voice (e.g., CampusX teaching style)?
- **Naive LLM-as-a-Judge** has high variance:
  - **Reason 1**: Loose criteria → LLM interprets differently each call.
  - **Reason 2**: Direct integer scoring (0–10) → token probabilities for adjacent scores (7, 8, 9) are close, causing run-to-run jumps.
- GEval makes evaluation **stable, deterministic, and reliable** across runs.

## How does it work?

### Step-by-Step GEval Process

1. **Define Metric & High-Level Criterion**
   - Example: Correctness → "Compare actual answer against expected answer on factuality."
2. **Generate Evaluation Steps (CoT)**
   - LLM (GPT-4) breaks criterion into 4–5 explicit steps (rule book).
   - *Better*: Provide hand-crafted evaluation steps directly to remove generation variance.
3. **Build Judge Prompt**
   - System prompt includes: role, evaluation steps, **scoring rubric** (score bands with descriptions).
   - Input: Question, Expected Answer, Actual Answer.
4. **Extract Log Probabilities**
   - Instead of generated token, fetch top-k token log probs for numeric scores (0–10).
   - Filter non-numeric tokens.
   - **Normalize** probabilities to sum to 1.
   - Compute **weighted average** → final score (e.g., 7.84).
5. **Threshold & Aggregate**
   - Divide by 10 → 0–1 range.
   - Compare against threshold (e.g., 0.7) → Pass/Fail.
   - Average across dataset (e.g., 15 questions) for final metric score.

### Implementation with DeepEval

```python
# Define metric with GEval
correctness = GEval(
    name="Correctness",
    evaluation_steps=[...],  # or provide `criteria` for auto CoT
    rubric={...},            # explicit score bands
    model="gpt-4o-mini",
    threshold=0.7,
    strict_mode=False        # enables probability-weighted scoring
)

# Run evaluation loop
for qa in golden_dataset:
    actual = rag_pipeline.run(qa.question)
    test_case = LLMTestCase(
        input=qa.question,
        actual_output=actual,
        expected_output=qa.ideal_answer
    )
evaluate(test_cases=[test_case], metrics=[correctness])
```

## Real World Example

- **Correctness Evaluation**:
  - Golden dataset: 15 Q&A pairs (universally correct answers).
  - Initial run: 66% pass (8/15). Failures due to penalizing missing details (coverage) even when factually correct.
  - **Fix**: Refined evaluation steps + rubric to **not penalize brevity/omitted points** if factually accurate. Score → 84%.
- **Completeness Evaluation**:
  - Same dataset. Initial: 68% (5 pass, 10 fail).
  - **Root cause**: Generator prompt restricted to concise answers.
  - **Fix**: Updated generator prompt → "Address every distinct part of the question." Score → 75% (14 pass).
- **Style Evaluation (CampusX)**:
  - No expected answer needed. Rubric defines style: intuitive, conversational, examples/analogies, "why it matters" framing.
  - Initial: 54% (no style guidance in generator).
  - **Fix**: Generator prompt → "Write like a teacher explaining aloud… explain intuition first… use analogies for abstract concepts." + Rubric fix: "Analogy is a bonus, not required." Score → 74%.

## Important Points

- **Count-based vs Judgment-based**: Count-based = deterministic ratios. Judgment-based = need LLM judge + GEval for stability.
- **Two GEval Innovations**: (1) CoT → Evaluation Steps (Rule Book). (2) Log-prob Weighted Average → Stable Scores.
- **Strict Mode**: `strict_mode=False` enables weighted scoring; `True` takes raw token (high variance).
- **Evaluation Steps vs Criteria**: Start with `criteria` (auto CoT). After 2–3 runs, switch to hand-crafted `evaluation_steps` + `rubric` for maximum determinism.
- **Prompt Engineering Matters**: Small generator prompt changes significantly move metric scores (completeness, style).
- **Trade-offs**: Over-optimizing one metric (style) may hurt others (faithfulness). Target thresholds realistically (e.g., style threshold 0.6 vs 0.7).

## Common Mistakes

- Using naive LLM-as-a-Judge (direct 0–10 scoring) → high variance, unreliable.
- Providing only high-level criteria without CoT decomposition or explicit steps.
- Penalizing **brevity** or **missing elaboration** in correctness (should only penalize wrong statements).
- Requiring **analogies/examples in every answer** for style (over-correction); mark as bonus for abstract concepts only.
- Not iterating: run → analyze failures → refine steps/rubric/generator prompt → re-run.

## Interview Questions

1. **What are the two core innovations of GEval that reduce variance in LLM-as-a-Judge?**
   - CoT-based evaluation step generation (rule book) and probability-weighted scoring using log probs of top-k tokens.
2. **Why can't count-based metrics (recall, precision, faithfulness) evaluate "style" or "correctness"?**
   - They rely on claim-level counting; style is holistic (answer-level), and correctness requires semantic judgment (analogies, context) not claim matching.
3. **How does probability-weighted scoring work in GEval?**
   - Extract top-k token log probs for scores 0–10 → filter non-numeric → normalize → compute weighted average → final continuous score (e.g., 7.84).
4. **When should you provide hand-crafted `evaluation_steps` vs just `criteria` in GEval?**
   - Start with `criteria` (auto CoT) during pipeline design. After stability is understood, switch to explicit `evaluation_steps` + `rubric` to eliminate step-generation variance.
5. **What is the risk of setting `strict_mode=True` in DeepEval's GEval?**
   - It disables weighted scoring and uses the single highest-prob token (e.g., "8"), reintroducing high run-to-run variance.

## Revision Notes

- **GEval** = LLM-as-a-Judge + **CoT steps** + **Log-prob weighted scoring**.
- **Count-based metrics**: Recall, Precision, Faithfulness, Answer Relevance, Context Relevance.
- **Judgment-based metrics**: Correctness, Completeness, Style, Helpfulness, Safety → need GEval.
- **Variance sources**: (1) Loose criteria → inconsistent interpretation. (2) Discrete token scoring → adjacent score confusion.
- **Fixes**: Explicit evaluation steps (rule book) + scoring rubric + weighted average from log probs.
- **Workflow**: Golden Dataset → RAG Pipeline → Actual Answers → GEval Metric(s) → Scores + Pass/Fail → Analyze Failures → Refine (Steps/Rubric/Generator Prompt) → Re-run.
- **DeepEval**: `GEval` class with `evaluation_steps`, `rubric`, `strict_mode=False`.
- **Prompt Engineering** on generator directly improves completeness/style scores.


---

# Sequential Pipeline Agent Pattern

## What is it?

- A **multi-stage evaluation pipeline** for RAG applications where different quality metrics are assessed sequentially using **G-Eval** (LLM-as-a-Judge with Chain-of-Thought and probability-weighted scoring).
- Each stage evaluates a specific aspect: **Correctness → Completeness → Style**.
- The pipeline uses a **golden dataset** (question + ideal answer pairs) and runs the RAG application to generate actual answers, then feeds both to an LLM judge for scoring.

## Why do we need it?

- **Count-based metrics** (Recall, Precision, Faithfulness, Answer Relevance, Context Relevance) work by breaking answers into claims and counting matches. They **fail for judgment-based metrics** like style, correctness, and completeness.
- **Naive LLM-as-a-Judge** (direct 0–10 scoring) produces **high variance** across runs because:
  1. High-level criteria are interpreted differently each call.
  2. Direct token sampling (e.g., "8" vs "7") is unstable due to token probability fluctuations.
- **G-Eval solves this** by making evaluation **deterministic and reliable** through structured reasoning and probability-weighted scores.

## How does it work?

1. **Prepare Golden Dataset**
   - Curate Q&A pairs (e.g., 15 questions) with universally correct answers (human expert).

2. **Run RAG Pipeline**
   - Feed each question to the RAG system → collect generated answers.

3. **Define G-Eval Metric for Each Aspect**
   - **Name**: e.g., "correctness"
   - **High-level criteria** OR **explicit evaluation steps** (preferred for stability)
   - **Scoring rubric** (explicit score bands)
   - **Judge model**: GPT-4o / GPT-4o-mini
   - **Threshold**: e.g., 0.7 (pass/fail)

4. **G-Eval Execution (per question)**
   - **Step 1**: Convert criteria → evaluation steps via Chain-of-Thought (creates a "constitution").
   - **Step 2**: Build system prompt with steps, rubric, question, expected answer, actual answer.
   - **Step 3**: Call judge model with `logprobs=true`, extract top-k numeric tokens (0–10).
   - **Step 4**: Normalize probabilities → compute **weighted average** → divide by 10 → final score ∈ [0,1].
   - **Step 5**: Compare against threshold → pass/fail.

5. **Aggregate & Iterate**
   - Average scores across dataset.
   - Analyze failures → refine evaluation steps / rubric / RAG prompts → re-run.

## Real World Example

- **Correctness**: Golden answer explains "offline eval" in detail. Generated answer covers 70%. Initial G-Eval scores low (penalizes missing details). After relaxing rubric ("do not deduct for brevity/omitted points"), score jumps from 66% → 84%.
- **Completeness**: Golden answer has 3 points (A, B, C). Generated answer covers A, B. G-Eval scores ~6/10. Fix: update generator prompt to "address every distinct part of the question". Score improves 68% → 75%, failures drop from 10 → 1.
- **Style**: Target "CampusX teaching voice" (intuitive, conversational, analogies). Initial score 54%. Fix: update generator prompt + adjust rubric (analogy = bonus, not required). Score rises to 74%.

## Important Points

- **G-Eval = LLM-as-a-Judge + two core innovations**:
  1. **Criteria → Evaluation Steps** (via CoT) → fixed "rule book" reduces interpretation variance.
  2. **Probability-weighted score** (top-k token logprobs) → stable, continuous scores instead of discrete jumps.
- **Provide explicit evaluation steps + rubric** once you understand the pipeline; skip auto-CoT for maximum determinism.
- **Strict mode = false** enables weighted scoring; `true` falls back to raw token (unstable).
- **Iterative refinement** of prompts, rubrics, and generator instructions is the standard workflow.
- **Same pipeline structure** works for any judgment-based metric: helpfulness, safety, tone, coherence, etc.

## Common Mistakes

- Using **only high-level criteria** and relying on auto-CoT every call → introduces step variance.
- Asking judge for **direct integer score** → high run-to-run variance (token probability noise).
- **Over-constraining rubric** (e.g., requiring analogies in every answer) → false failures.
- Not **analyzing failure reasons** before tweaking prompts/rubrics.
- Expecting **perfect scores**; trade-offs exist (e.g., style vs faithfulness).

## Interview Questions

1. What are the two core innovations of G-Eval that make it more reliable than naive LLM-as-a-Judge?
2. Why does direct 0–10 token sampling produce high variance, and how does probability-weighted scoring fix it?
3. When should you provide explicit evaluation steps vs. letting G-Eval generate them via CoT?
4. How would you diagnose and improve a low "completeness" score in a RAG evaluation pipeline?
5. Explain the difference between **faithfulness** and **correctness** in RAG evaluation.

## Revision Notes

- **Count-based metrics** → claim breakdown + ratio (Recall, Precision, Faithfulness, etc.).
- **Judgment-based metrics** → need LLM judge (Correctness, Completeness, Style, Safety, Helpfulness).
- **Naive LLM judge** → high variance (loose criteria + discrete token output).
- **G-Eval fixes**:
  - CoT → criteria to fixed evaluation steps (constitution).
  - Logprobs → top-k numeric tokens → normalize → weighted average → stable score.
- **Pipeline**: Golden Dataset → RAG Generate → G-Eval (steps + rubric + judge) → Weighted Score → Threshold → Pass/Fail → Aggregate → Analyze Failures → Refine → Repeat.
- **Best practice**: Supply explicit steps + rubric; keep strict_mode=false; iterate on generator prompt & rubric based on failure analysis.


---

# Composing Multi-Agent Design Patterns

> **Note:** The provided transcript covers **RAG Application Quality Evaluation using GEval**, not multi-agent design patterns. The notes below reflect the actual lecture content from the transcript.

## What is it?

**GEval (G-Eval)** is an evaluation framework that uses LLMs as judges with two core innovations to produce stable, deterministic scores for **judgment-based metrics** (correctness, completeness, style, helpfulness, safety) where simple counting/ratios don't work.

- **Count-based metrics** (recall, precision, faithfulness, answer relevance, context relevance) break answers into claims and count matches against context.
- **Judgment-based metrics** require holistic assessment (e.g., "Is this answer correct?" "Does it match CampusX teaching style?") — cannot be reduced to claim counting.

## Why do we need it?

**Basic LLM-as-a-Judge has high variance:**
1. **Loose criteria** — A single-sentence prompt ("compare and score 0–10") lets the LLM interpret criteria differently each call.
2. **Token probability sampling** — The model outputs a single integer (e.g., 8) by picking the highest-probability token. Small probability shifts cause score jumps (6 → 8 → 7) across runs.

**GEval solves this** by making evaluation deterministic and reliable.

## How does it work?

### Step-by-step GEval Pipeline

1. **Define metric & high-level criterion**  
   Example: *Correctness* — "Compare actual answer against expected answer and decide how factually correct it is."

2. **Chain-of-Thought (CoT) → Evaluation Steps (Rule Book)**  
   LLM (GPT-4) breaks the criterion into explicit, ordered steps.  
   *Example steps for Correctness:*
   - Compare only factual claims in actual output against expected output.
   - A claim is wrong only if it contradicts expected output or is factually false.
   - Factually accurate answers score high even if shorter/fewer points.
   - Do not penalize brevity or omitted points; only wrong statements count.
   - Additional correct information must never lower the score.

3. **Build System Prompt with Steps + Scoring Rubric**  
   Rubric maps answer quality to score ranges:
   - 9–10: All claims factually correct.
   - 5–8: Mostly correct, minor inaccuracies.
   - 0–4: Clear factual errors.

4. **Probability-Weighted Scoring (Core Innovation)**  
   Instead of taking the emitted token (e.g., "8"), extract **log-probabilities** of top-k numeric tokens (e.g., 7, 8, 9), normalize, and compute weighted average:
   ```
   P(8)=0.70, P(7)=0.20, P(9)=0.05 → Normalize → Weighted Avg = 7.84
   ```
   This smooths variance across runs.

5. **Threshold & Pass/Fail**  
   Divide by 10 → 0.784. Compare to threshold (e.g., 0.7) → Pass/Fail.

6. **Aggregate**  
   Average scores across all test questions (e.g., 15 golden-set questions).

### Implementation Flow (DeepEval)
```python
# 1. Golden dataset: 15 Qs with ideal answers
# 2. For each Q: run RAG pipeline → get generated answer
# 3. Create test case: input, actual_output, expected_output
# 4. Define GEval metric:
GEval(
    name="correctness",
    evaluation_steps=[...],  # or provide high-level criteria
    rubric={...},            # optional but recommended
    model="gpt-4o-mini",
    threshold=0.7,
    strict_mode=False        # False = use weighted scoring
)
# 5. Evaluate → get deterministic scores
```

## Real World Example

| Metric | Golden Set | Criterion / Steps | Rubric | Fix Applied |
|--------|------------|-------------------|--------|-------------|
| **Correctness** | 15 Qs + ideal answers | Factual accuracy vs ideal answer | 0–4 / 5–8 / 9–10 | Relaxed penalty for missing details → score 66% → 84% |
| **Completeness** | Same golden set | Coverage of all distinct question parts | 0–4 / 5–8 / 9–10 | Generator prompt: "Address every part of the question" → score 68% → 75% |
| **Style (CampusX)** | No ideal answer needed | Conversational, intuition-first, analogies for abstract concepts | 0–4 (robotic) / 5–8 (textbook) / 9–10 (teaching voice) | Generator prompt + rubric fix: "Analogy is bonus, not required" → score 54% → 74% |

## Important Points

- **GEval = LLM-as-Judge + CoT steps + Probability-weighted scoring.**
- **Two innovations**: (1) CoT converts loose criteria → deterministic rule book. (2) Log-prob weighted average replaces single-token sampling.
- **Strict mode = False** enables weighted scoring; **True** reverts to raw token output (high variance).
- **Evaluation steps vs. Criteria**: Start with criteria (let LLM generate steps). Once stable, **provide your own steps + rubric** for maximum determinism.
- **Prompt engineering matters** — small generator prompt tweaks significantly move metric scores.
- **Golden dataset** must reflect universally correct answers, not course-specific content.

## Common Mistakes

- Using basic LLM-as-Judge (single prompt, raw score) → high run-to-run variance.
- Omitting rubric → LLM decides scoring boundaries inconsistently.
- Over-constraining generator (e.g., "be concise") → kills completeness/style scores.
- Treating judgment metrics like count metrics (claim-level comparison fails for analogies, holistic correctness).
- Not extracting log-probs → missing GEval's core variance-reduction mechanism.

## Interview Questions

1. **Why can't faithfulness-style claim counting work for correctness or style evaluation?**  
   *Analogy/example sentences make no sense in isolation; style is a document-level property.*

2. **What are the two failure modes of naive LLM-as-Judge?**  
   *Loose criteria → inconsistent interpretation; single-token sampling → high score variance.*

3. **How does GEval's probability-weighted scoring reduce variance?**  
   *Uses normalized log-probs of top-k numeric tokens to compute a weighted average instead of picking the max-prob token.*

4. **When should you provide your own evaluation steps vs. letting GEval generate them from criteria?**  
   *Start with criteria. After 2–3 runs, once you understand failure patterns, lock in your own steps + rubric.*

5. **What does `strict_mode=False` do in DeepEval's GEval?**  
   *Enables log-prob extraction and weighted averaging; `True` returns the raw generated integer score.*

## Revision Notes

- **Count-based metrics**: Recall, Precision, Faithfulness, Answer Relevance, Context Relevance → claim breakdown + ratio.
- **Judgment-based metrics**: Correctness, Completeness, Style, Helpfulness, Safety → need GEval.
- **GEval pipeline**: Metric + Criterion → CoT → Evaluation Steps → System Prompt + Rubric → Log-prob weighted score → Threshold.
- **Weighted score formula**: `Σ (token_value × normalized_prob)` over top-k numeric tokens.
- **Determinism levers**: Explicit steps, explicit rubric, `strict_mode=False`, fixed judge model (GPT-4).
- **Improvement loop**: Run → analyze failures → refine steps/rubric/generator prompt → re-run.


---

# Horizontal Production Use Cases for Multi-Agent Systems

## What is it?

- **G-Eval** is a research-backed evaluation technique (2023 paper) that improves **LLM-as-a-Judge** reliability for **judgment-based metrics** where counting-based methods fail.
- It addresses metrics like **correctness, completeness, style, helpfulness, safety** that require holistic assessment rather than claim counting.
- Uses **Chain-of-Thought (CoT)** to convert high-level criteria into detailed evaluation steps (a "constitution"), then applies **probability-weighted scoring** using log-probabilities instead of raw token output.

## Why do we need it?

- **Count-based metrics** (recall, precision, faithfulness, answer relevance, context relevance) break answers into claims and count matches → works for factual grounding.
- **Judgment-based metrics** (correctness, completeness, style) cannot be reduced to claim counting:
  - *Style* exists at answer level, not sentence level (e.g., "Why-What-How" structure).
  - *Correctness* fails with analogies: isolated claims look unrelated to golden answer but make sense in context.
- **Naive LLM-as-a-Judge** has high variance: same input yields different scores (6→8→7) because:
  1. Loose criteria → judge interprets differently each call.
  2. Direct integer scoring (0–10) → token probability ties cause jumps (e.g., 7 at 40%, 8 at 51%).
- G-Eval stabilizes scores across runs for reliable offline evaluation suites.

## How does it work?

1. **Define metric & high-level criterion**  
   Example: *Correctness* → "Compare actual vs expected answer, score 0–10 on factuality."

2. **CoT breakdown → Evaluation Steps (Constitution)**  
   LLM (GPT-4) converts criterion into deterministic bullet steps:  
   - Compare only factual claims.  
   - Penalize contradictions.  
   - Reward semantic matches.  
   - Do not penalize brevity/omissions.  
   - Extra correct info never lowers score.

3. **Build System Prompt with Steps + Scoring Rubric**  
   Rubric example:  
   - 9–10: All claims factually correct.  
   - 5–8: Mostly correct, minor inaccuracies.  
   - 0–4: Clear factual errors.

4. **Probability-Weighted Scoring (Core Innovation)**  
   - Extract top-k token log-probabilities for numeric tokens (0–10).  
   - Ignore non-numeric tokens.  
   - Normalize probabilities to sum = 1.  
   - Compute weighted average: Σ(score_i × prob_i).  
   - Divide by 10 → final score in [0,1].  
   - Compare against threshold (e.g., 0.7) for pass/fail.

5. **Implementation via DeepEval**  
   - Provide `GEval` metric with: name, criterion/evaluation_steps, rubric, judge model (GPT-4o-mini), threshold.  
   - Loop over golden dataset: feed question → RAG pipeline → actual answer → build test case (input, actual, expected).  
   - Run `evaluate()` with metrics list → get per-question scores + aggregate.

## Real World Example

> **Scenario**: Evaluate a RAG chatbot for CampusX teaching style.  
> - **Golden dataset**: 15 questions + ideal answers (universally correct, not course-specific).  
> - **Correctness**: G-Eval scores factual accuracy vs golden answer. Initial 66% → after refining evaluation steps & rubric: 84%.  
> - **Completeness**: Checks if all question parts covered. Initial 68% (5/15 pass) → after generator prompt tweak ("address every distinct part"): 75% (14/15 pass).  
> - **Style**: Measures "CampusX voice" (intuitive, conversational, analogies for abstract concepts). Initial 54% → after generator prompt ("flowing conversational prose, intuition first") + rubric fix (analogies = bonus, not required): 74%.

## Important Points

- **Two core G-Eval innovations**:  
  1. CoT → evaluation steps (reduces interpreter variance).  
  2. Log-prob weighted average (reduces token-selection variance).
- **Start with high-level criterion**, let G-Eval generate steps. After 2–3 runs, **lock in your own steps + rubric** for maximum determinism.
- **Strict mode = False** enables weighted scoring; `True` forces raw token output (defeats purpose).
- **Prompt engineering matters**: Small generator prompt changes significantly move metric scores.
- **Golden dataset** must reflect *universal* correctness, not course-specific content.

## Common Mistakes

- Using count-based logic (claim breakdown + ratio) for judgment metrics → fails on style/completeness.
- Relying on raw LLM integer score (0–10) → high run-to-run variance.
- Omitting rubric → leaves scoring scale interpretation to judge → instability.
- Over-constraining rubric (e.g., requiring analogies for every answer) → false failures.
- Not iterating: evaluate → analyze failures → refine steps/rubric/prompts → re-evaluate.

## Interview Questions

1. **Why can't faithfulness-style claim counting evaluate "style" or "correctness"?**  
   Style is holistic (answer-level); correctness fails on analogies that are locally unrelated but globally valid.

2. **What two problems cause high variance in naive LLM-as-a-Judge?**  
   (1) Loose criteria → inconsistent interpretation per call. (2) Direct integer sampling → token probability ties cause score jumps.

3. **How does G-Eval's probability-weighted scoring work?**  
   Extract top-k numeric token log-probs → normalize → weighted average → divide by 10 → stable continuous score.

4. **When should you provide your own evaluation steps vs. letting G-Eval generate them?**  
   Start with criterion (exploration). After stability, lock in custom steps + rubric (production determinism).

5. **What does `strict_mode=False` enable in DeepEval's GEval?**  
   Activates log-prob weighted scoring; `True` forces discrete token output (defeats G-Eval's variance reduction).

## Revision Notes

- **Count-based metrics**: Recall, Precision, Faithfulness, Answer Relevance, Context Relevance → claim counting + ratios.
- **Judgment-based metrics**: Correctness, Completeness, Style, Helpfulness, Safety → need LLM judge.
- **G-Eval = CoT steps + Probability-weighted scoring**.
- **Flow**: Criterion → CoT → Evaluation Steps → System Prompt + Rubric → Log-prob extraction → Weighted avg → Threshold.
- **DeepEval GEval**: name, criterion/steps, rubric, model, threshold → `evaluate(test_cases, metrics)`.
- **Iterate**: Run → Analyze failures → Refine steps/rubric/prompts → Re-run.
- **Stability**: Custom steps + rubric + weighted scoring = deterministic, reliable eval suite.

