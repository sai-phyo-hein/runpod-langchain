# Installation & Publishing Guide

## 📦 Package Structure

```
runpod-langchain/
├── runpod_langchain/
│   ├── __init__.py
│   └── chat_model.py
├── tests/
│   └── test_chat_model.py
├── examples/
│   └── examples.py
├── setup.py
├── pyproject.toml
├── MANIFEST.in
├── LICENSE
├── README.md
├── COMPARISON.md
├── .gitignore
└── INSTALL_GUIDE.md (this file)
```

## 🚀 Installation Methods

### Method 1: Install from Local Directory (Development)

```bash
# Navigate to the package directory
cd /path/to/runpod-langchain

# Install in development mode (editable)
pip install -e .

# Or regular install
pip install .
```

### Method 2: Install from Git Repository

```bash
# Install directly from GitHub
pip install git+https://github.com/yourusername/runpod-langchain.git

# Install specific branch
pip install git+https://github.com/yourusername/runpod-langchain.git@main

# Install specific tag/version
pip install git+https://github.com/yourusername/runpod-langchain.git@v0.1.0
```

### Method 3: Install from PyPI (After Publishing)

```bash
# Install from PyPI
pip install runpod-langchain

# Install with dev dependencies
pip install runpod-langchain[dev]

# Install specific version
pip install runpod-langchain==0.1.0
```

## 📤 Publishing to PyPI

### Step 1: Create PyPI Account

1. Go to https://pypi.org/account/register/
2. Create an account and verify your email
3. (Optional) Create a Test PyPI account at https://test.pypi.org/

### Step 2: Install Build Tools

```bash
pip install build twine
```

### Step 3: Build the Package

```bash
# Navigate to package root directory
cd /path/to/runpod-langchain

# Build the package
python -m build
```

This creates:
- `dist/runpod_langchain-0.1.0-py3-none-any.whl` (wheel)
- `dist/runpod-langchain-0.1.0.tar.gz` (source)

### Step 4: Test on Test PyPI (Optional but Recommended)

```bash
# Upload to Test PyPI
python -m twine upload --repository testpypi dist/*

# Install from Test PyPI to verify
pip install --index-url https://test.pypi.org/simple/ runpod-langchain
```

### Step 5: Upload to PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*

# You'll be prompted for username and password
# Or use API token (recommended):
# Username: __token__
# Password: pypi-...
```

### Step 6: Verify Installation

```bash
# Try installing from PyPI
pip install runpod-langchain

# Test import
python -c "from runpod_langchain import RunPodChatModel; print('Success!')"
```

## 🔑 Using API Tokens (Recommended)

### Create PyPI API Token

1. Go to https://pypi.org/manage/account/
2. Scroll to "API tokens"
3. Click "Add API token"
4. Give it a name (e.g., "runpod-langchain-upload")
5. Select scope (entire account or specific project)
6. Copy the token (starts with `pypi-`)

### Configure .pypirc

```bash
# Create/edit ~/.pypirc
cat > ~/.pypirc << EOF
[pypi]
username = __token__
password = pypi-your-token-here

[testpypi]
username = __token__
password = pypi-your-test-token-here
EOF

# Secure the file
chmod 600 ~/.pypirc
```

Now you can upload without entering credentials:
```bash
python -m twine upload dist/*
```

## 🔄 Version Updates

### Update Version Number

1. Edit `setup.py` and `pyproject.toml`
2. Change version from `0.1.0` to `0.1.1` (or appropriate version)

### Rebuild and Republish

```bash
# Clean old builds
rm -rf build/ dist/ *.egg-info

# Build new version
python -m build

# Upload new version
python -m twine upload dist/*
```

## 🧪 Testing Before Publishing

### Create Test Environment

```bash
# Create virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install your package locally
pip install -e .

# Run tests
pytest tests/

# Test examples
python examples/examples.py
```

### Run All Quality Checks

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Format code
black runpod_langchain/

# Lint code
flake8 runpod_langchain/

# Type checking
mypy runpod_langchain/

# Run tests with coverage
pytest --cov=runpod_langchain tests/
```

## 📝 Complete Publishing Checklist

- [ ] Update version in `setup.py` and `pyproject.toml`
- [ ] Update `CHANGELOG.md` with changes
- [ ] Run tests: `pytest tests/`
- [ ] Run linting: `flake8 runpod_langchain/`
- [ ] Format code: `black runpod_langchain/`
- [ ] Clean old builds: `rm -rf build/ dist/ *.egg-info`
- [ ] Build package: `python -m build`
- [ ] Test on Test PyPI: `python -m twine upload --repository testpypi dist/*`
- [ ] Install from Test PyPI and test
- [ ] Upload to PyPI: `python -m twine upload dist/*`
- [ ] Verify installation: `pip install runpod-langchain`
- [ ] Create Git tag: `git tag v0.1.0 && git push origin v0.1.0`
- [ ] Create GitHub release

## 🌐 GitHub Release

After publishing to PyPI, create a GitHub release:

```bash
# Tag the release
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

Then on GitHub:
1. Go to your repository
2. Click "Releases" → "Create a new release"
3. Select the tag you just created
4. Add release notes
5. Attach the wheel and source distribution files from `dist/`

## 📊 After Publishing

Users can now install with:

```bash
pip install runpod-langchain
```

And use it:

```python
from runpod_langchain import RunPodChatModel
import os

llm = RunPodChatModel(
    endpoint_id=os.getenv("RUNPOD_ENDPOINT_ID"),
    api_key=os.getenv("RUNPOD_API_KEY")
)

response = llm.invoke("Hello!")
print(response.content)
```

## 🔧 Troubleshooting

### "Package already exists"
- You can't re-upload the same version
- Increment version number and rebuild

### "Invalid username/password"
- Use API token instead: username=`__token__`, password=`pypi-...`
- Check your .pypirc file

### "Package name already taken"
- Choose a different name in setup.py
- Suggestion: `runpod-langchain-yourusername`

### Import errors after install
- Check package structure: `pip show runpod-langchain`
- Verify __init__.py exports: `from runpod_langchain import RunPodChatModel`

## 📚 Resources

- PyPI Publishing Guide: https://packaging.python.org/tutorials/packaging-projects/
- Setuptools Documentation: https://setuptools.pypa.io/
- Twine Documentation: https://twine.readthedocs.io/
- Python Packaging User Guide: https://packaging.python.org/