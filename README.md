This repository contains the code for an Iterated Rational Speech Acts model.
See https://www.aclweb.org/anthology/W19-0109

## Requirements:
`numpy`
`treelib`

## Usage:

Import the `IterRSA` class from `iterRSA`. Each instance of an `IterRSA` model is simply defined by a dictionary represeting the semantics function that takes in pair consisting an complete utterance u and world state w, and returns a 0 or 1. The list of possible utterances and possible worlds are automatically extracted from this dict. Once the model is defined, one can call methods defined in the iterRSA class to play around with it.

See `main.py` for examples of usage.
