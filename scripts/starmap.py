#!/usr/bin/env python3
"""Star map generator v2 (starplot 0.20) - zenith chart for a date/place"""
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from starplot import ZenithPlot, Observer, _
from starplot.styles import PlotStyle, extensions

def make(date_str, lat, lon, tz, out):
    dt = datetime.fromisoformat(date_str).replace(tzinfo=ZoneInfo(tz))
    obs = Observer(lat=lat, lon=lon, dt=dt)
    style = PlotStyle().extend(extensions.BLUE_DARK)
    p = ZenithPlot(observer=obs, style=style, resolution=2600, scale=1.0)
    p.constellations()
    p.stars(where=[_.magnitude < 4.6])
    p.planets()
    p.moon(true_size=False)
    p.constellation_labels()
    p.export(out, transparent=True, padding=0.1)
    print("SAVED", out)

if __name__ == "__main__":
    make(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5])
