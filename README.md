# RaMix 

RaMix generates synthetic Raman mixture spectra. These mixture spectra can be used to compare the predictive performance of different chemoinformatics algorithms, such as partial least squares (PLS) and 1D Convolution Neural Networks (1D-CNN). 

## Repo Contents 
This Github repo is divided into five distinct folders. Each folder contains files related to a certain step in the generation process. The folder names and a description of their contents is listed below:
1. **peak_fitting_example** This folder contains a Jupyter notebook useful for extracting the peak parameters from a experimental Raman spectra. 
2. **data_gen_example** In this folder, the RaMix package is used by the `main.py` file to generate a series of different dataset of different sizes and different noise levels. 
3. **ramix** the folder containing the source files for the RaMix package, which is able to generate mixture spectra datasets. 
4. **model_comparison_example** A folder containing a Jupyter notebook used to compare and visualize the differences in performance of several different chemoinformatics algorithms using data generated in the data_gen_example. 
5. **tests** unit tests for the RaMix package 

## Installation 
The RaMix package can be installed via PyPI using `pip install ramix`. 

It can also be installed directly by 
1. cloning this repo `git clone github.com/DexterAntonio/RaMix.git` 
2. Navigating to the repo  `cd RaMix`
3. An running `pip install .`

To create a custom dataset, it is recommended to clone the repo and modify the examples to meet your own requirements. 

## Usage 
This is a brief tutorial that gives an overview of how to use the RaMix package and the additional Jupyter notebooks in this repo to generate custom mixture datasets. 

### 1. Decide on your components, locate individual component spectra and clean the data. 
1.1 The first stage in this process is to decide on and find the individual component spectra to compose the mixture spectra. This choice depends on what system you are interested in simulating and is entirely up to you. 

1.2 The next stage is actually finding the Raman spectra of the system that you are interested in. This can be a challenging as there are not that many freely accessible Raman spectra databases 

