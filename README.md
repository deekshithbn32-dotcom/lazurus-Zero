# 🛡️ Lazarus-Zero
### Autonomous Self-Healing Runtime: AST Patch Synthesis, Sandbox Verification & Zero-Downtime Exploit Immunization

> **HackNova-26 (Anveshana-26) | Round 1 Solution Note**  
> **Focus Track:** Cybersecurity / Software Engineering / AI & ML  
> **Team:** BitWise  
> **Members:** Deekshith (1EW25CS406) | Lalith Adithya (1EW25CS414) | Moses J (1EW25CS418) | Nagendra (1EW25CS419) | Vidya JS (1EW24CS213) | Vindya S (1EW24CS216)

---

## 1. Executive Summary & Problem Statement

Production detection tools like **Datadog, Sentry, and Web Application Firewalls (WAFs)** only *alert* engineers when services fail or face attacks. They do not remediate the vulnerability. 
A human engineer must still wake up at 2 AM, inspect raw stack traces, write a code patch, run regression tests, and execute a redeployment. This gap — **Mean Time To Remediate (MTTR)** — typically costs **3 to 5 hours of downtime and data exposure**.

Furthermore, regex-based WAFs add high false-positive rates that block legitimate customers while leaving the underlying vulnerable code paths untouched.

### The Lazarus-Zero Solution:
Lazarus-Zero is runtime middleware for Python/Flask services that **autonomously detects, diagnoses, synthesizes a code-level patch, verifies it in an isolated shadow sandbox, and hot-swaps it into memory with zero downtime** while the service keeps running.

---

## 2. In-Scope Bug Classes & Deterministic AST Transformations

Rather than relying on non-deterministic generative LLMs that hallucinate, Lazarus-Zero uses **deterministic Abstract Syntax Tree (AST) rewrites** (`ast.parse`, `ast.NodeTransformer`, `ast.unparse`):

| Bug Class | Typical Trigger | Deterministic AST Transformation |
| :--- | :--- | :--- |
| **Class A: Crash-Class Bugs** | None dereference, `KeyError`, `IndexError`, `ZeroDivisionError` on edge payloads | Inserts guard clauses, safe-access wrappers (`.get()`), and typed fallback returns |
| **Class B: SQL Injection** | String-built queries (`f-string`, `%`, `+`, `.format`) reaching `execute()` | Rewrites query into parameterized queries with bound argument tuples (`?`, `(val,)`) |
| **Class C: Command Injection** | Unsanitized user input reaching `os.system` or `subprocess(shell=True)` | Rewrites to structured argument lists `subprocess.run(shell=False)` with regex allow-list validation |

---

## 3. The 5-Stage Autonomous Remediation Pipeline

```
[ Incoming Web Traffic + Exploits ]
                 │
                 ▼
┌────────────────────────────────────────┐
│  STAGE 1: WSGI Shield Interceptor      │  -> Captures stack frames (inspect), line no.,
│           & Graceful Fallback          │     returns 200/202 degraded response (0 downtime)
└──────────────────┬─────────────────────┘
                 ▼
┌────────────────────────────────────────┐
│  STAGE 2: Machine Learning Triage      │  -> Shannon Entropy + Lexical Ratios + PCA
│           (PCA + RBF-SVM Classifier)   │  -> Classifies: Exploit vs. Code Bug vs. Glitch
└──────────────────┬─────────────────────┘
                 ▼
┌────────────────────────────────────────┐
│  STAGE 3: Deterministic AST Synthesis  │  -> Python ast NodeTransformer rewrites
│           (Zero LLM Hallucinations)    │  -> Generates clean Python code & unified diff
└──────────────────┬─────────────────────┘
                 ▼
┌────────────────────────────────────────┐
│  STAGE 4: Shadow Sandbox Verification  │  -> 1. Replays triggering exploit (must neutralize)
│           (Replay + Regression + Fuzz) │  -> 2. Replays benign regression tests (100% fidelity)
│                                        │  -> 3. Hypothesis property-based fuzzing (50+ iter)
└──────────────────┬─────────────────────┘
                 ▼
┌────────────────────────────────────────┐
│  STAGE 5: Zero-Downtime Hot-Swap       │  -> Confidence >= 0.85: Atomic in-memory swap
│           & Rollback Guard             │  -> Confidence < 0.85: Human-in-the-Loop review
│                                        │  -> Rollback Guard reverts if post-swap error rate spikes
└──────────────────┬─────────────────────┘
                 ▼
[ Forensic Ledger (MySQL / SQLite) + Permanent Git .patch Export ]
```

---

## 4. Mathematical Confidence Score Formulation

Before any patch is permitted into runtime memory, it must pass the mathematical threshold:

$$\text{Confidence Score} = \text{Sandbox Pass Rate} \times \text{Classifier Probability} \times \text{Patch Size Penalty}$$

