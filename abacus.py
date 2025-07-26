class Abacus:
    def __init__(self, num_rods=13):
        self.num_rods = num_rods
        self.rods = []
        for _ in range(num_rods):
            # Each rod has 2 heaven beads and 5 earth beads.
            # Heaven beads: 0 = up (value 0), 1 = down (value 5)
            # Earth beads: 0 = down (value 0), 1 = up (value 1)
            self.rods.append({
                'heaven_beads': [0, 0], # [bead1_pos, bead2_pos]
                'earth_beads': [0, 0, 0, 0, 0] # [bead1_pos, ..., bead5_pos]
            }) # Initialize all beads to their 'zero' position

    def reset(self):
        for rod in self.rods:
            rod['heaven_beads'] = [0, 0]
            rod['earth_beads'] = [0, 0, 0, 0, 0]

    def get_value(self):
        total_value = 0
        for i, rod in enumerate(reversed(self.rods)):
            rod_value = self._get_rod_value(rod)
            total_value += rod_value * (10 ** i)
        return total_value

    def _get_rod_value(self, rod):
        rod_value = 0
        # Calculate value from heaven beads
        for bead_pos in rod['heaven_beads']:
            if bead_pos == 1: # Bead is down
                rod_value += 5
        # Calculate value from earth beads
        for bead_pos in rod['earth_beads']:
            if bead_pos == 1: # Bead is up
                rod_value += 1
        return rod_value

    def move_bead(self, rod_index, bead_type, bead_index):
        if not (0 <= rod_index < self.num_rods):
            raise IndexError("Rod index out of bounds")

        rod = self.rods[rod_index]
        carry_info = None # Initialize carry_info to None
        changes = [] # List to store bead changes for the current rod

        # Create a mutable copy of the rod state to apply changes to for simulation
        current_simulated_rod = {
            'heaven_beads': list(rod['heaven_beads']),
            'earth_beads': list(rod['earth_beads'])
        }

        if bead_type == "heaven":
            if not (0 <= bead_index < 2):
                raise IndexError("Heaven bead index out of bounds (0 or 1)")
            
            # Get current state of the clicked heaven bead from the actual rod (initial click)
            current_bead_pos = rod['heaven_beads'][bead_index]
            
            if bead_index == 1: # Bottom heaven bead (value 5) was clicked
                if current_simulated_rod['heaven_beads'][1] == 0: # Bottom bead is currently UP (0), moving DOWN (1) - ADDITION
                    changes.append(("heaven", 1, 1)) # Move bottom heaven bead down
                    current_simulated_rod['heaven_beads'][1] = 1
                    # If top heaven bead is down, and bottom is now down, it's a 10. Reset and carry.
                    if current_simulated_rod['heaven_beads'][0] == 1:
                        for i in range(2):
                            changes.append(("heaven", i, 0)) # Reset both heaven beads
                            current_simulated_rod['heaven_beads'][i] = 0
                        carry_info = (rod_index - 1, 'earth', 0, 'rod_10_carry')
                else: # Bottom bead is currently DOWN (1), moving UP (0) - SUBTRACTION
                    changes.append(("heaven", 1, 0)) # Move bottom heaven bead up
                    current_simulated_rod['heaven_beads'][1] = 0
                    # Ensure top heaven bead is up if it was down (shouldn't happen with correct logic, but for safety)
                    if current_simulated_rod['heaven_beads'][0] == 1:
                        changes.append(("heaven", 0, 0))
                        current_simulated_rod['heaven_beads'][0] = 0

            elif bead_index == 0: # Top heaven bead (value 5) was clicked
                # Check current state of both heaven beads
                top_bead_is_up = current_simulated_rod['heaven_beads'][0] == 0
                bottom_bead_is_up = current_simulated_rod['heaven_beads'][1] == 0

                if top_bead_is_up and bottom_bead_is_up: # Both are up (value 0), clicking top implies adding 10
                    # Temporarily move both down for visual effect (before reset)
                    changes.append(("heaven", 0, 1))
                    current_simulated_rod['heaven_beads'][0] = 1
                    changes.append(("heaven", 1, 1))
                    current_simulated_rod['heaven_beads'][1] = 1

                    # Then, reset both and trigger carry
                    for i in range(2):
                        changes.append(("heaven", i, 0)) # Reset both heaven beads
                        current_simulated_rod['heaven_beads'][i] = 0
                    carry_info = (rod_index - 1, 'earth', 0, 'rod_10_carry')

                elif top_bead_is_up and not bottom_bead_is_up: # Top is up, bottom is down (value 5), clicking top implies adding 5 to make 10
                    changes.append(("heaven", 0, 1)) # Move top heaven bead down
                    current_simulated_rod['heaven_beads'][0] = 1
                    # Now both are down, so it's a 10. Reset and carry.
                    for i in range(2):
                        changes.append(("heaven", i, 0)) # Reset both heaven beads
                        current_simulated_rod['heaven_beads'][i] = 0
                    carry_info = (rod_index - 1, 'earth', 0, 'rod_10_carry')

                elif not top_bead_is_up: # Top bead is currently DOWN (1), moving UP (0) - SUBTRACTION
                    changes.append(("heaven", 0, 0)) # Move top heaven bead up
                    current_simulated_rod['heaven_beads'][0] = 0

        elif bead_type == "earth":
            if not (0 <= bead_index < 5):
                raise IndexError("Earth bead index out of bounds (0-4)")
            
            # Determine the new state for the clicked bead
            current_pos = rod['earth_beads'][bead_index]
            new_pos = 1 - current_pos # Toggle 0 to 1, 1 to 0

            if new_pos == 1: # Moving earth bead UP
                # All beads from clicked bead's position to the top (index 0) move up
                for i in range(bead_index + 1):
                    if current_simulated_rod['earth_beads'][i] == 0: # Only add change if bead actually moves
                        changes.append(("earth", i, 1))
                        current_simulated_rod['earth_beads'][i] = 1
            else: # Moving earth bead DOWN
                # All beads from clicked bead's position to the bottom (index 4) move down
                for i in range(bead_index, 5):
                    if current_simulated_rod['earth_beads'][i] == 1: # Only add change if bead actually moves
                        changes.append(("earth", i, 0))
                        current_simulated_rod['earth_beads'][i] = 0
            
            # Earth Bead Carry (Value 5): When all 5 earth beads are up
            if sum(current_simulated_rod['earth_beads']) == 5:
                # If bottom heaven bead is up, move it down and reset earth beads
                if current_simulated_rod['heaven_beads'][1] == 0: # Check current state of heaven bead
                    # Reset all earth beads to down (explicitly set all to 0)
                    for i in range(5):
                        changes.append(("earth", i, 0))
                        current_simulated_rod['earth_beads'][i] = 0
                    changes.append(("heaven", 1, 1)) # Move bottom heaven bead down
                    current_simulated_rod['heaven_beads'][1] = 1
                    changes.append(("heaven", 0, 0)) # Ensure top heaven bead is up
                    current_simulated_rod['heaven_beads'][0] = 0
                else: # If bottom heaven bead is already down, and earth beads sum to 5, it's a carry of 10
                    # This means the rod value is 5 (heaven) + 5 (earth) = 10
                    # Reset current rod and indicate a carry to the next rod
                    for i in range(2):
                        changes.append(("heaven", i, 0))
                        current_simulated_rod['heaven_beads'][i] = 0
                    for i in range(5):
                        changes.append(("earth", i, 0))
                        current_simulated_rod['earth_beads'][i] = 0
                    carry_info = (rod_index - 1, 'earth', 0, 'rod_10_carry') # Carry 1 to the next rod

        else:
            raise ValueError("Invalid bead_type. Must be 'heaven' or 'earth'.")

        # After any bead movement, check for rod carry (value 10 or more)
        # This check should only trigger if the value *increases* to 10 or more
        # and hasn't already been handled by the earth bead carry logic above.
        
        current_rod_value = self._get_rod_value(current_simulated_rod)

        # If the current rod value is 10 or more, and it wasn't a direct heaven_10_carry from top heaven bead click
        # and it wasn't already handled by the earth bead carry (which sets carry_info)
        if current_rod_value >= 10 and carry_info is None:
            # Reset current rod (explicitly set all to 0)
            for i in range(2):
                changes.append(("heaven", i, 0))
                current_simulated_rod['heaven_beads'][i] = 0
            for i in range(5):
                changes.append(("earth", i, 0))
                current_simulated_rod['earth_beads'][i] = 0
            # Indicate a carry to the next rod
            carry_info = (rod_index - 1, 'earth', 0, 'rod_10_carry') # Add a carry_type for animation
        
        return changes, carry_info # Return changes and carry information

    def __str__(self):
        s = f"Abacus with {self.num_rods} rods. Current value: {self.get_value()}\n"
        for i, rod in enumerate(self.rods):
            s += f"Rod {i}: Heaven: {rod['heaven_beads']}, Earth: {rod['earth_beads']}\n"
        return s

