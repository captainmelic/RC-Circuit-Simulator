# RC Circuit Simulator

A PyQt6-based graphical application for visualizing and simulating RC (Resistor-Capacitor) circuits. This simulator provides an interactive interface to explore how RC circuits charge and discharge.

## Features

- **Interactive Circuit Diagram**: Visual representation of an RC circuit with EMF (voltage source), resistor, capacitor, and switch
- **Real-time Parameter Editing**: 
  - Adjust EMF (Electromotive Force/Voltage): 0-100 V
  - Modify Resistance: 1-10,000 Ω
  - Change Capacitance: 1-10,000 μF
- **Switch Control**: Toggle between OPEN and CLOSED states to control circuit flow
- **Automatic Calculations**: Displays the RC time constant (τ = R × C)
- **Modular Design**: Well-commented, object-oriented code structure for easy extension

## Installation

1. Clone the repository:
```bash
git clone https://github.com/captainmelic/RC-Circuit-Simulator.git
cd RC-Circuit-Simulator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python rc_circuit_simulator.py
```

### Controls

- **EMF (Voltage)**: Set the voltage of the power source
- **Resistance**: Adjust the resistance value
- **Capacitance**: Modify the capacitance value
- **Switch Button**: Click to toggle between OPEN (red) and CLOSED (green)

The circuit diagram updates in real-time as you change parameters, and the time constant is automatically recalculated.

## Project Structure

```
RC-Circuit-Simulator/
├── rc_circuit_simulator.py  # Main application file with GUI components
├── circuit_diagram.py        # Circuit diagram rendering module
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Code Architecture

The application follows a modular, object-oriented design:

- **`MainWindow`**: Main application window that coordinates all components
- **`ParameterPanel`**: Control panel for editing circuit parameters
- **`InfoPanel`**: Information display showing calculated values
- **`CircuitDiagram`**: Widget that renders the circuit schematic

All classes are extensively commented to facilitate easy modification and extension.

## RC Circuit Theory

An RC circuit consists of a resistor (R) and capacitor (C) connected in series. Key characteristics:

- **Time Constant (τ)**: τ = R × C
  - Determines charging/discharging rate
  - At τ: capacitor is ~63.2% charged
  - At 5τ: capacitor is ~99.3% charged (considered fully charged)

## Requirements

- Python 3.7+
- PyQt6 6.6.0+

## License

This project is open source and available for educational purposes.

## Contributing

Contributions are welcome! The modular design makes it easy to:
- Add new circuit components
- Implement charging/discharging animations
- Add voltage/current graphs over time
- Extend calculations and visualizations
