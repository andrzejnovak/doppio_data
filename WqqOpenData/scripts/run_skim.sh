#!/bin/bash
#SBATCH --partition=submit
#SBATCH --cpus-per-task=1
#SBATCH --mem=6G
#SBATCH --time=02:00:00
#SBATCH --no-requeue
#SBATCH --exclude=submit01,submit08,submit95,submit96
#SBATCH --output=/work/submit/novaka/wqq_opendata/logs/skim_%a.out
set -euo pipefail
cd /work/submit/novaka/wqq_opendata
read -r sample path mc < <(sed -n "${SLURM_ARRAY_TASK_ID}p" jobs.txt)
out=skims/$sample/$(basename $path .root).npz
mkdir -p skims/$sample
[ -s "$out" ] && { echo "exists $out"; exit 0; }
tmp=${TMPDIR:-/tmp}/wqq_$SLURM_JOB_ID; mkdir -p $tmp; trap 'rm -rf $tmp' EXIT
for i in 1 2 3; do xrdcp -s -f root://eospublic.cern.ch/$path $tmp/f.root && break; sleep 30; done
flag=""; [ "$mc" = 1 ] && flag="--mc"
/work/submit/novaka/doppio-paper-gain/.pixi/envs/default/bin/python skim.py $tmp/f.root $out.tmp.npz $flag
python3 -c "import numpy as np,sys;d=np.load('$out.tmp.npz');" && mv $out.tmp.npz $out
# record the true source path inside a sidecar
echo "$path" > $out.src
