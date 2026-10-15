document.addEventListener("DOMContentLoaded", () => {
  const weather = document.getElementById("weather");
  if (weather) {
    navigator.geolocation.getCurrentPosition(
      (pos) => loadWeather(pos.coords.latitude, pos.coords.longitude),
      () => loadWeather(12.9716, 77.5946),
    );
  }
  const chat = document.getElementById("chatForm");
  if (chat)
    chat.addEventListener("submit", async (event) => {
      event.preventDefault();
      const input = document.getElementById("chatQuestion"),
        messages = document.getElementById("chatMessages"),
        question = input.value.trim();
      if (!question) return;
      messages.insertAdjacentHTML(
        "beforeend",
        `<p class="user">${escapeHtml(question)}</p>`,
      );
      input.value = "";
      try {
        const r = await fetch("/api/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN,
          },
          body: JSON.stringify({ question }),
        });
        const data = await r.json();
        messages.insertAdjacentHTML(
          "beforeend",
          `<p class="bot">${escapeHtml(data.answer || data.error)}</p>`,
        );
      } catch {
        messages.insertAdjacentHTML(
          "beforeend",
          '<p class="bot">Connection problem. Please try again.</p>',
        );
      }
      messages.scrollTop = messages.scrollHeight;
    });
  const search = document.getElementById("vendorSearch");
  if (search)
    search.addEventListener("input", () =>
      document
        .querySelectorAll(".vendor")
        .forEach(
          (x) =>
            (x.hidden = !x.dataset.search.includes(search.value.toLowerCase())),
        ),
    );
});
async function loadWeather(lat, lon) {
  const area = document.getElementById("weather");
  try {
    const r = await fetch(`/api/weather?lat=${lat}&lon=${lon}`),
      d = await r.json();
    if (d.error) throw Error(d.error);
    const c = d.current,
      days = d.daily;
    area.innerHTML = `<div class="col-md-5"><div class="display-5">${Math.round(c.temperature_2m)}°C</div><b>${c.label}</b><p>Humidity ${c.relative_humidity_2m}% · Wind ${c.wind_speed_10m} km/h</p></div><div class="col-md-7"><canvas id="weatherChart"></canvas></div>`;
    new Chart(document.getElementById("weatherChart"), {
      type: "line",
      data: {
        labels: days.time,
        datasets: [
          {
            label: "High °C",
            data: days.temperature_2m_max,
            borderColor: "#4b9560",
            tension: 0.35,
          },
          {
            label: "Rain chance %",
            data: days.precipitation_probability_max,
            borderColor: "#5191cc",
            tension: 0.35,
          },
        ],
      },
      options: { responsive: true },
    });
  } catch (e) {
    area.innerHTML = `<div class="col text-warning">${escapeHtml(e.message)}</div>`;
  }
}
function initVendorMap() {
    if (!window.VENDORS) return;

    const m = L.map("vendorMap");

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "© OpenStreetMap",
    }).addTo(m);

    navigator.geolocation.getCurrentPosition(
        (position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            m.setView([lat, lon], 13);

            L.marker([lat, lon])
                .addTo(m)
                .bindPopup("<b>📍 Your Location</b>")
                .openPopup();

            VENDORS.forEach((v) => {
                L.marker([v[5], v[4]])
                    .addTo(m)
                    .bindPopup(
                        `<b>${escapeHtml(v[0])}</b><br>
                        ${escapeHtml(v[1])}<br>
                        ${escapeHtml(v[2])}`
                    );
            });
        },
        () => {
            // If location permission fails
            m.setView([12.9716, 77.5946], 11);

            VENDORS.forEach((v) => {
                L.marker([v[5], v[4]])
                    .addTo(m)
                    .bindPopup(
                        `<b>${escapeHtml(v[0])}</b><br>
                        ${escapeHtml(v[1])}<br>
                        ${escapeHtml(v[2])}`
                    );
            });
        }
    );
}

function escapeHtml(v) {
    const d = document.createElement("div");
    d.textContent = v;
    return d.innerHTML;
}
