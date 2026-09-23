loaded_data = np.load('filename.npz')
packed_loaded = loaded_data['my_bits']
unpacked_array = np.unpackbit(packed_loaded)[:decks.size].reshape(decks.shape)