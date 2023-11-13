# Define a function that takes mass, distance, and time as parameters
def force(mass, distance, time):
    # Calculate the initial and final velocities using the average velocity formula
    initial_velocity = 0  # Assume the mass starts from rest
    final_velocity = distance / time  # Average velocity is distance divided by time
    # Calculate the acceleration using the acceleration formula
    # Acceleration is change in velocity divided by time
    acceleration = (final_velocity - initial_velocity) / time
    # Calculate the force using Newton's second law of motion
    force = mass * acceleration  # Force is mass times acceleration
    # Return the force
    return force

# Define a function that takes force, distance, time, efficiency, and voltage as parameters


def energy_consumption(force, distance, time, efficiency, voltage):
    # Calculate the speed using the distance and time formula
    speed = distance / time  # Speed is distance divided by time
    # Calculate the power output using the force and speed formula
    power_output = force * speed  # Power output is force times speed
    # Calculate the power input using the power output and efficiency formula
    # Power input is power output divided by efficiency
    power_input = power_output / efficiency
    # Calculate the current using the power input and voltage formula
    current = power_input / voltage  # Current is power input divided by voltage
    # Calculate the energy consumption using the voltage, current, and time formula
    # Energy consumption is voltage times current times time
    energy_consumption = voltage * current * time
    # Return the energy consumption
    return energy_consumption


if __name__ == "__main__":
    with open("motor_energy_v_mass.csv", "w+") as f:
        f.write("Mass (kg),Energy (J)\n")
        for mass in range(1, 1000, 10):
            m_force = force(mass, 10, 10 * 2)
            e = energy_consumption(m_force, 10, 10 * 2, 1, 210)
            f.write(f"{mass},{e}\n")
