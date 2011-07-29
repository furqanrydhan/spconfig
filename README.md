# StylePage tools: Python configuration

## Dependencies

This tool has no dependencies outside of standard Python libraries.

## Installation

```bash
pip install spconfig
```

or

```bash
pip install -e "git+http://github.com/stylepage/spconfig.git#egg=spconfig"
```

or

```bash
git clone git@github.com:stylepage/spconfig.git spconfig
pip install -e spconfig
```

## Examples

```python
import spconfig
settings = spconfig.configuration()
```