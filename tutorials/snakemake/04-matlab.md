# Step 4.2: Plot Results with MATLAB
Now create a new rule to plot using MATLAB:

```python
rule plot_with_matlab:
    input:
        "derivatives/hilbert/freq-{freq}_r-{r}_phase.npy"
    output:
        "figures/matlab-plot/freq-{freq}_r-{r}_phase.png"
    shell:
        matlab2shell()
```

create a new file `scripts/plot.m` with the following content:

```matlab
function plot_hilbert_signal(input_file, output_file)
%PLOT_HILBERT_SIGNAL Load a signal, plot it, and save the figure.
%   plot_hilbert_signal(input_file, output_file)

% Load the signal
sig = load(input_file);

% If load returns a struct, extract the first field
if isstruct(sig)
    fn = fieldnames(sig);
    sig = sig.(fn{1});
end

% Ensure sig is a vector
sig = squeeze(sig);

% Plot the signal
fig = figure('Position', [100, 100, 800, 400]);
plot(sig);
title('Hilbert Transform Result');
xlabel('Sample');
ylabel('Amplitude');

% Save the figure
saveas(fig, output_file);

% Close the figure to free resources
close(fig);
end

% Invoke the function with Snakemake-provided paths
plot_hilbert_signal(snakemake.input{1}, snakemake.output{1});
```

---

# Step 5: Complete Snakefile

