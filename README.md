# Universal Clipboard

A cross-platform clipboard synchronization tool that allows seamless sharing of clipboard content between Windows and macOS devices.

![Universal Clipboard Demo](docs/demo.gif)

## Features

- 🔄 Real-time clipboard synchronization
- 🔒 End-to-end encryption
- 🖼️ Support for text and images
- 🚀 Background service operation
- 🔌 Automatic device discovery
- 🔄 Bidirectional sync

## Project Structure

```
cross_clipboard/
├── windows_client/     # Windows client application
├── mac_client/         # macOS client application
├── shared/             # Shared utilities and protocols
└── server/             # Optional relay server
```

## Requirements

### Windows Client
- Python 3.8+
- pywin32
- cryptography
- websockets

### macOS Client
- Python 3.8+
- pyobjc
- cryptography
- websockets

## Installation

### Windows
1. Download the latest release from the [Releases](https://github.com/yourusername/universal-clipboard/releases) page
2. Run `install.bat` as Administrator
3. The service will automatically start and run in the background

### macOS
```bash
pip install universal-clipboard[mac]
```

## Usage

1. Start the application on both devices
2. The devices will automatically discover each other on the same network
3. Copy and paste as usual - content will sync automatically

## Development

### Prerequisites
- Python 3.8+
- pip

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/universal-clipboard.git
cd universal-clipboard

# Install development dependencies
pip install -e ".[dev]"
```

### Building Windows Executable
```bash
cd windows_client
python setup.py build
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Security

- All clipboard data is encrypted using AES-256
- Communication is secured with WebSocket over TLS
- No data is stored permanently
- Device pairing requires manual confirmation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [websockets](https://github.com/aaugustin/websockets) for the WebSocket implementation
- [cryptography](https://github.com/pyca/cryptography) for the encryption library
- [pywin32](https://github.com/mhammond/pywin32) for Windows integration
- [pyobjc](https://github.com/ronaldoussoren/pyobjc) for macOS integration 