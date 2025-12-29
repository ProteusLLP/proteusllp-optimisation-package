<div style="display: flex; align-items: center; gap: 15px;">
  <img src="https://raw.githubusercontent.com/ProteusLLP/proteus-optimisation-package/main/POP.svg" alt="POP Logo" width="80"/>
  <div>
    <h1 style="margin: 0;">Proteus Optimisation Package (POP)</h1>
  </div>
</div>

<br/>

Welcome to the Proteus Optimisation Package documentation!

## Overview

Proteus Optimisation Package (POP) is a domain-agnostic stochastic optimization engine designed to work seamlessly with [PAL (Proteus Actuarial Library)](https://proteusllp-actuarial-library.readthedocs.io/) variables.

## Key Features

- **Domain-Agnostic**: Works with any PAL stochastic variables
- **Multiple Objectives**: Support for composite objectives and constraints
- **Efficient Frontiers**: Trace Pareto-optimal risk-return trade-offs
- **Flexible Constraints**: Equality, inequality, and box constraints
- **Type-Safe**: Comprehensive Pydantic validation

## Contents

```{toctree}
:maxdepth: 2
:caption: User Guide

installation
quickstart
objectives
constraints
examples
```

```{toctree}
:maxdepth: 2
:caption: API Reference

api/models
api/config
api/scipy_interface
api/efficient_frontier
```

```{toctree}
:maxdepth: 1
:caption: Development

contributing
style_guide
changelog
```

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
