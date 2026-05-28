import { createCanvas } from 'canvas';
import fs from 'fs';

const WIDTH = 1200;
const HEIGHT = 630;

// Neon palette colors
const colors = {
  background: '#0a0e27',
  grid: '#1a1f3a',
  gridAccent: '#252b4a',
  neonCyan: '#00f5ff',
  neonBlue: '#4d7cff',
  neonPurple: '#b14eff',
  neonGreen: '#00ff88',
  neonPink: '#ff6b9d',
  neonOrange: '#ff9f43',
  text: '#ffffff',
  textMuted: '#8892b0'
};

function drawBlueprintGrid(ctx) {
  ctx.strokeStyle = colors.grid;
  ctx.lineWidth = 0.5;
  
  const gridSize = 20;
  
  for (let x = 0; x <= WIDTH; x += gridSize) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, HEIGHT);
    ctx.stroke();
  }
  
  for (let y = 0; y <= HEIGHT; y += gridSize) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(WIDTH, y);
    ctx.stroke();
  }
  
  ctx.strokeStyle = colors.gridAccent;
  ctx.lineWidth = 1;
  
  for (let x = 0; x <= WIDTH; x += 100) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, HEIGHT);
    ctx.stroke();
  }
  
  for (let y = 0; y <= HEIGHT; y += 100) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(WIDTH, y);
    ctx.stroke();
  }
}

function drawRoundedRect(ctx, x, y, width, height, radius, fill, stroke = null) {
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.lineTo(x + width - radius, y);
  ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
  ctx.lineTo(x + width, y + height - radius);
  ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
  ctx.lineTo(x + radius, y + height);
  ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
  ctx.lineTo(x, y + radius);
  ctx.quadraticCurveTo(x, y, x + radius, y);
  ctx.closePath();
  
  if (fill) {
    ctx.fillStyle = fill;
    ctx.fill();
  }
  
  if (stroke) {
    ctx.strokeStyle = stroke;
    ctx.lineWidth = 2;
    ctx.stroke();
  }
}

function drawArrow(ctx, x1, y1, x2, y2, color, label = null) {
  const headLen = 15;
  const angle = Math.atan2(y2 - y1, x2 - x1);
  
  ctx.save();
  ctx.shadowColor = color;
  ctx.shadowBlur = 15;
  
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.strokeStyle = color;
  ctx.lineWidth = 3;
  ctx.stroke();
  
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - headLen * Math.cos(angle - Math.PI / 6), y2 - headLen * Math.sin(angle - Math.PI / 6));
  ctx.lineTo(x2 - headLen * Math.cos(angle + Math.PI / 6), y2 - headLen * Math.sin(angle + Math.PI / 6));
  ctx.closePath();
  ctx.fillStyle = color;
  ctx.fill();
  
  ctx.restore();
  
  if (label) {
    ctx.fillStyle = colors.text;
    ctx.font = 'bold 12px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(label, (x1 + x2) / 2, (y1 + y2) / 2 - 18);
  }
}

