import hashlib

u = b'MOCSCTF{cryp70curr3ncy_4s537s_4r3_s0m3t1m3s_5tol3n_v1a_cl1pb04rd}'

results = []
for i in range(len(u)+1):
    for j in range(i+7, len(u)+1):
        results.append((
            j-i,
            hashlib.sha256(u[i:j]).hexdigest()
        ))

results = sorted(results, reverse=True)

print(results)
