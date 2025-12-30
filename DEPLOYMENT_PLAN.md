# Deployment Plan for Proteus Optimisation Package (POP)

This document outlines the remaining steps to deploy POP to PyPI.

## Current Status

✅ **Complete:**
- Full package structure (optimizer/, tests/, examples/, docs/)
- 127 passing tests with comprehensive coverage
- Pydantic models with validation
- Docker support (Dockerfile.cpu + Dockerfile.gpu)
- Devcontainer configs (CPU + GPU variants)
- GitHub Actions CI/CD pipeline (static analysis, tests, build, publish)
- Documentation (Sphinx + ReadTheDocs integration)
- All template files (STYLE_GUIDE, CONTRIBUTING, CLA, LICENSE)
- Placeholder logo (POP.svg)
- Git repository initialized with proper branch structure:
  - `main` - production branch
  - `dev` - development branch (default)
  - `feature/initial-package-structure` - feature branch merged to dev
  - `fix/add-dev-dependencies` - current work branch
- Remote configured: `https://github.com/ProteusLLP/proteus-optimisation-package`
- GitHub repository created (currently private)

⚠️ **Current Development Setup:**
- Using local PAL wheel: `proteusllp_actuarial_library-0.2.8.dev10+g27c24bb-py3-none-any.whl`
- PAL 0.2.8 is available on PyPI - ready to switch
- Single line change needed in `pyproject.toml` to switch to PyPI

🔄 **Next Steps:**
- Complete Phase 2: GitHub repository configuration and PyPI setup
- Complete Phase 3: Switch to PyPI PAL and publish first release

---

## Phase 2: GitHub Repository Configuration & PyPI Setup

**Prerequisites:** GitHub repository created, branches pushed

**Time Estimate:** 30-45 minutes

### 2.1 Configure Repository Settings to Match PAL

Open both repositories side-by-side for consistency:
- **PAL**: https://github.com/ProteusLLP/proteusllp-actuarial-library/settings
- **POP**: https://github.com/ProteusLLP/proteus-optimisation-package/settings

#### Branch Protection Rules

**For `main` branch:**
1. Settings → Branches → Add branch protection rule
2. Branch name pattern: `main`
3. Enable:
   - ☑️ Require a pull request before merging
     - Require approvals: `1`
     - Dismiss stale pull request approvals when new commits are pushed
   - ☑️ Require status checks to pass before merging
     - Add status check: `test` (from CI workflow)
     - Require branches to be up to date before merging
   - ☑️ Require conversation resolution before merging
   - Leave unchecked: Allow force pushes, Allow deletions
4. Click Create

**Repeat for `dev` branch** with same settings.

#### Actions Permissions

1. Settings → Actions → General
2. Actions permissions:
   - Select: ⦿ Allow all actions and reusable workflows
3. Workflow permissions:
   - Select: ⦿ Read and write permissions
   - ☑️ Allow GitHub Actions to create and approve pull requests
4. Click Save

#### Security Settings

1. Settings → Code security and analysis
2. Enable:
   - Dependabot alerts
   - Dependabot security updates
3. Optional: Enable code scanning

### 2.2 Update CI Workflow for PR Testing

Update `.github/workflows/ci.yaml` to run on PRs to `dev`:

```yaml
pull_request:
  branches: [main, dev]  # Add 'dev' here
```

Commit and push this change.

### 2.3 Create GitHub Environment for PyPI Publishing

1. Settings → Environments → New environment
2. Name: `pypi-publish`
3. Click Configure environment
4. Required reviewers:
   - ☑️ Required reviewers
   - Add team members who can approve releases
5. Optional: ☑️ Wait timer (e.g., 5 minutes)
6. Click Save protection rules

### 2.4 Configure PyPI Trusted Publishing

