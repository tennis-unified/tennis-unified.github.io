---
title: Rod Cross Double Pendulum — complete technical reference
description: Complete technical reference for Rod Cross's double-pendulum model of tennis strokes, with timing data, model parameters, and energy transfer analysis.
---

# Rod Cross Double Pendulum — complete technical reference

**The most important tennis physics paper you probably haven't read.**

Rod Cross's 2011 paper in *American Journal of Physics* 79 (5), 470 — *"A double pendulum model of tennis strokes"* — gives tennis players and coaches a quantitative framework for what was previously only folklore: **why the forearm decelerates just before ball impact**, **how the wrist unlocks to multiply racquet speed**, and **what each stage of the swing is actually doing mechanically**.

This reference collects all of Cross's published data into one place, for both the serve and the forehand.

---

## Why the double pendulum?

The forearm + racquet acts as a double pendulum during tennis strokes. Treating the upper arm separately, the two-segment model gives tractable equations of motion that match high-speed video of real serves and forehands to within a few percent.

The double pendulum:

- **Segment 1:** Forearm (~1.5 kg, ~25 cm from elbow to wrist)
- **Segment 2:** Racquet (~300 g, ~70 cm from butt to tip, swing weight ~310 kg·cm², balance 35 cm from butt)
- **Joint between them:** Wrist, with torque couple C₂ (controlled by wrist muscles)
- **Plus the elbow** applying torque couple C₁ to segment 1

The system is **non-minimum phase** — the racquet can accelerate or decelerate independently of the forearm. This is the key insight.

---

## The serve: three-stage timing model

Cross filmed serves at 300 fps with ~100 mph impact. The serve divides into three distinct stages:

### Stage 1 — Upper arm reaches maximum speed (t = 0 to 0.05 s)

- Upper arm swings from approximately horizontal to vertical
- Forearm remains horizontal and stays locked at right angles to upper arm
- This is the "high elbow" position — the same kinematic seen in elite servers
- Wrist is locked (no wrist torque)

### Stage 2 — Forearm reaches maximum speed (t = 0.05 to 0.103 s, Δt = 0.053 s)

- Forearm swings from horizontal to vertical
- Racquet remains locked at 90° to forearm (wrist still locked)
- Combined angular speed = **90° / 0.053 s = 1700°/s = 4.72 rev/s = 283 rpm**
- During this stage, the upper arm begins to decelerate as it transfers energy to the forearm

### Stage 3 — Racquet reaches maximum speed (t = 0.103 to 0.123 s, Δt = 0.020 s)

- Wrist unlocks (the critical moment)
- Forearm rotates only ~10° while racquet rotates 90°
- Average forearm angular speed = **500°/s ≈ 83 rpm**
- Average racquet angular speed = **4500°/s ≈ 750 rpm**
- **Just before impact, racquet hits 6000°/s ≈ 1000 rpm**

This is the energy transfer moment: **the forearm decelerates (giving up its angular momentum), the racquet accelerates (taking it up)**.

---

## Energy transfer principle (Cross 2011)

> "Before the forearm slows down, the upper arm slows down to transfer its energy to the forearm. And before that, the upper torso slows down to transfer its energy to the upper arm."

> "In an efficient tennis (or golf or baseball) swing, energy is first transferred from the upper arm to the forearm and is subsequently transferred from the forearm to the racquet after a short time delay."

This is the **kinematic chain** in its most rigorous form: the kinetic energy propagates from segment to segment, each one decelerating as it hands off to the next. The racquet — being the lightest segment with the largest moment arm — gets the highest tip speed.

---

## Forehand model parameters (Cross's published values)

| Parameter | Value |
|-----------|-------|
| Racquet mass | 300 g |
| Racquet length | 70 cm |
| Swing weight | 310 kg·cm² |
| Balance | 35 cm from butt |
| Forearm mass | 1.5 kg |
| Hand mass | 0.5 kg |
| Elbow torque couple (C₁) | **25 N·m** |
| Wrist torque couple (C₂) | **2.5 N·m** |
| Final forearm deceleration | ~0.2 s |

