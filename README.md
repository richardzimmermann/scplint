# SCP Lint

This package is used to test, validate and optimize AWS Service Control
Policies.

## Installation via GitHub

```
$ pip install git+https://github.com/richardzimmermann/scplint.git
```

---

## Features

- [Schema Validation](#schema-validation)
- [Check Limits](#check-limits)
- [Check Actions](#check-actions)
- [Check Recommendations](#check-recommendations)

### Schema Validation

- Mandatory keys exist (based on the [AWS documentation](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_reference_scp-syntax.html))
- Unknown keys are not allowed
- Unknown conditions are not allowed (based on the [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition_operators.html))
- Keys are unique

### Check Limits

- Return warnings if the policy size is above 90% of the hard limit of AWS (5120 bytes)
- Return errors if the policy size is above 100% of the hard limit of AWS.

### Check Actions

- Count actions which are explicit AWS actions (e.g. `ec2:CreateVpc` is an explicit action without any wildcards)
- Count actions which contains wildcards and also count the amount of actions which are covered by those wildcards.
- Check for actions which are unknown and return warnings (action can contain typo or is a new action which isn't covered by the documentation yet).
- Check for duplicates and return warnings if there are duplicate items in the statements (doesn't compare conditions or resource restrictions yet).

### Check Recommendations

- Returns an recommendation if the actions are unsorted.
- Returns recommendations if you can combine one or more items by adding wildcards.

---

## Usage

```
$ scplint -h
usage: scplint.bat [-h] -i INPUT [-d] [-m] [-r] [-o {json,yaml}] [-v] [--version]

SCPlint to validate and optimize your AWS SCPs

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to the SCP(s), e.g. "path/to/scp.json"
  -d, --detailed        Enable detailed report of your SCP(s)
  -m, --minimize        Minimize the SCP (remove linebreaks and blanks)
  -r, --recursive       Search recursive for json files the given folder.
  -o {json,yaml}, --output {json,yaml}
                        Configure output format of the report
  -v, --verbose         Enable verbose logging.
  --version             Print the current version of scplint
```

Here's an example output:

```
$ scplint -i my_scp.json -m -d

{
    "details": [
        {
            "actions": {
                "actions": 94,
                "actual": 0,
                "error": 0,
                "explicit": 42,
                "info": 0,
                "notactions": 1,
                "warning": 0,
                "wildcard": 670
            },
            "details": {
                "recommendations": [
                    {
                        "code": "O301",
                        "msg": "Actions are unsorted.",
                        "rule": "Action unsorted"
                    },
                    {
                        "code": "O301",
                        "msg": "Actions are unsorted.",
                        "rule": "Action unsorted"
                    },
                    {
                        "code": "O301",
                        "msg": "Actions are unsorted.",
                        "rule": "Action unsorted"
                    }
                ]
            },
            "file": "my_scp.json",
            "percent": "83.7%",
            "size": 4283,
            "size_maximum": 5120,
            "summary": {
                "errors": 0,
                "infos": 0,
                "recommendations": 3,
                "warnings": 0
            }
        }
    ],
    "files": [
        "my_scp.json"
    ],
    "summary": {
        "errors": 0,
        "infos": 0,
        "recommendations": 3,
        "warnings": 0
    }
}
```
