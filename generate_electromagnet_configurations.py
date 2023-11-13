import math
import json
import argparse
from tqdm import tqdm

class ElectromagnetConfiguration:
    object_distance_centimeters: float
    current_amps: float
    wire_diameter_millimeters: float

    def __init__(self, object_distance: float, current_amps: float, wire_diameter_millimeters: float) -> None:
        self.object_distance_centimeters = object_distance
        self.current_amps = current_amps
        self.wire_diameter_millimeters = wire_diameter_millimeters


class Electromagnet:
    def __init__(self, inputs: dict) -> None:
        self.force_newtons = inputs["force_newtons"]
        self.coil_diameter_millimeters = inputs["coil_diameter_millimeters"]
        self.copper_resistivity = inputs["copper_resistivity"]
        self.wire_outside_coil_millimeters = inputs["wire_outside_coil_millimeters"]
        self.battery_voltage = inputs["battery_voltage"]

    def calculate_cross_sectional_area_square_meters(self, diameter_millimeters: float) -> float:
        return math.pi * (diameter_millimeters / 2000)**2

    def force(self, distance_meters: float, current_amps: float, diameter_meters: float) -> float:
        return (self.coil_turns*current_amps)**2 * 4 * math.pi * 10 ** -7 * self.calculate_cross_sectional_area_square_meters(diameter_meters) / (2 * distance_meters**2)

    def calculate_length_of_wire_in_millimeters(self, turns: float, diameter_millimeters: float) -> float:
        return turns * (self.coil_diameter_millimeters + diameter_millimeters/2) * math.pi + 2 * self.wire_outside_coil_millimeters

    def calculate_resistance_ohms(self, wire_diameter: float, coil_turns: float) -> float:
        return self.copper_resistivity * (self.calculate_length_of_wire_in_millimeters(coil_turns, wire_diameter) / 1000) / self.calculate_cross_sectional_area_square_meters(wire_diameter)

    def _millimeter_to_meter(self, value_millimeters: float) -> float:
        return value_millimeters / 1000

    def _get_max_wire_amps(self, diameter_millimeters: float) -> float:
        return self.battery_voltage / self.calculate_resistance_ohms(diameter_millimeters, self.coil_turns)

    def find_optimal_values(self, path: str):
        with open(path, "w+") as f:
            f.write(
                "Current (Amps),Coil Diameter (Millimeters),Wire Diameter,Distance (Millimeters),Turns,Voltage,Force (Newtons)\n")
            for voltage in [7.4, 9, 110, 220]:
                print(f"Now doing {voltage}V")
                self.battery_voltage = voltage
                for wire_diameter_millimeters in tqdm(range(1, 11)):
                    for distance_millimeters in range(10, 60, 10):
                        for coil_diameter_millimeters in tqdm(range(2, 30)):
                            self.coil_diameter_millimeters = coil_diameter_millimeters
                            for turns in range(30, 1000):
                                self.coil_turns = turns
                                max_amps = int(self._get_max_wire_amps(wire_diameter_millimeters))
                                for current_amps in range(1, max_amps, int(max_amps / 200) + 1):
                                    force_i_j = self.force(
                                        self._millimeter_to_meter(distance_millimeters), current_amps, self._millimeter_to_meter(wire_diameter_millimeters))
                                    if force_i_j > self.force_newtons:
                                        f.write(
                                            f"{current_amps},{coil_diameter_millimeters},{wire_diameter_millimeters},{distance_millimeters},{self.coil_turns},{voltage},{force_i_j}\n")

    def see_if_em_produces_required_force(self, current_amps, coil_diameter_millimeters, wire_diameter_millimeters, turns, voltage, distance_millimeters=10):
        self.battery_voltage = voltage
        self.coil_diameter_millimeters = coil_diameter_millimeters
        self.coil_turns = turns
        max_amps = int(self._get_max_wire_amps(wire_diameter_millimeters))
        if current_amps > max_amps:
            print(f"Current is too high, current:{current_amps}, max: {max_amps}")
        force_i_j = self.force(
                               self._millimeter_to_meter(distance_millimeters), current_amps, self._millimeter_to_meter(wire_diameter_millimeters)
                               )
        if force_i_j > self.force_newtons:
            print("Sufficient Force")

        else:
            print("Not Enough Force")
    
    def generate_max_current_for_turns_and_diameters_configurations(self, output: str, min_diameter_millimeters=1, max_diameter_millimeters=20, max_turns=150, min_turns=30):
        with open(output, "w+") as f:
            f.write("Current (Amps),Diameter (Millimeters),Turns\n")
            for turns in tqdm(range(min_turns, max_turns)):
                self.coil_turns = turns
                for diameter_millimeters in range(min_diameter_millimeters, max_diameter_millimeters):
                    max_current = self._get_max_wire_amps(diameter_millimeters)
                    f.write(f"{max_current},{diameter_millimeters},{turns}\n")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find working configurations for an electromagnet')
    parser.add_argument('config', type=str,
                        help='path to json config file')
    parser.add_argument('output', type=str,
                        help='path to output csv file')
    args = parser.parse_args()

    with open(args.config, "r") as f:
        inputs = json.load(f)

    em = Electromagnet(inputs)
    #em.find_optimal_values(args.output)
    #em.generate_max_current_for_turns_and_diameters_configurations(args.output)
    em.see_if_em_produces_required_force(350, 25, 5, 150, 9)
