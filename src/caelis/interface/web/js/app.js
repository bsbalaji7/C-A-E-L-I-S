/**
 * CAELIS // Main Application Controller
 * Wires UI controls, 3D WebGL field, physics loop, radar, voice AI, audio SFX, and system logger.
 */

class CaelisApp {
  constructor() {
    this.physics = window.caelisPhysics;
    this.field3D = null;
    this.radar = null;
    this.audio = window.caelisAudio;
    this.voice = window.caelisVoice;

    this.timer = null;
  }

  init() {
    console.log("C.A.E.L.I.S. HUD Application initializing...");

    // 1. Init 3D Visualizer
    this.field3D = new CaelisField3D('canvas-3d-container');
    this.field3D.init();

    // 2. Init 2D Radar Scope
    this.radar = new CaelisRadar('radar-canvas');
    this.radar.init();

    // 3. Init Voice AI
    this.voice.init();

    // 4. Bind UI Event Listeners
    this.bindEvents();

    // 5. Start Main Telemetry Loop (20Hz)
    this.timer = setInterval(() => this.tick(), 50);

    // 6. Start continuous anti-gravity audio hum
    setTimeout(() => {
      if (this.audio) this.audio.startEngineHum();
    }, 1000);

    this.log("CAELIS Quantum Flux Matrix Online. All sub-systems operational.", "success");
  }

