# Installation and first launch

This guide is for a first-time player who has never used a developer tool.
You do not need an account, a database, or a separate web server. The project
is currently distributed as source code, so the first compilation downloads
Rust dependencies and can take a few minutes.

The project documents a source setup for macOS, Windows, and Linux. Chromium
evergreen desktop is the verified browser target; other browsers are deferred
and non-certified. This guide does not claim operating-system certification.

## 1. Install the prerequisites

### Rust and Cargo

Rust is the programming language used by the game. Cargo is the small command
that compiles and launches it. Follow the official
[Rust installation guide](https://www.rust-lang.org/learn/get-started).

- **macOS or Linux:** the guide installs `rustup` from a Terminal window.
- **Windows:** use the `rustup-init.exe` installer described by the guide. The
  commands below use **PowerShell**, Windows' command-line window.

After installation, close the old Terminal or PowerShell window and open a new
one. This reloads the system's command search path. Verify both commands:

```text
rustc --version
cargo --version
```

Each command should print a version. If either says “command not found” or “is
not recognized,” see the [FAQ](#faq) before continuing.

### Optional Git

Git is useful when you want repeatable updates. It is not required for a ZIP
download. Install it from the official [Git downloads](https://git-scm.com/downloads)
page and verify it in a new terminal:

```text
git --version
```

## 2. Get the game source

### Lowest-friction path: GitHub ZIP

1. Open the repository page in a browser.
2. Select **Code → Download ZIP**.
3. Extract the ZIP to a folder you can find again, such as `Documents`.
4. The extracted folder is the repository folder. It must contain
   `Cargo.toml` near its top level.

This path is ideal for a one-time play session. To update later, download a
new ZIP and use the newer folder; do not copy files over a live checkpoint
without first reading [Saved checkpoints](#saved-checkpoints).

### Repeatable-update path: Git clone

If Git is installed, follow the official
[GitHub cloning guide](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).
The short form is:

```bash
git clone <repository-url>
cd <repository-folder>
```

Replace the angle-bracket placeholders with the repository URL and folder name
shown by GitHub. Later, update that checkout with:

```bash
git pull
```

Do not run `git pull` while a game command is compiling or while you are
editing files in the checkout.

## 3. Open the repository folder

The repository folder is the directory containing `Cargo.toml`. A terminal is
a text window where you type commands; PowerShell is the Windows version of
that window.

- **macOS/Linux:** open Terminal, type `cd ` (including the space), drag the
  repository folder into the window, press Enter, then type `pwd`.
- **Windows PowerShell:** open PowerShell, type `Set-Location ` (including the
  space), drag the repository folder into the window, and press Enter. You can
  confirm the folder with `Get-Location`.

Check that the folder is correct:

```text
# macOS/Linux
ls Cargo.toml

# Windows PowerShell
Get-Item Cargo.toml
```

If the command cannot find the file, you are one folder too high or too low;
see [“could not find `Cargo.toml`”](#could-not-find-cargotoml).

## 4. Compile and play

The first run compiles the game and downloads dependencies. From the folder
containing `Cargo.toml`, start the recommended GUI tutorial:

```bash
cargo run --bin vital-margin-gui
```

Leave that terminal open. When it prints a URL, open the URL in a Chromium
evergreen desktop browser, normally `http://127.0.0.1:7878`. Choose
**Stabilization tutorial**, seed `42`, and follow the five-stage
Brief → Decide → Resolve → Review flow.

The CLI is an alternative, not a required setup step:

```bash
cargo run
```

Choose `1` for `stabilization-v1`, then beginner guided choices (`b`) and seed
`42`. The [CLI guide](how-to-play.md) explains competitive commands. The
[GUI guide](gui-how-to-play.md) covers settings, checkpoints, alternate ports,
and recovery.

## Updating and stopping

Stop the GUI by returning to its terminal and pressing **Ctrl-C** (Control-C on
macOS). Stop the CLI by using its `q`, `quit`, or `exit` command, or Ctrl-C.

- ZIP users: download and extract a fresh ZIP, then launch from the new folder.
- Git users: stop the game, run `git pull`, and launch again.

Updating source does not install a separate application. If a new compile
fails, read the error before deleting the older checkout.

### Saved checkpoints

Checkpoints belong to the running host and its source checkout. Before
replacing or removing a folder, use the GUI's **Save host checkpoint** and
**Find saved checkpoints** controls, or finish the session. A browser stores
only an opaque session ID; it does not contain the game state. A checkpoint is
not portable between unrelated hosts or folders unless the host can discover
the matching archive.

### Optional removal

After stopping the host, you may move the extracted/cloned repository folder
to the Trash or Recycle Bin. This removes the source and any host checkpoints
stored alongside it; keep a copy if you may want to resume. Rust and Git remain
installed until you remove them using their own official uninstall guidance.

## FAQ

### `cargo` or `git` is missing

Install Rust/Cargo from the [official Rust guide](https://www.rust-lang.org/learn/get-started)
and Git from [git-scm.com/downloads](https://git-scm.com/downloads) if you
need Git. Then close and reopen the terminal or PowerShell. Installation
changes do not reach an already-open command window.

### I reopened the terminal, but the command is still missing

Run `rustc --version` and `cargo --version` again in a brand-new window. On
Windows, restart PowerShell after `rustup-init.exe`; on macOS/Linux, rerun the
`rustup` command from the Rust guide if the installer reported a PATH change.
If a version prints, return to the repository folder with `cd` or
`Set-Location`.

### “could not find `Cargo.toml`”

Cargo only works from this repository folder. List the folder (`ls` on
macOS/Linux, `Get-ChildItem` in PowerShell), locate `Cargo.toml`, and change
into that directory before running Cargo.

### The first compilation is slow

That is expected: Cargo compiles the game and downloads dependencies once.
Keep the terminal open and wait for the URL or the final CLI prompt. Later
runs reuse the build cache and are normally faster.

### Dependency downloads fail

Check your internet connection, retry the same command, and avoid closing the
terminal while Cargo is fetching crates. A corporate proxy, VPN, or firewall
may block the Rust package registry; try an allowed network or ask its
administrator. No game files are changed by a failed download.

### The browser says “connection refused”

The Rust GUI host is not running, is still compiling, or you opened the wrong
address. Restart `cargo run --bin vital-margin-gui`, wait for its printed URL,
keep that terminal open, and open the exact URL.

### The port is occupied (“address already in use”)

Stop the older GUI process, or choose another loopback port:

```bash
cargo run --bin vital-margin-gui -- --bind 127.0.0.1:8787
```

Open the URL printed by that process.

### I opened `gui/index.html` and see demo data

That file is a static demonstration page. It does not connect to the Rust
host. Close it and launch `cargo run --bin vital-margin-gui`; live play starts
only at the printed loopback URL.

### My browser is unsupported

Use a current Chromium-based desktop browser. Firefox, WebKit/Safari, mobile,
and legacy-browser support are deferred and non-certified; the game remains
source-only and does not provide a hosted fallback.

### Audio is silent

Audio is optional. Click **Enable audio** in the page (browsers require a
user gesture), check the tab and system mute controls, and raise the Master
volume. Written cues, decisions, results, history, and debriefs remain
available when audio is muted or unavailable.

### I cannot recover a checkpoint

The host must still be running or must have the archive that contains the
checkpoint. Choose **Find saved checkpoints**, select the matching opaque
session ID, and use **Load existing session** or **Restore host checkpoint**.
If the ID is unknown, stale, or from another checkout, start a new session;
the browser cannot reconstruct the missing state. See the detailed
[checkpoint section in the GUI guide](gui-how-to-play.md#load-an-existing-session).

### I need more help

Read [How to Play in GUI Mode](gui-how-to-play.md) for browser settings,
refresh behavior, alternate ports, and the full recovery boundary. For the
campaign rules and CLI syntax, use [How to Play](how-to-play.md).
