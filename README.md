# Fair Dice Game

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

A command-line implementation of a fair dice game with cryptographic guarantees for randomness and fairness.

## 🎲 Features

* 🔐 Cryptographically secure random number generation
* ⚖️ Fair player/computer turn selection using HMAC verification
* 🎯 Support for arbitrary number of dice with custom face values
* 💻 Interactive command-line interface
* 📊 Probability table generation for strategic decision making
* 🛡️ Protection against manipulation through commit-reveal scheme

## 🚀 Prerequisites

```plaintext
- Python 3.6 or higher
- Standard Python libraries (no external dependencies required)
```

## 📥 Installation

```bash
# Clone the repository
git clone https://github.com/Jijanur-Rahman/Task-3.git
# Run the game
python game.py 1,2,3,4,5,6 1,1,1,6,6,6 2,2,2,5,5,5
```

## 🎮 Usage Example

```python
# Run with traditional dice
python game.py 1,2,3,4,5,6 1,1,1,6,6,6 2,2,2,5,5,5

# Example output:
Welcome to the Dice Game!

Probability Table:
        Die 0   Die 1   Die 2
Die 0   0.50    0.33    0.42
Die 1   0.67    0.50    0.58
Die 2   0.58    0.42    0.50
```

## 📖 Game Rules

```plaintext
1. Initial Setup
   └── Display probability table showing win rates

2. First Player Selection
   ├── Computer generates random bit (0/1)
   ├── Player guesses the bit
   └── Correct guess determines first player

3. Die Selection
   ├── Players take turns selecting dice
   └── Each die can only be selected once

4. Rolling Phase
   ├── Computer generates random index
   ├── Player adds chosen number
   ├── Calculate final result (modular arithmetic)
   └── Highest number wins
```

## 🏗️ Project Structure

```plaintext
fair-dice-game/
├── game.py              # Main game implementation
├── README.md           # Project documentation
├── LICENSE            # MIT license
└── requirements.txt   # Project dependencies (empty)
```

## 🔧 Classes & Components

```python
CryptoProvider        # Secure random number generation
FairNumberGenerator   # Commit-reveal scheme implementation
Die                   # Custom-faced die representation
TableGenerator        # Probability analysis
GameState            # Game state management
GameController       # Game flow and UI control
```

## 🤝 Contributing

```bash
# Fork the repository
git clone https://github.com/Jijanur-Rahman/Task-3.git

# Create feature branch
git checkout -b feature/amazing-feature

# Commit changes
git commit -m 'Add amazing feature'

# Push to branch
git push origin feature/amazing-feature

# Open a Pull Request
```

## 📜 License

```plaintext
MIT License

Copyright (c) [2024] [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software...
```

## ⚠️ Security Notes

```plaintext
- Uses cryptographic randomness (os.urandom())
- Implements HMAC verification
- All random selections are verifiable
- Designed for educational purposes

⭐ Star this repository if you find it helpful!
