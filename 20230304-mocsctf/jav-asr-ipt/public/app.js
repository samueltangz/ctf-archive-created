// returns a^n mod p
function modPower(a, n, p) {
  const ZERO = BigInt(0)
  const ONE = BigInt(1)
  const TWO = BigInt(2)

  if (n == ZERO) return ONE
  if (n % TWO == ZERO) return modPower(a * a % p, n / TWO, p)
  return modPower(a, n - ONE, p) * a % p
}

// One round of Miller-Rabin
function witnessLoop(n, r, d, base) {
  const ONE = BigInt(1)

  let x = modPower(base, d, n)
  if (x == ONE || x == n - ONE) return true

  for (let j = 0; j < r - ONE; j++) {
    x = x * x % n
    if (x == n - ONE) return true
  }
  return false
}

// returns true if n is a prime number, false otherwise
// https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
function isPrime(n) {
  const ZERO = BigInt(0)
  const ONE = BigInt(1)
  const TWO = BigInt(2)

  if (n <= ONE) return false

  const bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229].map(BigInt)
  if (bases.includes(n)) return true

  let d = n - ONE
  let r = ZERO

  while (d % TWO == ZERO) {
    d /= TWO
    r += ONE
  }

  for (let i = 0; i < 50; i++) {
    const base = bases[i]
    if (!witnessLoop(n, r, d, base)) return false
  }

  return true
}

function generatePrime(p0) {
  while (true) {
    let p = p0
    for (let i = 0; i < 1022; i++) {
      if (Math.random() < 0.5) {
        p += BigInt(1 << i)
      }
    }
    if (isPrime(p)) return p
  }
}

// Guaranteed that p - q has a large enough difference: p = 0b11xxx...xxx and q = 0b10xxx...xxx
const p = generatePrime(BigInt('2') ** BigInt('1023'))
const q = generatePrime(BigInt('2') ** BigInt('1023') + BigInt('2') ** BigInt('1022'))
const n = p * q

// This was the real flag when creating output.json
const m = BigInt('0x4d4f43534354467b2a2a2a52454441435445442a2a2a7d')

const e = BigInt('0x10001')

const c = modPower(m, e, n)
console.log(JSON.stringify({
  c: c.toString(),
  e: e.toString(),
  n: n.toString()
}))
