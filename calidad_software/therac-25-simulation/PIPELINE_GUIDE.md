# 🏥 Therac-25 Quality Pipeline Guide

## 🚀 How to Run the Pipeline

### Manual Execution Only
This pipeline is configured to run **ONLY manually** for educational demonstration purposes.

### Steps to Execute:

1. **Go to GitHub Actions tab** in your repository
2. **Click "Therac-25 Quality Pipeline"**
3. **Click "Run workflow"**
4. **Choose options:**
   - ✅ **Run k6 load tests**: Check this to include performance testing
   - **Test groups**: Leave default `unit,integration,concurrency`
5. **Click "Run workflow"** button

## 📊 Pipeline Jobs

### Job 1: 🔧 Build & Setup
- Sets up Python environment
- Installs dependencies
- Verifies simulator imports

### Job 2: 🔒 Security Scan (OWASP)
- Scans for dependency vulnerabilities
- Generates security report
- Would catch security issues in real medical devices

### Job 3: 📊 Static Analysis (SonarCloud)
- **Requires SONAR_TOKEN secret** in repository settings
- Runs Pylint code analysis
- Executes test suite with coverage
- Uploads to SonarCloud for analysis

### Job 4: 🧪 Run Tests (Accident Detection)
- **Unit Tests**: Individual component testing
- **Integration Tests**: Full hospital workflows
- **Concurrency Tests**: Reproduces exact Therac-25 accidents

### Job 5: ⚡ Load Testing (k6)
- **Fast Typing Test**: Simulates experienced operators
- **Concurrent Operations**: Multiple operators simultaneously
- **Counter Overflow**: Extended use triggering bugs

### Job 6: 📋 Generate Quality Report
- Consolidates all results
- Creates executive summary
- Demonstrates how tools would have prevented deaths

## 🔧 Required Secrets

For full functionality, add these secrets in GitHub repository settings:

### SONAR_TOKEN
1. Go to [SonarCloud.io](https://sonarcloud.io)
2. Login with GitHub account
3. Create new project
4. Copy the token
5. Add as secret in GitHub repo: `Settings > Secrets > Actions > New repository secret`

## 📈 Expected Results

### ✅ What Should Pass:
- Build and setup
- Security scan (with warnings)
- Test execution (all 29 tests)
- Load testing scenarios

### ⚠️ What Shows Issues:
- **Static Analysis**: Detects concurrency issues, complexity
- **Tests**: Confirm bugs are reproducible
- **k6**: Shows timing-dependent problems

## 🎯 Educational Value

### The Pipeline Demonstrates:
1. **Race Condition Detection**: Tests catch mode change bugs
2. **Overflow Detection**: Counter tests find safety bypasses
3. **Security Analysis**: OWASP finds dependency issues
4. **Performance Issues**: k6 exposes timing bugs
5. **Code Quality**: SonarCloud identifies complexity problems

### Key Message:
**Every Therac-25 bug would be caught by this pipeline.**

The 6+ patient deaths were **100% preventable** with modern software quality practices.

## 🚨 Common Issues

### SonarCloud Missing
- Pipeline will skip SonarCloud step if SONAR_TOKEN is not configured
- All other steps will still run successfully

### k6 Load Tests
- May show "errors" - this is expected as they detect the bugs
- Focus on the summary reports, not individual test failures

### Test "Failures"
- Some tests are designed to detect bugs, not prevent them
- Look for PASSED status and bug detection messages

## 📊 Interpreting Results

### Successful Run Shows:
- ✅ All tools executed successfully
- ⚠️ Quality issues detected (this is good!)
- 📊 Comprehensive reports generated
- 💀 Bugs that killed patients are found

### Artifacts Generated:
- OWASP security report
- Test coverage reports
- k6 performance results
- Final quality summary

## 🎓 Educational Use

This pipeline serves as a powerful demonstration of:
- Why software quality processes matter
- How modern tools prevent tragedies
- The importance of comprehensive testing
- Real-world application of DevOps practices

Use the results to discuss how proper engineering practices save lives in safety-critical systems.