import { DAY, dateKey, daySerial, yearProgress, lifeProgress } from "./life-time.js";

import { LIFE_PROFILE } from "./life-profile.js";
const formatNumber = new Intl.NumberFormat("zh-CN");
const clamp = (value, low, high) => Math.max(low, Math.min(high, value));

// Scoped to its host so the same component can be embedded on any page.
class TimeField {
  constructor(root) {
    this.root = root;
    this.canvas = root.querySelector("canvas");
    this.context = this.canvas.getContext("2d");
    this.stage = root.querySelector(".time-field-stage");
    this.tooltip = root.querySelector("[data-field-tooltip]");
    this.reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
    this.embedded = Boolean(root.closest(".hero-time-field"));
    this.mode = "life";
    this.pointer = null;
    this.hover = -1;
    this.visible = false;
    this.frame = 0;
    this.lastFrame = 0;
    if (!this.context) {
      root.querySelector("[data-field-count]").textContent = "此浏览器暂不支持时间点阵。";
      return;
    }
    root.querySelectorAll("[data-field-mode]").forEach((button) => {
      button.addEventListener("click", () => {
        if (button.dataset.fieldMode === this.mode) return;
        this.mode = button.dataset.fieldMode;
        this.update();
      });
    });
    this.stage.addEventListener("pointermove", (event) => {
      if (event.pointerType === "touch") return;
      const rect = this.stage.getBoundingClientRect();
      this.pointer = { x: event.clientX - rect.left, y: event.clientY - rect.top };
      this.inspect();
      if (!this.reducedMotion.matches) {
        this.canvas.style.transform = `perspective(1000px) rotateX(${(0.5 - this.pointer.y / this.height) * 2}deg) rotateY(${(this.pointer.x / this.width - 0.5) * 2}deg)`;
      }
      this.start();
    });
    this.stage.addEventListener("pointerleave", () => {
      this.pointer = null;
      this.tooltip.hidden = true;
      this.canvas.style.transform = "";
      this.draw(performance.now());
    });
    this.reducedMotion.addEventListener("change", () => {
      this.canvas.style.transform = "";
      this.revealStart = performance.now() - 2000;
      this.stop();
      this.start();
    });
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) this.stop();
      else {
        if (this.day !== dateKey(new Date())) this.update();
        this.start();
      }
    });
    this.resizeObserver = new ResizeObserver(() => this.resize());
    this.resizeObserver.observe(this.stage);
    this.intersectionObserver = new IntersectionObserver(([entry]) => {
      this.visible = entry.isIntersecting;
      if (this.visible && !this.hasEntered) {
        this.hasEntered = true;
        this.revealStart = performance.now();
      }
      if (this.visible) this.start();
      else this.stop();
    });
    this.intersectionObserver.observe(root);
    this.timer = setInterval(() => {
      if (!document.hidden && this.day !== dateKey(new Date())) this.update();
    }, 60_000);
    this.update();
  }

  update() {
    const now = new Date();
    this.day = dateKey(now);
    const life = lifeProgress(LIFE_PROFILE.birthday, LIFE_PROFILE.expectancyYears, now);
    const year = yearProgress(now);
    const isLife = this.mode === "life";
    this.total = isLife ? life.weeks : year.total;
    this.completed = isLife ? life.completed : year.elapsed;
    this.current = isLife ? life.current : year.elapsed;
    this.firstSerial = isLife ? daySerial(life.birth) : daySerial(new Date(year.year, 0, 1));
    this.lastSerial = isLife ? daySerial(life.end) - 1 : daySerial(new Date(year.year + 1, 0, 1)) - 1;
    this.step = isLife ? 7 : 1;
    this.root.dataset.mode = this.mode;
    this.root.dataset.total = this.total;
    this.root.dataset.current = this.current;
    this.root.querySelectorAll("[data-field-mode]").forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.fieldMode === this.mode)));
    this.root.dataset.birthday = LIFE_PROFILE.birthday;
    this.root.dataset.expectancy = String(LIFE_PROFILE.expectancyYears);
    const source = this.root.querySelector('[data-field-source]');
    source.textContent = `中国男性 ${LIFE_PROFILE.expectancyYears.toFixed(2)} 岁 · 世行 ${LIFE_PROFILE.dataYear} ↗`;
    source.href = LIFE_PROFILE.sourceUrl;
    source.title = `中国男性出生时预期寿命 ${LIFE_PROFILE.expectancyYears} 岁；${LIFE_PROFILE.sourceName}，${LIFE_PROFILE.dataYear} 年，指标 ${LIFE_PROFILE.indicator}。群体时期统计，不能预测个人寿命。`;
    const summary = `${formatNumber.format(this.completed)} / ${formatNumber.format(this.total)} ${isLife ? "周" : "天"}已走过`;
    this.root.querySelector("[data-field-count]").textContent = summary;
    this.canvas.setAttribute("aria-label", `${LIFE_PROFILE.birthday} 出生。${summary}。中国男性出生时预期寿命参考 ${LIFE_PROFILE.expectancyYears} 岁，数据为 ${LIFE_PROFILE.dataYear} 年；群体统计，非个人寿命预测。${this.current < 0 ? "已越过群体参考尺度，时间仍在继续。" : `绿色光点代表${isLife ? `人生第 ${this.current + 1} 周` : "今天"}。`}`);
    this.revealStart = performance.now();
    this.pointer = null;
    this.tooltip.hidden = true;
    this.resize();
  }

  resize() {
    this.width = this.stage.clientWidth;
    this.height = this.stage.clientHeight;
    if (!this.width || !this.height) return;
    const ratio = Math.min(devicePixelRatio || 1, 2);
    this.canvas.width = Math.round(this.width * ratio);
    this.canvas.height = Math.round(this.height * ratio);
    this.context.setTransform(ratio, 0, 0, ratio, 0, 0);
    const style = getComputedStyle(this.root);
    this.pastColor = style.getPropertyValue("--field-dot-past").trim().split(",").map(Number);
    this.futureColor = style.getPropertyValue("--field-dot-future").trim().split(",").map(Number);
    this.highlightColor = style.getPropertyValue("--field-highlight").trim();
    this.haloColor = style.getPropertyValue("--field-halo").trim();
    const life = this.mode === "life";
    const compact = this.width < 600;
    const groups = life ? 4 : 1;
    const across = life ? compact ? 2 : 4 : 1;
    const down = life && compact ? 2 : 1;
    const rows = life ? this.embedded ? 26 : 52 : this.embedded ? 7 : compact ? 26 : 13;
    const columns = Math.ceil(this.total / (groups * rows));
    const paddingX = this.embedded ? 6 : compact ? 9 : 18;
    const paddingY = this.embedded ? 8 : 24;
    const groupGap = life ? this.embedded ? 12 : compact ? 24 : 32 : 0;
    const verticalGap = this.embedded ? 14 : 32;
    const groupWidth = (this.width - paddingX * 2 - groupGap * (across - 1)) / across;
    const groupHeight = (this.height - paddingY * 2 - (down - 1) * verticalGap) / down;
    const dx = groupWidth / Math.max(columns - 1, 1);
    const dy = groupHeight / (rows - 1);
    this.radius = Math.min(life ? 3.5 : 4.5, dx * 0.3, dy * 0.3);
    this.points = Array.from({ length: this.total }, (_, index) => {
      const group = Math.floor(index / (columns * rows));
      const local = index % (columns * rows);
      return {
        x: paddingX + (group % across) * (groupWidth + groupGap) + Math.floor(local / rows) * dx,
        y: paddingY + Math.floor(group / across) * (groupHeight + verticalGap) + (local % rows) * dy,
      };
    });
    this.draw(performance.now());
    this.start();
  }

  inspect() {
    if (!this.pointer || !this.points) return;
    let nearest = -1;
    let distance = 16 * 16;
    for (let index = 0; index < this.points.length; index++) {
      const point = this.points[index];
      const candidate = (point.x - this.pointer.x) ** 2 + (point.y - this.pointer.y) ** 2;
      if (candidate < distance) { nearest = index; distance = candidate; }
    }
    this.tooltip.hidden = nearest < 0;
    if (nearest < 0) return;
    const start = this.firstSerial + nearest * this.step;
    const end = Math.min(start + this.step - 1, this.lastSerial);
    const iso = (serial) => new Date(serial * DAY).toISOString().slice(0, 10).replaceAll("-", ".");
    this.tooltip.textContent = this.mode === "life" ? `第 ${formatNumber.format(nearest + 1)} 周 · ${iso(start)} — ${iso(end)}` : `${iso(start)}${nearest === this.current ? " · 今天" : ""}`;
    this.tooltip.style.left = `${clamp(this.pointer.x + 14, 4, this.width - Math.min(280, this.width - 8))}px`;
    this.tooltip.style.top = `${clamp(this.pointer.y + 18, 4, this.height - 38)}px`;
    if (this.reducedMotion.matches) this.draw(performance.now());
  }

  draw(time) {
    if (!this.points) return;
    const context = this.context;
    context.clearRect(0, 0, this.width, this.height);
    const progress = this.reducedMotion.matches ? 1 : clamp((time - this.revealStart) / 1350, 0, 1);
    const reveal = progress * (this.completed + 1);
    for (let index = 0; index < this.points.length; index++) {
      const point = this.points[index];
      const elapsed = index < this.completed;
      const distance = this.pointer && !this.reducedMotion.matches ? Math.hypot(point.x - this.pointer.x, point.y - this.pointer.y) : Infinity;
      const influence = Math.max(0, 1 - distance / 95);
      let x = point.x;
      let y = point.y;
      if (influence > 0 && distance > 0) {
        x += (point.x - this.pointer.x) / distance * influence * 2;
        y += (point.y - this.pointer.y) / distance * influence * 2;
      }
      const revealed = index <= reveal;
      const color = elapsed && revealed ? this.pastColor : this.futureColor;
      const shift = Math.round(influence * (this.embedded ? -35 : 55));
      context.fillStyle = `rgb(${color.map((channel) => clamp(channel + shift, 0, 255)).join(",")})`;
      context.beginPath();
      context.arc(x, y, this.radius * (1 + influence * 0.55), 0, Math.PI * 2);
      context.fill();
    }
    const point = this.points[this.current];
    if (point && progress >= 0.99) {
      const breath = this.reducedMotion.matches ? 0.5 : (Math.sin(time / 800) + 1) / 2;
      const radius = this.radius + 1;
      const halo = context.createRadialGradient(point.x, point.y, 0, point.x, point.y, radius * 5);
      halo.addColorStop(0, `rgba(${this.haloColor},${0.2 + breath * 0.14})`);
      halo.addColorStop(1, `rgba(${this.haloColor},0)`);
      context.fillStyle = halo;
      context.beginPath();
      context.arc(point.x, point.y, radius * 5, 0, Math.PI * 2);
      context.fill();
      context.strokeStyle = `rgba(${this.haloColor},${0.3 + breath * 0.4})`;
      context.lineWidth = 0.8;
      context.beginPath();
      context.arc(point.x, point.y, radius + 3 + breath * 2, 0, Math.PI * 2);
      context.stroke();
      context.fillStyle = `rgb(${this.highlightColor})`;
      context.beginPath();
      context.arc(point.x, point.y, radius, 0, Math.PI * 2);
      context.fill();
    }
  }

  start() {
    if (!this.visible || document.hidden || this.frame) return;
    if (this.reducedMotion.matches) { this.draw(performance.now()); return; }
    const animate = (time) => {
      if (!this.visible || document.hidden) { this.frame = 0; return; }
      if (time - this.lastFrame >= 32) {
        this.draw(time);
        this.lastFrame = time;
      }
      this.frame = requestAnimationFrame(animate);
    };
    this.frame = requestAnimationFrame(animate);
  }

  stop() {
    cancelAnimationFrame(this.frame);
    this.frame = 0;
  }
}

document.querySelectorAll("[data-time-field]").forEach((root) => new TimeField(root));
