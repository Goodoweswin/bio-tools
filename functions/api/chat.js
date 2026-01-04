/**
 * Handle AI Chat Request
 * Route: POST /api/chat
 */
export async function onRequestPost({ request, env }) {
  try {
    // 1. Authentication
    if (!checkPassword(request, env)) {
      return new Response(JSON.stringify({ error: "Unauthorized" }), { 
        status: 401, 
        headers: { "Content-Type": "application/json" } 
      });
    }

    // 2. Rate Limiting
    const ip = request.headers.get("CF-Connecting-IP") || "unknown";
    const isAllowed = await checkRateLimit(ip, env);
    if (!isAllowed) {
      return new Response(JSON.stringify({ error: "Rate limit exceeded (100 requests/day)" }), { 
        status: 429, 
        headers: { "Content-Type": "application/json" } 
      });
    }

    // 3. Parse Request
    const body = await request.json();
    const userQuestion = body.question || "";
    if (!userQuestion) {
      return new Response(JSON.stringify({ error: "Question is required" }), { status: 400 });
    }

    // [DEBUG MODE]
    if (userQuestion.trim() === "/debug") {
      const debugInfo = await diagnoseConnection(env);
      return new Response(JSON.stringify({
        answer: "### 🔍 Diagnostic Report\n\n" + debugInfo,
        references: ["System Diagnosis"],
        quota: { used: 0, total: 100 }
      }), { headers: { "Content-Type": "application/json" } });
    }

    // 4. Retrieve Knowledge Context
    const context = await fetchKnowledgeContext(userQuestion, env);

    // 5. Build Prompt
    const prompt = buildSingleCellPrompt(userQuestion, context);

    // 6. Call AI API (Gemini or DeepSeek)
    let aiResponse;
    const provider = env.AI_PROVIDER || "gemini"; // Default to gemini

    if (provider.toLowerCase() === "deepseek") {
      aiResponse = await callDeepSeek(prompt, env);
    } else {
      aiResponse = await callGemini(prompt, env);
    }

    // 7. Return Result
    return new Response(JSON.stringify({
      answer: aiResponse,
      references: context.map(c => c.title),
      quota: { used: "tracked_internally", total: 100, provider: provider }
    }), { 
      headers: { "Content-Type": "application/json" } 
    });

  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), { 
      status: 500, 
      headers: { "Content-Type": "application/json" } 
    });
  }
}

/**
 * Check HTTP Basic Auth
 */
function checkPassword(request, env) {
  const authHeader = request.headers.get("Authorization");
  if (!authHeader || !authHeader.startsWith("Basic ")) return false;

  const base64Credentials = authHeader.split(" ")[1];
  const credentials = atob(base64Credentials); // user:password
  const [username, password] = credentials.split(":");

  // Compare with environment variable
  return password === env.ACCESS_PASSWORD;
}

/**
 * Check Rate Limit using KV
 * Limit: 100 requests per IP per day
 */
async function checkRateLimit(ip, env) {
  const key = `rate_limit:${ip}:${new Date().toISOString().split('T')[0]}`; // Key: rate_limit:1.2.3.4:2025-01-03
  // Note: In Pages Functions, KV bindings are accessed directly from `env` just like in Workers
  if (!env.RATE_LIMIT) return true; // Skip if KV not bound (dev mode)

  const count = await env.RATE_LIMIT.get(key);
  
  if (count && parseInt(count) >= 100) {
    return false;
  }

  // Increment count
  const newCount = count ? parseInt(count) + 1 : 1;
  await env.RATE_LIMIT.put(key, newCount.toString(), { expirationTtl: 86400 }); // Expire in 24h
  return true;
}

/**
 * Fetch relevant context from Knowledge Base KV
 */
async function fetchKnowledgeContext(question, env) {
  return []; 
}

/**
 * Build System Prompt for Single Cell Domain
 */
function buildSingleCellPrompt(question, context) {
  const contextText = context.map(c => `Title: ${c.title}\nContent: ${c.content}`).join("\n\n");
  
  return `
    You are the AI Research Assistant for a Plastic Surgery PhD Candidate's personal website (Bio-Tools).
    The website owner is an expert in Single-Cell Omics, Skin Aging, and AI4Med.
    
    Your Role:
    1. Answer questions about the owner's research (Skin Aging, Alopecia, Single-Cell Analysis).
    2. Assist with bioinformatics questions using your general knowledge.
    3. Represent the owner professionally but warmly.

    Context from Knowledge Base:
    ${contextText}
    
    User Question: ${question}
    
    Instructions:
    - If the user asks "Who are you?" or "Who is the owner?", introduce the PhD candidate and this website.
    - If the answer is found in the Context above, use it.
    - If the answer is NOT in the Context, use your own vast knowledge to answer helpfully (do not say "I don't know" unless it's personal info not provided).
    - Use Markdown for formatting.
  `;
}

