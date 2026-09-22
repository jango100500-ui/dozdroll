# 🪰 Fly REROLL — real-connectome experiment shell

This package is the **honest next step** from the earlier visual prototype.

The target experiment is:

`START → fly chooses → reaches REROLL → reward/dopamine → plasticity → wait → next trial`

The human does **not** click REROLL.

## What is scientifically real

The intended simulator is based on the published FlyWire/Shiu whole-brain LIF work and the open `dtch1997/fly-api` learning/navigation implementation. That project reports:

- 139,255 FlyWire neurons / 50M+ synapses
- LIF spiking simulation
- dopamine-gated KC→MBON plasticity
- 5 reward pairings
- learned odor navigation with a physical fly body
- CPU-only operation

The exact published learning protocol uses an **olfactory conditioned stimulus**, not a visual HTML button. Therefore this package treats the REROLL target as an environmental object whose cue can be connected to the real olfactory CS. A future visual-CS implementation would be a different scientific experiment.

## Important

`backend/server.py` is **not pretending to be the connectome**. In `real` mode it refuses to invent neural results. It is the HTTP seam for the real simulator.

A `demo` mode exists only to verify that the Three.js page and HTTP bridge work.

## Run the UI smoke test

Terminal 1:

```bash
cd backend
FLY_SIM_MODE=demo python server.py
```

Terminal 2:

```bash
cd web
python -m http.server 8080
```

Open `http://localhost:8080`.

## Connect the real simulator

Use the upstream project:

https://github.com/dtch1997/fly-api

and the underlying published whole-brain model:

https://github.com/philshiu/Drosophila_brain_model

The upstream fly-api repository is the source of the learning protocol. Its README explicitly says there is no backprop/dataset: reward is a PAM dopamine teaching signal and plasticity is dopamine-gated LTD at KC→MBON synapses.

The adapter should expose only:

POST /start
POST /step {"dt_ms":250}
POST /stop

`/step` must return the **actual** body pose and an event only when the simulator's body/brain loop says the target was reached. The browser must never manufacture a press.

## Why this is not yet a single-file website

The real connectome data are large/licensed and the scientific simulator is Python/Brian2/MuJoCo, not a tiny JavaScript library. The browser is therefore the renderer/controller UI; the actual neural simulation belongs in the local/server process.

