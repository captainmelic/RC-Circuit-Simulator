"""
RC Circuit Diagram Generator

This module generates an image of an RC circuit using PyQt6's QPainter.
The circuit includes:
- EMF (voltage source)
- Resistor
- Capacitor
- Switch (open/closed)

DESIGN:
-------
The CircuitDiagram class is a QFrame widget that draws a complete RC circuit
schematic. It uses QPainter to draw standard electrical symbols and updates
in real-time when parameters change.

The drawing is organized into modular methods:
- _draw_wires(): Connects all components with wires
- _draw_emf(): Draws the voltage source symbol
- _draw_resistor(): Draws the resistor symbol
- _draw_capacitor(): Draws the capacitor symbol
- _draw_switch(): Draws the switch (open or closed)
- _draw_labels(): Adds parameter labels to components

ADDING NEW COMPONENTS:
---------------------
To add a new component to the circuit:

1. Add a new parameter to __init__() and set_parameters()
2. Create a new _draw_componentname() method following the pattern of existing methods
3. Call your new drawing method from paintEvent()
4. Update _draw_wires() if the component needs wire connections
5. Update _draw_labels() to show the component's value

Example component drawing method structure:
    def _draw_componentname(self, painter, x, y):
        '''Draw the component symbol'''
        pen = QPen(QColor(0, 0, 0), 2)
        painter.setPen(pen)
        # Use painter.drawLine(), painter.drawRect(), etc.
        # Use QPointF for float coordinates or integers for exact pixels

ELECTRICAL SYMBOLS:
------------------
- EMF: Two parallel lines (+ and -)
- Resistor: Rectangular box
- Capacitor: Two parallel plates
- Switch: Two connection points with movable arm
- Wires: Simple lines connecting components
"""

from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QPixmap, QBrush
from PyQt6.QtWidgets import QWidget, QFrame


