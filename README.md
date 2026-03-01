# JARVIS Voice Assistant (this readme is outdated)

![We are NOT limited by the technology of our time!](poster.jpg)

`Jarvis` - is a voice assistant made as an experiment using neural networks for things like **STT/TTS/Wake Word/NLU** etc.

The main project challenges we try to achieve is:
 - 100% offline *(no cloud)*
 - Open source *(full transparency)*
 - No data collection *(we respect your privacy)*

Our backend stack is 🦀 **[Rust](https://www.rust-lang.org/)** with ❤️ **[Tauri](https://tauri.app/)**.<br>
For the frontend we use ⚡️ **[Vite](https://vitejs.dev/)** + 🛠️ **[Svelte](https://svelte.dev/)**.

*Other libraries, tools and packages can be found in source code.*

## Neural Networks

This are the neural networks we are currently using:

 - Speech-To-Text
	 - [Vosk Speech Recognition Toolkit](https://github.com/alphacep/vosk-api) via [Vosk-rs](https://github.com/Bear-03/vosk-rs)
 - Text-To-Speech
	 - [~~Silero TTS~~](https://github.com/snakers4/silero-models) *(currently not used)*
	 - [~~Coqui TTS~~](https://github.com/coqui-ai/TTS) *(currently not used)*
	 - [~~WinRT~~](https://github.com/ndarilek/tts-rs) *(currently not used)*
	 - [~gTTS~](https://github.com/nightlyistaken/tts_rust) *(currently not used)*
	 - [~~SAM~~](https://github.com/s-macke/SAM) *(currently not used)*
 - Wake Word
	 - [Rustpotter](https://github.com/GiviMAD/rustpotter) *(Partially implemented, still WIP)*
	 - [Picovoice Porcupine](https://github.com/Picovoice/porcupine) via [official SDK](https://github.com/Picovoice/porcupine#rust) *(requires API key)*
	 - [Vosk Speech Recognition Toolkit](https://github.com/alphacep/vosk-api) via [Vosk-rs](https://github.com/Bear-03/vosk-rs) *(very slow)*
	 - [~~Snowboy~~](https://github.com/Kitt-AI/snowboy) *(currently not used)*
 - NLU
	 - Nothing yet.
- Chat
	- [~~ChatGPT~~](https://chat.openai.com/) (coming soon)

## Supported Languages

Currently, only Russian language is supported.<br>
But soon, Ukranian and English will be added for the interface, wake-word detection and speech recognition.

## How to build?

Nothing special was used to build this project.<br>
You need only Rust and NodeJS installed on your system.<br>
Other than that, all you need is to install all the dependencies and then compile the code with `cargo tauri build` command.<br>
Or run dev with `cargo tauri dev`.

### Linux Build

For Linux systems, you may need to install additional dependencies:

**Arch Linux / CachyOS:**
```bash
sudo pacman -S webkit2gtk gtk3 libappindicator libayatana-appindicator
```

**Debian / Ubuntu:**
```bash
sudo apt install libwebkit2gtk-4.0-dev libgtk-3-dev libayatana-appindicator3-dev librsvg2-dev libgdk-pixbuf2.0-dev
```

**Fedora:**
```bash
sudo dnf install webkit2gtk3-devel gtk3-devel libappindicator-devel
```

### Running on Wayland

If you're using GNOME on Wayland, you may need to run with X11 backend for the tray icon:

```bash
GDK_BACKEND=x11 WEBKIT_DISABLE_COMPOSITING_MODE=1 ./target/release/jarvis-gui
```

Or use the provided launcher script:
```bash
./jarvis.sh
```

### Starting the Assistant

The GUI is just the interface. To start the voice assistant backend:

```bash
# Terminal 1: Start the backend assistant
LC_NUMERIC=C GDK_BACKEND=x11 ./target/release/jarvis-app

# Terminal 2: Start the GUI interface  
GDK_BACKEND=x11 WEBKIT_DISABLE_COMPOSITING_MODE=1 ./target/release/jarvis-gui
```

Both `jarvis-app` and `jarvis-gui` should be running for full functionality.

**Important:** On Linux, you must set `LC_NUMERIC=C` to prevent Vosk from outputting numbers with comma decimal separators (Russian locale issue).

**Note:** On Wayland systems, you must set `GDK_BACKEND=x11` for the tray icon to work properly.

<br><br>
*Thought you might need some of the platform specific libraries for [PvRecorder](https://github.com/Picovoice/pvrecorder) and [Vosk](https://github.com/alphacep/vosk-api).*

## Author

Abraham Tugalov

## Python version?
Old version of Jarvis was built with Python.<br>
The last Python version commit can be found [here](https://github.com/Priler/jarvis/tree/943efbfbdb8aeb5889fa5e2dc7348ca4ea0b81df).

## License

[Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)<br>
See LICENSE.txt file for more details.
