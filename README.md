# Healthcare Claims — API Automation Suite

![API Regression](https://github.com/SrinivasaraoThata/claims-api-automation/actions/workflows/api-regression.yml/badge.svg)

API validation layer for the Healthcare Claims Management system. Built with **Python + Requests**.

## Requirement to Endpoint Map

| Requirement | Endpoint | Test Module |
| :--- | :--- | :--- |
| **REQ-LOG-01** | `/services/bank/login/{user}/{pw}` | `tests/test_auth.py` |
| **REQ-CLM-01** | `/services/bank/accounts/{id}` | `tests/test_claim_submission.py` |
| **REQ-CLM-02** | `/services/bank/transfer` | `tests/test_claim_status.py` |
| **REQ-HIS-01** | `/services/bank/accounts/{id}/transactions` | `tests/test_claim_history.py` |
| **REQ-SEC-01** | `/services/bank/accounts/{id}` | `tests/test_security.py` |

## Usage Instructions

### Local Execution

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SrinivasaraoThata/claims-api-automation.git
   cd claims-api-automation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the suite**:
   ```bash
   pytest tests/ -v
   ```

## CI/CD Integration

This suite automatically runs on every push or pull request to the `main` branch via **GitHub Actions**. Results are visible in the **Actions** tab of this repository.
