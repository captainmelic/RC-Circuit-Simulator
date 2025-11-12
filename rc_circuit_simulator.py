"""
RC Circuit Simulator - Main Application

This is the main application file for the RC Circuit Simulator.
It provides a graphical interface for:
- Viewing an RC circuit diagram
- Editing circuit parameters (EMF, Resistance, Capacitance)
- Controlling the circuit switch (open/close)

The application is built with PyQt6 and uses a modular design for easy
extension and modification.

ARCHITECTURE:
-------------
The application follows a modular, object-oriented design with three main components:

1. ParameterPanel (QGroupBox)
   - Contains all input controls (spinboxes for EMF, R, C, and switch button)
   - Emits 'parameters_changed' signal when any value changes
   - Easy to extend with new parameters

2. InfoPanel (QGroupBox)
   - Displays calculated information about the circuit
   - Currently shows time constant (τ = R × C)
   - Can be extended to show additional calculations

3. CircuitDiagram (QFrame - see circuit_diagram.py)
   - Renders the circuit schematic using QPainter
   - Updates automatically when parameters change
   - Modular drawing methods for each component

4. MainWindow (QMainWindow)
   - Coordinates all components
   - Manages signal/slot connections
   - Main entry point for the application

EXTENDING THE APPLICATION:
--------------------------
To add new features:

- Add new circuit components: Modify CircuitDiagram class in circuit_diagram.py
- Add new parameters: Add controls to ParameterPanel and update signal handlers
- Add calculations: Extend InfoPanel with new computed values
- Add animations: Use QTimer and update circuit parameters over time
- Add graphs: Use matplotlib or PyQtGraph to show voltage/current vs time

Example of adding a new parameter:
1. Add a spinbox in ParameterPanel._setup_ui()
2. Connect its valueChanged signal in _connect_signals()
3. Update _on_parameter_changed() to include the new value
4. Pass the value to CircuitDiagram.set_parameters()
5. Update CircuitDiagram to use the new parameter
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QDoubleSpinBox, QPushButton, QGroupBox, QFormLayout,
    QSpinBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from circuit_diagram import CircuitDiagram


class ParameterPanel(QGroupBox):
    """
    A panel containing controls for editing circuit parameters.
    
    This panel groups all the input controls for EMF, Resistance,
    Capacitance, and the switch state. It emits signals when parameters
    are changed.
    
    Signals:
        parameters_changed: Emitted when any parameter is modified
            Args: (emf, resistance, capacitance, switch_closed)
    """
    
    parameters_changed = pyqtSignal(float, float, float, bool)
    
    def __init__(self, parent=None):
        """
        Initialize the parameter panel.
        
        Args:
            parent: Optional parent widget
        """
        super().__init__("Circuit Parameters", parent)
        self._setup_ui()
        self._connect_signals()
        
    def _setup_ui(self):
        """
        Set up the user interface elements for the parameter panel.
        
        Creates and arranges all input controls with appropriate labels,
        ranges, and default values.
        """
        layout = QFormLayout()
        layout.setSpacing(15)
        
        # EMF (Voltage Source) control
        self.emf_spinbox = QDoubleSpinBox()
        self.emf_spinbox.setRange(0.0, 100.0)  # 0 to 100 Volts
        self.emf_spinbox.setValue(10.0)  # Default 10V
        self.emf_spinbox.setSuffix(" V")
        self.emf_spinbox.setDecimals(1)
        self.emf_spinbox.setSingleStep(0.5)
        self.emf_spinbox.setToolTip("Electromotive Force (Voltage) in Volts")
        layout.addRow("EMF (Voltage):", self.emf_spinbox)
        
        # Resistance control
        self.resistance_spinbox = QDoubleSpinBox()
        self.resistance_spinbox.setRange(1.0, 10000.0)  # 1 to 10k Ohms
        self.resistance_spinbox.setValue(1000.0)  # Default 1kΩ
        self.resistance_spinbox.setSuffix(" Ω")
        self.resistance_spinbox.setDecimals(1)
        self.resistance_spinbox.setSingleStep(10.0)
        self.resistance_spinbox.setToolTip("Resistance in Ohms")
        layout.addRow("Resistance:", self.resistance_spinbox)
        
        # Capacitance control
        self.capacitance_spinbox = QDoubleSpinBox()
        self.capacitance_spinbox.setRange(1.0, 10000.0)  # 1 to 10000 μF
        self.capacitance_spinbox.setValue(100.0)  # Default 100μF
        self.capacitance_spinbox.setSuffix(" μF")
        self.capacitance_spinbox.setDecimals(1)
        self.capacitance_spinbox.setSingleStep(10.0)
        self.capacitance_spinbox.setToolTip("Capacitance in microFarads")
        layout.addRow("Capacitance:", self.capacitance_spinbox)
        
        # Switch control
        switch_layout = QHBoxLayout()
        self.switch_button = QPushButton("OPEN")
        self.switch_button.setCheckable(True)
        self.switch_button.setStyleSheet("""
            QPushButton {
                min-width: 100px;
                min-height: 30px;
                background-color: #f44336;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:checked {
                background-color: #4CAF50;
            }
        """)
        self.switch_button.setToolTip("Click to toggle switch state")
        switch_layout.addWidget(self.switch_button)
        switch_layout.addStretch()
        layout.addRow("Switch:", switch_layout)
        
        self.setLayout(layout)
        
    def _connect_signals(self):
        """
        Connect signals from UI elements to handler methods.
        
        This sets up the signal-slot connections so that changes in
        any parameter trigger an update.
        """
        self.emf_spinbox.valueChanged.connect(self._on_parameter_changed)
        self.resistance_spinbox.valueChanged.connect(self._on_parameter_changed)
        self.capacitance_spinbox.valueChanged.connect(self._on_parameter_changed)
        self.switch_button.clicked.connect(self._on_switch_toggled)
        
    def _on_parameter_changed(self):
        """
        Handle parameter changes from spinboxes.
        
        This method is called when EMF, Resistance, or Capacitance is changed.
        It emits the parameters_changed signal with current values.
        """
        self.parameters_changed.emit(
            self.emf_spinbox.value(),
            self.resistance_spinbox.value(),
            self.capacitance_spinbox.value(),
            self.switch_button.isChecked()
        )
        
    def _on_switch_toggled(self, checked):
        """
        Handle switch button toggle.
        
        Updates the button text and style based on the switch state,
        then emits the parameters_changed signal.
        
        Args:
            checked: Boolean indicating if the switch is closed
        """
        if checked:
            self.switch_button.setText("CLOSED")
        else:
            self.switch_button.setText("OPEN")
            
        self._on_parameter_changed()
        
    def get_parameters(self):
        """
        Get current parameter values.
        
        Returns:
            tuple: (emf, resistance, capacitance, switch_closed)
        """
        return (
            self.emf_spinbox.value(),
            self.resistance_spinbox.value(),
            self.capacitance_spinbox.value(),
            self.switch_button.isChecked()
        )
        
    def set_parameters(self, emf, resistance, capacitance, switch_closed):
        """
        Set parameter values programmatically.
        
        This method allows setting all parameters at once without
        triggering multiple update signals.
        
        Args:
            emf: EMF value in Volts
            resistance: Resistance value in Ohms
            capacitance: Capacitance value in microFarads
            switch_closed: Boolean indicating if switch is closed
        """
        # Temporarily block signals to avoid multiple updates
        self.emf_spinbox.blockSignals(True)
        self.resistance_spinbox.blockSignals(True)
        self.capacitance_spinbox.blockSignals(True)
        self.switch_button.blockSignals(True)
        
        self.emf_spinbox.setValue(emf)
        self.resistance_spinbox.setValue(resistance)
        self.capacitance_spinbox.setValue(capacitance)
        self.switch_button.setChecked(switch_closed)
        self.switch_button.setText("CLOSED" if switch_closed else "OPEN")
        
        # Re-enable signals
        self.emf_spinbox.blockSignals(False)
        self.resistance_spinbox.blockSignals(False)
        self.capacitance_spinbox.blockSignals(False)
        self.switch_button.blockSignals(False)
        
        # Emit single update
        self._on_parameter_changed()


class InfoPanel(QGroupBox):
    """
    A panel that displays information about the RC circuit.
    
    This panel shows calculated values and information about the
    circuit behavior, such as time constant and charging characteristics.
    """
    
    def __init__(self, parent=None):
        """
        Initialize the information panel.
        
        Args:
            parent: Optional parent widget
        """
        super().__init__("Circuit Information", parent)
        self._setup_ui()
        
    def _setup_ui(self):
        """
        Set up the user interface elements for the info panel.
        """
        layout = QVBoxLayout()
        
        # Time constant label
        self.time_constant_label = QLabel()
        self.time_constant_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.time_constant_label)
        
        # Information text
        info_text = QLabel(
            "The RC time constant (τ = R × C) determines how quickly\n"
            "the capacitor charges and discharges.\n\n"
            "• At τ: ~63.2% charged\n"
            "• At 5τ: ~99.3% charged (fully charged)"
        )
        info_text.setFont(QFont("Arial", 9))
        info_text.setWordWrap(True)
        layout.addWidget(info_text)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def update_info(self, resistance, capacitance):
        """
        Update the displayed information based on circuit parameters.
        
        Args:
            resistance: Resistance value in Ohms
            capacitance: Capacitance value in microFarads
        """
        # Calculate time constant (R in Ohms, C in Farads)
        # Convert capacitance from μF to F
        time_constant = resistance * (capacitance * 1e-6)
        
        # Format the time constant
        if time_constant >= 1.0:
            tc_text = f"Time Constant (τ): {time_constant:.3f} s"
        elif time_constant >= 0.001:
            tc_text = f"Time Constant (τ): {time_constant*1000:.3f} ms"
        else:
            tc_text = f"Time Constant (τ): {time_constant*1e6:.3f} μs"
            
        self.time_constant_label.setText(tc_text)


class MainWindow(QMainWindow):
    """
    Main application window for the RC Circuit Simulator.
    
    This window contains:
    - Circuit diagram display
    - Parameter editing panel
    - Information panel
    
    The window coordinates updates between all components to maintain
    a consistent state.
    """
    
    def __init__(self):
        """
        Initialize the main application window.
        """
        super().__init__()
        self._setup_ui()
        self._connect_signals()
        
        # Initialize with default values
        self._update_circuit()
        
    def _setup_ui(self):
        """
        Set up the main window user interface.
        
        Creates and arranges all major UI components including the
        circuit diagram, parameter panel, and info panel.
        """
        self.setWindowTitle("RC Circuit Simulator")
        self.setMinimumSize(900, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Left side: Circuit diagram
        self.circuit_diagram = CircuitDiagram()
        self.circuit_diagram.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.circuit_diagram.setLineWidth(2)
        main_layout.addWidget(self.circuit_diagram, stretch=2)
        
        # Right side: Control panels
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(20)
        
        # Parameter controls
        self.parameter_panel = ParameterPanel()
        right_layout.addWidget(self.parameter_panel)
        
        # Information display
        self.info_panel = InfoPanel()
        right_layout.addWidget(self.info_panel)
        
        # Add stretch to push everything to the top
        right_layout.addStretch()
        
        main_layout.addWidget(right_panel, stretch=1)
        
        # Set some styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
    def _connect_signals(self):
        """
        Connect signals between UI components.
        
        Sets up communication between the parameter panel and other
        components so that changes propagate correctly.
        """
        self.parameter_panel.parameters_changed.connect(self._update_circuit)
        
    def _update_circuit(self, emf=None, resistance=None, capacitance=None, switch_closed=None):
        """
        Update the circuit diagram and info panel with new parameters.
        
        This method is called when any parameter changes. If parameters
        are not provided, current values from the parameter panel are used.
        
        Args:
            emf: EMF value in Volts (optional)
            resistance: Resistance value in Ohms (optional)
            capacitance: Capacitance value in microFarads (optional)
            switch_closed: Boolean indicating if switch is closed (optional)
        """
        # Get current parameters if not provided
        if emf is None:
            emf, resistance, capacitance, switch_closed = self.parameter_panel.get_parameters()
        
        # Update circuit diagram
        self.circuit_diagram.set_parameters(emf, resistance, capacitance, switch_closed)
        
        # Update information panel
        self.info_panel.update_info(resistance, capacitance)


def main():
    """
    Main entry point for the RC Circuit Simulator application.
    
    Creates and displays the main window.
    """
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = QFont("Arial", 10)
    app.setFont(font)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
