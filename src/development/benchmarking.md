# Benchmarking Infrastructure

## Overview

Bitcoin Commons maintains a comprehensive benchmarking infrastructure to measure and track performance across all components. Benchmarks are automatically generated and published at [benchmarks.thebitcoincommons.org](https://benchmarks.thebitcoincommons.org).

## Benchmark Infrastructure

### bllvm-bench Repository

The benchmarking infrastructure is maintained in a separate repository (`bllvm-bench`) that:

- Runs performance benchmarks across all BLLVM components
- Generates benchmark reports and visualizations
- Publishes results to `benchmarks.thebitcoincommons.org`
- Tracks performance over time
- Compares performance with Bitcoin Core

### Automated Benchmark Generation

Benchmarks are generated automatically via GitHub Actions workflows:

- **Scheduled Runs**: Regular benchmark runs on schedule
- **PR Triggers**: Benchmarks run on pull requests
- **Release Triggers**: Comprehensive benchmarks before releases
- **Results Publishing**: Automatic publishing to benchmark website

## Published Benchmarks

### Benchmark Website

All benchmark results are published at:
- **URL**: [benchmarks.thebitcoincommons.org](https://benchmarks.thebitcoincommons.org)
- **Content**: Performance metrics, comparisons, historical trends
- **Format**: Interactive charts and detailed reports

### Benchmark Categories

Benchmarks cover:

1. **Consensus Performance**
   - Block validation speed
   - Transaction validation speed
   - Script execution performance
   - UTXO operations

2. **Network Performance**
   - P2P message handling
   - Block propagation
   - Transaction relay
   - Network protocol overhead

3. **Storage Performance**
   - Database operations
   - Index operations
   - Cache performance
   - Disk I/O

4. **Memory Performance**
   - Memory usage
   - Allocation patterns
   - Cache efficiency
   - Memory leaks

## Running Benchmarks Locally

### Prerequisites

```bash
# Install Rust benchmarking tools
cargo install criterion

# Install benchmark dependencies
cargo build --release --benches
```

### Run All Benchmarks

```bash
cd bllvm-consensus
cargo bench
```

### Run Specific Benchmark

```bash
# Run specific benchmark suite
cargo bench --bench block_validation

# Run specific benchmark
cargo bench --bench block_validation -- block_connect
```

### Benchmark Configuration

Benchmarks can be configured via environment variables:

```bash
# Set benchmark iterations
export BENCH_ITERATIONS=1000

# Set benchmark warmup time
export BENCH_WARMUP_SECS=5

# Set benchmark measurement time
export BENCH_MEASUREMENT_SECS=10
```

## Benchmark Structure

### Criterion Benchmarks

Benchmarks use the Criterion.rs framework:

```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn benchmark_block_validation(c: &mut Criterion) {
    c.bench_function("block_connect", |b| {
        let block = create_test_block();
        b.iter(|| {
            black_box(validate_block(&block));
        });
    });
}

criterion_group!(benches, benchmark_block_validation);
criterion_main!(benches);
```

### Benchmark Groups

Benchmarks are organized into groups:

- **Block Validation**: Block connection, header validation
- **Transaction Validation**: Transaction parsing, input validation
- **Script Execution**: Script VM performance, opcode execution
- **Cryptographic**: SHA256, double SHA256, signature verification
- **UTXO Operations**: UTXO set updates, lookups, batch operations

## Interpreting Results

### Performance Metrics

Benchmarks report:

- **Throughput**: Operations per second
- **Latency**: Time per operation
- **Memory**: Memory usage per operation
- **CPU**: CPU utilization

### Comparison with Bitcoin Core

Benchmarks include comparisons with Bitcoin Core:

- **Relative Performance**: Speedup/slowdown vs Bitcoin Core
- **Feature Parity**: Functional equivalence verification
- **Optimization Impact**: Performance impact of optimizations

### Historical Trends

Benchmark results track performance over time:

- **Performance Regression Detection**: Identify performance regressions
- **Optimization Validation**: Verify optimization effectiveness
- **Release Impact**: Measure performance impact of releases

## Benchmark Workflows

### GitHub Actions

Benchmark workflows in `bllvm-bench`:

- **Scheduled Benchmarks**: Daily/weekly benchmark runs
- **PR Benchmarks**: Benchmark on pull requests
- **Release Benchmarks**: Comprehensive benchmarks before releases
- **Results Publishing**: Automatic publishing to website

### Benchmark Artifacts

Workflows generate:

- **Benchmark Reports**: Detailed performance reports
- **Visualizations**: Charts and graphs
- **Comparison Data**: Bitcoin Core comparisons
- **Historical Data**: Performance trends

## Performance Targets

### Consensus Performance

- **Block Validation**: Target <100ms per block (mainnet average)
- **Transaction Validation**: Target <1ms per transaction
- **Script Execution**: Target <10ms per script (average complexity)

### Network Performance

- **Block Propagation**: Target <1s for block propagation
- **Transaction Relay**: Target <100ms for transaction relay
- **P2P Overhead**: Target <5% protocol overhead

### Storage Performance

- **Database Operations**: Target <10ms for common queries
- **Index Operations**: Target <1ms for index lookups
- **Cache Hit Rate**: Target >90% cache hit rate

## Benchmark Best Practices

### Benchmark Design

1. **Isolate Components**: Benchmark individual components
2. **Use Realistic Data**: Use real-world data when possible
3. **Warm Up**: Include warmup iterations
4. **Multiple Runs**: Run benchmarks multiple times
5. **Statistical Analysis**: Use statistical methods for accuracy

### Benchmark Maintenance

1. **Regular Updates**: Update benchmarks with code changes
2. **Performance Monitoring**: Monitor for regressions
3. **Documentation**: Document benchmark methodology
4. **Reproducibility**: Ensure benchmarks are reproducible

## Components

The benchmarking infrastructure includes:
- Criterion.rs benchmark framework
- Automated benchmark generation (GitHub Actions)
- Benchmark website (benchmarks.thebitcoincommons.org)
- Performance tracking and visualization
- Bitcoin Core comparisons
- Historical performance trends

**Location**: `bllvm-bench` repository, benchmark results at [benchmarks.thebitcoincommons.org](https://benchmarks.thebitcoincommons.org)

