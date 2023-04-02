# Network Scanner

A simple and efficient network scanner built using Python, PyQt5, and the ping3 library. The application allows users to input a CIDR (Classless Inter-Domain Routing) notation and scans the entire network to find alive hosts.

## Features

- User-friendly GUI for entering CIDR notation
- Displays alive hosts in the network with their respective RTTs (Round-Trip Time)
- Concurrent scanning using threads for faster results
- Progress bar to visualize the scanning progress

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Steps

1. Clone the repository or download the source code.

```
git clone https://github.com/solariscodes/network_scanner.git
```

2. Navigate to the project directory.

```
cd network_scanner
```

3. Install the required dependencies using `pip`.

```
pip install -r requirements.txt
```

4. Run the application.

```
python app.py
```

## Usage

1. Launch the application.
2. Enter the desired CIDR notation (e.g., `192.168.1.0`) in the input field.
3. Click the "Scan Network" button.
4. The application will display alive hosts in the network along with their RTTs.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
