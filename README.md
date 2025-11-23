## 教育小模型示例：FastAPI + FastAPIMCP + MCP

本仓库重新搭建了一个「大小模型协同」样例流程：

1. 使用 **FastAPI** 定义多个教育领域的 OpenAPI 接口。
2. 通过自定义的 **fastapimcp** 适配器，把这些 HTTP 接口注册成 **MCP 工具**。
3. 任意支持 MCP 的 IDE/Agent（如 Cursor）即可调用这些小模型工具，配合大模型完成教学任务。

---

### 目录结构

```
app/                # FastAPI 应用及领域逻辑
fastapimcp/         # FastAPI -> MCP 轻量适配层
mcp_server.py       # 启动 fastapimcp 的入口
README.md
requirements.txt
```

---

### 1. 安装依赖

```bash
cd "/Users/yanxiangyu/Desktop/educational models"
python -m venv .venv      # 可选
source .venv/bin/activate # Windows 使用 .venv\Scripts\activate
pip install -r requirements.txt
```

---

### 2. 启动 FastAPI HTTP 服务（便于调试）

```bash
python -m app.main
```

默认监听 `http://127.0.0.1:8000`，可访问 `http://127.0.0.1:8000/docs` 查看自动生成的 OpenAPI 文档、在线调试接口。

---

### 3. 通过 fastapimcp 暴露为 MCP 工具

```bash
python mcp_server.py
```

该命令会读取 FastAPI 的全部 POST 路由并注册为 MCP 工具（使用 `mcp.server.fastmcp` 实例），然后通过 **stdio** 与上层大模型代理通信。

如需在 Cursor 中使用，可在 `~/.cursor/mcp.json` 中添加：

```jsonc
{
  "servers": {
    "edu-fastapi-mcp": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "/Users/yanxiangyu/Desktop/educational models"
    }
  }
}
```

---

### 4. 当前包含的“小模型”接口

- `/grade-answer`：主观题评分（关键词覆盖）。
- `/practice-plan`：个性化练习计划。
- `/reflection-questions`：课后反思问题生成。
- `/cognitive-diagnosis`：认知诊断分析（概念掌握、风险、建议）。
- `/knowledge-tracing`：知识追踪（Bayesian 风格掌握度与推荐序列）。
- `/affective-analysis`：情感状态识别与调节提示。
- `/cdm/mastery`：DeepIRT 风格掌握度输出。
- `/kt/predict`：MRTKT/DKVMN 风格掌握 + 下一题正确率。
- `/path/recommend`：基于先修图的学习路径推荐。
- `/sentiment/analyze`：整体情感分类。
- `/sentiment/aspect`：方面级情感分类。
- `/sentiment/intensity`：情感强度回归。

注册为 MCP 后，工具名称与 FastAPI 路径对应，便于在对话中直接调用。

---

### 5. 示例请求与返回

以下均使用 `fastapi.testclient` 实测（状态码均为 200）：

- `/grade-answer`
  ```json
  {"question":"解释光合作用","correct_answer":"植物利用光能将二氧化碳和水转化为有机物并释放氧气的过程","student_answer":"植物用光把二氧化碳和水变成有机物，放出氧气"}
  ```
  ```json
  {"is_correct":false,"similarity":0.0,"matched_keywords":[],"missing_keywords":["植物利用光能将二氧化碳和水转化为有机物并释放氧气的过程"],"feedback":"与标准答案差距较大，可引导学生重新审题并列出要点。"}
  ```
- `/practice-plan`
  ```json
  {"topic":"一次函数","student_level":"初二","weak_points":["斜率意义","图像与解析式转换"],"available_minutes":45}
  ```
  ```json
  {"topic":"一次函数","student_level":"初二","total_minutes":45,"weak_points":["斜率意义","图像与解析式转换"],"phases":[{"name":"回顾核心概念","duration_minutes":15,"activities":["用思维导图复盘「一次函数」相关定义","找出与薄弱点相关的两个例子"]},{"name":"针对性练习","duration_minutes":15,"activities":["优先攻克：斜率意义, 图像与解析式转换","完成 2-3 道示例题，记录错误原因"]},{"name":"迁移与反思","duration_minutes":15,"activities":["尝试一道综合拓展题，写出解题步骤","总结保留问题与改进策略"]}]}
  ```
- `/reflection-questions`
  ```json
  {"lesson_title":"牛顿第二定律","skills_focus":["建模","数据分析"],"difficulty":"medium"}
  ```
  ```json
  {"lesson_title":"牛顿第二定律","difficulty":"medium","questions":["本课知识与之前内容有什么联系？","如果向同学讲授这个内容，你会怎么安排步骤？","在本课中，你如何体现「建模」这一能力？","在本课中，你如何体现「数据分析」这一能力？"]}
  ```
