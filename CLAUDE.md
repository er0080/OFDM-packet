# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a GNU Radio OFDM packet communication system implementing full packet TX/RX over TUN/TAP network interfaces. It is authored by Barry Duggan and runs in loopback mode (TX directly feeds RX) for development and testing.

## How to Run

```bash
python3 pkt_8.py
```

Requires root or network admin privileges for TUN/TAP device access (`tnc0`, `tnc1`).

The GRC flowgraph can be opened and modified in GNU Radio Companion:
```bash
gnuradio-companion Pkt_8.grc
```

After editing `Pkt_8.grc` in GNU Radio Companion, regenerate `pkt_8.py` via **Run > Generate** (or F5) in the GUI. Do not manually edit `pkt_8.py` — it is auto-generated from the `.grc` file.

## Architecture

The system has two independent packet paths (path 0 via `tnc0`, path 1 via `tnc1`) that each follow the same pipeline.

### TX Pipeline (per path)
```
TUN/TAP (network) → CRC-32 append → Protocol formatter (access code header)
  → PDU-to-tagged-stream (header + payload separately)
  → Tagged stream mux → OFDM TX (FFT=64, CP=16, BPSK header, QPSK payload)
```

### RX Pipeline (loopback from TX output)
```
OFDM RX → Tagged-stream-to-PDU → CRC check
  → TUN/TAP output + message debug logger
```

Path 1 also has an additional access code correlator branch that demodulates raw bits to a virtual sink (`demod_bits_1`).

### Key Parameters
- **FFT size**: 64, **Cyclic prefix**: 16
- **Occupied carriers**: `(-2,-1,1,3)` and `(-3,-1,1,2)`
- **Pilot carriers**: `(-3,2)` and `(-2,3)`
- **Access code**: `11100001010110101110100010010011` (32-bit)
- **Header mod**: BPSK | **Payload mod**: QPSK
- **CRC polynomial**: 0x4C11DB7 (32-bit)
- **MTU**: 576 bytes (TUN/TAP)

### Message Passing vs. Stream Connections
GNU Radio uses two connection types here:
- **Message/PDU connections** (async): CRC → formatter → PDU converters → CRC check → TUN/TAP
- **Stream connections** (synchronous): bit repack/mux chains, OFDM TX→RX loopback

### Debug Data Files
The `.dat` files in the repo root are probe/logging outputs from intermediate points in the signal chain (e.g., `tx-hdr.dat`, `post-payload-eq.dat`). They are populated when the flowgraph runs with logging enabled (`log=True` on OFDM blocks).

## Dependencies

- GNU Radio 3.10.x (`gnuradio.blocks`, `gnuradio.digital`, `gnuradio.pdu`, `gnuradio.network`, `gnuradio.fft`, `gnuradio.filter`)
- Python 3
- Linux TUN/TAP kernel support
