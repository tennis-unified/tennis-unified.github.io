# ART-207: Diagnostic App Logic — The 5-Pillar Decision Engine

## Executive Summary
This article specifies the logic, algorithms, and data structures for a "5-Pillar Diagnostic App" — a clinical decision support tool that encodes the Tennis Knowledgebase into executable diagnostic pathways. It transforms 200 articles of expert knowledge into a structured, queryable, and auditable software system for coaches, medics, and athletes.

## System Architecture: The Diagnostic Engine

### Core Philosophy
*   **Expert System, Not Black Box AI:** Transparent rule-based logic derived from the 5-Pillar articles. Every recommendation traces to a specific ART reference.
*   **Differential Diagnosis First:** Never single-pathway. Always presents ranked differential with confidence intervals.
*   **Action-Oriented Output:** Diagnosis → Matched Protocol → Monitoring Gates → Review Date.
*   **Athlete-Centric:** Inputs are athlete-reported + coach-observed + sensor-derived. Outputs are personalized.

### Data Model: The Athlete State Vector (ASV)

```typescript
interface AthleteStateVector {
  // Identity & Context
  athleteId: string;
  timestamp: Date;
  age: number;
  biologicalAge: number;      // PHV offset
  sex: 'M' | 'F';
  handedness: 'R' | 'L';
  playingStyle: 'Baseline' | 'All-Court' | 'Serve-Volley' | 'Counterpuncher';
  currentRank: number;
  targetRank: number;
  surface: 'Clay' | 'Grass' | 'Hard' | 'Carpet';
  phase: 'Base' | 'Pre-Comp' | 'Comp' | 'Transition';
  daysSinceLastMatch: number;
  
  // Pillar I: Biomechanics & Medical
  pillar1: {
    grfProfile: 'Vertical' | 'Horizontal' | 'Linear' | 'Mixed';
    kineticChainIntegrity: 'Intact' | 'Compromised' | 'Unknown';
    hipSeparationDeg: number;        // Measured
    xFactorDeg: number;              // Measured
    coreBracingScore: 1-10;          // Subjective + Objective
    injuryHistory: Injury[];         // Structured: site, type, date, RTP status
    currentPain: PainMap[];          // Body chart + severity 0-10
    romDeficits: ROMDeficit[];       // Joint, plane, degrees
    strengthAsymmetries: Asymmetry[]; // Limb, metric, %
    grfAsymmetryPct: number;         // Force plate derived
  };
  
  // Pillar II: Neuro-Cognitive & Mental
  pillar2: {
    visualAcuity: number;            // LogMAR
    contrastSensitivity: number;     // Pelli-Robson
    depthPerception: 'Normal' | 'Reduced';
    quietEyeMs: number;              // Eye-tracker derived
    anticipationScore: number;       // Occlusion test %
    decisionSpeedMs: number;         // Choice RT
    workingMemorySpan: number;       // Digit span / n-back
    attentionalControl: 'High' | 'Moderate' | 'Low'; // Questionnaire + Dual-task
    csaI2rCognitive: number;         // CSAI-2R Cognitive Anxiety
    csaI2rSomatic: number;           // CSAI-2R Somatic Anxiety
    csaI2rConfidence: number;        // CSAI-2R Self-Confidence
    pomsProfile: POMSProfile;        // Tension, Depression, Anger, Vigor, Fatigue, Confusion
    routineFidelityPct: number;      // Between-point routine compliance
    flowStateFrequency: 'Never' | 'Rare' | 'Sometimes' | 'Often' | 'Always';
  };
  
  // Pillar III: Technical Production
  pillar3: {
    serve: {
      firstServePct: number;
      firstServeSpeedKph: number;
      firstServeSpinRpm: number;
      firstServePlacementAccuracy: number; // % in target zone
      secondServeSpinRpm: number;
      secondServeDepthPct: number;
      tossConsistencyScore: 1-10;
      routineFidelityPct: number;
    };
    forehand: {
      grip: 'Eastern' | 'SemiWestern' | 'Western';
      contactHeightCm: number;
      contactDistanceCm: number;
      spinRpm: number;
      speedKph: number;
      depthPct: number;              // % past service line
      consistencyPct: number;        // In court
      insideOutPct: number;          // Usage rate
    };
    backhand: {
      type: '1HBH' | '2HBH';
      grip: string;
      contactHeightCm: number;
      spinRpm: number;
      speedKph: number;
      depthPct: number;
      consistencyPct: number;
      sliceUsagePct: number;
      sliceQuality: 1-10;
    };
    volley: {
      fhVolleyQuality: 1-10;
      bhVolleyQuality: 1-10;
      overheadQuality: 1-10;
      transitionSuccessPct: number;
    };
    return: {
      firstServeReturnInPlayPct: number;
      secondServeAttackPct: number;
      returnDepthPct: number;
      neutralizePct: number;
    };
    movement: {
      shuffleSpeedMs: number;
      crossoverSpeedMs: number;
      cod505TimeSec: number;
      codProAgilityTimeSec: number;
      recoveryStepEfficiency: 1-10;
    };
  };
  
  // Pillar IV: Tactics & Geometry
  pillar4: {
    patternLibrary: Pattern[];       // Named patterns with success rates
    firstStrikeEfficiencyPct: number;
    patternUnpredictabilityIndex: number; // Entropy measure
    courtPositionHeatmap: Heatmap;   // Time spent in zones
    tacticalDecisionAccuracy: number; // % optimal choices per scouting
    scoutingDossierQuality: 1-10;    // Opponent prep completeness
    gamePlanAdherencePct: number;    // % points played per plan
    momentumManagementScore: 1-10;   // Coach rated
    scoreboardPressurePerformance: {
      breakPointSavePct: number;
      breakPointConvertPct: number;
      setPointPerformance: 'Strong' | 'Average' | 'Weak';
      matchPointPerformance: 'Strong' | 'Average' | 'Weak';
    };
    environmentalAdaptability: {
      wind: 'High' | 'Moderate' | 'Low';
      sun: 'High' | 'Moderate' | 'Low';
      altitude: 'High' | 'Moderate' | 'Low';
    };
  };
  
  // Pillar V: Conditioning & Flow
  pillar5: {
    physical: {
      vo2maxMlKgMin: number;
      masKph: number;
      rsaTotalTimeSec: number;       // Repeated Sprint Ability
      rsaFatigueIndex: number;
      cmjHeightCm: number;
      cmjRsi: number;                // Reactive Strength Index
      sprint10mTimeSec: number;
      sprint20mTimeSec: number;
      cod505Sec: number;
      proAgilitySec: number;
      strengthBenchPress1rmKg: number;
      strengthSquat1rmKg: number;
      strengthPullUpReps: number;
      nordicsEccentricDurationSec: number;
      injuryRiskScore: number;       // Composite 0-100
    };
    recovery: {
      hrvBaselineMs: number;
      hrvCurrentMs: number;
      hrvTrend7d: 'Rising' | 'Stable' | 'Falling';
      sleepDurationHrs: number;
      sleepEfficiencyPct: number;
      sleepConsistencyScore: 1-10;   // Bed/wake time variance
      wellnessScore: 1-10;           // Daily questionnaire
      muscleSoreness: 1-10;          // Daily
      fatigueLevel: 1-10;            // Daily
    };
    nutrition: {
      dailyEnergyAvailabilityKcalKgFfm: number;
      carbIntakeGkg: number;
      proteinIntakeGkg: number;
      hydrationStatus: 'Euhydrated' | 'Hypohydrated';
      supplementCompliance: 'Full' | 'Partial' | 'None';
    };
    mental: {
      gritScore: number;             // Grit Scale
      resilienceScore: number;       // Connor-Davidson
      confidenceLevel: number;       // 1-10
      motivationProfile: 'Intrinsic' | 'Extrinsic' | 'Amotivated';
      burnoutRisk: 'Low' | 'Moderate' | 'High'; // MBI
    };
    travel: {
      tluLast7Days: number;          // Travel Load Units
      timeZonesCrossedLast14Days: number;
      circadianAlignmentScore: 1-10;
    };
  };
}
```

