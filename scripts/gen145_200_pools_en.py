# -*- coding: utf-8 -*-
"""EN archetype pools for articles 145-200 (Pillar IV tactics, Pillar V conditioning)."""

EN_POOL = {}

# ----------------------------------------------------------------------------
# PILLAR IV - TACTICS
# ----------------------------------------------------------------------------
EN_POOL["tactics"] = {
    "intent": [
        r"""Tactical decision-making at the competitive level is a **probability management problem**, not an aesthetic preference. Every ball you receive carries a distribution of outcomes, and every ball you strike shifts that distribution for the next exchange. The player who manages distributions beats the player who chases highlights, because over a two-hour match the accumulation of small percentage advantages overwhelms isolated spectacular winners. The practical consequence is that tactics must be trained as a **repeatable decision architecture**: scan, classify, commit, execute, recover, audit.""",
        r"""Most tactical losses are not caused by a lack of shot quality but by a **failure of information intake before the ball arrives**. Elite players begin their decision roughly 300-500 ms earlier than intermediate players because their pre-point scan and opponent-profiling habits give them a prior. When the prior is accurate, the required reaction time drops and the shot selection becomes almost automatic; when the prior is absent, the player is forced into late, high-risk improvisation that inflates the unforced error count.""",
        r"""Scoreboard leverage changes the correct shot selection even when the ball is identical. A serve at 30-15 and the same serve at 30-40 occupy different risk budgets, because the cost of an error is asymmetric. Elite competitors explicitly re-price risk at break point, set point, and tiebreak transitions rather than playing one continuous style. This deliberate re-pricing is a trainable skill and it is one of the fastest routes to winning more close matches without changing a single technical stroke.""",
        r"""The final layer is **auditability**. Tactical intuition that cannot be measured cannot be improved, and cannot be trusted under pressure. A structured post-match audit converts a chaotic match narrative into a small set of countable pattern outcomes: which patterns produced points, at which score states, against which ball heights, and with what margin. That audit is the feedback signal that closes the loop between intention and result.""",
    ],
    "sub": [
        (
            "Court Geometry & the Angular Error Budget",
            "Every target on the court is defined by three geometric quantities: the **lateral angle** from your contact point to the target, the **net clearance height** available along that angle, and the **depth margin** before the baseline. These three form a conserved budget. Opening the angle to a sharp cross-court target reduces available net clearance and depth margin simultaneously, which is why extreme angle shots carry a structurally higher error rate than their visual appeal suggests.",
            [
                "Lateral angle beyond 38-42 degrees from the center line forces net clearance above 0.9 m to keep the same safety margin.",
                "Depth margin collapses from ~2.5 m (down-the-line) to ~1.2 m (acute cross-court) for identical swing speed.",
                "The **safest high-percentage target** is the deep middle third: largest combined margin, shortest recovery distance.",
                "Angular error budget should be spent only when the opponent is displaced beyond 2.5 m from court center.",
            ],
        ),
        (
            "Serve +1 Pattern Architecture",
            "The serve is not a point-ending weapon; it is the **first half of a two-shot pattern**. Serve plus one architecture means the server pre-commits to a location pairing: a serve location that produces a predictable return type, and a first groundstroke that exploits exactly that return type. The pairing must be decided before the toss, so that the recovery footwork already positions the body for the intended second shot.",
            [
                "Body serve to the deuce court returns most often to the middle: the +1 is a forehand inside-in to the open court.",
                "Wide slice on the ad court pulls the returner 2.2-3.0 m off center: the +1 is a cross-court forehand into the vacated space.",
                "Serve+1 conversion rate above 62% at club level and above 71% at elite level is the benchmark for a functional pattern.",
                "Never serve to a location whose most probable return you have not rehearsed at least 200 times.",
            ],
        ),
        (
            "Return Positioning, Depth Control & the Neutralizing Ball",
            "The return of serve has two legitimate goals, and confusing them is a common tactical error. The first goal is to **neutralize** (deny the server an immediate +1), and the second is to **attack** (take time away). Neutralizing requires depth and height; attacking requires early contact and a shortened backswing. The decision depends on serve quality, not on the returner's mood.",
            [
                "First-serve return: stand 1.2-1.6 m behind the baseline, block with a compact swing, target depth beyond 6.5 m from the net.",
                "Second-serve return: step 0.6-1.0 m inside the baseline and take the ball on the rise to compress the server's recovery window.",
                "A return landing inside 4 m of the net converts directly into a losing position within two shots in over 70% of cases.",
                "Return height above 1.1 m at the net plane is the single strongest predictor of a neutral rally outcome.",
            ],
        ),
        (
            "Pattern Recognition Under Time Constraint",
            "Recognition is a classification problem solved under a hard deadline. The brain must map a small number of kinematic cues (racket face angle, hip rotation, contact height, shoulder line) onto a shortlist of probable ball trajectories within roughly 200-400 ms of the opponent's contact. Training recognition means shrinking the cue set that triggers a correct classification, not merely hitting more balls.",
            [
                "Three cues resolve over 80% of direction predictions: racket face at contact, front-foot plant direction, and non-dominant shoulder line.",
                "Occipital-parietal activation rises sharply when cues are occluded, which is why occlusion drills accelerate recognition.",
                "Recognition latency below 220 ms supports early commitment; above 350 ms the player is structurally late.",
                "Chunking opponent tendencies into 3-5 named patterns reduces decision latency more than raw repetition volume.",
            ],
        ),
        (
            "Score-State Leverage Modeling",
            "Not all points are equal, and treating them as equal is expensive. Leverage is the change in win probability produced by the next point. Serving at 30-40 on your own serve is a high-leverage point because the cost of losing is a break; serving at 40-0 is low leverage because the cost is nearly zero. Elite players consciously expand or contract their risk envelope according to leverage.",
            [
                "At high leverage, contract risk: raise first-serve percentage targets by 6-10 percentage points and favor the higher-margin serve.",
                "At low leverage, expand risk: test a secondary pattern or a lower-percentage serve that you intend to use later in the match.",
                "Break-point conversion improves when the returner pre-selects one pattern instead of reacting to the serve.",
                "Tiebreak points above 4-4 behave like high-leverage games; the same contraction rule applies.",
            ],
        ),
        (
            "Opponent Profiling & Exploitation Maps",
            "An opponent profile is a **compressed decision aid**, not a scouting novel. It should fit on a single card and contain four items: preferred serve location under pressure, weakest defensive movement direction, highest-error shot under height, and the pattern the opponent uses to escape trouble. Everything else is noise that will not be recalled at 4-4 in the third set.",
            [
                "Profiles built from 20+ observed points predict direction correctly 65-75% of the time, versus ~50% baseline intuition.",
                "The highest-value profile item is the **trouble-escape pattern**: it tells you what to deny when the opponent is defensive.",
                "Weak-side movement exploitation should be tested twice per set before being trusted as a tactic.",
                "Profile updates at each changeover prevent stale assumptions after the opponent adjusts.",
            ],
        ),
    ],
    "step": [
        ("Pre-Point Scan", "0-4 s before the toss or the serve", "Sweep opponent position, stance width, and racket grip before committing to any intention. Record the single most informative cue and discard the rest."),
        ("Intention Lock", "3-1 s before contact", "Declare one primary target and one contingency. A point with two equally-weighted intentions has effectively no intention."),
        ("Toss / Split Timing", "Toss apex or opponent's contact", "Anchor the movement trigger to the opponent's contact, not to the ball's flight, to gain the 80-120 ms that decides whether the stroke is offensive or defensive."),
        ("First-Step Directionality", "0-250 ms after contact", "The first step must solve the largest geometric problem first: deep or short, wide or middle. Diagonal recovery steps are banned at this stage."),
        ("Classification Window", "250-500 ms after contact", "Classify ball as attackable, neutral, or defensive. The classification decides backswing length, grip pressure, and target margin before arrival."),
        ("Commitment Threshold", "500-650 ms after contact", "Once the classification is made, the decision must not be revised. Late revision produces deceleration and the classic 'half-shot' error."),
        ("Execution & Margin Discipline", "Contact window +/- 60 ms", "Apply the margin that matches the classification: attackable balls get aggressive targets, defensive balls get maximum net clearance and depth."),
        ("Recovery & Reset", "0-1.2 s after your contact", "Recover to the bisector of the opponent's available angles, then reset the pre-point scan. Recovery distance must be balanced, never a full sprint to the center line."),
    ],
    "metric": [
        ("First-Serve Points Won", "Points won / first serves in play", "62-68%", "72-78%"),
        ("Second-Serve Points Won", "Points won / second serves in play", "48-53%", "56-62%"),
        ("Serve +1 Conversion", "Points won when the +1 lands in the intended third", "58-64%", "68-74%"),
        ("Return Depth", "Average return landing distance from the net (m)", "5.5-6.5 m", "6.5-7.5 m"),
        ("Break-Point Conversion", "Break points converted / break points earned", "35-42%", "45-55%"),
        ("Unforced Errors per Set", "Counted unforced errors per set", "9-13", "4-7"),
        ("Pattern Adherence", "Points where the pre-declared pattern was executed", "55-65%", "75-85%"),
        ("Net Approaches Won", "Points won / net approaches", "58-64%", "68-75%"),
    ],
    "error": [
        ("Over-hitting on high-leverage points", "Risk envelope is priced by emotion rather than by leverage", "Break points and set points are donated back with low-percentage attempts", "Re-price risk explicitly: at break point, raise first-serve percentage 6-10 points and target the deep middle third"),
        ("Serving to the same location when ahead in the game", "Comfort-seeking under low perceived pressure", "Opponent grooves a return pattern and converts it at the next high-leverage point", "Rotate serve location on a fixed rule (e.g. never the same third twice in a row at 30-0 or 40-15)"),
        ("Returning second serves from behind the baseline", "Fear of being passed rather than commitment to attacking", "The server completes recovery and the return becomes a neutral rally at best", "Step 0.6-1.0 m inside the baseline on second serves and take the ball on the rise"),
        ("Late classification producing half-shots", "Ball is watched but not classified until after the bounce", "Deceleration at contact, shortened follow-through, mid-court sitter", "Force an early verbal classification ('attack / neutral / defend') at the opponent's contact"),
        ("Chasing acute cross-court angles without displacement", "The shot is chosen for aesthetics instead of geometry", "Error rate doubles while the opponent is not moved at all", "Only spend the angular budget when the opponent is more than 2.5 m from court center"),
        ("Recovering to the center line instead of the bisector", "A memorized habit instead of a geometric calculation", "Open court is exposed and the next ball requires a maximal sprint", "Recover to the bisector of the opponent's available angles, weighted by their best option"),
        ("Ignoring the opponent's trouble-escape pattern", "Profile card is too long to recall under pressure", "The opponent repeatedly escapes from defensive positions", "Keep four profile items only, and rehearse the escape-denial pattern before the match"),
        ("Abandoning the pattern after one failed attempt", "Outcome bias: judging a decision by a single result", "Viable patterns are discarded on statistical noise", "Evaluate a pattern over a minimum of five executions before changing the plan"),
    ],
    "drill": [
        ("Serve +1 Architecture", "Serve, then immediately hit the pre-declared +1 into a 2 m target zone", "4 x 10 serves", "Declare the target before the toss, not after the return", "60 s between sets"),
        ("Return Depth Ladder", "Return first and second serves, scoring only returns that land beyond 6 m", "3 x 12 returns", "Depth first, pace second", "45 s"),
        ("Occlusion Recognition", "Partner occludes racket face until 200 ms before contact; call direction out loud", "4 x 15 balls", "Call early, accept being wrong, then correct", "30 s"),
        ("Leverage Simulation", "Play tiebreaks starting at 4-4 with normal scoring but contracted risk rules", "5 tiebreaks", "At 4-4 and beyond, first-serve percentage over ambition", "2 min between tiebreaks"),
        ("Pattern Adherence Set", "Play a 4-game set with a fixed pattern per game, tracked by a partner", "4 games", "Execute the plan; do not grade the points", "90 s"),
        ("Displacement Attack", "Feed a ball, partner recovers to center, you must move them beyond 2.5 m before attacking", "3 x 8 points", "Displace first, attack second", "60 s"),
    ],
    "video": [
        "Watch the server's recovery footwork immediately after contact: elite servers are already balanced for the +1 before the return crosses the net.",
        "Observe the returner's stance height on second serves - a forward-leaning, stepping-in posture is the visible signature of an attacking return intention.",
        "Note the shoulder-line angle at the opponent's contact; this single cue predicts direction more reliably than racket-face tracking alone.",
        "Track the recovery position after each shot: the strongest players recover to a dynamic bisector, not to the painted center mark.",
        "Study deceleration patterns: a shortened follow-through on an easy ball is the visible marker of late classification.",
        "Compare body language across score states at 4-4 and above - elite competitors maintain identical pre-point routines at high leverage.",
    ],
    "rubric": [
        ("Court Geometry Awareness", "Targets chosen by habit; center of court only", "Can identify open court after the ball is struck", "Pre-selects angular targets based on opponent displacement", "Manipulates the error budget deliberately, spending angle only when displacement exceeds 2.5 m"),
        ("Pattern Adherence", "No declared pattern; plays each point reactively", "Declares a pattern but abandons it after one error", "Executes the declared pattern in most neutral points", "Executes and re-prices the pattern according to score-state leverage"),
        ("Recognition Speed", "Reacts to the ball after the bounce", "Classifies ball type after the bounce", "Classifies before the bounce using two cues", "Classifies before the bounce with a third cue and commits without revision"),
        ("Serve +1 Integration", "Serve treated as a standalone shot", "Recovery footwork sometimes suits the intended +1", "Recovery always loads the intended +1", "The +1 is chosen to exploit the opponent's most probable return, pre-declared before the toss"),
        ("Leverage Discipline", "One risk level for all points", "Aware of break points but not of adjusted targets", "Contracts risk at high leverage and expands it at low leverage", "Quantifies the risk adjustment and reviews it after the match"),
        ("Match Audit Practice", "No post-match review", "Recalls a general impression", "Counts pattern outcomes after the match", "Counts pattern outcomes by score state and updates the opponent profile before the next match"),
    ],
    "dosage": [
        "Tactical pattern work belongs in the **early, fresh portion** of a session: decision quality collapses measurably after 70-80 minutes of high-intensity hitting, well before physical fatigue is perceived.",
        "Two to three tactical blocks per week are sufficient for pattern consolidation; additional volume without scoring feedback produces no measurable improvement.",
        "Every tactical block must include at least one **scored condition** (tiebreak, 4-game set, or target points); unscored pattern rehearsal produces execution without commitment.",
        "Total weekly decision load should be capped so that no single session exceeds roughly 120 high-leverage decisions; beyond that, adherence degrades faster than fitness gains.",
    ],
    "decision": [
        "If the opponent's return depth averages below 5.5 m, serve and volley or attack the +1 immediately; there is no neutral rally to be won.",
        "If your pattern adherence stalls below 55% across two sets, simplify to a single pattern until adherence recovers, then re-expand.",
        "If unforced errors exceed 12 per set with no compensating winners, contract the risk envelope before changing technique.",
        "If the opponent repeatedly escapes from defensive positions, the escape pattern - not the defensive shot - is the target of the next adjustment.",
    ],
    "progression": [
        "Weeks 1-2: one declared pattern per game, tracked by a partner, with no score pressure.",
        "Weeks 3-4: two patterns per game, scored tiebreaks, and a written opponent profile updated each set.",
        "Weeks 5-8: full leverage modeling with contracted risk at break points, plus a post-match audit of pattern adherence by score state.",
    ],
}

