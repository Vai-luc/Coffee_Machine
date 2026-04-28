const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

export function initSporographAnimation(canvasId = 'sporographCanvas') {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const palette = ['#0a4426', '#4a7a50', '#b8c9b1', '#fffcf5', '#f0ae50'];
  let width = 0;
  let height = 0;
  let frame = 0;
  let lastTime = performance.now();
  let frameCount = 0;
  let fps = 0;

  const resize = () => {
    const ratio = window.devicePixelRatio || 1;
    width = canvas.clientWidth;
    height = canvas.clientHeight;
    canvas.width = width * ratio;
    canvas.height = height * ratio;
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  };

  const draw = (currentTime) => {
    ctx.clearRect(0, 0, width, height);
    ctx.save();
    ctx.translate(width / 2, height / 2);

    const segments = 6;
    const baseRadius = Math.min(width, height) * 0.18;
    const time = frame * 0.014;

    for (let ring = 0; ring < 4; ring += 1) {
      const hue = (frame * 2 + ring * 40) % 360;
      ctx.strokeStyle = palette[ring % palette.length];
      ctx.globalAlpha = 0.7 - ring * 0.14;
      ctx.lineWidth = 2 + ring * 0.8;
      ctx.beginPath();

      for (let step = 0; step <= 240; step += 1) {
        const angle = (step / 240) * Math.PI * 2;
        const radius = baseRadius + ring * 28 + Math.sin(angle * (2 + ring) + time * (ring + 1)) * 18;
        const offset = time * (ring + 1) * 0.55;
        const x = Math.cos(angle + offset) * radius;
        const y = Math.sin(angle - offset) * radius;

        if (step === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }
      ctx.closePath();
      ctx.stroke();
    }

    for (let arc = 0; arc < 3; arc += 1) {
      const t = time + arc * 1.9;
      ctx.strokeStyle = palette[(arc + 1) % palette.length];
      ctx.globalAlpha = 0.25;
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      for (let step = 0; step <= 120; step += 1) {
        const angle = (step / 120) * Math.PI * 2;
        const radius = baseRadius * 1.6 + Math.cos(angle * 2 + t) * 14;
        const x = Math.cos(angle + t * 0.1) * radius;
        const y = Math.sin(angle - t * 0.1) * radius;
        if (step === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.stroke();
    }

    ctx.restore();

    // Performance tracking
    frameCount++;
    if (currentTime - lastTime >= 1000) {
      fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
      frameCount = 0;
      lastTime = currentTime;
      // Log FPS every second
      console.log(`Sporograph FPS: ${fps}`);
    }

    frame += 1;
    requestAnimationFrame(draw);
  };

  resize();
  requestAnimationFrame(draw);
  window.addEventListener('resize', () => {
    resize();
  });
}