## Diagnostic Algorithms: The Decision Trees

### Algorithm 1: Performance Drop Differential (ART-171 Slump Audit)
**Input:** ASV with performance trend flag (KPIs declining > 2 weeks)
**Process:**
```
1. CHECK Pillar V Recovery Flags:
   IF hrvTrend7d == 'Falling' AND wellnessScore < 6 AND fatigueLevel > 6
     → PRIMARY: Physical Slump (ART-171 Physical Exit Protocol)
     → CONFIDENCE: HIGH
   ELSE IF injuryRiskScore > 70 OR currentPain.max > 4
     PRIMARY: Physical/Medical Slump
     CONFIDENCE: HIGH

2. CHECK Pillar II Mental Flags:
   IF csaI2rCognitive > 25 OR routineFidelityPct < 80 OR flowStateFrequency in ['Never','Rare']
     → PRIMARY: Mental Slump (ART-171 Mental Exit Protocol)
     CONFIDENCE: HIGH

3. CHECK Pillar III Technical Flags:
   IF serve.firstServePct < baseline - 10% OR forehand.consistencyPct < baseline - 15%
     → PRIMARY: Technical Slump (ART-171 Technical Exit Protocol)
     CONFIDENCE: MODERATE

4. CHECK Pillar IV Tactical Flags:
   IF patternUnpredictabilityIndex < baseline - 20% OR gamePlanAdherencePct < 50%
     → PRIMARY: Tactical Slump (ART-171 Tactical Exit Protocol)
     CONFIDENCE: MODERATE

5. CHECK Environmental:
   IF tluLast7Days > 50 OR timeZonesCrossedLast14Days > 6
     → CONTRIBUTORY: Environmental Slump (ART-169 Travel Protocol)

OUTPUT: Ranked Differential Diagnosis with Confidence % + Matched Exit Protocols
```

