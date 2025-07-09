# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build System

This project uses CMake as the build system. To build the camera calibration programs:

```bash
mkdir build
cd build
cmake ..
make
```

This creates the `camcalib` executable in the `build` directory.

## Camera Calibration Programs

The project contains multiple OpenCV-based camera calibration programs in `src/`:

- **`camera_calibration_v4_11_0.cpp`**: Single camera calibration (default build target)
- **`3calibration.cpp`**: Three-camera stereo calibration for horizontally aligned cameras
- **`camera_calibration_v4_6_0.cpp`**: Legacy single camera calibration

The CMakeLists.txt currently builds `camera_calibration_v4_11_0.cpp` as the main `camcalib` executable.

## Python Scripts

The `scripts/` directory contains Python utilities:

- **`calibration_manager.py`**: Manages calibration metadata in YAML format
- **`cam_calibration.py`**: Python-based calibration utilities

Run Python scripts directly:
```bash
python scripts/calibration_manager.py
```

## Configuration and Data Structure

- **`config/`**: Contains calibration configuration files
  - `calibrations.yaml`: Metadata for camera calibrations including camera specs, dates, and parameters
  - `*.xml`: OpenCV calibration parameter files
- **`calibration-videos/`**: Source videos for calibration
- **`test-videos/`**: Test videos and extracted frames
- **`outputs/`**: Generated calibration results
- **`data/`**: Additional calibration data


## Dependencies

- OpenCV 4.x with core and aruco modules
- CMake 3.10+
- C++17 standard
- Python 3.x with PyYAML for scripts

## Common Calibration Workflow

1. Record calibration videos with chessboard patterns
2. Extract frames from videos
3. Run appropriate calibration program (`camcalib` for single camera, build `3calibration` for multi-camera)
4. Use `calibration_manager.py` to manage calibration metadata
5. Output calibration parameters to `outputs/` directory
