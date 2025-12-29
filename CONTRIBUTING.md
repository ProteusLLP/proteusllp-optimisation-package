# Contributing to Proteus Optimisation Package

Thank you for your interest in contributing!
We welcome pull requests, bug reports, and ideas that help improve this project.

## How to Contribute

1. **Fork the repository** and create your own branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   Keep the code clean, documented, and consistent with existing style.

3. **Run tests** before submitting a pull request:
   ```bash
   make check
   ```

4. **Submit a Pull Request (PR)**
   - Provide a clear description of what the change does and why it's useful.
   - Reference any related issues.
   - Each PR should be focused on a single topic.

## Contributor License Agreement (CLA)

Before we can accept your pull request, you must agree to the
[Proteus Consulting Contributor License Agreement](CLA.md).

By submitting a contribution, you confirm that:
- You are the author of your contribution or have the right to submit it, and
- You agree to license your contribution under the same terms as this project (currently the [MIT License](LICENSE)).

If you submit a pull request, that submission constitutes agreement to the CLA.

## Code Quality Standards

This project follows strict code quality standards:

- **Type hints**: All public functions must have complete type annotations
- **Docstrings**: All public APIs must have Google-style docstrings
- **Tests**: New features require corresponding unit tests
- **Linting**: Code must pass ruff linting and formatting checks
- **Type checking**: Code must pass mypy type checking

See [STYLE_GUIDE.md](STYLE_GUIDE.md) for detailed coding standards.

## Development Setup

1. Open the project in VS Code with the devcontainer:
   ```bash
   code /proteus-optimisation-package
   # VS Code will prompt to reopen in container
   ```

2. The devcontainer automatically installs all dependencies via PDM

3. Run tests to verify setup:
   ```bash
   pdm run pytest tests/ -v
   ```

## Code of Conduct

Please be respectful and constructive.
We aim to foster a professional and collaborative open-source community.

## Reporting Issues

If you find a bug or have an idea for improvement:
- Open a [GitHub Issue](../../issues) with a clear title and description.
- Include steps to reproduce problems when reporting bugs.
- Feature requests are welcome — please explain the use case.

## Getting Help

For general questions or discussions, you can open a [GitHub Discussion](../../discussions)
or reach out via our website at [proteusllp.com](https://proteusllp.com).

---

Thank you for helping make Proteus software better!
