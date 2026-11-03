/**
 * CAELIS // 2D Collision Detection Radar Scope
 * Renders rotating scope, range circles, target blips, and proximity warnings.
 */

class CaelisRadar {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas ? this.canvas.getContext('2d') : null;
    this.sweepAngle = 0;
    this.targets = [
      { r: 40, theta: 0.8, type: 'debris' },
      { r: 80, theta: 2.4, type: 'craft' },
      { r: 110, theta: 4.8, type: 'satellite' },
    ];
  }

  init() {
    if (!this.canvas || !this.ctx) return;
    this.animate();
  }

  animate() {
    requestAnimationFrame(() => this.animate());
    if (!this.ctx) return;

    const w = this.canvas.width;
    const h = this.canvas.height;
    const cx = w / 2;
    const cy = h / 2;
    const radius = Math.min(cx, cy) - 5;

    // Clear
    this.ctx.clearRect(0, 0, w, h);

    // Background
    this.ctx.fillStyle = '#02060e';
    this.ctx.beginPath();
    this.ctx.arc(cx, cy, radius, 0, Math.PI * 2);
    this.ctx.fill();

    // Concentric Range Rings
    this.ctx.strokeStyle = 'rgba(0, 240, 255, 0.25)';
    this.ctx.lineWidth = 1;

    [0.3, 0.6, 0.9].forEach(factor => {
      this.ctx.beginPath();
      this.ctx.arc(cx, cy, radius * factor, 0, Math.PI * 2);
      this.ctx.stroke();
    });

    // Crosshairs
    this.ctx.beginPath();
    this.ctx.moveTo(cx - radius, cy);
    this.ctx.lineTo(cx + radius, cy);
    this.ctx.moveTo(cx, cy - radius);
    this.ctx.lineTo(cx, cy + radius);
    this.ctx.stroke();

    // Rotating Sweep Line
    const sweepX = cx + Math.cos(this.sweepAngle) * radius;
    const sweepY = cy + Math.sin(this.sweepAngle) * radius;

    // Sweep Line Gradient
    this.ctx.strokeStyle = 'rgba(0, 240, 255, 0.8)';
    this.ctx.shadowColor = '#00f0ff';
    this.ctx.shadowBlur = 8;
    this.ctx.beginPath();
    this.ctx.moveTo(cx, cy);
    this.ctx.lineTo(sweepX, sweepY);
    this.ctx.stroke();
    this.ctx.shadowBlur = 0;

    // Render Targets
    this.targets.forEach(target => {
      const tx = cx + Math.cos(target.theta) * (target.r * (radius / 130));
      const ty = cy + Math.sin(target.theta) * (target.r * (radius / 130));

      const diff = Math.abs(this.sweepAngle - target.theta) % (Math.PI * 2);
      const alpha = diff < 0.8 ? 1.0 - diff / 0.8 : 0.2;

      this.ctx.fillStyle = target.type === 'debris' ? `rgba(255, 170, 0, ${alpha})` : `rgba(0, 255, 157, ${alpha})`;
      this.ctx.beginPath();
      this.ctx.arc(tx, ty, 3, 0, Math.PI * 2);
      this.ctx.fill();

      // Pulsing Ring for active blips
      if (alpha > 0.6) {
        this.ctx.strokeStyle = this.ctx.fillStyle;
        this.ctx.beginPath();
        this.ctx.arc(tx, ty, 6, 0, Math.PI * 2);
        this.ctx.stroke();
      }
    });

    // Update Angle & Target motion
    this.sweepAngle = (this.sweepAngle + 0.03) % (Math.PI * 2);
    this.targets.forEach(t => {
      t.theta = (t.theta + 0.002) % (Math.PI * 2);
    });
  }
}

window.caelisRadar = CaelisRadar;
