## PDF password remover

This utility decrypts all PDFs in a folder (using a shared password) and saves new copies that are **not** password-protected.

### What it does

- **Input folder**: `/Users/himanshubansal7/Downloads/password_protected_pdfs`
- **Output folder**: `/Users/himanshubansal7/Downloads/unlocked_pdfs`
- **Output naming**: adds `_nopw` to the filename (example: `file.pdf` → `file_nopw.pdf`)

### Prerequisites

- macOS with `python3` available

### One-time setup

From Terminal:

```bash
cd /Users/himanshubansal7/CursorDev

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install pypdf "cryptography>=3.1"
```

### Run

```bash
cd /Users/himanshubansal7/CursorDev
source venv/bin/activate
python remove_pdf_passwords.py /Users/himanshubansal7/Downloads/password_protected_pdfs \
  -o /Users/himanshubansal7/Downloads/unlocked_pdfs
```

When prompted, enter the **shared PDF password** (it won’t echo).

### Output

Unlocked PDFs will be written to:

- `/Users/himanshubansal7/Downloads/unlocked_pdfs`

### Notes / troubleshooting

- If you see `cryptography>=3.1 is required for AES algorithm`, re-run:

```bash
source venv/bin/activate
pip install "cryptography>=3.1"
```
