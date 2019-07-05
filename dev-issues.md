05/07/2019 - Lohit's ideas:
For processing large data, currently need to save file to disk then reload in the next node. Is it possible to keep data persistent across nodes?
E.g. make an image in node1, pass the image by reference into the next node.
This would be useful for potential GPU pipelines where you can only pass IDs for VBOs, Textures, etc.
