# Go Hygiene Ratchet

Use this when a Go repository does not already have a hygiene-budget test. Install a prebuild ratchet at `internal/hygiene_test.go` or another package-level `*_test.go` file that participates in `go test ./...`.

## Requirements

- Scan production `.go` files only.
- Exclude `*_test.go`.
- Enforce test boundary hygiene (`test-boundary-hygiene.md`): no `func Test` in
  non-`*_test.go` files. Banned-pattern budgets apply to production `.go` only.
- Encode each smell as a budget constant.
- Budgets must be monotonic: initialize to current totals, then only lower them.
- Failure output must print file:line hits for exceeded categories.

## Required baseline checks

- ` any`
  Use a simple token search first; the point is to ratchet down `any` usage in production code.
- `log.Printf`, `log.Println`, `log.Fatal`, `log.Panic`
  This catches ad hoc logging and panic-driven control flow leaking into production paths.

## Optional extra budgets

Add these when they fit the repo's style and debt model:

- `panic(`
- `_ =` or `var _ =` patterns that discard meaningful results
- `context.Background()` outside process wiring

## Starter template

```go
package hygiene_test

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

const maxAny = 0
const maxLogCalls = 0

type sourceFile struct {
	path    string
	content string
}

func collectGoFiles(dir string) []sourceFile {
	var files []sourceFile
	_ = filepath.WalkDir(dir, func(path string, d os.DirEntry, err error) error {
		if err != nil || d.IsDir() {
			return err
		}
		if !strings.HasSuffix(path, ".go") || strings.HasSuffix(path, "_test.go") {
			return nil
		}
		data, readErr := os.ReadFile(path)
		if readErr == nil {
			files = append(files, sourceFile{path: path, content: string(data)})
		}
		return nil
	})
	return files
}

func countMatches(files []sourceFile, pattern string) int {
	total := 0
	for _, f := range files {
		for _, line := range strings.Split(f.content, "\n") {
			if strings.Contains(line, pattern) {
				total++
			}
		}
	}
	return total
}

func TestHygiene_AnyBudget(t *testing.T) {
	files := collectGoFiles(".")
	count := countMatches(files, " any")
	if count > maxAny {
		t.Fatalf("`any` budget exceeded: found %d, max %d", count, maxAny)
	}
}
```

Mirror that test shape for the log-call budget and include detailed hit reporting when it exceeds the limit.

## Installation notes

- Use package-local paths so `go test ./...` picks the test up automatically.
- Favor simple substring scans unless a regex is necessary.
- Run `go test ./...` after adding the ratchet, and `go test -run Hygiene ./...` if the repo needs a narrower first pass.
