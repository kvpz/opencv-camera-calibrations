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

This will create two executables in the `build` directory:
- `camcalib`: Single camera calibration program
- `3calibration`: Three-camera stereo calibration program

### Running the Single Camera Calibration Program

You can run the `camcalib` executable from the `build` directory. Usage details for the program itself will depend on its implementation.

### Running the Three-Camera Calibration Program

The `3calibration` program calibrates three cameras simultaneously in a stereo setup. It requires synchronized images from all three cameras showing the same chessboard pattern.

#### Command-line Usage:

```bash
./3calibration -w=<board_width> -h=<board_height> [options] <input_file>
```

**Required Parameters:**
- `-w=<width>`: Number of inner corners horizontally on the chessboard
- `-h=<height>`: Number of inner corners vertically on the chessboard  
- `<input_file>`: Text file listing all calibration images (must be divisible by 3)

**Optional Parameters:**
- `-s=<size>`: Square size in real units (default: 1.0)
- `-o=<output>`: Output filename (default: out_camera_data.yml)
- `-zt`: Assume zero tangential distortion
- `-a=<ratio>`: Fix aspect ratio (fx/fy)
- `-p`: Fix principal point at image center

**Example:**
```bash
./3calibration -w=9 -h=6 -s=0.025 -o=calibration_results.yml image_list.txt
```

#### Input File Format:

The input file should list images in groups of 3 (one from each camera), with each line containing one image path. Example:

```
left_image_001.jpg
center_image_001.jpg
right_image_001.jpg
left_image_002.jpg
center_image_002.jpg
right_image_002.jpg
...
```

The program expects images to be grouped sequentially by camera position for each capture session.

## Calibration Programs Overview

This project utilizes two primary C++ calibration programs, both adapted from OpenCV examples:

*   **`calibration` program:** This program is typically used for calibrating a single camera. It takes images of a known pattern (like a chessboard) from different angles to determine the camera's intrinsic parameters (focal length, principal point, distortion coefficients) and extrinsic parameters (rotation and translation relative to the pattern).

*   **`3calibration` program:** This program is designed for calibrating a stereo camera setup or multiple cameras. It extends the single-camera calibration by finding the relative poses (rotation and translation) between the cameras, which is crucial for applications like 3D reconstruction or stereo vision.

## Best Practices for Calibration Image Capture

Proper image capture is crucial for successful multi-camera calibration. Follow these guidelines for optimal results:

### Equipment Requirements

1. **Chessboard Pattern:**
   - Use a high-quality printed chessboard with precise square dimensions
   - Recommended size: 9x6 inner corners (10x7 squares) for good detection
   - Mount on a rigid, flat surface (foam board, cardboard, or metal plate)
   - Ensure the chessboard is perfectly flat without wrinkles or distortions

2. **Lighting:**
   - Use diffuse, even lighting to minimize shadows and reflections
   - Avoid direct sunlight or harsh artificial lighting
   - Ensure consistent lighting throughout the capture session

### Camera Synchronization

**Critical:** All three cameras must capture the exact same moment to ensure the chessboard is in identical position across all views.

- Use hardware synchronization if available (external trigger)
- If using software synchronization, minimize delay between captures
- Verify synchronization by checking that the chessboard (or any object) position matches across all three images

### Capture Methodology

1. **Coverage Requirements:**
   - Capture 25-50 synchronized image sets (3 images per set)
   - Focus on the overlapping regions between cameras where stereo matching will occur

2. **Chessboard Positioning:**
   - **Distance variation:** Capture at near, medium, and far distances
   - **Angle variation:** Tilt the board in different directions (pitch, yaw, roll)
   - **Position variation:** Move the board to different areas of the overlapping field of view
   - **Orientation variation:** Rotate the board to different orientations

3. **Specific Positions to Capture:**
   - **Center positions:** Board centered in the overlapping region
   - **Edge positions:** Board near the edges of the overlapping area
   - **Corner positions:** Board in the corners of the overlapping field of view
   - **Angled positions:** Board tilted at 15°, 30°, 45° angles
   - **Close-up positions:** Board filling most of the frame
   - **Distant positions:** Board occupying ~20% of the frame

### Image Quality Guidelines

1. **Focus and Sharpness:**
   - Ensure all cameras are properly focused
   - Avoid motion blur - use sufficient shutter speed
   - Check that chessboard corners are clearly visible and sharp

2. **Exposure:**
   - Avoid over-exposure (blown out whites) and under-exposure (lost details)
   - Use consistent exposure settings across all cameras
   - Ensure the chessboard pattern has good contrast

3. **Chessboard Visibility:**
   - The entire chessboard must be visible in all three cameras
   - No occlusion of corner squares
   - Maintain good contrast between black and white squares

