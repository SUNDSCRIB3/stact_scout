# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.2.x   | ✅ |
| < 0.2.0 | ❌ |

## Reporting a Vulnerability

**Do not file a public issue.** Stack-Scout is a technology stack detection tool — security issues could include path traversal, YAML/JSON parsing vulnerabilities, or regex DoS vectors.

Report vulnerabilities privately:
- GitHub: [Report a vulnerability](https://github.com/lukebancroft4-max/stact_scout/security/advisories/new)
- Email: [security contact email placeholder]

We aim to respond within 48 hours and provide a resolution within 7 days.

## Scope

- Code injection via file scanning
- Denial of service via crafted repository structures
- Information disclosure via stack detection output
- Supply chain issues in packaging (PyPI)

## Out of Scope

- Issues in repositories being scanned (not our code)
- Social engineering
- Physical security
