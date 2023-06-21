![exsecwarez-combined](https://github.com/exploitsecurityio/ExSecWareZ/assets/131332424/ca3fcd5a-d050-4d9a-8b21-a4419edf19cc)

This toolset incorporates an all round utility envisaged to be used by security researchers in the field. 

UART-Exploiter - Interactive UART passthrough and Baud Scanner used over FTDI (Requires FTDI cable of choice). 

ExploitToolFinder - Scowers the internet for commonly used software tools.

# Description

The UART-Exploiter module, developed in python, is designed to be used by Security Researchers who require quick access to a UART interface using an physical FTDI cable. 

Originally developed as a standlone module, however further development is underway to incorporate this into a much larger Exploit Security Toolkit in the future. 

The module allows for UART passthrough mode and a rudimentary UART baud scan, when used alongside a physical FTDI cable.

The ExploitToolFinder Utility [by exploitsecurity.io] is intended to assist security researchers in their quest to find the right tool for the job. 

Using a menu driven system and OPENAI, this tool trawls the internet for currently published software tools used by the community.

# Prerequisites

- Python3.11
- PyFtdi Library
  - [Installation/Documentation](https://eblot.github.io/pyftdi/installation.html)
- Physical FTDI cable
- OPENAI module and a valid API key. More info can be found [here](https://platform.openai.com/docs/api-reference/introduction)

# Installation

- Using pip to install required libraries.

```
pip3 install -r requirements.txt
```

# Usage

```
./exsecwarez.py

or 

python3 exsecwarez.py
```

# Supported host OSes

- macOS
- Linux
- FreeBSD
- Windows, although not officially supported

# Screenshots

![exsecwarez-screenshot](https://github.com/exploitsecurityio/ExSecWareZ/assets/131332424/0fb34ecb-3043-4fb6-aa29-eff932b187e8)

<p align="left">Fig 1. Main Menu</p>

![exploittoolfinder](https://github.com/exploitsecurityio/ExSecWareZ/assets/131332424/6677364c-7453-4191-aff2-6651596127e4)

<p align="left">Fig 2. Exploit Tool Finder Menu</p>

![uart-exploiter-menu](https://github.com/exploitsecurityio/ExSecWareZ/assets/131332424/371fe8cc-6144-4b3f-9e1a-7c27c3ada889)

<p align="left">Fig 3. UART Exploiter Menu</p>

# Contact

Web: www.exploitsecurity.io

Email: info@exploitsecurity.io

# Copyright
ExSecWareZ is developed by The Security Team @ [exploitsecurity.io]

This program is freely redistributable under the terms of the GNU General Public License as published by the Free Software Foundation.

It is the intention that this software adds usefulness, however it is not currently covered under WARRANTY. 

[GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html).
