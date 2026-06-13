package main

import (
	"bufio"
	"bytes"
	"crypto/aes"
	"crypto/hmac"
	"crypto/sha256"
	"crypto/sha512"
	"encoding/binary"
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"sync"
	"sync/atomic"
	"time"
)

var (
	signature      = []byte{0x03, 0xd9, 0xa2, 0x9a, 0x67, 0xfb, 0x4b, 0xb5}
	outerCipherAES = []byte{0x31, 0xc1, 0xf2, 0xe6, 0xbf, 0x71, 0x43, 0x50, 0xbe, 0x58, 0x05, 0x21, 0x6a, 0xfc, 0x5a, 0xff}
	kdfAES         = []byte{0xc9, 0xd9, 0xf3, 0x9a, 0x62, 0x8a, 0x44, 0x60, 0xbf, 0x74, 0x0d, 0x08, 0xc1, 0x8a, 0x4f, 0xea}
)

type headerInfo struct {
	header     []byte
	headerHMAC []byte
	masterSeed []byte
	kdfSeed    []byte
	kdfRounds  uint64
}

func parseVariantDictionary(data []byte) (map[string][]byte, error) {
	if len(data) < 2 {
		return nil, fmt.Errorf("variant dictionary too short")
	}

	values := make(map[string][]byte)
	index := 2

	for index < len(data) {
		valueType := data[index]
		index++

		if valueType == 0 {
			return values, nil
		}

		if index+4 > len(data) {
			return nil, fmt.Errorf("truncated variant name length")
		}
		nameLen := int(binary.LittleEndian.Uint32(data[index : index+4]))
		index += 4

		if index+nameLen > len(data) {
			return nil, fmt.Errorf("truncated variant name")
		}
		name := string(data[index : index+nameLen])
		index += nameLen

		if index+4 > len(data) {
			return nil, fmt.Errorf("truncated variant value length")
		}
		valueLen := int(binary.LittleEndian.Uint32(data[index : index+4]))
		index += 4

		if index+valueLen > len(data) {
			return nil, fmt.Errorf("truncated variant value")
		}
		values[name] = data[index : index+valueLen]
		index += valueLen
	}

	return nil, fmt.Errorf("variant dictionary missing terminator")
}

func parseHeader(data []byte) (*headerInfo, error) {
	if len(data) < 12 {
		return nil, fmt.Errorf("file too short")
	}

	if !bytes.Equal(data[:8], signature) {
		return nil, fmt.Errorf("unexpected signature")
	}

	if binary.LittleEndian.Uint16(data[10:12]) != 4 {
		return nil, fmt.Errorf("expected KDBX4")
	}

	fields := make(map[byte][][]byte)
	index := 12

	for {
		if index+5 > len(data) {
			return nil, fmt.Errorf("truncated header field")
		}

		fieldID := data[index]
		fieldLen := int(binary.LittleEndian.Uint32(data[index+1 : index+5]))
		index += 5

		if index+fieldLen > len(data) {
			return nil, fmt.Errorf("truncated header value")
		}

		value := data[index : index+fieldLen]
		index += fieldLen
		fields[fieldID] = append(fields[fieldID], value)

		if fieldID == 0 {
			break
		}
	}

	if index+64 > len(data) {
		return nil, fmt.Errorf("missing header hashes")
	}

	header := data[:index]
	storedSHA256 := data[index : index+32]
	index += 32
	headerHMAC := data[index : index+32]

	calculatedSHA256 := sha256.Sum256(header)
	if !bytes.Equal(calculatedSHA256[:], storedSHA256) {
		return nil, fmt.Errorf("header SHA256 mismatch")
	}

	cipherFields := fields[2]
	if len(cipherFields) == 0 || !bytes.Equal(cipherFields[0], outerCipherAES) {
		return nil, fmt.Errorf("unsupported outer cipher")
	}

	masterSeedField := fields[4]
	kdfField := fields[11]
	if len(masterSeedField) == 0 || len(kdfField) == 0 {
		return nil, fmt.Errorf("missing KDF fields")
	}

	kdfParams, err := parseVariantDictionary(kdfField[0])
	if err != nil {
		return nil, err
	}

	kdfUUID, ok := kdfParams["$UUID"]
	if !ok || !bytes.Equal(kdfUUID, kdfAES) {
		return nil, fmt.Errorf("unsupported KDF UUID")
	}

	kdfSeed, ok := kdfParams["S"]
	if !ok {
		return nil, fmt.Errorf("missing KDF seed")
	}

	roundsRaw, ok := kdfParams["R"]
	if !ok || len(roundsRaw) != 8 {
		return nil, fmt.Errorf("missing KDF rounds")
	}

	return &headerInfo{
		header:     append([]byte(nil), header...),
		headerHMAC: append([]byte(nil), headerHMAC...),
		masterSeed: append([]byte(nil), masterSeedField[0]...),
		kdfSeed:    append([]byte(nil), kdfSeed...),
		kdfRounds:  binary.LittleEndian.Uint64(roundsRaw),
	}, nil
}

