@echo off
cd /d "%~dp0"
title Rosalind Bio Solver

:menu
cls
echo ================================
echo     Rosalind Bio Solver
echo ================================
echo.
echo 1. Bio Solver (opens in browser)
echo 2. DNA Analyzer (type sequence)
echo 3. Exit
echo.
set /p choice=Input number (1-3): 

if "%choice%"=="1" goto run1
if "%choice%"=="2" goto run2
if "%choice%"=="3" exit
goto menu

:run1
cls
echo Opening Bio Solver in browser...
python -m streamlit run rosalind_bio_solver.py
goto menu

:run2
cls
echo === DNA Analyzer ===
set /p seq=Enter DNA sequence (e.g. ATCGATCG): 
python rosalind_dna_analyzer.py --seq %seq%
echo.
pause
goto menu