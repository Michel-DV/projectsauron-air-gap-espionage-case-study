# References

Primary and high-confidence sources used for **CASE-004 - ProjectSauron / Strider: Air-Gap Espionage Platform**.

1. Kaspersky GReAT — **ProjectSauron: top level cyber-espionage platform covertly extracts encrypted government comms** (8 Aug 2016)  
   https://securelist.com/faq-the-projectsauron-apt/75533/

2. Kaspersky GReAT — **The ProjectSauron APT - Technical Analysis**, v1.02 (9 Aug 2016)  
   https://securelist.com/files/2016/07/The-ProjectSauron-APT_Technical_Analysis_KL.pdf

3. Kaspersky GReAT — **The ProjectSauron APT**, v1.02 (9 Aug 2016)  
   https://securelist.com/files/2016/07/The-ProjectSauron-APT_research_KL.pdf

4. Symantec Security Response / Broadcom — **Strider: Cyberespionage group turns eye of Sauron on targets** (8 Aug 2016)  
   https://community.broadcom.com/symantecenterprise/viewdocument/strider-cyberespionage-group-turns?CommunityKey=1ecf5f55-9545-44d6-b0f4-4e4a7f5f5e68

5. MITRE ATT&CK — **Strider / ProjectSauron, Group G0041**  
   https://attack.mitre.org/groups/G0041/

6. MITRE ATT&CK — **Remsec, Software S0125**  
   https://attack.mitre.org/software/S0125/

7. MITRE ATT&CK — **Modify Authentication Process: Password Filter DLL (T1556.002)**  
   https://attack.mitre.org/techniques/T1556/002/

8. Kaspersky — **IT threat evolution Q3 2016**, ProjectSauron section (3 Nov 2016)  
   https://securelist.com/it-threat-evolution-q3-2016/76482/

## Source handling

- Initial access is kept **unknown** because Kaspersky's public investigation did not establish a confirmed entry vector.
- Kaspersky and Symantec victim telemetry are not combined into one total.
- ProjectSauron's air-gap mechanism is described as a transfer capability using specially prepared removable media, not as proof that USB was the original infection vector.
- Attribution language is preserved at the level used by the source; the report does not independently identify a government sponsor.
- The publication does not reproduce functional malware, credentials, private keys, or operational exfiltration tooling.
