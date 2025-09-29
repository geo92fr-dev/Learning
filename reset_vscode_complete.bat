@echo off
echo RESET COMPLET VS CODE - Elimination fichiers fantomes
echo.

echo Fermeture forcée VS Code...
taskkill /F /IM "Code.exe" 2>nul

echo Attente 3 secondes...
timeout /t 3 /nobreak >nul

echo Nettoyage cache extensions...
python force_clean_vscode_cache.py

echo Suppression workspace storage...
rd /S /Q "%APPDATA%\Code\User\workspaceStorage" 2>nul

echo Reset diagnostics...
rd /S /Q "%APPDATA%\Code\logs" 2>nul

echo.
echo ✅ RESET TERMINÉ
echo Redémarrez VS Code maintenant
echo.
pause
