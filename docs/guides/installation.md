# Installation and First Launch

[Documentation Home](../index.md) | [GUI Guide](gui-how-to-play.md) | [CLI Guide](how-to-play.md) | [Strategy Guide](strategy-and-mechanics.md) | [Glossary](../reference/glossary.md)

---

This guide is for a first-time player who has never used a developer tool.
You do not need an account, a database, or a separate web server. The project
is currently distributed as source code, so the first compilation downloads
Rust dependencies and can take a couple of minutes.

The project documents a source setup for **macOS**, **Windows**, and **Linux**.
**Chromium evergreen desktop** (Chrome, Edge, Brave, Chromium) is the verified
browser target; other browsers are deferred and non-certified.

---

## 1. Install the Prerequisites

### Rust and Cargo
Rust is the programming language used by the game. Cargo is the command-line tool
that compiles and launches it. Follow the official
[Rust installation guide](https://www.rust-lang.org/learn/get-started):

- **macOS or Linux:** Open a Terminal window and install via `rustup`:
  ```bash
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
  ```
- **Windows:** Download and run the `rustup-init.exe` installer from
  [rustup.rs](https://rustup.rs). The commands below use **PowerShell**, Windows'
  default command-line window.

After installation, **close your Terminal or PowerShell window and open a brand-new
one**. This ensures your system's PATH environment variables are refreshed.

Verify both commands in the new window:
```bash
rustc --version
cargo --version
```
Each command should print a version number (e.g., `cargo 1.80.0 ...`). If you see
"command not found" or "is not recognized", see the [FAQ](#faq) below.

### Optional Git
Git is useful for fast, repeatable updates with `git pull`. It is not required
if you download the game as a ZIP archive. Install it from
[git-scm.com/downloads](https://git-scm.com/downloads) and verify:
```bash
git --version
```

---

## 2. Get the Game Source

### Lowest-Friction Path: GitHub ZIP Download
1. Open the repository on GitHub.
2. Click the green **Code** button and select **Download ZIP**.
3. Extract the ZIP archive to a convenient folder (such as your `Documents` or `Desktop` folder).
4. Ensure the extracted folder contains `Cargo.toml` at its top level.

### Repeatable-Update Path: Git Clone
If Git is installed:
```bash
git clone https://github.com/SaehwanPark/vital-margin.git
cd vital-margin
```
To update in the future, simply run `git pull` from inside the repository folder.

---

## 3. Open the Repository Folder

Open your terminal and navigate to the directory containing `Cargo.toml`:

- **macOS / Linux:** Open Terminal, type `cd ` (with space), drag the folder
  into Terminal, and press Enter.
- **Windows PowerShell:** Open PowerShell, type `Set-Location ` (with space),
  drag the folder into PowerShell, and press Enter.

Verify you are in the correct directory:
```bash
# macOS/Linux
ls Cargo.toml

# Windows PowerShell
Get-Item Cargo.toml
```

---

## 4. Compile and Play

### Recommended: Live Browser GUI
From the repository root folder, launch the live GUI:

```bash
cargo run --bin vital-margin-gui
```

Leave that terminal open. When compilation finishes, it prints:
```text
Vital Margin GUI: http://127.0.0.1:7878
```
Open `http://127.0.0.1:7878` in your Chromium browser, select **Stabilization
tutorial** (`stabilization-v1`), seed `42`, and click **Start selected session**!

### Alternative: Interactive Terminal CLI
If you prefer playing directly in the terminal:

```bash
cargo run
```
Press Enter (or `1`) for `stabilization-v1`, press `b` for beginner guided
mode, and accept seed `42`.

---

## 🛑 Stopping and Updating

- **To Stop the Game:** Return to the terminal running Cargo and press **Ctrl-C**
  (Control-C on macOS). In the CLI, type `q`, `quit`, or `exit`.
- **To Update:**
  - *Git users:* Stop the host, run `git pull`, and restart with `cargo run`.
  - *ZIP users:* Download the latest ZIP, extract to a new folder, and run from
    there.

### Saved Checkpoints
Checkpoints are saved by the host to your local checkout. Use the GUI's **Save host
checkpoint** and **Find saved checkpoints** controls before switching folders.
Session states are managed by the host, not stored in the browser.

---

## ❓ Frequently Asked Questions (FAQ)

### `cargo` or `git` is missing
Install Rust from [rustup.rs](https://rustup.rs) and Git from
[git-scm.com/downloads](https://git-scm.com/downloads). Close and reopen your
terminal window so that the PATH changes take effect.

### “could not find `Cargo.toml`”
You are not in the repository directory. Use `cd` or `Set-Location` to navigate
to the folder where `Cargo.toml` is located.

### The first compilation is taking a few minutes
This is completely normal. Cargo downloads and compiles all necessary Rust
libraries during the initial build. Subsequent runs will use cached build
artifacts and start in seconds.

### The browser displays "Connection Refused"
The Rust GUI host is either still compiling or has stopped. Check your
terminal to ensure `cargo run --bin vital-margin-gui` is actively running.

### "Address already in use (port 7878)"
Stop any existing instance of the GUI, or bind to an alternate port:
```bash
cargo run --bin vital-margin-gui -- --bind 127.0.0.1:8787
```
Then open `http://127.0.0.1:8787`.

### I opened `gui/index.html` and see mock data
Opening the HTML file directly runs the static fallback demo without the Rust
simulation engine. Always launch via `cargo run --bin vital-margin-gui` and visit
the printed `http://127.0.0.1:7878` URL.

---

## 📖 Next Steps

- [How to Play in GUI Mode](gui-how-to-play.md)
- [How to Play in the CLI](how-to-play.md)
- [Comprehensive Strategy & Mechanics Guide](strategy-and-mechanics.md)
- [Glossary of Key Terms](../reference/glossary.md)
