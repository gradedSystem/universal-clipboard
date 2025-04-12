# Universal Clipboard for Windows

A background service that syncs your clipboard with Mac devices.

## Installation

1. Download the latest release
2. Run `install.bat` as Administrator
3. The service will automatically start and run in the background

## Features

- Runs as a Windows service (starts automatically with Windows)
- Syncs clipboard content with Mac devices
- Supports text and images
- Secure encrypted communication
- No user interface required

## Managing the Service

You can manage the service through:
1. Windows Services (services.msc)
2. Command Prompt (as Administrator):
   - Start: `UniversalClipboard.exe start`
   - Stop: `UniversalClipboard.exe stop`
   - Restart: `UniversalClipboard.exe restart`
   - Remove: `UniversalClipboard.exe remove`

## Logs

Service logs are stored in:
`C:\ProgramData\UniversalClipboard\service.log`

## Troubleshooting

If the service fails to start:
1. Check the log file for errors
2. Ensure you have the required permissions
3. Verify your network connection
4. Make sure the Mac client is running

## Uninstallation

1. Stop the service: `UniversalClipboard.exe stop`
2. Remove the service: `UniversalClipboard.exe remove`
3. Delete the program files and data directory 