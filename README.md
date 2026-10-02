# PC Shutdown Timer

A simple Windows desktop application that lets you schedule a PC shutdown with a visible countdown.

## Features

- Set hours, minutes, and seconds.
- Start a Windows shutdown countdown.
- See the remaining time in the app.
- Cancel the scheduled shutdown at any time.
- Uses Windows' built-in `shutdown` command.
- No external Python packages are required.

## Run

Install Python 3 on Windows, then run:

```powershell
python shutdown_timer.py
```

## Build a standalone EXE

If you want an EXE that does not require Python:

```powershell
pip install pyinstaller
pyinstaller --onefile --windowed --name PC-Shutdown-Timer shutdown_timer.py
```

The EXE will be created in the `dist` folder.

## How it works

When you press **Start Shutdown**, the app runs Windows:

```
shutdown /s /t <seconds>
```

When you press **Cancel Shutdown**, it runs:

```
shutdown /a
```

The app does not shut down immediately; it schedules the shutdown for the countdown you selected.