### Algorithm 2: Pressure Failure Classification (ART-176 Choke vs Panic)
**Input:** Match event data + ASV physiological/cognitive markers
**Process:**
```
FOR each pressure failure event (BP faced, MP, Set Point, Tiebreak):
  COLLECT: HR at event, HRV pre-event, self-report cognitive load, video behavioral coding
  
  IF (HR < 85% max) AND (cognitive load self-report == 'High - Technical') 
     AND (behavioral: frozen, late contact, abbreviated swing)
     → DIAGNOSIS: CHOKING (PFC Hyperactivity)
     → PROTOCOL: ART-176 Anti-Choking (PFC Quiet)
     
  ELSE IF (HR > 90% max) AND (cognitive load == 'Blank / Fear') 
     AND (behavioral: rushed, chaotic, tunnel vision, gasping)
     → DIAGNOSIS: PANICKING (Amygdala Hijack)
     → PROTOCOL: ART-176 Anti-Panicking (Amygdala Calm)
     
  ELSE IF (HR > 90% max) AND (cognitive load == 'High - Technical') 
     → DIAGNOSIS: CHOKE-PANIC SPIRAL
     → PROTOCOL: SEQUENTIAL — Panic First (Physio Reset), Then Choke (PFC Quiet)

OUTPUT: Event-by-Event Classification + Session Protocol Prescription
```

### Algorithm 3: Injury RTP Readiness (ART-148, ART-174)
**Input:** ASV medical/physical pillars + surgeon clearance
**Process:**
```
RTP_STAGE = 0
IF surgeonClearance == TRUE AND painAtRest == 0 AND sleepNormalized == TRUE:
  RTP_STAGE = 1  // Protection Phase Complete
  
IF romSymmetryPct > 95 AND strengthSymmetryPct > 90 
   AND forcePlateSymmetryPct > 90 AND yBalanceSymmetryPct > 90:
  RTP_STAGE = 2  // Load Introduction Ready
  
IF trainingWeeksPainFreeHighIntensity >= 3 
   AND psychologicalReadinessScore > 80 (ACL-RSI/TSRQ)
   AND trustMetricDaily > 8 FOR 14 consecutive days:
  RTP_STAGE = 3  // Competition Simulation Ready
  
IF practiceMatchWins > 2 at target intensity 
   AND noPainNoCompensation 7 consecutive days:
  RTP_STAGE = 4  // Full Return Authorized

OUTPUT: Current RTP Stage + Gates to Next Stage + Specific Deficits
```

