import * as THREE from "three";

const canvas = document.getElementById("bg");
const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x070b14, 0.055);
const camera = new THREE.PerspectiveCamera(50, 1, 0.1, 100);
camera.position.set(0, 1.2, 9);

// network sphere: Fibonacci nodes linked to nearest neighbours
const N = 150, R = 3.2, ga = Math.PI * (3 - Math.sqrt(5));
const pts = [];
for (let i = 0; i < N; i++) {
  const y = 1 - 2 * (i + 0.5) / N, r = Math.sqrt(1 - y * y);
  pts.push(new THREE.Vector3(Math.cos(ga * i) * r, y, Math.sin(ga * i) * r).multiplyScalar(R));
}
const seg = [], seen = new Set();
pts.forEach((a, i) => {
  pts.map((b, j) => [a.distanceToSquared(b), j]).sort((x, y) => x[0] - y[0]).slice(1, 4).forEach(([, j]) => {
    const k = Math.min(i, j) + "-" + Math.max(i, j);
    if (!seen.has(k)) { seen.add(k); seg.push(a, pts[j]); }
  });
});
const net = new THREE.Group();
net.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(seg),
  new THREE.LineBasicMaterial({ color: 0x4c9aff, transparent: true, opacity: 0.35 })));
net.add(new THREE.Points(new THREE.BufferGeometry().setFromPoints(pts),
  new THREE.PointsMaterial({ color: 0x9ccbff, size: 0.07, sizeAttenuation: true })));
// inner core + drifting particles for depth
const dust = [];
for (let i = 0; i < 260; i++) dust.push(new THREE.Vector3((Math.random() - 0.5) * 26, (Math.random() - 0.3) * 12, (Math.random() - 0.7) * 20));
const dustPts = new THREE.Points(new THREE.BufferGeometry().setFromPoints(dust),
  new THREE.PointsMaterial({ color: 0x6fa8f0, size: 0.04, transparent: true, opacity: 0.6 }));
net.position.set(3.4, 0.6, 0);
scene.add(net, dustPts);

const grid = new THREE.GridHelper(80, 80, 0x4c9aff, 0x1f3b66);
grid.position.y = -3.6;
grid.material.transparent = true; grid.material.opacity = 0.5;
scene.add(grid);

function resize() {
  const w = innerWidth, h = innerHeight;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  // on narrow screens, centre the sphere behind the text
  net.position.x = w < 800 ? 0 : 2.9;
  net.scale.setScalar(w < 800 ? 0.62 : 0.92);
  net.position.y = w < 800 ? 2.2 : 0.6;
  camera.updateProjectionMatrix();
}
addEventListener("resize", resize); resize();

let mx = 0, my = 0;
addEventListener("pointermove", (e) => { mx = e.clientX / innerWidth - 0.5; my = e.clientY / innerHeight - 0.5; });
let t0 = performance.now(), run = true;
document.addEventListener("visibilitychange", () => { run = !document.hidden; if (run) { t0 = performance.now(); loop(); } });

function frame(t) {
  const s = (t - t0) / 1000;
  net.rotation.y = s * 0.12; net.rotation.x = 0.25;
  dustPts.rotation.y = s * 0.01;
  grid.position.z = (s * 0.8) % 1;                    // grid glides toward the viewer
  camera.position.x += (mx * 1.6 - camera.position.x) * 0.04;
  camera.position.y += (1.2 - my * 1.0 - camera.position.y) * 0.04;
  camera.lookAt(0, 0.4, 0);
  renderer.render(scene, camera);
}
function loop() { if (!run) return; frame(performance.now()); if (!reduce) requestAnimationFrame(loop); }
loop();
