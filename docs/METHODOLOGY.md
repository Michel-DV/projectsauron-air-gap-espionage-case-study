# Methodology

**CASE-004 - ProjectSauron / Strider: Air-Gap Espionage Platform** is an independent technical reconstruction based on publicly available material.

## Evidence hierarchy

The report prioritizes, in order:

1. first-party technical research from organizations that directly investigated ProjectSauron / Strider activity;
2. primary technical reports and malware analyses published with those investigations;
3. MITRE ATT&CK mappings used to normalize observed behaviors into a common defensive vocabulary;
4. later summaries only when they clarify chronology or terminology without replacing the original evidence.

## Confidence handling

Claims are separated into **confirmed**, **strongly supported**, **analytical interpretation**, and **unknown**. The report does not convert an unresolved entry vector, incomplete victim set, or vendor-specific attribution language into certainty.

Kaspersky's ProjectSauron telemetry and Symantec's Strider / Remsec telemetry are treated as related but independent visibility sets. Victim counts are therefore not added together.

## Terminology

- **ProjectSauron** is used when discussing Kaspersky's reporting and the broader operation/platform described there.
- **Strider** is retained for Symantec/Broadcom's actor label and MITRE ATT&CK group G0041.
- **Remsec** is retained for Symantec/Broadcom's malware label and MITRE ATT&CK software S0125.

These labels overlap in public reporting but are not treated as proof that every artifact observed by one vendor is identical to every artifact observed by another.

## Original analysis layer

The report adds an explicitly analytical layer built from documented behavior:

- trust-boundary reconstruction;
- detection hypotheses;
- defensive choke points;
- behavior-first hunting logic;
- safe Red Team / research emulation notes.

These sections are interpretations by **Michel-DV** and are distinguished from source-reported facts.

## Safety boundary

The publication is designed for threat research, detection engineering, incident-response study, education, and authorized security testing. It does not provide working credential theft, covert exfiltration tooling, operational malware, or instructions for compromising third-party systems.

## Publication integrity

The release PDF is built from version-controlled source, receives explicit document metadata naming **Michel-DV (@Michel-DV)** as author, and is accompanied by a SHA-256 checksum. The GitHub release, repository history, `CITATION.cff`, cover credit, footer credit, and document metadata provide redundant authorship and provenance signals.
