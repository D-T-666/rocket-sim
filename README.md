# rocket-sim

Super minimal, 1D rocket launch and landing simulation.

![a demo plot of the simulation data](/plots/fig-1609936940.png)

## features:
- [x] takeoff
- [x] hover
  - [x] PID controll
- [x] landing
  - [x] distance-till-zero-velocity calculation
    - [ ] basic
    - [ ] accounting for drag*
  - [ ] time-till-ignition and time-till-touchdown calculation
    - [x] basic
    - [ ] accounting for fuel mass loss
    - [ ] accounting for drag*
  - [x] smoothened  touchdown
- [ ] smooth (realistic) throttling
- [ ] drag*
  - [ ] basic
  - [ ] accounting for exhaust plumes
- [ ] setting limits
  - [ ] lift off velocity
  - [ ] lift off acceleration
  - [ ] maximum altitude
  - [ ] landing velocity
  - [ ] landing acceleration
- [ ] real rocket numbers*
  - [ ] New Shepard*
  - [ ] Starship*
  - [ ] Falcon 9*