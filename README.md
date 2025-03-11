# Human-assembly-intention-recognition dataset
There are mainly three folders, namely dataset acquisition software, dataset annotatation sofrtware, and benchmark algorithms. The dataset details and acquisition can be found in https://mdx-box.github.io/MCV_Intention.
## 1. Dataset acquisition
The dataset acquisition software developed based on PyQT is capable of collecting data across six modalities: RGB, skeleton, depth, optical flow, infrared, and mask, in addition to a top-down perspective data. 
## 2. Dataset annotatation sofrtware
The dataset annotation software is primarily designed for detailed labeling of intent recognition datasets. The annotation labels can be manually defined by users or directly imported from an Excel file. If importing from Excel, the format should be structured as follows:

| Action      | Object      | Target        | Tool                 |
|-------------|-------------|---------------|----------------------|
| Reach       | Battery     | holder 1      | Screwdriver          |
| Pick        | Inner plane | holder 2      | Electric Screwdriver |
| Hold        | loader      | holder 3      | Hex Wrench           |
| Install     | Solar plane | holder 4      | Adjustable Spanner   |
| disassembly | Radiator    | Chassis       | others               |
| others      | Top plane   | Battery holder|                      |
|             | Screw       |               |                      |

## 3. Benchmark algorithms
