export function latLonToPercent(lat, lon) {
  const x = (lon + 180) / 360 * 100;
  const yFull = (90 - lat) / 180 * 100;
  const y = yFull * 0.10;
  return [ x, y ];
}