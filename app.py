import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calc_point_load_center(beam_length, load):
    a = beam_length / 2
    R1 = R2 = load / 2

    x = np.linspace(0, beam_length, 500)
    shear = np.piecewise(x, [x < a, x >= a], [lambda x: R1, lambda x: -R2])
    moment = np.piecewise(x, [x < a, x >= a],
                          [lambda x: R1 * x, lambda x: R1 * x - load * (x - a)])

    max_moment = (load * beam_length) / 4
    return x, shear, moment, R1, max_moment

def calc_point_load_anywhere(beam_length, load, load_pos):
    a = load_pos
    b = beam_length - a
    R1 = load * b / beam_length
    R2 = load * a / beam_length

    x = np.linspace(0, beam_length, 500)
    shear = np.piecewise(x,
                         [x < a, x >= a],
                         [lambda x: R1,
                          lambda x: R1 - load])
    moment = np.piecewise(x,
                          [x < a, x >= a],
                          [lambda x: R1 * x,
                           lambda x: R1 * x - load * (x - a)])

    max_moment = max(R1 * a, R2 * b)  # Approximate max moment at load point
    return x, shear, moment, R1, max_moment

def calc_udl(beam_length, load):  # load = total uniform load in kN
    w = load / beam_length  # load per unit length (kN/m)
    R1 = R2 = load / 2

    x = np.linspace(0, beam_length, 500)
    shear = w * (beam_length/2 - x)
    moment = (w * x / 2) * (beam_length - x)

    max_moment = (w * beam_length**2) / 8
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
    st.title("🔧 Beam Load Calculator (Simply Supported Beam)")

    beam_length = st.number_input("Beam Length (meters)", min_value=0.1, value=5.0, step=0.1)

    load_type = st.selectbox("Select Load Type", 
                             ("Point Load at Center", "Point Load at Arbitrary Position", "Uniformly Distributed Load (UDL)"))

    # Dynamic inputs based on load type
    if load_type == "Point Load at Center":
        load = st.number_input("Point Load (kN)", min_value=0.1, value=10.0, step=0.1)
        load_pos = beam_length / 2  # fixed center

    elif load_type == "Point Load at Arbitrary Position":
        load = st.number_input("Point Load (kN)", min_value=0.1, value=10.0, step=0.1)
        load_pos = st.number_input("Load Position from Left Support (m)", min_value=0.0, max_value=beam_length, value=beam_length/2, step=0.1)

    else:  # UDL
        total_load = st.number_input("Total Uniform Load (kN)", min_value=0.1, value=20.0, step=0.1)
        load = total_load
        load_pos = None

    # Live input preview
    st.markdown("### Input Preview:")
    st.write(f"Beam Length: **{beam_length:.2f} m**")
    if load_type == "Point Load at Center":
        st.write(f"Load Type: Point Load at Center")
        st.write(f"Load Magnitude: **{load:.2f} kN**")
        st.write(f"Load Position: Center (at {load_pos:.2f} m)")
    elif load_type == "Point Load at Arbitrary Position":
        st.write(f"Load Type: Point Load at Arbitrary Position")
        st.write(f"Load Magnitude: **{load:.2f} kN**")
        st.write(f"Load Position: **{load_pos:.2f} m** from left support")
    else:
        st.write(f"Load Type: Uniformly Distributed Load (UDL)")
        st.write(f"Total Load: **{load:.2f} kN** spread over the entire beam")

    if st.button("Calculate"):
        if beam_length <= 0 or load <= 0:
            st.error("Please enter positive values for beam length and load.")
            return

        if load_type == "Point Load at Center":
            x, shear, moment, R1, max_moment = calc_point_load_center(beam_length, load)
        elif load_type == "Point Load at Arbitrary Position":
            if load_pos <= 0 or load_pos >= beam_length:
                st.error("Load position must be within the beam length (0 < position < beam length).")
                return
            x, shear, moment, R1, max_moment = calc_point_load_anywhere(beam_length, load, load_pos)
        else:
            x, shear, moment, R1, max_moment = calc_udl(beam_length, load)

        st.markdown("### Results:")
        st.write(f"Reactions at supports: R1 = R2 = **{R1:.2f} kN**")
        st.write(f"Maximum bending moment: **{max_moment:.2f} kNm**")

        plot_diagrams(x, shear, moment)

if __name__ == "__main__":
    main()
