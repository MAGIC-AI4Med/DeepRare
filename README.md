# [Nature] DeepRare: An Agentic System for Rare Disease Diagnosis with Traceable Reasoning

<div style='display:flex; gap: 0.6rem; '>
<a href='https://arxiv.org/pdf/2506.20430'><img src='https://img.shields.io/badge/Arxiv-PDF-red'></a>
<a href='https://huggingface.co/datasets/Angelakeke/DeepRare'><img src='https://img.shields.io/badge/DeepRare-Database-blue'></a>
<!-- <a href='https://huggingface.co/datasets/Angelakeke/RaTE-Eval'><img src='https://img.shields.io/badge/RaTEEval-Benchmark-green'></a>  -->
<a href='http://deeprare.cn'><img src='https://img.shields.io/badge/DeepRare-WebApp-pink'></a>
<a href='https://creativecommons.org/licenses/by-nc/4.0/'><img src='https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey'></a>
</div>

## Overview
Rare diseases collectively affect over 300 million individuals worldwide, yet timely and accurate diagnosis remains a pervasive challenge. This is largely due to their clinical heterogeneity, low individual prevalence, and the limited familiarity most clinicians have with rare conditions. Here, we introduce DeepRare, the first rare disease diagnosis agentic system powered by a large language model (LLM), capable of processing heterogeneous clinical inputs. The system generates ranked diagnostic hypotheses for rare diseases, each accompanied by a transparent chain of reasoning that links intermediate analytic steps to verifiable medical evidence.

![](./figs/architecture.png)

DeepRare comprises three key components: a central host with a long-term memory module; specialized agent servers responsible for domain-specific analytical tasks integrating over 40 specialized tools and web-scale, up-to-date medical knowledge sources, ensuring access to the most current clinical information. This modular and scalable design enables complex diagnostic reasoning while maintaining traceability and adaptability. 

We evaluate DeepRare on eight datasets. The system demonstrates exceptional diagnostic performance among 2,919 diseases. In HPO-based evaluations, DeepRare significantly outperforms other 15 methods, like traditional bioinformatics diagnostic tools, LLMs, and other agentic systems, achieving an average Recall@1 score of 57.18% and surpassing the second-best method (Reasoning LLM) by a substantial margin of 23.79 percentage points. For multi-modal input scenarios, DeepRare achieves 70.60% at Recall@1 compared to Exomiser's 53.20% in 109 cases. Manual verification of reasoning chains by clinical experts achieves 95.40% agreements. Furthermore, the DeepRare system has been implemented as a user-friendly web application http://raredx.cn/doctor.

![](./figs/performance.png)

For more detailed about our pipeline, please refer to our paper.

## System requirements

### Hardware Requirements
- **RAM**: Minimum 16GB (32GB recommended)
- **Storage**: 100GB+ free disk space (SSD preferred)
- **GPU**: Optional but recommended for faster model inference
- **CPU**: Any modern 64-bit processor

### Software Requirements
- **OS**: Any 64-bit operating system
- **Java**: Version 21 or above
- **Python**: 3.8+ (for model inference)

**Note:** GPU is optional - models can run on CPU with slower performance. Exomiser tool requires the specified minimum resources for optimal functionality.

## LLM API Key Requirements
The system supports multiple LLM providers. You need to obtain an API key from at least one of the following:

