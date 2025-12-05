#!/usr/bin/env python3

def normalize_crs(crs_input):
    if crs_input is None:
        return "EPSG:4326"
    crs_str = str(crs_input).strip()
    if crs_str.startswith("EPSG:"):
        return crs_str
    if crs_str.startswith("ESPG"):
        code = crs_str[4:]
        return f"EPSG:{code}"
    if crs_str.startswith("epsg:"):
        return crs_str.upper()
    if crs_str.isdigit():
        return f"EPSG:{crs_str}"
    return "EPSG:4326"

print("Testando normalização de CRS:")
print("ESPG4326 ->", normalize_crs("ESPG4326"))
print("EPSG:4326 ->", normalize_crs("EPSG:4326"))
print("4326 ->", normalize_crs("4326"))
print("epsg:4326 ->", normalize_crs("epsg:4326"))
print("EPSG4326 ->", normalize_crs("EPSG4326"))

