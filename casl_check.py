"""casl-footer-check: check a commercial email draft for the identification and unsubscribe
parts Canada's anti-spam law (CASL) asks for, and check recipients against a suppression list.

This is a checklist tool, not legal advice. It looks for four things in the draft:
  1. who is sending (a name and an organisation),
  2. a mailing address,
  3. a way to reach the sender (an email address, a web address or a phone number),
  4. an unsubscribe mechanism.

Usage:
    python casl_check.py draft --file email.txt
    python casl_check.py recipients --suppression suppressed.csv --to a@example.com b@example.com
"""
import argparse
import csv
import pathlib
import re
import sys

POSTAL = re.compile(r"\b[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ -]?\d[ABCEGHJ-NPRSTV-Z]\d\b", re.I)  # Canada
ZIP = re.compile(r"\b[A-Z]{2}\s+\d{5}(-\d{4})?\b")  # United States, "ON 12345" style
STREET = re.compile(r"\b\d{1,6}\s+\w+(\s+\w+)?\s+(st|street|ave|avenue|rd|road|blvd|boulevard|dr|drive|way|lane|ln|cres|court|ct|pl|place)\b\.?", re.I)
PO_BOX = re.compile(r"\b(p\.?\s?o\.?\s?box|case postale)\s*\d+", re.I)
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
WEB = re.compile(r"\b(https?://|www\.)\S+|\b[\w-]+\.(com|ca|io|ai|org|net|ventures)\b", re.I)
PHONE = re.compile(r"(\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}")
UNSUB = re.compile(r"unsubscribe|opt[- ]out|d[ée]sabonn|stop receiving|no longer (wish|want) to (receive|hear)", re.I)


def check_draft(text, sender_name=None):
    """Return a list of the missing parts (empty when the footer looks complete)."""
    missing = []
    if sender_name and sender_name.lower() not in text.lower():
        missing.append(f"the sender's name ({sender_name})")
    if not (POSTAL.search(text) or ZIP.search(text) or PO_BOX.search(text)) or not (STREET.search(text) or PO_BOX.search(text)):
        missing.append("a mailing address (street or PO box, with a postal or ZIP code)")
    if not (EMAIL.search(text) or WEB.search(text) or PHONE.search(text)):
        missing.append("a way to contact the sender (email, web address or phone)")
    if not UNSUB.search(text):
        missing.append("an unsubscribe mechanism (a link or a reply instruction)")
    return missing


def load_suppression(path):
    """Read emails from a CSV; uses a column whose header contains 'email', else the first column."""
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.reader(fh))
    if not rows:
        return set()
    header = [h.lower() for h in rows[0]]
    col = next((i for i, h in enumerate(header) if "email" in h), None)
    body = rows[1:] if col is not None else rows
    col = col or 0
    return {r[col].strip().lower() for r in body if len(r) > col and r[col].strip()}


def check_recipients(recipients, suppressed):
    return [r for r in recipients if r.strip().lower() in suppressed]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("draft")
    d.add_argument("--file", required=True)
    d.add_argument("--sender-name")
    r = sub.add_parser("recipients")
    r.add_argument("--suppression", required=True)
    r.add_argument("--to", nargs="+", required=True)
    args = ap.parse_args(argv)
    if args.cmd == "draft":
        missing = check_draft(pathlib.Path(args.file).read_text(encoding="utf-8"), args.sender_name)
        if missing:
            print("Footer incomplete. Missing:\n- " + "\n- ".join(missing))
            return 1
        print("Footer complete")
        return 0
    blocked = check_recipients(args.to, load_suppression(args.suppression))
    if blocked:
        print("Do not send to (on the suppression list): " + ", ".join(blocked))
        return 1
    print("No recipient is on the suppression list")
    return 0


if __name__ == "__main__":
    sys.exit(main())
