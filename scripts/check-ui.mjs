import fs from "node:fs/promises";
import path from "node:path";
import os from "node:os";

const output = process.env.QA_OUTPUT || path.join(os.tmpdir(), "daiger-ui");
await fs.mkdir(output, { recursive: true });

const ws = new WebSocket(process.env.BIDI_URL || "ws://127.0.0.1:9224/session");
await new Promise((resolve, reject) => {
  ws.onopen = resolve;
  ws.onerror = reject;
});
let id = 0;
const pending = new Map();
const errors = [];
ws.onmessage = ({ data }) => {
  const m = JSON.parse(data);
  if (m.method === "log.entryAdded" && m.params.level === "error")
    errors.push(m.params.text);
  const task = pending.get(m.id);
  if (!task) return;
  pending.delete(m.id);
  if (m.type === "error") task.reject(new Error(m.message));
  else task.resolve(m.result);
};
const call = (method, params = {}) =>
  new Promise((resolve, reject) => {
    pending.set(++id, { resolve, reject });
    ws.send(JSON.stringify({ id, method, params }));
  });
const checks = [];
const check = (label, ok, detail) => {
  checks.push({ label, ok, detail });
  console.log(JSON.stringify({ label, ok, detail }));
};
let context;
let sessionStarted = false;
const linkTargets = new Set();
const evaluate = async (expression) => {
  const result = await call("script.evaluate", {
    target: { context },
    expression,
    awaitPromise: true,
  });
  if (result.type === "exception")
    throw new Error(result.exceptionDetails.text);
  return result.result.value;
};
const json = async (expression) =>
  JSON.parse(
    await evaluate(
      "(async () => JSON.stringify(await (" + expression + ")))()",
    ),
  );
const settle = () =>
  evaluate(
    "Promise.all([document.fonts.ready, new Promise(r=>setTimeout(r,250))]).then(()=>true)",
  );
