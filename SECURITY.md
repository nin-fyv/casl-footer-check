<!--
SPDX-FileCopyrightText: 2026 fyv.ai Ltd.
SPDX-License-Identifier: Apache-2.0
-->

# Security policy

## Reporting a vulnerability

Please report security issues privately by email to **admin@fyv.ventures**. Do not open a public issue or pull request, as this repository does not accept them.

Include what you found, the version or commit, steps to reproduce, and the impact you expect. If you want credit, say how you would like to be named.

## What to expect

- We acknowledge reports within **5 business days**.
- We tell you whether we accept the report and, if we do, roughly when a fix will be released.
- We credit reporters in the release notes unless you ask us not to.
- We do not run a paid bug bounty.

## Supported versions

Only the latest tagged release receives security fixes.

## Checking a release

Every release is published with an SBOM, checksums and a GitHub build attestation signed through Sigstore. To confirm that a downloaded archive was built from this repository:

```bash
gh attestation verify casl-footer-check-<version>.tar.gz --repo nin-fyv/casl-footer-check
```
