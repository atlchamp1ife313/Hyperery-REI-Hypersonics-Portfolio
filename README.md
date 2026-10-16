# Hyperery REI (Hypersonics ReImagined)
## Technical Work Portfolio: Hypersonic Flow, High-Order CFD & Thermal Protection

**Founder & Lead R&D Engineer:** Hwang Ju (JJ)  
**Domain:** Advanced Aerospace, Defense, High-Performance Computing (HPC), and AI/ML Applications  

---

### OVERVIEW
This portfolio outlines representative computational and analytical research projects executed under **Hyperery REI**. It demonstrates advanced capabilities in solving non-linear governing equations, managing stiff chemical kinetics, and bridging aerodynamic loading to structural finite-element models under extreme flight regimes ($M > 5$).

---

### PORTFOLIO PROJECTS

#### Project 1: High-Order Discontinuous Galerkin (DG) & Flux Reconstruction for Hypersonic Re-Entry
* **Objective:** Develop high-order accurate numerical formulations to resolve extreme shock discontinuities and boundary layer interactions without introducing excessive artificial dissipation.
* **Technical Approach:**
  * Implemented high-order Discontinuous Galerkin (DG) and Flux Reconstruction (FR) methods for multi-species reactive Navier-Stokes equations.
  * Integrated custom, physics-informed Riemann solvers optimized for real-gas effects and high-enthalpy dissociation.
* **Deliverable / Output:** Validated convergence rates on benchmark supersonic wedge and double-wedge test cases; generated high-fidelity surface pressure and heat-flux distributions.

#### Project 2: Stiff Finite-Rate Chemical Kinetics & Algorithm Optimization in Exhaust Plumes
* **Objective:** Overcome numerical stiffness associated with rapid chemical reactions in high-speed rocket and scramjet exhaust plumes.
* **Technical Approach:**
  * Developed and integrated Implicit-Explicit (IMEX) Additive Runge-Kutta time-integration schemes.
  * Implemented point-wise analytical Jacobians to accelerate convergence and eliminate time-step restrictions caused by fast radical recombination chemistry.
* **Deliverable / Output:** Achieved significant speedups in computational turnaround time for multi-species reacting flow simulations in Linux/OpenFOAM and custom Python/C++ frameworks.

#### Project 3: Automated CFD-to-FEA Thermal-Structural Data Transfer Workflows
* **Objective:** Accurately map high-gradient aerodynamic heat fluxes, fluctuating surface pressures, and severe shear stresses from fluid domains to structural finite-element models.
* **Technical Approach:**
  * Built automated data-mapping pipelines between OpenFOAM/ParaView field data and structural solvers (Abaqus/ANSYS).
  * Implemented conservative interpolation algorithms to preserve global energy and momentum balances across non-matching mesh interfaces.
* **Deliverable / Output:** Provided structural engineers with precise thermal boundary conditions for analyzing thermal ablation, structural buckling, and material degradation under hypersonic flight conditions.

#### Project 4: Hessian-Based Anisotropic Mesh Adaptation for Aero-Optical Window Degradation
* **Objective:** Quantify the impact of severe thermal gradients and shock-layer density fluctuations on optical transmission and seeker-window performance.
* **Technical Approach:**
  * Utilized Hessian matrix eigenvalue analysis and refinement indicators to detect high-gradient flow features (e.g., bow shocks, shear layers).
  * Executed automated anisotropic mesh adaptation to concentrate resolution precisely where physical gradients demand it, minimizing overall grid size while maximizing solution accuracy.
* **Deliverable / Output:** Mapped refractive-index variations across the flow field to evaluate wavefront distortion and optical contrast constraints for high-altitude tracking systems.

---

### TECHNICAL TOOLKIT & COMPUTATIONAL ENVIRONMENT
* **Numerical Methods:** Discontinuous Galerkin (DG), Flux Reconstruction (FR), IMEX Runge-Kutta, Finite Volume, Anisotropic Mesh Adaptation, Hessian Eigenanalysis.
* **Physics Domains:** Hypersonic Aerothermodynamics, Chemical Non-Equilibrium, Thermal Ablation, Rocket Plumes, Aero-Optics.
* **Software & Languages:** OpenFOAM, ParaView, Abaqus, ANSYS, LS-DYNA, Python, C++, MATLAB, Linux/Ubuntu HPC clusters.

---
*© Hyperery REI (Hypersonics ReImagined). All rights reserved.*