- **Sandbox Pass Rate (0.0 to 1.0):** Weighted composite of Exploit Replay, Regression Fidelity, and Hypothesis Property Fuzzing.
- **Classifier Probability (0.0 to 1.0):** SVM probability estimation of malicious vs glitch classification.
- **Patch Size Penalty ($1 - \frac{\Delta\text{lines}}{120}$):** Penalizes overly bloated AST rewrites to favor surgical, minimal modifications.
- **Threshold Policy:** $\ge 0.85 \implies$ Autonomous Instant Hot-Swap; $< 0.85 \implies$ Human-in-the-Loop Approval Required.

---

## 5. Quickstart & 1-Click Startup

### Prerequisites:
- Python 3.9+
- Dependencies installed:
  ```bash
  pip install -r requirements.txt
  ```

### Launch Lazarus-Zero:
```bash
python run_demo.py
```
*(Or simply double-click `start.bat` on Windows!)*

Once started:
- **Clean Enterprise Dashboard:** `http://127.0.0.1:5000/`
- **Cyber-Ops War-Room View:** `http://127.0.0.1:5000/war-room`

---

## 6. Live 5-Minute Demo Script for Judges

When presenting to hackathon judges, follow this concise, high-impact walkthrough:

### Minute 1: The Pitch & Industry Pain Point
> *"Judges, when Datadog or Sentry detects a 500 error or SQL injection at 2 AM, production crashes and data leaks until a human engineer wakes up and spends 3 hours fixing it. Lazarus-Zero eliminates this MTTR window by closing the loop autonomously: Intercept $\rightarrow$ Diagnose with ML $\rightarrow$ Rewrite at the AST level $\rightarrow$ Sandbox verify with fuzzing $\rightarrow$ Hot-swap into memory with zero downtime."*

### Minute 2: Show The Unprotected Failure (The Status Quo)
1. Open the War-Room or Enterprise Dashboard.
2. Under **SQL Injection**, click **"🔴 Unprotected"**.
3. **Show Judges:** The raw application dumps the entire customer database, balances, and passwords.
4. Under **Crash Bug**, click **"🔴 Unprotected"**.
5. **Show Judges:** The worker thread crashes with an unhandled `ZeroDivisionError` and HTTP 500 downtime.

### Minute 3: Launch Lazarus-Zero Autonomous Self-Healing
1. Click **"🛡️ Heal Live"** (or in the clean UI, click the attack card).
2. **Watch the live 5-Stage visualizer:**
   - **Stage 1 (Intercept):** Stack frame captured at `account_lookup`. The client gets an immediate graceful fallback response (0 dropped connections).
   - **Stage 2 (ML Triage):** Shannon entropy and lexical ratios are reduced via PCA. RBF-SVM classifies the event as `ACTIVE_EXPLOIT` with 98.6% confidence.
   - **Stage 3 (AST Synthesis):** Deterministic AST transformation rewrites `f-string` query concatenation to parameterized query bindings. Show judges: **"Notice we don't use LLMs here — this is deterministic compiler theory, zero hallucinations."**
   - **Stage 4 (Shadow Sandbox):** Replays the injection payload (neutralized), verifies `alice` regression (passed), and runs 50 Hypothesis property fuzz iterations.
   - **Stage 5 (Hot-Swap):** Confidence clears 0.88; atomic memory bytecode replacement occurs in milliseconds!

### Minute 4: Live Verification (The "Magic" Moment)
1. Go to the **Target Microservice Live Verification Console**.
2. Click **"Query User: Injection Payload"** (`' OR '1'='1' --`).
3. **Show Judges:** The live running server now safely parameterizes the query, returning 0 records leaked with no restart!
4. Click **"Query User: 'alice'"**. Normal business traffic works with 100% fidelity.
5. Point to the **MTTR KPI Card**: **`0.54s`** (Down from 3.5 hours!).

### Minute 5: Enterprise Governance & Git Patch
1. Show the **Forensic Audit Ledger**: Normalized records in `Incident_Stack_Traces`, `AST_Patch_Diffs`, and `Sandbox_Test_Results`.
2. Click **"Download .patch File"** to show judges the unified Git patch ready for senior engineer pull-request auditing.
3. Highlight the **Rollback Guard**: If post-swap error rates ever spike, the runtime automatically reverts bytecode to the pre-patch state.

---

## 7. Key Judge Q&A Defense

| Question from Judges | Your Winning Answer |
| :--- | :--- |
| **"Isn't automatic patching risky? What if the patch introduces new bugs?"** | *"That is our primary safety guarantee: No patch touches memory without passing our 3-tier Shadow Sandbox: exact exploit replay, benign regression tests, and Hypothesis property fuzzing. If confidence drops below 85%, it halts and routes to Human-in-the-Loop Approval."* |
| **"Do you use LLMs that might hallucinate bad code?"** | *"No! Section 10 of our solution note explicitly guarantees that patch synthesis uses deterministic Python `ast` transformations. AST node rewriting is mathematically provable, consistent, and runs in sub-milliseconds."* |
| **"How does hot-swapping work across multiple workers?"** | *"Each patch generates an immutable cryptographic version ID recorded in the shared MySQL/SQLite ledger. Python workers poll and hot-reload updated bytecode into memory, ensuring cluster consistency without dropping TCP connections."* |