**On PyPI:**
1. Go to: https://pypi.org/manage/account/publishing/
2. Click "Add a new pending publisher"
3. Fill in the form:
   - **PyPI Project Name**: `proteusllp-optimisation-package`
   - **Owner**: `ProteusLLP`
   - **Repository name**: `proteus-optimisation-package`
   - **Workflow name**: `ci.yaml`
   - **Environment name**: `pypi-publish`
4. Click "Add"

**Note:** This creates a "pending publisher" - the project will be created on PyPI when you first publish.

### 2.5 Optional: Add Codecov Token

**For code coverage reporting:**
1. Create account at: https://codecov.io/
2. Get token for repository
3. GitHub Settings → Secrets and variables → Actions → New repository secret
   - Name: `CODECOV_TOKEN`
   - Secret: (paste token)
4. Click "Add secret"

---

## Phase 3: Switch to PyPI PAL and First Release

**Prerequisites:** Phase 2 complete, PAL 0.2.8 available on PyPI ✅

**Time Estimate:** 20-30 minutes

### 3.1 Switch from Wheel to PyPI PAL (5 minutes)

**On branch `fix/add-dev-dependencies` or create new branch:**

```bash
# Edit pyproject.toml line 36-37
# Change from:
#   "proteusllp-actuarial-library @ file://proteusllp_actuarial_library-0.2.8.dev10+g27c24bb-py3-none-any.whl",
# To:
#   "proteusllp-actuarial-library>=0.2.8",

# Regenerate lock file
pdm lock --update-reuse

# Test installation
pdm install

# Verify PAL is from PyPI
pdm run python -c "import pal; print(pal.__version__)"
# Should show: 0.2.8 (or later)

# Run tests to ensure everything works
pdm run pytest tests/ -v

# Delete wheel file (no longer needed)
rm proteusllp_actuarial_library-*.whl

# Update Dockerfile.cpu to remove wheel COPY line

# Commit changes
git add pyproject.toml pdm.lock Dockerfile.cpu
git rm proteusllp_actuarial_library-*.whl
git commit -m "Switch to PyPI PAL dependency

- Replace wheel file with PyPI dependency (>=0.2.8)
- Remove wheel from Dockerfile
- Ready for production publishing"

git push
```

### 3.2 Merge to Main (5 minutes)

```bash
# Create PR: fix/add-dev-dependencies → dev
# Review and merge via GitHub UI

# After merge to dev, create PR: dev → main
# Review and merge via GitHub UI

# Or merge directly if you prefer:
git checkout main
git pull origin main
git merge --no-ff dev -m "Release v0.1.0: Initial POP package

- Complete PyPI package structure
- 127 tests passing
- Full CI/CD pipeline
- Documentation and examples included
- Ready for production use"

git push origin main
```

### 3.3 Make Repository Public (1 minute)

**Required before publishing to PyPI:**
1. Settings → General → Scroll to "Danger Zone"
2. Click "Change visibility"
3. Select "Make public"
4. Type repository name to confirm
5. Click "I understand, change repository visibility"

### 3.4 Create GitHub Release (10 minutes)

**Tag and release:**
```bash
# Ensure you're on main with latest changes
git checkout main
git pull origin main

# Create and push tag
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

git push origin v0.1.0
```

**Create GitHub Release:**
1. Go to: https://github.com/ProteusLLP/proteus-optimisation-package/releases/new
2. Choose tag: `v0.1.0`
3. Release title: `v0.1.0 - Initial Release`
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

## Requirements

- Python >= 3.13
- proteusllp-actuarial-library >= 0.2.8

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

MIT License - See [LICENSE](LICENSE) for details.
```
5. Check: ☑️ **Set as the latest release**
6. Click **Publish release**

**This triggers:**
- CI pipeline runs on release tag
- Build job creates wheel + sdist
- Publish job uploads to PyPI (requires approval in `pypi-publish` environment)

### 3.5 Verify PyPI Publication (5 minutes)

1. **Approve the deployment** (if required reviewers configured):
   - Go to: Actions tab → running workflow
   - Review and approve the `pypi-publish` job

2. **Wait for CI to complete** (2-5 minutes)

3. **Check PyPI**:
   - https://pypi.org/project/proteusllp-optimisation-package/

4. **Test installation**:
```bash
# In a fresh environment
pip install proteusllp-optimisation-package

