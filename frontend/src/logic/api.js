const BASE_URL = 'http://localhost:8000'

//I have not tested this one yet

export async function resetCube() {
  const res = await fetch(`${BASE_URL}/reset`, { method: 'POST' })
  return await res.json()
}

export async function stepCube(action) {
  const res = await fetch(`${BASE_URL}/step`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action })
  })
  return await res.json()
}

export async function getCubeState() {
  const res = await fetch(`${BASE_URL}/state`)
  return await res.json()
}