import math
import random
import tqdm

COPPER_RESISTIVITY = 1.72e-08
COIL_DIAMETER_MILLIS = 3000
H = 0.0001

properties = [
    "current_amps",
    "voltage",
    "coil_turns",
    "wire_diameter_millis"
]


class Electromagnet:
    coil_diameter_millis: float
    coil_turns: int
    wire_diameter_millis: float
    distance_meters: float
    mass_kg: float
    voltage: float
    current_amps: float
    time_to_zero: float = 0
    obj_velocity: float = 0
    time_step_second = 0.0001

    def __init__(self, coil_diameter_millis, coil_turns, wire_diameter_millis, distance_meters, mass_kg, current_amps, voltage):
        self.coil_diameter_millis = coil_diameter_millis
        self.coil_turns = coil_turns
        self.wire_diameter_millis = wire_diameter_millis
        self.distance_meters = distance_meters
        self.mass_kg = mass_kg
        self.current_amps = current_amps
        self.voltage = voltage
        self.time_to_zero = 0

    def calculate_cross_sectional_area_square_meters(self) -> float:
        return math.pi * (self.coil_diameter_millis/2000)**2

    def force(self):
        if self.wire_can_handle_current():
            return (self.coil_turns*self.current_amps)**2 * 4 * math.pi * 10 ** -7 * self.calculate_cross_sectional_area_square_meters() / (2 * self.distance_meters**2)
        else:
            raise ValueError("Wire cannot handle current")

    def get_acceleration(self):
        return self.force() / self.mass_kg

    def wire_length(self) -> float:
        return self.coil_turns * (self.coil_diameter_millis + self.wire_diameter_millis/2) * math.pi

    def calculate_resistance_ohms(self) -> float:
        return COPPER_RESISTIVITY * (self.wire_length() / 1000) / self.calculate_cross_sectional_area_square_meters()

    def wire_can_handle_current(self) -> bool:
        return self.current_amps <= self.voltage / self.calculate_resistance_ohms()

    def attract_object(self):
        if self.get_acceleration() == 0:
            self.time_to_zero = 1e6

        while self.distance_meters > 0:
            self.obj_velocity += self.get_acceleration() * self.time_step_second
            self.distance_meters -= self.obj_velocity * self.time_step_second
            self.time_to_zero += self.time_step_second

    def calculate_energy(self):
        self.attract_object()
        return self.time_to_zero * self.voltage * self.current_amps

    def get(self, property: str):
        return getattr(self, property)

    def set(self, property: str, value):
        setattr(self, property, value)

    def copy(self):
        self.distance_meters = 10
        self.coil_diameter_millis = COIL_DIAMETER_MILLIS
        return Electromagnet(self.coil_diameter_millis, self.coil_turns, self.wire_diameter_millis, self.distance_meters, self.mass_kg, self.current_amps, self.voltage)

    def optimize_energy(self, epochs=100, lr=1e-5):
        em = self.copy()
        for epoch in tqdm.tqdm(range(epochs)):
            alt_em = em.copy()
            energy = em.calculate_energy()

            for property in properties:
                new_em = em.copy()
                new_em.set(property, em.get(property) + H)
                new_energy = new_em.calculate_energy()
                delta_energy = new_energy - energy / H
                alt_em.set(property, alt_em.get(
                    property) + (delta_energy * lr))

                i = 2
                while not alt_em.wire_can_handle_current():
                    alt_em.set(property, em.get(property) +
                               (delta_energy * (lr) / i))
                    i *= i

                if alt_em.calculate_energy() <= 0:
                    return em

            em = alt_em.copy()

            if epoch % 50 == 0:
                print(f"Epoch {epoch}: {energy}")

        return em


if __name__ == "__main__":
    with open("mass_v_energy.csv", "w+") as f:
        f.write("Mass (kg),Energy (J)\n")

        for mass in tqdm.tqdm(range(1, 1000, 10)):
            em = Electromagnet(coil_diameter_millis=COIL_DIAMETER_MILLIS, wire_diameter_millis=1,
                               current_amps=1000, coil_turns=10000, distance_meters=10, mass_kg=mass, voltage=10).optimize_energy(epochs=45)
            f.write(f"{mass},{em.calculate_energy()}\n")
