# Text-To-Image Encryption

Steganography is the practice of concealing a file, message, image, or video
within another file, message, image, or video.

This project implements a steganographic algorithm based on an arbitrary amount
of customized text encryption layers. The text is read from an input plaintext
file, encoded through several layers with a password, and mapped to the RGB
values of an output image in PNG format, with adequate padding.

> The input file must only contain ASCII characters

While initially the password was not required for the execution of application,
it was decided to add an extra layer of security that could also work as a way
to select the algorithms. It is important to note that most (if not all)
algorithms implemented in this project are not secure by themselves, and
combining them will probably only inconvenience an attacker. In order to select
a password, please read [the algorithm list](Algorithm_list.txt).
    
### Output image structure

In order to create a (more or less) compact image, the data is rear-padded
with bytes sampled from the encoded data, seamlessly merging with the possible
created colors. This allows for the image to maintain a squared shape and
make it easier to visualize. So as to keep track of the padded bytes, a
certain amount of bytes are added to the beginning of the data. The value
obtained from these bytes indicate how many bytes were added at the end of
the input data, making it possible to crop accurately when trying to decode.
Therefore, the output image structure will follow the next format.

- N bytes of padding information (Defined in `src/utilities/image_conversions.py`).
- Encoded data.
- Up to `2^(N*8)` bytes of padding, randomly selected from the encoded data.

### Usage

Encoding plaintext file

    python3 src/encoder.py <inputfile> <password>
    
Decoding images

    python3 src/decoder.py <inputfile> <password>