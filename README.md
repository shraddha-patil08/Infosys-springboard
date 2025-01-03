# ANPR and ATCC for Smart Traffic Management 🚗 

## 🎯 Project Overview
This project implements an intelligent traffic management system designed for smart city environments, integrating Automatic Number Plate Recognition (ANPR) and Automatic Traffic Classification and Control (ATCC). Utilizing advanced Deep Learning and Object Detection techniques, the system automates traffic monitoring and control by recognizing vehicle number plates in real-time and classifying vehicles based on type. The ANPR module facilitates tasks such as toll collection, traffic rule enforcement, and vehicle tracking, while the ATCC module dynamically adjusts traffic control measures to optimize flow and reduce congestion. This solution enhances urban mobility, improves traffic efficiency, and supports smarter, safer city infrastructure.

### Key Features
- 📝 Automatic Number Plate Recognition (ANPR)
- 🚦 Automatic Traffic Classification and Control (ATCC)
- 📊 Data interpolation for accurate tracking
- 📈 Visualization capabilities

### Results
- see the video result : "https://drive.google.com/file/d/1tQjoaz0CrAbL-sfKNiE6HIdwONYYNAyN/view?usp=drive_link"

## 🏗️ Project Structure
```
├── number_plate_detection_model_training/  # Model training files
├── object_tracker/            # Main detection and vehicle tracking code
├── results/                  # Initial detection CSV files
├── testing/                 # Project testing files
├── add_missing_data.py     # Data interpolation script
├── main.py                 # Main execution file
├── requirements.txt        # Project dependencies
└── visualize.py           # Video visualization script
```

## 🚀 Workflow
1. Execute `main.py` to perform initial vehicle detection and generate CSV file in `results/` directory
2. Run `add_missing_data.py` to perform data interpolation and generate enhanced CSV file in `Interpolated_results/` directory
3. Run `visualize.py` to create visualization video using interpolated data, saved in `output_videos/` directory



## 🏃‍♂️ Running the Project


1. Replace the path to your input video and your desired output directory.

2. Run the main detection:
```bash
python main.py
```

3. Perform data interpolation:
```bash
python add_missing_data.py
```

4. Generate visualization:
```bash
python visualize.py
```

## 📄 License
ANPR and ATCC for Smart Traffic Management is released under the [MIT License](LICENSE), allowing you to freely use, modify, and distribute the project.
