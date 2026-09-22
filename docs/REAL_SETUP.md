# Real setup notes

1. Install Python 3.11 and the dependencies from `dtch1997/fly-api`.
2. Clone the upstream repositories.
3. Download the required FlyWire data under the location expected by the upstream experiment.
4. Run the upstream learning/navigation experiment first to verify the real stack.
5. Then adapt its per-step loop to `backend/server.py`.

The key upstream facts are documented in the repository README and learning report. Do not replace the adapter with random motion and call it neural activity.

For the first real integration, use the existing **olfactory learning + navigation** path:
- the REROLL object emits the rewarded odor cue;
- the fly's antennae sample the field;
- the LIF olfactory→MB network computes valence;
- the learned KC→MBON synapses alter that valence;
- the existing navigation controller moves the physical fly;
- reaching the REROLL target triggers the reward event;
- reward is injected into PAM DANs according to the upstream conditioning protocol;
- repeat.

A visual REROLL button can be rendered in Three.js, but its visual pixels should not be claimed to drive the published model unless a visual-CS pathway is actually connected.
