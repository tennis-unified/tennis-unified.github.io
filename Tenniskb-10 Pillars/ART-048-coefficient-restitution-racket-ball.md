---
title: "Art 048: Coefficient of Restitution in Racket-Ball Collisions"
description: "How the coefficient of restitution determines energy transfer efficiency in racket-ball collisions and affects ball speed."
locale: en
pillar: 1
article_id: 048
vault_sources: []
tags: [biomechanics, coefficient-of-restitution, racket-ball-collision, energy-transfer, ball-speed]
status: published
---

# ART:048: Coefficient of Restitution in Racket-Ball Collisions

## Executive Summary
The coefficient of restitution (COR) measures the elasticity of the racket-ball collision, determining how much kinetic energy is retained versus lost to heat and deformation. A higher COR indicates a more elastic collision with less energy loss, resulting in greater ball speed for a given racket speed. Understanding COR explains why certain racket and string combinations produce more power and why the sweet spot produces the highest ball speeds.

## Coefficient of Restitution Definition

### Mathematical Definition
The COR (e) is defined as the ratio of relative separation velocity to relative approach velocity:

e = (v_ball_after - v_racket_after) / (v_racket_before - v_ball_before)

### COR Values in Tennis
- **Racket-ball collision at sweet spot**: 0.75-0.85
- **Racket-ball collision off sweet spot**: 0.60-0.75
- **Ball-court collision**: 0.70-0.80 (depending on surface)

### Energy Retention
The COR determines the percentage of kinetic energy retained in the collision:
- **COR = 0.80**: 64% of kinetic energy retained (0.80²)
- **COR = 0.70**: 49% of kinetic energy retained (0.70²)
- **COR = 0.60**: 36% of kinetic energy retained (0.60²)

## Factors Affecting COR

### Impact Location
- **Sweet spot**: Highest COR (0.75-0.85)
- **Off-sweet spot**: Lower COR (0.60-0.75)
- **Reason**: The sweet spot maximizes the effective mass participating in the collision

### String Tension
- **Higher tension**: Lower COR (less string deformation, more energy lost to ball deformation)
- **Lower tension**: Higher COR (more string deformation, less energy lost to ball deformation)
- **Optimal tension**: Balances COR with control and durability

### String Material**
- **Natural gut**: Highest COR (most elastic)
- **Multifilament**: High COR
- **Polyester**: Lower COR (less elastic)
- **Reason**: Different materials have different elastic properties

### Racket Stiffness
- **Stiffer racket**: Lower COR (less racket deformation, more energy lost to ball deformation)
- **More flexible racket**: Higher COR (more racket deformation, less energy lost to ball deformation)
- **Reason**: The racket and ball share the deformation; more flexible rackets absorb less energy

### Ball Condition
- **New ball**: Higher COR (more elastic)
- **Used ball**: Lower COR (less elastic due to wear)
- **Cold ball**: Lower COR (less elastic at lower temperatures)
- **Warm ball**: Higher COR (more elastic at higher temperatures)

## COR and Ball Speed

### The Relationship
Ball exit speed depends on both racket speed and COR:

v_ball = (v_racket × (1 + e) + v_ball_approach × (e - m_ball/m_racket_effective)) / (1 + m_ball/m_racket_effective)

### Practical Implications
- **10% increase in COR** → approximately 5-10% increase in ball speed
- **Contact at sweet spot vs. off sweet spot** → 10-15% difference in ball speed
- **New ball vs. used ball** → 5-10% difference in ball speed

## Practical Application: "The Bounce Test"
Drop a tennis ball from a fixed height onto your racket and measure how high it bounces. A higher bounce indicates a higher COR and more efficient energy transfer. Test different string tensions, different impact locations, and different ball conditions to understand how they affect the COR. The goal is to maximize the COR at the sweet spot by optimizing your string tension, string material, and ball condition. A higher COR means more ball speed for the same racket speed—pure efficiency.
