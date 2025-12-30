# Deployment Plan for Proteus Optimisation Package (POP)

This document outlines the remaining steps to deploy POP to PyPI.

## Current Status

✅ **Complete:**
- Full package structure (optimizer/, tests/, examples/, docs/)
- 127 passing tests
- Pydantic models with comprehensive validation
- Docker support (Dockerfile.cpu + Dockerfile.gpu)
- Devcontainer configs (CPU + GPU variants)
- GitHub Actions CI/CD pipeline (static analysis, tests, build, publish)
- Documentation (Sphinx + ReadTheDocs integration)
- All template files (STYLE_GUIDE, CONTRIBUTING, CLA, LICENSE)
- Placeholder logo (POP.svg)
- Git repository initialized with proper branch structure:
  - `main` - production branch (empty, ready for releases)
  - `dev` - development branch (has initial package structure)
  - `feature/initial-package-structure` - feature branch merged to dev
- Remote configured: `https://github.com/ProteusLLP/proteusllp-optimisation-package.git`

❌ **Blocked by PAL 0.2.8 Publication:**
- Switching from wheel to PyPI PAL dependency
- `pdm.lock` file regeneration with PyPI PAL
- Testing with PyPI-installed PAL
- First PyPI release

⚠️ **Current Development Setup:**
- Using local PAL wheel: `proteusllp_actuarial_library-0.2.8.dev10+g27c24bb-py3-none-any.whl`
- Single line change needed in `pyproject.toml` to switch to PyPI
- **Switch to PyPI when available** (see Phase 3.0)

🔄 **Pending (Not Blocked):**
- GitHub repository creation
- Push branches to GitHub
- GitHub repository configuration

---

## Phase 1: GitHub Repository Setup (Ready Now)

### 1.1 Create GitHub Repository

**Via Web UI:**
1. Navigate to: https://github.com/organizations/ProteusLLP/repositories/new
2. Repository name: `proteus-optimisation-package`
3. Description: `Proteus Optimisation Package (POP): Domain-agnostic stochastic optimization engine for PAL variables`
4. Visibility: **Public** (required for PyPI publishing)
5. **Do NOT initialize** with README, .gitignore, or license (we already have them)
6. Click "Create repository"

### 1.2 Push All Branches

```bash
cd /proteus-optimisation-package

# Push main branch (production-ready)
git push -u origin main

# Push dev branch (current work)
git push -u origin dev

# Push feature branch (for reference)
git push -u origin feature/initial-package-structure
```

### 1.3 Configure Repository Settings

**Branch Protection (main):**
1. Go to: Settings → Branches → Add rule
2. Branch name pattern: `main`
3. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require approvals (1)
   - ✅ Require status checks to pass before merging
     - Add: `static-analysis`, `test`
   - ✅ Require branches to be up to date before merging
   - ✅ Include administrators
4. Save changes

**Default Branch:**
- Set default branch to `dev` for development
- Settings → General → Default branch → Change to `dev`

---

## Phase 2: PyPI Publishing Setup (Ready Now)

### 2.1 Configure PyPI Trusted Publishing

**In GitHub:**
1. Settings → Environments → New environment
2. Name: `pypi-publish`
3. Deployment protection rules:
   - ✅ Required reviewers (add team/users)
   - ✅ Wait timer: 0 minutes
4. Save

**In PyPI:**
1. Go to: https://pypi.org/manage/account/publishing/
2. Add a new pending publisher:
   - PyPI Project Name: `proteusllp-optimisation-package`
   - Owner: `ProteusLLP`
   - Repository name: `proteus-optimisation-package`
   - Workflow name: `ci.yaml`
   - Environment name: `pypi-publish`
3. Save

### 2.2 Add GitHub Secrets (Optional)

**For Code Coverage:**
1. Create Codecov account: https://codecov.io/
2. Get token for repository
3. GitHub Settings → Secrets → Actions → New repository secret
   - Name: `CODECOV_TOKEN`
   - Value: (your token)

---

## Phase 3: Waiting on PAL 0.2.8 (BLOCKED)

**Cannot proceed until PAL 0.2.8+ is published to PyPI.**

### Current Temporary Setup for Development

**Using a local wheel file as a simple temporary solution:**

1. **`proteusllp_actuarial_library-0.2.8.dev10+g27c24bb-py3-none-any.whl`** - In project root
   - Wheel file copied from PAL build output
   - Referenced in `pyproject.toml` with `file://` URL

2. **`pyproject.toml`** - Line 27:
   - Uses wheel: `"proteusllp-actuarial-library @ file://proteusllp_actuarial_library-0.2.8.dev10+g27c24bb-py3-none-any.whl"`
   - **Single line change** when switching to PyPI

3. **`Dockerfile.cpu`** - Copies wheel into image:
   - `COPY proteusllp_actuarial_library-*.whl ./`

