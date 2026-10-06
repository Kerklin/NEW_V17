# NEW_V17 – setup guide

V17 searches for jobs every 5 minutes and **scores each job against your CV**: skills, experience, education, languages and eligibility.
Every morning it emails you a **Fit digest** ranking the open jobs. For jobs that fit well, it also emails a full **application pack**:
a fit analysis, HR prescreening, ATS keywords, salary expectations, a tailored CV and a cover letter (Word files).

This repository is **public**, but your CV, your scores and your packs never enter it.

---

## Before you start (5 minutes)
You need:
- A **GitHub** account. A new **public** repository named `NEW_V17` holds the agent.
- A **Gmail** account with **2-Step Verification** turned on.
- Your **CV as plain text**. Copy it from Word, without tables or columns, and keep it under 7,000 characters.

> If you used V15 or V16 before: open each old repository → **Actions** → the workflow → **⋯** → **Disable workflow**.
> Otherwise both agents will use your one AI allowance.

---

## Step 1 – Create the repository (2 minutes)
1. On github.com select **+** → **New repository**.
2. **Repository name:** `NEW_V17` · **Public** · tick **Add a README file** → **Create repository**.

## Step 2 – Upload the files (3 minutes)
1. **Add file** → **Upload files** → drag in `agent.py`, `save.py` and `SETUP.md` → **Commit changes**.
2. **Add file** → **Create new file** → type exactly `.github/workflows/v17.yml` → paste the contents of `v17.yml` → **Commit changes**.

✅ **Check:** the repository shows `agent.py`, `save.py`, `SETUP.md`, `README.md` and a `.github` folder.

## Step 3 – Create a Gmail app password (3 minutes)
1. Open **myaccount.google.com/apppasswords**. If the page doesn't open, turn on 2-Step Verification first.
2. Name it `V17` → **Create** → copy the 16 characters. Spaces don't matter.

## Step 4 – Add the secrets (5 minutes)
In **NEW_V17**: **Settings** → **Secrets and variables** → **Actions** → **Secrets** tab → **New repository secret**.

| Name (exactly) | Value | |
|---|---|---|
| `MASTER_CV` | Your full CV as plain text. **Line 1 = your name, line 2 = city/country and contact.** | required |
| `MAIL_USER` | Your Gmail address | required |
| `MAIL_PASS` | The 16-character app password from step 3 | required |
| `BACKUP_KEY` | **40 random characters** (see below) – enables the encrypted backup | recommended |
| `MAIL_TO` | Another address that should receive the emails | optional |
| `SEARCH_API_KEY` | Brave Search API key, for salary evidence from the web | optional |

**How to make the BACKUP_KEY.** In Windows PowerShell, run the line below, copy the result and paste it as the secret. **Never change it later.**
```powershell
-join ((48..57)+(65..90)+(97..122) | Get-Random -Count 40 | % {[char]$_})
```

⚠️ **Common mistakes**
- Using **Environment** or **Dependabot** secrets. They must be **Repository secrets**.
- Mistyping names. Use capital letters and no spaces.
- Assuming secrets copy over from V15 or V16. They don't, so add them again.

## Step 5 – One setting (1 minute)
**Settings** → **Actions** → **General** → **Workflow permissions** → **Read and write permissions** → **Save**.

## Step 6 – First run (2 minutes)
**Actions** → **V17** → **Run workflow**. Tick **Send the fit digest now** → **Run workflow**.

✅ **Check after 2–4 minutes:**
- a green ✓ on the run
- the job table on the **Code** tab, with no ⚠️ lines at the top
- a "Your fit digest" email in Gmail
- two new branches, `agent-lock` and later `agent-backup`. Don't delete them.

---

