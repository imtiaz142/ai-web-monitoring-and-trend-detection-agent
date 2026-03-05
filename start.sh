#!/bin/bash
echo ""
echo "  Starting AI Trend Detection Agent..."
echo ""

# Start backend
echo "  Starting backend on http://localhost:8000"
cd backend && python run.py &
BACKEND_PID=$!

# Wait for backend to be ready
sleep 3

# Start frontend
echo "  Starting dashboard on http://localhost:3000"
cd ../frontend && npm run dev &
FRONTEND_PID=$!

echo ""
echo "  Open http://localhost:3000 to view your dashboard"
echo "  API docs at http://localhost:8000/docs"
echo ""
echo "  Press Ctrl+C to stop both services"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
