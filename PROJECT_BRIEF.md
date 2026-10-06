# PROJECT BRIEF — AI Productivity Cube

> Canonical product definition. Only **accepted** content lives here. Research
> conclusions that are still provisional live in `DECISIONS.md` / `CURRENT_STATE.md`.

## 1. Product objective

A pocketable physical interface for a personal AI productivity agent: a small,
cube-like object that works in **Pocket Mode** and in **Desktop Mode** (on a dock).

The cube exists because it makes interacting with the agent **faster, more tactile,
more contextual and less distracting than pulling out a phone**.

## 2. User problem

Quick productivity interactions cost a phone unlock, an app switch and attention:

- capture an idea, create a task, save a reminder
- check the next calendar item, ask what is pending
- start a focus session, enter Do Not Disturb, change work/study context
- confirm an action, delegate a simple workflow to an agent

The user should do most of these **without opening a phone app**.

## 3. Product philosophy

> **The phone provides compute and connectivity.**
> **The cloud provides intelligence.**
> **The cube provides physical presence, context, interaction and low-friction access.**

It is **not** a Flipper Zero clone, a phone or smartwatch replacement, a sensor box,
a local-LLM computer, a smart-home controller or a fitness tracker.

## 4. Interaction model

### Six faces
- **Four display faces** around a rotation axis. Default contexts: `WORK`, `STUDY`,
  `AVAILABLE`, `DND` (user-configurable later).
- **Two interaction faces** at the ends of the rotation axis. They carry buttons,
  microphone port, status LED, dock contacts and magnetic alignment. Exact layout is
  a design output, not an input.

### Orientation is the interface
The display face pointing **up** selects the active context. An IMU detects it.
The IMU may also provide pickup, shake/tap, motion state, steps and desk/pocket
inference **only if they come naturally from the selected IMU**.

### Voice is push-to-talk
`hold button → speak → release → request sent → agent acts → haptic + display feedback`.
V1 never records continuously.

## 5. Modes

### Pocket Mode
Wi-Fi mostly off, BLE low-power, displays mostly idle, mic off until PTT, IMU in
low-power, MCU sleeping aggressively, haptics available, brief UI responses only.

```text
USER  holds button: "Remind me tomorrow morning to check the electronics order."
CUBE  → sends request
AGENT → creates reminder
CUBE  → buzz, shows:  ✓ SAVED / Tomorrow / 09:00   → back to low power
```

### Desktop Mode (docked)
External power, battery charging, richer display, Wi-Fi may stay on, agent / focus
status and pending items visible. The dock gives desktop presence **without making the
cube bigger**.

```text
WORK
01:27
FOCUS
3 pending
```

## 6. System responsibility split

| Layer | Responsibilities |
|---|---|
| **Cube** | displays, orientation, buttons, mic capture, haptics, BLE, optional Wi-Fi, battery management, lightweight state, local low-power logic, short-term buffering |
| **Phone** | internet gateway, authentication, permissions, background app, location, notifications, optional audio relay |
| **Cloud** | STT, LLM, productivity agent, memory, tools, workflows, integrations (Google Calendar/Tasks/Workspace, Notion, notes, reminders) |

The main LLM never runs on the MCU.

## 7. V1 scope

- Cube with 4 display faces, orientation sensing, PTT voice, haptics, BLE link to a phone
  app, optional Wi-Fi, rechargeable battery, magnetic dock with charging contacts.
- Bench prototype (Phase A) → integrated prototype (Phase B). PCB design starts only
  after TASK-001 is reviewed.

## 8. V1 non-goals

Camera, GPS, LTE, UWB, Raspberry Pi, AI accelerator, local LLM, touchscreen, keyboard,
unrelated environmental sensing, health tracking, always-on audio, facial recognition,
smart-home hub, dedicated step-counter IC. Step count may come from the IMU.

## 9. Future possibilities (parking lot)

NFC, camera / "what am I seeing?", speaker, mic array, wireless charging, UWB, desktop
USB data, capacitive touch, smarter dock. See `research/future_features.md`.
