if status is-interactive
    # Commands to run in interactive sessions can go here
end

# Initialize Starship prompt
starship init fish | source

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
set mamba_root "$HOME/mambaforge"

if test -f "$mamba_root/bin/conda"
    eval ($mamba_root/bin/conda "shell.fish" "hook" $argv) | source
end

if test -f "$mamba_root/etc/fish/conf.d/mamba.fish"
    source "$mamba_root/etc/fish/conf.d/mamba.fish"
end
# <<< conda initialize <<<

# Set CUDA paths if CUDA is installed
set cuda_root "/usr/local/cuda-11.8"
if test -d "$cuda_root"
    set -x LD_LIBRARY_PATH "$cuda_root/lib64" $LD_LIBRARY_PATH
    set -x PATH "$cuda_root/bin" $PATH
end

# Alias for running stable diffusion
set code_path "$HOME/Code"
set sd_path "$code_path/stable-diffusion/stable-diffusion-webui/runsd.sh"
if test -f "$sd_path"
    alias runsd="$sd_path"
else
    function runsd
        echo "Stable Diffusion not installed at $sd_path"
    end
end