class CircuitDiagram(QFrame):
    """
    A widget that renders an RC circuit diagram.
    
    The circuit is drawn with proper electrical symbols and can be
    updated to show different component values and switch states.
    """
    
    def __init__(self, parent=None):
        """
        Initialize the circuit diagram widget.
        
        Args:
            parent: Optional parent widget
        """
        super().__init__(parent)
        self.setMinimumSize(600, 400)
        
        # Circuit parameters (for display)
        self.emf_value = 10.0  # Volts
        self.resistance_value = 1000.0  # Ohms
        self.capacitance_value = 100.0  # microFarads
        self.switch_closed = False  # Switch state
        self.charge_level = 0.0  # Capacitor charge level (0-100%)
        
    def set_parameters(self, emf, resistance, capacitance, switch_closed):
        """
        Update circuit parameters and refresh the display.
        
        Args:
            emf: EMF value in Volts
            resistance: Resistance value in Ohms
            capacitance: Capacitance value in microFarads
            switch_closed: Boolean indicating if switch is closed
        """
        self.emf_value = emf
        self.resistance_value = resistance
        self.capacitance_value = capacitance
        self.switch_closed = switch_closed
        self.update()  # Trigger a repaint
        
    def set_charge_level(self, level):
        """
        Update the capacitor charge level for visualization.
        
        Args:
            level: Charge level from 0 to 100
        """
        self.charge_level = level
        self.update()  # Trigger a repaint
        
    def paintEvent(self, event):
        """
        Paint the circuit diagram showing two loops:
        - Charging loop (switch closed): EMF → Switch → Resistor → Capacitor → EMF
        - Discharging loop (switch open): Resistor ⟷ Capacitor (via center wire)
        
        This method is called automatically when the widget needs to be redrawn.
        
        Args:
            event: The paint event
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Set up drawing parameters
        pen = QPen(QColor(0, 0, 0), 2)
        painter.setPen(pen)
        
        # Define circuit layout positions for two-loop design
        margin = 50
        width = self.width()
        height = self.height()
        
        # Calculate key positions for circuit components
        left_x = margin + 50
        right_x = width - margin - 50
        top_y = margin + 50
        bottom_y = height - margin - 50
        center_y = (top_y + bottom_y) // 2
        mid_x = (left_x + right_x) // 2
        
        # Resistor position (moved to right side, top)
        resistor_x = right_x - 60
        resistor_y = top_y + 60
        
        # Draw the circuit components
        self._draw_wires(painter, left_x, right_x, top_y, bottom_y, center_y, mid_x, resistor_x, resistor_y)
        self._draw_emf(painter, left_x, center_y)
        self._draw_resistor(painter, resistor_x, resistor_y)
        self._draw_capacitor(painter, right_x, center_y)
        self._draw_switch(painter, left_x + 80, bottom_y)
        
        # Draw labels
        self._draw_labels(painter, left_x, right_x, top_y, bottom_y, center_y, mid_x, resistor_x, resistor_y)
        
        # Draw loop indicators to show charging vs discharging paths
        self._draw_loop_indicators(painter, left_x, right_x, top_y, bottom_y, center_y, mid_x)
        
    def _draw_wires(self, painter, left_x, right_x, top_y, bottom_y, center_y, mid_x, resistor_x, resistor_y):
        """
        Draw the connecting wires showing two distinct loops with center dividing wire:
        - Charging loop (switch closed): EMF → Switch → Resistor → Capacitor → EMF
        - Discharging loop (switch open): Resistor ⟷ Capacitor (via center wire)
        
        Args:
            painter: QPainter object
            left_x, right_x, top_y, bottom_y, center_y, mid_x: Layout coordinates
            resistor_x, resistor_y: Resistor position
        """
        pen = QPen(QColor(0, 0, 0), 2)
        painter.setPen(pen)
        
        # CENTER DIVIDING WIRE - creates the two loops
        # This vertical wire in the middle divides the circuit into left and right loops
        painter.drawLine(mid_x, top_y, mid_x, bottom_y)
        
        # LEFT LOOP (with EMF and switch)
        # Left vertical wire from EMF top to top
        painter.drawLine(left_x, center_y - 30, left_x, top_y)
        
        # Top horizontal wire (left to center)
        painter.drawLine(left_x, top_y, mid_x, top_y)
        
        # Bottom horizontal wire (center to switch)
        painter.drawLine(mid_x, bottom_y, left_x + 80 + 30, bottom_y)
        
        # Wire from switch to EMF (connected or disconnected based on switch state)
        if self.switch_closed:
            # Complete charging loop
            painter.drawLine(left_x + 80 - 30, bottom_y, left_x, bottom_y)
        else:
            # Partial wire when switch is open (stops before EMF)
            painter.drawLine(left_x + 80 - 30, bottom_y, left_x + 40, bottom_y)
        
        # Left bottom vertical wire (from EMF bottom) - ALWAYS DRAW THIS
        painter.drawLine(left_x, bottom_y, left_x, center_y + 30)
        
        # RIGHT LOOP (with Resistor and Capacitor)
        # Top: center to resistor to capacitor
        painter.drawLine(mid_x, top_y, resistor_x - 40, resistor_y)
        painter.drawLine(resistor_x + 40, resistor_y, right_x, resistor_y)
        painter.drawLine(right_x, resistor_y, right_x, center_y - 30)
        
        # Bottom: capacitor to center
        painter.drawLine(right_x, center_y + 30, right_x, bottom_y)
        painter.drawLine(right_x, bottom_y, mid_x, bottom_y)
        
    def _draw_emf(self, painter, x, y):
        """
        Draw the EMF (voltage source) symbol.
        
        The EMF is represented by two parallel lines of different lengths
        with + and - symbols.
        
        Args:
            painter: QPainter object
            x, y: Center position of the EMF
        """
        pen = QPen(QColor(0, 0, 0), 3)
        painter.setPen(pen)
        
        # Positive terminal (longer line)
        painter.drawLine(x - 20, y - 30, x + 20, y - 30)
        
        # Negative terminal (shorter line)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(x - 10, y + 30, x + 10, y + 30)
        
        # Draw + and - symbols
        font = QFont("Arial", 12, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(x - 35, y - 30, "+")
        painter.drawText(x - 35, y + 35, "-")
        
        # Connection wires
        painter.drawLine(x, y - 30, x, y - 30)
        painter.drawLine(x, y + 30, x, y + 30)
        
    def _draw_resistor(self, painter, x, y):
        """
        Draw the resistor symbol with proper zigzag pattern.
        
        Args:
            painter: QPainter object
            x, y: Center position of the resistor
        """
        pen = QPen(QColor(0, 0, 0), 2)
        painter.setPen(pen)
        
        # Draw zigzag resistor symbol (actual zigzag pattern)
        # The zigzag has 6 peaks over a length of 60 pixels
        wire_length = 20  # Connection wires on each side
        zigzag_width = 60
        zigzag_height = 12
        num_peaks = 6
        segment_width = zigzag_width / num_peaks
        
        # Left connection wire
        painter.drawLine(QPointF(x - zigzag_width/2 - wire_length, y), 
                        QPointF(x - zigzag_width/2, y))
        
        # Draw zigzag pattern
        for i in range(num_peaks):
            x_start = x - zigzag_width/2 + i * segment_width
            x_end = x - zigzag_width/2 + (i + 1) * segment_width
            
            # Alternate between up and down peaks
            if i % 2 == 0:
                # Peak up
                painter.drawLine(QPointF(x_start, y), 
                               QPointF(x_start + segment_width/2, y - zigzag_height))
                painter.drawLine(QPointF(x_start + segment_width/2, y - zigzag_height), 
                               QPointF(x_end, y))
            else:
                # Peak down
                painter.drawLine(QPointF(x_start, y), 
                               QPointF(x_start + segment_width/2, y + zigzag_height))
                painter.drawLine(QPointF(x_start + segment_width/2, y + zigzag_height), 
                               QPointF(x_end, y))
        
        # Right connection wire
        painter.drawLine(QPointF(x + zigzag_width/2, y), 
                        QPointF(x + zigzag_width/2 + wire_length, y))
        
    def _draw_capacitor(self, painter, x, y):
        """
        Draw the capacitor symbol (two parallel plates).
        
        Args:
            painter: QPainter object
            x, y: Center position of the capacitor
        """
        pen = QPen(QColor(0, 0, 0), 3)
        painter.setPen(pen)
        
        plate_length = 40
        plate_gap = 10
        
        # Top plate
        painter.drawLine(x - plate_length//2, y - plate_gap//2,
                        x + plate_length//2, y - plate_gap//2)
        
        # Bottom plate
        painter.drawLine(x - plate_length//2, y + plate_gap//2,
                        x + plate_length//2, y + plate_gap//2)
        
    def _draw_switch(self, painter, x, y):
        """
        Draw the switch symbol.
        
        The switch is shown as open (gap) or closed (connected) based on
        the switch_closed state.
        
        Args:
            painter: QPainter object
            x, y: Center position of the switch
        """
        pen = QPen(QColor(0, 0, 0), 3)
        painter.setPen(pen)
        
        # Left connection point
        painter.drawEllipse(QPointF(x - 30, y), 4, 4)
        
        # Right connection point
        painter.drawEllipse(QPointF(x + 30, y), 4, 4)
        
        # Switch arm
        if self.switch_closed:
            # Closed - horizontal line
            painter.drawLine(x - 26, y, x + 26, y)
        else:
            # Open - angled line
            painter.drawLine(x - 26, y, x + 20, y - 15)
        
    def _draw_labels(self, painter, left_x, right_x, top_y, bottom_y, center_y, mid_x, resistor_x, resistor_y):
        """
        Draw labels for all circuit components showing their values.
        
        Args:
            painter: QPainter object
            left_x, right_x, top_y, bottom_y, center_y, mid_x: Layout coordinates
            resistor_x, resistor_y: Resistor position
        """
        font = QFont("Arial", 10)
        painter.setFont(font)
        pen = QPen(QColor(0, 0, 255))
        painter.setPen(pen)
        
        # EMF label
        emf_text = f"EMF: {self.emf_value:.1f} V"
        painter.drawText(left_x - 60, center_y, emf_text)
        
        # Resistor label (adjusted for new position on right side)
        if self.resistance_value >= 1000:
            r_text = f"R: {self.resistance_value/1000:.1f} kΩ"
        else:
            r_text = f"R: {self.resistance_value:.1f} Ω"
        painter.drawText(resistor_x - 30, resistor_y - 15, r_text)
        
        # Capacitor label
        c_text = f"C: {self.capacitance_value:.1f} μF"
        painter.drawText(right_x + 10, center_y - 30, c_text)
        
        # Charge level indicator on capacitor (moved further away to avoid blocking symbol)
        charge_text = f"{self.charge_level:.1f}%"
        painter.drawText(right_x + 10, center_y + 40, charge_text)
        
        # Switch label
        switch_text = "Switch: " + ("CLOSED" if self.switch_closed else "OPEN")
        painter.drawText(left_x + 20, bottom_y + 20, switch_text)
        
    def _draw_loop_indicators(self, painter, left_x, right_x, top_y, bottom_y, center_y, mid_x):
        """
        Draw indicators showing the charging and discharging loops.
        The center wire divides the circuit into two loops:
        - Left loop: EMF and Switch (charging path when closed)
        - Right loop: Resistor and Capacitor (always active for discharging)
        
        Args:
            painter: QPainter object
            left_x, right_x, top_y, bottom_y, center_y, mid_x: Layout coordinates
        """
        font = QFont("Arial", 9, QFont.Weight.Bold)
        painter.setFont(font)
        
        if self.switch_closed:
            # Show charging loop indicator (both loops active)
            pen = QPen(QColor(0, 150, 0))
            painter.setPen(pen)
            painter.drawText(left_x + 20, center_y - 30, "Charging")
            painter.drawText(left_x + 10, center_y - 15, "(EMF active)")
        else:
            # Show discharging loop indicator (only right loop active)
            pen = QPen(QColor(200, 0, 0))
            painter.setPen(pen)
            painter.drawText(mid_x + 10, center_y - 20, "Discharging")
            painter.drawText(mid_x + 10, center_y - 5, "(R ⟷ C)")


def generate_circuit_image(emf=10.0, resistance=1000.0, capacitance=100.0, 
                          switch_closed=False, width=600, height=400):
    """
    Generate a circuit diagram as a QPixmap.
    
    This is a helper function that can be used to generate circuit images
    programmatically without creating a widget.
    
    Args:
        emf: EMF value in Volts (default: 10.0)
        resistance: Resistance value in Ohms (default: 1000.0)
        capacitance: Capacitance value in microFarads (default: 100.0)
        switch_closed: Boolean indicating if switch is closed (default: False)
        width: Image width in pixels (default: 600)
        height: Image height in pixels (default: 400)
        
    Returns:
        QPixmap containing the circuit diagram
    """
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.GlobalColor.white)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # Create a temporary widget to use its drawing methods
    circuit = CircuitDiagram()
    circuit.resize(width, height)
    circuit.set_parameters(emf, resistance, capacitance, switch_closed)
    
    # Render the circuit onto the pixmap
    circuit.render(painter)
    painter.end()
    
    return pixmap
