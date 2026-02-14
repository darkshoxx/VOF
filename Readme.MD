Weclome to Voice Only Frotz

Built from a modified version of dumb frotz.
`original_dumb` contains the files form the original tarball
`modified_dumb` has compiler-friendly modifications to compile with MingW64 using
`gcc -std=c89 -o dumb-frotz *.c`
creating the `dumb-frotz.exe` which lets you play z-files like zork directly
on the windows commandline. Tested with `cmd` and `PowerShell`.

Requires Python 3.10  as 3.11 doesn't have STT, 3.12 doesn't have TTS and 3.13 doesn't even have torch.
switched to whisper, maybe 3.11 will work?


install the torch stuff with `pip install torch==2.1.0+cu118 torchvision==0.16.0+cu118 torchaudio==2.1.0+cu118 --index-url https://download.pytorch.org/whl/cu1181`

TODO:
gong shorter
sequence of directions
make reader faster
zorque
zorg
work
attack loop
heal loop

homophone dict:
feast: east
mouth: south
south east: southeast
# -> number