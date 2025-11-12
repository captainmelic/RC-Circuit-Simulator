#!/usr/bin/env python3
"""
Demo script for the RC Circuit Simulator

This script demonstrates programmatic control of the circuit parameters.
You can use this as a reference for extending the simulator.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from rc_circuit_simulator import MainWindow


def run_demo():
    """
    Run an automated demo of the RC Circuit Simulator.
    
    This demonstrates how to programmatically control the circuit
    parameters, which can be useful for creating animations or
    automated demonstrations.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    print("RC Circuit Simulator - Demo Mode")
    print("=" * 50)
    print("\nThis demo will automatically cycle through different")
    print("circuit configurations to showcase the features.\n")
    
    # Define demo states
    demo_states = [
        {
            'name': 'Low Voltage, Low Capacitance',
            'emf': 5.0,
            'resistance': 500.0,
            'capacitance': 10.0,
            'switch': False
        },
        {
            'name': 'Medium Voltage, Medium Capacitance (Switch Closed)',
            'emf': 10.0,
            'resistance': 1000.0,
            'capacitance': 100.0,
            'switch': True
        },
        {
            'name': 'High Voltage, High Capacitance',
            'emf': 20.0,
            'resistance': 5000.0,
            'capacitance': 1000.0,
            'switch': True
        },
        {
            'name': 'Maximum Values (Switch Open)',
            'emf': 50.0,
            'resistance': 10000.0,
            'capacitance': 5000.0,
            'switch': False
        }
    ]
    
    current_state = [0]  # Use list to modify in nested function
    
    def next_state():
        """Display the next demo state"""
        if current_state[0] < len(demo_states):
            state = demo_states[current_state[0]]
            
            print(f"State {current_state[0] + 1}: {state['name']}")
            print(f"  EMF: {state['emf']} V")
            print(f"  Resistance: {state['resistance']} Ω")
            print(f"  Capacitance: {state['capacitance']} μF")
            print(f"  Switch: {'CLOSED' if state['switch'] else 'OPEN'}")
            
            # Update the circuit parameters
            window.parameter_panel.set_parameters(
                state['emf'],
                state['resistance'],
                state['capacitance'],
                state['switch']
            )
            
            current_state[0] += 1
            
            if current_state[0] < len(demo_states):
                # Schedule next state after 3 seconds
                QTimer.singleShot(3000, next_state)
            else:
                print("\n" + "=" * 50)
                print("Demo complete! You can now interact with the controls.")
        
    # Start the demo after a short delay
    QTimer.singleShot(1000, next_state)
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    # Check if demo mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == '--no-demo':
        # Just run the normal application
        from rc_circuit_simulator import main
        main()
    else:
        # Run the demo
        run_demo()
