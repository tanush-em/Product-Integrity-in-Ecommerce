# Product Integrity Checker for E-Commerce

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A machine learning approach to detect and mitigate dark patterns in e-commerce platforms, focusing on misleading pricing strategies and manipulated rating systems.

## Project Overview

This project addresses two critical dark patterns prevalent across major e-commerce platforms (Amazon, Flipkart, IndiaMart, Alibaba, and Meesho):

1. **Misleading Product Information**: Detection of deceptive pricing strategies, particularly artificial price inflation followed by "discounts"
2. **Rating System Manipulation**: Analysis of rating distributions to identify potentially manipulated review systems

## Directory Structure

```
PRODUCT-INTEGRITY-IN-ECOMMERCE/
├── docs/
│   ├── Abstract_Description.docx
│   └── Sample Links.txt
├── img/
│   ├── amazon.png
│   ├── cross.png
│   ├── dbph.png
│   └── tick.jpg
├── notebooks/
│   ├── flagger_code.ipynb
│   ├── misleading_prices.ipynb
│   └── ratings_regulation.ipynb
├── app.py
├── dataset_untouched.zip
├── GRFmodel.pkl
├── README.md
└── user_data.xlsx
```

## Technical Implementation

### Data Collection and Processing
- High-level scraping of e-commerce platforms (primarily Amazon)
- Feature extraction including:
  - Product ID
  - Product name
  - Original and discounted prices
  - Rating distributions
  - Additional metadata

### Machine Learning Components
- **Price Analysis Model** (`misleading_prices.ipynb`)
  - Detects artificial price inflation patterns
  - Analyzes historical price trends
  - Flags suspicious discount patterns

- **Rating Analysis Model** (`ratings_regulation.ipynb`)
  - Evaluates rating distributions
  - Identifies suspicious rating patterns
  - Compares against established benchmarks

- **Pattern Detection System** (`flagger_code.ipynb`)
  - Combines insights from both models
  - Implements final decision logic
  - Generates integrity scores

### Application
The main application (`app.py`) serves as the integration point for all components and provides the interface for analysis results.

## Getting Started

### Prerequisites
- Python 3.7+
- Jupyter Notebook
- Required Python packages 

### Installation

1. Clone the repository
```bash
git clone https://github.com/username/PRODUCT-INTEGRITY-IN-ECOMMERCE.git
cd PRODUCT-INTEGRITY-IN-ECOMMERCE
```

2. Create and activate a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages

4. Extract the dataset
```bash
unzip dataset_untouched.zip
```

### Usage

1. Start with the Jupyter notebooks in the `notebooks/` directory to understand the analysis process:
   - `misleading_prices.ipynb` for price analysis
   - `ratings_regulation.ipynb` for rating system analysis
   - `flagger_code.ipynb` for the combined detection system

2. Run the main application:
```bash
python app.py
```

## Future Developments

- Browser extension implementation
- Real-time analysis capabilities
- Integration with additional e-commerce platforms
- Enhanced visualization of detected patterns
- API development for third-party integration

## Contributing

We welcome contributions! Please see Contributing Guidelines for details on how to submit pull requests, report issues, and contribute to the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- E-commerce platforms that provided data through their public interfaces
- Academic research on dark patterns in digital interfaces
- Open-source community for various tools and libraries used in this project

## Contact

For questions and feedback:
- Create an issue in this repository
- Contact the maintainers directly through their GitHub profiles

---

<div align="center">
A project aimed at fostering transparency in e-commerce through machine learning
</div>