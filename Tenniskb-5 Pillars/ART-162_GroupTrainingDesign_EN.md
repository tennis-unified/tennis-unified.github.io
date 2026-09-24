# ART-162: Group Training Design — Academy Systems Architecture

## Executive Summary
An academy is not a collection of private lessons; it is a system that produces players at scale. This article provides the architectural blueprint for group training: court organization, player grouping, session flow, and the integration of the 5-Pillar curriculum across a squad.

## The Academy System Hierarchy

### 1. Program Levels (Vertical Integration)
| Level | Age/Stage | Focus | Court Ratio | Session Freq |
| :--- | :--- | :--- | :--- | :--- |
| **Foundation (Red/Orange/Green Ball)** | U8–U10 | Physical Literacy + Fun + Basics | 6:1 | 2-3x/week |
| **Development (Yellow Ball U12–U14)** | U12–U14 | Skill Acquisition + Tactics + Athleticism | 4:1 | 4-6x/week |
| **Performance (U14–U18 ITF)** | U14–U18 | Weapon Building + Periodization + Mental | 3:1 | 10-14x/week |
| **Pro / Transition** | 18+ | Tour Readiness + Individualization | 2:1 / 1:1 | 15-20x/week |

### 2. The Daily Schedule Template (Performance Level)
| Time | Block | Content | Pillar Focus | Coach Role |
| :--- | :--- | :--- | :--- | :--- |
| **08:00-09:30** | **Technical-Tactical** | Theme-based, live ball, constraints | III, IV, I | Lead / Design |
| **09:30-10:00** | **Physical** | Gym / Track / Court Conditioning | I, V | S&C Coach |
| **10:00-10:15** | **Break / Fuel** | Nutrition / Hydration / Mental Reset | V, II | Monitor |
| **10:15-11:45** | **Match Play / Scenarios** | Sets, Tiebreaks, Score scenarios | IV, II, V | Observe / Data |
| **11:45-12:00** | **Cool Down / Review** | Stretch, Journal, Coach Check-in | I, V | Facilitate |

## Court Organization: The "Station Rotation" Model

### 4-Court, 12-Player, 2-Coach Model (Development)
*   **Court 1 (Coach A):** Technical Theme (e.g., Serve +1 Patterns). 4 Players.
*   **Court 2 (Coach B):** Tactical Theme (e.g., Building Points Cross-Court). 4 Players.
*   **Court 3 (Assistant/S&C):** Physical / Athletic Development. 4 Players.
*   **Court 4 (Autonomous):** Mental Skills / Video Analysis / Recovery. 4 Players (Rotating).
*   **Rotation:** 90 min blocks. Players hit all 4 pillars daily.

### Grouping Logic (The "Challenge Point" System)
*   **Not by Age.** By *Competitive Level* (UTR/WTN/Internal Rating).
*   **Fluid Movement:** Weekly "Challenge Matches" determine court assignment for next week.
*   **Top Court = Highest Intensity/Expectation.** Bottom Court = Highest Volume/Fundamentals.

## The 5-Pillar Curriculum Mapping (Weekly Microcycle)

| Day | Pillar I (Bio) | Pillar II (Neuro) | Pillar III (Tech) | Pillar IV (Tact) | Pillar V (Cond) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Mon** | Kinetic Chain Mechanics | Anticipation Drills | Serve / Return Tech | Serve +1 / Ret +1 Patterns | Aerobic Base (Tempo) |
| **Tue** | Power Conversion (Med Ball) | Decision Speed Games | Forehand Weapon | First Strike Patterns | Anaerobic Power (RSA) |
| **Wed** | Mobility / Prehab | Visual Tracking | Backhand Stability | Neutral / Defense | Recovery / Yoga |
| **Thu** | Strength (Gym) | Pressure Simulation | Transition / Net | Game Plan Execution | Glycolytic Intervals |
| **Fri** | Reactive Movement | Match Play Analysis | Weapon Refinement | Scenario Sets (4-4, TB) | Pre-Match Taper |
| **Sat** | **Competition / Match Play** | | | | |
| **Sun** | **Recovery / Off** | | | | |

## Managing the "Group vs. Individual" Tension

### 1. The 80/20 Rule
*   **80% Group:** Shared warm-ups, physical, tactical themes, match play.
*   **20% Individual:** Technical "prescriptions" (1-on-1 15 min slots), video review, goal setting.

### 2. Individual "Prescription Cards"
Each player carries a card:
*   **Technical Key:** "Backhand contact point."
*   **Tactical Key:** "Serve wide +1 FH."
*   **Mental Key:** "Breathing routine."
*   **Physical Key:** "Ankle mobility."
*   *Coach references card during group drills to individualize feedback.*

## The Coaching Team Structure

| Role | Responsibility | Pillars |
| :--- | :--- | :--- |
| **Head Coach / Program Director** | Curriculum, Culture, Parent Comms, Progression Decisions | All (Strategy) |
| **Technical Lead (Coach A)** | Stroke mechanics, Skill acquisition design | I, III |
| **Tactical Lead (Coach B)** | Patterns, Match play, Scouting, Game plans | II, IV |
| **S&C Coach** | Physical testing, Gym, On-court conditioning, Injury liaison | I, V |
| **Mental Skills Coach** | Routines, Pressure training, Life skills | II, V |
| **Assistant / Hitting Partners** | Ball feeding, Drill management, Volume | III, IV |

## Diagnostic & Training Matrix

| System Symptom | Structural Failure | Architectural Fix |
| :--- | :--- | :--- |
| "Dead" court energy | All players same drill, no competition | Gamify everything. Score every drill. |
| Top players bored / Bottom players lost | Grouping by age, not level | Implement Challenge Point System. Weekly resorting. |
| Technical gaps persist in match play | No individual prescription in group | Mandatory Prescription Cards. 15-min 1-on-1 slots. |
| High injury rate | S&C siloed from tennis coaches | Integrated S&C. Shared daily wellness sheet. |
| Parents complaining "not enough attention" | No communication structure | Weekly 5-min coach-player-parent huddle. Monthly report card. |

## Practical Application: "The Factory"
A private lesson is a tailor shop — bespoke, slow, expensive. An academy is a factory — standardized processes, quality control, scalable output. But the *raw material* (athletes) varies. The system must be rigid enough to ensure quality, flexible enough to fit the individual. Design the conveyor belt; monitor the product.
