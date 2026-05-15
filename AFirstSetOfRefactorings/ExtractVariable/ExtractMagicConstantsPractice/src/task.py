SPEED_OF_LIGHT = 299792458.0
PLANCK_CONSTANT = 6.62607015e-34

def calculate_photon_energy(wave_length: float) -> float:
    frequency = SPEED_OF_LIGHT / wave_length
    return PLANCK_CONSTANT * frequency


def calculate_photon_mass(energy: float) -> float:
    return energy / (SPEED_OF_LIGHT * SPEED_OF_LIGHT)


def main() -> None:
    wave_length = 0.5e-6

    photon_energy = calculate_photon_energy(wave_length)
    photon_mass = calculate_photon_mass(photon_energy)

    print(f"Photon energy: {photon_energy} Joules")
    print(f"Photon mass: {photon_mass} kg")