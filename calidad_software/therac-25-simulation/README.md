# Therac-25 Software Quality Demonstration

## Historical Background
The Therac-25 was a radiation therapy machine that caused at least 6 accidents between 1985-1987 due to software bugs, resulting in massive radiation overdoses and deaths. This simulation reproduces those bugs to demonstrate the importance of software quality practices.

## The Original Bugs
1. **Race Condition**: Turntable/software desynchronization causing wrong beam mode
2. **Counter Overflow**: 8-bit variable bypassing safety checks after 256 operations
3. **Poor Error Messages**: "MALFUNCTION 54" with no actionable details

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Run Buggy Version (Reproduces Original Accidents)
```bash
python src/simulator/main.py --version=buggy
```

### Run Fixed Version (With Modern Safety Practices)
```bash
python src/simulator/main.py --version=fixed
```

### Run Tests
```bash
# All tests
pytest

# Specific accident scenarios
pytest src/tests/concurrency/test_accidents.py

# Performance tests
pytest src/tests/integration/test_load.py
```

### Docker
```bash
# Start simulation
docker-compose up

# Run specific version
docker-compose run -e VERSION=buggy therac_simulator
```

## What This Demonstrates
- How race conditions cause catastrophic failures in safety-critical systems
- Why proper testing, synchronization, and quality tools are essential
- The human cost of software engineering shortcuts

## Understanding the Results
The simulation will show how modern tools (SonarQube, ThreadSanitizer, comprehensive testing) would have caught these bugs before deployment, potentially saving lives.