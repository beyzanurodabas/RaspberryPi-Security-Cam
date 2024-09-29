# Raspberry Pi Surveillance System

A motion-activated surveillance system using Raspberry Pi, camera module, and sensors.

## Features

- Motion detection and video capture
- Email alerts with video attachment
- Fire detection (basic implementation)
- Automatic file cleanup

## Requirements

- Raspberry Pi with camera module
- PIR motion sensor, fire sensor
- Python 3, picamera, RPi.GPIO, smtplib
- MP4Box

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   sudo apt-get update && sudo apt-get install -y gpac python3-picamera
   ```
3. Configure email settings in `surveillance_.py`

## Usage

Run:
python3 surveillance_.py
