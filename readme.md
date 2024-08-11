# Tesla Dashcam GUI

A graphical user interface for the [tesla_dashcam](https://github.com/ehendrix23/tesla_dashcam) command-line tool, designed to simplify the process of creating videos from Tesla dashcam and sentry mode footage.

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
6. [GUI Tabs and Options](#gui-tabs-and-options)
7. [Future Improvements](#future-improvements)
8. [Contributing](#contributing)
9. [License](#license)
10. [Acknowledgments](#acknowledgments)
11. [Disclaimer](#disclaimer)

## Introduction

Tesla Dashcam GUI is a user-friendly interface for the tesla_dashcam command-line tool. It allows Tesla owners to easily process and combine footage from their vehicle's cameras into a single video file. This tool is particularly useful for managing Sentry Mode and Dashcam recordings, providing an intuitive way to create comprehensive video clips from multiple camera angles.

## Features

- User-friendly interface for all major tesla_dashcam options
- Organized tabs for Main, Layout, Timestamp, Advanced, and Output options
- File and folder browsing for easy source and output selection
- Tooltips with performance impact information for each option
- Automatic detection and use of Apple Silicon ffmpeg if available
- Support for various video layouts (Fullscreen, Widescreen, Perspective, Cross, Diamond)
- Customizable timestamp overlay
- Video processing options (motion detection, speed adjustment, quality settings)
- GPU acceleration support (where available)

## Prerequisites

Before using Tesla Dashcam GUI, you need to install:

1. [tesla_dashcam](https://github.com/ehendrix23/tesla_dashcam)
2. ffmpeg

### Installing tesla_dashcam

```bash
pip install tesla_dashcam
```

### Installing ffmpeg

#### macOS
Using Homebrew:
```bash
brew install ffmpeg
```

#### Windows
1. Download ffmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract the downloaded file
3. Add the bin folder to your system PATH

#### Linux
Using apt (Debian/Ubuntu):
```bash
sudo apt update
sudo apt install ffmpeg
```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/gbgbgb8/tesla-dashcam-gui.git
   ```
2. Navigate to the project directory:
   ```bash
   cd tesla-dashcam-gui
   ```
3. Install required Python packages:
   ```bash
   pip install tkinter
   ```

## Usage

Run the GUI:

```bash
python3 tesla_dashcam_gui.py
```

## GUI Tabs and Options

The Tesla Dashcam GUI is organized into several tabs for easy navigation:

1. **Main Tab**
   - Source and output folder selection
   - Options for skipping existing files, deleting source files, and excluding subdirectories

2. **Layout Tab**
   - Video layout selection (Fullscreen, Widescreen, Perspective, Cross, Diamond)
   - Camera scaling and perspective options
   - Background color selection

3. **Timestamp Tab**
   - Timestamp display options
   - Font selection and customization
   - Timestamp positioning

4. **Advanced Tab**
   - Video quality and compression settings
   - FPS selection
   - Encoding options (x264, x265)
   - GPU acceleration toggle

5. **Output Options Tab**
   - Video merging options
   - Intermediate file handling
   - Speed adjustment (slow down or speed up)
   - Chapter offset settings

Each option in the GUI comes with a tooltip providing a brief explanation and potential performance impact.

## Future Improvements

- Add progress bar for video processing
- Implement save/load functionality for GUI settings
- Create installable package for easier distribution
- Add support for batch processing multiple events
- Implement dark mode for the GUI

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [ehendrix23](https://github.com/ehendrix23) for creating the original tesla_dashcam tool
- The Tesla community for their ongoing support and feedback
- This README was created with the assistance of [Claude.ai](https://www.anthropic.com)

## Disclaimer

This software is not officially affiliated with or endorsed by Tesla, Inc. Use this software at your own risk. Always ensure you have backups of your important dashcam footage before processing.