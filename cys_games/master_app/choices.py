

OPERATING_SYSTEM_CHOICES = (
    ("1", "Windows"),
    ("2", "Linux"),
    ("3", "Kali Linux"),
    ("4", "BackBox"),
    ("5", "Parrot Security Operating System"),
    ("6", "DEFT Linux"),
    ("7", "Samurai Web Testing Framework"),
    ("8", "Network Security Toolkit"),
    ("9", "BlackArch Linux"),
    ("10", "Cyborg Hawk Linux"),
    ("11", "GnackTrack"),
    ("12", "CNodeZero"),
)


OPERATING_SYSTEM_CHOICES_TEXT = {
    "1": "Windows",
    "2": "Linux",
    "3": "Kali Linux",
    "4": "BackBox",
    "5": "Parrot Security Operating System",
    "6": "DEFT Linux",
    "7": "Samurai Web Testing Framework",
    "8": "Network Security Toolkit",
    "9": "BlackArch Linux",
    "10": "Cyborg Hawk Linux",
    "11": "GnackTrack",
    "12": "CNodeZero"
}


SCENARIOS_CATEGORYIES = (
    ("1", "Active Directory Attack"),
    ("2", "OS Exploitation"),
    ("3", "Privilege Escalation on Linux OS"),
    ("4", "Privilege Escalation / RCE-Command Injection / Brute Force"),
)


SCENARIOS_CATEGORYIES_TEXT = {
    "1": "Active Directory Attack",
    "2": "OS Exploitation",
    "3": "Privilege Escalation on Linux OS",
    "4": "Privilege Escalation / RCE-Command Injection / Brute Force"
}


RATING_CHOICES = (
    ("1", 1),
    ("2", 2),
    ("3", 3),
    ("4", 4),
    ("5", 5),
)

CHALLENGE_LEVELS = (
    ("1", "EASY"),
    ("2", "MEDIUM"),
    ("3", "HARD")
)

CHALLENGE_LEVELS_TEXT = {
    "1": "EASY",
    "2": "MEDIUM",
    "3": "HARD"
}


APPROVED_CHOICES = (
    ("1", "Pending"),
    ("2", "Sent Admin for Approval"),
    ("3", "Approved"),
    ("4", "Rejected"),
)


CHALLENGE_SUBMISSION_CHOICES = (
    ("PENDING", "PENDING"),
    ("SUBMITTED", "SUBMITTED"),
)

FLAG_SUBMISSION_CHOICES = (
    ("PENDING", "PENDING"),
    ("SUBMITTED", "SUBMITTED"),
)


USER_TYPE = (
    ("1", "ATTACKER"),
    ("2", "DEFENSER"),
)


COURSE_TYPE = (
    ("1", "ATTACK"),
    ("2", "ATTACH-DEEFENSE"),
)
