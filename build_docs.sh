#!/bin/bash
# Script pour construire la documentation Sphinx

echo "🔨 Construction de la documentation Sphinx..."

# Naviguer vers le répertoire docs
cd "$(dirname "$0")/docs" || exit 1

# Nettoyer les fichiers de build précédents
echo "🧹 Nettoyage des fichiers de build précédents..."
rm -rf _build/

# Construire la documentation
echo "📚 Construction de la documentation HTML..."
poetry run sphinx-build -b html . _build/html

if [ $? -eq 0 ]; then
    echo "✅ Documentation construite avec succès!"
    echo "📂 Les fichiers HTML sont disponibles dans docs/_build/html/"
    echo "🌐 Ouvrir avec: xdg-open docs/_build/html/index.html"
else
    echo "❌ Erreur lors de la construction de la documentation"
    exit 1
fi