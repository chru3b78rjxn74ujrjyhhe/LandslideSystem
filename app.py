from flask import Flask, render_template, jsonify
import random, time

app = Flask(__name__)

# --- Helpers to produce fake series data ---
def now_label():
    return time.strftime("%H:%M:%S")

def make_timeseries(length=40, low=0, high=100, jitter=5, start=None):
    """Return labels and values for a timeseries (length points)."""
    vals = []
    labels = []
    base = random.uniform(low, high)
    for i in range(length):
        base += random.uniform(-jitter, jitter)
        base = max(low, min(high, base))
        vals.append(round(base, 2))
        labels.append(now_label())
        time.sleep(0 if i==length-1 else 0)  # no delay, but keeps code simple
    return labels, vals

# --- API endpoints returning "latest" + "series" for graphs ---
@app.route("/")
def combined():
    return render_template("index.html", title="Combined Dashboard")

@app.route("/landslide")
def landslide():
    return render_template("landslide.html", title="Landslide Dashboard")

@app.route("/flood")
def flood():
    return render_template("flood.html", title="Flood Dashboard")

@app.route("/camera")
def camera():
    return render_template("camera.html", title="Camera")

@app.route("/api/landslide")
def api_landslide():
    # Soil moisture values typically 200-900 (simulate sensor ADC)
    labels = []
    soil1 = []
    soil2 = []
    tilt = []
    vibration = []
    rain = []
    for i in range(40):
        labels.append(now_label())
        soil1.append(random.randint(200, 900))
        soil2.append(random.randint(200, 900))
        tilt.append(round(random.uniform(-8, 8), 2))
        vibration.append(random.randint(0, 10))  # counts or magnitude
        rain.append(random.choice([0,0,0,1]))  # mostly no rain
    # landslide danger calculation (fake): more danger if soil high + tilt + vibration
    last_soil = (soil1[-1] + soil2[-1]) / 2
    last_tilt = abs(tilt[-1])
    last_vib = vibration[-1]
    landslide_score = int(min(100, ( (last_soil-200)/7 + last_tilt*6 + last_vib*5 )))
    return jsonify({
        "labels": labels,
        "soil1": soil1,
        "soil2": soil2,
        "tilt": tilt,
        "vibration": vibration,
        "rain": rain,
        "landslide_danger": landslide_score
    })

@app.route("/api/flood")
def api_flood():
    labels = []
    water_level = []
    rain_intensity = []
    soil_sat = []
    for i in range(40):
        labels.append(now_label())
        water_level.append(round(random.uniform(10, 120), 2))  # cm
        rain_intensity.append(random.randint(0, 100))
        soil_sat.append(random.randint(200, 900))
    # flood danger: high water level + rainfall + saturation
    last_water = water_level[-1]
    last_rain = rain_intensity[-1]
    last_sat = soil_sat[-1]
    flood_score = int(min(100, last_water/1.5 + last_rain*0.3 + (last_sat-200)/7))
    return jsonify({
        "labels": labels,
        "water_level": water_level,
        "rain_intensity": rain_intensity,
        "soil_sat": soil_sat,
        "flood_danger": flood_score
    })

@app.route("/api/combined")
def api_combined():
    # combine the two endpoints in a simple fused way
    import math
    ls = api_landslide().json
    fl = api_flood().json
    # last scores
    ls_score = ls["landslide_danger"]
    fl_score = fl["flood_danger"]
    combined_score = int(min(100, (ls_score*0.6 + fl_score*0.6)/1.2))
    return jsonify({
        "landslide": ls_score,
        "flood": fl_score,
        "combined": combined_score,
        "timestamp": now_label()
    })

@app.route("/api/notifications")
def api_notifications():
    sample = [
        {"msg": "System initialized", "time": now_label()},
        {"msg": "Fake dataset refreshed", "time": now_label()},
    ]
    # Randomly inject warnings
    if random.random() > 0.85:
        sample.append({"msg": "Warning: High tilt detected", "time": now_label()})
    if random.random() > 0.92:
        sample.append({"msg": "Alert: Rapid water level rise", "time": now_label()})
    return jsonify(sample)

if __name__ == "__main__":
    app.run(debug=True)