With C₂ held constant, the racquet accelerates while the forearm decelerates over the final ~0.2 s. **This is the energy-transfer signature** — if you see a forehand where the forearm continues to accelerate through contact, the wrist isn't doing its job and power is leaking.

---

## Other measured quantities

- **Wrist torque max:** ~30 N·m; player can only generate ~20 ft-lbs from wrist (~27 N·m) — the wrist is near its mechanical limit in any powerful stroke
- **Forearm and racquet remain at right angles for ~80 % of the swing** — the wrist only unlocks in the last fraction of a second
- A triple-pendulum (upper arm + forearm + racquet) is more accurate than a double, but the double captures the dominant energy-transfer events

---

## The wrist question: who rotates whom?

> "Does the racquet rotate the wrist, or vice versa?" — Cross 2011

Answer: **sometimes the racquet is so fast that it rotates the hand**. When the wrist muscles reach their torque limit (~30 N·m max), the racquet can drag the hand around. This is more common at higher swing speeds and is one reason why extremely fast swings sometimes feel "out of control."

---

## The triple pendulum and the upper torso

The full serve is actually a **triple pendulum**: upper torso → upper arm → forearm → racquet. The sequencing is:

1. Upper torso decelerates, transfers energy to upper arm
2. Upper arm decelerates, transfers energy to forearm
3. Forearm decelerates, transfers energy to racquet
4. Racquet hits ball

Each transition happens at a slight time delay (~20–50 ms), which is what allows the segments to peak in speed sequentially and the racquet to reach the highest tip speed at the moment of impact.

---

## Mechanical analogy

Cross demonstrates that a passive double pendulum — a sawn-off baseball bat as "forearm" and a wood dowel as "racquet", connected by two eye hooks held loosely with a bolt — reproduces serve motion under gravity alone. With only minor elbow/wrist torque modifications, this simple mechanical model mimics the real serve.

The implication: **the basic physics of the serve is gravity + the geometry of the double pendulum + torque couple controls at the joints**. Coaching cues like "let the forearm slow down so the racket can speed up" are direct applications of the physics.

---

## Practical coaching takeaways

1. **Don't fight the deceleration.** When coaches say "let the forearm decelerate," they're describing Cross's energy-transfer mechanism. Don't try to keep accelerating the forearm through contact — the racquet needs the energy.
2. **The wrist unlocks last.** If you unlock the wrist too early, you dump energy into the racquet before it's optimally positioned. The wrist should unlock in the last 10 % of the swing.
3. **Strength matters at the wrist, not the hand.** The wrist torque limit (~30 N·m) is a mechanical ceiling. Wrist-strength training has real value but won't make you serve 150 mph — the upstream kinetic chain matters more.
4. **Racket weight is a double-edged sword.** Heavier rackets have higher swing weight (more momentum) but require more elbow/wrist torque to handle. Cross's equations let you calculate the trade-off for any given racket.
5. **The triple pendulum is the goal.** Coaching that ignores the upper torso and just focuses on the arm is missing 50 %+ of the energy chain.

---

## References

- Cross, R. (2011). *A double pendulum model of tennis strokes*. American Journal of Physics 79 (5), 470. DOI: 10.1119/1.3550242
- Cross, R. (2006). *Physics of the Tennis Kick Serve*. TWU Learning Center.
- Cross, R. & Lindsey, C. (2013). *Measurements of drag and lift on tennis balls in flight*. Sports Engineering.
- Kotze, J., Mitchell, S. R., & Rothberg, S. J. (2001). *The role of the racket in high-speed tennis serves*. Sports Engineering.
- Local cache: `D:/Users/Phamd/Documents/tennis_gap_analysis/extracted/The_Double_Pendulum_In_Tennis.docx.txt`

---

[← Back to Tier 1 high-value gaps](../../reports/tier-1-high-value-gaps/#1-rod-cross-double-pendulum-swing-mechanics) · [Browse all tennis books](../../)
