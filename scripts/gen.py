#!/usr/bin/env python3
import base64, json, os, sys, urllib.request

KEY = open(os.path.expanduser("~/etsy-magaza-v3-baby/.env")).read().strip().split("=",1)[1]
MODEL = "gemini-3.1-flash-image"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}"

def generate(prompt, out_path, aspect="4:5", input_image=None):
    parts = []
    if input_image:
        with open(input_image, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        parts.append({"inline_data": {"mime_type": "image/png", "data": img_b64}})
    parts.append({"text": prompt})
    body = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": aspect}
        }
    }
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        resp = json.load(r)
    for part in resp["candidates"][0]["content"]["parts"]:
        if "inlineData" in part:
            with open(out_path, "wb") as f:
                f.write(base64.b64decode(part["inlineData"]["data"]))
            print(f"SAVED {out_path}")
            return True
    print("NO IMAGE IN RESPONSE"); print(json.dumps(resp)[:500])
    return False

if __name__ == "__main__":
    prompt_file, out_path = sys.argv[1], sys.argv[2]
    aspect = sys.argv[3] if len(sys.argv) > 3 else "4:5"
    input_img = sys.argv[4] if len(sys.argv) > 4 else None
    generate(open(prompt_file).read(), out_path, aspect, input_img)
