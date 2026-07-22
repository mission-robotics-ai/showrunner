# Judge Comms — three-block pattern

**How to use:** Three sequential blocks, each gated on a different trigger. Block A is sendable the moment a judge confirms (T-2 from judging day). Block B waits on rubric sign-off from the event host — don't send it before the rubric in `judge-ops-plan.md` is approved. Block C goes out morning-of, by text or Slack DM, not email. Personalize the `[name]` slot per judge each time.

---

## Block A — Confirm + logistics (T-2, send as soon as a judge confirms)

**Subject:** [EVENT NAME] — judging, [JUDGING DAY/DATE]

Hi [name] —

Thank you again for judging [EVENT NAME]. It means a lot to have you in the room, and I wanted to get you the details early so [JUDGING DAY] is easy.

Here's the shape of it. Judging is [DAY, DATE], and I'd love you there in person from [START TIME] to [END TIME]. We're at [VENUE + ADDRESS]. Around [N] teams will demo [what they built] — real hardware, real tasks, done live in front of you. Demos run about [DURATION], then you all deliberate while we run the room, and we announce winners around [TIME].

A few practical things: food is covered, so come hungry. [Parking / transit note.] I'll send exact door instructions closer to the day. A short scoring rubric will follow this week so you know what we're looking for before you walk in.

That's it. Just confirm you're good for [START]–[END] on [DAY] and I'll take care of the rest.

Thank you again —
[HOST NAME]

---

## Block B — The rubric + optional pre-reads (T-1, day before or two days before)

**Send only after the rubric is approved — see the PROPOSED rubric in `judge-ops-plan.md`.**

**Subject:** How we're scoring [JUDGING DAY] + the team [repos/submissions]

Hi [name] —

Quick follow-up before [JUDGING DAY] so you can walk in ready.

Here's how we're scoring. Every team gets rated on [N] things, one to five each:

- **[CRITERION 1 — usually the thing that defines your event's identity]** — [what this measures and why it's the heart of the event].
- **[CRITERION 2]** — [what this measures].
- **[CRITERION 3]** — [what this measures].
- **[CRITERION 4]** — [what this measures].

Add the [N] up per team, highest total wins. If there's a tie, the higher "[TIE-BREAK CRITERION]" score breaks it — and if it's still tied, the judges talk it out. You'll each get a printed sheet at check-in, so there's nothing to prepare.

Every team submits [an open-source repo / a written summary / etc.], and I'll send the list [when]. Skimming a few beforehand is welcome if you're curious, but it's entirely optional — you can judge everything you need to from the live demos.

See you [DAY] at [TIME]. Anything you need before then, just ask.

[HOST NAME]

---

## Block C — Day-of morning note (text / Slack DM, short)

We're on — see you at [TIME] at [VENUE]. Ask for [GREETER NAME] at the door and they'll get you settled and hand you your scoring sheet. Demos start right at [TIME]. Text me if anything comes up. — [HOST NAME]

---

**Why the gating matters:** Block A can go out the moment a judge says yes — it's pure logistics, nothing to approve. Block B carries the actual scoring mechanism, so it should never ship ahead of the host signing off on the rubric; sending a rubric you later change confuses judges and undercuts the scoring. Block C is deliberately terse — judges are walking in the door, not reading email.
