from ramix.mixture_maker import MixtureMaker
import matplotlib.pyplot as plt

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

    # visualize the individual component spectra
    wavenumbers = mixture_maker.get_wavenumbers()
    component_spectra = mixture_maker.get_component_spectra()
    fig, axes = plt.subplots(nrows=len(component_spectra), ncols=1, figsize=(5, 15))
    for key, ax in zip(component_spectra, axes.flatten()):
        ax.plot(wavenumbers, component_spectra[key])
        ax.set_xlabel("wavenumbers $(cm^{-1})$")
        ax.set_ylabel("Intensity")
        ax.set_title(key)

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()