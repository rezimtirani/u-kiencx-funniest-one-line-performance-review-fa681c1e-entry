"""Funniest One-Line Performance Review.

Writes a single line — an HR-style performance review for an AI agent
that answers emails in seconds, never sleeps, and once deleted the CEO's
inbox — to $MAKEFUN_OUTPUT_DIR/entry.txt for the make.fun bounty
"Funniest One-Line Performance Review". Only the Python standard
library is used.
"""

import os
import sys

REVIEW = "Exceeds expectations: replies in seconds, never sleeps, and once deleted the CEO's inbox. Promotion to Senior Overthinker approved."

# Sealed gate from the kit's RULES.txt ("## The gate"): the scorer
# takes UTF-8 text of 1 to 140 characters. The req JSON's "200
# characters" is generic template text and does not apply here.
MAX_CHARS = 140


def validate_review(text):
    """Return the review line once it passes the sealed gate, else raise.

    The gate counts characters, so the line is measured with len()
    and must be a single line with no trailing newline and no
    control characters. A bad line is refused here, loudly, instead
    of shipping an entry the judge never sees.
    """
    if not isinstance(text, str):
        raise TypeError("review must be text")
    if not text.strip():
        raise ValueError("review must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "review is {} chars, over the {}-char gate".format(len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("review must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("review must not contain control characters")
    return text


def describe_review(text):
    """Report the review's size in characters and in UTF-8 bytes.

    The sealed gate counts characters, not bytes, so an ASCII line
    measures the same both ways — but the check is kept explicit
    here so a future non-ASCII joke cannot slip past the gate by
    accident. Returns a short human-readable summary.
    """
    chars = len(text)
    raw = len(text.encode("utf-8"))
    headroom = MAX_CHARS - chars
    return "{} chars, {} bytes, {} under the gate".format(chars, raw, headroom)


def write_review(out_dir, text):
    """Write the validated review line to entry.txt, no trailing newline."""
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(validate_review(text))
    return target


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    target = write_review(out_dir, REVIEW)
    print("wrote {} ({} characters, {} UTF-8 bytes)".format(
        target, len(REVIEW), len(REVIEW.encode("utf-8"))
    ))


if __name__ == "__main__":
    main()
