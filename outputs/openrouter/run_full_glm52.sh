#!/usr/bin/env bash
# Full BehaviorBench run on tencent/hy3 via OpenRouter — all 39 tasks at full
# sample sizes. This is the exact script that produced the JSONs in z-ai/glm-5.2/
# and the log in run.log.
#
# Retries each task up to 3x (transient errors / 429) and continues past a
# persistent failure so one bad task cannot abort the whole sweep.
#
# Success is detected by grepping for "Saved results" rather than the pipeline
# exit code: `cmd | grep | tee` returns tee's status, which masks failures.
set -u
export PATH="$HOME/.local/bin:$PATH"
export UV_PROJECT_ENVIRONMENT="$HOME/.venvs/behaviorbench-wf"   # py3.12 venv (has BLEURT)
export UV_LINK_MODE=copy
cd /mnt/c/Users/owenh/behaviorbench_eval

LOG=outputs/openrouter/run_glm52.log; : > "$LOG"
TMP=outputs/openrouter/.task_glm52.out
MODEL="z-ai/glm-5.2"
COMMON="--model-type openai --model-name $MODEL --api-base https://openrouter.ai/api/v1 --concurrency 8 --reasoning-effort none --output-dir outputs/openrouter"
FILTER='oneDNN|cpu_feature_guard|AVX|absl::InitializeLog|TF-TRT|TensorRT|W0000|I0000|E0000|external/local_xla|rebuild TensorFlow|CUDA|GPU|cuda_executor|DOCTYPE|_next|keyframe|pricing table|Completed [0-9]'
KEEP='Running |BLEURT:|ROUGE|_distance:|_averaged:|MAE|accuracy|num_failed_parses:|num_samples:|win_rate|Saved results'

ok=0; failed=0; failed_list=""
run () {  # $1=task(s)  $2=sampleflag(optional)
  local tries=0
  echo "===== $1 =====" | tee -a "$LOG"
  while : ; do
    tries=$((tries+1))
    timeout 5400 uv run --no-sync behaviorbench-eval --task $1 ${2:-} $COMMON > "$TMP" 2>&1
    if grep -q "Saved results" "$TMP"; then
      grep -aviE "$FILTER" "$TMP" | grep -aiE "$KEEP" | tail -8 | tee -a "$LOG"
      ok=$((ok+1)); echo "" | tee -a "$LOG"; return 0
    fi
    if [ "$tries" -ge 3 ]; then
      echo "  !! FAILED after $tries attempts — skipping" | tee -a "$LOG"
      grep -aiE "429|rate limit|RuntimeError|NoneType|Error code|Daily limit" "$TMP" | tail -2 | tee -a "$LOG"
      failed=$((failed+1)); failed_list="$failed_list $1"; echo "" | tee -a "$LOG"; return 1
    fi
    echo "  attempt $tries failed; retrying..." | tee -a "$LOG"
  done
}

# 1) game_behavior (9) — full = default 1000 samples per game
for g in dictator bomb guessing public_goods push_pull trust_banker trust_investor ultimatum_proposer ultimatum_responder; do
  run "game_behavior_$g"
done

# 2) prediction / config families (25) — full datasets (no --num-samples cap)
for t in \
  acrossgame_behavior_dictator acrossgame_behavior_ultimatum_proposer acrossgame_behavior_ultimatum_responder \
  acrossgame_behavior_trust_investor acrossgame_behavior_trust_banker acrossgame_behavior_public_goods \
  acrossgame_behavior_bomb acrossgame_behavior_guessing acrossgame_behavior_push_pull \
  multiround_behavior_dictator multiround_behavior_trust_investor multiround_behavior_trust_banker_inv50 \
  multiround_behavior_trust_banker_inv100 multiround_behavior_public_goods multiround_behavior_bomb \
  multiround_behavior_guessing multiround_behavior_push_pull \
  acrossdim_pers_score demo_pred_age missing_surv_resp pers_score_pred seq_surv_resp surv_resp_pred \
  strategic_gameplay_guessing ieo_economics ; do
  run "$t"
done

# 3) workflow free-text (5, run together) — full, scored with BLEURT + ROUGE-1
run "workflow_idea_generation workflow_method_recommendation workflow_outcome_prediction workflow_title_prediction workflow_impact_prediction"

echo "===== RUN DONE: ok=$ok failed=$failed  failed:[$failed_list] =====" | tee -a "$LOG"