### File Organization

1. **Naming Convention:**
   ```
   capture_001_left.jpg
   capture_001_center.jpg
   capture_001_right.jpg
   capture_002_left.jpg
   capture_002_center.jpg
   capture_002_right.jpg
   ...
   ```

2. **Image List File:**
   Create a text file listing images in groups of 3:
   ```
   capture_001_left.jpg
   capture_001_center.jpg
   capture_001_right.jpg
   capture_002_left.jpg
   capture_002_center.jpg
   capture_002_right.jpg
   ```

### Validation During Capture

1. **Real-time Checking:**
   - Verify corner detection works on sample images
   - Check that all cameras detect the same number of corners
   - Ensure good distribution of chessboard positions

2. **Quality Assessment:**
   - Review captured images for sharpness and visibility
   - Verify synchronization between cameras
   - Check for adequate coverage of the calibration volume

### Common Pitfalls to Avoid

- **Insufficient overlap:** Chessboard not visible in all cameras
- **Poor synchronization:** Chessboard in different positions across cameras
- **Limited coverage:** Not enough variation in board positions and angles
- **Motion blur:** Camera or board movement during capture
- **Inconsistent lighting:** Changing illumination between captures
- **Too few images:** Insufficient data for robust calibration (minimum 20 sets)

Following these guidelines will ensure high-quality calibration data and robust multi-camera calibration results.

## Calibration Method Comparison

### Stereo Calibration Procedure (2-Camera Setup)

**Approach:**
- Uses OpenCV's `cv::stereoCalibrate` function 
- Two-stage process: individual camera calibration + stereo calibration
- Designed for exactly 2 cameras (left/right configuration)

**Process:**
1. **Individual calibration** for each camera using `cv::calibrateCamera`
   - Captures multiple chessboard images per camera
   - Outputs intrinsic matrix (K) and distortion coefficients (D)

2. **Stereo calibration** using `cv::stereoCalibrate`
   - Captures synchronized chessboard images from both cameras simultaneously
   - Inputs: 2D corner points from both cameras, 3D world coordinates, K and D matrices
   - Outputs: Rotation matrix (R) and translation vector (T) describing transformation from right to left camera

**Key Characteristics:**
- **True 3D model**: Provides exact physical properties and spatial arrangement
- **Handles parallax correctly**: Accounts for 3D baseline between cameras
- **High geometric accuracy**: Superior to homography-based methods
- **Production-ready**: Documented as the recommended approach for the videostitcher

### 3-Camera Calibration Method

**Approach:**
- Uses custom `3calibration.cpp` program adapted from OpenCV samples
- Extends stereo calibration to handle 3 horizontally aligned cameras
- Pairwise stereo calibration approach

**Process:**
1. **Individual calibration** for all 3 cameras (left, center, right)
   - Same as stereo method but for 3 cameras
   - Outputs K and D matrices for each camera

2. **Pairwise stereo calibration**:
   - **Left-Center pair**: `stereoCalibrate` between cameras 1 and 2
   - **Right-Center pair**: `stereoCalibrate` between cameras 1 and 3
   - Center camera serves as reference coordinate system

#### Image Collection Strategy for 3-Camera Setup

**Synchronized Capture Requirements:**
- All three cameras must capture the exact same moment simultaneously
- **Important**: The chessboard does NOT need to be visible in all three cameras at once
- Use hardware triggers or minimize software synchronization delays

**Pairwise Calibration Approach:**
The 3-camera algorithm works by performing two separate stereo calibrations:
1. **Left-Center stereo pair**: Uses images where both left and center cameras see the chessboard
2. **Right-Center stereo pair**: Uses images where both right and center cameras see the chessboard

**Optimal Capture Strategy for Large Baseline Setups:**

1. **Left-Center Image Sets** (~40% of total captures):
   - Position chessboard in the left-center overlap region
   - **Required**: Both left and center cameras must see the chessboard clearly
   - **Optional**: Right camera doesn't need to see the chessboard (but still captures)
   - Focus on positions that maximize left-center stereo geometry

2. **Right-Center Image Sets** (~40% of total captures):
   - Position chessboard in the right-center overlap region
   - **Required**: Both right and center cameras must see the chessboard clearly
   - **Optional**: Left camera doesn't need to see the chessboard (but still captures)
   - Focus on positions that maximize right-center stereo geometry

3. **Individual Camera Enhancement Sets** (~20% of total captures):
   - Position chessboard for optimal individual camera calibration
   - Can focus on single camera's full field of view
   - Helps improve intrinsic parameter accuracy
   - Other cameras don't need to see the chessboard

