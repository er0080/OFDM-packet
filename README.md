# OFDM Packet Transceiver

A GNU Radio flowgraph implementing a simulated one-way RF link between two TAP network interfaces. The forward path (`tnc0 → tnc1`) uses OFDM modulation; the return path (`tnc1 → tnc0`) is a direct bit-stream path using access code correlation. Ping works in both directions.

**Author:** Barry Duggan
**License:** GPL-3.0
**GNU Radio version:** 3.10.9.2
**Status:** Early prototype

---

## How it works

The two directions of the link are intentionally asymmetric:

**tnc0 → tnc1 (OFDM RF path)**
```
tnc0 → CRC-32 → OFDM TX ──[simulated RF]──> OFDM RX → CRC check → tnc1
```

**tnc1 → tnc0 (return path, no RF simulation)**
```
tnc1 → CRC-32 → Protocol formatter → bit stream → access code correlator → CRC check → tnc0
```

The OFDM TX block handles its own internal framing (preamble + header + payload). No external protocol formatter is used on the RF path.

### OFDM Parameters

| Parameter | Value |
|-----------|-------|
| FFT size | 64 |
| Cyclic prefix | 16 samples |
| Occupied carriers | `(-4,-3,-2,-1,1,2,3,4)` — 8 carriers, single group |
| Pilot carriers | `(-6,-5,5,6)` |
| Header modulation | BPSK |
| Payload modulation | QPSK |
| Sync words | GNU Radio defaults (`None`) |
| CRC | 32-bit, poly 0x4C11DB7, reflected I/O |
| MTU | 576 bytes |

---

## Requirements

- GNU Radio 3.10.x (`gnuradio-digital`, `gnuradio-blocks`, `gnuradio-pdu`, `gnuradio-network`)
- Python 3
- Linux with TUN/TAP kernel support
- Root or `CAP_NET_ADMIN` privilege

---

## Setup

Create the TAP interfaces before running:

```bash
sudo ip tuntap add dev tnc0 mode tap
sudo ip tuntap add dev tnc1 mode tap
sudo ip link set tnc0 up
sudo ip link set tnc1 up
sudo ip addr add 10.0.0.1/24 dev tnc0
sudo ip addr add 10.0.0.2/24 dev tnc1
```

---

## Running

```bash
python3 pkt_8.py
```

Press **Enter** to stop, or send `SIGINT`/`SIGTERM`.

### Testing

```bash
ping -I tnc0 10.0.0.2   # forward path: OFDM
ping -I tnc1 10.0.0.1   # return path: access code correlator
```

CRC-passing packets on the OFDM path are printed to stdout by the message debug block.

---

## Files

| File | Description |
|------|-------------|
| `Pkt_8.grc` | GNU Radio Companion flowgraph — edit this |
| `pkt_8.py` | Auto-generated Python executable — do not edit directly |
| `*.dat` | Signal probe files written when `debug_log=True` on the OFDM blocks |

## Modifying the Flowgraph

```bash
gnuradio-companion Pkt_8.grc   # open and edit
grcc Pkt_8.grc                  # regenerate pkt_8.py from CLI
```
