@echo off
REM Script de génération rapide d'un cours HTML accessible
REM Usage: double-cliquer (le fichier exemple_fractions.md doit être présent)

SET SRC=exemple_fractions.md
SET DRIVE_CONF=drive_path.txt
SET TPL=template_base.html
SET SHARE_URL=https://drive.google.com/drive/folders/1wn1ZwfpWlJAOo10Y-P65z-UbxBve6rwR?usp=drive_link

REM Permettre de passer un fichier source en argument : generer_cours.bat mon_cours.md
IF NOT "%~1"=="" (
  IF EXIST "%~1" (
    SET SRC=%~1
  ) ELSE (
    echo Argument fourni introuvable: %~1
    echo Utilisation: generer_cours.bat [fichier_markdown]
    pause
    exit /b 1
  )
)

REM Horodatage pour éviter l'ecrasement (utilise PowerShell)
for /f %%i in ('powershell -NoProfile -Command "(Get-Date).ToString('yyyyMMdd_HHmmss')"') do set TS=%%i
SET OUT=cours_%TS%.html

IF NOT EXIST %SRC% (
  echo Source %SRC% introuvable. Placez votre fichier markdown dans ce dossier.
  pause
  exit /b 1
)

IF NOT EXIST %TPL% (
  echo Template %TPL% introuvable.
  pause
  exit /b 1
)

where python >nul 2>&1
IF ERRORLEVEL 1 (
  echo Python non detecte. Installez Python depuis https://www.python.org/downloads/
  pause
  exit /b 1
)

python generate_course_page.py %SRC% -o %OUT% -t %TPL%
IF ERRORLEVEL 1 (
  echo Erreur lors de la generation.
  pause
  exit /b 1
)

echo Fichier genere: %OUT%

IF EXIST %DRIVE_CONF% (
  for /f "usebackq delims=" %%D in ("%DRIVE_CONF%") do set DRIVE_TARGET=%%D
  echo Dossier Drive cible lu: %DRIVE_TARGET%
  if NOT EXIST "%DRIVE_TARGET%" (
    echo Le dossier cible n'existe pas encore. Creation...
    mkdir "%DRIVE_TARGET%" >nul 2>&1
  )
  copy /Y "%OUT%" "%DRIVE_TARGET%" >nul 2>&1
  if ERRORLEVEL 1 (
    echo Echec de la copie vers le dossier Drive.
  ) else (
    echo Copie OK vers: %DRIVE_TARGET%\%OUT%
    REM Generation de l'index dans le dossier cible si build_index.py present
    if EXIST build_index.py (
       echo Generation de l'index parent...
       pushd "%DRIVE_TARGET%"
       python "%~dp0build_index.py" --dir . --output College_4ieme_Maths.html >nul 2>&1
       popd
       if EXIST "%DRIVE_TARGET%\College_4ieme_Maths.html" (
         echo Index mis a jour: College_4ieme_Maths.html
       ) else (
         echo Echec generation index (verifiez Python et droits ecriture).
       )
    )
  )
) ELSE (
  echo Fichier drive_path.txt introuvable. Skipping copie Drive.
)

start "" %OUT%
echo Ouverture du dossier Drive dans le navigateur (si partage web actif)...
start "" %SHARE_URL%
echo Terminé. Appuyez sur une touche pour fermer.
pause >nul
