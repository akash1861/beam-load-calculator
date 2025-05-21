import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_beam_response(beam_length, load):
    a = beam_length / 2
    R1 = R2 = load / 2

    x = np.linspace(0, beam_length, 500)
    shear = np.piecewise(x, [x < a, x >= a], [lambda x: R1, lambda x: -R2])
    moment = np.piecewise(x, [x < a, x >= a],
                          [lambda x: R1 * x, lambda x: R1 * x - load * (x - a)])

    max_moment = (load * beam_length) / 4
    return x, shear, moment, R1, max_moment

def plot_diagrams(x, shear, moment):
    fig, ax = plt.subplots(2, 1, figsize=(8, 6))

    ax[0].plot(x, shear, 'r')
    ax[0].set_title("Shear Force Diagram")
    ax[0].set_ylabel("Shear Force (kN)")
    ax[0].grid(True)

    ax[1].plot(x, moment, 'b')
    ax[1].set_title("Bending Moment Diagram")
    ax[1].set_xlabel("Beam Length (m)")
    ax[1].set_ylabel("Moment (kNm)")
    ax[1].grid(True)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def main():
    st.title("🔧 Beam Load Calculator (Simply Supported Beam with Center Point Load)")

    beam_length = st.number_input("Beam Length (meters)", min_value=0.1, value=5.0, step=0.1)
    load = st.number_input("Point Load (kN)", min_value=0.1, value=10.0, step=0.1)

    if st.button("Calculate"):
        if beam_length <= 0 or load <= 0:
            st.error("Please enter positive values for beam length and load.")
            return

        x, shear, moment, R1, max_moment = calculate_beam_response(beam_length, load)

        st.markdown("### Results:")
        st.write(f"Reactions at supports: R1 = R2 = **{R1:.2f} kN**")
        st.write(f"Maximum bending moment: **{max_moment:.2f} kNm** (at center of beam)")

        plot_diagrams(x, shear, moment)

if __name__ == "__main__":
    main()
