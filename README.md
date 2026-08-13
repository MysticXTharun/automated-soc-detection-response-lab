# \# Automated SOC Detection \& Response Lab

# 

# A hands-on Security Operations Center (SOC) lab built to develop practical skills in endpoint telemetry, SIEM monitoring, threat detection, incident investigation, custom detection engineering, and SOC automation.

# 

# > \*\*Status:\*\* Phase 1 complete — Wazuh, Windows 11, and Sysmon telemetry are operational. Kali Linux connectivity and attack simulations are the next phase.

# 

# \## Project Objective

# 

# The goal of this project is to build an end-to-end detection and automated response workflow:

# 

# ```text

# Kali Linux (Simulation)

# &#x20;       |

# &#x20;       v

# Windows 11 Endpoint

# &#x20;       |

# &#x20;     Sysmon

# &#x20;       |

# &#x20;       v

# Wazuh Agent

# &#x20;       |

# &#x20;       v

# Wazuh Manager / SIEM

# &#x20;       |

# &#x20;       v

# Detection \& Investigation

# &#x20;       |

# &#x20;       v

# Custom Rules / Automation

# &#x20;       |

# &#x20;       v

# Automated Response

