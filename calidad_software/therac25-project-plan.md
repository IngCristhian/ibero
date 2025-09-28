# Therac-25 Software Quality Simulation Project

## Project Overview
This project simulates the Therac-25 radiation therapy machine's software failures to demonstrate the importance of software quality practices. We'll create a containerized simulation that reproduces the original bugs, then show how modern quality tools would have prevented these tragic accidents.

## Historical Context
The Therac-25 was a radiation therapy machine that caused at least 6 accidents between 1985-1987 due to software bugs, resulting in massive radiation overdoses. The main issues were:
- Race conditions in concurrent operations
- 8-bit counter overflow bypassing safety checks
- Poor error messages (MALFUNCTION 54)
- Lack of hardware interlocks
- Code reused from previous models without proper review

## Project Structure
```
therac-25-simulation/
├── docker/
│   ├── Dockerfile.simulator
│   └── docker-compose.yml
├── src/
│   ├── simulator/
│   │   ├── main.py (or main.js/main.go)
│   │   ├── control_module.py
│   │   ├── operator_interface.py
│   │   ├── hardware_simulator.py
│   │   ├── dosage_system.py
│   │   └── event_logger.py
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── concurrency/
│   └── config/
│       └── settings.yml
├── .github/
│   └── workflows/
│       └── quality-pipeline.yml
├── quality/
│   ├── sonar-project.properties
│   ├── owasp-suppression.xml
│   └── k6-scenarios/
│       ├── operator-fast-typing.js
│       ├── concurrent-operations.js
│       └── stress-overflow.js
├── requirements.txt (or package.json)
└── README.md
```

## Implementation Phases

### PHASE 1: Build the Therac-25 Simulator

#### Core Components to Implement

**1. Control Module (`control_module.py`)**
```
Purpose: Manages machine state and coordinates all components
Key Features:
- State machine with modes: STARTUP, READY, SETUP, BEAM_READY, FIRING, ERROR
- Shared state variables (THIS IS WHERE BUGS WILL BE)
- No proper mutex/locks in buggy version
- 8-bit counter for setup verification (will overflow after 255)
```

**2. Operator Interface (`operator_interface.py`)**
```
Purpose: Simulates the VT-100 terminal interface
Key Features:
- Command input: SET_MODE, SET_DOSE, SET_POSITION, FIRE, EDIT
- Fast input capability (no forced delays in buggy version)
- Cryptic error messages in buggy version
- Better feedback in fixed version
```

**3. Hardware Simulator (`hardware_simulator.py`)**
```
Purpose: Simulates physical components
Components to simulate:
- Turntable (rotates between electron and X-ray positions)
- Collimator (shapes the beam)
- Beam emitter (simulated - just logs)
- Position sensors (can be out of sync in buggy version)
```

**4. Dosage System (`dosage_system.py`)**
```
Purpose: Calculates and applies radiation dose
Key Features:
- Dose calculation based on mode (electron vs X-ray)
- In buggy version: Can fire with wrong settings
- In fixed version: Multiple verification steps
```

**5. Event Logger (`event_logger.py`)**
```
Purpose: Records all operations for analysis
Logs:
- Timestamp, operation, state before, state after
- Error conditions and malfunctions
- Used to demonstrate the accident scenarios
```

#### Bugs to Implement in "Buggy Version"

**Bug 1: Race Condition in Mode Change**
```
Scenario: Operator changes from X-ray (X) to Electron (E) mode quickly
Problem: Turntable starts moving but software doesn't wait for completion
Result: High-power electron beam without proper shielding
Implementation: No synchronization between hardware_simulator and control_module
```

**Bug 2: Counter Overflow (Class3 Variable)**
```
Scenario: Setup procedure done 256+ times
Problem: 8-bit counter overflows to 0, bypassing safety checks
Result: System thinks it's properly set up when it's not
Implementation: Use uint8 counter, increment on each setup
```

**Bug 3: Edit Race Condition**
```
Scenario: Operator uses up-arrow to edit while system is setting up
Problem: Partial state update without proper verification
Result: Inconsistent machine state
Implementation: Allow editing during state transitions without locks
```

### PHASE 2: Docker Configuration

**Main Simulator Container (`docker/Dockerfile.simulator`)**
```
Base image: python:3.9-slim (or node:16-alpine if using JavaScript)
Include:
- Application code
- Logging configuration
- Web server for status dashboard (port 8080)
- Health check endpoint
```

