# ProjectSauron / Strider: Air-Gap Espionage Platform - v1.0.0

Initial public release of **CASE-004** in the Michel-DV Threat Case Studies series.

This publication reconstructs ProjectSauron as a long-lived **modular cyber-espionage platform** rather than a single backdoor. The case follows persistence on domain controllers, encrypted Lua-driven plugin orchestration, memory-only execution, multi-protocol C2 and exfiltration, target-specific operational infrastructure, and the specialized removable-media mechanism used to transfer data across air-gapped environments.

## Included

- ProjectSauron / Strider / Remsec terminology and confidence boundaries
- 2011-2016 activity timeline
- victim-scope comparison across Kaspersky and Symantec telemetry
- LSA password-filter persistence and plaintext credential capture
- modified Lua runtime and encrypted VFS architecture
- memory-only modular execution and plugin framework
- lateral deployment through legitimate software-update scripts
- dormant listener / wake-up command model
- internal proxy-node architecture
- DNS, HTTP, SMTP, ICMP, TCP and UDP communications
- DNS metadata exfiltration and milestone reporting
- air-gap bridge and hidden removable-media storage
- `MyTrampoline` / shadow filesystem data-flow reconstruction
- encryption-key and secure-communications targeting
- anti-forensic timestamp tailoring and per-victim customization
- analysis of why traditional IOCs lose value
- representative MITRE ATT&CK mapping
- original trust-boundary reconstruction
- original detection hypotheses and defensive blueprint
- safe Red Team / research emulation notes
- primary-source evidence trail

## Publication status

**v1.0.0 is the final analytical edition of CASE-004.** Future changes should be limited to factual corrections, broken references, or material new evidence.

**Author:** @Michel-DV  
**License:** CC BY-NC-ND 4.0  
**Publication date:** 1 October 2026