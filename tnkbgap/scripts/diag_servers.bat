@echo off
REM diag_servers.bat — diagnose why servers aren't binding to 8765 / 8766.
REM Shows: netstat for both ports, tasklist for python.exe, and tries a direct
REM (foreground) launch of each server so you can read any error message.

setlocal
set PY="D:\Github Repos\research-intranet\.venv\Scripts\python.exe"

echo === Port check ===
netstat -ano | findstr ":8765 "
netstat -ano | findstr ":8766 "

echo.
echo === Python processes ===
tasklist /FI "IMAGENAME eq python.exe"

echo.
echo === Direct foreground test (research-intranet) ===
echo Starting research-intranet foreground on 8765 — Ctrl+C in this window to stop.
%PY% -m http.server 8765 --directory "D:\Github Repos\research-intranet\site"
