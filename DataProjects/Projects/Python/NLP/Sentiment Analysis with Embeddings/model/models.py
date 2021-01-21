from keras.models import Sequential
from keras import layers

def buildmodel(modeltype, max_words, embedding_dim, maxlen):
    
    if modeltype == 'a':
        model = Sequential()
        # We specify the maximum input length to our Embedding layer
        # so we can later flatten the embedded inputs
        model.add(layers.Embedding(max_words, embedding_dim, input_length = maxlen))
        # After the Embedding layer, 
        # our activations have shape `(samples, maxlen, 8)`.

        # We flatten the 3D tensor of embeddings 
        # into a 2D tensor of shape `(samples, maxlen * 8)`
        model.add(layers.Flatten())
        # We add the classifier on top
        model.add(layers.Dense(1, activation='sigmoid'))

    if modeltype == 'b':
        model = Sequential()
        model.add(layers.Embedding(max_words, embedding_dim, input_length = maxlen))
        model.add(layers.Flatten())
        model.add(layers.Dense(32, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))

    model.summary()

    return model