# Track_expenses_telegram_bot
You need to create a .bat file and paste there this commands.(After # is a comemnts)


@echo off

call %~dp0 # You need to apply you way to venv (ex: .\venv\Scripts\activate)

cd %~dp0 # You need to apply you way to dir where you bot is(ex: Progs\PyBOT\)

set TOKEN= # Here you need to set your telegram bot token

python bot_telegram.py # and run you python file

pause
