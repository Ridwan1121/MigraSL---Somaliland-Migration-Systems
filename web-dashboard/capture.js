// MigraSL: sawirka ajaanibta kamerada computer-ka laga qaado
(function () {
  let stream = null;

  function make(tag, attrs, text) {
    const e = document.createElement(tag);
    Object.entries(attrs || {}).forEach(([k, v]) => e.setAttribute(k, v));
    if (text) e.textContent = text;
    return e;
  }

  function stopCamera() {
    if (stream) stream.getTracks().forEach(t => t.stop());
    stream = null;
  }

  async function startCamera(video) {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user', width: { ideal: 1280 }, height: { ideal: 720 } },
      audio: false
    });
    video.srcObject = stream;
    await video.play();
  }

  function captureJpeg(video) {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    return new Promise((resolve, reject) => {
      canvas.toBlob(b => (b ? resolve(b) : reject(new Error('Sawirka lama qaadi karo'))), 'image/jpeg', 0.92);
    });
  }

  window.attachWebcamCapture = function (containerId) {
    const box = document.getElementById(containerId);
    if (!box || document.getElementById('camPanel')) return;

    const panel = make('div', { id: 'camPanel', class: 'space-y-2' });
    const openBtn = make('button', { type: 'button', class: 'px-3 py-2 rounded-lg bg-emerald-600 text-white text-xs font-semibold' }, 'Kamera fur');
    const video = make('video', { autoplay: '', playsinline: '', muted: '', class: 'hidden w-64 rounded-lg border border-gray-600' });
    const shootBtn = make('button', { type: 'button', class: 'hidden px-3 py-2 rounded-lg bg-blue-600 text-white text-xs font-semibold' }, 'Qaad sawirka');
    const closeBtn = make('button', { type: 'button', class: 'hidden px-3 py-2 rounded-lg bg-gray-700 text-white text-xs font-semibold' }, 'Xir kamerada');
    const msg = make('div', { class: 'text-xs text-amber-300' });

    function showLive(on) {
      video.classList.toggle('hidden', !on);
      shootBtn.classList.toggle('hidden', !on);
      closeBtn.classList.toggle('hidden', !on);
      openBtn.classList.toggle('hidden', on);
    }

    openBtn.addEventListener('click', async () => {
      msg.textContent = '';
      try {
        await startCamera(video);
        showLive(true);
      } catch (err) {
        msg.textContent = 'Kamerada ma furmi karo: ' + err.message;
      }
    });

    shootBtn.addEventListener('click', async () => {
      try {
        const blob = await captureJpeg(video);
        const file = new File([blob], 'ajaanib_' + Date.now() + '.jpg', { type: 'image/jpeg' });
        const dt = new DataTransfer();
        dt.items.add(file);
        const input = document.getElementById('migraslPhotoInput');
        input.files = dt.files;
        input.dispatchEvent(new Event('change'));
        stopCamera();
        showLive(false);
        msg.textContent = 'Sawirka waa la qaaday. Haddii aad rabto mar kale, "Kamera fur" dib u riix.';
      } catch (err) {
        msg.textContent = 'Qalad: ' + err.message;
      }
    });

    closeBtn.addEventListener('click', () => {
      stopCamera();
      showLive(false);
      msg.textContent = '';
    });

    panel.append(openBtn, video, shootBtn, closeBtn, msg);
    box.appendChild(panel);
  };

  window.addEventListener('beforeunload', stopCamera);
})();