const screenshot = async (name, full = false) => {
  if (full) {
    await evaluate(`Promise.all([...document.images].map(image => {
      image.loading = 'eager';
      return image.decode().catch(() => null);
    })).then(() => true)`);
    check(
      "Images in " + name,
      await evaluate(
        `[...document.images].every(image => image.complete && image.naturalWidth > 0)`,
      ),
    );
  }
  const shot = await call("browsingContext.captureScreenshot", {
    context,
    origin: full ? "document" : "viewport",
  });
  await fs.writeFile(
    path.join(output, name + ".png"),
    Buffer.from(shot.data, "base64"),
  );
};
try {
  await call("session.new", { capabilities: { alwaysMatch: {} } });
  sessionStarted = true;
  await call("session.subscribe", { events: ["log.entryAdded"] });
  ({ context } = await call("browsingContext.create", { type: "tab" }));
  const base = process.env.BASE_URL || "http://127.0.0.1:61531";
  const routes = [
    "/",
    "/research.html",
    "/tools.html",
    "/knowledge.html",
    "/publications.html",
  ];
  for (const width of [1440, 390, 320, 768, 1920]) {
    await call("browsingContext.setViewport", {
      context,
      viewport: { width, height: width > 1000 ? 900 : 844 },
      devicePixelRatio: 1,
    });
    for (const route of routes) {
      await call("browsingContext.navigate", {
        context,
        url: base + route,
        wait: "complete",
      });
      await settle();
      for (const url of await json(
        `[...document.querySelectorAll('a[href],img[src],link[rel="stylesheet"],script[src]')].map(e=>e.href||e.src).filter(url=>url && new URL(url).origin===location.origin)`,
      ))
        linkTargets.add(url);
      const info = await json(
        `({width:innerWidth,scroll:document.documentElement.scrollWidth,h1:[...document.querySelectorAll('h1')].map(x=>x.textContent),active:[...document.querySelectorAll('.nav-links [aria-current="page"]')].map(x=>x.textContent),broken:[...document.images].filter(i=>!i.closest('details:not([open])') && i.loading!=='lazy' && (!i.complete || !i.naturalWidth)).map(i=>i.src),overflow:[...document.querySelectorAll('main *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0 && (r.right>innerWidth+1 || r.left< -1)}).slice(0,6).map(e=>e.tagName+'.'+e.className)})`,
      );
      check(
        route + " @" + width,
        info.scroll <= width &&
          info.h1.length === 1 &&
          info.active.length === 1 &&
          !info.broken.length &&
          !info.overflow.length,
        info,
      );
      if (route === "/" && width === 1440) {
        const fonts = await json(`Promise.all([
          document.fonts.load('400 17px "Source Sans 3"'),
          document.fonts.load('600 20px "Source Sans 3"'),
          document.fonts.load('400 64px "Source Serif 4"'),
          document.fonts.load('600 32px "Source Serif 4"')
        ]).then(groups=>groups.map(group=>group.map(face=>({family:face.family,status:face.status}))))`);
        check(
          "Self-hosted fonts loaded",
          fonts.every(
            (group) =>
              group.length > 0 &&
              group.every((face) => face.status === "loaded"),
          ),
          fonts,
        );
        check(
          "M.D. student identity",
          await evaluate(
            `document.querySelector('.hero-identity').textContent.includes('M.D. Student') && document.querySelector('meta[name="description"]').content.includes('M.D. student') && !document.body.textContent.toLowerCase().includes("master's student")`,
          ),
        );
      }
      if (route === "/" && width === 390) {
        check(
          "Mobile biography has full reading width",
          await evaluate(
            `document.querySelector('.about-copy').getBoundingClientRect().width >= innerWidth-64`,
          ),
        );
      }
      if (route === "/publications.html" && width === 1440) {
        check(
          "Submitted work and contribution are explicit",
          await evaluate(
            `document.querySelector('#manuscripts').textContent.includes('Manuscript submitted') && document.querySelector('#manuscripts').textContent.includes('Co-first author, listed second')`,
          ),
        );
      }
      if ([1440, 390].includes(width))
        await screenshot(
          (route === "/" ? "home" : route.slice(1, -5)) + "-" + width,
        );
      if (route === "/" && [1440, 390, 1920].includes(width)) {
        const hero = await json(
          `({bottom:document.querySelector('.home-hero').getBoundingClientRect().bottom,height:innerHeight,portraitFilter:getComputedStyle(document.querySelector('.portrait')).filter})`,
        );
        check(
          "Homepage next-section hint @" + width,
          hero.bottom < hero.height && hero.portraitFilter === "none",
          hero,
        );
        if (width === 1440) await screenshot("home-full", true);
      }
    }
  }
  for (const [width, height] of [
    [320, 568],
    [390, 667],
    [768, 844],
    [1440, 768],
    [1920, 900],
  ]) {
    await call("browsingContext.setViewport", {
      context,
      viewport: { width, height },
      devicePixelRatio: 1,
    });
    await call("browsingContext.navigate", {
      context,
      url: base + "/",
      wait: "complete",
    });
    await settle();
    const next = await json(
      `({top:document.querySelector('.about-layout > :first-child').getBoundingClientRect().top,viewport:innerHeight})`,
    );
    check(
      "Next content visible " + width + "x" + height,
      next.top < height,
      next,
    );
    await screenshot("home-" + width + "x" + height);
  }
  await call("browsingContext.setViewport", {
    context,
    viewport: { width: 390, height: 844 },
    devicePixelRatio: 1,
  });
  await call("browsingContext.navigate", {
    context,
    url: base + "/knowledge.html",
    wait: "complete",
  });
  await settle();
  await evaluate(`document.querySelector('.menu-toggle').click()`);
  check(
    "Mobile menu opens",
    await evaluate(
      `document.querySelector('.menu-toggle').getAttribute('aria-expanded')==='true' && getComputedStyle(document.querySelector('#site-links')).display==='flex'`,
    ),
  );
  await screenshot("menu-390");
  await call("input.performActions", {
    context,
    actions: [
      {
        type: "key",
        id: "keyboard",
        actions: [
          { type: "keyDown", value: "\uE00C" },
          { type: "keyUp", value: "\uE00C" },
        ],
      },
    ],
  });
  check(
    "Escape closes menu and returns focus",
    await evaluate(
      `document.querySelector('.menu-toggle').getAttribute('aria-expanded')==='false' && document.activeElement.matches('.menu-toggle')`,
    ),
  );
  for (const [query, expected] of [
    ["HES1", 1],
    ["皮肤衰老", 4],
    ["zzzz-not-found", 0],
    ["", 12],
  ]) {
    await evaluate(
      `document.querySelector('#knowledge-search').value=${JSON.stringify(query)}; document.querySelector('#knowledge-search').dispatchEvent(new Event('input'))`,
    );
    const count = await evaluate(
      `document.querySelectorAll('.knowledge-note:not([hidden])').length`,
    );
    check("Search " + query, count === expected, { count, expected });
    if (!count) await screenshot("empty-390");
  }
  for (const track of ["ai-single-cell", "skin-aging", "ai4med"]) {
    await evaluate(
      `document.querySelector('[data-track="${track}"].knowledge-filter').click()`,
    );
    check(
      "Filter " + track,
      await evaluate(
        `document.querySelectorAll('.knowledge-note:not([hidden])').length===4 && document.querySelectorAll('.knowledge-track-group:not([hidden])').length===1`,
      ),
    );
  }
  await evaluate(
    `document.querySelector('#knowledge-search').value='zzzz';document.querySelector('#knowledge-search').dispatchEvent(new Event('input'));document.querySelector('#reset-notes').click()`,
  );
  check(
    "Clear filters resets query and category",
    await evaluate(
      `document.querySelectorAll('.knowledge-note:not([hidden])').length===12 && document.activeElement.id==='knowledge-search' && document.querySelector('#empty-state').hidden`,
    ),
  );
  await evaluate(`document.querySelector('#sc-chat-toggle').click()`);
  check(
    "Assistant opens and focuses password",
    await evaluate(
      `!document.querySelector('#sc-chat-window').hidden && document.activeElement.id==='chat-password'`,
    ),
  );
  await screenshot("chat-390");
  await call("input.performActions", {
    context,
    actions: [
      {
        type: "key",
        id: "keyboard",
        actions: [
          { type: "keyDown", value: "\uE00C" },
          { type: "keyUp", value: "\uE00C" },
        ],
      },
    ],
  });
  check(
    "Assistant closes and restores focus",
    await evaluate(
      `document.querySelector('#sc-chat-window').hidden && document.activeElement.id==='sc-chat-toggle'`,
    ),
  );
  const noteLinks = await json(
    `[...document.querySelectorAll('.knowledge-note')].map(a=>a.href)`,
  );
  for (const url of noteLinks) {
    await call("browsingContext.navigate", { context, url, wait: "complete" });
    check(
      "Article " + new URL(url).pathname,
      await evaluate(
        `document.querySelectorAll('h1').length===1 && document.documentElement.scrollWidth<=innerWidth && getComputedStyle(document.body).backgroundColor==='rgb(255, 255, 255)'`,
      ),
    );
  }
  await screenshot("article-390");
  await call("browsingContext.navigate", {
    context,
    url: base + "/research.html",
    wait: "complete",
  });
  await evaluate(
    `document.querySelectorAll('details').forEach(e=>e.open=true)`,
  );
  await evaluate(
    `Promise.all([...document.images].map(i=>{i.loading='eager';return i.decode().catch(()=>null)})).then(()=>true)`,
  );
  check(
    "All research figures load",
    await evaluate(
      `[...document.images].every(i=>i.complete && i.naturalWidth>0)`,
    ),
  );
  const ratios = await json(
    `[...document.querySelectorAll('.scientific-figure img')].map(i=>({src:i.src,natural:i.naturalWidth/i.naturalHeight,rendered:i.width/i.height}))`,
  );
  check(
    "Research figure proportions",
    ratios.every((r) => Math.abs(r.natural - r.rendered) < 0.02),
    ratios,
  );
  await screenshot("research-expanded-390", true);
  const linkResults =
    await json(String.raw`Promise.all(${JSON.stringify([...linkTargets])}.map(async href => {
    const url=new URL(href);
    const response=await fetch(url.href);
    let ok=response.ok;
    let reason='';
    const type=response.headers.get('content-type') || '';
    if(/\\.(webp|png|jpg)$/.test(url.pathname) && !type.startsWith('image/')){ok=false;reason='wrong image content type'}
    if(url.pathname.endsWith('.pdf') && !type.includes('application/pdf')){ok=false;reason='wrong PDF content type'}
    if(url.hash && type.includes('text/html')){
      const doc=new DOMParser().parseFromString(await response.text(),'text/html');
      if(!doc.getElementById(decodeURIComponent(url.hash.slice(1)))){ok=false;reason='missing anchor'}
    }
    return {href,ok,status:response.status,reason};
  }))`);
  check(
    "Local links and assets",
    linkResults.every((r) => r.ok),
    { checked: linkResults.length, failed: linkResults.filter((r) => !r.ok) },
  );
  await call("browsingContext.navigate", {
    context,
    url: base + "/knowledge.html",
    wait: "complete",
  });
  await evaluate(
    `window.originalFetch=window.fetch;window.fetch=async()=>new Response(JSON.stringify({answer:'<img src=x onerror=alert(1)>'}),{status:200,headers:{'Content-Type':'application/json'}});document.querySelector('#sc-chat-toggle').click();document.querySelector('#chat-password').value='qa-only';authenticate();document.querySelector('#chat-input').value='test';sendMessage()`,
  );
  await settle();
  check(
    "Assistant response renders as text",
    await evaluate(
      `!document.querySelector('#messages-container img') && document.querySelector('#messages-container').textContent.includes('<img')`,
    ),
  );
  await evaluate(
    `window.fetch=async()=>new Response('',{status:401});document.querySelector('#chat-input').value='test';sendMessage()`,
  );
  await settle();
  check(
    "Assistant 401 returns to authentication",
    await evaluate(
      `!document.querySelector('#auth-view').hidden && document.querySelector('#chat-view').hidden && !localStorage.getItem('sc_chat_password')`,
    ),
  );
  await evaluate(
    `window.fetch=window.originalFetch;delete window.originalFetch;document.querySelector('.chat-close').click();document.documentElement.classList.remove('js')`,
  );
  check(
    "Navigation fallback without JS class",
    await evaluate(
      `getComputedStyle(document.querySelector('#site-links')).display==='flex'`,
    ),
  );
  check("Browser console", !errors.length, errors);
  await fs.writeFile(
    path.join(output, "checks.json"),
    JSON.stringify(checks, null, 2),
  );
  if (checks.some((c) => !c.ok)) process.exitCode = 1;
} finally {
  if (context) await call("browsingContext.close", { context }).catch(() => {});
  if (sessionStarted) await call("session.end").catch(() => {});
  ws.close();
}
