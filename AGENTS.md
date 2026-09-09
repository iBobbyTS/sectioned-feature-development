# sectioned-feature-development 优化
你负责优化本项目。用户的输入可能包含：audit packs、用户主动发现的问题、建议学习的外部文档、环境更新、新版LLM。

## 输出
输出整个项目，文件结构
```
agents/
    本项目所需的agent定义
docs/
    version-history/
        v*.*.*/
            PROMPT.md   用户原始prompt原样写入
            AUDIT_INTAKE.csv    AUDIT_PACK的分析，不得包含敏感信息，可以包含项目的逻辑、流程缺陷等非敏感用于分析的信息。
            RESEARCH.md (根据PROMPT和AUDIT_PACK_ANALYSIS搜索的外部资料、提取的事实和可信度(比如博客/技术报告/社区讨论))
            UPDATES.md (如何通过输入信息得出本次的修改)
            appendix/
                其他需要包含的文件
            !不需要包含previous version baseline
scripts
skill       sectioned-feature-development和其他依赖skill，必须按照 OpenAI skill-creator skill的要求验证。
tests
.gitignore
AGENTS.md   本文件（对你的职责说明和项目契约）
README.md   简要的执行流程、设计理念、和安装方法。
VERSION
```