### Algorithm 4: "Uncoachable" Profile Classification (ART-175)
**Input:** Coach observation log + ASV cognitive/physical/relational data
**Process:**
```
SCORES = {
  cognitive: teachBackAccuracyPct,          // Target 100%
  autonomy: athleteInitiativesPerSession,   // Target > 2
  physical: movementScreenSymmetryPct,      // Target > 90%
  relational: parentCoachAlignmentScore,    // Target: Aligned
  environmental: athleteEngagementScore     // Target > 8/10
}

PRIMARY_PROFILE = argmin(SCORES)  // Lowest scoring domain

IF PRIMARY_PROFILE == 'cognitive' AND teachBackAccuracyPct < 70:
  → DIAGNOSIS: Cognitive Mismatch (ART-175 Protocol 1)
  
ELSE IF PRIMARY_PROFILE == 'autonomy' AND athleteInitiativesPerSession == 0:
  → DIAGNOSIS: Autonomy/Trust Deficit (ART-175 Protocol 2)
  
ELSE IF PRIMARY_PROFILE == 'physical' AND movementScreenSymmetryPct < 80:
  → DIAGNOSIS: Physical Limitation (ART-175 Protocol 3)
  
ELSE IF PRIMARY_PROFILE == 'relational' AND parentCoachAlignmentScore in ['Tension','Conflict']:
  → DIAGNOSIS: Triangle Fracture (ART-175 Protocol 4)
  
ELSE IF PRIMARY_PROFILE == 'environmental' AND athleteEngagementScore < 5:
  → DIAGNOSIS: Environmental Misfit (ART-175 Protocol 5)

OUTPUT: Primary Profile + Secondary Contributors + Matched Reconstruction Protocol
```

### Algorithm 5: Style Change Readiness (ART-172)
**Input:** Athlete request + ASV technical/physical/mental + coach assessment
**Process:**
```
READINESS_SCORE = 0

// Strategic Necessity (0-25 pts)
IF currentStyleCeilingEvidence == STRONG: READINESS_SCORE += 25
ELSE IF currentStyleCeilingEvidence == MODERATE: READINESS_SCORE += 15
ELSE: READINESS_SCORE += 5

// Physical Capacity Match (0-25 pts)
IF physicalToolsForNewStyle == EXCELLENT: READINESS_SCORE += 25
ELSE IF physicalToolsForNewStyle == ADEQUATE: READINESS_SCORE += 15
ELSE: READINESS_SCORE += 5

// Time Budget (0-25 pts)
IF protectionWindowMonths >= 12: READINESS_SCORE += 25
ELSE IF protectionWindowMonths >= 6: READINESS_SCORE += 15
ELSE: READINESS_SCORE += 5

// Psychological Buy-In (0-25 pts)
IF athleteAutonomyScore == HIGH: READINESS_SCORE += 25
ELSE IF athleteAutonomyScore == MODERATE: READINESS_SCORE += 15
ELSE: READINESS_SCORE += 5

IF READINESS_SCORE >= 80: GREEN_LIGHT = TRUE
ELSE IF READINESS_SCORE >= 60: YELLOW_LIGHT = TRUE (Conditional)
ELSE: RED_LIGHT = TRUE

OUTPUT: Readiness Score (0-100), Traffic Light, Specific Conditions if Yellow/Red
```

### Algorithm 6: Late-Career (35+) Adaptation Prescription (ART-173)
**Input:** ASV age > 35 + all pillar data
**Process:**
```
PRESCRIPTION = {
  biomechanics: [
    "Shorten swing: Early prep, compact finish",
    "Serve: Placement + Spin > Velocity. Body serve weapon",
    "Movement: Slide/Glide > Sprint/Stop. Hold baseline",
    "Daily 15-min Prehab: Hip, Thoracic, Ankle, Scapular"
  ],
  neurocognitive: [
    "Video occlusion 3x/week: Anticipation training",
    "Quiet Eye: Extend fixation 200ms",
    "Decision tree: Reduce to 3 core patterns",
    "Cognitive OFF periods: No tennis analysis outside practice"
  ],
  technical: [
    "Weapon audit: Keep only >70% reliability shots",
    "High% architecture: Serve 65%+, Cross-court depth, Heavy spin",
    "Equipment: RA < 62, Tension -4 to -6 lbs, Gut/Poly hybrid"
  ],
  tactical: [
    "Game plan: Make them play MY game",
    "Serve +1 FH dictate, Return +1 deep cross neutralize",
    "Energy mgmt: Tank low-leverage, Surge high-leverage",
    "Target weakness relentlessly"
  ],
  conditioning: [
    "Ratio: 1 High Day : 2 Low Days. NO back-to-back high",
    "S&C: Heavy/Low Volume (3x5@85%), Med Ball/Plyo Low Vol Max Intent",
    "Daily 20-min mobility + Fascial hydration",
    "Recovery Stack: Sleep 9-10h, Protein 2.5-3g/kg, Omega-3 3-4g, Creatine 5g, Collagen 15g+VitC",
    "Modalities budget = Priority: Contrast, Compression, Soft Tissue, Red Light, Sauna",
    "HRV Daily. ACWR < 1.1. Red Flag = Immediate Deload"
  ],
  scheduling: [
    "Surface: Prioritize best (Hard/Grass > Clay for joints)",
    "Draw: Realistic QF/SF path. Avoid grind weeks",
    "Travel: Minimize TZ jumps. Cluster geographically",
    "Recovery window: Min 10 days between finals (ideal 14+)",
    "Block Periodization: Build 6wk/1wk, Peak 3wk/2wk, Maintain 2wk/1wk, Regen 1wk/3wk"
  ]
}

OUTPUT: Personalized Masters Protocol Document
```

