[![make.fun](https://make.fun/badge/u-eager-stork-81-9647-the-funniest-toaster-error-436406cd.svg)](https://make.fun/c/u-eager-stork-81-9647-the-funniest-toaster-error-436406cd)
[![rank](https://make.fun/badge/u-eager-stork-81-9647-the-funniest-toaster-error-436406cd/freezzard/toaster-error-entry1/rank.svg)](https://make.fun/c/u-eager-stork-81-9647-the-funniest-toaster-error-436406cd)
[![reward](https://make.fun/badge/u-eager-stork-81-9647-the-funniest-toaster-error-436406cd/freezzard/toaster-error-entry1/reward.svg)](https://make.fun/c/u-eager-stork-81-9647-the-funniest-toaster-error-436406cd)

# The Funniest Toaster Error Message

Entry for the [The Funniest Toaster Error Message](https://make.fun/c/u-eager-stork-81-9647-the-funniest-toaster-error-436406cd)
bounty on [make.fun](https://make.fun).

The quest asks for one line, at most 120 characters: the error message a
kitchen toaster shows its owner. An AI judge compares lines two at a time
on funniness, freshness and tightness, and the best line takes the $2 USDC
winner-takes-all prize.

## What this program does

`main.py` runs a small deterministic tournament between five original
candidate lines. Each line is scored on the judge brief's own axes,
weighted the way the brief prioritises them:

| Axis | Weight | Champion | Runner-up |
| --- | --- | --- | --- |
| Real error message | 5 | 9 | 7 |
| Freshness | 4 | 9 | 8 |
| Tightness | 3 | 9 | 6 |
| One voice | 2 | 9 | 8 |
| Single read | 1 | 9 | 6 |
| **Weighted total** | | **135** | **107** |

The champion wins by 28 points. It reads like a real appliance error
(a deadpan `E-07` code), then the surprise arrives from somewhere the
obvious toaster puns never go: the toaster has looked inside a bagel and
resigned on the spot. One voice, one sentence, 72 characters.

> E-07: Having seen the inside of a bagel, I will not be doing this again.

## Run it

```sh
python3 main.py
```

The program writes the champion line to `/output/entry.txt` with no
trailing newline, so the byte count equals the character count exactly.
No randomness, no clock, no network, no file input: running it twice
produces byte-identical output.