function generateHeroImage() {
  const canvas = createCanvas(WIDTH, HEIGHT);
  const ctx = canvas.getContext('2d');
  
  // Background
  ctx.fillStyle = colors.background;
  ctx.fillRect(0, 0, WIDTH, HEIGHT);
  
  // Blueprint grid
  drawBlueprintGrid(ctx);
  
  // Title
  ctx.fillStyle = colors.neonCyan;
  ctx.font = 'bold 52px Arial';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'top';
  ctx.fillText('OpenCLI', WIDTH / 2, 35);
  
  ctx.fillStyle = colors.text;
  ctx.font = '26px Arial';
  ctx.fillText('把网站变成 CLI 命令', WIDTH / 2, 95);
  
  // Flowchart boxes
  const boxWidth = 180;
  const boxHeight = 90;
  const boxY = 200;
  
  // 1. Website box
  ctx.save();
  ctx.shadowColor = colors.neonBlue;
  ctx.shadowBlur = 20;
  drawRoundedRect(ctx, 80, boxY, boxWidth, boxHeight, 12, colors.background, colors.neonBlue);
  ctx.restore();
  
  ctx.fillStyle = colors.neonBlue;
  ctx.font = 'bold 22px Arial';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('网站', 80 + boxWidth / 2, boxY + 30);
  ctx.fillStyle = colors.textMuted;
  ctx.font = '14px Arial';
  ctx.fillText('Website', 80 + boxWidth / 2, boxY + 55);
  
  // Draw globe icon
  ctx.strokeStyle = colors.neonBlue;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(80 + boxWidth / 2, boxY + boxHeight - 20, 12, 0, Math.PI * 2);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(80 + boxWidth / 2 - 12, boxY + boxHeight - 20);
  ctx.lineTo(80 + boxWidth / 2 + 12, boxY + boxHeight - 20);
  ctx.stroke();
  
  // 2. OpenCLI box (center)
  const centerWidth = 220;
  const centerHeight = 120;
  const centerX = WIDTH / 2 - centerWidth / 2;
  
  ctx.save();
  ctx.shadowColor = colors.neonCyan;
  ctx.shadowBlur = 30;
  drawRoundedRect(ctx, centerX, boxY - 15, centerWidth, centerHeight, 15, colors.background, colors.neonCyan);
  ctx.restore();
  
  ctx.fillStyle = colors.neonCyan;
  ctx.font = 'bold 28px Arial';
  ctx.textAlign = 'center';
  ctx.fillText('OpenCLI', WIDTH / 2, boxY + 25);
  
  ctx.fillStyle = colors.neonGreen;
  ctx.font = 'bold 18px Arial';
  ctx.fillText('100+ Adapters', WIDTH / 2, boxY + 55);
  
  ctx.fillStyle = colors.textMuted;
  ctx.font = '14px Arial';
  ctx.fillText('Browser → CLI', WIDTH / 2, boxY + 80);
  
  // 3. CLI output box
  ctx.save();
  ctx.shadowColor = colors.neonGreen;
  ctx.shadowBlur = 20;
  drawRoundedRect(ctx, WIDTH - 260, boxY, boxWidth, boxHeight, 12, colors.background, colors.neonGreen);
  ctx.restore();
  
  ctx.fillStyle = colors.neonGreen;
  ctx.font = 'bold 22px Arial';
  ctx.fillText('CLI 命令', WIDTH - 260 + boxWidth / 2, boxY + 30);
  ctx.fillStyle = colors.textMuted;
  ctx.font = '14px Arial';
  ctx.fillText('Command Line', WIDTH - 260 + boxWidth / 2, boxY + 55);
  
  // Draw terminal icon
  ctx.strokeStyle = colors.neonGreen;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(WIDTH - 260 + boxWidth / 2 - 15, boxY + boxHeight - 25);
  ctx.lineTo(WIDTH - 260 + boxWidth / 2 - 5, boxY + boxHeight - 18);
  ctx.lineTo(WIDTH - 260 + boxWidth / 2 - 15, boxY + boxHeight - 11);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(WIDTH - 260 + boxWidth / 2 - 3, boxY + boxHeight - 18);
  ctx.lineTo(WIDTH - 260 + boxWidth / 2 + 15, boxY + boxHeight - 18);
  ctx.stroke();
  
  // Arrows
  drawArrow(ctx, 80 + boxWidth + 10, boxY + boxHeight / 2, centerX - 10, boxY + boxHeight / 2 - 15, colors.neonPurple, 'Browser Extension');
  drawArrow(ctx, centerX + centerWidth + 10, boxY + boxHeight / 2 - 15, WIDTH - 260 - 10, boxY + boxHeight / 2, colors.neonPink, 'Structured Output');
  
  // Example commands section
  const exampleY = 390;
  ctx.fillStyle = colors.text;
  ctx.font = 'bold 16px Arial';
  ctx.textAlign = 'center';
  ctx.fillText('示例命令 Example Commands', WIDTH / 2, exampleY);
  
  const examples = [
    { cmd: '$ opencli hackernews top', color: colors.neonOrange },
    { cmd: '$ opencli bilibili hot', color: colors.neonPurple },
    { cmd: '$ opencli zhihu hot', color: colors.neonBlue },
  ];
  
  let exampleX = 100;
  examples.forEach((ex, i) => {
    drawRoundedRect(ctx, exampleX, exampleY + 20, 320, 40, 6, colors.background, ex.color + '50');
    
    ctx.fillStyle = ex.color;
    ctx.font = '15px monospace';
    ctx.textAlign = 'left';
    ctx.fillText(ex.cmd, exampleX + 15, exampleY + 46);
    
    exampleX += 340;
  });
  
  // Bottom text
  ctx.fillStyle = colors.textMuted;
  ctx.font = '14px Arial';
  ctx.textAlign = 'center';
  ctx.fillText('让 AI Agent 操作你已登录的浏览器', WIDTH / 2, HEIGHT - 60);
  ctx.fillStyle = colors.neonCyan;
  ctx.fillText('github.com/jackwener/opencli', WIDTH / 2, HEIGHT - 35);
  
  // Corner decorations
  ctx.strokeStyle = colors.neonCyan + '60';
  ctx.lineWidth = 2;
  
  // Top left
  ctx.beginPath();
  ctx.moveTo(20, 50);
  ctx.lineTo(20, 20);
  ctx.lineTo(50, 20);
  ctx.stroke();
  
  // Top right
  ctx.beginPath();
  ctx.moveTo(WIDTH - 20, 50);
  ctx.lineTo(WIDTH - 20, 20);
  ctx.lineTo(WIDTH - 50, 20);
  ctx.stroke();
  
  // Bottom left
  ctx.beginPath();
  ctx.moveTo(20, HEIGHT - 50);
  ctx.lineTo(20, HEIGHT - 20);
  ctx.lineTo(50, HEIGHT - 20);
  ctx.stroke();
  
  // Bottom right
  ctx.beginPath();
  ctx.moveTo(WIDTH - 20, HEIGHT - 50);
  ctx.lineTo(WIDTH - 20, HEIGHT - 20);
  ctx.lineTo(WIDTH - 50, HEIGHT - 20);
  ctx.stroke();
  
  // Save to PNG first
  const outputPath = process.argv[2] || './src/assets/opencli-hero.webp';
  const buffer = canvas.toBuffer('image/png');
  fs.writeFileSync(outputPath.replace('.webp', '.png'), buffer);
  console.log(`Generated PNG: ${outputPath.replace('.webp', '.png')}`);
  console.log(`Size: ${WIDTH}x${HEIGHT}`);
}

generateHeroImage();