/**
 * Call Google Gemini API
 * Supports Cloudflare AI Gateway if configured
 */
async function callGemini(prompt, env) {
  const apiKey = env.GEMINI_API_KEY;
  if (!apiKey) throw new Error("GEMINI_API_KEY not configured");

  // Use model from env var, or default to a stable version that exists for this user
  const model = env.GEMINI_MODEL || "gemini-2.0-flash";

  let url;
  // Check if AI Gateway is configured
  if (env.CF_ACCOUNT_ID && env.AI_GATEWAY_NAME) {
    // Use Cloudflare AI Gateway
    // Format: https://gateway.ai.cloudflare.com/v1/{account_id}/{gateway_id}/google-ai-studio/...
    url = `https://gateway.ai.cloudflare.com/v1/${env.CF_ACCOUNT_ID}/${env.AI_GATEWAY_NAME}/google-ai-studio/v1beta/models/${model}:generateContent?key=${apiKey}`;
  } else {
    // Direct Google API
    url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;
  }

  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }]
    })
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`Gemini API Error: ${response.status} - ${err}`);
  }

  const data = await response.json();
  return data.candidates[0].content.parts[0].text;
}

/**
 * Call DeepSeek API (OpenAI Compatible)
 * Supports Cloudflare AI Gateway if configured
 */
async function callDeepSeek(prompt, env) {
  const apiKey = env.DEEPSEEK_API_KEY;
  if (!apiKey) throw new Error("DEEPSEEK_API_KEY not configured");

  let url;
  // Check if AI Gateway is configured
  if (env.CF_ACCOUNT_ID && env.AI_GATEWAY_NAME) {
    // Use Cloudflare AI Gateway (OpenAI Compatible Endpoint)
    // Format: https://gateway.ai.cloudflare.com/v1/{account_id}/{gateway_id}/openai/chat/completions
    // Note: We map DeepSeek to the 'openai' provider in Gateway because it uses the OpenAI format.
    // You must ensure your Gateway is configured to allow the 'openai' provider (or 'universal').
    url = `https://gateway.ai.cloudflare.com/v1/${env.CF_ACCOUNT_ID}/${env.AI_GATEWAY_NAME}/openai/chat/completions`;
  } else {
    // Direct DeepSeek API
    url = "https://api.deepseek.com/chat/completions";
  }

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model: "deepseek-chat",
      messages: [
        { role: "system", content: "You are a helpful assistant." }, // DeepSeek often behaves better with a system prompt
        { role: "user", content: prompt }
      ],
      stream: false
    })
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`DeepSeek API Error: ${response.status} - ${err}`);
  }

  const data = await response.json();
  return data.choices[0].message.content;
}

/**
 * Diagnostic Function to List Available Models
 */
async function diagnoseConnection(env) {
  const apiKey = env.GEMINI_API_KEY;
  if (!apiKey) return "❌ Error: GEMINI_API_KEY is missing in environment variables.";

  const logs = [];
  logs.push(`- **API Key Configured**: Yes (Starts with ${apiKey.substring(0, 4)}...)`);
  logs.push(`- **AI Gateway**: ${env.AI_GATEWAY_NAME ? "Configured" : "Not Configured"}`);
  
  // Try to list models via Direct API (Bypass Gateway to isolate issue)
  const directUrl = `https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey}`;
  
  try {
    const response = await fetch(directUrl);
    const status = response.status;
    const text = await response.text();
    
    logs.push(`- **Direct API Status**: ${status}`);
    
    if (status === 200) {
      const data = JSON.parse(text);
      const models = data.models ? data.models.map(m => `\`${m.name}\``).join(", ") : "No models found";
      logs.push(`- **Available Models**: ${models}`);
      return logs.join("\n");
    } else {
      logs.push(`- **Error Response**: \`${text}\``);
      
      if (status === 404) logs.push("\n**Diagnosis**: 404 on ListModels usually means the API Key is invalid, or the 'Generative Language API' is not enabled in Google Cloud Console.");
      if (status === 403) logs.push("\n**Diagnosis**: 403 means Permission Denied. Check if your API Key has restrictions.");
      
      return logs.join("\n");
    }
  } catch (e) {
    return `❌ Network Error: ${e.message}`;
  }
}
