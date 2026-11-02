// Calendar-day arithmetic uses UTC serials so DST never adds or removes a day.
export const DAY = 86_400_000;
export const dateKey = (date) => `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
export const daySerial = (date) => Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()) / DAY;
export function parseDate(value) {
  if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return null;
  const [year, month, day] = value.split("-").map(Number);
  const date = new Date(year, month - 1, day);
  return year >= 1900 && dateKey(date) === value ? date : null;
}
export function yearProgress(now = new Date()) {
  const year = now.getFullYear();
  const start = new Date(year, 0, 1);
  const end = new Date(year + 1, 0, 1);
  const total = daySerial(end) - daySerial(start);
  const elapsed = daySerial(now) - daySerial(start);
  const dayFraction = (now.getHours() * 3600 + now.getMinutes() * 60 + now.getSeconds()) / 86400;
  return { year, total, elapsed, percent: (elapsed + dayFraction) / total * 100 };
}
export function lifeProgress(birthday, horizon, now = new Date()) {
  const birth = parseDate(birthday);
  if (!birth || daySerial(birth) > daySerial(now) || !Number.isFinite(horizon) || horizon < 1 || horizon > 120) return null;
  // A Feb 29 anniversary falls on Feb 28 in a non-leap year.
  const wholeYears = Math.floor(horizon);
  const end = new Date(birth.getFullYear() + wholeYears, birth.getMonth(), 1);
  const lastDay = new Date(end.getFullYear(), end.getMonth() + 1, 0).getDate();
  end.setDate(Math.min(birth.getDate(), lastDay));
  if (horizon !== wholeYears) {
    const next = new Date(birth.getFullYear() + wholeYears + 1, birth.getMonth(), 1);
    next.setDate(Math.min(birth.getDate(), new Date(next.getFullYear(), next.getMonth() + 1, 0).getDate()));
    // Fractional years interpolate between real anniversaries, rounded to a day.
    // The data retain their precision; only the UI rounds years to two decimals.
    end.setDate(end.getDate() + Math.round((daySerial(next) - daySerial(end)) * (horizon - wholeYears)));
  }
  const totalDays = daySerial(end) - daySerial(birth);
  const elapsedDays = daySerial(now) - daySerial(birth);
  const weeks = Math.ceil(totalDays / 7);
  const completed = Math.min(Math.floor(elapsedDays / 7), weeks);
  const ended = elapsedDays >= totalDays;
  return { birth, end, totalDays, elapsedDays, weeks, completed: ended ? weeks : completed, current: ended ? -1 : completed, remaining: Math.max(0, totalDays - elapsedDays), ended };
}
