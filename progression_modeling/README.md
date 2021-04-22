# Progression Modeling

A generative model for harmonic rhythm.

<div style="text-align: center; margin: 0 1.5em;">
  <img src="progression_modeling.png" width=800>
</div>

For details on how the model dataset was prepared, see [progression_extraction](../progression_extraction/docs/model_datset.md).

### The model

Variational Auto-Encoder (VAE)

Generate new samples of a particular class.

Target output tensor: L bars x M time steps x N pitches

##### Reference

-   [Music VAE](https://magenta.tensorflow.org/music-vae)

## Model UX

<div style="text-align: center; margin: 0 1.5em;">
  <img src="using_the_model.png" width=800>
</div>

Two modes:

1. Depicted above: user locks some chords and hits generate. The latent space is sampled for a new progression according to their current progression state and constraints

2. User syncs knobs to a progression they like, then can hit generate to get similar progressions.

## TODO

-   train VAE

#### Maybe

-   [feature] harmonic style transfer
-   [feature] generate chords with specific [perceptual qualities](dataset.md###perceptual_qualities)
-   use genre as a target: "Generate chord progressions in the style of any genre"
