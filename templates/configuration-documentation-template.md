# Configuration Documentation Template

**Purpose**: Template for documenting configuration systems in a reference + examples format.

## Structure

### 1. Overview (50-100 words)
- What the configuration controls
- Where it's defined
- How it's loaded
- **Present tense** - describes current system

### 2. Configuration Structure (100-200 words)
- File format (YAML, TOML, etc.)
- Schema
- Key organization
- **Complete schema** - not just links
- **Examples** of structure

### 3. Configuration Reference (200-400 words)
- Table of all options
- Type, default, description
- Validation rules
- **Complete table** - all options documented
- **No "see config file"** - include actual details

### 4. Usage Examples (100-200 words)
- Common configurations
- Use case examples
- **Complete examples** - not just snippets
- **Multiple examples** for different scenarios

### 5. Advanced Configuration (100-200 words)
- Advanced options
- Performance tuning
- Security considerations

### 6. See Also (Links)
- Related documentation
- Schema reference
- **Supplement, don't replace** content

## Minimum Requirements

- **500+ words** substantive content
- **Complete configuration table** (all options)
- **Multiple examples** (different scenarios)
- **No placeholder text**
- **Actual defaults** documented

## Example Structure

```markdown
# Configuration System Name

## Overview

[50-100 words on what it controls]

## Configuration Structure

[100-200 words on format and schema]

```yaml
# Example structure
key: value
```

## Configuration Reference

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `key1` | `string` | `"default"` | Description |
| `key2` | `number` | `100` | Description |

## Usage Examples

### Example 1: [Scenario]

```yaml
# Complete configuration example
```

### Example 2: [Scenario]

```yaml
# Complete configuration example
```

## Advanced Configuration

[100-200 words on advanced options]

## See Also

- [Schema Reference](link)
```



