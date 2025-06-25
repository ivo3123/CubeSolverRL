# Rubik's Cube Solver API

A FastAPI-based REST API that provides endpoints for solving Rubik's cubes using a trained reinforcement learning agent.

## Features

- **Cube Scrambling**: Generate random scrambles for testing
- **Cube Solving**: Solve cubes using the trained DQN agent
- **Health Monitoring**: Check API and model status
- **CORS Enabled**: Ready for frontend integration
- **Auto Documentation**: Swagger UI available at `/docs`

## Setup

### 1. Install Dependencies

```bash
cd backend/api
pip install -r requirements.txt
```

### 2. Ensure Model is Available

Make sure you have a trained model in one of these locations:
- `backend/models/model_edges_first_layer.pt`
- `backend/models/1_edges_first_layer.pt`
- `backend/saved_models/edges_first_layer/model_*.pt` (latest will be used)

### 3. Start the API

**Windows:**
```bash
start_api.bat
```

**Linux/Mac:**
```bash
chmod +x start_api.sh
./start_api.sh
```

**Manual:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

## API Endpoints

### Health Check
- **GET** `/` - Basic health check
- **GET** `/health` - Detailed health status

### Cube Operations
- **POST** `/scramble?moves=20` - Generate a scrambled cube
- **POST** `/solve` - Solve a cube using the RL agent
- **GET** `/model-info` - Get information about the loaded model

## Request/Response Examples

### Generate Scramble

**Request:**
```bash
curl -X POST "http://localhost:8000/scramble?moves=15"
```

**Response:**
```json
{
    "scramble": ["R", "U'", "D2", "L", "F'"],
    "cube_state": [0, 1, 2, 3, 4, 5, ...]
}
```

### Solve Cube

**Request:**
```bash
curl -X POST "http://localhost:8000/solve" \
     -H "Content-Type: application/json" \
     -d '{
         "cube_state": null,
         "max_moves": 100
     }'
```

**Response:**
```json
{
    "success": true,
    "moves": ["R", "U", "R'", "U'"],
    "move_count": 4,
    "final_state": [0, 0, 0, 0, 0, 0, ...],
    "message": "Cube solved in 4 moves!"
}
```

## Frontend Integration

The API is configured with CORS to work with:
- Vite dev server: `http://localhost:5173`
- Standard dev server: `http://localhost:3000`

### JavaScript Client

```javascript
import CubeSolverAPI from './api/cubeApi.js';

const api = new CubeSolverAPI();

// Generate scramble
const scramble = await api.generateScramble(20);
console.log('Scramble moves:', scramble.scramble);

// Solve cube
const solution = await api.solveCube();
if (solution.success) {
    console.log('Solution:', solution.moves);
}
```

## Development

### Project Structure

```
backend/
├── api/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # API dependencies
│   ├── start_api.bat       # Windows startup script
│   └── start_api.sh        # Unix startup script
├── agent/
│   ├── agent.py            # DQN Agent
│   └── network.py          # Neural network
├── cube/
│   ├── cube.py             # Cube logic
│   ├── enums.py            # Enums and constants
│   └── ...
└── models/                 # Trained models
```

### Adding New Endpoints

1. Define Pydantic models for request/response
2. Add endpoint function with proper typing
3. Handle errors with HTTPException
4. Update this README

### Error Handling

The API uses standard HTTP status codes:
- `200`: Success
- `404`: Not found
- `422`: Validation error
- `500`: Internal server error

## Troubleshooting

### Model Not Found
Ensure you have trained a model and it's in the correct location:
```bash
python backend/train/edges_first_layer.py
```

### Import Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### CORS Issues
Update the allowed origins in `main.py` if using different ports:
```python
allow_origins=["http://localhost:YOUR_PORT"]
```

## Performance Notes

- The API loads the model on startup for better response times
- Use `--workers 1` for uvicorn to avoid model loading issues
- For production, consider using gunicorn with uvicorn workers

## Next Steps

1. **Authentication**: Add API key authentication for production
2. **Rate Limiting**: Implement rate limiting for solve requests
3. **Caching**: Cache solved states for faster responses
4. **WebSockets**: Add real-time solving progress updates
5. **Model Management**: Hot-swapping of different models
