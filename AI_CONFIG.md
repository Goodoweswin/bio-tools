# AI Configuration Guide

This guide explains how to configure, switch, and manage the AI models (Google Gemini & DeepSeek) for the Bio-Tools website.

All configurations are managed via **Cloudflare Pages Environment Variables**, so you do not need to modify the code to switch providers or models.

## 1. Accessing Configuration

1.  Log in to the [Cloudflare Dashboard](https://dash.cloudflare.com/).
2.  Go to **Compute (Workers & Pages)** -> Select your project (`bio-tools`).
3.  Navigate to **Settings** -> **Environment Variables**.
4.  Click **Edit variables** to make changes.

---

## 2. Switching AI Providers (`AI_PROVIDER`)

You can switch between Google Gemini and DeepSeek by changing the `AI_PROVIDER` variable.

| Variable Name | Value | Description |
| :--- | :--- | :--- |
| `AI_PROVIDER` | `gemini` | **(Default)** Uses Google Gemini API. |
| `AI_PROVIDER` | `deepseek` | Uses DeepSeek API (OpenAI Compatible). |

**Note**: After changing this value, you must go to the **Deployments** tab and click **Retry deployment** on the latest build for the change to take effect.

---

## 3. Configuring Google Gemini

If `AI_PROVIDER` is set to `gemini`:

### Required Variables
*   `GEMINI_API_KEY`: Your Google AI Studio API Key.
*   `CF_ACCOUNT_ID`: Your Cloudflare Account ID (for AI Gateway).
*   `AI_GATEWAY_NAME`: The name of your AI Gateway (e.g., `biotools-gateway`).

### Optional Variables
*   `GEMINI_MODEL`: The specific model version to use.
    *   **Default**: `gemini-2.0-flash` (if not set).
    *   **Examples**: `gemini-1.5-pro`, `gemini-1.5-flash`, `gemini-1.0-pro`.
    *   *Tip*: Use the `/debug` command in the chat window to see which models your API Key has access to.

---

## 4. Configuring DeepSeek

If `AI_PROVIDER` is set to `deepseek`:

### Required Variables
*   `DEEPSEEK_API_KEY`: Your DeepSeek API Key (starts with `sk-`).

### Notes
*   DeepSeek currently uses the `deepseek-chat` (V3) model by default.
*   The integration uses the OpenAI-compatible endpoint (`https://api.deepseek.com/chat/completions`).

---

## 5. Troubleshooting

### Common Errors

*   **404 Not Found (Gemini)**:
    *   Usually means the `GEMINI_MODEL` you set is not available for your API Key.
    *   **Fix**: Remove the `GEMINI_MODEL` variable to use the default, or use `/debug` to find a valid model name.

*   **429 Quota Exceeded**:
    *   Means you hit the rate limit.
    *   **Fix**: Switch providers (e.g., from Gemini to DeepSeek) temporarily, or wait a few minutes.

*   **500 Internal Server Error**:
    *   Check if your API Keys are correct.
    *   Check if `AI_PROVIDER` is spelled correctly (lowercase).

### Diagnostic Tool
In the website chat window, type:
```
/debug
```
This will run a connection test and list available Gemini models.
