<!--
SPDX-FileCopyrightText: 2026 fyv.ai Ltd.
SPDX-License-Identifier: Apache-2.0
-->

# casl-footer-check

A small checklist tool for commercial email sent from or to Canada.

Canada's anti-spam law (CASL) asks that a commercial electronic message identify the sender, give a mailing address and a way to get in touch, and offer a working unsubscribe mechanism. Senders also have to stop writing to anyone who unsubscribes. This tool checks a draft for those parts, and checks a recipient list against your suppression list.

**It is a checklist, not legal advice.** It cannot tell whether you have consent to write to someone in the first place. Read the official guidance from the CRTC and the Government of Canada's Fight Spam pages, and ask a lawyer about your own situation.

## Use

```bash
# check a draft's footer
python casl_check.py draft --file email.txt --sender-name "Alex Example"

# check recipients against a suppression list (any CSV with an email column)
python casl_check.py recipients --suppression suppressed.csv --to sam@example.com lee@example.com
```

Exit code `0` means the check passed, `1` means something is missing or a recipient is suppressed, so it can sit in a script or a pre-send hook.

## What it looks for

| Part | Accepted examples |
|---|---|
| Sender | the name you pass with `--sender-name` |
| Mailing address | a street line or PO box with a Canadian postal code or a US ZIP code |
| Contact | an email address, a web address or a phone number |
| Unsubscribe | "unsubscribe", "opt out", "se désabonner", "désabonnement", "stop receiving" |

## Tests

```bash
python -m unittest -v
```

Python 3.9+, standard library only. Apache-2.0, see `LICENSE` and `NOTICE`.

## Licence

Copyright 2026 fyv.ai Ltd. Licensed under the [Apache License 2.0](LICENSE). Every file states its own licence in an SPDX header or in `REUSE.toml`, following the [REUSE](https://reuse.software/) specification.

**Our promise:** code released here under Apache-2.0 will not be moved to a more restrictive licence.

This repository is read-only: see [CONTRIBUTING.md](CONTRIBUTING.md). Report security issues privately as described in [SECURITY.md](SECURITY.md). The fyv name is covered by [TRADEMARKS.md](TRADEMARKS.md).
