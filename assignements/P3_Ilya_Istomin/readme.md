# Assignment 3

## Installation

First of all you should create an environment and install the required dependencies.

### pip installation

1. Create a virtual environment:
    ```sh
    python -m venv .venv
    ```

2. Activate the virtual environment:
    - For Windows:
        ```sh
        .venv\Scripts\activate
        ```
    - For macOS/Linux:
        ```sh
        source .venv/bin/activate
        ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Verify the installation:
    ```sh
    pip list
    ```

### conda installation

1. Create a conda environment:
    ```sh
    conda create --name myenv python=3.12
    ```

2. Activate the conda environment:
    ```sh
    conda activate myenv
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Verify the installation:
    ```sh
    conda list
    ```

## Part 1
To start Cache Test you should execute:
```sh
python cache_test.py
```

### Note
The test might fail because I am creating new models with my `models_product.yml` file. If something goes wrong, just use your `.yml` file.

## Part 2
To start the packaging program you should execute:
```sh
python packaging.py
```