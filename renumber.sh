#!/usr/bin/env bash
#
# renumber.sh — renumber image_NNN.png files consecutively, filling gaps.
#
# Usage:
#   ./renumber.sh [--dry-run] [DIRECTORY]
#
# Example:
#   image_001.png image_005.png image_006.png
#     -> image_001.png image_002.png image_003.png
#
# Environment:
#   START=0   start numbering at 0 instead of 1

set -euo pipefail

dry_run=0
if [[ "${1:-}" == "-n" || "${1:-}" == "--dry-run" ]]; then
    dry_run=1; shift
fi

dir="${1:-.}"
prefix='image_'
suffix='.png'
start="${START:-1}"

cd -- "$dir"

# --- Collect candidates -----------------------------------------------
shopt -s nullglob
candidates=( "${prefix}"*"${suffix}" )
shopt -u nullglob

if (( ${#candidates[@]} == 0 )); then
    echo "No files matching ${prefix}*${suffix} in $PWD" >&2
    exit 1
fi

# --- Sort by numeric index (skip names whose middle part isn't digits) -
sorted=()
while IFS= read -r f; do
    sorted+=( "$f" )
done < <(
    for f in "${candidates[@]}"; do
        [[ -f $f ]] || continue
        num=${f#"$prefix"}
        num=${num%"$suffix"}
        [[ $num =~ ^[0-9]+$ ]] || continue
        printf '%d\t%s\n' "$((10#$num))" "$f"   # 10# -> avoid octal pitfalls
    done | sort -n | cut -f2-
)

if (( ${#sorted[@]} == 0 )); then
    echo "No ${prefix}<digits>${suffix} files found in $PWD" >&2
    exit 1
fi

# --- Compute the new names --------------------------------------------
newnames=()
n=$start
for _ in "${sorted[@]}"; do
    newnames+=( "$(printf '%s%03d%s' "$prefix" "$n" "$suffix")" )
    n=$(( n + 1 ))
done

# --- Dry run -----------------------------------------------------------
if (( dry_run )); then
    for i in "${!sorted[@]}"; do
        printf 'mv -- %q %q\n' "${sorted[i]}" "${newnames[i]}"
    done
    exit 0
fi

# --- Phase 1: move everything to unique temporary names ----------------
# Two-phase rename is mandatory: a plain one-pass rename can clobber files
# that haven't been processed yet (e.g. shifting 1..5 -> 2..6).
tmps=()
i=0
for f in "${sorted[@]}"; do
    t=".renumber.$$.$i"
    while [[ -e $t ]]; do t="${t}_"; done
    mv -- "$f" "$t"
    tmps+=( "$t" )
    i=$(( i + 1 ))
done

# --- Phase 2: move temporary names to the final names ------------------
for i in "${!tmps[@]}"; do
    mv -- "${tmps[i]}" "${newnames[i]}"
    printf '%s -> %s\n' "${sorted[i]}" "${newnames[i]}"
done
