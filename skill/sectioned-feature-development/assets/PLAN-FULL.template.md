# PLAN-FULL — 替换为当前功能

此文件是模板，不是已批准计划。示例 SHA/路径/检查命令必须替换为当前仓库事实。单 section 可以保留一项并采用 serial；不得为了使用示例并行图人为制造任务。

## 原始要求和确认
- Requirements Contract 路径、SHA-256、用户确认：
- 原始请求 / 后续更正 / SUPERSEDED / non-goals：
- 最小端到端结果、准确失败样例与 expected outcome：

## Owner、表示和生命周期
- 当前 source→normalizer→storage→API→UI / permission / cleanup 路径：
- 同一规则的权威 owner，避免复制判断：
- 必要的状态转换与重复操作序列：
- 真实环境 gate 的最小可运行探测；不可运行时的准确阻塞：
- 基础修复与局部补丁是否需要用户选择：

## 模型和阶段
- 作者 astra_xhigh；不同实例 astra_xhigh review；复杂计划是否需要 GLM challenge及理由：
- 实现每节选一个 profile，写证据而非“高危=大模型”：
- 探索可按独立问题并行；PLAN 和 PLAN review 串行；section DAG 可并行；同一候选 writer/reviewer 不重叠；feature integration 串行。

## 各 section 的具体行为合同
### S01
- Goal / REQ / owner / AC / tests / failure oracle：
### S02
- Goal / REQ / owner / AC / tests / failure oracle：
### S03
- Goal / REQ / owner / AC / tests / failure oracle：

## 集成和完成
- 固定 integration_order 与每个依赖产物：
- feature branch 与各 worktree 命名，DB/ports/cache 隔离：
- exact candidate review 和 merged-head checks：
- 未证明 composition / required final gates / 环境 blocker：
- 完成后冻结，不把后续请求追加到此 PLAN：