## Daily use
| What | How |
|---|---|
| **Fit digest** | Arrives every morning: open jobs ranked by fit, with ✓ matches, ✗ missing and ⚠ risks |
| **Automatic packs** | Made for jobs with fit ≥ `PACK_MIN_FIT` (65), most urgent first, up to `PACKS_PER_DAY` |
| **Pack for one job now** | **Actions** → **V17** → **Run workflow** → paste the job's link (+ language, focus) |
| **Job behind a login (LinkedIn, Workday)** | From Gmail, **send an email to yourself** with a subject starting **`JOB`**, and the job link **and the full job text** in the body. It's picked up within about 5 minutes. |
| **Emergency stop** | **Settings** → **Secrets and variables** → **Actions** → **Variables** tab → new variable `AI_ENABLED` = `no`. Delete it to resume. |

### How to read a fit score (0–100)
| Part | Points | What it checks |
|---|---|---|
| Skills | 55 | How many of the job's key terms appear in your CV (terms in the job title count double) |
| Experience | 15 | Years asked for vs. years in your CV (approximate) |
| Education | 10 | Degree level asked for vs. yours |
| Languages | 15 | Required languages vs. yours. **A missing required language caps the score at 55.** |
| Eligibility | 5 | "Nationals of …", local-hire or internal-only posts that exclude you → **score capped at 25** |

**High** = 70+, **Medium** = 50–69, **Low** = under 50.
**UNCONFIRMED** means the job description couldn't be read, so the score is capped at 60.

The score is a fast automatic check. Each application pack also contains a full AI fit analysis that confirms or corrects it.

---

## Where your data is
| Public (anyone can see) | Private (only you) |
|---|---|
| Job titles, links, deadlines and a coarse High/Medium/Low label | Your CV (secret) |
| The code | Fit scores, ✓/✗ reasons and risks (email only) |
| AI usage counters and unreadable job codes (branch `agent-lock`) | Application packs (email, or your Gmail folder `V17-packs`) |
| Run logs: status and references like `#43a957` | Jobs you send yourself (link or `JOB` email) |
| Encrypted backups, only if email fails (branch `agent-backup`) | The key to those backups (`BACKUP_KEY`) |

To hide even the High/Medium/Low label, set `PUBLIC_FIT: "no"` in `v17.yml`.

## When email fails
1. **Sending fails**, e.g. Gmail's daily limit or a short outage: the pack is saved straight into your Gmail folder **V17-packs**.
2. **Gmail can't be reached at all** and `BACKUP_KEY` is set: an encrypted copy waits on the branch `agent-backup`. It's emailed automatically once Gmail works again, then deleted. Only one copy of that branch is ever kept, with no history. Copies older than 30 days are discarded.
3. **No `BACKUP_KEY`:** nothing is stored anywhere. The pack is made again the next day.

---

## Warnings on the front page
| Warning | Fix |
|---|---|
| Setup not finished – add these secrets: … | Add the listed secrets (step 4) |
| MASTER_CV looks too short | Paste your **full** CV as plain text |
| Email not usable: Gmail refused the app password | Make a new app password (step 3) → update `MAIL_PASS`. **Changing your Google password revokes app passwords.** |
| BACKUP_KEY is shorter than 32 characters | Make a 40-character key (step 4) |
| AI is switched off | Delete the `AI_ENABLED` variable |
| Red ✗ on "Save" | Step 5 (Read and write permissions) |
| Red ✗ on "Get the code" | Run it again. If it repeats, check that the repository and branch are named `main`. |

## Settings (top of `.github/workflows/v17.yml`)
`PACK_MIN_FIT` (40–100) · `PACKS_PER_DAY` (max 30) · `DIGEST_HOUR_UTC` · `PUBLIC_FIT` · `AI_HIGH_PER_DAY` (max 35) ·
`AI_LOW_PER_DAY` (max 110) · `AI_PER_HOUR` (max 20) · `SEARCH_WORDS` · `FEEDS` (extra RSS or job-board links).
Values above a maximum are ignored.

## Good to know
- **V17 remembers which jobs already got a pack** using a key made from `BACKUP_KEY`, or from `MAIL_PASS` if there's no backup key. If you change that key, a few packs may be made once more, still within the daily limits.
- **Keep the repository to yourself.** Don't add collaborators: anyone with write access could change the workflow and read your secrets.
- **Always read a pack before sending.** Fill in or delete every `[ADD ONLY IF TRUE: …]` placeholder.