# ----------------------------------------------------------------------------
# PILLAR V - CONDITIONING
# ----------------------------------------------------------------------------
EN_POOL["conditioning"] = {
    "intent": [
        r"""Physical preparation for tennis is **not** general fitness with a racket in hand. Tennis is an intermittent, multi-directional, high-deceleration sport whose decisive physiological qualities are repeated-sprint ability, eccentric braking capacity, rotational power endurance, and autonomic recovery speed. Training that ignores the sport's actual loading signature produces athletes who test well and break down in the third set, because they have trained qualities the match does not demand and neglected the ones it does.""",
        r"""Adaptation is a **dose-response relationship with a recovery term in the denominator**. The same session can be anabolic or destructive depending on where it sits relative to the previous stimulus. This is why the ordering of hard days, the sleep and nutritional context between them, and the objective monitoring of recovery markers matter as much as the content of the session itself. Conditioning without recovery management is simply accumulated fatigue with a training log attached.""",
        r"""The most frequently neglected quality at competitive levels is **eccentric and isometric capacity** - the ability to absorb force and hold position. Tennis points are decided in the 80-150 ms after a direction change, where the limiting factor is not concentric strength but the ability to brake, stabilise, and re-accelerate without energy leakage through the trunk and hip. Athletes who train only concentric power improve their best-case outputs while leaving their worst-case positions - the ones that decide matches - untouched.""",
        r"""Finally, every conditioning decision must be filtered through the **individual response profile**. Chronological age, training age, sleep architecture, menstrual cycle phase where relevant, prior injury history, and autonomic baseline all shift the appropriate dose by large margins. Protocols published for elite populations are hypotheses to be tested on the individual, not prescriptions to be applied verbatim.""",
    ],
    "sub": [
        (
            "Energy System Demands of Match Play",
            "A competitive tennis match is an **alactic-aerobic hybrid**: the majority of points last under 10 s and are separated by 20-25 s of recovery, so the phosphagen system supplies the decisive work while the aerobic system governs how quickly that system is reconstituted between points and between games. Training priority therefore follows the recovery interval, not the point duration.",
            [
                "Mean point duration is 4-8 s on clay and 3-6 s on hard courts; work-to-rest ratios cluster around 1:3 to 1:5.",
                "Match duration of 90-180 min with 45-60% of time spent in active recovery implies a high aerobic contribution to total energy turnover.",
                "Phosphocreatine resynthesis follows a fast and a slow component, with roughly 85-95% restored after 60-90 s of complete recovery.",
                "Training the recovery interval (20-25 s) is more transferable than training maximal point duration.",
            ],
        ),
        (
            "Neuromuscular & Tendon Adaptation",
            "Tendon and connective tissue adapt on a **slower timescale than muscle**, which is the structural reason that rapid loading increases produce tendinopathy before they produce performance. Collagen turnover requires mechanical loading plus adequate recovery time, and it responds best to moderate loads applied frequently rather than maximal loads applied occasionally.",
            [
                "Collagen synthesis peaks roughly 24-36 h after loading and remains elevated for up to 72 h, which sets the minimum spacing for high-impact sessions.",
                "Isometric and heavy-slow-resistance protocols produce analgesic effects that can mask ongoing pathology; pain must be tracked, not merely suppressed.",
                "Patellar and Achilles tendon stiffness increases measurably across 8-12 weeks of progressive loading; abrupt volume jumps above 20% per week invert that trend.",
                "Eccentric capacity below 1.5 x body mass on single-leg heel raise endurance is a practical flag for lower-limb risk.",
            ],
        ),
        (
            "Autonomic Recovery & Monitoring Markers",
            "Autonomic state determines whether a given session will be absorbed or accumulated. The practical monitoring set is deliberately small: **resting heart rate, heart-rate variability, sleep duration and quality, perceived readiness, and session RPE load**. Trends across 7-day rolling windows carry information that single-day values do not.",
            [
                "A 7-day rolling decrease in HRV above 10-12% alongside a 5-7 bpm rise in resting heart rate indicates accumulated strain.",
                "Session RPE multiplied by duration (arbitrary units) gives a load metric that tracks week-to-week progression without laboratory equipment.",
                "Acute:chronic workload ratios above roughly 1.5 are associated with elevated injury risk in intermittent sports.",
                "Sleep below 7 h for consecutive nights reduces both reactive agility and decision accuracy before it reduces raw strength.",
            ],
        ),
        (
            "Periodisation & Load Distribution",
            "Periodisation is the deliberate sequencing of stress so that adaptation accumulates while fatigue is periodically discharged. For tennis, the constraint is that technical and tactical work must remain high-quality year-round, so conditioning volume is distributed around competition rather than off-season blocks alone.",
            [
                "A practical annual structure: 8-10 weeks general preparation, 6-8 weeks specific preparation, then in-season maintenance at roughly 40-60% of peak volume.",
                "Tapering 7-14 days before a priority event with a 40-60% volume reduction preserves fitness while restoring autonomic balance.",
                "Strength maintenance requires as little as one session weekly at moderate volume once a base is established.",
                "Hard days should be separated by at least one recovery-oriented day when the following session requires decision quality.",
            ],
        ),
        (
            "Movement Signature, Deceleration & Change of Direction",
            "Tennis movement is dominated by **lateral and diagonal braking**. Each change of direction requires a plant, an eccentric absorption phase, and a re-acceleration, and the brake quality limits the subsequent acceleration. Conditioning that trains only straight-line speed leaves the most frequently used pattern untrained.",
            [
                "Elite players execute 3-6 direction changes per point; deceleration forces can exceed 3-4 times body mass at the plant foot.",
                "Penultimate-step shortening is the observable marker of efficient braking; a long final step converts into a slow, energy-expensive stop.",
                "Lateral shuffle-to-sprint transitions should be trained with external cues to preserve reactive rather than pre-planned movement.",
                "Hip abduction and external rotation strength are the primary controllable limiters of braking capacity.",
            ],
        ),
        (
            "Concurrent Training Interference & Session Ordering",
            "Strength, power, and endurance adaptations interact, and the interference is largely a **session-ordering problem**. Placing high-intensity aerobic work immediately before maximal strength work degrades both the quality of the strength session and the retention of the adaptation, whereas the reverse order or adequate separation preserves both.",
            [
                "Separate maximal-strength and high-intensity-endurance sessions by at least 6 h, or place them on different days, when the goal is power retention.",
                "Perform explosive and technical work before fatiguing work within the same session.",
                "Protein intake of 0.3 g/kg within the post-session window reduces the practical interference effect on strength adaptation.",
                "Concurrent training is acceptable in-season; the constraint is sequencing and recovery, not the mere coexistence of modalities.",
            ],
        ),
    ],
    "step": [
        ("Baseline Assessment", "Pre-block, 60-90 min session", "Establish the individual's current values before any prescription: movement screen, single-leg braking quality, aerobic baseline, and autonomic baseline."),
        ("Readiness Gate", "5-10 min before the session", "Read the daily readiness markers and choose one of three session variants: as planned, reduced volume, or recovery replacement."),
        ("General Warm-Up", "12-18 min escalating", "Progressive elevation, joint mobilisation, and dynamic patterning with no static stretching before explosive work."),
        ("Neural Priming", "6-8 min", "Short-duration, high-quality jumps, throws, or med-ball work to raise the nervous system's output ceiling without accumulating fatigue."),
        ("Primary Stimulus", "25-40 min", "The session's main adaptation target, executed while fresh, with full technical standards and defined rest intervals."),
        ("Accessory & Prehabilitation", "15-20 min", "Targeted work for individually identified limiters: tendon capacity, hip and scapular control, calf and foot intrinsic strength."),
        ("Conditioning Finish", "10-20 min", "Sport-specific intermittent work at controlled work-to-rest ratios, sized to the current block's intent."),
        ("Downshift & Rehydration", "10-15 min", "Parasympathetic downshift, breathing work, and immediate rehydration and carbohydrate-protein intake."),
    ],
    "metric": [
        ("Resting Heart Rate", "Morning supine measurement, 7-day rolling mean", "52-58 bpm", "42-48 bpm"),
        ("Heart-Rate Variability", "rMSSD, 7-day rolling mean", "55-75 ms", "80-110 ms"),
        ("Sleep Duration", "Nightly total sleep time", "7.0-8.0 h", "8.0-9.0 h"),
        ("Session Load", "Session RPE x duration (arbitrary units)", "250-400 AU/day", "400-650 AU/day"),
        ("Acute:Chronic Ratio", "7-day load / 28-day load", "0.8-1.3", "0.9-1.2"),
        ("Repeated-Sprint Decrement", "Percent drop in sprint time across 6 x 30 m", "4-7%", "2-4%"),
        ("Single-Leg Braking Quality", "Penultimate-step shortening score (0-5 scale)", "3-4", "4-5"),
        ("Change-of-Direction Time", "5-10-5 shuttle or tennis-specific 505", "2.55-2.75 s", "2.30-2.50 s"),
    ],
    "error": [
        ("Training hard sessions on consecutive days", "Programme is built from a session library rather than a load model", "Accumulated fatigue reduces decision quality and raises soft-tissue risk", "Separate hard days by at least one recovery-oriented day; track the acute:chronic ratio and hold it between 0.8 and 1.3"),
        ("Static stretching before explosive work", "Traditional warm-up habit retained from junior coaching", "Acute reductions in power output of 4-8% for up to 60 min", "Replace pre-session static work with dynamic mobilisation and neural priming, and move static work to post-session"),
        ("Ignoring sleep debt when interpreting poor performance", "Sleep is treated as lifestyle rather than as training input", "Readiness markers are misread as under-training, prompting additional load", "Record sleep nightly and treat sub-7 h nights as a scheduling constraint, not a motivation problem"),
        ("Progressing volume by more than 20% per week", "Enthusiasm or calendar compression before a tournament", "Tendon and connective tissue lag behind muscle, producing tendinopathy", "Cap weekly volume progression at roughly 10-15% and hold one week in three at a reduced load"),
        ("Training only concentric power", "Gym culture emphasises lifting and jumping rather than braking", "Direction changes remain slow and energy-expensive despite good test numbers", "Programme eccentric and isometric capacity at least twice weekly with measurable braking targets"),
        ("Concurrent endurance immediately before maximal strength", "Single-session time pressure", "Both adaptations are blunted and the strength session's technique degrades", "Order explosive and strength work first, or separate the two sessions by 6 h or more"),
        ("Using a single-day HRV value to change the plan", "Daily fluctuations are interpreted as signal rather than noise", "Programme oscillates and loses its progression structure", "Only act on 7-day rolling trends, and act by adjusting volume rather than by cancelling the stimulus"),
        ("Skipping rehydration and post-session nutrition", "Training ends when the last ball is hit", "Recovery is prolonged and the next session begins from a deficit", "Standardise a 10-15 min downshift block with fluids, electrolytes, and 0.3 g/kg protein"),
    ],
    "drill": [
        ("Intermittent Court Conditioning", "6 x 45 s of sport-specific movement at 1:2 work-to-rest", "6 reps x 2 sets", "Match the movement signature: lateral and diagonal braking, not straight lines", "90 s between sets"),
        ("Eccentric Braking Ladder", "Single-leg drop landings and lateral plant-and-hold, 5 positions", "4 x 6 per leg", "Quiet landings; absorb, do not collapse", "60 s"),
        ("Tendon Capacity Block", "Heavy-slow calf and patellar tendon loading at 3 s up / 3 s down", "4 x 8", "Slow tempo, full range, no bouncing", "90 s"),
        ("Rotational Power Circuit", "Med-ball rotational throws, side throws, and scoop tosses", "3 x 8 per side", "Hips initiate, trunk transfers, arms finish", "45 s"),
        ("Repeated-Sprint Set", "6 x 30 m with 25 s recovery, tracked for decrement", "2 sets", "Hold the first rep's quality; stop the set when decrement exceeds 7%", "3 min between sets"),
        ("Autonomic Downshift", "Diaphragmatic breathing 4 s in / 6 s out with legs elevated", "8-10 min", "Exhale longer than inhale; aim for a measurable HR drop", "continuous"),
    ],
    "video": [
        "Observe the plant foot at each direction change: the penultimate step should shorten, and the knee should track over the toe without valgus collapse.",
        "Watch trunk position under fatigue in the final games - a rising centre of mass and reduced hip flexion are the earliest visible markers of accumulated load.",
        "Note breathing mechanics during the 20-25 s between points; elite competitors restore nasal, diaphragmatic breathing rather than gasping.",
        "Track the first two steps after the split step: elite movers use a short, direction-setting first step instead of a long, slow lunge.",
        "Study service and overhead landing mechanics - eccentric control at landing is where most lower-limb tendon load accumulates.",
        "Compare movement quality in the first and last 15 minutes of a session; a large degradation indicates the session's dose exceeded its recovery capacity.",
    ],
    "rubric": [
        ("Load Management Discipline", "Sessions chosen by feel with no load record", "Records sessions but does not track trends", "Maintains acute:chronic ratio within 0.8-1.3 and adjusts weekly", "Models load against readiness markers and pre-plans deloads before competition"),
        ("Eccentric & Braking Capacity", "No dedicated eccentric work", "Occasional landing drills without measurable targets", "Twice-weekly eccentric block with tracked single-leg quality", "Integrates braking capacity into sport-specific patterns with external cues and fatigue conditions"),
        ("Autonomic Monitoring", "No monitoring", "Measures resting heart rate sporadically", "Daily HRV and resting heart rate with 7-day rolling review", "Uses rolling trends to select among pre-planned session variants rather than improvising"),
        ("Sleep & Recovery Practice", "Sleep is unmanaged", "Aware of sleep importance but no data", "Nightly sleep duration recorded, sub-7 h nights flagged", "Sleep and nutrition scheduled as training inputs with tracked compliance"),
        ("Tendon & Joint Preparation", "No prehabilitation", "Occasional accessory work", "Individualised accessory block targeting identified limiters", "Tendon capacity programmed across the season with progressive loading and monitored pain response"),
        ("Concurrent Training Sequencing", "Endurance and strength randomly ordered", "Strength generally first but not consistently", "Explosive and strength work always precede fatiguing work", "Sessions separated by 6 h or more with nutrition timed to minimise interference"),
    ],
    "dosage": [
        "For in-season maintenance, **two strength sessions and two conditioning sessions per week** preserve most adaptations; the constraint is not the number of sessions but the quality of the first 20 minutes of each.",
        "Tendon and accessory work tolerates - and benefits from - higher frequency: 3-4 short exposures per week beat one long session for connective tissue adaptation.",
        "High-intensity intermittent conditioning should not exceed 2-3 exposures weekly in-season, each capped so that the following day's decision quality remains intact.",
        "Deload weeks every third or fourth week (volume reduced 30-40%, intensity maintained) produce better long-term progression than continuous loading in most athletes.",
    ],
    "decision": [
        "If the 7-day HRV trend falls more than 10-12% with a rising resting heart rate, replace the planned session with an aerobic-recovery variant and re-assess in 24 h.",
        "If single-leg braking quality scores below 3, hold conditioning progression and prioritise eccentric capacity for two weeks.",
        "If repeated-sprint decrement exceeds 7%, the set is terminated - continuing trains fatigue tolerance at the expense of speed quality.",
        "If sleep is below 7 h for three consecutive nights, reduce session volume by 20-30% rather than cancelling, and protect the next night's sleep.",
    ],
    "progression": [
        "Weeks 1-3: baseline assessment, movement quality, tendon preparation at low intensity, and consistent autonomic monitoring.",
        "Weeks 4-8: progressive strength and eccentric loading with sport-specific intermittent conditioning at controlled ratios.",
        "Weeks 9-12: competition-phase maintenance with pre-planned deloads, tapering, and load decisions driven by rolling readiness trends.",
    ],
}
