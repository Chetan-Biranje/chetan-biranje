import * as THREE from "three";

const canvas = document.getElementById("bg");
const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x070b14, 0.032);
const camera = new THREE.PerspectiveCamera(50, 1, 0.1, 200);
const STEP = 16, STOPS = 4;                       // distance between scenes along -z, number of scenes
const BLUE = 0x4c9aff, LIGHT = 0x9ccbff;

const lineMat = (o = 0.4) => new THREE.LineBasicMaterial({ color: BLUE, transparent: true, opacity: o });
const dotMat = (s = 0.07) => new THREE.PointsMaterial({ color: LIGHT, size: s });

// ---- scene 0: network sphere
function networkSphere(N = 150, R = 3) {
  const ga = Math.PI * (3 - Math.sqrt(5)), pts = [];
  for (let i = 0; i < N; i++) {
    const y = 1 - 2 * (i + 0.5) / N, r = Math.sqrt(1 - y * y);
    pts.push(new THREE.Vector3(Math.cos(ga * i) * r, y, Math.sin(ga * i) * r).multiplyScalar(R));
  }
  const seg = [], seen = new Set();
  pts.forEach((a, i) => pts.map((b, j) => [a.distanceToSquared(b), j]).sort((x, y) => x[0] - y[0]).slice(1, 4)
    .forEach(([, j]) => { const k = Math.min(i, j) + "-" + Math.max(i, j); if (!seen.has(k)) { seen.add(k); seg.push(a, pts[j]); } }));
  const g = new THREE.Group();
  g.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(seg), lineMat(0.35)));
  g.add(new THREE.Points(new THREE.BufferGeometry().setFromPoints(pts), dotMat()));
  return g;
}
// ---- scene 1: focus areas, a wireframe torus knot with orbiting rings
function knot() {
  const g = new THREE.Group();
  const geo = new THREE.TorusKnotGeometry(1.9, 0.5, 220, 18);
  g.add(new THREE.LineSegments(new THREE.WireframeGeometry(geo), lineMat(0.22)));
  g.add(new THREE.Points(geo, dotMat(0.045)));
  for (let i = 0; i < 2; i++) {
    const ring = new THREE.Mesh(new THREE.TorusGeometry(3.2 + i * 0.6, 0.012, 8, 160), new THREE.MeshBasicMaterial({ color: BLUE, transparent: true, opacity: 0.5 }));
    ring.rotation.x = Math.PI / 2.4 + i * 0.5; ring.userData.spin = 0.15 + i * 0.1; g.add(ring);
  }
  return g;
}
// ---- scene 2: projects, three solids (one per repo)
function solids() {
  const g = new THREE.Group();
  [new THREE.IcosahedronGeometry(1.5, 1), new THREE.OctahedronGeometry(1.5, 1), new THREE.BoxGeometry(2.2, 2.2, 2.2, 3, 3, 3)].forEach((geo, i) => {
    const m = new THREE.Group();
    m.add(new THREE.LineSegments(new THREE.WireframeGeometry(geo), lineMat(0.55)));
    m.add(new THREE.Points(geo, dotMat(0.06)));
    m.position.set((i - 1) * 2.7 + 0.6, Math.sin(i * 2) * 0.8, -i * 1.2);
    m.userData.phase = i; g.add(m);
  });
  return g;
}
// ---- scene 3: contact, expanding ripple rings
function ripples() {
  const g = new THREE.Group();
  for (let i = 0; i < 5; i++) {
    const r = new THREE.Mesh(new THREE.RingGeometry(1, 1.02, 96), new THREE.MeshBasicMaterial({ color: BLUE, transparent: true, side: THREE.DoubleSide }));
    r.userData.offset = i / 5; g.add(r);
  }
  g.add(new THREE.Points(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3()]), dotMat(0.25)));
  return g;
}

const objs = [networkSphere(), knot(), solids(), ripples()];
objs.forEach((o, i) => { o.position.z = -i * STEP; scene.add(o); });

