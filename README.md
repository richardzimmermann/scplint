# SCP Lint

This package is used to test, validate and optimize AWS Service Control
Policies.

## Installation

---

## Features

- [Schema Validation](#schema-validation)

### Schema Validation

Validates the JSON schema with a first SCP specific syntax check:

- Mandatory keys exist (based on the [AWS documentation](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_reference_scp-syntax.html))
- Unknown keys are not allowed
- Unknown conditions are not allowed (based on the [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition_operators.html))

---
