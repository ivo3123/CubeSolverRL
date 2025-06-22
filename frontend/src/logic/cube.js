// Speffz -> index -> color value
export function mapSpeffzToFlat(faceMap) {
  const faceOrder = ['U', 'L', 'F', 'R', 'B', 'D']
  const flat = []
  faceOrder.forEach(face => {
    const facelets = faceMap.get(face)
    facelets.forEach(c => {
      flat.push(charToColorIndex[c])
    })
  })
  return flat
}

export const charToColorIndex = {
  'w': 0,
  'b': 1,
  'r': 2,
  'y': 3,
  'g': 4,
  'o': 5
}

export const colorMap = {
  0: '#F8F8F8',  // white
  1: '#009DFF',  // blue
  2: '#FF0000',  // red
  3: '#FFFF00',  // yellow
  4: '#00FF00',  // green
  5: '#FFA500'   // orange
}