**Center Camera Priority:**
- The center camera acts as the reference coordinate system
- It should see the chessboard in approximately 80% of all captures
- Critical for establishing the common reference frame between left and right cameras

**Large Baseline Advantages:**
- Wide baselines provide better geometric constraints for stereo calibration
- More accurate depth estimation and camera pose relationships
- Don't force all cameras to see a distant chessboard - it's counterproductive

**Position Distribution:**
- **Near field** (close to cameras): 25% of captures
- **Mid field** (optimal working distance): 50% of captures  
- **Far field** (maximum detection distance): 25% of captures

**Angle Variations:**
- **Frontal**: Chessboard parallel to camera plane (30% of captures)
- **Tilted**: Various pitch/yaw angles (50% of captures)
- **Extreme angles**: Near maximum detection limits (20% of captures)

**Quality Verification:**
- Verify corner detection succeeds in all three cameras for each capture
- Check that the number of detected corners matches across all cameras
- Ensure good contrast and sharpness in all three views
- Monitor for any camera-specific issues (exposure, focus, occlusion)

#### GStreamer Pipeline Commands for Video Capture

This section provides the GStreamer pipeline commands for capturing synchronized video recordings from the three cameras for calibration purposes.

**Pipeline Commands:**

[Pipeline commands will be added here]

**Key Characteristics:**
- **Center camera as reference**: Identity rotation matrix for center camera
- **Synchronized capture requirement**: All 3 cameras must capture simultaneously
- **Pairwise relationships**: Establishes R12 and R13 transformation matrices
- **Code limitation**: Current videostitcher code only supports 2 cameras

### Critical Differences

| Aspect | Stereo Calibration | 3-Camera Calibration |
|--------|-------------------|---------------------|
| **Camera Count** | Exactly 2 cameras | 3 cameras (left, center, right) |
| **Calibration Pairs** | 1 stereo pair | 2 stereo pairs (left-center, right-center) |
| **Reference Frame** | Left camera reference | Center camera reference |
| **OpenCV Function** | `cv::stereoCalibrate` | `cv::stereoCalibrate` (called twice) |
| **Implementation** | Documented in videostitcher | Custom `3calibration.cpp` program |
| **Current Support** | Fully supported | **Not supported** - code hardcoded for 2 cameras |
| **Synchronization** | 2-camera sync required | 3-camera sync required (more complex) |

### Practical Implications

1. **Stereo calibration** is the **current production method** for the videostitcher plugin
2. **3-camera calibration** is **experimental** and requires code modifications to `StitchingComponents` class
3. Both methods use the same fundamental `cv::stereoCalibrate` function - the difference is in how many times it's called and how the results are organized
4. The 3-camera method is more complex due to synchronization requirements and the need to establish a common coordinate system

The documentation strongly emphasizes that `stereoCalibrate` is superior to homography-based methods because it provides a true 3D model that correctly handles parallax, while homography only provides 2D image alignment.

### Advantages of stereoCalibrate vs. Homography

**3D Model Benefits:**
- **Intrinsic Matrices (K)**: Defines internal optical properties of each camera (focal length, sensor center)
- **Distortion Coefficients (D)**: Models physical imperfections and warping of each lens
- **Rotation Matrix (R)**: Exact 3D rotation (roll, pitch, yaw) between cameras
- **Translation Vector (T)**: Exact 3D position (x, y, z) that separates cameras, defining their baseline

**Comparison Summary:**

| Feature | Reusing Homography | Using `stereoCalibrate` |
| :--- | :--- | :--- |
| **Core Idea** | 2D Image Alignment | 3D Model-Based Reconstruction |
| **What it Represents** | A 2D mapping that aligns one image plane with another | The true physical properties and 3D arrangement of the cameras |
| **Parallax** | Handles it poorly, causing artifacts and ghosting | Handles it correctly, resulting in a clean, stable stitch |
| **Result** | A fast but geometrically flawed stitch | A fast, stable, and geometrically correct stitch |
| **Best For** | Quick approximations, mostly flat scenes | High-quality, real-time video from a fixed multi-camera rig |

## Attribution

The C++ calibration programs in this repository are based on examples from the OpenCV library:

*   `3calibration.cpp` originated from: [https://github.com/opencv/opencv/blob/4.10.0/samples/cpp/3calibration.cpp](https://github.com/opencv/opencv/blob/4.10.0/samples/cpp/3calibration.cpp)
*   Other `camera_calibration` C++ programs originated from: [https://github.com/opencv/opencv/blob/4.10.0/samples/cpp/calibration.cpp](https://github.com/opencv/opencv/blob/4.10.0/samples/cpp/calibration.cpp)
