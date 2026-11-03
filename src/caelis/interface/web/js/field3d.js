/**
 * CAELIS // 3D Anti-Gravity Field Visualizer (Three.js WebGL Engine)
 * Renders levitating anti-gravity reactor core, graviton flux matrix, force bubble, and vector lines.
 */

class CaelisField3D {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.controls = null;

    // Objects
    this.coreMesh = null;
    this.ringGroup = null;
    this.particleSystem = null;
    this.bubbleMesh = null;
    this.vectorArrowGroup = null;

    // Parameters
    this.intensity = 650;
    this.stability = 94.2;
    this.showParticles = true;
    this.showVectors = true;
    this.showBubble = true;

    // State
    this.clock = null;
  }

  init() {
    if (!this.container) return;

    // Check if Three.js is loaded
    if (typeof THREE === 'undefined') {
      this.renderFallback2D();
      return;
    }

    const width = this.container.clientWidth || 600;
    const height = this.container.clientHeight || 400;

    // 1. Scene Setup
    this.scene = new THREE.Scene();
    this.scene.fog = new THREE.FogExp2(0x040810, 0.03);

    // 2. Camera Setup
    this.camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    this.camera.position.set(0, 8, 18);

    // 3. Renderer Setup
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setSize(width, height);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.container.appendChild(this.renderer.domElement);

    // 4. OrbitControls
    if (typeof THREE.OrbitControls !== 'undefined') {
      this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
      this.controls.enableDamping = true;
      this.controls.dampingFactor = 0.05;
      this.controls.maxDistance = 35;
      this.controls.minDistance = 5;
    }

    // 5. Lighting
    const ambientLight = new THREE.AmbientLight(0x00f0ff, 0.4);
    this.scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x00f0ff, 2, 50);
    pointLight.position.set(0, 0, 0);
    this.scene.add(pointLight);

    const dirLight = new THREE.DirectionalLight(0xff0055, 1.2);
    dirLight.position.set(10, 15, 10);
    this.scene.add(dirLight);

    // 6. Build Core Reactor
    this.buildCore();

    // 7. Build Containment Rings
    this.buildRings();

    // 8. Build Graviton Particle Matrix
    this.buildParticles();

    // 9. Build Force Bubble Mesh
    this.buildForceBubble();

    // 10. Build Vector Lines
    this.buildVectorArrows();

    // 11. Handle Window Resize
    window.addEventListener('resize', () => this.onWindowResize());

    this.clock = new THREE.Clock();
    this.animate();
  }

  buildCore() {
    // Inner Glowing Core Reactor Geometry
    const coreGeo = new THREE.IcosahedronGeometry(1.6, 2);
    const coreMat = new THREE.MeshStandardMaterial({
      color: 0x00f0ff,
      emissive: 0x0077aa,
      roughness: 0.2,
      metalness: 0.8,
      wireframe: false,
    });
    this.coreMesh = new THREE.Mesh(coreGeo, coreMat);
    this.scene.add(this.coreMesh);

    // Core Outer Wireframe Shell
    const wireGeo = new THREE.IcosahedronGeometry(1.9, 1);
    const wireMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      wireframe: true,
      transparent: true,
      opacity: 0.4,
    });
    const wireMesh = new THREE.Mesh(wireGeo, wireMat);
    this.coreMesh.add(wireMesh);
  }

  buildRings() {
    this.ringGroup = new THREE.Group();
    const ringColors = [0x00f0ff, 0xff0055, 0xffaa00];
    const ringRadii = [2.8, 3.4, 4.0];

    for (let i = 0; i < 3; i++) {
      const ringGeo = new THREE.TorusGeometry(ringRadii[i], 0.06, 16, 100);
      const ringMat = new THREE.MeshStandardMaterial({
        color: ringColors[i],
        emissive: ringColors[i],
        emissiveIntensity: 0.6,
        roughness: 0.1,
      });
      const ringMesh = new THREE.Mesh(ringGeo, ringMat);
      ringMesh.rotation.x = Math.PI / (i + 1.5);
      ringMesh.rotation.y = (i * Math.PI) / 3;
      this.ringGroup.add(ringMesh);
    }
    this.scene.add(this.ringGroup);
  }

  buildParticles() {
    const particleCount = 1200;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const baseColor = new THREE.Color(0x00f0ff);

    for (let i = 0; i < particleCount; i++) {
      // Cylinder / Sphere distribution around center
      const radius = 2 + Math.random() * 6;
      const theta = Math.random() * Math.PI * 2;
      const y = (Math.random() - 0.5) * 12;

      positions[i * 3] = Math.cos(theta) * radius;
      positions[i * 3 + 1] = y;
      positions[i * 3 + 2] = Math.sin(theta) * radius;

      colors[i * 3] = baseColor.r;
      colors[i * 3 + 1] = baseColor.g;
      colors[i * 3 + 2] = baseColor.b;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const particleMat = new THREE.PointsMaterial({
      size: 0.15,
      vertexColors: true,
      transparent: true,
      opacity: 0.75,
      blending: THREE.AdditiveBlending,
    });

    this.particleSystem = new THREE.Points(geometry, particleMat);
    this.scene.add(this.particleSystem);
  }

  buildForceBubble() {
    const bubbleGeo = new THREE.SphereGeometry(5.2, 32, 32);
    const bubbleMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      wireframe: true,
      transparent: true,
      opacity: 0.18,
    });
    this.bubbleMesh = new THREE.Mesh(bubbleGeo, bubbleMat);
    this.scene.add(this.bubbleMesh);
  }

  buildVectorArrows() {
    this.vectorArrowGroup = new THREE.Group();

    // Central Upward Thrust Arrow
    const dir = new THREE.Vector3(0, 1, 0);
    const origin = new THREE.Vector3(0, 0, 0);
    const arrow = new THREE.ArrowHelper(dir, origin, 4.5, 0x00ff9d, 0.8, 0.5);
    this.vectorArrowGroup.add(arrow);

    this.scene.add(this.vectorArrowGroup);
  }

  updateMetrics(intensity, stability) {
    this.intensity = intensity;
    this.stability = stability;

    // Reactively change colors if unstable or overloaded
    if (this.coreMesh) {
      if (this.stability < 40) {
        this.coreMesh.material.color.setHex(0xff0055);
        this.coreMesh.material.emissive.setHex(0xaa0022);
      } else if (this.intensity > 850) {
        this.coreMesh.material.color.setHex(0xffaa00);
        this.coreMesh.material.emissive.setHex(0x995500);
      } else {
        this.coreMesh.material.color.setHex(0x00f0ff);
        this.coreMesh.material.emissive.setHex(0x0077aa);
      }
    }

    // Scale force bubble based on field intensity
    if (this.bubbleMesh) {
      const scaleFactor = 0.7 + (intensity / 1000) * 0.8;
      this.bubbleMesh.scale.set(scaleFactor, scaleFactor, scaleFactor);
    }
  }

  toggleLayer(layerName, state) {
    if (layerName === 'particles' && this.particleSystem) {
      this.particleSystem.visible = state;
    } else if (layerName === 'vectors' && this.vectorArrowGroup) {
      this.vectorArrowGroup.visible = state;
    } else if (layerName === 'bubble' && this.bubbleMesh) {
      this.bubbleMesh.visible = state;
    }
  }

  resetCamera() {
    if (this.camera) {
      this.camera.position.set(0, 8, 18);
      if (this.controls) this.controls.reset();
    }
  }

  onWindowResize() {
    if (!this.container || !this.renderer || !this.camera) return;
    const width = this.container.clientWidth;
    const height = this.container.clientHeight;
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }

  animate() {
    requestAnimationFrame(() => this.animate());

    const delta = this.clock ? this.clock.getDelta() : 0.016;
    const time = this.clock ? this.clock.getElapsedTime() : Date.now() * 0.001;

    // Rotate Core
    if (this.coreMesh) {
      this.coreMesh.rotation.y += 0.01 * (this.intensity / 500);
      this.coreMesh.rotation.x += 0.005;

      // Pulsing scale
      const pulse = 1.0 + Math.sin(time * 4) * 0.04;
      this.coreMesh.scale.set(pulse, pulse, pulse);
    }

    // Orbit Rings
    if (this.ringGroup) {
      this.ringGroup.children.forEach((ring, idx) => {
        ring.rotation.z += (0.01 + idx * 0.005) * (this.intensity / 400);
        ring.rotation.y += 0.008;
      });
    }

    // Particle Swirl
    if (this.particleSystem) {
      this.particleSystem.rotation.y += 0.005 * (this.intensity / 400);
      const positions = this.particleSystem.geometry.attributes.position.array;

      for (let i = 0; i < positions.length / 3; i++) {
        positions[i * 3 + 1] += 0.02 * (this.intensity / 500);
        if (positions[i * 3 + 1] > 6) {
          positions[i * 3 + 1] = -6;
        }
      }
      this.particleSystem.geometry.attributes.position.needsUpdate = true;
    }

    // Force Bubble Rotation
    if (this.bubbleMesh) {
      this.bubbleMesh.rotation.y -= 0.002;
    }

    if (this.controls) {
      this.controls.update();
    }

    if (this.renderer && this.scene && this.camera) {
      this.renderer.render(this.scene, this.camera);
    }
  }

  // Fallback 2D Canvas in case Three.js is not accessible
  renderFallback2D() {
    this.container.innerHTML = `
      <canvas id="fallback-3d-canvas" width="600" height="400" style="width:100%; height:100%;"></canvas>
    `;
    const canvas = document.getElementById('fallback-3d-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let angle = 0;
    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const cx = canvas.width / 2;
      const cy = canvas.height / 2;

      // Outer rings
      ctx.save();
      ctx.translate(cx, cy);

      for (let i = 1; i <= 4; i++) {
        ctx.strokeStyle = i % 2 === 0 ? '#00f0ff' : '#ff0055';
        ctx.lineWidth = 2;
        ctx.shadowColor = ctx.strokeStyle;
        ctx.shadowBlur = 10;
        ctx.beginPath();
        ctx.ellipse(0, 0, 50 * i, 20 * i, angle * (i % 2 === 0 ? 1 : -1), 0, Math.PI * 2);
        ctx.stroke();
      }

      // Core
      ctx.fillStyle = '#00f0ff';
      ctx.shadowColor = '#00f0ff';
      ctx.shadowBlur = 20;
      ctx.beginPath();
      ctx.arc(0, 0, 25 + Math.sin(angle * 3) * 3, 0, Math.PI * 2);
      ctx.fill();

      ctx.restore();

      angle += 0.02;
      requestAnimationFrame(draw);
    };
    draw();
  }
}

window.caelisField3D = CaelisField3D;
