package main

import (
	"bytes"
	"cmp"
	"crypto/rand"
	"embed"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io/fs"
	"log"
	"net/http"
	"os"
	"sync"

	"github.com/go-webauthn/webauthn/protocol"
	"github.com/go-webauthn/webauthn/webauthn"
	"github.com/google/uuid"
)

//go:embed static
var staticFiles embed.FS

var (
	flagValue string
	wa        *webauthn.WebAuthn

	adminAAGUID = uuid.MustParse("c0ffee00-cafe-babe-dead-beef12345678")
)

type User struct {
	id          []byte
	name        string
	isAdmin     bool
	credentials []webauthn.Credential
}

func (u *User) WebAuthnID() []byte                         { return u.id }
func (u *User) WebAuthnName() string                       { return u.name }
func (u *User) WebAuthnDisplayName() string                { return u.name }
func (u *User) WebAuthnCredentials() []webauthn.Credential { return u.credentials }

type Session struct {
	Username      string
	WebAuthnData  *webauthn.SessionData
	LoggedIn      bool
	AdminVerified bool
}

var (
	mu       sync.RWMutex
	users    = map[string]*User{}
	sessions = map[string]*Session{}
)

func init() {
	flagValue = cmp.Or(os.Getenv("FLAG"), "CPCTF{dummy_flag}")

	var err error
	wa, err = webauthn.New(&webauthn.Config{
		RPDisplayName: "Physical CTF",
		RPID:          cmp.Or(os.Getenv("RP_ID"), "localhost"),
		RPOrigins:     []string{cmp.Or(os.Getenv("RP_ORIGIN"), "http://localhost:8080")},
	})
	if err != nil {
		log.Fatal(err)
	}

	adminID := make([]byte, 32)
	rand.Read(adminID)
	adminCredID := make([]byte, 32)
	rand.Read(adminCredID)
	users["admin"] = &User{
		id: adminID, name: "admin", isAdmin: true,
		credentials: []webauthn.Credential{{ID: adminCredID}},
	}
}

func getSession(r *http.Request) *Session {
	cookie, err := r.Cookie("session")
	if err != nil {
		return nil
	}
	mu.RLock()
	defer mu.RUnlock()
	return sessions[cookie.Value]
}

func setSession(w http.ResponseWriter, s *Session) {
	id := make([]byte, 32)
	rand.Read(id)
	sid := hex.EncodeToString(id)
	mu.Lock()
	sessions[sid] = s
	mu.Unlock()
	http.SetCookie(w, &http.Cookie{
		Name:     "session",
		Value:    sid,
		Path:     "/",
		HttpOnly: true,
		SameSite: http.SameSiteLaxMode,
	})
}

func jsonResponse(w http.ResponseWriter, v interface{}) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(v)
}

func handleRegisterBegin(w http.ResponseWriter, r *http.Request) {
	var req struct {
		Username string `json:"username"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil || req.Username == "" {
		http.Error(w, "invalid request", 400)
		return
	}

	mu.RLock()
	_, exists := users[req.Username]
	mu.RUnlock()
	if exists {
		http.Error(w, "user already exists", 409)
		return
	}

	userID := make([]byte, 32)
	rand.Read(userID)
	user := &User{id: userID, name: req.Username}

	mu.Lock()
	users[req.Username] = user
	mu.Unlock()

	options, sessionData, err := wa.BeginRegistration(user,
		webauthn.WithAuthenticatorSelection(protocol.AuthenticatorSelection{
			ResidentKey:      protocol.ResidentKeyRequirementPreferred,
			UserVerification: protocol.VerificationDiscouraged,
		}),
	)
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}

	setSession(w, &Session{Username: req.Username, WebAuthnData: sessionData})
	jsonResponse(w, options)
}

func handleRegisterFinish(w http.ResponseWriter, r *http.Request) {
	sess := getSession(r)
	if sess == nil || sess.WebAuthnData == nil {
		http.Error(w, "no session", 400)
		return
	}

	mu.RLock()
	user := users[sess.Username]
	mu.RUnlock()
	if user == nil {
		http.Error(w, "user not found", 400)
		return
	}

	credential, err := wa.FinishRegistration(user, *sess.WebAuthnData, r)
	if err != nil {
		http.Error(w, err.Error(), 400)
		return
	}

	mu.Lock()
	user.credentials = append(user.credentials, *credential)
	mu.Unlock()

	sess.WebAuthnData = nil
	sess.LoggedIn = true
	jsonResponse(w, map[string]string{"status": "ok"})
}

func handlePasskeyLoginBegin(w http.ResponseWriter, r *http.Request) {
	options, sessionData, err := wa.BeginDiscoverableLogin(
		webauthn.WithUserVerification(protocol.VerificationDiscouraged),
	)
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}

	setSession(w, &Session{WebAuthnData: sessionData})
	jsonResponse(w, options)
}

func handleSecurityKeyLoginBegin(w http.ResponseWriter, r *http.Request) {
	var req struct {
		Username string `json:"username"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil || req.Username == "" {
		http.Error(w, "invalid request", 400)
		return
	}

	mu.RLock()
	user := users[req.Username]
	mu.RUnlock()
	if user == nil || len(user.credentials) == 0 {
		http.Error(w, "user not found", 404)
		return
	}

	options, sessionData, err := wa.BeginDiscoverableLogin(
		webauthn.WithUserVerification(protocol.VerificationDiscouraged),
	)
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}

	for _, c := range user.credentials {
		options.Response.AllowedCredentials = append(options.Response.AllowedCredentials,
			protocol.CredentialDescriptor{
				Type:         protocol.PublicKeyCredentialType,
				CredentialID: c.ID,
			},
		)
	}

	setSession(w, &Session{Username: req.Username, WebAuthnData: sessionData})
	jsonResponse(w, options)
}

