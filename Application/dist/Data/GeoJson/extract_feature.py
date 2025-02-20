import json

feat = dict()
countries_geo = json.load(open("countries.json"))
for feature in countries_geo["features"]:
    if feature["properties"]["ISO_A3"] == "RUS":
        feat = feature
        feat["properties"]["CONTINENT"] = feature["properties"]["ADMIN"]
        break

with open("feature.json", "w") as f:
    json.dump(feat, f, indent=4)