### Prerequisites:
- `proteusllp-actuarial-library>=0.2.8` must be available on PyPI

### Once PAL is Published:

**3.0 Switch from Wheel to PyPI** ⚠️ **CRITICAL - DO THIS FIRST**

```bash
# Edit pyproject.toml - Line 27:
# Change from:
# "proteusllp-actuarial-library @ file://proteusllp_actuarial_library-0.2.8.dev10+g27c24bb-py3-none-any.whl",
# To:
# "proteusllp-actuarial-library>=0.2.8",

# Delete the wheel file (no longer needed)
rm proteusllp_actuarial_library-*.whl

# Update Dockerfile.cpu to remove wheel COPY
# Remove line: COPY proteusllp_actuarial_library-*.whl ./

# Commit changes
git add pyproject.toml Dockerfile.cpu
git rm proteusllp_actuarial_library-*.whl
git commit -m "Switch to PyPI PAL dependency

- Replace wheel file with PyPI dependency (>=0.2.8)
- Remove wheel from Dockerfile
- Ready for production publishing"
```

**3.1 Generate Lock File**
```bash
cd /proteus-optimisation-package
git checkout dev

# Generate pdm.lock with PyPI PAL
pdm lock

# Verify lock file created
ls -la pdm.lock
```

**3.2 Test Installation**
```bash
# Install from lock file
pdm install

# Verify PAL installed from PyPI (not local source)
pdm run python -c "import pal; print(pal.__version__)"

# Should show: 0.2.8 (or later)
```

**3.3 Run Full Test Suite**
```bash
# Run all tests with coverage
pdm run pytest tests/ -v --cov=optimizer --cov-report=term-missing

# All 127 tests should pass
# Example output:
# ========================= 127 passed, 3 warnings in 2.12s =========================
```

**3.4 Commit Lock File**
```bash
# Create new feature branch for lock file
git checkout -b feature/add-pdm-lock

# Add lock file
git add pdm.lock

# Commit
git commit -m "Add pdm.lock with PAL 0.2.8 from PyPI

- Generated lock file with proteusllp-actuarial-library>=0.2.8
- All 127 tests passing with PyPI PAL
- Ready for first release"

# Push feature branch
git push -u origin feature/add-pdm-lock
```

**3.5 Create Pull Request**
1. Go to: https://github.com/ProteusLLP/proteusllp-optimisation-package/pulls
2. Create PR: `feature/add-pdm-lock` → `dev`
3. Title: "Add pdm.lock with PAL 0.2.8 from PyPI"
4. Wait for CI checks to pass (static-analysis, test jobs)
5. Merge to `dev`

---

## Phase 4: First Release (After PAL 0.2.8)

### 4.1 Merge dev to main

```bash
# Checkout main
git checkout main
git pull origin main

# Merge dev (no fast-forward for clean history)
git merge --no-ff dev -m "Release v0.1.0: Initial POP package

- Complete PyPI package structure
- 127 tests passing
- Full CI/CD pipeline
- Documentation and examples included
- Ready for production use"

# Push to main
git push origin main
```

### 4.2 Create Release Tag

```bash
# Tag the release
git tag -a v0.1.0 -m "Release v0.1.0: Initial POP package

First production release of Proteus Optimisation Package (POP).

Features:
- Domain-agnostic stochastic optimization engine
- Supports PAL StochasticScalar and FreqSevSims variables
- Multiple metric types: Mean, Std, SpreadVaR
- Composite metrics: Ratio, Product, Sum, Difference
- Linear and non-linear constraints
- Efficient frontier calculations
- Type-safe Pydantic API
- Comprehensive test suite (127 tests)
- Full documentation and examples

Requirements:
- Python >= 3.13
- proteusllp-actuarial-library >= 0.2.8"

# Push tag
git push origin v0.1.0
```

### 4.3 Create GitHub Release

1. Go to: https://github.com/ProteusLLP/proteusllp-optimisation-package/releases/new
2. Tag: `v0.1.0`
3. Title: `v0.1.0 - Initial Release`
4. Description:
```markdown
# Proteus Optimisation Package v0.1.0 🚀

First production release of POP - a domain-agnostic stochastic optimization engine for PAL variables.

## Features

- **Flexible Optimization**: Works with any PAL stochastic variables
- **Multiple Metrics**: Mean, Std, SpreadVaR, plus composite metrics (Ratio, Product, Sum, Difference)
- **Constraints**: Linear and non-linear constraints with automatic validation
- **Efficient Frontier**: Calculate risk-return tradeoffs
- **Type-Safe API**: Pydantic models with comprehensive validation
- **Well Tested**: 127 tests with high coverage

## Installation

```bash
pip install proteusllp-optimisation-package
```

## Quick Start

```python
from pal import StochasticScalar
from optimizer import ObjectiveSpec, OptimizationInput, optimize
from optimizer.config import OptimizationDirection, MetricType

