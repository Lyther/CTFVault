# Physical CTF

Flag:

```text
CPCTF{s!6nA7Ure_v4l1D_BUT_wHo_ar3_YoU?}
```

The challenge pretends that we need to physically steal the admin's hardware key. In reality, the server has two independent WebAuthn logic bugs, and together they give full admin access.

The first bug is in the security-key login flow. `handleSecurityKeyLoginBegin` stores the requested username in the session:

```go
setSession(w, &Session{Username: req.Username, WebAuthnData: sessionData})
```

and `handleLoginFinish` only replaces that username when it is empty:

```go
if sess.Username == "" {
 sess.Username = credOwner.WebAuthnName()
}
```

So if we begin login as `admin`, a successful assertion keeps `sess.Username == "admin"` even if the credential actually belongs to someone else.

The second bug is how the credential owner is resolved during login:

```go
_, err := wa.FinishDiscoverableLogin(
 func(rawID, userHandle []byte) (webauthn.User, error) {
  for _, u := range users {
   for _, c := range u.credentials {
    if bytes.Equal(c.ID, rawID) {
     credOwner = u
     return u, nil
    }
   }
  }
  return nil, fmt.Errorf("credential not found")
 },
 *sess.WebAuthnData,
 r,
)
```

This callback ignores `userHandle` completely and searches only by `rawID`. Registration also never checks for duplicate credential ids, so we can register our own credential using the exact same credential id as admin's fake credential.

That gives the login exploit:

1. Call `/api/login/security-key/begin` with `{"username":"admin"}`.
2. Read admin's credential id from `publicKey.allowCredentials[0].id`.
3. Register a new attacker account, but forge the WebAuthn registration so its credential id is that leaked admin credential id.
4. Start security-key login as `admin` and submit assertions signed by our key.
5. Go's map iteration order is randomized, so the `for _, u := range users` search eventually finds our attacker-owned duplicate credential before the seeded admin one.
6. The assertion validates with our public key, but the session username stays `"admin"`.

After that, `/api/me` shows:

```json
{"adminVerified":false,"isAdmin":true,"username":"admin"}
```

There is one more bug in the admin-only verification step. The server tries to check whether the authenticator is the special admin key:

```go
if !bytes.Equal(credential.Authenticator.AAGUID, adminAAGUID[:]) {
 http.Error(w, "invalid security key", 403)
 return
}
```

But `handleAdminVerifyBegin` only sets a preference for direct attestation:

```go
webauthn.WithConveyancePreference(protocol.PreferDirectAttestation)
```

and `FinishRegistration` still accepts `fmt:"none"`. That means the AAGUID is taken from attacker-controlled `authData` with no authenticated attestation chain behind it. We can simply forge a registration response whose AAGUID is:

```text
c0ffee00-cafe-babe-dead-beef12345678
```

Then `/api/admin/verify/finish` returns the flag.

So the final exploit is:

1. Leak admin's credential id.
2. Register a duplicate credential id under our own account.
3. Repeatedly log in as `admin` until the server resolves that duplicated id to our account.
4. Forge an admin verification registration with the admin AAGUID.
5. Read the flag.

`solve.py` automates the full chain.
