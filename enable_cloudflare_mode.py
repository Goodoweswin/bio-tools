import os
import json

# Configuration
ASSETS_DIR = "public/tools/assets/pyodide"
LOCK_FILE = os.path.join(ASSETS_DIR, "pyodide-lock.json")
SCIPY_FILENAME = "scipy-1.11.2-cp311-cp311-emscripten_3_1_46_wasm32.whl"
SCIPY_URL = "https://pyodide-cdn2.iodide.io/v0.25.0/full/" + SCIPY_FILENAME
FILEPATH = os.path.join(ASSETS_DIR, SCIPY_FILENAME)

def install_cloudflare():
    print(f"--- Switching to CLOUDFLARE MODE ---")
    
    # 1. Delete local Scipy wheel to save space/meet limits
    if os.path.exists(FILEPATH):
        print(f"Removing local {SCIPY_FILENAME}...")
        os.remove(FILEPATH)
    else:
        print(f"Local {SCIPY_FILENAME} not found (good).")

    # 2. Update Lockfile to use Remote CDN URL
    with open(LOCK_FILE, "r") as f:
        data = json.load(f)
    
    if "packages" in data and "scipy" in data["packages"]:
        print("Updating pyodide-lock.json to use REMOTE URL...")
        data["packages"]["scipy"]["file_name"] = SCIPY_URL
        # We don't touch sha256 because it should be the same for official file
        
    with open(LOCK_FILE, "w") as f:
        json.dump(data, f, indent=None, separators=(',', ':'))
        
    print("SUCCESS: Project is now configured for Cloudflare Pages (25MB limit compliant).")

if __name__ == "__main__":
    install_cloudflare()
