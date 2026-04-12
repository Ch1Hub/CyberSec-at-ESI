# DevSecOps Practical Labs - Vulnerable Web Application

Welcome to the DevSecOps engineering lab. This repository contains a deliberately vulnerable Python (Flask) microservice, complete with outdated dependencies and insecure Docker configurations.

**Do not deploy this application in a production environment.**

## 🎯 Objective

Your mission in Workshops 12 & 13 is to implement a complete **Continuous Integration (CI) Pipeline** using GitLab CI/CD. You will progressively add automated security gates to detect:

1. Hardcoded Secrets (Gitleaks)
2. Insecure Code / SAST (Semgrep)
3. Vulnerable Dependencies / SCA (Safety)
4. Infrastructure as Code flaws (Checkov)
5. Container OS vulnerabilities (Trivy)
6. Dynamic runtime flaws / DAST (OWASP ZAP)

## 🚀 Getting Started

1. **Fork this repository:** Click the "Fork" button in the top-right corner of this page to create your own copy.
2. **Follow the Lab Sheet:** Create a `.gitlab-ci.yml` file at the root of your newly forked repository and follow the step-by-step instructions provided by your instructor.

---

## 🌟 Advanced Challenge: Industry-Standard SAST with SonarQube (SonarCloud)

_For brilliant students looking to master enterprise-grade tools._

In Workshop 12, we utilize `Semgrep` for Static Application Security Testing (SAST) due to its speed and stateless nature. However, the global industry standard for code quality and security is **SonarQube**.

If you want an extra challenge, replace the Semgrep job with **SonarCloud** (the cloud-native, SaaS version of SonarQube).

### Step 1: Provision your SonarCloud Environment

1. Go to [sonarcloud.io](https://sonarcloud.io/).
2. Click **Log in** and authenticate using your **GitLab** account.
3. Once logged in, click the **+ (Plus)** icon in the top right to analyze a new project.
4. Import your forked GitLab repository.
5. SonarCloud will generate a **Token** (e.g., `sqa_8f7d6c5...`). Copy this token securely. It will also provide you with a **Project Key** (e.g., `yourusername_devsecops-app`).

### Step 2: Inject CI/CD Variables in GitLab

SonarQube requires authentication to send the scan results back to the dashboard. You must never hardcode this token in your `.gitlab-ci.yml`.

1. Go to your GitLab repository.
2. Navigate to **Settings > CI/CD > Variables**.
3. Click **Add variable**:
   - **Key:** `SONAR_TOKEN`
   - **Value:** _Paste the token you copied from SonarCloud._
   - Check **"Mask variable"** (Crucial for security).
   - Click Add.
4. Add another variable:
   - **Key:** `SONAR_HOST_URL`
   - **Value:** `https://sonarcloud.io`

### Step 3: Configure the Pipeline Job

Instead of the `sast_semgrep` job provided in the standard lab sheet, insert the official SonarScanner job into your `.gitlab-ci.yml`:

```yaml
sast_sonarqube:
  stage: sast
  image:
    name: sonarsource/sonar-scanner-cli:latest
    entrypoint: [""]
  variables:
    SONAR_USER_HOME: "${CI_PROJECT_DIR}/.sonar" # Defines the location of the analysis task cache
    GIT_DEPTH: "0" # Tells git to fetch all the branches of the project, required by the analysis task
  cache:
    key: "${CI_JOB_NAME}"
    paths:
      - .sonar/cache
  script:
    - sonar-scanner
      -Dsonar.projectKey=YOUR_PROJECT_KEY_HERE
      -Dsonar.organization=YOUR_GITLAB_USERNAME
      -Dsonar.sources=.
      -Dsonar.host.url=$SONAR_HOST_URL
      -Dsonar.login=$SONAR_TOKEN
```
