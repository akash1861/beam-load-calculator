# Beam Load Calculator (Simply Supported Beam with Center Point Load)
# Predefined input version for sandbox environments

import numpy as np
import matplotlib.pyplot as plt

def calculate_beam_response(beam_length, load):
    a = beam_length / 2  # Load at center
    R1 = R2 = load / 2  # Symmetrical reactions

    x = np.linspace(0, beam_length, 500)
    shear = np.piecewise(x, [x < a, x >= a], [lambda x: R1, lambda x: -R2])
    moment = np.piecewise(x, [x < a, x >= a],
                          [lambda x: R1 * x,
                           lambda x: R1 * x - load * (x - a)])

    max_moment = (load * beam_length) / 4
    return x, shear, moment, R1, max_moment

def plot_results(x, shear, moment):
    fig, ax = plt.subplots(2, 1, figsize=(8, 6))

    ax[0].plot(x, shear, color='red')
    ax[0].axhline(0, color='black', linewidth=0.5)
    ax[0].set_title("Shear Force Diagram")
    ax[0].set_ylabel("Shear Force (kN)")
    ax[0].grid(True)

    ax[1].plot(x, moment, color='blue')
    ax[1].axhline(0, color='black', linewidth=0.5)
    ax[1].set_title("Bending Moment Diagram")
    ax[1].set_ylabel("Moment (kNm)")
    ax[1].set_xlabel("Beam Length (m)")
    ax[1].grid(True)

    plt.tight_layout()
    plt.show()

def main():
    # Predefined values for testing in environments without input() support
    beam_length = 5.0  # meters
    load = 10.0        # kN

    x, shear, moment, R1, max_moment = calculate_beam_response(beam_length, load)

    print(f"\nResults:")
    print(f"Beam Length: {beam_length} m")
    print(f"Load: {load} kN")
    print(f"Reactions: R1 = R2 = {R1:.2f} kN")
    print(f"Maximum Bending Moment: {max_moment:.2f} kNm at center")

    plot_results(x, shear, moment)

if __name__ == "__main__":
    main()
