import test from "node:test";
import assert from "node:assert/strict";
import { dateKey, daySerial, parseDate, yearProgress, lifeProgress } from "../src/js/life-time.js";

test("real calendar years include leap days", () => {
  assert.equal(yearProgress(new Date(2024, 11, 31, 12)).total, 366);
  assert.equal(yearProgress(new Date(2025, 0, 1)).percent, 0);
  assert.equal(yearProgress(new Date(2025, 11, 31)).elapsed, 364);
  assert.equal(lifeProgress("2000-01-01", 80, new Date(2026, 10, 2)).totalDays, 29220);
});
test("invalid, future and corrupt profile dates are rejected", () => {
  for (const value of ["2025-02-29", "2024-04-31", "garbage", null, "1899-01-01"]) assert.equal(parseDate(value), null);
  for (const horizon of [0, -1, 121, NaN, Infinity, "80", null]) assert.equal(lifeProgress("2000-01-01", horizon), null);
  assert.equal(lifeProgress("2026-11-03", 80, new Date(2026, 10, 2)), null);
});
test("a newborn starts at week one and advances after seven real days", () => {
  const born = lifeProgress("2024-02-29", 80, new Date(2024, 1, 29));
  assert.equal(born.completed, 0);
  assert.equal(born.current, 0);
  assert.equal(lifeProgress("2024-02-29", 80, new Date(2024, 2, 7)).completed, 1);
});
test("February 29 horizons clamp to February 28", () => {
  const life = lifeProgress("2000-02-29", 1, new Date(2001, 1, 28));
  assert.equal(dateKey(life.end), "2001-02-28");
  assert.equal(life.totalDays, 365);
  assert.equal(life.ended, true);
  assert.equal(life.current, -1);
  assert.equal(life.completed, life.weeks);
});
test("older visitors and horizons already passed have a finite complete calendar", () => {
  const life = lifeProgress("1930-01-01", 80, new Date(2026, 10, 2));
  assert.equal(life.ended, true);
  assert.equal(life.remaining, 0);
  assert.equal(life.completed, life.weeks);
});
test("calendar-day arithmetic survives daylight saving transitions", () => {
  assert.equal(daySerial(new Date(2026, 2, 9)) - daySerial(new Date(2026, 2, 8)), 1);
});

test("fractional life expectancy preserves source precision", () => {
  const life = lifeProgress("2000-09-05", 75.249, new Date(2026, 10, 2));
  assert.equal(dateKey(life.end), "2075-12-05");
  assert.ok(life.totalDays > lifeProgress("2000-09-05", 75).totalDays);
  assert.ok(life.totalDays < lifeProgress("2000-09-05", 76).totalDays);
  assert.equal(life.weeks, Math.ceil(life.totalDays / 7));
});