# Verify version
python -c "import optimizer; print(optimizer.__version__)"
# Should show: 0.1.0

# Test basic functionality
python -c "from optimizer import ObjectiveSpec, OptimizationDirection, MetricType; print('✓ Import successful')"
```

---

## Phase 4: Post-Release Setup (Optional)

### 4.1 ReadTheDocs Setup

1. Go to: https://readthedocs.org/dashboard/
2. Click "Import a Project"
3. Select: `ProteusLLP/proteus-optimisation-package`
4. Configure:
   - Python interpreter: `CPython 3.13`
   - Install Project: ✅ (uses pyproject.toml)
5. Trigger build
6. Verify: https://proteusllp-optimisation-package.readthedocs.io/

### 4.2 Update Dashboard to Use PyPI Package

Once published, update any dependent projects (like the dashboard) to use:
```bash
pip install proteusllp-optimisation-package
```

Instead of local source/wheel installations.

---

## Timeline Summary

| Phase | Status | Duration | Dependencies |
|-------|--------|----------|--------------|
| 1. Git Setup | ✅ Complete | - | None |
| 2. GitHub Config & PyPI Setup | 🔄 Ready | 30-45 min | GitHub repo |
| 3. Switch to PyPI PAL & Release | 🔄 Ready | 20-30 min | Phase 2, PAL on PyPI ✅ |
| 4. Post-Release (Optional) | ⏳ After release | 15 min | Phase 3 |

**Total Time (Phases 2-3):** ~1 hour

---

## Checklist

### Phase 2: GitHub Configuration & PyPI Setup
- [ ] Configure branch protection rules (main, dev)
- [ ] Set Actions permissions (read/write, allow PR creation)
- [ ] Enable Dependabot alerts and security updates
- [ ] Update CI to run on PRs to dev branch
- [ ] Create `pypi-publish` GitHub environment with reviewers
- [ ] Configure PyPI Trusted Publishing pending publisher
- [ ] Optional: Add Codecov token

### Phase 3: Switch to PyPI PAL & First Release
- [ ] Create branch for PAL switch
- [ ] Edit pyproject.toml to use PyPI PAL (>=0.2.8)
- [ ] Regenerate pdm.lock file
- [ ] Test installation with PyPI PAL
- [ ] Run full test suite (verify 127 tests pass)
- [ ] Delete wheel file and update Dockerfile
- [ ] Commit and push changes
- [ ] Merge to dev branch
- [ ] Merge dev to main
- [ ] Make repository public
- [ ] Create tag v0.1.0
- [ ] Push tag to GitHub
- [ ] Create GitHub Release with tag v0.1.0
- [ ] Approve PyPI deployment (if reviewers configured)
- [ ] Verify package on PyPI
- [ ] Test pip install proteusllp-optimisation-package

### Phase 4: Post-Release (Optional)
- [ ] Set up ReadTheDocs
- [ ] Update dashboard to use PyPI package
- [ ] Announce release
- [ ] Monitor for issues

---

## Notes

- **PAL Dependency**: PAL 0.2.8+ is now on PyPI ✅
- **Testing**: All 127 tests pass with local PAL wheel
- **CI/CD**: Pipeline ready, will auto-publish on GitHub Release
- **Documentation**: Sphinx docs complete, ReadTheDocs will build automatically
- **Versioning**: Using semantic versioning (MAJOR.MINOR.PATCH)
- **Repository**: Currently private, will be made public before first release

## Contact

For questions or issues, open an issue on GitHub or contact info@proteusllp.com


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
