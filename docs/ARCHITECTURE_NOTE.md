# Architecture Note: Stlite/Pyodide Deployment

**Date**: 2026-01-09
**Issue**: Deployment Failure on Cloudflare Pages.
**Cause**: The `scipy` wheel file in Pyodide is ~41MB. Cloudflare Pages Free/Pro plans have a hard limit of 25MB per file.

## Solution: Hybrid CDN Loading
Instead of hosting the full Python runtime environment locally in `public/tools/assets/pyodide/`, we switched to a CDN-based approach.

### Changes
1.  **Removed**: Local `tools/assets/pyodide` directory (saving ~200MB space).
2.  **Kept**: `tools/assets/pypi` (contains our custom/small wheels like `seaborn`).
3.  **Updated**: `index.html` configuration:
    ```javascript
    stlite.mount({
        // Point to official CDN for the heavy runtime and standard libs (numpy, scipy)
        pyodideUrl: "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js",
        
        // Still load specific lightweight requirements
        requirements: [ "pandas", "matplotlib", ... ]
    })
    ```

## Implications
- **Internet Access**: The tool now requires internet access for the **first load** to fetch Pyodide from CDN. It is no longer strictly "offline-capable" out of the box (unless cached).
- **Performance**: Generally faster for users due to CDN edge caching of common Pyodide libraries.
