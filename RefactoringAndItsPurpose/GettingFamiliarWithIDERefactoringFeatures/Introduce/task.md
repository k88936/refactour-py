Refactor is an important feature for an IDE, we will introduce cover some common backing components here.

## Language Server Protocol

The Language Server Protocol (LSP) defines the protocol used between an editor or IDE and a language server that
provides language features like auto complete, go to definition, find all references etc.
The most famous example is vscode. Vim, Neovim also benefit from it. Plus, IntelliJ Platform can use external LSP via
plugin (LSP4j), for example: to empower RustRover with rust-analyzer.

## Program Structure Interface

IntelliJ Platform (%IDE_NAME%, ...) use The Program Structure Interface (PSI) as the layer in the responsible for
parsing files and creating the syntactic and semantic code model that powers so many of the platform's features.

