# A Real-Time Fatigue Estimation System Using IMU for Athlete Monitoring

## Overview
This application is designed to calculate athlete stamina and fatigue status in real-time based on IMU (Inertial Measurement Unit) sensor data. The program processes accelerometer and gyroscope sensor data to provide real-time monitoring of physical condition, stamina consumption, and fatigue levels with visualization and analysis capabilities.

## Features
- **Real-time IMU Data Processing**: Processes accelerometer and gyroscope data from IMU sensors
- **Athlete Performance Monitoring**: Real-time calculation of stamina and fatigue status for athletes
- Composite acceleration and jerk calculation from 3-axis sensor data
- Signal filtering using Butterworth low-pass filter for noise reduction
- Resting Energy Expenditure (REE) calculation using Ten-Haaf equation
- Dynamic stamina consumption and recovery calculation with adaptive algorithms
- Real-time data visualization with interactive graphs
- Calorie expenditure estimation for training analysis

## Installation
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python main.py
```

### Command Line Arguments
```bash
python main.py --data your_data.csv --weight 65 --height 1.70 --age 30 --output result.png
```

### Arguments Description
- `--data`: Path to data file (default: test_data.csv)
- `--weight`: Body weight in kg (default: 70)
- `--height`: Height in meters (default: 1.78)
- `--age`: Age in years (default: 25)
- `--output`: Output file path (default: fatigue_analysis.png)

## Algorithm & Core Formula

The core HP (Hit Point) calculation follows this mathematical model:

$$\mathrm{HP}_n = \min \left(\mathrm{HP}_{n-1} - \underbrace{\mathrm{EE}_n \cdot \mathrm{EE\_increase}_n}_{\text{Stamina depletion term}} + \underbrace{\mathrm{heal}_n \cdot \mathrm{heal\_increase}_n}_{\text{Recovery term}}, \mathrm{sup\_HP}_{n-1}\right)$$

Where:
- $\mathrm{HP}_n$: Health Points at time step n
- $\mathrm{EE}_n$: Energy Expenditure at time step n
- $\mathrm{EE\_increase}_n$: Energy expenditure amplification factor
- $\mathrm{heal}_n$: Base recovery rate
- $\mathrm{heal\_increase}_n$: Recovery amplification factor
- $\mathrm{sup\_HP}_{n-1}$: Maximum HP limit at time step n-1

### Key Components:
1. **Energy Expenditure (EE)**: `EE = std × REE × max_score`
2. **REE Calculation**: Ten-Haaf equation for basal metabolic rate
3. **Amplification Factors**: Based on consecutive exercise/recovery periods
4. **Adaptive HP Ceiling**: Dynamic maximum HP that adjusts based on fatigue accumulation

## Input Data Format
CSV file must contain the following columns:
- Accel1X, Accel1Y, Accel1Z: Acceleration data
- Gyro1X, Gyro1Y, Gyro1Z: Gyroscope data

## Output
- Graphs showing stamina consumption, exercise intensity, and recovery
- Final HP value
- Estimated calorie expenditure

## Project Structure
```
├── main.py                # Main execution file
├── data_preprocessing.py  # Data preprocessing module
├── fatigue_calculator.py  # Fatigue calculation module
├── visualization.py       # Visualization module
├── config.py             # Configuration file
├── requirements.txt      # Dependencies
├── test_data.csv        # Sample test data
└── README.md           # This file
```

## Module Description

### data_preprocessing.py
- Data loading and preprocessing
- Accelerometer and gyroscope data conversion
- Signal filtering operations

### fatigue_calculator.py
- Basal metabolic rate calculation
- Fatigue and recovery computation
- Exercise intensity calculation

### visualization.py
- Graph creation and display
- Result visualization

### config.py
- Application configuration management
- Default value definitions

## Development & Customization
To modify settings, edit `config.py`. Each module is independent, allowing for individual extension and modification.