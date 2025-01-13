# wpa2-python-checker

A simple Python script to demonstrate WPA2 handshake validation using PMKID (Hashcat 22000 format) or 4-way handshake. This tool derives keys, verifies MICs, and attempts to confirm a correct WPA2 passphrase.


## Table of Contents
 - [1. Overview](#1-overview)
 - [2.Features](#2-features)
 - [3.Preparation](#3-preparation)
 - [4.Usage](#4-usage)
 - [5.Example](5-#example)

---
<br/><br/>

## 1. Overview

`wpa2-python-checker` is a minimal Python script that can test whether a provided password matches a WPA2 handshake. It demonstrates the following steps:

1. Deriving the Pairwise Master Key (PMK) via PBKDF2.
2. Generating the Pairwise Transient Key (PTK) using the WPA2 PRF function.
3. Computing the MIC to validate a handshake or verifying PMKID for a PMKID-based attack.

---
<br/><br/>

## 2. Features

- **PMKID Checking** (Hashcat 22000)  
  Verifies if the provided password is correct by calculating the PMKID.

- **MIC Checking** (4-Way Handshake)  
  Uses the PTK to verify the MIC of the handshake data.

- **Minimal Dependencies**  
  Only requires a small set of Python libraries (e.g., `hashlib`, `hmac`, `binascii`).

---
<br/><br/>

## 3. Preparation

1. Clone the repository:
   ```bash
   git clone https://github.com/tomasvanagas/wpa2-python-checker.git
   cd wpa2-python-checker
   ```
   
2. Install the required dependencies:
   ```bash
   pip install pbkdf2
   ```
   
---
<br/><br/>

## 4. Usage

The project consists of a single file named [`checker.py`](checker.py). Simply run it with Python:

```bash
python3 checker.py
```

### Command-Line Arguments (Optional)

You can modify or extend `checker.py` to accept arguments for the password or handshake string. Currently, the script includes a `RunTest` method and a small example in the main body:

```python
password = "vanagas123"
handshake = "WPA*02*4cb5dd3b660d7936940be82911be3b94*7669d957e8ca*a4c6f023fce8*546f6d61736950686f6e65*..."
HC22000_Checker.RunTest(password, handshake)
```

Feel free to replace `password` and `handshake` with your own test values or incorporate command-line arguments as needed.

---
<br/><br/>

## 5. Example

1. Edit [`checker.py`](checker.py), modifying the variables at the end of the file:
   ```python
   password = "your_password_here"
   handshake = "WPA*02*..."
   HC22000_Checker.RunTest(password, handshake)
   ```

2. Run the script:
   ```bash
   python checker.py
   ```
   - If the handshake is correct, it will print the PMK and the SSID hex, followed by the password.
   - If incorrect, it will return `False` without printing.
