# CubeSolverRL

A reinforcement learning project for solving Rubik's cubes, featuring a trained DQN agent, web API, and interactive frontend.

## 🎯 Project Overview

This project combines deep reinforcement learning with web technologies to create a complete Rubik's cube solving system:

- **🧠 RL Agent**: Deep Q-Network (DQN) trained to solve Rubik's cubes
- **🚀 FastAPI Backend**: REST API for cube solving and scrambling
- **🎨 Vue.js Frontend**: Interactive 3D cube visualization with Three.js
- **📊 Training Analytics**: Comprehensive training data and performance metrics

## 🏗️ Project Structure

```
CubeSolverRL/
├── backend/
│   ├── api/                 # FastAPI REST API
│   │   ├── main.py         # API server
│   │   ├── requirements.txt # API dependencies
│   │   └── README.md       # API documentation
│   ├── agent/              # DQN Agent implementation
│   ├── cube/               # Cube logic and utilities
│   ├── cube_env/           # Gymnasium environment
│   ├── train/              # Training scripts
│   ├── models/             # Trained models
│   └── docs/               # Training documentation
├── frontend/               # Vue.js + Three.js frontend
│   ├── src/
│   │   ├── api/           # API client
│   │   └── components/    # Vue components
│   └── package.json
└── README.md
```

## 🚀 Quick Start

### 1. Backend API

```bash
# Navigate to API directory
cd backend/api

# Install dependencies
pip install -r requirements.txt

# Start the API server
# Windows:
start_api.bat
# Unix:
./start_api.sh

# API available at: http://localhost:8000
# Documentation at: http://localhost:8000/docs
```

### 2. Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Frontend available at: http://localhost:5173
```

## 🎮 Usage

### API Endpoints

- `POST /scramble` - Generate a scrambled cube
- `POST /solve` - Solve a cube using the trained agent
- `GET /health` - Check API status
- `GET /model-info` - Get model information

### Example API Usage

```javascript
import CubeSolverAPI from './api/cubeApi.js';

const api = new CubeSolverAPI();

// Generate a scramble
const scramble = await api.generateScramble(20);
console.log('Scramble:', scramble.scramble);

// Solve the cube
const solution = await api.solveCube();
if (solution.success) {
    console.log('Solution found!');
    console.log('Moves:', solution.moves);
    console.log('Move count:', solution.move_count);
}
```

## 🧠 Machine Learning

### Training the Agent

The project uses a Deep Q-Network (DQN) to learn cube solving strategies:

```bash
cd backend
python train/edges_first_layer.py
```

### Model Architecture

- **Input**: 54-dimensional cube state (flattened)
- **Output**: 18 possible actions (6 faces × 3 rotations)
- **Network**: Multi-layer perceptron with ReLU activations
- **Training**: DQN with experience replay and target networks

### Performance

Current models achieve:
- **Success Rate**: High percentage of cubes solved
- **Average Moves**: Competitive with optimal solutions
- **Training Time**: Efficient convergence

## 📊 Training Analytics

The `backend/docs/` directory contains detailed training analytics:
- Training curves and metrics
- Performance visualizations
- Model comparison studies
- Hyperparameter analysis

## 🛠️ Development

### Backend Development

```bash
cd backend

# Install development dependencies
pip install -r requirements.txt

# Run training
python train/edges_first_layer.py

# Test the environment
python -m cube_env.env

# Start API in development mode
cd api
uvicorn main:app --reload
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server with hot reload
npm run dev

# Build for production
npm run build
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
MODEL_PATH=models/model_edges_first_layer.pt
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Model Configuration

Training parameters can be adjusted in the training scripts:

```python
# Training hyperparameters
LEARNING_RATE = 0.001
GAMMA = 0.99
EPSILON_START = 1.0
EPSILON_END = 0.01
EPSILON_DECAY = 0.995
BATCH_SIZE = 32
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Future Enhancements

- [ ] **Multi-Phase Solving**: Implement complete cube solving pipeline
- [ ] **Real-time Visualization**: WebSocket-based solving animation
- [ ] **Model Comparison**: A/B testing interface for different models
- [ ] **Mobile App**: React Native or Flutter mobile application
- [ ] **Cloud Deployment**: Docker containerization and cloud hosting
- [ ] **Advanced Algorithms**: Integration with traditional solving methods

## 📚 References

- [Deep Q-Learning](https://arxiv.org/abs/1312.5602)
- [Gymnasium Documentation](https://gymnasium.farama.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue.js Documentation](https://vuejs.org/)
- [Three.js Documentation](https://threejs.org/)