## App Interface Specification

### Input Modules
1.  **Daily Morning Check-In (2 min):** Wellness, HRV, Sleep, Pain Map, Motivation
2.  **Weekly Coach Input (10 min):** Technical/Tactical Ratings, Video Tags, Session RPE
3.  **Monthly Testing Battery (60 min):** Physical, Technical, Cognitive, Medical
4.  **Event-Triggered:** Match Data Import (Hawk-Eye/Video), Injury Report, Travel Log

### Output Modules
1.  **Dashboard (Real-Time):** Traffic Light KPIs, Trend Arrows, Red Flags
2.  **Diagnostic Report (On-Demand):** Differential Diagnosis, Confidence %, Protocol Links
3.  **Session Plan Generator (Daily):** Constraints, Volume, Feedback Schedule, Focus Cues
4.  **Weekly/Monthly/Quarterly Reviews:** Trend Analysis, Protocol Adherence, Pivot Recommendations
5.  **Alert System:** Push Notifications for Red Flags (HRV drop, Pain spike, ACWR spike, RTP gate miss)

### Audit Trail & Explainability
*   Every recommendation logs: **Rule ID, ART Reference, Input Values, Confidence %, Timestamp**
*   Coach/Athlete can query: "Why this protocol?" → Shows decision tree path
*   Monthly "Explainability Audit": Random sample of 10 recommendations reviewed for clinical accuracy

## Data Governance & Privacy
*   **Athlete Owns Data:** Export/Delete anytime. Sharing = Explicit Opt-In per recipient.
*   **Medical Data:** Encrypted separate vault. Access = Medical Team only (Coach sees only RTP Stage).
*   **Retention:** Active career + 7 years. Anonymized for research after consent.
*   **Compliance:** GDPR, HIPAA, COPPA (juniors), WADA (supplement/TUE logs).

## Implementation Roadmap
| Phase | Scope | Timeline | Success Criteria |
|-------|-------|----------|------------------|
| **MVP (Phase 1)** | Algorithms 1-3 (Slump, Pressure, RTP) + Daily Check-In + Dashboard | 3 months | 10 beta athletes, >90% diagnostic agreement with expert panel |
| **Phase 2** | Algorithms 4-6 (Uncoachable, Style Change, Masters) + Session Plan Generator | 3 months | 50 athletes, 5 coaches, protocol adherence > 85% |
| **Phase 3** | Full Testing Battery Integration + Video Auto-Tagging + Predictive Analytics | 6 months | 200 athletes, predictive accuracy > 80% for injury/slump |
| **Phase 4** | Multi-Language (EN/VN/ES) + Coach Certification Program + API for Federation Integration | 6 months | 1000+ users, federation adoption |

## Practical Application: "The Stethoscope"
The Diagnostic App is the **Stethoscope of the 5-Pillar System**. It doesn't replace the doctor (Coach/Medic) — it amplifies their hearing. It hears the murmurs (HRV drift, technical regression, cognitive load) before they become crashes. **Use it daily. Trust its differentials. Verify its prescriptions. The athlete's career is the patient.**
