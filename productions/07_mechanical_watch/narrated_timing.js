// Keep the approved composition while aligning its six sections to the supplied take.
const narrationMap = [
  [0, 0], [13.357542, 6], [20.714417, 11.5], [26.670250, 16.5],
  [38.851292, 25], [46.230292, 33], [53, 39.5], [55.5, 42]
];
function remapTime(value, inputIndex) {
  const outputIndex = 1 - inputIndex;
  let index = 0;
  while (index < narrationMap.length - 2 && value >= narrationMap[index + 1][inputIndex]) index++;
  const first = narrationMap[index], last = narrationMap[index + 1];
  const progress = clamp((value - first[inputIndex]) / (last[inputIndex] - first[inputIndex]));
  return first[outputIndex] + progress * (last[outputIndex] - first[outputIndex]);
}
function narrationClock(seconds) {
  if (seconds < 26.670250) return seconds;
  if (seconds < 38.851292) return 26.670250 + (seconds - 26.670250) / 50;
  const slowEnd = 26.670250 + (38.851292 - 26.670250) / 50;
  if (seconds < 46.230292) {
    const elapsed = seconds - 38.851292, duration = 46.230292 - 38.851292;
    return slowEnd + .5 * elapsed + .25 * elapsed * elapsed / duration;
  }
  return slowEnd + .75 * (46.230292 - 38.851292) + seconds - 46.230292;
}
sim = sourceTime => narrationClock(remapTime(sourceTime, 1));
const approvedSeek = OPENER.seek;
OPENER.seek = seconds => {
  const outputTime = clamp(seconds, 0, 55.5);
  approvedSeek(remapTime(outputTime, 0));
  window.watchState.outputTime = outputTime;
};
window.narrationTiming = { map: narrationMap, clock: narrationClock, sourceTime: seconds => remapTime(seconds, 0) };