# Example usage (for testing the model)
if __name__ == "__main__":
    abacus = Abacus(num_rods=3)
    print("Initial Abacus:")
    print(abacus)

    print("\nMoving earth bead 0 on rod 0 up (units rod):")
    abacus.move_bead(0, "earth", 0)
    print(abacus)

    print("\nMoving bottom heaven bead on rod 0 down:")
    abacus.move_bead(0, "heaven", 1)
    print(abacus)

    print("\nMoving earth bead 4 on rod 0 up (should trigger carry of 5 to heaven bead on same rod): ")
    abacus.reset() # Reset for a clean test
    abacus.move_bead(0, "earth", 0)
    abacus.move_bead(0, "earth", 1)
    abacus.move_bead(0, "earth", 2)
    abacus.move_bead(0, "earth", 3)
    abacus.move_bead(0, "earth", 4) # This should trigger the carry to heaven bead
    print(abacus)

    print("\nMoving top heaven bead on rod 0 (should trigger carry of 10 to next rod):")
    abacus.reset() # Reset for a clean test
    abacus.move_bead(0, "heaven", 0) # This should trigger the carry
    print(abacus)

    print("\nSetting rod 0 to 9, then adding 1 (should trigger carry of 10 to next rod via earth bead):")
    abacus.reset() # Reset for a clean test
    # Set rod 0 to 9 (bottom heaven bead down, 4 earth beads up)
    abacus.move_bead(0, "heaven", 1)
    abacus.move_bead(0, "earth", 0)
    abacus.move_bead(0, "earth", 1)
    abacus.move_bead(0, "earth", 2)
    abacus.move_bead(0, "earth", 3)
    print("Rod 0 set to 9:")
    print(abacus)
    abacus.move_bead(0, "earth", 4) # Move 5th earth bead up, should make it 10 and carry
    print("After adding 1 (should be 10):")
    print(abacus)

    print("\nResetting Abacus:")
    abacus.reset()
    print(abacus)

    print("\nSetting a value (e.g., 75 on rod 0 and 1):\n(This will now use the new carry logic, so direct setting might be complex)")
    # To set 75, we need to manually move beads for now
    # Rod 0 (units) = 5 (bottom heaven bead 0 down) + 2 (earth beads 0,1 up) = 7
    abacus.move_bead(0, "heaven", 1)
    abacus.move_bead(0, "earth", 0)
    abacus.move_bead(0, "earth", 1)
    # Rod 1 (tens) = 5 (bottom heaven bead 0 down) + 2 (earth beads 0,1 up) = 7
    abacus.move_bead(1, "heaven", 1)
    abacus.move_bead(1, "earth", 0)
    abacus.move_bead(1, "earth", 1)
    print(abacus)
    print(f"Current abacus value: {abacus.get_value()}")
