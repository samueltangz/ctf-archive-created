const crypto = require('crypto')

const key = crypto.randomBytes(16)

function encryptToken (state) {
  const token = JSON.stringify(state)
  const cipher = crypto.createCipheriv('aes-128-cbc', key, Buffer.alloc(16))
  cipher.setAutoPadding(true)
  const encryptedToken = Buffer.concat([
    Buffer.alloc(16),
    cipher.update(token),
    cipher.final()
  ])
  return encryptedToken.toString('hex')
}

function decryptToken (encryptedTokenHex) {
  const encryptedToken = Buffer.from(encryptedTokenHex, 'hex')
  const cipher = crypto.createDecipheriv('aes-128-cbc', key, encryptedToken.slice(0, 16))
  cipher.setAutoPadding(true)
  const token = Buffer.concat([
    cipher.update(encryptedToken.slice(16)),
    cipher.final()
  ]).toString()
  const state = JSON.parse(token)
  return { token, state }
}

module.exports = {
  encryptToken,
  decryptToken
}