1.3 After locating the data, you should clean the data into a usable form. The recomended form for the next stage of the process is a `.csv` format for each spectra, where the first column is the `wavenumbers` and the second column is the `relative intensity`.  If you only have images, this conversion can be achieved by using [WebPlotDigitizer](https://apps.automeris.io/wpd/). 

### 2. Extract peak parameters from the component spectra 

2.1 The next stage is to extract the peak parameters from the component spectra. The `Jupyter` notebook `sugar_fitting.ipynb` in the **peak_fitting_example** folder walks through the steps to perform this fitting. It makes use of the python package [dataphile](https://github.com/glentner/dataphile), which can be installed via `pip`. A great tutorial and description of this package can be found [here](https://lentner.io/2018/06/14/autogui-for-curve-fitting-in-python.html). 

2.2 After fitting the peaks, combine them into a JSON file that mimics the following format. This JSON file is automatically generated and saved by the Jupyter notebook. This JSON file is refered to as the peak skeleton because it outlines the individual peaks in the spectra. 

Example JSON from sugar fitting

```python 
{'glucose': [{'wavenumber': 440.0, 'amplitude': 0.185, 'width': 56.28},
  {'wavenumber': 512.0, 'amplitude': 0.192, 'width': 38.64},
  {'wavenumber': 752.0, 'amplitude': 0.022, 'width': 90.09},
  {'wavenumber': 860.0, 'amplitude': 0.065, 'width': 21.21},
  {'wavenumber': 906.0, 'amplitude': 0.074, 'width': 22.03},
  {'wavenumber': 1059.0, 'amplitude': 0.083, 'width': 40.51},
  {'wavenumber': 1124.0, 'amplitude': 0.084, 'width': 28.74},
  {'wavenumber': 1355.0, 'amplitude': 0.166, 'width': 90.66},
  {'wavenumber': 1820.0, 'amplitude': 0.038, 'width': 349.7}],
 'fructose': [{'wavenumber': 452.0, 'amplitude': 0.127, 'width': 92.35},
  {'wavenumber': 626.0, 'amplitude': 0.125, 'width': 25.16},
  {'wavenumber': 816.0, 'amplitude': 0.105, 'width': 13.13},
  {'wavenumber': 864.0, 'amplitude': 0.075, 'width': 21.68},
  {'wavenumber': 1074.0, 'amplitude': 0.067, 'width': 45.49},
  {'wavenumber': 1347.0, 'amplitude': 0.139, 'width': 88.64},
  {'wavenumber': 1819.0, 'amplitude': 0.024, 'width': 220.43}],
 'sucrose': [{'wavenumber': 467.0, 'amplitude': 0.104, 'width': 151.71},
  {'wavenumber': 840.0, 'amplitude': 0.086, 'width': 34.11},
  {'wavenumber': 1071.0, 'amplitude': 0.056, 'width': 62.0},
  {'wavenumber': 1353.0, 'amplitude': 0.15, 'width': 97.41}]}
  ```

### 3. Pick noise levels for your datasets and create a noise dictionary 

3.1 The noise levels determine the parameters for the distributions that generate the random numbers, which shift the location, size and width of the peaks. For each peak in the "spectrum skeleton" a random number is generated for each parameter for a given peak and either added or multiplied by that parameter. For example, the noisy spectrum skeleton wavenumbers have a random number added to them, which has been pulled from a Gaussian distribution with a mean of 0 and a standard deviation specified in the noise dictionary. The amplitude and width are multiplied by a lognormal distribution with a mean of 1 and a standard deviation specified by the user. 

Think about what noise level and data set sizes you are interested in exploring, before making the noise dictionary. 

3.2 The RaMix package is designed to assess the performance of different cheminformatic algoritims across different noise levels, thus when running the software, a "noise dictionary" is supplied which describes the noise levels for all of the different datasets that will be generated. An example noise dictionary is shown below: 

```python
 noise_dict = {'size': [10, 100],  
               'wavenumber_noise': [0.1, 0.5],  
               'amplitude_noise': [0.1, 0.5],  
               'width_noise': [0.5, 1.0],  
               'add_baseline': [False, True]}```
 ```
 
 In the original design of the software every single possible permutation of the values in each list were constructed from the noise dictionary. The program has since been changed so that the `wavenumber_noise`, `amplitude_noise` and `width_noise` are grouped together during the permutation construction. For example, using noise dictionary specified above the following datasets with the following parameters are generated: 
 
| size | wavenumber noise | amplitude noise | width noise | add baseline |
|------|------------------|-----------------|-------------|--------------|
| 10   | 0.1              | 0.1             | 0.5         | FALSE        |
| 100  | 0.1              | 0.1             | 1           | FALSE        |
| 10   | 0.5              | 0.5             | 0.5         | FALSE        |
| 100  | 0.5              | 0.5             | 1           | FALSE        |
| 10   | 0.1              | 0.1             | 0.5         | FALSE        |
| 100  | 0.1              | 0.1             | 1           | FALSE        |
| 10   | 0.5              | 0.5             | 0.5         | FALSE        |
| 100  | 0.5              | 0.5             | 1           | FALSE        |
| 10   | 0.1              | 0.1             | 0.5         | TRUE         |
| 100  | 0.1              | 0.1             | 1           | TRUE         |
| 10   | 0.5              | 0.5             | 0.5         | TRUE         |
| 100  | 0.5              | 0.5             | 1           | TRUE         |
| 10   | 0.1              | 0.1             | 0.5         | TRUE         |
| 100  | 0.1              | 0.1             | 1           | TRUE         |
| 10   | 0.5              | 0.5             | 0.5         | TRUE         |
| 100  | 0.5              | 0.5             | 1           | TRUE         |

### 4. Run Ramix 

4.1 Now that you have constructed a peak skeleton and noise dict you can finally use the RaMix package to generate different mixture datasets with different noise levels. An example can be found in the **data_gen_example** folder. Here is an example below: 


```python
from ramix.mixture_maker import MixtureMaker  

def main():  
    """  
 This main function generates the following datasets and puts them in the gen_data directory 
 """ 
 # make noise dictionary  
 noise_dict = {'size': [10, 100, 1000, 10_000],  
                  'wavenumber_noise': [0, 0.1, 0.5, 1.0, 1.5, 2.0],  
                  'amplitude_noise': [0, 0.1, 0.5, 1.0, 1.5, 2.0],  
                  'width_noise': [0, 0.1, 0.5, 1.0, 1.5, 2.0],  
                  'add_baseline': [False, True]}  
  
    mixture_maker = MixtureMaker('default_spectra.json', noise_dict, 'gen_data')  
    mixture_maker.generate_all()  # generate all of the spectra  
  
if __name__ == "__main__":  
    main()
```
Now run the file and be patient. It should take several hours to generate many datasets. This is partially because the entire program runs on a single thread and the artificial baseline construction algorithm is slow. Please feel free to contribute to speeding up the program. 

Each dataset will get a (verbose) folder name and contain a binary X and y NumPy arrays and a `species_indices.json` file which maps between the chemical species names and the indicies of the y NumPy array. Your folder structure should resemble the example below: 

```bash
size_10000_wn_std_0.1_amp_std_0.1_width_std_0.1_add_baseline_False
├── X.npy
├── species_indices.json
└── y.npy
```


### 5. Analysis 

5.1 At this point you have generated a lot of datasets and you can now try different ML algorithms to predict the concentration from the mixture spectra. A Jupyter notebook that performs this analysis is shown in the **model_comparison_example** folder. A Google colab version of this notebook can be found here. Using the google colab version is recommenced since it has easy-to-use GPU support, which significantly (~x20) speeds neural network training and testing. 

## Support

If you encounter any issues create an issue with the issue tracker. If you have any questions about using this package, feel free to reach out to me at dexter.d.antonio at gmail dot com . 

## Licence

Copyright 2021 Dexter Antonio 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---------- 
