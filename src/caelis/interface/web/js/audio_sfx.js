/**
 * CAELIS // Web Audio API Procedural Sound Synthesizer
 * Generates futuristic sci-fi audio feedback and dynamic engine hums without external assets.
 */

class CaelisAudioFX {
  constructor() {
    this.enabled = true;
    this.audioCtx = null;
    this.humOsc = null;
    this.humGain = null;
    this.isHumActive = false;
  }

  init() {
    if (!this.audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        this.audioCtx = new AudioContext();
      }
    }
    if (this.audioCtx && this.audioCtx.state === 'suspended') {
      this.audioCtx.resume();
    }
  }

  toggleSound(forceState) {
    this.enabled = forceState !== undefined ? forceState : !this.enabled;
    if (!this.enabled && this.humGain) {
      this.humGain.gain.setValueAtTime(0, this.audioCtx.currentTime);
    }
    return this.enabled;
  }

  // Quick high-tech click chirp
  playClick() {
    if (!this.enabled) return;
    this.init();
    if (!this.audioCtx) return;

    const osc = this.audioCtx.createOscillator();
    const gain = this.audioCtx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(1200, this.audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(400, this.audioCtx.currentTime + 0.05);

    gain.gain.setValueAtTime(0.15, this.audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, this.audioCtx.currentTime + 0.05);

    osc.connect(gain);
    gain.connect(this.audioCtx.destination);

    osc.start();
    osc.stop(this.audioCtx.currentTime + 0.05);
  }

  // Futuristic Voice Wake Chime
  playVoiceChime() {
    if (!this.enabled) return;
    this.init();
    if (!this.audioCtx) return;

    const now = this.audioCtx.currentTime;

    const osc1 = this.audioCtx.createOscillator();
    const osc2 = this.audioCtx.createOscillator();
    const gain = this.audioCtx.createGain();

    osc1.type = 'sine';
    osc2.type = 'triangle';

    osc1.frequency.setValueAtTime(523.25, now); // C5
    osc1.frequency.setValueAtTime(659.25, now + 0.08); // E5
    osc1.frequency.setValueAtTime(783.99, now + 0.16); // G5

    osc2.frequency.setValueAtTime(1046.5, now); // C6
    osc2.frequency.setValueAtTime(1318.5, now + 0.16); // E6

    gain.gain.setValueAtTime(0.2, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);

    osc1.connect(gain);
    osc2.connect(gain);
    gain.connect(this.audioCtx.destination);

    osc1.start(now);
    osc2.start(now);
    osc1.stop(now + 0.4);
    osc2.stop(now + 0.4);
  }

  // Power Increase / Decrease Pitch Sweep
  playPowerSweep(increasing = true) {
    if (!this.enabled) return;
    this.init();
    if (!this.audioCtx) return;

    const now = this.audioCtx.currentTime;
    const osc = this.audioCtx.createOscillator();
    const gain = this.audioCtx.createGain();

    osc.type = 'sawtooth';
    const startFreq = increasing ? 150 : 600;
    const endFreq = increasing ? 600 : 150;

    osc.frequency.setValueAtTime(startFreq, now);
    osc.frequency.exponentialRampToValueAtTime(endFreq, now + 0.25);

    gain.gain.setValueAtTime(0.1, now);
    gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);

    osc.connect(gain);
    gain.connect(this.audioCtx.destination);

    osc.start(now);
    osc.stop(now + 0.25);
  }

  // Emergency Warning Siren Pulse
  playWarningAlarm() {
    if (!this.enabled) return;
    this.init();
    if (!this.audioCtx) return;

    const now = this.audioCtx.currentTime;
    const osc = this.audioCtx.createOscillator();
    const gain = this.audioCtx.createGain();

    osc.type = 'square';
    osc.frequency.setValueAtTime(880, now);
    osc.frequency.setValueAtTime(440, now + 0.1);
    osc.frequency.setValueAtTime(880, now + 0.2);

    gain.gain.setValueAtTime(0.2, now);
    gain.gain.exponentialRampToValueAtTime(0.01, now + 0.35);

    osc.connect(gain);
    gain.connect(this.audioCtx.destination);

    osc.start(now);
    osc.stop(now + 0.35);
  }

  // Start continuous subtle background engine hum
  startEngineHum() {
    if (this.isHumActive || !this.enabled) return;
    this.init();
    if (!this.audioCtx) return;

    try {
      this.humOsc = this.audioCtx.createOscillator();
      this.humGain = this.audioCtx.createGain();

      this.humOsc.type = 'sine';
      this.humOsc.frequency.setValueAtTime(55, this.audioCtx.currentTime); // Low 55Hz base hum

      this.humGain.gain.setValueAtTime(0.03, this.audioCtx.currentTime);

      this.humOsc.connect(this.humGain);
      this.humGain.connect(this.audioCtx.destination);

      this.humOsc.start();
      this.isHumActive = true;
    } catch (e) {
      console.warn("Audio Context hum start notice:", e);
    }
  }

  // Dynamic hum pitch modulation based on field intensity (0 - 1000%)
  updateHumPitch(intensityPct) {
    if (!this.isHumActive || !this.humOsc || !this.audioCtx) return;
    const targetFreq = 55 + (intensityPct * 0.15); // Scale 55Hz to ~205Hz
    this.humOsc.frequency.setTargetAtTime(targetFreq, this.audioCtx.currentTime, 0.1);
  }
}

window.caelisAudio = new CaelisAudioFX();
