# Automated Incident Timeline Reconstruction

**Incident ID:** INC-20260813-051403-8E6ED3A1
**Case ID:** CASE-20260814-035612-R100111
**Rule ID:** 100111
**Events:** 5
**Timeline Start:** 2026-08-13T05:14:03.915000+00:00
**Timeline End:** 2026-08-14T05:39:33.504577+00:00
**Total Duration:** 1465.49 minutes

## Investigation Timeline

| # | Timestamp (UTC) | Event | Source | Elapsed (min) | Gap (min) |
|---:|---|---|---|---:|---:|
| 1 | 2026-08-13T05:14:03.915000+00:00 | SECURITY_ALERT | Wazuh / Detection 005 | 0.0 | 0.0 |
| 2 | 2026-08-14T03:39:46.338412+00:00 | TRIAGE_COMPLETED | Detection 005 | 1345.71 | 1345.71 |
| 3 | 2026-08-14T03:56:12.686158+00:00 | CASE_CREATED | Detection 006 | 1362.15 | 16.44 |
| 4 | 2026-08-14T04:10:24.850571+00:00 | NOTIFICATION_GENERATED | Detection 007 | 1376.35 | 14.2 |
| 5 | 2026-08-14T05:39:33.504577+00:00 | RISK_ASSESSMENT | Detection 011 | 1465.49 | 89.14 |

## Event Details

### 1. SECURITY_ALERT

- Timestamp: `2026-08-13T05:14:03.915000+00:00`
- Source: Wazuh / Detection 005
- Elapsed from initial event: 0.0 minutes
- Gap from previous event: 0.0 minutes
- Description: Wazuh Rule 100111 detected activity from 192.168.130.141 to 192.168.130.130:445

### 2. TRIAGE_COMPLETED

- Timestamp: `2026-08-14T03:39:46.338412+00:00`
- Source: Detection 005
- Elapsed from initial event: 1345.71 minutes
- Gap from previous event: 1345.71 minutes
- Description: Automated alert triage completed

### 3. CASE_CREATED

- Timestamp: `2026-08-14T03:56:12.686158+00:00`
- Source: Detection 006
- Elapsed from initial event: 1362.15 minutes
- Gap from previous event: 16.44 minutes
- Description: SOC case CASE-20260814-035612-R100111 created with priority P3

### 4. NOTIFICATION_GENERATED

- Timestamp: `2026-08-14T04:10:24.850571+00:00`
- Source: Detection 007
- Elapsed from initial event: 1376.35 minutes
- Gap from previous event: 14.2 minutes
- Description: SOC notification generated with escalation level No Immediate Escalation

### 5. RISK_ASSESSMENT

- Timestamp: `2026-08-14T05:39:33.504577+00:00`
- Source: Detection 011
- Elapsed from initial event: 1465.49 minutes
- Gap from previous event: 89.14 minutes
- Description: Incident risk evaluated as MEDIUM with score 40/100
