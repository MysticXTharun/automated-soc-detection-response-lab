\# Detection 001 - Network Reconnaissance



\## Detection Name



External Network Connection from Controlled Kali Host



\## MITRE ATT\&CK Mapping



Technique: T1046 - Network Service Discovery



Tactic: Discovery



\## Lab Systems



Source:



Kali Linux  

192.168.130.141



Destination:



Windows 11  

192.168.130.130



Monitoring:



Sysmon  

Wazuh Agent  

Wazuh Manager



\## Detection Flow



```text

Kali Linux

&#x20;     |

&#x20;     | Nmap TCP Scan

&#x20;     v

Windows 11

&#x20;     |

&#x20;     v

Sysmon Event ID 3

&#x20;     |

&#x20;     v

Wazuh Agent

&#x20;     |

&#x20;     v

Custom Wazuh Rule 100100

&#x20;     |

&#x20;     v

Level 7 Alert

&#x20;     |

&#x20;     v

MITRE T1046

