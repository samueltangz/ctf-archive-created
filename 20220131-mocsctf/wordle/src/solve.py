from pwn import *

import chall


CORRECT   = 0
MISPLACED = 1
INCORRECT = 2


def verdict(word, guess):
    verdict = [INCORRECT for _ in range(5)]

    unmatched_letters = {}

    for k in range(5):
        g, w = guess[k], word[k]

        if g == w:
            verdict[k] = CORRECT
        else:
            unmatched_letters[w] = unmatched_letters.get(w, 0) + 1

    for k in range(5):
        if verdict[k] == CORRECT: continue

        g = guess[k]
        if unmatched_letters.get(g, 0) >= 1:
            verdict[k] = MISPLACED
            unmatched_letters[g] -= 1

    return verdict

    
def guess(id, word):
    r.sendlineafter('🔍 ', word)
    r.recvuntil(f'#{id} | {word} | ')
    return [
        {
            "🟩": CORRECT,
            "🟨": MISPLACED,
            "⬜": INCORRECT,
        }[c] for c in r.recvline().strip().decode()
    ]


def update_candidates(candidates, word, _verdict):
    return [candidate for candidate in candidates if verdict(candidate, word) == _verdict]

def play():
    candidates = chall.words[::4]
    
    for i in range(6):
        word = candidates[0 % len(candidates)]
        v = guess(i+1, word)

        if v == [CORRECT for _ in range(5)]: return chall.words.index(word)
        candidates = update_candidates(candidates, word, v)

        # print(word, v, len(candidates))
    

# =========================================

# The real deal
r = remote('localhost', 50010)

xs = [play() for _ in range(34)]

x33s = [9640705563541584152 + 2**64 * u for u in range(13337) if (9640705563541584152 + 2**64 * u) % 12972 == xs[32] % 12972]
x34s = [9640705563541584152 + 2**64 * u for u in range(13337) if (9640705563541584152 + 2**64 * u) % 12972 == xs[33] % 12972]

x34s = list(set([(271828182845904523536028*x + 314159265358979323846264) % 246024225711064289902592 for x in x33s]) & set(x34s))
assert len(x34s) == 1

x, = x34s

for _ in range(10):
    x = (271828182845904523536028*x + 314159265358979323846264) % 246024225711064289902592
    guess(1, chall.words[x % 12972])

r.interactive()