// API client for the Rubik's Cube Solver backend
class CubeSolverAPI {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
    }

    async healthCheck() {
        try {
            const response = await fetch(`${this.baseURL}/health`);
            return await response.json();
        } catch (error) {
            console.error('Health check failed:', error);
            throw error;
        }
    }

    async generateScramble(moves = 20) {
        try {
            const response = await fetch(`${this.baseURL}/scramble?moves=${moves}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Failed to generate scramble:', error);
            throw error;
        }
    }

    async solveCube(cubeState = null, maxMoves = 100) {
        try {
            const requestBody = {
                cube_state: cubeState,
                max_moves: maxMoves
            };

            const response = await fetch(`${this.baseURL}/solve`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Failed to solve cube:', error);
            throw error;
        }
    }

    async getModelInfo() {
        try {
            const response = await fetch(`${this.baseURL}/model-info`);
            return await response.json();
        } catch (error) {
            console.error('Failed to get model info:', error);
            throw error;
        }
    }
}

// Example usage:
/*
const api = new CubeSolverAPI();

// Check if API is healthy
api.healthCheck().then(health => {
    console.log('API Health:', health);
});

// Generate a scramble
api.generateScramble(15).then(scramble => {
    console.log('Scramble:', scramble.scramble);
    console.log('Cube state:', scramble.cube_state);
});

// Solve a cube (with random scramble)
api.solveCube().then(solution => {
    if (solution.success) {
        console.log('Solution found!');
        console.log('Moves:', solution.moves);
        console.log('Move count:', solution.move_count);
    } else {
        console.log('Could not solve:', solution.message);
    }
});

// Get model information
api.getModelInfo().then(info => {
    console.log('Model info:', info);
});
*/

export default CubeSolverAPI;