  bindEvents() {
    // Audio Toggle
    const btnAudio = document.getElementById('btn-sound-toggle');
    if (btnAudio) {
      btnAudio.addEventListener('click', () => {
        const state = this.audio.toggleSound();
        btnAudio.innerHTML = state ? `<span class="icon">🔊</span> AUDIO: ON` : `<span class="icon">🔇</span> AUDIO: OFF`;
        this.log(`Audio SFX ${state ? 'ENABLED' : 'MUTED'}`, 'info');
      });
    }

    // Simulation Mode Toggle
    const btnSim = document.getElementById('btn-sim-mode');
    if (btnSim) {
      btnSim.addEventListener('click', () => {
        const simState = this.physics.toggleSimulationMode();
        btnSim.classList.toggle('active', simState);
        btnSim.innerHTML = simState ? `<span class="icon">🎮</span> SIMULATION: ON` : `<span class="icon">🎮</span> SIMULATION: OFF`;
        
        const badgeMode = document.getElementById('val-mode');
        if (badgeMode) badgeMode.textContent = simState ? 'VIRTUAL SIMULATION' : 'TELEMETRY LIVE';

        const physOverlay = document.getElementById('overlay-physics-mode');
        if (physOverlay) physOverlay.textContent = simState ? 'PHYSICS: VIRTUAL SIMULATION' : 'PHYSICS: NORMAL TELEMETRY';

        this.log(`Switched operating mode to ${simState ? 'VIRTUAL SIMULATION' : 'TELEMETRY LIVE'}`, 'warning');
        this.audio.playClick();
      });
    }

    // Emergency Stop
    const btnEStop = document.getElementById('btn-emergency-stop');
    if (btnEStop) {
      btnEStop.addEventListener('click', () => {
        this.physics.emergencyStop();
        this.audio.playWarningAlarm();
        this.log("⚠️ EMERGENCY FIELD BRAKE ACTIVATED! Field intensity zeroed.", "danger");
      });
    }

    // Slider Field Intensity
    const slider = document.getElementById('slider-intensity');
    if (slider) {
      slider.addEventListener('input', (e) => {
        const val = parseInt(e.target.value, 10);
        this.physics.setIntensity(val);
        document.getElementById('slider-intensity-disp').textContent = `${val} %`;
        this.audio.updateHumPitch(val);
      });
    }

    // Power Quick Buttons
    document.getElementById('btn-inc-5')?.addEventListener('click', () => this.adjustPower(5));
    document.getElementById('btn-inc-20')?.addEventListener('click', () => this.adjustPower(20));
    document.getElementById('btn-dec-5')?.addEventListener('click', () => this.adjustPower(-5));
    document.getElementById('btn-dec-20')?.addEventListener('click', () => this.adjustPower(-20));

    // Stabilize
    document.getElementById('btn-stabilize')?.addEventListener('click', () => {
      this.physics.stabilizeField();
      this.audio.playPowerSweep(true);
      this.log("Field phase lock stabilized to 99.5%", "success");
    });

    // Navigation Controls
    document.getElementById('btn-nav-ascend')?.addEventListener('click', () => {
      this.physics.navMode = 'ASCEND';
      this.audio.playPowerSweep(true);
      this.log("Flight Mode set to: ASCEND", "info");
    });

    document.getElementById('btn-nav-descend')?.addEventListener('click', () => {
      this.physics.navMode = 'DESCEND';
      this.audio.playPowerSweep(false);
      this.log("Flight Mode set to: DESCEND", "info");
    });

    document.getElementById('btn-nav-hover')?.addEventListener('click', () => {
      this.physics.navMode = 'HOVER';
      this.audio.playClick();
      this.log("Flight Mode set to: HOVER (Position Lock)", "success");
    });

    document.getElementById('btn-drift-n')?.addEventListener('click', () => { this.physics.pitch = -5.0; this.log("Drifting North Vector", "info"); });
    document.getElementById('btn-drift-s')?.addEventListener('click', () => { this.physics.pitch = 5.0; this.log("Drifting South Vector", "info"); });
    document.getElementById('btn-drift-e')?.addEventListener('click', () => { this.physics.roll = 5.0; this.log("Drifting East Vector", "info"); });
    document.getElementById('btn-drift-w')?.addEventListener('click', () => { this.physics.roll = -5.0; this.log("Drifting West Vector", "info"); });

    document.getElementById('btn-rot-cw')?.addEventListener('click', () => { this.physics.yaw = (this.physics.yaw + 15) % 360; this.log("Rotating Clockwise +15°", "info"); });
    document.getElementById('btn-rot-ccw')?.addEventListener('click', () => { this.physics.yaw = (this.physics.yaw - 15 + 360) % 360; this.log("Rotating Counter-Clockwise -15°", "info"); });

    // 3D Canvas Layer Toggles
    document.getElementById('chip-particles')?.addEventListener('click', (e) => {
      e.target.classList.toggle('active');
      this.field3D.toggleLayer('particles', e.target.classList.contains('active'));
    });
    document.getElementById('chip-vectors')?.addEventListener('click', (e) => {
      e.target.classList.toggle('active');
      this.field3D.toggleLayer('vectors', e.target.classList.contains('active'));
    });
    document.getElementById('chip-bubble')?.addEventListener('click', (e) => {
      e.target.classList.toggle('active');
      this.field3D.toggleLayer('bubble', e.target.classList.contains('active'));
    });
    document.getElementById('btn-recenter')?.addEventListener('click', () => {
      this.field3D.resetCamera();
    });

    // Simulation parameter buttons
    document.getElementById('btn-inject-turb')?.addEventListener('click', () => {
      this.physics.turbulence += 15;
      this.audio.playWarningAlarm();
      this.log("Injected 15kt wind turbulence into simulation environment!", "warning");
    });
    document.getElementById('btn-overload-test')?.addEventListener('click', () => {
      this.physics.setIntensity(980);
      this.physics.stability = 38.5;
      this.audio.playWarningAlarm();
      this.log("⚠️ FIELD OVERLOAD TEST TRIGGERED! 980% Flux. Stability dropped!", "danger");
    });

    // Voice Mic Button
    const btnMic = document.getElementById('btn-mic-toggle');
    if (btnMic) {
      btnMic.addEventListener('click', () => {
        const listening = this.voice.toggleListening();
        btnMic.classList.toggle('active', listening);
        document.getElementById('voice-state-txt').textContent = listening ? 'LISTENING... (SPEAK COMMAND)' : 'WAKE WORD LISTENING: "CAELIS"';
        this.audio.playClick();
      });
    }

    // Quick Voice Command Simulator Presets
    document.querySelectorAll('.preset-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const cmd = btn.getAttribute('data-cmd');
        if (cmd) {
          this.voice.processCommand(cmd);
        }
      });
    });

    // Clear Logs
    document.getElementById('btn-clear-logs')?.addEventListener('click', () => {
      const logWin = document.getElementById('log-window');
      if (logWin) logWin.innerHTML = '';
    });
  }

  adjustPower(pct) {
    this.physics.adjustIntensity(pct);
    const newIntensity = this.physics.intensity;

    const slider = document.getElementById('slider-intensity');
    if (slider) slider.value = newIntensity;
    document.getElementById('slider-intensity-disp').textContent = `${newIntensity} %`;

    this.audio.playPowerSweep(pct > 0);
    this.audio.updateHumPitch(newIntensity);
    this.log(`Field Intensity adjusted by ${pct > 0 ? '+' : ''}${pct}% (Current: ${newIntensity}%)`, pct > 0 ? "success" : "info");
  }

  executeVoiceIntent(intent, val, text) {
    if (intent === 'EMERGENCY_STOP') {
      this.physics.emergencyStop();
      this.log(`Voice Command execution: EMERGENCY STOP`, "danger");
    } else if (intent === 'STABILIZE_FIELD') {
      this.physics.stabilizeField();
      this.log(`Voice Command execution: STABILIZE FIELD`, "success");
    } else if (intent === 'SET_FIELD_INTENSITY') {
      if (val !== null) this.physics.setIntensity(val);
      this.log(`Voice Command execution: SET INTENSITY (${val || 'default'}%)`, "success");
    } else if (intent === 'INCREASE_POWER') {
      this.adjustPower(15);
      this.log(`Voice Command execution: INCREASE POWER`, "success");
    } else if (intent === 'DECREASE_POWER') {
      this.adjustPower(-15);
      this.log(`Voice Command execution: DECREASE POWER`, "info");
    } else if (intent === 'ASCEND') {
      this.physics.navMode = 'ASCEND';
      this.log(`Voice Command execution: ASCEND`, "success");
    } else if (intent === 'DESCEND') {
      this.physics.navMode = 'DESCEND';
      this.log(`Voice Command execution: DESCEND`, "info");
    } else if (intent === 'NAV_HOVER') {
      this.physics.navMode = 'HOVER';
      this.log(`Voice Command execution: AUTO HOVER`, "success");
    } else if (intent === 'TOGGLE_SIMULATION') {
      this.physics.toggleSimulationMode();
      this.log(`Voice Command execution: TOGGLE SIMULATION`, "warning");
    } else if (intent === 'SYSTEM_STATUS') {
      this.log(`Voice Command execution: SYSTEM STATUS REPORT`, "info");
    }
  }

  // 20Hz Telemetry Tick
  tick() {
    const data = this.physics.update(0.05);

    // Update DOM Metrics
    const gaugeIntensity = document.getElementById('gauge-intensity');
    if (gaugeIntensity) gaugeIntensity.style.width = `${Math.min(100, data.intensity / 10)}%`;
    const numIntensity = document.getElementById('num-intensity');
    if (numIntensity) numIntensity.textContent = data.intensity;

    const gaugeStability = document.getElementById('gauge-stability');
    if (gaugeStability) gaugeStability.style.width = `${data.stability}%`;
    const numStability = document.getElementById('num-stability');
    if (numStability) numStability.textContent = data.stability;

    const numAltitude = document.getElementById('num-altitude');
    if (numAltitude) numAltitude.textContent = data.altitude;

    const numClimbRate = document.getElementById('num-climb-rate');
    if (numClimbRate) numClimbRate.textContent = (data.climbRate >= 0 ? '+' : '') + data.climbRate;

    const numEnergy = document.getElementById('num-energy');
    if (numEnergy) numEnergy.textContent = data.powerGW;

    const numGDist = document.getElementById('num-g-dist');
    if (numGDist) numGDist.textContent = data.gDistortion;

    // Vectors
    document.getElementById('num-pitch').textContent = `${data.pitch}°`;
    document.getElementById('num-roll').textContent = `${data.roll}°`;
    document.getElementById('num-yaw').textContent = `${data.yaw}°`;

    // Battery
    document.getElementById('val-battery-pct').textContent = `${data.battery}%`;
    document.getElementById('battery-fill-bar').style.width = `${data.battery}%`;
    document.getElementById('num-discharge-rate').textContent = data.dischargeRate;

    // Pressure
    document.getElementById('val-pressure').textContent = `${data.pressure} hPa`;

    // 3D Visualizer Sync
    if (this.field3D) {
      this.field3D.updateMetrics(data.intensity, data.stability);
    }

    // Coordinates overlay
    const overlayCoords = document.getElementById('overlay-coordinates');
    if (overlayCoords) {
      overlayCoords.textContent = `X: ${(data.roll * 0.1).toFixed(2)} | Y: ${data.altitude.toFixed(2)} | Z: ${(data.pitch * 0.1).toFixed(2)}`;
    }
  }

  log(msg, type = "info") {
    const logWin = document.getElementById('log-window');
    if (!logWin) return;

    const now = new Date();
    const timeStr = now.toTimeString().split(' ')[0];

    const line = document.createElement('div');
    line.className = `log-line ${type}`;
    line.textContent = `[${timeStr}] ${msg}`;

    logWin.appendChild(line);
    logWin.scrollTop = logWin.scrollHeight;
  }
}

window.addEventListener('DOMContentLoaded', () => {
  window.caelisApp = new CaelisApp();
  window.caelisApp.init();
});