func handleLoginFinish(w http.ResponseWriter, r *http.Request) {
	sess := getSession(r)
	if sess == nil || sess.WebAuthnData == nil {
		http.Error(w, "no session", 400)
		return
	}

	var credOwner webauthn.User

	_, err := wa.FinishDiscoverableLogin(
		func(rawID, userHandle []byte) (webauthn.User, error) {
			mu.RLock()
			defer mu.RUnlock()
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
	if err != nil {
		http.Error(w, err.Error(), 401)
		return
	}

	if sess.Username == "" {
		sess.Username = credOwner.WebAuthnName()
	}

	sess.WebAuthnData = nil
	sess.LoggedIn = true
	jsonResponse(w, map[string]string{"status": "ok"})
}

func handleAdminVerifyBegin(w http.ResponseWriter, r *http.Request) {
	sess := getSession(r)
	if sess == nil || !sess.LoggedIn {
		http.Error(w, "not logged in", 401)
		return
	}

	mu.RLock()
	user := users[sess.Username]
	mu.RUnlock()
	if user == nil || !user.isAdmin {
		http.Error(w, "not admin", 403)
		return
	}

	options, sessionData, err := wa.BeginRegistration(user,
		webauthn.WithConveyancePreference(protocol.PreferDirectAttestation),
		webauthn.WithAuthenticatorSelection(protocol.AuthenticatorSelection{
			UserVerification: protocol.VerificationDiscouraged,
		}),
	)
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}

	sess.WebAuthnData = sessionData
	jsonResponse(w, options)
}

func handleAdminVerifyFinish(w http.ResponseWriter, r *http.Request) {
	sess := getSession(r)
	if sess == nil || !sess.LoggedIn || sess.WebAuthnData == nil {
		http.Error(w, "invalid session", 400)
		return
	}

	mu.RLock()
	user := users[sess.Username]
	mu.RUnlock()
	if user == nil || !user.isAdmin {
		http.Error(w, "not admin", 403)
		return
	}

	credential, err := wa.FinishRegistration(user, *sess.WebAuthnData, r)
	if err != nil {
		http.Error(w, err.Error(), 400)
		return
	}

	if !bytes.Equal(credential.Authenticator.AAGUID, adminAAGUID[:]) {
		http.Error(w, "invalid security key", 403)
		return
	}

	sess.WebAuthnData = nil
	sess.AdminVerified = true
	jsonResponse(w, map[string]interface{}{"status": "ok", "flag": flagValue})
}

func handleMe(w http.ResponseWriter, r *http.Request) {
	sess := getSession(r)
	if sess == nil || !sess.LoggedIn {
		http.Error(w, "not logged in", 401)
		return
	}

	mu.RLock()
	user := users[sess.Username]
	mu.RUnlock()

	jsonResponse(w, map[string]interface{}{
		"username":      sess.Username,
		"isAdmin":       user != nil && user.isAdmin,
		"adminVerified": sess.AdminVerified,
	})
}

func main() {
	staticFS, _ := fs.Sub(staticFiles, "static")
	http.Handle("/", http.FileServer(http.FS(staticFS)))
	http.HandleFunc("/api/register/begin", handleRegisterBegin)
	http.HandleFunc("/api/register/finish", handleRegisterFinish)
	http.HandleFunc("/api/login/passkey/begin", handlePasskeyLoginBegin)
	http.HandleFunc("/api/login/security-key/begin", handleSecurityKeyLoginBegin)
	http.HandleFunc("/api/login/finish", handleLoginFinish)
	http.HandleFunc("/api/admin/verify/begin", handleAdminVerifyBegin)
	http.HandleFunc("/api/admin/verify/finish", handleAdminVerifyFinish)
	http.HandleFunc("/api/me", handleMe)

	log.Fatal(http.ListenAndServe(":8080", nil))
}