## 可执行调度（唯一机器事实源）
<!-- SFD_PLAN_V4 -->
```json
{
  "schema_version": 4,
  "feature_id": "example-feature",
  "run_id": "example-run",
  "invocation_source": "USER_EXPLICIT",
  "status": "DRAFT",
  "execution_mode": "EXECUTE_WITH_COMMITS",
  "main_branch": "main",
  "feature_branch": "codex/example-feature",
  "base_ref": "0000000000000000000000000000000000000000",
  "branch_authority": "USER_EXPLICIT feature branch from main; replace with actual source",
  "requirements_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
  "max_parallel_writers": 2,
  "parallel_capacity_authority": null,
  "worktree_parent": "git-worktree",
  "integration_order": [
    "S01",
    "S02",
    "S03"
  ],
  "stages": [
    {
      "id": "discover",
      "depends_on": [],
      "parallelism": "bounded-independent-queries",
      "profile": "sfd_explorer",
      "optional": true
    },
    {
      "id": "plan",
      "depends_on": [
        "discover"
      ],
      "parallelism": "serial",
      "profile": "astra_xhigh"
    },
    {
      "id": "plan-review",
      "depends_on": [
        "plan"
      ],
      "parallelism": "serial",
      "profile": "astra_xhigh"
    },
    {
      "id": "execute-dag",
      "depends_on": [
        "plan-review"
      ],
      "parallelism": "section-dag",
      "profile": "per-section"
    },
    {
      "id": "integrate",
      "depends_on": [
        "execute-dag"
      ],
      "parallelism": "serial",
      "profile": "orchestrator"
    },
    {
      "id": "audit",
      "depends_on": [
        "integrate"
      ],
      "parallelism": "serial",
      "profile": "orchestrator"
    }
  ],
  "checks": {
    "S01-focused": {
      "command": "REPLACE_WITH_EXISTING_COMMAND",
      "cwd": ".",
      "environment_id": "isolated-S01"
    },
    "S02-focused": {
      "command": "REPLACE_WITH_EXISTING_COMMAND",
      "cwd": ".",
      "environment_id": "isolated-S02"
    },
    "S03-focused": {
      "command": "REPLACE_WITH_EXISTING_COMMAND",
      "cwd": ".",
      "environment_id": "isolated-S03"
    }
  },
  "sections": [
    {
      "id": "S01",
      "depends_on": [],
      "owner": "shared-contract",
      "requirement_ids": [
        "REQ-001"
      ],
      "write_paths": [
        "src/shared.py",
        "tests/shared"
      ],
      "read_paths": [],
      "exclusive_resources": [],
      "mutates_contracts": [
        "contract-v1"
      ],
      "consumes_contracts": [],
      "parallel_eligible": true,
      "parallel_reason": "Distinct consumer owners after S01 is accepted and integrated; tests use private state.",
      "profile": "sol_medium",
      "model_reason": "Replace with source-grounded decision; this is an example only.",
      "task_features": {
        "analogue": "src/example.py (replace with verified path)",
        "ambiguity": "resolved",
        "semantic_hops": [
          "producer",
          "consumer"
        ],
        "state_coupling": "local",
        "oracle_strength": "decisive",
        "novel_reasoning": false
      },
      "assurance": "TWO",
      "check_ids": [
        "S01-focused"
      ],
      "oracle": "Replace with executable acceptance and failure trace.",
      "acceptance": "REQ-001 observable behavior and existing contracts pass."
    },
    {
      "id": "S02",
      "depends_on": [
        "S01"
      ],
      "owner": "ui-consumer",
      "requirement_ids": [
        "REQ-001"
      ],
      "write_paths": [
        "src/ui",
        "tests/ui"
      ],
      "read_paths": [
        "src/shared.py"
      ],
      "exclusive_resources": [],
      "mutates_contracts": [],
      "consumes_contracts": [
        "contract-v1"
      ],
      "parallel_eligible": true,
      "parallel_reason": "Distinct consumer owners after S01 is accepted and integrated; tests use private state.",
      "profile": "terra_high",
      "model_reason": "Replace with source-grounded decision; this is an example only.",
      "task_features": {
        "analogue": "src/example.py (replace with verified path)",
        "ambiguity": "resolved",
        "semantic_hops": [
          "producer",
          "consumer"
        ],
        "state_coupling": "local",
        "oracle_strength": "decisive",
        "novel_reasoning": false
      },
      "assurance": "TWO",
      "check_ids": [
        "S02-focused"
      ],
      "oracle": "Replace with executable acceptance and failure trace.",
      "acceptance": "REQ-001 observable behavior and existing contracts pass."
    },
    {
      "id": "S03",
      "depends_on": [
        "S01"
      ],
      "owner": "import-consumer",
      "requirement_ids": [
        "REQ-001"
      ],
      "write_paths": [
        "src/importer",
        "tests/importer"
      ],
      "read_paths": [
        "src/shared.py"
      ],
      "exclusive_resources": [],
      "mutates_contracts": [],
      "consumes_contracts": [
        "contract-v1"
      ],
      "parallel_eligible": true,
      "parallel_reason": "Distinct consumer owners after S01 is accepted and integrated; tests use private state.",
      "profile": "luna_xhigh",
      "model_reason": "Replace with source-grounded decision; this is an example only.",
      "task_features": {
        "analogue": "src/example.py (replace with verified path)",
        "ambiguity": "resolved",
        "semantic_hops": [
          "producer",
          "consumer"
        ],
        "state_coupling": "local",
        "oracle_strength": "decisive",
        "novel_reasoning": false
      },
      "assurance": "TWO",
      "check_ids": [
        "S03-focused"
      ],
      "oracle": "Replace with executable acceptance and failure trace.",
      "acceptance": "REQ-001 observable behavior and existing contracts pass."
    }
  ]
}
```
<!-- /SFD_PLAN_V4 -->
