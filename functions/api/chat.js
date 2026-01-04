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

    // 4. Retrieve Knowledge Context
    const context = await fetchKnowledgeContext(userQuestion, env);

    // 5. Build Prompt
    const prompt = buildSingleCellPrompt(userQuestion, context);

    // 6. Call Gemini API
    const aiResponse = await callGemini(prompt, env);

    // 7. Return Result
    return new Response(JSON.stringify({
      answer: aiResponse,
      references: context.map(c => c.title),
      quota: { used: "tracked_internally", total: 100 }
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
    You are an expert in Single-Cell Omics and Bioinformatics.
    Use the following context to answer the user's question.
    If the answer is not in the context, use your general knowledge but mention that it's general info.
    
    Context:
    ${contextText}
    
    User Question: ${question}
    
    Answer in a professional, academic tone. Use Markdown.
  `;
}

/**
 * Call Google Gemini API
 * Supports Cloudflare AI Gateway if configured
 */
async function callGemini(prompt, env) {
  const apiKey = env.GEMINI_API_KEY;
  if (!apiKey) throw new Error("GEMINI_API_KEY not configured");

  let url;
  // Check if AI Gateway is configured
  if (env.CF_ACCOUNT_ID && env.AI_GATEWAY_NAME) {
    // Use Cloudflare AI Gateway
    // Format: https://gateway.ai.cloudflare.com/v1/{account_id}/{gateway_id}/google-ai-studio/...
    url = `https://gateway.ai.cloudflare.com/v1/${env.CF_ACCOUNT_ID}/${env.AI_GATEWAY_NAME}/google-ai-studio/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;
  } else {
    // Direct Google API
    url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;
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