- `/cognitive-diagnosis`
  ```json
  {"student_id":"S001","subject":"代数","concept_snapshots":[{"concept_name":"一次函数","attempts":10,"correct":8,"misconceptions":["忽略截距"]},{"concept_name":"方程求解","attempts":6,"correct":2,"misconceptions":["移项错误","系数漏写"]}],"recent_behaviors":["课堂走神","作业按时提交"]}
  ```
  ```json
  {"student_id":"S001","subject":"代数","overall_mastery":0.567,"strengths":[],"risks":["方程求解"],"concepts":[{"concept_name":"一次函数","mastery":0.8,"level":"发展中","misconceptions":["忽略截距"],"recommendation":"安排变式练习，突出对比 忽略截距。"},{"concept_name":"方程求解","mastery":0.333,"level":"高风险","misconceptions":["移项错误","系数漏写"],"recommendation":"回到概念本源，结合具体例子重新建模。"}],"summary":"S001 在 代数 中整体掌握度约为 57%。优势概念：暂未形成亮点；风险概念：方程求解。行为观察：课堂走神、作业按时提交。"}
  ```
- `/knowledge-tracing`
  ```json
  {"student_id":"S002","interactions":[{"skill":"分式化简","correct":true,"time_spent_seconds":50,"confidence":0.8},{"skill":"分式化简","correct":false,"time_spent_seconds":140,"confidence":0.4},{"skill":"方程求解","correct":true,"time_spent_seconds":90,"confidence":0.7}],"prior_mastery":{"方程求解":0.6}}
  ```
  ```json
  {"student_id":"S002","skills":[{"skill":"方程求解","probability_mastery":0.714,"trend":"平稳","next_action":"保持混合题训练，关注错误类型。"},{"skill":"分式化简","probability_mastery":0.265,"trend":"下降","next_action":"回到基础例题，配合讲解反馈。"}],"recommended_sequence":["分式化简","方程求解"]}
  ```
- `/affective-analysis`
  ```json
  {"student_id":"S003","current_task":"几何证明","affective_signals":[{"channel":"face","emotion":"frustration","intensity":0.7,"evidence":"眉头紧皱"},{"channel":"keystroke","emotion":"bored","intensity":0.3,"evidence":"低频输入"}],"recent_performance":"近两次练习正确率下降"}
  ```
  ```json
  {"student_id":"S003","state":{"dominant_emotion":"frustration","confidence":0.7,"message":"检测到 S003 在「几何证明」中可能感到挫折。建议先处理最关键步骤。 学习表现备注：近两次练习正确率下降。","regulation_strategies":["给出分步提示并降低任务难度。","安排 2 分钟呼吸或伸展休息。"]},"nudges":["使用 1-2 句同理心话语回应学生感受。","根据情绪状态对「几何证明」调整脚手架层级。"]}
  ```
- `/cdm/mastery`
  ```json
  [{"student_id":1,"item_id":101,"correct":1},{"student_id":1,"item_id":102,"correct":0},{"student_id":1,"item_id":103,"correct":1}]
  ```
  ```json
  {"mastery":{"K1":0.7,"K2":0.6833333333333333,"K3":0.6666666666666666},"raw_vector":[0.7,0.6833333333333333,0.6666666666666666]}
  ```
- `/kt/predict`
  ```json
  [{"item_id":201,"correct":1,"timestamp":0.0},{"item_id":202,"correct":0,"timestamp":1.0},{"item_id":203,"correct":1,"timestamp":2.2}]
  ```
  ```json
  {"next_question_correct_prob":0.651,"mastery":{"K1":0.595,"K2":0.658,"K3":0.626}}
  ```
- `/path/recommend`
  ```json
  {"mastery":{"K1":0.9,"K2":0.6,"K3":0.4,"K4":0.8},"threshold":0.75,"max_recommend":3}
  ```
  ```json
  {"recommended_path":["K2","K3","K5"]}
  ```
- `/sentiment/analyze`
  ```json
  {"text":"老师讲得很清晰，也很有趣"}
  ```
  ```json
  {"probabilities":{"负面":0.1,"中性":0.1,"正面":0.9},"label":"正面"}
  ```
- `/sentiment/aspect`
  ```json
  {"text":"课堂气氛有趣，但作业有点难","aspects":["课堂","作业"]}
  ```
  ```json
  {"aspect_results":{"课堂":"负面","作业":"负面"}}
  ```
- `/sentiment/intensity`
  ```json
  {"text":"这节课非常棒，非常喜欢"}
  ```
  ```json
  {"score":0.583}
  ```

---

### 6. 后续扩展建议

1. 在 `app/services.py` 中替换规则逻辑为真实的小模型推理。
2. 新增 FastAPI 路由后，重新运行 `python mcp_server.py` 即可自动注册新的 MCP 工具。
3. 如需部署为 HTTP + MCP 双模式，可将 FastAPIMCPBridge 改造成读取远程 URL，或在不同端口上运行。

通过这种方式，大模型能够把可控的教育小模型（HTTP 接口）当作工具调用，实现稳定、可审计的“大小模型协同”。
