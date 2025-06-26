# CubeSolverRL

A reinforcement learning project for solving Rubik's cubes, featuring a trained DQN agent, web API, and interactive frontend.

## 🎯 Project Overview

This project combines deep reinforcement learning with web technologies to create a complete Rubik's cube solving system:

- **🧠 RL Agent**: Deep Q-Network (DQN) trained to solve Rubik's cubes
- **🚀 FastAPI Backend**: REST API for cube solving
- **🎨 Vue.js Frontend**: Interactive 3D cube visualization with Three.js
- **📊 Training Analytics**: Comprehensive training data and performance metrics

## 🏗️ Project Structure

```
CubeSolverRL/
├── backend/
│   ├── agent/              # DQN Agent implementation
│   ├── cube/               # Cube logic and utilities
│   ├── cube_env/           # Gymnasium environment
│   ├── models/             # Trained models (.pt files)
│   └── docs/               # Training documentation
├── frontend/               # Vue.js + Three.js frontend
│   ├── src/
│   │   └── components/     # Vue components
│   └── package.json
└── README.md
```

## 🚀 Quick Start

### 1. Backend API

```bash
cd backend/

uv install

uvicorn api:app --reload
```

### 2. Frontend

```bash
cd frontend/

npm install

npm run dev
```

## 📊 Training Analytics

The `backend/docs/` directory contains detailed training analytics:

- Training curves and metrics
- Performance visualizations
- Model comparison studies
- Hyperparameter analysis

## 📚 References

- [Deep Q-Learning](https://arxiv.org/abs/1312.5602)
- [Gymnasium Documentation](https://gymnasium.farama.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue.js Documentation](https://vuejs.org/)
- [Three.js Documentation](https://threejs.org/)
