#!/bin/bash

# OSS 117 Soundboard Launcher
# This script starts a local web server and opens the soundboard in your browser

PORT=8000
URL="http://localhost:$PORT/soundboard.html"

echo "🎬 Démarrage du soundboard OSS 117..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if port is already in use
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Le port $PORT est déjà utilisé."
    echo "   Le serveur est probablement déjà lancé."
    echo ""
    echo "🌐 Ouverture de $URL"
    xdg-open "$URL" 2>/dev/null || sensible-browser "$URL" 2>/dev/null || firefox "$URL" 2>/dev/null || google-chrome "$URL" 2>/dev/null
    exit 0
fi

# Start Python HTTP server in background
echo "🚀 Démarrage du serveur web sur le port $PORT..."
python3 -m http.server $PORT > /dev/null 2>&1 &
SERVER_PID=$!

# Wait a moment for server to start
sleep 1

# Check if server started successfully
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "❌ Erreur: Impossible de démarrer le serveur"
    exit 1
fi

echo "✅ Serveur démarré (PID: $SERVER_PID)"
echo ""
echo "🌐 Ouverture de $URL"
echo ""

# Open browser (try multiple commands for compatibility)
xdg-open "$URL" 2>/dev/null || sensible-browser "$URL" 2>/dev/null || firefox "$URL" 2>/dev/null || google-chrome "$URL" 2>/dev/null

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 Le serveur tourne en arrière-plan"
echo "   URL: $URL"
echo ""
echo "Pour arrêter le serveur:"
echo "   kill $SERVER_PID"
echo ""
echo "Ou utilisez: pkill -f 'python3 -m http.server $PORT'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Keep script running to show server is active
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur..."
wait $SERVER_PID