func deriveHMACKey(index uint64, hmacBaseKey []byte) []byte {
	buf := make([]byte, 8+len(hmacBaseKey))
	binary.LittleEndian.PutUint64(buf[:8], index)
	copy(buf[8:], hmacBaseKey)
	sum := sha512.Sum512(buf)
	return sum[:]
}

func validatePassword(password string, info *headerInfo) bool {
	inner := sha256.Sum256([]byte(password))
	composite := sha256.Sum256(inner[:])

	block, err := aes.NewCipher(info.kdfSeed)
	if err != nil {
		return false
	}

	transformed := make([]byte, 32)
	copy(transformed, composite[:])

	for range info.kdfRounds {
		block.Encrypt(transformed[:16], transformed[:16])
		block.Encrypt(transformed[16:], transformed[16:])
	}

	transformedHash := sha256.Sum256(transformed)

	masterInput := make([]byte, 0, len(info.masterSeed)+len(transformedHash))
	masterInput = append(masterInput, info.masterSeed...)
	masterInput = append(masterInput, transformedHash[:]...)

	hmacBaseInput := make([]byte, 0, len(masterInput)+1)
	hmacBaseInput = append(hmacBaseInput, masterInput...)
	hmacBaseInput = append(hmacBaseInput, 0x01)
	hmacBaseKey := sha512.Sum512(hmacBaseInput)

	headerKey := deriveHMACKey(^uint64(0), hmacBaseKey[:])
	mac := hmac.New(sha256.New, headerKey)
	mac.Write(info.header)

	return hmac.Equal(mac.Sum(nil), info.headerHMAC)
}

func worker(info *headerInfo, jobs <-chan string, found chan<- string, done <-chan struct{}, tested *uint64) {
	for {
		select {
		case <-done:
			return
		case password, ok := <-jobs:
			if !ok {
				return
			}

			atomic.AddUint64(tested, 1)
			if validatePassword(password, info) {
				select {
				case found <- password:
				default:
				}
				return
			}
		}
	}
}

func defaultDatabasePath() string {
	exe, err := os.Executable()
	if err != nil {
		return ""
	}

	base := filepath.Dir(exe)
	return filepath.Join(base, "..", "files", "Database.kdbx")
}

func main() {
	var (
		dbPath    string
		wordlist  string
		single    string
		workers   int
		progress  time.Duration
		showStats bool
	)

	flag.StringVar(&dbPath, "db", defaultDatabasePath(), "path to Database.kdbx")
	flag.StringVar(&wordlist, "wordlist", "", "candidate wordlist file")
	flag.StringVar(&single, "password", "", "single password candidate")
	flag.IntVar(&workers, "workers", runtime.NumCPU(), "worker count")
	flag.DurationVar(&progress, "progress", 5*time.Second, "progress interval")
	flag.BoolVar(&showStats, "stats", true, "print periodic progress to stderr")
	flag.Parse()

	if (wordlist == "") == (single == "") {
		log.Fatal("use exactly one of -wordlist or -password")
	}

	data, err := os.ReadFile(dbPath)
	if err != nil {
		log.Fatalf("read database: %v", err)
	}

	info, err := parseHeader(data)
	if err != nil {
		log.Fatalf("parse header: %v", err)
	}

	if single != "" {
		if validatePassword(single, info) {
			fmt.Println(single)
			return
		}
		os.Exit(1)
	}

	file, err := os.Open(wordlist)
	if err != nil {
		log.Fatalf("open wordlist: %v", err)
	}
	defer file.Close()

	jobs := make(chan string, workers*4)
	found := make(chan string, 1)
	done := make(chan struct{})

	var tested uint64
	var once sync.Once
	var workerWG sync.WaitGroup

	for range workers {
		workerWG.Add(1)
		go func() {
			defer workerWG.Done()
			worker(info, jobs, found, done, &tested)
		}()
	}

	if showStats {
		go func() {
			ticker := time.NewTicker(progress)
			defer ticker.Stop()

			start := time.Now()
			for {
				select {
				case <-done:
					return
				case <-ticker.C:
					count := atomic.LoadUint64(&tested)
					elapsed := time.Since(start).Seconds()
					if elapsed == 0 {
						continue
					}
					fmt.Fprintf(os.Stderr, "tested=%d rate=%.2f/sec\n", count, float64(count)/elapsed)
				}
			}
		}()
	}

	scanner := bufio.NewScanner(file)
	// Long passphrases are rare here, but raise the cap enough to avoid surprises.
	scanner.Buffer(make([]byte, 0, 4096), 1024*1024)

	go func() {
		defer close(jobs)
		for scanner.Scan() {
			line := strings.TrimRight(scanner.Text(), "\r")
			if line == "" {
				continue
			}

			select {
			case <-done:
				return
			case jobs <- line:
			}
		}

		if err := scanner.Err(); err != nil {
			log.Printf("scan wordlist: %v", err)
		}
	}()

	workersDone := make(chan struct{})
	go func() {
		workerWG.Wait()
		close(workersDone)
	}()

	select {
	case password := <-found:
		once.Do(func() { close(done) })
		fmt.Println(password)
	case <-workersDone:
		once.Do(func() { close(done) })
		os.Exit(1)
	}
}
