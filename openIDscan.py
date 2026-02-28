import os, re, sys, json, pytesseract, pycountry, cv2
from dateutil import parser

def simple_scan(file_path, debug=False):
    # 1. Basic Load
    img = cv2.imread(file_path)
    if img is None: 
        return {"errors": ["File not found or unreadable."]}
    
    # 2. Minimum Preprocessing (Grayscale + Rescale)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # 3. Get RAW string (PSM 11 is best for scattered text)
    raw_text = pytesseract.image_to_string(gray, config='--oem 3 --psm 11').upper()
    
    # 4. Brute Force Nation Detection
    nation = None
    nation_conf = 0.0
    
    if "USA" in raw_text or "UNITED STATES" in raw_text:
        nation = "USA"
        nation_conf = 0.95 
    else:
        for c in pycountry.countries:
            if c.alpha_3 in raw_text or c.name.upper() in raw_text:
                nation = c.alpha_3
                nation_conf = 0.85
                break

    # 5. Brute Force DOB Detection
    date_pattern = re.compile(r'(\d{1,4}[\/\-\.\s][A-Z0-9]{2,9}[\/\-\.\s]\d{2,4})')
    matches = date_pattern.findall(raw_text)
    
    birth = None
    birth_conf = 0.0
    dayfirst = False if nation == "USA" else True
    
    # Check for ID keywords anywhere in the text
    kw_found = any(kw in raw_text for kw in ['DOB', 'BIRTH', 'BORN', 'DATE', '3 ', 'POS'])
    
    for match in matches:
        if kw_found:
            try:
                dt = parser.parse(match.replace(':', ' '), fuzzy=True, dayfirst=dayfirst)
                birth = dt.strftime("%m/%d/%Y" if nation == "USA" else "%d/%m/%Y")
                birth_conf = 0.90 
                break
            except: 
                continue

    # 6. Build the secure base result
    result = {
        "nation": nation,
        "nation_confidence": nation_conf,
        "birth": birth,
        "birth_format": "MM/DD/YYYY" if nation == "USA" else "DD/MM/YYYY",
        "birth_confidence": birth_conf,
        "needs_human_review": (nation is None) or (birth is None)
    }

    # 7. Append debug info ONLY if requested, and sanitize PII
    if debug:
        result["raw_matches"] = matches
        # Redact all numbers with 'X' to prevent PII leakage in logs
        sanitized_text = re.sub(r'\d', 'X', raw_text[:150].replace('\n', ' '))
        result["ocr_text_sample_sanitized"] = sanitized_text

    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        # Check if the user passed '--debug' or 'debug=True' in the CLI
        is_debug = any(arg.lower() in ['--debug', 'debug=true'] for arg in sys.argv)
        
        print(json.dumps(simple_scan(file_path, debug=is_debug), indent=2))
