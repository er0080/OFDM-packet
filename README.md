# OFDM Packet Transceiver

A GNU Radio flowgraph implementing OFDM-based packet transmission and reception over virtual network (TUN/TAP) interfaces. Designed for loopback testing — the TX output feeds directly into the RX input with no RF hardware required.

**Author:** Barry Duggan
**License:** GPL-3.0
**GNU Radio version:** 3.10.9.2

---

## Overview

The flowgraph (`Pkt_8.grc`) creates two independent packet paths, each backed by a TAP network interface (`tnc0`, `tnc1`). Packets injected into either interface are CRC-stamped, OFDM-modulated, demodulated, CRC-checked, and delivered to the opposite interface — making the system function as a simulated wireless link between two virtual network adapters.

Path 1 includes an additional access-code correlator branch that exposes the raw demodulated bit stream for inspection.

### Signal Flow (per path)

```
TAP interface (tnc0/tnc1)
  → CRC-32 append
  → Protocol formatter  (prepends access-code header)
  → PDU → tagged stream (header and payload separately)
  → Tagged stream mux
  → OFDM TX  (FFT=64, CP=16, BPSK header / QPSK payload)
       ↓  [loopback]
  → OFDM RX
  → Tagged stream → PDU
  → CRC-32 check
  → TAP interface (cross-delivered) + message debug logger
```

### Key Parameters

| Parameter | Value |
|-----------|-------|
| FFT size | 64 |
| Cyclic prefix | 16 samples |
| Header modulation | BPSK (1 bit/symbol) |
| Payload modulation | QPSK (2 bits/symbol) |
| Occupied carriers | `(-2,-1,1,3)` / `(-3,-1,1,2)` |
| Pilot carriers | `(-3,2)` / `(-2,3)` |
| Access code | `11100001010110101110100010010011` |
| CRC | 32-bit, poly 0x4C11DB7, reflected I/O |
| MTU | 576 bytes |

---

## Requirements

- GNU Radio 3.10.x with the following OOT modules (included in a standard install):
  - `gnuradio-digital`
  - `gnuradio-blocks`
  - `gnuradio-pdu`
  - `gnuradio-network`
- Python 3
- Linux with TUN/TAP kernel support
- Root or `CAP_NET_ADMIN` privilege (to open TAP devices)

---

## Setup

The flowgraph opens two TAP interfaces at startup. Create them before running:

```bash
sudo ip tuntap add dev tnc0 mode tap
sudo ip tuntap add dev tnc1 mode tap
sudo ip link set tnc0 up
sudo ip link set tnc1 up
```

Assign addresses if you want to send real IP traffic across the link:

```bash
sudo ip addr add 10.0.0.1/24 dev tnc0
sudo ip addr add 10.0.0.2/24 dev tnc1
```

---

## Running

```bash
python3 pkt_8.py
```

Press **Enter** to stop cleanly, or send `SIGINT` / `SIGTERM`.

### Testing the link

With the flowgraph running and addresses assigned:

```bash
ping -I tnc0 10.0.0.2
```

Successfully received packets (CRC pass) are printed to stdout by the message debug block.

---

## Files

| File | Description |
|------|-------------|
| `Pkt_8.grc` | GNU Radio Companion flowgraph (edit this, not the .py) |
| `pkt_8.py` | Auto-generated Python executable — regenerate via GRC after edits |
| `*.dat` | Intermediate signal probe outputs written when `log=True` on the OFDM blocks (e.g. `tx-signal.dat`, `post-payload-eq.dat`) |

---

## Modifying the Flowgraph

Open `Pkt_8.grc` in GNU Radio Companion, make changes, then regenerate:

- **GUI:** Run → Generate (F5), then run `python3 pkt_8.py`
- **CLI:** `grcc Pkt_8.grc` (produces `pkt_8.py`)

Do not edit `pkt_8.py` directly — it will be overwritten on the next generate.
