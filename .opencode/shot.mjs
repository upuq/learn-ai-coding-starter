import { chromium } from "playwright";

const width = Number(process.argv[2] ?? 375);
const out = process.argv[3] ?? `screenshot-${width}.png`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width, height: 900 } });
const errors = [];
page.on("console", (m) => {
  if (m.type() === "error") errors.push(m.text());
});
page.on("pageerror", (e) => errors.push(String(e)));

await page.goto("http://localhost:8080/", { waitUntil: "load" });
await page.fill("#source", "hallucinate(\u201cthe slop must flow\u201d)\u2728");
await page.click("#run");
await page.waitForFunction(
  () => document.querySelector("#output")?.textContent !== "Running\u2026",
  { timeout: 10000 },
);
await page.waitForTimeout(200);

const metrics = await page.evaluate(() => {
  const doc = document.documentElement;
  const pre = document.querySelector("#output");
  const ta = document.querySelector("#source");
  const rect = pre.getBoundingClientRect();
  return {
    viewport: doc.clientWidth,
    docScrollWidth: doc.scrollWidth,
    bodyScrollWidth: document.body.scrollWidth,
    preScrollWidth: pre.scrollWidth,
    preClientWidth: pre.clientWidth,
    preRight: Math.round(rect.right),
    preMinWidth: getComputedStyle(pre).minWidth,
    textareaScrollWidth: ta.scrollWidth,
    output: pre.textContent.trim(),
  };
});

console.log(JSON.stringify({ width, out, errors, metrics }, null, 2));
await page.screenshot({ path: out, fullPage: true });
await browser.close();