**Docker Compose Setup (`docker/docker-compose.yml`)**
```
Services:
- therac_simulator: Main application
- Optional: monitoring dashboard
Networks: 
- therac_network (bridge)
Volumes:
- ./logs:/app/logs
- ./reports:/app/reports
Environment variables:
- VERSION=buggy or VERSION=fixed
- DEBUG_MODE=true/false
- SIMULATION_SPEED=1x/10x/100x
```

### PHASE 3: Quality Tools Configuration

#### 3.1 SonarQube Configuration
**File: `quality/sonar-project.properties`**
```
Key configurations:
- sonar.projectKey=therac-25-simulator
- sonar.sources=src/simulator
- sonar.tests=src/tests
- sonar.python.coverage.reportPaths=coverage.xml
- Focus rules: Concurrency issues, complexity, error handling
```

**What SonarQube will detect:**
- Missing synchronization in control_module
- Cyclomatic complexity > 10 in state management
- Duplicate code between modules
- Missing error handling
- Code smells in shared state access

#### 3.2 ThreadSanitizer Setup
**Implementation approach:**
- If using Python: Use `threading` module with race condition detection
- If using C/C++: Compile with `-fsanitize=thread` flag
- If using Go: Built-in race detector with `-race` flag
- If using JavaScript/Node: Use worker_threads with detection tools

**What it will find:**
- Data races in shared state variables
- Missing mutex locks
- Concurrent access to hardware state
- Read/write conflicts in control module

#### 3.3 Test Suite Structure
**Test Categories:**

**Unit Tests (`src/tests/unit/`)**
- Test each module in isolation
- Mock dependencies
- Verify individual functions
- Edge cases (counter at 254, 255, 0)

**Integration Tests (`src/tests/integration/`)**
- Full operation sequences
- Mode changes with timing
- Error propagation
- State consistency

**Concurrency Tests (`src/tests/concurrency/`)**
- Parallel operations
- Race condition reproduction
- The 3 historical accident scenarios
- Timing-dependent bugs

**Specific Test Cases to Include:**
```
test_accident_scenario_1: X-to-E mode change during setup
test_accident_scenario_2: Edit during beam preparation  
test_accident_scenario_3: Counter overflow after 256 setups
test_race_condition_detection: Concurrent state modifications
test_synchronization_fix: Verify mutex implementation works
```

#### 3.4 OWASP Dependency Check
**Configuration file: `quality/owasp-suppression.xml`**
```
What to check:
- All third-party dependencies
- Simulate "inherited code" vulnerabilities
- Check for outdated libraries
- Security vulnerabilities in dependencies
```

#### 3.5 k6 Load Testing Scenarios

**Scenario 1: Fast Operator (`k6-scenarios/operator-fast-typing.js`)**
```
Simulates: Experienced operator typing quickly
Operations: 
- Rapid mode changes (< 1 second between commands)
- Quick edit sequences
- No pause between setup and fire
Duration: 5 minutes
Virtual Users: 1
Success Criteria: System maintains state consistency
```

**Scenario 2: Concurrent Operations (`k6-scenarios/concurrent-operations.js`)**
```
Simulates: Multiple operators or system processes
Operations:
- Parallel state reads/writes
- Simultaneous mode changes
- Concurrent dose calculations
Duration: 10 minutes  
Virtual Users: 5-10
Success Criteria: No race conditions detected
```

**Scenario 3: Overflow Test (`k6-scenarios/stress-overflow.js`)**
```
Simulates: Extended use causing counter overflow
Operations:
- 300+ setup procedures
- Verify behavior at counts: 254, 255, 256, 257
- Check all safety verifications
Duration: 15 minutes
Virtual Users: 1
Success Criteria: Safety checks never bypassed
```

### PHASE 4: GitHub Actions Pipeline

**File: `.github/workflows/quality-pipeline.yml`**

```yaml
name: Therac-25 Quality Pipeline

Workflow Structure:
1. Triggers: push to main, pull_request, manual dispatch
2. Matrix strategy: Test both buggy and fixed versions

Jobs to implement:

job: build-and-setup
  - Checkout code
  - Setup Python/Node environment
  - Install dependencies
  - Build Docker image
  - Upload image to registry

job: security-scan
  - Run OWASP Dependency Check
  - Generate vulnerability report
  - Fail if critical vulnerabilities found
  - Upload security report as artifact

job: static-analysis
  - Setup SonarQube scanner
  - Run analysis on source code
  - Check quality gates
  - Generate coverage report
  - Upload to SonarCloud

job: run-tests
  - Run unit tests with coverage
  - Run integration tests
  - Run concurrency tests with ThreadSanitizer
  - Generate JUnit XML reports
  - Fail if any test fails in "fixed" version

job: load-testing
  - Start Docker container
  - Run k6 operator fast typing scenario
  - Run k6 concurrent operations scenario  
  - Run k6 overflow scenario
  - Generate performance reports
  - Check performance thresholds

job: generate-reports
  - Consolidate all test results
  - Create HTML dashboard
  - Compare buggy vs fixed metrics
  - Upload as GitHub Pages artifact
```