#### OpenAI
- **How to obtain**: Sign up at [platform.openai.com](https://platform.openai.com)
- **Environment variable**: `OPENAI_API_KEY`

#### Anthropic Claude
- **How to obtain**: Sign up at [console.anthropic.com](https://console.anthropic.com)
- **Environment variable**: `ANTHROPIC_API_KEY`

#### Google Gemini
- **How to obtain**: Sign up at [ai.google.dev](https://ai.google.dev)
- **Environment variable**: `GOOGLE_API_KEY`

#### DeepSeek
- **How to obtain**: Sign up at [platform.deepseek.com](https://platform.deepseek.com)
- **Environment variable**: `DEEPSEEK_API_KEY`

#### Local Models (Optional)
- **Custom LLM Integration**: Support for locally hosted or custom LLM endpoints
- **Setup**: Modify `api/interface.py` to adapt your custom LLM provider
- **Implementation**: 
  - Extend the base LLM interface class in `api/interface.py`
  - Configure endpoint URL and authentication if needed


## Installation

1. **Clone the repository and install dependencies:**
   ```bash
   git clone https://github.com/MAGIC-AI4Med/DeepRare.git
   cd DeepRare
   pip install -r requirements.txt
   ```

2. **Setup ChromeDriver:**
   
   Download ChromeDriver that matches your Chrome browser version:
   - Visit [ChromeDriver Downloads](https://chromedriver.chromium.org/)
   - Download the version compatible with your Chrome browser
   - Extract the downloaded file

   **Install ChromeDriver (Linux/Mac):**
   
   Open terminal, navigate to the directory containing chromedriver, and run:
   ```bash
   sudo mv chromedriver /usr/local/bin/
   sudo chmod +x /usr/local/bin/chromedriver
   ```
   
   **Verify installation:**
   ```bash
   chromedriver --version
   ```

   **For Windows:**
   ```bash
   # Place chromedriver.exe in your desired location, e.g.:
   C:\chromedriver\chromedriver.exe
   ```
   **Note:** Make sure ChromeDriver version matches your installed Chrome browser version.

3. **Install Exomizer （If required Gene Part）:**

   Following [Online document](https://exomiser.readthedocs.io/en/latest/)
   
   **Linux/Mac:**
   ```bash
    # download the distribution (won't take long)
    wget https://data.monarchinitiative.org/exomiser/latest/exomiser-cli-14.1.0-distribution.zip
    # download the data (this is ~20GB and will take a while)
    wget https://data.monarchinitiative.org/exomiser/latest/2410_hg19.zip
    wget https://data.monarchinitiative.org/exomiser/latest/2410_hg38.zip
    wget https://data.monarchinitiative.org/exomiser/latest/2410_phenotype.zip

    # unzip the distribution and data files - this will create a directory called 'exomiser-cli-14.1.0' in the current working directory
    unzip exomiser-cli-14.1.0-distribution.zip
    unzip 2410_*.zip -d exomiser-cli-14.1.0/data

    # Check the application.properties are pointing to the correct versions:
    #  exomiser.hg19.data-version=2410
    #  exomiser.hg38.data-version=2410
    #  exomiser.phenotype.data-version=2410
   ```
   
   **Windows:**
   - Download pre-built binaries from [Exomizer releases](https://bitbucket.org/magli143/exomizer/wiki/Home)
   - Extract and add to your PATH

   **Verify installation:**
   ```bash
   exomizer --version
   ```

## Reproduction Instruction
Follow these steps to reproduce the results:

1. Download database files from huggingface:
   ```bash
   huggingface-cli download Angelakeke/DeepRare --repo-type=dataset --local-dir ./database
   ```
2. Add your LLM API key to `inference.sh`, `inference_gene.sh`, `eval.sh`.
3. Configure ChromeDriver path in `inference.sh` and `inference_gene.sh`.
4. Run the script:
   ```bash
   # For HPO input
   bash inference.sh
   # For HPO+Gene input
   bash inference_gene.sh
   # For Free-text preprocess
   bash extract_hpo.sh
   # For Evaluation
   bash eval.sh
   ```



## Web Application

Due to complex environment setup and LLM API requirements, we strongly recommend using our pre-deployed web application [DeepRare](http://deeprare.cn) for easy access and testing. 

For web engineering implementation, we package this workflow using FastAPI with DeepSeek-V3 locally deployed on **16 Ascend 910B cards** serving as the central host to ensure system stability and data security. The system architecture employs a microservices design with Redis for session management and SQL databases for persistent data storage. More details can be found in our paper (Section 11.4).


## Demo
![Demo](video/deeprare_compressed.gif)

## Reference:
```latex
@article{zhao2026agentic,
  title={An agentic system for rare disease diagnosis with traceable reasoning},
  author={Zhao, Weike and Wu, Chaoyi and Fan, Yanjie and Qiu, Pengcheng and Zhang, Xiaoman and Sun, Yuze and Zhou, Xiao and Zhang, Shuju and Peng, Yu and Wang, Yanfeng and others},
  journal={Nature},
  pages={1--10},
  year={2026},
  publisher={Nature Publishing Group UK London}
}
```

## Acknowledgement:
We gratefully acknowledge the developers and contributors of publicly available rare disease datasets, foundational research works, bioinformatics tools, and large language models that have collectively enabled our research. 
