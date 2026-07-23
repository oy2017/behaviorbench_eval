#!/usr/bin/env bash
# Full BehaviorBench run on z-ai/glm-5.2 with the model's DEFAULT settings —
# no --reasoning-effort flag, so reasoning is ON (GLM-5.2 reasons by default).
# This matches the paper's provider-defaults convention. Counterpart to the
# reasoning-disabled run in z-ai/glm-5.2/ (which passed --reasoning-effort none).
#
# All 39 tasks at full sample sizes. Results live at
# outputs/openrouter/reasoning/z-ai/glm-5.2/ (the pipeline appends the model
# name to --output-dir); the reasoning-disabled run sits beside them in
# no-reasoning/.
#
# Resumable: invocations whose result JSON already exists are skipped, so
# after an interruption (e.g. OpenRouter credit exhaustion) rerunning the
# script only executes the missing tasks.
#
# Runs 10 parallel lanes, each at --concurrency 12 (~120 calls in flight).
# The workflow lane starts first because its BLEURT scoring is a CPU-bound
# tail. Same per-task retry (3x) and "Saved results" success detection as
# run_full_glm52.sh.
set -u
export PATH="$HOME/.local/bin:$PATH"
export UV_PROJECT_ENVIRONMENT="$HOME/.venvs/behaviorbench-wf"   # py3.12 venv (has BLEURT)
export UV_LINK_MODE=copy
cd /mnt/c/Users/owenh/behaviorbench_eval

OUT=outputs/openrouter/reasoning
LOGDIR=outputs/openrouter/logs_glm52_reasoning
mkdir -p "$LOGDIR"
MODEL="z-ai/glm-5.2"
COMMON="--model-type openai --model-name $MODEL --api-base https://openrouter.ai/api/v1 --concurrency 12 --output-dir $OUT"

run_lane () {  # $1=lane name, remaining args = one invocation's task list each
  local lane=$1; shift
  local log="$LOGDIR/$lane.log" tmp="$LOGDIR/$lane.out"
  : > "$log"
  for tasks in "$@"; do
    # Resume support: skip invocations whose result JSON already exists.
    # The combined workflow invocation saves as combined_5subtasks_<ts>.json.
    local marker
    case "$tasks" in workflow_*) marker=combined_5subtasks ;; *) marker="${tasks%% *}" ;; esac
    if ls "$OUT/z-ai/glm-5.2/${marker}"_2*.json >/dev/null 2>&1; then
      echo "===== $tasks — already done, skipping =====" >> "$log"
      continue
    fi
    local tries=0
    echo "===== $tasks =====" >> "$log"
    while : ; do
      tries=$((tries+1))
      timeout 7200 uv run --no-sync behaviorbench-eval --task $tasks $COMMON > "$tmp" 2>&1
      if grep -q "Saved results" "$tmp"; then
        grep -aE "Saved results|_distance:|MAE|accuracy|BLEURT:|num_failed_parses:" "$tmp" | tail -6 >> "$log"
        break
      fi
      if [ "$tries" -ge 3 ]; then
        echo "  !! FAILED after $tries attempts — skipping: $tasks" >> "$log"
        grep -aiE "429|rate limit|RuntimeError|Error code" "$tmp" | tail -2 >> "$log"
        break
      fi
      echo "  attempt $tries failed; retrying..." >> "$log"
    done
  done
  echo "LANE DONE" >> "$log"
}

# Workflow first: its BLEURT scoring is the CPU-bound critical path.
run_lane wf "workflow_idea_generation workflow_method_recommendation workflow_outcome_prediction workflow_title_prediction workflow_impact_prediction" &
run_lane gameA game_behavior_dictator game_behavior_bomb game_behavior_guessing game_behavior_public_goods game_behavior_push_pull &
run_lane gameB game_behavior_trust_banker game_behavior_trust_investor game_behavior_ultimatum_proposer game_behavior_ultimatum_responder &
run_lane acrossA acrossgame_behavior_dictator acrossgame_behavior_ultimatum_proposer acrossgame_behavior_ultimatum_responder acrossgame_behavior_trust_investor acrossgame_behavior_trust_banker &
run_lane acrossB acrossgame_behavior_public_goods acrossgame_behavior_bomb acrossgame_behavior_guessing acrossgame_behavior_push_pull &
run_lane mrA multiround_behavior_dictator multiround_behavior_trust_investor multiround_behavior_trust_banker_inv50 multiround_behavior_trust_banker_inv100 &
run_lane mrB multiround_behavior_public_goods multiround_behavior_bomb multiround_behavior_guessing multiround_behavior_push_pull &
run_lane pers acrossdim_pers_score pers_score_pred demo_pred_age &
run_lane surv missing_surv_resp seq_surv_resp surv_resp_pred &
run_lane misc strategic_gameplay_guessing ieo_economics &
wait

saved=$(cat "$LOGDIR"/*.log | grep -c "Saved results")
failed=$(cat "$LOGDIR"/*.log | grep -c "FAILED")
echo "===== RUN DONE: saved=$saved failed=$failed ====="
grep -l "FAILED" "$LOGDIR"/*.log 2>/dev/null || true
