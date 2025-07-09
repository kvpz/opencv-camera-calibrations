# Camera Calibration

This directory holds several programs for calibrating cameras and camera setups that will produce video streams that will be fed into a video stitching gstreamer plugin.

## Directory Structure

* `src/`: Contains the C++ and Python source code for camera calibration.
* `data/`: Contains calibration data, videos, and images.
* `config/`: Contains configuration files for the calibration programs.
* `scripts/`: Contains Python scripts for managing the calibration process.
* `build/`: Contains the build files for the C++ programs.
* `calibration-videos/`: Contains video files for calibration.
* `test-videos/`: Contains video files for testing the calibration.
* `outputs/`: Contains the output files from the calibration process.

## Usage

### Building the C++ Program

To build the C++ calibration program, navigate to the root of this directory and execute the following commands:

```bash
mkdir build
cd build
cmake ..
make
```

This will create an executable named `camcalib.x` in the `build` directory.

### Running the C++ Program

You can run the `camcalib.x` executable from the `build` directory. Usage details for the program itself will depend on its implementation.

### Running Python Scripts

The Python scripts in the `scripts/` directory can be run directly. For example:

```bash
python scripts/calibration_manager.py
```

Please refer to the individual Python scripts for their specific usage and arguments.
