# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A GNU Radio OFDM packet communication system implementing a simulated one-way RF link between two TAP network interfaces (`tnc0` and `tnc1`). Authored by Barry Duggan. Early-stage prototype; ping works in both directions.

## How to Run

```bash
python3 pkt_8.py
```

Requires root or `CAP_NET_ADMIN` for TUN/TAP device access. Press Enter to stop cleanly.

Edit the flowgraph in GNU Radio Companion, then regenerate `pkt_8.py`:
- **GUI:** Run → Generate (F5)
- **CLI:** `grcc Pkt_8.grc`

Do not edit `pkt_8.py` directly — it is auto-generated from `Pkt_8.grc`.

## Architecture

The two paths are **asymmetric** — only one direction uses the OFDM RF simulation.

### tnc0 → tnc1 (RF path)
```
tnc0 → CRC-32 append → PDU-to-tagged-stream
     → OFDM TX (FFT=64, CP=16)
     → OFDM RX
     → tagged-stream-to-PDU → CRC check → tnc1 + message_debug
```
The `digital_crc_append_0` output feeds directly into `pdu_pdu_to_tagged_stream_0` (tag `packet_len_0`) without a protocol formatter. The OFDM TX block handles its own internal framing (sync preamble + header + payload).

### tnc1 → tnc0 (return path, no RF)
```
tnc1 → CRC-32 append → Protocol formatter (header/payload split)
     → PDU-to-tagged-stream (x2) → tagged-stream mux
     → bit repack (8→1) → [virtual sink/source] → access code correlator
     → bit repack (1→8) → tagged-stream-to-PDU → CRC check → tnc0
```
This path uses the access code correlator (`correlate_access_code_bb_ts`) for framing instead of OFDM. The protocol formatter and access code are only used here.

### Key Parameters
- **FFT size**: 64, **Cyclic prefix**: 16
- **Occupied carriers**: `(-4,-3,-2,-1,1,2,3,4)` — 8 carriers, single group, no DC
- **Pilot carriers**: `(-6,-5,5,6)` — 4 pilots
- **sync_word1 / sync_word2**: `None` (GNU Radio internal defaults)
- **Header mod**: BPSK | **Payload mod**: QPSK
- **CRC**: 32-bit, poly 0x4C11DB7, reflected I/O
- **Access code**: `11100001010110101110100010010011` (return path only)
- **MTU**: 576 bytes

### Buffer Sizing
Both `digital_ofdm_tx_0_0` and `digital_ofdm_rx_0_0` have `set_min_output_buffer(100000)`. This is required because `header_payload_demux` (internal to `ofdm_rx`) must buffer a complete packet before outputting — the default GNU Radio buffer is too small.

### Debug / Observation
- `blocks_tag_debug_0` monitors the OFDM RX output stream (display disabled by default, tag name `"Rx Packets"`)
- `blocks_message_debug_0` prints CRC-passing packets from the RF path to stdout
- `debug_log=False` on OFDM blocks (set to `True` to enable `.dat` probe files)

## Dependencies

- GNU Radio 3.10.x (`gnuradio.blocks`, `gnuradio.digital`, `gnuradio.pdu`, `gnuradio.network`, `gnuradio.fft`, `gnuradio.filter`)
- Python 3
- Linux TUN/TAP kernel support
