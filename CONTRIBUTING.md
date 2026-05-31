# Contributing to Stack-Scout

Thanks for taking the time to contribute! Stack-Scout is a zero-dependency technology stack detector for code repositories.

## How to contribute

### Report bugs or request features
Open an issue with:
- A clear title and description
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Stack-Scout version and Python version

### Submit code

1. **Fork** the repository
2. **Create a branch**: `git checkout -b your-feature`
3. **Make changes**: add detectors, fix bugs, improve docs
4. **Write tests**: all new features need tests. Run `pytest tests/` before committing.
5. **Format your code**: follow PEP 8 conventions visible in existing code
6. **Commit**: use clear commit messages
7. **Push and open a PR**: describe what changed and why

### Adding a new detector

1. Create a file in `stack_scout/detectors/` (e.g. `mytech_detector.py`)
2. Subclass `Detector` from `stack_scout.detectors.base`
3. Implement the `detect(file_paths, file_contents)` method
4. Add your detector to `stack_scout/detectors/__init__.py`
5. Register it in `stack_scout/scanner.py` `StackScanner.__init__`
6. Add an icon for your category in `stack_scout/formatters/console_formatter.py`
7. Write tests in `tests/`

### Testing
```bash
pip install -e ".[dev]"
pytest tests/ -v
```

### Pull request checklist
- [ ] Tests pass (`pytest tests/`)
- [ ] New detectors have tests
- [ ] README updated if adding user-facing features
- [ ] No new external dependencies added (stdlib only)

### Code of Conduct
Be respectful, constructive, and inclusive. We follow the [Contributor Covenant](https://www.contributor-covenant.org/).
