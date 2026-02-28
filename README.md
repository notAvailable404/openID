# OpenIDScan — CC0 / Public Domain

**This project is released under [CC0 1.0 Universal (CC0 1.0) Public Domain Dedication].**
You can copy, modify, redistribute, and use this project for any purpose without restriction.

---

## What is this?

`OpenIDScan` is a tiny, permissive, open-source Python library to extract the **country** and **date of birth** text from identity documents (ID cards, passports, driver’s licenses) using simple OCR and heuristics. It is intentionally minimal — no LLMs, no big proprietary vision stacks — just OCR and lightweight parsing so projects can have a transparent, auditable alternative to closed-source age/ID checks.

This library was made as a gift to the open-source community because the author is opposed to proprietary systems handling sensitive personal identity data — especially surveillance-style vendors. Projects like Palantir are exactly the kind of opaque tooling the author wants to avoid. Freedom and privacy matter.

---

## Key points / design goals

* **Simple**: Only extracts `nation` and `birth` (date of birth). Keep the surface area small.
* **Transparent**: All code runs locally; easy to audit and modify.
* **Lightweight**: Uses Tesseract OCR + heuristics — no heavy ML models.
* **FOSS & Public Domain**: CC0 license so organizations and individuals can reuse freely.
* **Privacy-first**: The library does **not** upload user data anywhere. If you build a cloud service with it, make the privacy trade-offs explicit.

> ⚠️ The library does **not** attempt to verify whether an ID is real or forged. It only reads text. Detecting fraud or liveness is the responsibility of the integrator.

---

## Supported (and planned) input formats

* **Images**: JPEG, PNG, BMP — these are supported by OpenCV and work out of the box.
* **PDFs**: *Planned / optional* — requires `pdf2image` and a system dependency (`poppler-utils` / `poppler`) to rasterize pages before OCR. If you want PDFs, install the extras (see Installation).

---

## Installation

1. Clone the repo:

```bash
git clone https://github.com/you/OpenIDScan.git
cd OpenIDScan
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. **System dependency — Tesseract OCR**
   `pytesseract` is only a Python wrapper. You **must** install the Tesseract binary on your system:

* Debian/Ubuntu/Zorin:

```bash
sudo apt update
sudo apt install tesseract-ocr
```

* macOS (Homebrew):

```bash
brew install tesseract
```

* Windows: install from the official Tesseract installer and ensure the exe is on your PATH.

4. (Optional) For PDF support:

* Install `poppler` (system package) and add `pdf2image` to `requirements.txt`.

---

## Quick usage

### As a CLI (provided script)

```bash
python openIDscan.py /path/to/id_image.jpg
# Optional: python openIDscan.py /path/to/doc.pdf --debug
```

Output: JSON with keys:

* `nation`: ISO alpha-3 code or `None`
* `nation_confidence`: float 0.0–1.0
* `birth`: formatted date string (MM/DD/YYYY for USA or DD/MM/YYYY otherwise) or `None`
* `birth_format`: which format is used
* `birth_confidence`: float 0.0–1.0
* `needs_human_review`: boolean

### As a FastAPI endpoint (example)

The repo includes a minimal `api.py` that exposes:
`POST /scan` — accepts a file upload and returns the JSON result from `simple_scan()`.

Run with Uvicorn:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

Example `curl`:

```bash
curl -F "file=@/path/to/id.jpg" http://localhost:8000/scan
```

---

## Behavior & limitations

* **No authenticity checks**: The library does not validate holograms, MRZ, or security features.
* **Heuristic parsing**: Dates and countries are found by pattern matching; results vary with image quality and OCR accuracy.
* **Date parsing locale**: If “USA” or “UNITED STATES” is detected, month-first parsing is preferred; otherwise day-first is attempted.
* **Privacy**: The library attempts to avoid keeping files around; the API script deletes the temporary file after scanning. Still, do not upload sensitive IDs to third-party servers unless you trust and control them.

---

## Security & legal disclaimers

* This project is **not** legal or compliance advice. Many jurisdictions have legal rules for age verification, identity handling, and data retention. Integrators must ensure their system complies with applicable laws and industry best practices.
* Use of this library is at your own risk. It is provided "as-is" with no warranties.
* The library intentionally **does not** perform liveness/fraud detection. Relying solely on OCR results for authorization decisions is dangerous.

---

## Contributing

This library is of public use, you can use it at your own risk, i will not update it unless i personally feel like it, thus why i upload this as the CC0 1.0 License, so that any who feel interested can fork this library and make the modifications they wish for, i am just a spark on a matchbox, if the fire dies out or not, i do not personally care
Use this however you see fit, but i will probably just ghost this repository, i don't particularly understand how other people can keep working on the same project for years, i'm just a hobbyist who jumps from project to project on a daily basis, all of my code is released under CC0.

---

## License & attribution

**CC0 1.0 Universal (Public Domain Dedication)** — do whatever you want with this code.

If you redistribute, a short attribution is appreciated but not required.

---

## Final note from the author

> “I don’t like proprietary code touching personal identity data. This project is a small, public-domain alternative — built so people have a transparent option.”
> — ME

