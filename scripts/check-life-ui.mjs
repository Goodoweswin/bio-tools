// Start Firefox with --headless --remote-debugging-port 9224 before running.
import fs from "node:fs/promises";
import path from "node:path";

const output = process.env.QA_OUTPUT || "/tmp/daiger-life-qa";
const base = process.env.BASE_URL || "http://127.0.0.1:61531";
await fs.mkdir(output, { recursive: true });
const ws = new WebSocket(process.env.BIDI_URL || "ws://127.0.0.1:9224/session");
await new Promise((resolve, reject) => { ws.onopen = resolve; ws.onerror = reject; });
let sequence = 0;
const pending = new Map();
const errors = [];
const checks = [];
ws.onmessage = ({ data }) => {
  const result = JSON.parse(data);
  if (result.method === "log.entryAdded" && result.params.level === "error") errors.push(result.params.text);
  const task = pending.get(result.id);
  if (!task) return;
  pending.delete(result.id);
  if (result.type === "error") task.reject(new Error(result.message));
  else task.resolve(result.result);
};
const call = (method, params = {}) => new Promise((resolve, reject) => {
  pending.set(++sequence, { resolve, reject });
  ws.send(JSON.stringify({ id: sequence, method, params }));
});
let context;
const evaluate = async (expression) => {
  const result = await call("script.evaluate", { target: { context }, expression, awaitPromise: true });
  if (result.type === "exception") throw new Error(result.exceptionDetails.text);
  return result.result.value;
};
const check = async (label, expression) => {
  const ok = await evaluate(expression);
  checks.push({ label, ok });
  console.log(JSON.stringify({ label, ok }));
};
const go = async (route) => {
  await call("browsingContext.navigate", { context, url: base + route, wait: "complete" });
  await evaluate("new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))).then(()=>document.fonts.ready).then(()=>true)");
};
const screenshot = async (name, origin = "document") => {
  const shot = await call("browsingContext.captureScreenshot", { context, origin });
  await fs.writeFile(path.join(output, name + ".png"), Buffer.from(shot.data, "base64"));
};
try {
  await call("session.new", { capabilities: { alwaysMatch: {} } });
  await call("session.subscribe", { events: ["log.entryAdded"] });
  ({ context } = await call("browsingContext.create", { type: "tab" }));
  await go("/life.html");
  await evaluate("localStorage.setItem('jd-life-profile-v1',JSON.stringify({birthday:'1930-01-01',horizon:80}))");
  for (const width of [1440, 768, 390, 320]) {
    await call("browsingContext.setViewport", { context, viewport: { width, height: 900 }, devicePixelRatio: 1 });
    await go("/life.html");
    await evaluate("new Promise(r=>setTimeout(r,1500)).then(()=>true)");
    await check("Owner birthday and sourced fractional scale at " + width, "document.querySelector('[data-time-field]').dataset.birthday==='2000-09-05' && document.querySelector('[data-time-field]').dataset.expectancy==='75.249' && Number(document.querySelector('[data-time-field]').dataset.total)>3900 && Number(document.querySelector('[data-time-field]').dataset.total)<4000 && document.documentElement.scrollWidth<=innerWidth");
    await check("No example or custom profile controls at " + width, "!document.querySelector('[data-field-demo]') && !document.querySelector('.time-field-form') && !document.querySelector('.time-field-settings') && !document.querySelector('[name=horizon]') && !document.querySelector('[data-time-field]').textContent.includes('示例')");
    await check("Source year and interpretation are labeled at " + width, "document.querySelector('[data-field-source]').textContent.includes('75.25') && document.querySelector('[data-field-source]').textContent.includes('2024') && document.querySelector('[data-field-source]').href.includes('SP.DYN.LE00.MA.IN') && document.querySelector('.time-field-reference').textContent.includes('非个人预测')");
    await check("Canvas actually paints at " + width, "(()=>{const c=document.querySelector('canvas');return c.getContext('2d').getImageData(0,0,c.width,c.height).data.some((v,i)=>i%4===3&&v>0)})()");
    if ([1440,390].includes(width)) await screenshot("life-" + width, "viewport");
    await evaluate("document.querySelector('[data-field-mode=year]').click()");
    await check("Days mode still works at " + width, "Number(document.querySelector('[data-time-field]').dataset.total)>=365 && Number(document.querySelector('[data-time-field]').dataset.total)<=366 && document.querySelector('[data-field-mode=year]').getAttribute('aria-pressed')==='true'");
    await go("/");
    await check("First hero slide and concise homepage at " + width, "document.querySelector('[data-hero-carousel]').dataset.slide==='0' && document.querySelectorAll('h1').length===1 && document.querySelectorAll('main > section').length===4 && !document.querySelector('#notes [data-time-field]') && document.documentElement.scrollWidth<=innerWidth");
    await evaluate("document.querySelector('[data-carousel-pause]').click();document.querySelector('[data-carousel-dot=\"1\"]').click();new Promise(r=>setTimeout(r,1700)).then(()=>true)");
    await check("Personal time slide is visible and fits at " + width, "(()=>{const hero=document.querySelector('[data-hero-carousel]');const source=document.querySelector('#time .time-field-reference').getBoundingClientRect();return hero.dataset.slide==='1'&&hero.getBoundingClientRect().bottom<innerHeight&&source.bottom<=hero.getBoundingClientRect().bottom&&source.left>=0&&source.right<=innerWidth&&document.querySelector('#time [data-time-field]').dataset.birthday==='2000-09-05'&&document.documentElement.scrollWidth<=innerWidth})()");
    await screenshot("hero-time-" + width, "viewport");
    await evaluate("document.querySelector('[data-carousel-prev]').click();new Promise(r=>setTimeout(r,600)).then(()=>true)");
    await check("Returning to illustration makes time slide inert at " + width, "document.querySelector('[data-hero-carousel]').dataset.slide==='0'&&document.querySelectorAll('[data-carousel-slide][inert]').length===1");
    await evaluate("const viewport=document.querySelector('[data-carousel-viewport]');viewport.scrollTo({left:viewport.clientWidth,behavior:'instant'});new Promise(r=>setTimeout(r,250)).then(()=>true)");
    await check("Native horizontal scrolling updates controls at " + width, "document.querySelector('[data-hero-carousel]').dataset.slide==='1'");
  }
  await go("/life.html");
  await evaluate("document.querySelector('[data-field-mode=year]').click();const stage=document.querySelector('.time-field-stage');const rect=stage.getBoundingClientRect();stage.dispatchEvent(new PointerEvent('pointermove',{clientX:rect.left+9,clientY:rect.top+24,pointerType:'mouse'}))");
  await check("Pointer inspection retains dates", "!document.querySelector('[data-field-tooltip]').hidden && /[0-9]{4}\\.[0-9]{2}\\.[0-9]{2}/.test(document.querySelector('[data-field-tooltip]').textContent)");
  await go("/#time");
  await evaluate("new Promise(r=>setTimeout(r,300)).then(()=>true)");
  await check("The time anchor opens the personal slide", "document.querySelector('[data-hero-carousel]').dataset.slide==='1'");
  await go("/");
  await evaluate("new Promise(r=>setTimeout(r,8400)).then(()=>true)");
  await check("Automatic rotation reveals the personal time slide", "document.querySelector('[data-hero-carousel]').dataset.slide==='1'");
  await evaluate("document.querySelector('[data-carousel-pause]').click();document.querySelector('[data-carousel-dot=\"0\"]').click();new Promise(r=>setTimeout(r,8400)).then(()=>true)");
  await check("Pause prevents further automatic rotation", "document.querySelector('[data-hero-carousel]').dataset.slide==='0'&&document.querySelector('[data-carousel-pause]').getAttribute('aria-pressed')==='true'");
  const preload = await call("script.addPreloadScript", { functionDeclaration: "()=>{const original=window.matchMedia.bind(window);window.matchMedia=query=>{const result=original(query);if(query.includes('prefers-reduced-motion'))Object.defineProperty(result,'matches',{value:true});return result}}" });
  await go("/life.html");
  await evaluate("new Promise(r=>setTimeout(r,100)).then(()=>true)");
  await check("Reduced motion renders a static complete field immediately", "(async()=>{const canvas=document.querySelector('canvas');const before=canvas.toDataURL();await new Promise(r=>setTimeout(r,200));return before===canvas.toDataURL() && document.querySelector('canvas').getAttribute('aria-label').includes('绿色光点')})()");
  await go("/");
  await check("Reduced motion disables automatic hero rotation", "document.querySelector('[data-carousel-pause]').getAttribute('aria-pressed')==='true'");
  await call("script.removePreloadScript", { script: preload.script });
  await go("/life.html");
  await evaluate("localStorage.removeItem('jd-life-profile-v1')");
  // Firefox can report its own privileged-page CSP during preload emulation.
  const browserDiagnostics = errors.filter(error => error.includes("script-src resource: chrome:"));
  const pageErrors = errors.filter(error => !browserDiagnostics.includes(error));
  checks.push({ label: "Browser console", ok: pageErrors.length === 0, errors: pageErrors, browserDiagnostics });
  await fs.writeFile(path.join(output, "checks.json"), JSON.stringify(checks, null, 2));
  if (checks.some((check) => !check.ok)) process.exitCode = 1;
} finally {
  if (context) await call("browsingContext.close", { context }).catch(() => {});
  await call("session.end").catch(() => {});
  ws.close();
}
