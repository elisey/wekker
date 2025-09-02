# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Wekker is a smart alarm clock system designed for Raspberry Pi that integrates physical controls, radio streaming, and home automation via MQTT. The system features:

- Hardware abstraction layer (HAL) supporting different platforms (GPIO, file-based testing)
- Music playback with radio streaming via mpg123 and file-based alarm sounds
- Volume control with analog input via PCF8591 ADC and ALSA mixer
- MQTT integration for Home Assistant compatibility
- Physical controls: alarm switch, radio switch, band switch, and analog tune knob

## Architecture

The application follows a modular architecture:

- `src/app.py`: Main application orchestrating all components
- `src/hal/`: Hardware abstraction layer with factory pattern for different platforms
- `src/music/`: Audio playback system with radio and file players
- `src/volume_control/`: Analog volume control with ADC reading and ALSA control
- `src/smarthome/`: MQTT client for Home Assistant integration
- `src/settings.py`: Configuration management from `~/.config/wekker/settings.ini`

Key patterns:
- Factory pattern for HAL selection (`get_hal()`)
- Event-driven architecture with hardware input callbacks
- Separate player utilities for different audio backends (mpg123, cvlc)
- Settings loaded from user config directory

## Development Commands

Use `task` (Taskfile.yaml) for all development workflows:

```bash
# Code quality and formatting
task lint          # Run ruff linting checks
task format        # Format code with ruff 
task format-check  # Check if code needs formatting (dry-run)
task lint-fix      # Auto-fix linting issues where possible
task check         # Run all code quality checks (lint + format-check)

# Deployment and testing
task run           # Deploy to Pi and run with live logs
task remote:deploy # Deploy code to Raspberry Pi (see tasks/Taskfile.remote.yml)
```

The project uses ruff for both linting and formatting with configuration in `pyproject.toml`.

## Hardware Setup

The system is designed for Raspberry Pi with:
- I2C ADC (PCF8591) for analog volume control
- GPIO inputs for switches (alarm, radio, band)
- I2S audio output via MAX98357A amplifier
- ALSA audio system with custom `/etc/asound.conf`

Hardware abstraction allows testing on non-Pi systems using file-based HAL implementation.

## Configuration

Settings are loaded from `~/.config/wekker/settings.ini` with MQTT configuration for Home Assistant integration. Use `settings.ini.example` as a template.

## Media and Radio

Radio stations are defined in `streams.txt`. The system supports multiple radio formats via different player utilities (mpg123 for MP3 streams, cvlc as fallback).

Audio files for alarms are managed by `MediaStorage` class with predefined media types (GROUNDHOG for alarm, KRIK for error).
