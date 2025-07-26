from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QTimer
from abacus import Abacus # Import the Abacus model

class AbacusWidget(QWidget):
    valueChanged = pyqtSignal(int) # Signal to emit the abacus's current value

    def __init__(self, num_rods=13):
        super().__init__()
        self.num_rods = num_rods
        self.abacus = Abacus(num_rods=num_rods) # Create an instance of the Abacus model

        self.setMinimumSize(QSize(800, 400)) # Make it more elongated

        # Define key dimensions for bead positioning
        self.frame_margin = 50
        self.beam_height = 20
        self.bead_radius = 15
        self.heaven_bead_spacing = self.bead_radius * 2 + 5
        self.earth_bead_spacing = self.bead_radius * 2 + 5

        # Connect the carry animation signal to its handler
        

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Define colors
        frame_color = QColor(139, 69, 19) # SaddleBrown
        beam_color = QColor(160, 82, 45) # Sienna
        rod_color = QColor(100, 100, 100) # Dark Gray
        heaven_bead_color = QColor(255, 0, 0) # Red
        earth_bead_color = QColor(0, 0, 255) # Blue

        # Dimensions
        widget_width = self.width()
        widget_height = self.height()

        abacus_width = widget_width - 2 * self.frame_margin
        abacus_height = widget_height - 2 * self.frame_margin

        # Draw outer frame
        painter.setBrush(frame_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.frame_margin, self.frame_margin, abacus_width, abacus_height)

        # Draw the beam (divider)
        self.beam_y = self.frame_margin + abacus_height / 4 # Adjusted for elongation
        painter.setBrush(beam_color)
        painter.drawRect(self.frame_margin, int(self.beam_y), abacus_width, self.beam_height)

        # Draw rods and beads
        rod_spacing = abacus_width / (self.num_rods + 1)
        
        for i in range(self.num_rods):
            rod_x = int(self.frame_margin + (i + 1) * rod_spacing)

            # Draw rod
            painter.setPen(QPen(rod_color, 2))
            painter.drawLine(rod_x, self.frame_margin + 10, rod_x, widget_height - self.frame_margin - 10)

            # Draw heaven beads (2 per rod)
            painter.setBrush(heaven_bead_color)
            for j, bead_pos in enumerate(self.abacus.rods[i]['heaven_beads']):
                bead_y = 0
                if j == 0: # Top heaven bead
                    heaven_up_y = self.frame_margin + 10 # Top of frame + frame thickness
                    heaven_down_y = int(self.beam_y - self.bead_radius * 2 - 5) # Top of beam - bead height - small offset
                else: # Bottom heaven bead
                    heaven_up_y = self.frame_margin + 10 + self.bead_radius * 2 + 5 # y_up_0 + bead height + small gap
                    heaven_down_y = int(self.beam_y - self.bead_radius * 2) # Top of beam - bead height (touching beam)

                bead_y = heaven_down_y if bead_pos == 1 else heaven_up_y

                painter.drawEllipse(rod_x - self.bead_radius, int(bead_y), self.bead_radius * 2, self.bead_radius * 2)

            # Draw earth beads (5 per rod)
            painter.setBrush(earth_bead_color)
            for j, bead_pos in enumerate(self.abacus.rods[i]['earth_beads']):
                # Y position for earth beads when they are "up" (touching the beam)
                earth_up_y = int(self.beam_y + self.beam_height + 5 + j * self.earth_bead_spacing)
                # Y position for earth beads when they are "down" (at the bottom of the section)
                earth_down_y = int(widget_height - self.frame_margin - (5 - j) * self.earth_bead_spacing - 5)

                bead_y = earth_up_y if bead_pos == 1 else earth_down_y

                painter.drawEllipse(rod_x - self.bead_radius, int(bead_y), self.bead_radius * 2, self.bead_radius * 2)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            click_x = event.position().x()
            click_y = event.position().y()

            widget_width = self.width()
            abacus_width = widget_width - 2 * self.frame_margin
            rod_spacing = abacus_width / (self.num_rods + 1)

            # Determine clicked rod
            # Iterate through rods to find which one was clicked
            clicked_rod_index = -1
            for i in range(self.num_rods):
                rod_x_center = int(self.frame_margin + (i + 1) * rod_spacing)
                # Check if click_x is within the vicinity of this rod
                if (rod_x_center - self.bead_radius * 2) <= click_x <= (rod_x_center + self.bead_radius * 2):
                    clicked_rod_index = i
                    break
            
            if clicked_rod_index != -1:
                # Determine if heaven or earth bead was clicked
                # Heaven beads are above the beam, Earth beads are below
                if click_y < self.beam_y: # Click in heaven bead section
                    # Determine which heaven bead was clicked
                    # There are 2 heaven beads per rod
                    for j in range(2):
                        heaven_up_y = self.frame_margin + 10 + j * (self.bead_radius * 2 + 5) # Adjusted for new spacing
                        heaven_down_y = int(self.beam_y - self.bead_radius * 2) # Adjusted for new spacing

                        # Check if click_y is within the bead's area (either up or down position)
                        if (heaven_up_y <= click_y <= (heaven_up_y + self.bead_radius * 2)) or \
                           (heaven_down_y <= click_y <= (heaven_down_y + self.bead_radius * 2)):
                            changes, carry_info = self.abacus.move_bead(clicked_rod_index, "heaven", j)
                            self.valueChanged.emit(self.abacus.get_value()) # Emit signal immediately
                            if carry_info:
                                self._start_visual_carry_animation(clicked_rod_index, changes, carry_info)
                            else:
                                self.apply_bead_changes(clicked_rod_index, changes)
                                self.update()
                            break
                elif click_y > (self.beam_y + self.beam_height): # Click in earth bead section
                    # Determine which earth bead was clicked
                    # There are 5 earth beads per rod
                    for j in range(5):
                        earth_up_y = int(self.beam_y + self.beam_height + 5 + j * self.earth_bead_spacing)
                        earth_down_y = int(self.height() - self.frame_margin - (5 - j) * self.earth_bead_spacing - 5)

                        if (earth_up_y <= click_y <= (earth_up_y + self.bead_radius * 2)) or \
                           (earth_down_y <= click_y <= (earth_down_y + self.bead_radius * 2)):
                            changes, carry_info = self.abacus.move_bead(clicked_rod_index, "earth", j)
                            self.valueChanged.emit(self.abacus.get_value()) # Emit signal immediately
                            if carry_info:
                                self._start_visual_carry_animation(clicked_rod_index, changes, carry_info)
                            else:
                                self.apply_bead_changes(clicked_rod_index, changes)
                                self.update()
                            break

    def apply_bead_changes(self, rod_index, changes):
        """Applies a list of bead changes to the abacus model."""
        for bead_type, bead_index, new_position in changes:
            self.abacus.rods[rod_index][f'{bead_type}_beads'][bead_index] = new_position

    def _start_visual_carry_animation(self, rod_index, changes_for_current_rod, carry_info):
        """Initiates the delayed visual animation for carry operations."""
        QTimer.singleShot(500, lambda: self._apply_visual_changes_and_trigger_next_carry(rod_index, changes_for_current_rod, carry_info))

    def _apply_visual_changes_and_trigger_next_carry(self, rod_index, changes_for_current_rod, carry_info):
        """Applies visual changes to the current rod and then triggers the next carry."""
        self.apply_bead_changes(rod_index, changes_for_current_rod)
        self.update()

        if carry_info:
            QTimer.singleShot(500, lambda: self._apply_delayed_bead_change(*carry_info))

    def _apply_delayed_bead_change(self, rod_index, bead_type, bead_index, carry_type):
        """Applies delayed bead changes and handles cascading carries."""
        if rod_index < 0: # Cannot carry to a rod less than 0
            return

        # Simulate the move on the target rod
        changes, next_carry_info = self.abacus.move_bead(rod_index, bead_type, bead_index)
        self.apply_bead_changes(rod_index, changes)
        self.update()
        self.valueChanged.emit(self.abacus.get_value())

        if next_carry_info:
            QTimer.singleShot(500, lambda: self._apply_delayed_bead_change(*next_carry_info)) # Cascade delayed carry