### PHASE 5: Demonstration Scenarios

#### Accident Reproductions to Implement

**Scenario 1: Turntable Position Error**
```
Steps:
1. Set mode to X-ray (25 MeV)
2. Enter patient data
3. Quickly change to Electron mode (use up-arrow, edit, E, Enter)
4. Press SET immediately
5. System fires electron beam at X-ray power level

Expected in buggy version: Massive overdose (no turntable sync)
Expected in fixed version: System waits for hardware confirmation
```

**Scenario 2: Data Entry Race Condition**
```
Steps:
1. Start entering prescription
2. Use cursor to edit field
3. Quickly complete entry
4. Press B (beam on) within 8 seconds

Expected in buggy version: Partial data used for dosage
Expected in fixed version: Full validation before beam activation
```

**Scenario 3: Counter Overflow**
```
Steps:
1. Run 256 setup procedures
2. On the 257th setup, enter incorrect data
3. System should catch the error
4. But counter has overflowed to 0

Expected in buggy version: Safety check bypassed
Expected in fixed version: 32-bit counter, no overflow
```

## Fixed Version Improvements

The corrected version should implement:

1. **Proper Synchronization**
   - Mutex locks on all shared state
   - Thread-safe operations
   - Atomic state transitions

2. **Hardware Interlocks**
   - Wait for hardware confirmation
   - Timeout on all operations
   - Position verification before firing

3. **Better Error Handling**
   - Descriptive error messages
   - Proper error propagation
   - Fail-safe defaults

4. **Robust Data Types**
   - 32-bit counters (no overflow)
   - Enum for states (not integers)
   - Immutable configuration objects

5. **Verification Steps**
   - Multiple safety checks
   - Mandatory delays between critical operations
   - Operator confirmation for dose > threshold

## README.md Content Structure

The README should include:

```markdown
# Therac-25 Software Quality Demonstration

## Historical Background
Brief description of the Therac-25 accidents and their impact on software engineering.

## What This Simulation Demonstrates
- How race conditions cause catastrophic failures
- Why proper testing and quality tools are essential
- The importance of software engineering practices in safety-critical systems

## The Original Bugs
1. **Race Condition**: Turntable/software desynchronization
2. **Counter Overflow**: 8-bit variable bypassing safety checks  
3. **Poor Error Messages**: "MALFUNCTION 54" with no details

## How to Run

### Quick Start
`docker-compose up`

### Run Buggy Version
`docker-compose run -e VERSION=buggy therac_simulator`

### Run Fixed Version  
`docker-compose run -e VERSION=fixed therac_simulator`

### Execute Quality Pipeline
`gh workflow run quality-pipeline.yml`

## Understanding the Results

### Quality Metrics
- **Before**: X critical bugs, Y vulnerabilities, Z% test failure
- **After**: 0 critical bugs, all tests passing, proper synchronization

### Tool Reports
- SonarQube: See code quality issues
- ThreadSanitizer: View race conditions
- Test Results: Check accident scenario outcomes
- k6: Performance under stress
- OWASP: Dependency vulnerabilities

## Lessons Learned
1. Formal testing would have caught these bugs
2. Code review and static analysis are essential
3. Never assume hardware and software are in sync
4. Clear error messages save lives
5. Legacy code requires thorough review
```

## Development Steps for Claude Code

When implementing with Claude Code, follow this sequence:

1. **Start with project structure**: Create all directories and empty files
2. **Implement buggy simulator first**: Focus on reproducing the original bugs
3. **Create test suite**: Write tests that detect the bugs
4. **Set up Docker environment**: Containerize the application
5. **Configure quality tools**: One at a time, verify each works
6. **Build GitHub Actions pipeline**: Test locally with `act` first
7. **Implement fixed version**: Apply all safety improvements
8. **Generate comparison reports**: Show before/after metrics
9. **Document everything**: Focus on educational value

## Key Implementation Notes

- **Language Choice**: Python recommended for simplicity, but Go or Node.js also work well
- **Concurrency**: Must use real threads/processes to demonstrate race conditions
- **Timing**: Add configurable delays to control simulation speed
- **Logging**: Extensive logging to show exactly what goes wrong
- **Visualization**: Consider a simple web UI to show machine state in real-time

This simulation will powerfully demonstrate how modern software quality practices could have prevented tragic loss of life.