const dust = [];
for (let i = 0; i < 700; i++) dust.push(new THREE.Vector3((Math.random() - 0.5) * 40, (Math.random() - 0.4) * 20, 12 - Math.random() * (STEP * STOPS + 20)));
scene.add(new THREE.Points(new THREE.BufferGeometry().setFromPoints(dust), new THREE.PointsMaterial({ color: 0x6fa8f0, size: 0.04, transparent: true, opacity: 0.55 })));

const grid = new THREE.GridHelper(300, 300, BLUE, 0x1f3b66);
grid.position.set(0, -4.2, -STEP * 1.5);
grid.material.transparent = true; grid.material.opacity = 0.4;
scene.add(grid);

let narrow = false;
function resize() {
  const w = innerWidth, h = innerHeight;
  renderer.setSize(w, h, false);
  camera.aspect = w / h; narrow = w < 800;
  objs.forEach((o) => { o.position.x = narrow ? 0 : 3.9; o.position.y = narrow ? 2.4 : 0.4; o.scale.setScalar(narrow ? 0.6 : 0.9); });
  camera.updateProjectionMatrix();
}
addEventListener("resize", resize); resize();

let mx = 0, my = 0, target = 0, prog = 0;
addEventListener("pointermove", (e) => { mx = e.clientX / innerWidth - 0.5; my = e.clientY / innerHeight - 0.5; });
function readScroll() { const m = document.documentElement.scrollHeight - innerHeight; target = m > 0 ? scrollY / m : 0; }
addEventListener("scroll", readScroll, { passive: true }); readScroll();
const bar = document.getElementById("bar");

let t0 = performance.now(), run = true;
document.addEventListener("visibilitychange", () => { run = !document.hidden; if (run) { t0 = performance.now(); loop(); } });

function frame(now) {
  const s = (now - t0) / 1000;
  prog += (target - prog) * (reduce ? 1 : 0.06);
  const z = 9 - prog * STEP * (STOPS - 1);
  camera.position.set(mx * 1.6, 1.2 - my * 1.0, z);
  camera.lookAt(mx * 0.8, 0.4, z - 9);
  objs[0].rotation.y = s * 0.12; objs[0].rotation.x = 0.25;
  objs[1].rotation.y = s * 0.2; objs[1].rotation.x = s * 0.08;
  objs[1].children.forEach((c) => { if (c.userData.spin) c.rotation.z = s * c.userData.spin; });
  objs[2].children.forEach((c) => { c.rotation.y = s * 0.3 + c.userData.phase; c.rotation.x = s * 0.15; c.position.y = Math.sin(s * 0.8 + c.userData.phase * 2) * 0.5; });
  objs[3].children.forEach((c) => {
    if (!c.userData.offset && c.userData.offset !== 0) return;
    const k = (s * 0.18 + c.userData.offset) % 1;
    c.scale.setScalar(0.5 + k * 6); c.material.opacity = (1 - k) * 0.6; c.rotation.x = Math.PI / 2.6;
  });
  if (bar) bar.style.transform = `scaleX(${prog})`;
  renderer.render(scene, camera);
}
function loop() { if (!run) return; frame(performance.now()); if (!reduce) requestAnimationFrame(loop); }
loop();
if (reduce) addEventListener("scroll", () => frame(performance.now()), { passive: true });

// ---- 3D tilt on cards and chips (CSS perspective)
if (!reduce && matchMedia("(hover:hover)").matches) {
  document.querySelectorAll("[data-tilt]").forEach((el) => {
    el.addEventListener("pointermove", (e) => {
      const r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
      el.style.transform = `perspective(700px) rotateY(${x * 14}deg) rotateX(${-y * 14}deg) translateZ(12px)`;
    });
    el.addEventListener("pointerleave", () => { el.style.transform = ""; });
  });
}
// reveal on scroll
const io = new IntersectionObserver((es) => es.forEach((e) => e.isIntersecting && e.target.classList.add("in")), { threshold: 0.25 });
document.querySelectorAll(".panel").forEach((p) => io.observe(p));
