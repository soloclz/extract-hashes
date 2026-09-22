# extract-hashes

Extract common hexadecimal hash candidates from text, HTML, or Markdown evidence.
The command normalizes candidates to lowercase, removes duplicates, and writes one
hash per line for tools such as Hashcat or hashID.

## Install

Python 3.10 or newer is required. There are no runtime dependencies.

```sh
uv tool install git+https://github.com/soloclz/extract-hashes.git
extract-hashes --help
```

For development or an editable local checkout:

```sh
git clone https://github.com/soloclz/extract-hashes.git
cd extract-hashes
uv tool install .
```

`pipx install .` is also supported. After updating the checkout, use
`uv tool install --force .` or `pipx reinstall extract-hashes` to deploy the new
version.

On Kali, the same checkout-based pipx workflow used by `bhq` is:

```sh
git clone https://github.com/soloclz/extract-hashes.git ~/tools/extract-hashes
pipx install ~/tools/extract-hashes
extract-hashes --help
```

For development, run `uv sync --extra dev`, then `uv run pytest -q`.

## Usage

Write candidates to a file:

```sh
extract-hashes response.html -o hashes.txt
```

Read stdin and write the hashes to stdout:

```sh
cat response.html | extract-hashes - > hashes.txt
```

The extraction summary and structural candidates go to stderr, so redirected
stdout contains only hashes. The command recognizes unsalted hexadecimal strings
with lengths commonly used by MD5, SHA-1, SHA-2, MD4, and NTLM.

For example, a 32-character hexadecimal value is compatible with MD5, MD4, NTLM,
and other 128-bit formats. Length and character set do not prove the algorithm.
Confirm it from application context, source code, product documentation, or a
controlled known-plaintext verification before selecting a cracking mode.

## Hashcat handoff

After confirming MD5, mode `0` can consume the output directly:

```sh
hashcat -m 0 hashes.txt /path/to/wordlist
hashcat -m 0 hashes.txt --show
```

Keep engagement hashes and recovered credentials out of the repository. The
default `.gitignore` excludes common evidence and potfile paths, but review staged
files before every commit.

## License

MIT. See [LICENSE](LICENSE).