# Create portfolio items
items = [
    StochasticScalar(mean=0.1, std=0.15, name="Asset A"),
    StochasticScalar(mean=0.08, std=0.1, name="Asset B"),
]

# Define objective: maximize mean return
objective = ObjectiveSpec(
    metric_type=MetricType.MEAN,
    direction=OptimizationDirection.MAXIMIZE
)

# Create optimization input
opt_input = OptimizationInput(items=items, objective=objective)

# Optimize!
result = optimize(opt_input.preprocess())
print(f"Optimal weights: {result.optimal_weights}")
```

## Documentation

- **Installation**: https://proteusllp-optimisation-package.readthedocs.io/en/latest/installation.html
- **Quick Start**: https://proteusllp-optimisation-package.readthedocs.io/en/latest/quickstart.html
- **API Reference**: Coming soon

## Requirements

- Python >= 3.13
- proteusllp-actuarial-library >= 0.2.8

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

MIT License - See [LICENSE](LICENSE) for details.
```
5. Check "Set as the latest release"
6. Click "Publish release"

**This triggers:**
- CI pipeline runs on release
- Build job creates wheel + sdist
- Publish job uploads to PyPI (after approval in `pypi-publish` environment)

### 4.4 Verify PyPI Publication

1. Wait for CI publish job to complete
2. Check PyPI: https://pypi.org/project/proteusllp-optimisation-package/
3. Test installation:
```bash
# In a fresh environment
pip install proteusllp-optimisation-package

# Verify version
python -c "import optimizer; print(optimizer.__version__)"
# Should show: 0.1.0
```

---

## Phase 5: ReadTheDocs Setup (After First Release)

### 5.1 Import Project

1. Go to: https://readthedocs.org/dashboard/
2. Click "Import a Project"
3. Select: `ProteusLLP/proteusllp-optimisation-package`
4. Click "Next"

### 5.2 Configure Build

1. Admin → Advanced Settings:
   - Python interpreter: `CPython 3.13`
   - Install Project: ✅ (enabled)
   - Requirements file: (leave empty, uses pyproject.toml)
2. Admin → Environment Variables:
   - Add: `PIP_EXTRA_INDEX_URL` = `https://pypi.org/simple/` (if needed)
3. Save

### 5.3 Trigger Build

1. Go to "Builds" tab
2. Click "Build version: latest"
3. Wait for build to complete
4. Check: https://proteusllp-optimisation-package.readthedocs.io/

---

## Timeline Summary

| Phase | Status | Blocker | Duration |
|-------|--------|---------|----------|
| 1. GitHub Setup | Ready | None | 30 min |
| 2. PyPI Config | Ready | None | 20 min |
| 3. Add pdm.lock | **BLOCKED** | PAL 0.2.8 | 10 min |
| 4. First Release | **BLOCKED** | PAL 0.2.8 | 30 min |
| 5. ReadTheDocs | Ready after Phase 4 | None | 15 min |

**Total Time (after PAL 0.2.8):** ~1.5 hours

---

## Checklist

### Immediate (Can Do Now)
- [ ] Create GitHub repository
- [ ] Push all branches (main, dev, feature/initial-package-structure)
- [ ] Configure branch protection on main
- [ ] Set dev as default branch
- [ ] Configure PyPI trusted publishing
- [ ] Add Codecov token (optional)

### After PAL 0.2.8 Published
- [ ] **CRITICAL: Switch from wheel to PyPI PAL** (pyproject.toml one-line change)
- [ ] Delete wheel file and update Dockerfile
- [ ] Commit the changes
- [ ] Rebuild devcontainer
- [ ] Regenerate pdm.lock with PyPI PAL
- [ ] Test installation with PyPI PAL
- [ ] Run full test suite
- [ ] Create PR with pdm.lock
- [ ] Merge to dev
- [ ] Merge dev to main
- [ ] Tag v0.1.0
- [ ] Create GitHub Release
- [ ] Verify PyPI publication
- [ ] Set up ReadTheDocs

### Post-Release
- [ ] Announce on social media / blog
- [ ] Update dashboard to use PyPI package instead of local source
- [ ] Monitor for issues
- [ ] Plan v0.2.0 features

---

## Notes

- **PAL Dependency**: POP requires PAL to be on PyPI before we can publish
- **Testing**: All 127 tests currently pass with local PAL source
- **CI/CD**: Pipeline is ready, will auto-publish on GitHub Release
- **Documentation**: Sphinx docs are complete, ReadTheDocs will build automatically
- **Versioning**: Using semantic versioning (MAJOR.MINOR.PATCH)

## Contact

For questions or issues, open an issue on GitHub or contact info@proteusllp.com
