文本生成模型能够基于输入的提示词（Prompt）创作出逻辑清晰、连贯的文本。

文本生成模型所需的输入可以是简单的关键词、一句话概述或是更复杂的指令和上下文信息。模型通过分析海量数据学习语言模式，广泛应用于：

-   **内容创作**：生成新闻报道、商品介绍及短视频脚本。
    
-   **客户服务**：驱动聊天机器人提供全天候支持，解答常见问题。
    
-   **文本翻译**：实现跨语言的快速精准转换。
    
-   **摘要生成**：提炼长文、报告及邮件的核心内容。
    
-   **法律文档编写**：生成合同模板、法律意见书的基础框架。
    

更多示例可以参考[文本生成样例](https://bailian.console.aliyun.com/?tab=app#/plugin-market/prompt)。

## **模型选型建议**

### **服务地域**

阿里云百炼提供[北京](https://bailian.console.aliyun.com/?tab=model#/model-market)、[新加坡](https://modelstudio.console.aliyun.com/?tab=doc#/doc/?type=model&url=2840914)和[弗吉尼亚](https://modelstudio.console.aliyun.com/us-east-1?tab=doc#/doc/?type=model&url=2840914)地域的模型服务，各地域的API Key不同，选择邻近地域调用可降低网络延迟，详情请参见[选择部署模式](https://help.aliyun.com/zh/model-studio/regions/)。

### **通用模型**

千问文本生成模型兼容[OpenAI调用方式](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#28f6fd00cfp2q)，适用于智能客服、文本创作、内容润色以及摘要总结等多种场景。

-   [千问Plus](https://help.aliyun.com/zh/model-studio/models#5ef284d4ed42p)：在效果、速度和成本上表现均衡，是多数场景的**推荐选择**。
    
    > 最新的Qwen3.5-Plus系列在语言理解、逻辑推理、代码生成、智能体任务、图像理解、视频理解、图形用户界面（GUI）等多种任务中表现卓越，支持内置[工具调用](https://help.aliyun.com/zh/model-studio/tool-calls/)，文本能力媲美Qwen3-Max，推荐选用。
    
-   [千问Max](https://help.aliyun.com/zh/model-studio/models#d4ccf72f23jh9) ：千问3系列效果最好的模型，适合处理复杂、多步骤任务。
    
-   [千问Flash](https://help.aliyun.com/zh/model-studio/models#13ff05e329blt) ：千问系列速度最快、成本极低的模型，适用于执行简单任务。
    
-   **千问3.5 开源系列**：`qwen3.5-397b-a17b`、`qwen3.5-122b-a10b`、`qwen3.5-27b`、`qwen3.5-35b-a3b`。
    

### **特定场景模型**

针对明确的业务需求，阿里云百炼提供多种专用优化模型，覆盖[代码能力](https://help.aliyun.com/zh/model-studio/models#d698550551bob)、[长上下文](https://help.aliyun.com/zh/model-studio/models#27b2b3a15d5c6)、[翻译](https://help.aliyun.com/zh/model-studio/models#b51e22f4b036h)、[数据挖掘](https://help.aliyun.com/zh/model-studio/models#531dbf3f1addx)、[法律](https://help.aliyun.com/zh/model-studio/models#f0436273ef1xm)、[意图理解](https://help.aliyun.com/zh/model-studio/models#85209145a5r68)、[角色扮演](https://help.aliyun.com/zh/model-studio/models#083f31bde1lv3)、[深入研究](https://help.aliyun.com/zh/model-studio/models#af665c3673n6e)等领域。

### **多模态模型**

-   [千问Plus](https://help.aliyun.com/zh/model-studio/models#5ef284d4ed42p)（文+图/视频->文）：Qwen3.5-Plus系列同时支持视觉与文本输入，在语言理解、逻辑推理、代码生成、智能体任务、图像理解、视频理解、图形用户界面（GUI）等多种任务中展现出卓越性能，其视觉推理能力相比[千问VL](https://help.aliyun.com/zh/model-studio/models#3f1f1c8913fvo)系列实现飞跃式进步。
    
-   [千问Omni](https://help.aliyun.com/zh/model-studio/models#5e79514e7cqp5)（全模态-> 文+音）：支持视频、音频、图片、文本等多种数据输入，生成文本和语音输出，以应对跨模态复杂任务。
    
-   [语音识别模型](https://help.aliyun.com/zh/model-studio/models#696c1bf328gf9)（音->文）：识别并转写音频中的语音内容，支持中文（含粤语等各种方言）、英文、日语、韩语等。
    

### **第三方模型**

阿里云百炼支持 [DeepSeek](https://help.aliyun.com/zh/model-studio/minimax-llm-api)、[Kimi](https://help.aliyun.com/zh/model-studio/models#2363cbf60fe6m)、[GLM](https://help.aliyun.com/zh/model-studio/models#059d6a5d1chfp)、[MiniMax](https://help.aliyun.com/zh/model-studio/models#7b36766b81de6)等众多知名的第三方大语言模型，完整模型列表请参考[文本生成-第三方模型](https://help.aliyun.com/zh/model-studio/models#774b4cf48dtbp)。

## 核心概念

文本生成模型的输入为提示词（Prompt），它由一个或多个消息（Message）对象构成。每条消息由角色（Role）和内容（Content）组成，具体为：

-   **系统消息（System Message）**：设定模型扮演的角色或遵循的指令。若不指定，默认为"You are a helpful assistant"。
    
-   **用户消息（User Message）**：用户向模型提出的问题或输入的指令。
    
-   **助手消息（Assistant Message）**：模型的回复内容。
    

调用模型时，需构造一个由上述消息对象构成的数组`messages`。一个典型的请求通常由一条定义行为准则的 `system` 消息和一条用户提指令的 `user` 消息组成。

> `system`消息是可选的，但建议使用它来设定模型的角色和行为准则，以获得更稳定、一致的输出。

```
[
    {"role": "system", "content": "你是一个有帮助的助手，需要提供精准、高效且富有洞察力的回应，随时准备协助用户处理各种任务与问题。"},
    {"role": "user", "content": "你是谁？"}
]
```

输出的响应对象中会包含模型回复的`assistant`消息。

```
{
    "role": "assistant",
    "content": "你好！我是Qwen，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字、进行逻辑推理、编程等。我能够理解并生成多种语言，支持多轮对话和复杂任务处理。如果你有任何需要帮助的地方，尽管告诉我！"
}
```

## 快速开始

API 使用前提：已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并完成[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，需要[安装 OpenAI 或 DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk#8833b9274f4v8)。

## OpenAI兼容-Responses API

Responses API 是 Chat Completions API 的演进版本，关于使用说明、代码示例和迁移指南，请参见 [OpenAI兼容-Responses](https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api)。

## Python

```
import os
from openai import OpenAI

try:
    client = OpenAI(
        # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 各地域配置不同，请根据实际地域修改
        base_url="https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1",
    )

    response = client.responses.create(
        model="qwen3.5-plus",
        input="简要介绍下你能做什么？"
    )

    print(response)
except Exception as e:
    print(f"错误信息：{e}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

#### **返回结果**

返回结果主要包含以下字段：

-   `id`：响应 ID。
    
-   `output`：输出列表。包含 `reasoning`（思考过程）和 `message`（回复内容）。
    
    > `reasoning`仅在开启[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)时返回（如 Qwen3.5 系列默认开启）。
    
-   `usage`：Token 用量统计。
    

回复内容示例如下，完整响应请参考[curl](#responses-api-curl-h2)。

```
你好！我是人工智能助手，基于截至 2026 年的知识库训练。以下是我能为你做的主要事情：

1.  **文字创作**：撰写文章、邮件、报告、故事、诗歌等。
2.  **代码辅助**：编写、调试、解释代码，支持多种主流编程语言。
3.  **知识问答**：回答科学、历史、文化、技术等领域的问题。
4.  **逻辑分析**：协助数学解题、数据分析、方案规划与决策支持。
5.  **语言翻译**：支持多种语言之间的准确互译。
6.  **日常对话**：聊天解闷、提供生活建议、角色扮演或学习辅导。

有什么具体任务需要我帮忙吗？随时告诉我！
```

## Node.js

```
// 需要 Node.js v18+，需在 ES Module 环境下运行
import OpenAI from "openai";

const openai = new OpenAI({
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 各地域配置不同，请根据实际地域修改
    baseURL: "https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1"
});

async function main() {
    try {
        const response = await openai.responses.create({
            model: "qwen3.5-plus",
            input: "简要介绍下你能做什么？"
        });

        // 获取模型回复
        console.log(response);
    } catch (error) {
        console.error("错误信息：", error);
    }
}

main();
```

### **返回结果**

返回结果主要包含以下字段：

-   `id`：响应 ID。
    
-   `output`：输出列表。包含 `reasoning`（思考过程）和 `message`（回复内容）。
    
    > `reasoning`仅在开启[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)时返回（如 Qwen3.5 系列默认开启）。
    
-   `usage`：Token 用量统计。
    

回复内容示例如下，完整响应请参考[curl](#responses-api-curl-h2)。

```
你好！我是人工智能助手，基于截至 2026 年的知识库训练。以下是我能为你做的主要事情：

1.  **文字创作**：撰写文章、邮件、报告、故事、诗歌等。
2.  **代码辅助**：编写、调试、解释代码，支持多种主流编程语言。
3.  **知识问答**：回答科学、历史、文化、技术等领域的问题。
4.  **逻辑分析**：协助数学解题、数据分析、方案规划与决策支持。
5.  **语言翻译**：支持多种语言之间的准确互译。
6.  **日常对话**：聊天解闷、提供生活建议、角色扮演或学习辅导。

有什么具体任务需要我帮忙吗？随时告诉我！
```

## curl

```
# 各地域配置不同，请根据实际地域修改
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1/responses \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.5-plus",
    "input": "简要介绍下你能做什么？"
}'
```

#### **返回结果**

```
{
    "created_at": 1772249644,
    "id": "56ec1cc7-f246-448e-bdf9-b13838bc6xxx",
    "model": "qwen3.5-plus",
    "object": "response",
    "output": [
        {
            "id": "msg_082d9e97-2317-4a74-9c07-fc46e4845xxx",
            "summary": [
                {
                    "text": "Thinking Process:\n\n1.  **Analyze the Request:**\n    *   User asks: \"简要介绍下你能做什么？\" (Briefly introduce what you can do?)\n    *   Context: Current date is Saturday, February 28, 2026. Knowledge cutoff is 2026.\n    *   Goal: Provide a concise yet comprehensive overview of my capabilities as an AI assistant.\n\n2.  **Identify Capabilities:**\n    *   Text generation (writing, summarizing, translating).\n    *   Code assistance (writing, debugging, explaining).\n    *   Knowledge retrieval (based on training data up to 2026).\n    *   Reasoning and analysis (logical problems, data analysis).\n    *   Creative tasks (stories, poems, ideas).\n    *   Conversation (chat, role-play, support).\n    *   Limitations (no real-time access unless provided, no physical actions).\n\n3.  **Tailor to Context:**\n    *   Acknowledge the current date (2026) implicitly by ensuring my knowledge cutoff aligns (though I don't need to explicitly state \"I know up to 2026\" unless relevant, but I should sound up-to-date).\n    *   Keep it brief (\"简要\").\n\n4.  **Drafting the Response (Internal Monologue/Trial):**\n    *   *Okay, I need to list my main functions. Don't make it too long. Use bullet points for readability. Be friendly.*\n    *   *Start with a greeting.*\n    *   *Mention text processing, coding, learning, creativity.*\n    *   *Remind about limitations (no real-world actions).*\n    *   *End with an offer to help.*\n\n5.  **Refining the Content (Chinese):**\n    *   你好！我是人工智能助手。\n    *   我能做什么？\n    *   1. 文字处理：写作、翻译、总结。\n    *   2. 代码帮助：写代码、debug。\n    *   3. 知识问答：基于 2026 年前的知识。\n    *   4. 创意生成：故事、方案。\n    *   5. 逻辑分析：解决问题。\n    *   注意：我不能上网（除非有工具），不能做物理事情。\n    *   有什么需要尽管问。\n\n6.  **Polishing for Tone and Conciseness:**\n    *   Make it professional yet approachable.\n    *   Ensure the knowledge cutoff is respected (don't claim to know events after 2026).\n    *   Since the prompt asks for a \"brief introduction\", keep it structured.\n\n7.  **Final Output Construction (similar to the provided good response):**\n    *   Greeting.\n    *   Core capabilities (bullet points).\n    *   Limitations (briefly).\n    *   Closing.\n\n8.  **Self-Correction/Check:**\n    *   Did I mention the date? Not necessary unless asked, but my knowledge base aligns.\n    *   Is it too long? Keep it tight.\n    *   Is it accurate? Yes.\n\n9.  **Final Polish (matching the persona):**\n    你好！我是你的智能助手。基于截至 2026 年的知识库，我可以为你提供以下帮助：\n\n    1.  **内容创作**：撰写文章、邮件、故事、诗歌等。\n    2.  **信息查询与解答**：回答各类知识性问题（基于训练数据）。\n    3.  **代码辅助**：编写、调试、解释代码，支持多种编程语言。\n    4.  **文本处理**：翻译、总结、润色、提取关键信息。\n    5.  **逻辑与分析**：协助分析问题、提供建议、进行推理。\n\n    请注意，我无法访问实时互联网（除非配备特定工具），也不能执行物理操作。有什么具体任务需要我协助吗？\n\n10. **Final Review against constraints:** The user asked for \"brief\". The above is brief. The date context is respected.\n\n    *Wait, one nuance:* As an AI model, I should be careful not to overclaim \"real-time\" capabilities if I don't have tool use enabled in this specific context. Standard safe answer is \"based on training data\".\n\n    *Revised Plan:* Keep it general and helpful.\n\n    *Draft:*\n    你好！我是人工智能助手。我可以协助你完成多种任务，主要包括：\n\n    1.  **文字创作与编辑**：写作、翻译、总结、润色。\n    2.  **编程支持**：代码生成、调试、解释。\n    3.  **知识问答**：基于截至 2026 年的知识解答问题。\n    4.  **逻辑分析**：解决问题、提供建议、数据分析。\n    5.  **创意激发**：头脑风暴、策划方案。\n\n    我无法进行物理操作或访问实时外部信息（除非有特定工具支持）。有什么需要尽管告诉我！\n\n    *Looks good.*\n\n11. **Final Output Generation** (matching the thought process).",
                    "type": "summary_text"
                }
            ],
            "type": "reasoning"
        },
        {
            "content": [
                {
                    "annotations": [],
                    "text": "你好！我是人工智能助手。基于截至 2026 年的知识库，我可以为你提供以下帮助：\n\n1.  **内容创作**：撰写文章、邮件、故事、诗歌及各类文案。\n2.  **代码辅助**：编写、调试、解释代码，支持多种主流编程语言。\n3.  **知识问答**：回答科学、历史、文化等各类知识性问题。\n4.  **文本处理**：翻译、总结长文、提取关键信息、润色修改。\n5.  **逻辑与分析**：协助分析问题、提供建议、进行逻辑推理。\n\n请注意，我无法执行物理操作，且若无特定工具支持，无法访问实时互联网信息。有什么具体任务需要我协助吗？",
                    "type": "output_text"
                }
            ],
            "id": "msg_28643acb-1153-4d4f-84f8-19df29f11xxx",
            "role": "assistant",
            "status": "completed",
            "type": "message"
        }
    ],
    "parallel_tool_calls": false,
    "status": "completed",
    "tool_choice": "auto",
    "tools": [],
    "usage": {
        "input_tokens": 52,
        "input_tokens_details": {
            "cached_tokens": 0
        },
        "output_tokens": 1280,
        "output_tokens_details": {
            "reasoning_tokens": 1122
        },
        "total_tokens": 1332,
        "x_details": [
            {
                "input_tokens": 52,
                "output_tokens": 1280,
                "output_tokens_details": {
                    "reasoning_tokens": 1122
                },
                "total_tokens": 1332,
                "x_billing_type": "response_api"
            }
        ]
    }
}
```

## OpenAI兼容-Chat Completions API

## Python

```
import os
from openai import OpenAI

try:
    client = OpenAI(
        # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 各地域的base_url不同
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
        model="qwen3.5-plus",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "你是谁？"},
        ],
    )
    print(completion.choices[0].message.content)
    # 如需查看完整响应，请取消下列注释
    # print(completion.model_dump_json())
except Exception as e:
    print(f"错误信息：{e}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

#### **返回结果**

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

## Java

```
// 建议 OpenAI Java SDK版本 >= 3.5.0
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

public class Main {
    public static void main(String[] args) {
        try {
            OpenAIClient client = OpenAIOkHttpClient.builder()
                    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为.apiKey("sk-xxx")
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    // 各地域的base_url不同
                    .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                    .build();

            // 创建 ChatCompletion 参数
            ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                    .model("qwen3.5-plus")
                    .addSystemMessage("You are a helpful assistant.")
                    .addUserMessage("你是谁？")
                    .build();

            // 发送请求并获取响应
            ChatCompletion chatCompletion = client.chat().completions().create(params);
            String content = chatCompletion.choices().get(0).message().content().orElse("未返回有效内容");
            System.out.println(content);
            // 如需查看完整响应，请取消下列注释
            // System.out.println(chatCompletion);
            
        } catch (Exception e) {
            System.err.println("错误信息：" + e.getMessage());
            System.out.println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code");
        }
    }
}
```

#### **返回结果**

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

## Node.js

```
// 需要 Node.js v18+，需在 ES Module 环境下运行
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 各地域的base_url不同
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);
const completion = await openai.chat.completions.create({
    model: "qwen3.5-plus",
    messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: "你是谁？" }
    ],
});
console.log(completion.choices[0].message.content);
// 如需查看完整响应，请取消下列注释
// console.log(JSON.stringify(completion, null, 4));
```

#### **返回结果**

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

## Go

```
// OpenAI Go SDK版本不低于 v2.4.0
package main

import (
	"context"
	// 如需查看完整响应，请取消下方及代码末尾的注释
	// "encoding/json"
	"fmt"
	"os"

	"github.com/openai/openai-go/v2"
	"github.com/openai/openai-go/v2/option"
)

func main() {
	// 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
	// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey := "sk-xxx"
	apiKey := os.Getenv("DASHSCOPE_API_KEY")
	client := openai.NewClient(
		option.WithAPIKey(apiKey),
		// 各地域的base_url不同
		option.WithBaseURL("https://dashscope.aliyuncs.com/compatible-mode/v1"),
	)
	chatCompletion, err := client.Chat.Completions.New(
		context.TODO(), openai.ChatCompletionNewParams{
			Messages: []openai.ChatCompletionMessageParamUnion{
				openai.SystemMessage("You are a helpful assistant."),
				openai.UserMessage("你是谁？"),
			},
			Model: "qwen3.5-plus",
		},
	)

	if err != nil {
		fmt.Fprintf(os.Stderr, "请求失败: %v\n", err)
		// 更多错误信息，请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code
		os.Exit(1)
	}

	if len(chatCompletion.Choices) > 0 {
		fmt.Println(chatCompletion.Choices[0].Message.Content)
	}
	// 如需查看完整响应，请取消下列注释
	// jsonData, _ := json.MarshalIndent(chatCompletion, "", "  ")
	// fmt.Println(string(jsonData))

}
```

#### **返回结果**

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

## C#（HTTP）

```
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;

class Program
{
    private static readonly HttpClient httpClient = new HttpClient();

    static async Task Main(string[] args)
    {
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：string? apiKey = "sk-xxx";
        string? apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY");
        // 各地域的base_url不同/chat/completions
        string url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions";
        string jsonContent = @"{
            ""model"": ""qwen3.5-plus"",
            ""messages"": [
                {
                    ""role"": ""system"",
                    ""content"": ""You are a helpful assistant.""
                },
                {
                    ""role"": ""user"",
                    ""content"": ""你是谁？""
                }
            ]
        }";

        string result = await SendPostRequestAsync(url, jsonContent, apiKey);

        // 如需查看完整响应，请取消下列注释
        // Console.WriteLine(result);
        
        // 解析JSON并只输出content部分
        using JsonDocument doc = JsonDocument.Parse(result);
        JsonElement root = doc.RootElement;
        
        if (root.TryGetProperty("choices", out JsonElement choices) && 
            choices.GetArrayLength() > 0)
        {
            JsonElement firstChoice = choices[0];
            if (firstChoice.TryGetProperty("message", out JsonElement message) &&
                message.TryGetProperty("content", out JsonElement content))
            {
                Console.WriteLine(content.GetString());
            }
        }
    }

    private static async Task<string> SendPostRequestAsync(string url, string jsonContent, string apiKey)
    {
        using (var content = new StringContent(jsonContent, Encoding.UTF8, "application/json"))
        {
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", apiKey);
            httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
            HttpResponseMessage response = await httpClient.PostAsync(url, content);
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsStringAsync();
            }
            else
            {   
                // 更多错误信息，请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code
                return $"请求失败: {response.StatusCode}";
            }
        }
    }
}
```

#### **返回结果**

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

## PHP（HTTP）

```
<?php
// 设置请求的URL
// 各地域配置不同，请根据实际地域修改
$url = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions';
// 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：$apiKey = "sk-xxx";
$apiKey = getenv('DASHSCOPE_API_KEY');
// 设置请求头
$headers = [
    'Authorization: Bearer '.$apiKey,
    'Content-Type: application/json'
];
// 设置请求体
$data = [
    "model" => "qwen3.5-plus",
    "messages" => [
        [
            "role" => "system",
            "content" => "You are a helpful assistant."
        ],
        [
            "role" => "user",
            "content" => "你是谁？"
        ]
    ]
];
// 初始化cURL会话
$ch = curl_init();
// 设置cURL选项
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
// 执行cURL会话
$response = curl_exec($ch);
// 检查是否有错误发生
// 更多错误信息，请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code
if (curl_errno($ch)) {
    echo 'Curl error: ' . curl_error($ch);
}
// 关闭cURL资源
curl_close($ch);
// 输出响应结果
$dataObject = json_decode($response);
$content = $dataObject->choices[0]->message->content;
echo $content;
// 如需查看完整响应，请取消下列注释
//echo $response;
?>
```

#### **返回结果**

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

## curl

各地域的base\_url和API Key不同，详情请参见[OpenAI Chat](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions)和 [获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

```
# 各地域配置不同，请根据实际地域修改
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.5-plus",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user", 
            "content": "你是谁？"
        }
    ]
}'
```

#### **返回结果**

```
{
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
        }
    ],
    "object": "chat.completion",
    "usage": {
        "prompt_tokens": 26,
        "completion_tokens": 66,
        "total_tokens": 92
    },
    "created": 1726127645,
    "system_fingerprint": null,
    "model": "qwen3.5-plus",
    "id": "chatcmpl-81951b98-28b8-9659-ab07-xxxxxx"
}
```

## DashScope

**重要**

Qwen3.5系列的DashScope API采用多模态接口，以下示例会报错`url error`，调用方式请参见[图像、视频数据处理](#270b260cb6or2)。

## Python

```
import json
import os
from dashscope import Generation
import dashscope

# 各地域配置不同，请根据实际地域修改
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你是谁？"},
]
response = Generation.call(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # Qwen3.5系列需要使用多模态接口，直接替换模型会导致报错
    model="qwen-plus",
    messages=messages,
    result_format="message",
)

if response.status_code == 200:
    print(response.output.choices[0].message.content)
    # 如需查看完整响应，请取消下列注释
    # print(json.dumps(response, default=lambda o: o.__dict__, indent=4))
else:
    print(f"HTTP返回码：{response.status_code}")
    print(f"错误码：{response.code}")
    print(f"错误信息：{response.message}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

#### **返回结果**

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

## Java

```
import java.util.Arrays;
import java.lang.System;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.protocol.Protocol;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        // 各地域的base_url不同
        Generation gen = new Generation(Protocol.HTTP.getValue(), "https://dashscope.aliyuncs.com/api/v1");
        Message systemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .content("You are a helpful assistant.")
                .build();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("你是谁？")
                .build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // Qwen3.5系列需要使用多模态接口，直接替换模型会导致报错
                .model("qwen-plus")
                .messages(Arrays.asList(systemMsg, userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .build();
        return gen.call(param);
    }
    public static void main(String[] args) {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
            // 如需查看完整响应，请取消下列注释
            // System.out.println(JsonUtils.toJson(result));
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("错误信息："+e.getMessage());
            System.out.println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code");
        }
    }
}
```

#### **返回结果**

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

## Node.js（HTTP）

```
// 需要 Node.js v18+
// 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：const apiKey = "sk-xxx";
const apiKey = process.env.DASHSCOPE_API_KEY;

const data = {
    // Qwen3.5系列需要使用多模态接口，直接替换模型会导致报错
    model: "qwen-plus",
    input: {
        messages: [
            {
                role: "system",
                content: "You are a helpful assistant."
            },
            {
                role: "user",
                content: "你是谁？"
            }
        ]
    },
    parameters: {
        result_format: "message"
    }
};

async function callApi() {
    try {
        // 各地域配置不同，请根据实际地域修改
        const response = await fetch('https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log(result.output.choices[0].message.content);
        // 如需查看完整响应，请取消下列注释
        // console.log(JSON.stringify(result));
    } catch (error) {
        // 更多错误信息，请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code
        console.error('调用失败:', error.message);
    }
}

callApi();
```

#### **返回结果**

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

## Go（HTTP）

```
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

func main() {
	requestBody := map[string]interface{}{
		// Qwen3.5系列需要使用多模态接口，直接替换模型会导致报错
		"model": "qwen-plus",
		"input": map[string]interface{}{
			"messages": []map[string]string{
				{
					"role":    "system",
					"content": "You are a helpful assistant.",
				},
				{
					"role":    "user",
					"content": "你是谁？",
				},
			},
		},
		"parameters": map[string]string{
			"result_format": "message",
		},
	}

	// 序列化为 JSON
	jsonData, _ := json.Marshal(requestBody)

	// 创建 HTTP 客户端和请求
	client := &http.Client{}
	// 各地域配置不同，请根据实际地域修改
	req, _ := http.NewRequest("POST", "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation", bytes.NewBuffer(jsonData))

	// 设置请求头
	apiKey := os.Getenv("DASHSCOPE_API_KEY")
	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")

	// 发送请求
	resp, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	// 读取响应体
	bodyText, _ := io.ReadAll(resp.Body)
	
	// 解析JSON并输出content内容
	var result map[string]interface{}
	json.Unmarshal(bodyText, &result)
	content := result["output"].(map[string]interface{})["choices"].([]interface{})[0].(map[string]interface{})["message"].(map[string]interface{})["content"].(string)
	fmt.Println(content)

	// 如需查看完整响应，请取消下列注释
	// fmt.Printf("%s\n", bodyText)
}
```

#### **返回结果**

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

## C#（HTTP）

```
using System.Net.Http.Headers;
using System.Text;

class Program
{
    private static readonly HttpClient httpClient = new HttpClient();

    static async Task Main(string[] args)
    {
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：string? apiKey = "sk-xxx";
        string? apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY");
        // 设置请求 URL 和内容
        // 各地域配置不同，请根据实际地域修改
        string url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation";
        // Qwen3.5系列需要使用多模态接口，直接替换模型会导致报错
        string jsonContent = @"{
            ""model"": ""qwen-plus"",
            ""input"": {
                ""messages"": [
                    {
                        ""role"": ""system"",
                        ""content"": ""You are a helpful assistant.""
                    },
                    {
                        ""role"": ""user"",
                        ""content"": ""你是谁？""
                    }
                ]
            },
            ""parameters"": {
                ""result_format"": ""message""
            }
        }";

        // 发送请求并获取响应
        string result = await SendPostRequestAsync(url, jsonContent, apiKey);
        var jsonResult = System.Text.Json.JsonDocument.Parse(result);
        var content = jsonResult.RootElement.GetProperty("output").GetProperty("choices")[0].GetProperty("message").GetProperty("content").GetString();
        Console.WriteLine(content);
        // 如需查看完整响应，请取消下列注释
        // Console.WriteLine(result);
    }

    private static async Task<string> SendPostRequestAsync(string url, string jsonContent, string apiKey)
    {
        using (var content = new StringContent(jsonContent, Encoding.UTF8, "application/json"))
        {
            // 设置请求头
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", apiKey);
            httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

            // 发送请求并获取响应
            HttpResponseMessage response = await httpClient.PostAsync(url, content);

            // 处理响应
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsStringAsync();
            }
            else
            {
                return $"请求失败: {response.StatusCode}";
            }
        }
    }
}
```

#### **返回结果**

```
{
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": "我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！"
                }
            }
        ]
    },
    "usage": {
        "total_tokens": 92,
        "output_tokens": 66,
        "input_tokens": 26
    },
    "request_id": "09dceb20-ae2e-999b-85f9-xxxxxx"
}
```

## PHP（HTTP）

```
<?php
// 各地域配置不同，请根据实际地域修改
$url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation";
// 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：$apiKey = "sk-xxx";
$apiKey = getenv('DASHSCOPE_API_KEY');

$data = [
    // Qwen3.5系列需要使用多模态接口，直接替换模型会导致报错
    "model" => "qwen-plus",
    "input" => [
        "messages" => [
            [
                "role" => "system",
                "content" => "You are a helpful assistant."
            ],
            [
                "role" => "user",
                "content" => "你是谁？"
            ]
        ]
    ],
    "parameters" => [
        "result_format" => "message"
    ]
];

$jsonData = json_encode($data);

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonData);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Authorization: Bearer $apiKey",
    "Content-Type: application/json"
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

if ($httpCode == 200) {
    $jsonResult = json_decode($response, true);
    $content = $jsonResult['output']['choices'][0]['message']['content'];
    echo $content;
    // 如需查看完整响应，请取消下列注释
    // echo "模型响应: " . $response;
} else {
    echo "请求错误: " . $httpCode . " - " . $response;
}

curl_close($ch);
?>
```

#### **返回结果**

```
我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

## curl

各地域的base\_url和API Key不同，详情请参见[DashScope](https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope)和 [获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

```
# 各地域配置不同，请根据实际地域修改
curl --location "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "Content-Type: application/json" \
--data '{
    "model": "qwen-plus",
    "input":{
        "messages":[      
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    },
    "parameters": {
        "result_format": "message"
    }
}'
```

#### **返回结果**

```
{
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": "我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！"
                }
            }
        ]
    },
    "usage": {
        "total_tokens": 92,
        "output_tokens": 66,
        "input_tokens": 26
    },
    "request_id": "09dceb20-ae2e-999b-85f9-xxxxxx"
}
```

## **图像、视频数据处理**

多模态模型支持处理图像、视频等非文本数据，可用于视觉问答、事件检测等任务。其调用方式与纯文本模型主要有以下不同：

-   **用户消息（user message）的构造方式**：多模态模型的用户消息不仅包含文本，还包含图片、音频等多模态信息。
    
-   **DashScope SDK接口：**使用 DashScope Python SDK 时，需调用 `MultiModalConversation` 接口；使用DashScope Java SDK 时，需调用 `MultiModalConversation` 类。
    

> 图片、视频文件限制请参见[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision#430cb5ea4cety)。

## OpenAI兼容-Chat Completions API

## Python

```
from openai import OpenAI
import os

client = OpenAI(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 各地域配置不同，请根据实际地域修改
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
messages = [
    {
        "role": "user",
        "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"
                    },
                },
            {"type": "text", "text": "请问图片展现了有哪些商品？"},
        ],
    }
]
completion = client.chat.completions.create(
    model="qwen3.5-plus",
    messages=messages,
)
print(completion.choices[0].message.content)
```

## Node.js

```
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 各地域的base_url不同
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

let messages = [
    {
        role: "user",
        content: [
            { type: "image_url", image_url: { "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png" } },
            { type: "text", text: "请问图片展现了有哪些商品？" },
        ]
    }]
async function main() {
    let response = await openai.chat.completions.create({
        model: "qwen3.5-plus",
        messages: messages
    });
    console.log(response.choices[0].message.content);
}

main()
```

## curl

各地域的base\_url和API Key不同，详情请参见[OpenAI Chat](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions)和 [获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

```
# 各地域配置不同，请根据实际地域修改
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen3.5-plus",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"
          }
        },
        {
          "type": "text",
          "text": "请问图片展现了有哪些商品？"
        }
      ]
    }
  ]
}'
```

## DashScope

## Python

```
import os
import dashscope
from dashscope import MultiModalConversation

# 各地域配置不同，请根据实际地域修改
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {
                "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"
            },
            {"text": "请问图片展现了有哪些商品？"},
        ],
    }
]
response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3.5-plus',   # 可按需更换为其它多模态模型，并修改相应的 messages
    messages=messages)
print(response.output.choices[0].message.content[0]['text'])
```

## Java

```
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 各地域配置不同，请根据实际地域修改
    // static {Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";}

    private static final String modelName = "qwen3.5-plus";  // 可按需更换为其它多模态模型，并修改相应的 messages

    public static void MultiRoundConversationCall() throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"),
                        Collections.singletonMap("text", "请问图片展现了有哪些商品？"))).build();
        List<MultiModalMessage> messages = new ArrayList<>();
        messages.add(userMessage);
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model(modelName)
                .messages(messages)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));        // add the result to conversation
    }

    public static void main(String[] args) {
        try {
            MultiRoundConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## curl

各地域的base\_url和API Key不同，详情请参见[DashScope](https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope)和 [获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

```
# 各地域配置不同，请根据实际地域修改
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3.5-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"},
                    {"text": "请问图片展现了有哪些商品？"}
                ]
            }
        ]
    }
}'
```

## **异步调用模型**

调用异步接口，可有效提升高并发请求的处理效率。

## OpenAI兼容-Chat Completions API

## Python

```
import os
import asyncio
from openai import AsyncOpenAI
import platform

# 创建异步客户端实例
client = AsyncOpenAI(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 各地域配置不同，请根据实际地域修改
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 定义异步任务列表
async def task(question):
    print(f"发送问题: {question}")
    response = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant." },
            {"role": "user", "content": question}
        ],
        model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    )
    print(f"模型回复: {response.choices[0].message.content}")

# 主异步函数
async def main():
    questions = ["你是谁？", "你会什么？", "天气怎么样？"]
    tasks = [task(q) for q in questions]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    # 设置事件循环策略
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # 运行主协程
    asyncio.run(main(), debug=False)
    
```

## Java

```
import com.openai.client.OpenAIClientAsync;
import com.openai.client.okhttp.OpenAIOkHttpClientAsync;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

import java.util.Arrays;
import java.util.List;
import java.util.concurrent.CompletableFuture;

public class Main {
    public static void main(String[] args) {
        // 创建 OpenAI 客户端，连接 DashScope 的兼容接口
        OpenAIClientAsync client = OpenAIOkHttpClientAsync.builder()
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 各地域的base_url不同
                .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                .build();

        // 定义问题列表
        List<String> questions = Arrays.asList("你是谁？", "你会什么？", "天气怎么样？");

        // 创建异步任务列表
        CompletableFuture<?>[] futures = questions.stream()
                .map(question -> CompletableFuture.supplyAsync(() -> {
                    System.out.println("发送问题: " + question);
                    // 创建 ChatCompletion 参数
                    ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                            .model("qwen-plus")  // 指定模型
                            .addSystemMessage("You are a helpful assistant.")
                            .addUserMessage(question)
                            .build();

                    // 发送异步请求并处理响应
                    return client.chat().completions().create(params)
                        .thenAccept(chatCompletion -> {
                            String content = chatCompletion.choices().get(0).message().content().orElse("无响应内容");
                            System.out.println("模型回复: " + content);
                        })
                        .exceptionally(e -> {
                            System.err.println("错误信息：" + e.getMessage());
                            System.out.println("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code");
                            return null;
                        });
                }).thenCompose(future -> future))
                .toArray(CompletableFuture[]::new);

        // 等待所有异步操作完成
        CompletableFuture.allOf(futures).join();
    }
}
```

## DashScope

DashScope SDK的文本生成异步调用，目前仅支持Python。

```
# DashScope Python SDK版本需要不低于 1.19.0
import asyncio
import platform
from dashscope.aigc.generation import AioGeneration
import os
import dashscope 

# 各地域配置不同，请根据实际地域修改
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

# 定义异步任务列表
async def task(question):
    print(f"发送问题: {question}")
    response = await AioGeneration.call(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": question}],
        result_format="message",
    )
    print(f"模型回复: {response.output.choices[0].message.content}")

# 主异步函数
async def main():
    questions = ["你是谁？", "你会什么？", "天气怎么样？"]
    tasks = [task(q) for q in questions]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    # 设置事件循环策略
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # 运行主协程
    asyncio.run(main(), debug=False)
```

**返回结果**

> 由于调用是异步的，响应的返回顺序可能与示例不同。

```
发送问题: 你是谁？
发送问题: 你会什么？
发送问题: 天气怎么样？
模型回复: 你好！我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。如果你有任何问题或需要帮助，欢迎随时告诉我！
模型回复: 您好！我目前无法实时获取天气信息。您可以告诉我您所在的城市或地区，我会尽力为您提供一些通用的天气建议或信息。或者您也可以使用天气应用查看实时天气情况。
模型回复: 我会很多技能，比如：

1. **回答问题**：无论是学术问题、生活常识还是专业知识，我都可以尝试帮你解答。
2. **创作文字**：我可以写故事、公文、邮件、剧本等各类文本。
3. **逻辑推理**：我可以帮助你解决一些逻辑推理问题，比如数学题、谜语等。
4. **编程**：我可以提供编程帮助，包括代码编写、调试和优化。
5. **多语言支持**：我支持多种语言，包括但不限于中文、英文、法语、西班牙语等。
6. **观点表达**：我可以为你提供一些观点和建议，帮助你做出决策。
7. **玩游戏**：我们可以一起玩文字游戏，比如猜谜语、成语接龙等。

如果你有任何具体的需求或问题，欢迎告诉我，我会尽力帮助你！
```

## 应用于生产环境

### **构建高质量的上下文**

向大模型直接输入大量原始数据，会因上下文容量的限制导致成本增加与效果下降。上下文工程（Context Engineering）通过动态加载精准知识，显著提升生成质量与效率。核心技术包括：

-   **提示词工程（Prompt Engineering）**：通过设计和优化文本指令（Prompt），可以更精确地引导模型，使其输出更符合预期的结果。若想了解更多，可参考[文生文Prompt指南](https://help.aliyun.com/zh/model-studio/prompt-engineering-guide)、阿里云百炼 [提示词模板](https://bailian.console.aliyun.com/?tab=app#/plugin-market/prompt)页面。
    
-   [检索增强生成（RAG）](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)：适用于需要模型依据外部知识库（例如产品文档或技术手册）来回答问题的场景。
    
-   [工具调用（Tool）](https://help.aliyun.com/zh/model-studio/tool-calls/)：允许模型获取实时信息（如查询天气、路况）或完成特定操作（如调用API、发送邮件）。
    
-   **记忆机制（Memory）**：为模型建立长短期记忆，使其能够理解连续对话的历史信息。
    

若想系统了解，可参考[阿里云大模型高级工程师ACP认证课程](https://atomgit.com/alibabaclouddocs/aliyun_acp_learning/blob/main/%E5%A4%A7%E6%A8%A1%E5%9E%8BACP%E8%AE%A4%E8%AF%81%E6%95%99%E7%A8%8B/p2_%E6%9E%84%E9%80%A0%E5%A4%A7%E6%A8%A1%E5%9E%8B%E9%97%AE%E7%AD%94%E7%B3%BB%E7%BB%9F/2_1_%E7%94%A8%E5%A4%A7%E6%A8%A1%E5%9E%8B%E6%9E%84%E5%BB%BA%E6%96%B0%E4%BA%BA%E7%AD%94%E7%96%91%E6%9C%BA%E5%99%A8%E4%BA%BA.ipynb)。

### **控制回复多样性**

`temperature` 和 `top_p`用于控制生成文本的多样性。数值越高，内容越多样，数值越低，内容越确定。为准确评估参数效果，建议每次只调整一个。

-   `**temperature**`：范围 \[0, 2)。侧重调整随机性。
    
-   `**top_p**`：范围 \[0, 1\]。通过概率阈值筛选回复。
    

以下示例将展示不同参数设置对生成内容的影响。输入提示词为：“写一个三句话的短故事，主角是一只猫和一束阳光。”

-   **高多样性**（示例`temperature`\=0.9）：适用于需要创意、想象力和新颖表达的场景，如创意写作、头脑风暴或市场营销文案。
    
    ```
    阳光斜斜地切进窗台，橘猫蹑手蹑脚走近那块发光的方砖，绒毛瞬间被染成熔化的蜜糖。  
    它伸出前爪轻拍光斑，却像踩进温热的池水般陷了进去，整片阳光顺着肉垫汩汩漫上脊背。  
    午后忽然变得很重——猫儿蜷在流动的金砂里，听见时光在呼噜声中轻轻融化。
    ```
    
-   **高确定性**（示例`temperature`\=0.1）：适用于要求内容准确、严谨和可预测的场景，如事实问答、代码生成或法律文本。
    
    ```
    午后，一只老猫蜷在窗台，数着光斑打盹。  
    阳光轻轻跃过它斑驳的脊背，像在翻阅一本旧相册。  
    尘埃浮起又落下，仿佛时光低语：你曾年轻，我也炽热。
    ```
    

**原理介绍**

**temperature**：

-   temperature 越高，Token 概率分布变得更平坦（即高概率 Token 的概率降低，低概率 Token 的概率上升），使得模型在选择下一个 Token 时更加随机。
    
-   temperature 越低，Token 概率分布变得更陡峭（即高概率 Token 被选取的概率更高，低概率 Token 的概率更低），使得模型更倾向于选择高概率的少数 Token。
    

**top\_p**：

top\_p 采样是指从最高概率（最核心）的 Token 集合中进行采样。它将所有可能的下一个 Token 按概率从高到低排序，然后从概率最高的 Token 开始累加概率，直至概率总和达到阈值（例如80%，即 top\_p=0.8），最后从这些概率最高、概率总和达到阈值的 Token 中随机选择一个用于输出。

-   top\_p 越高，考虑的 Token 越多，因此生成的文本更多样。
    
-   top\_p 越低，考虑的 Token 越少，因此生成的文本更集中和确定。
    

**不同场景的参数配置示例**

```
# 不同场景的推荐参数配置
SCENARIO_CONFIGS = {
    # 创造性写作
    "creative_writing": {
        "temperature": 0.9,
        "top_p": 0.95
    },
    # 代码生成
    "code_generation": {
        "temperature": 0.2,
        "top_p": 0.8
    },
    # 事实性问答
    "factual_qa": {
        "temperature": 0.1,
        "top_p": 0.7
    },
    # 翻译
    "translation": {
        "temperature": 0.3,
        "top_p": 0.8
    }
}

# OpenAI使用示例
# completion = client.chat.completions.create(
#     model="qwen-plus",
#     messages=[{"role": "user", "content": "写一首关于月亮的诗"}],
#     **SCENARIO_CONFIGS["creative_writing"]
# )
# DashScope使用示例
# response = Generation.call(
#     # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
#     api_key=os.getenv("DASHSCOPE_API_KEY"),
#     model="qwen-plus",
#     messages=[{"role": "user", "content": "写一个判断输入n是否是质数的python函数，不要输出非代码内容"}],
#     result_format="message",
#     **SCENARIO_CONFIGS["code_generation"]
# )
```

### **更多功能**

上文介绍了基础的交互方式。针对更复杂的场景，可参考：

-   [多轮对话](https://help.aliyun.com/zh/model-studio/multi-round-conversation)：适用于追问、信息采集等需要连续交流的场景。
    
-   [流式输出](https://help.aliyun.com/zh/model-studio/stream)：适用于聊天机器人、实时代码生成等需要即时响应的场景，可以提升用户体验，并避免因响应时间过长导致的超时。
    
-   [深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)：适用于复杂推理、策略分析等需要更高质量、更具条理的深度回答的场景。
    
-   [结构化输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output)：当需要模型按稳定的 JSON 格式回复，以便于程序调用或数据解析时使用。
    
-   [前缀续写](https://help.aliyun.com/zh/model-studio/partial-mode)：适用于代码补全、长文写作等需要模型接续已有文本的场景。
    

## API 参考

模型调用的完整参数列表，请参考 [OpenAI 兼容 API 参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/#d397bcc41eu3q)和[DashScope API 参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/#69cac67a477k2)。

## **常见问题**

### **Q：千问 API 为何无法分析网页链接？**

A：千问 API 本身不具备直接访问和解析网页链接的能力，可以通过[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)、[MCP](https://help.aliyun.com/zh/model-studio/mcp)等功能，或结合 Python 的 Beautiful Soup 等网页抓取工具读取网页信息。

### **Q：**[**网页端千问**](https://tongyi.aliyun.com/qianwen/)**和千问 API 的回复为什么不一致？**

A：网页端千问在千问 API 的基础上做了额外的工程优化**，**因此可以达到解析网页、联网搜索、画图、制作 PPT等功能，这些本身并不属于大模型 API 的能力，可以通过[联网搜索](https://help.aliyun.com/zh/model-studio/web-search)、[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)、[MCP](https://help.aliyun.com/zh/model-studio/mcp)等功能优化模型的效果。

### Q：如何处理**模型超时的情况？**

A：使用[流式输出](https://help.aliyun.com/zh/model-studio/stream)可避免超时。

非流式调用若超过 300 秒未完成，服务将中断请求，但返回已生成的内容，且不再报超时错误。此时响应头将包含`x-dashscope-partialresponse: true`，表示返回的是超时前的部分结果。

支持该机制的模型如下：

支持的模型

-   qwen-max-2024-09-19 及之后的模型
    
-   qwen-plus-2024-11-25 及之后的模型
    
-   qwen-flash-2025-07-28 及之后的模型
    
-   qwen-turbo-2024-11-01 及之后的模型
    
-   qwen-vl-max-2025-01-25 及之后的模型
    
-   qwen-vl-plus-2025-01-02 及之后的模型
    
-   qwen-long-2025-01-25 及之后的模型
    
-   qwen3 开源模型（qwen3-235b-a22b、qwen3-32b、qwen3-30b-a3b、qwen3-14b、qwen3-8b、qwen3-4b、qwen3-1.7b、qwen3-0.6b）
    
-   qwen3.5 开源模型（`qwen3.5-122b-a10b`、`qwen3.5-27b`、`qwen3.5-35b-a3b`、`qwen3.5-397b-a17b`）
    
-   qwen2.5开源模型（qwen2.5-14b-instruct-1m、qwen2.5-7b-instruct-1m、qwen2.5-72b-instruct、qwen2.5-32b-instruct、qwen2.5-14b-instruct、qwen2.5-7b-instruct、qwen2.5-3b-instruct、qwen2.5-1.5b-instruct、qwen2.5-0.5b-instruct）
    

> 若无法获取响应头参数（例如通过 SDK 调用），可通过 `finish_reason`字段辅助判断，若为`null`，表示生成内容不完整（但不一定是触发了超时）。

大模型可续写不完整的内容，详情请参见：[基于不完整输出进行续写](https://help.aliyun.com/zh/model-studio/partial-mode#8cc28acfd7a91)。

> Java SDK 暂不支持前缀续写功能。

### **Q：模型能直接生成 Word、Excel、PDF 或 PPT 格式的文件吗？**

A：不能。阿里云百炼的文本生成模型仅输出纯文本内容。您需要通过代码或使用第三方库将文本转换为所需格式，或通过阿里云百炼[PPT自动生成应用](https://bailian.console.aliyun.com/?tab=app#/app-market/app-template-experience/assistant/AutoPptGenerator)、[网页端千问](https://www.qianwen.com/aippt)等方式进行生成。
视觉理解模型可以根据您传入的图片或视频进行回答，支持单图或多图的输入，适用于图像描述、视觉问答、物体定位等多种任务。

**支持的地域：**华北2（北京）、新加坡和美国（弗吉尼亚），需使用各地域的 [API Key](https://help.aliyun.com/zh/model-studio/get-api-key)和请求地址。

**在线体验：**访问[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing?spm=5176.29619931.J__Z58Z6CX7MY__Ll8p1ZOR.1.7dd7521cmX1pAh&tab=model#/model-market)，在页面右上角选择目标地域，进入[视觉模型](https://bailian.console.aliyun.com/#/efm/model_experience_center/vision)页面进行体验。

## **快速开始**

**前提条件**

-   已[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    
-   如果通过 SDK 进行调用，需安装[SDK](https://help.aliyun.com/zh/model-studio/install-sdk)，其中 DashScope Python SDK 版本不低于1.24.6，DashScope Java SDK 版本不低于 2.21.10。
    

以下示例演示了如何调用模型描述图像内容。关于本地文件和图像限制的说明，请参见[如何传入本地文件](#d987f8de5395x)、[图像限制](#71c2cb6e09ioo)章节。

## OpenAI兼容

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 各地域配置不同，请根据实际地域修改
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.5-plus", # 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                    },
                },
                {"type": "text", "text": "图中描绘的是什么景象?"},
            ],
        },
    ],
)
print(completion.choices[0].message.content)
```

### **返回结果**

```
这是一张在海滩上拍摄的照片。照片中，一个人和一只狗坐在沙滩上，背景是大海和天空。人和狗似乎在互动，狗的前爪搭在人的手上。阳光从画面的右侧照射过来，给整个场景增添了一种温暖的氛围。
```

## Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
   // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
  apiKey: process.env.DASHSCOPE_API_KEY,
  // 各地域配置不同，请根据实际地域修改
  baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

async function main() {
  const response = await openai.chat.completions.create({
    model: "qwen3.5-plus",  // 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages: [
      {
        role: "user",
        content: [{
            type: "image_url",
            image_url: {
              "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
            }
          },
          {
            type: "text",
            text: "图中描绘的是什么景象?"
          }
        ]
      }
    ]
  });
  console.log(response.choices[0].message.content);
}
main()
```

### **返回结果**

```
这是一张在海滩上拍摄的照片。照片中，一个人和一只狗坐在沙滩上，背景是大海和天空。人和狗似乎在互动，狗的前爪搭在人的手上。阳光从画面的右侧照射过来，给整个场景增添了一种温暖的氛围。
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改
# === 执行时请删除该注释 ===

curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "qwen3.5-plus",
  "messages": [
  {
    "role": "user",
    "content": [
      {"type": "image_url", "image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"}},
      {"type": "text", "text": "图中描绘的是什么景象?"}
    ]
  }]
}'
```

### **返回结果**

```
{
  "choices": [
    {
      "message": {
        "content": "这是一张在海滩上拍摄的照片。照片中，一个人和一只狗坐在沙滩上，背景是大海和天空。人和狗似乎在互动，狗的前爪搭在人的手上。阳光从画面的右侧照射过来，给整个场景增添了一种温暖的氛围。",
        "role": "assistant"
      },
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null
    }
  ],
  "object": "chat.completion",
  "usage": {
    "prompt_tokens": 1270,
    "completion_tokens": 54,
    "total_tokens": 1324
  },
  "created": 1725948561,
  "system_fingerprint": null,
  "model": "qwen3.5-plus",
  "id": "chatcmpl-0fd66f46-b09e-9164-a84f-3ebbbedbac15"
}
```

## DashScope

## Python

```
import os
import dashscope

# 各地域配置不同，请根据实际地域修改
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

messages = [
{
    "role": "user",
    "content": [
    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
    {"text": "图中描绘的是什么景象?"}]
}]
response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量， 请用百炼API Key将下行替换为： api_key ="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key = os.getenv('DASHSCOPE_API_KEY'),
    model = 'qwen3.5-plus',  # 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages = messages
)
print(response.output.choices[0].message.content[0]["text"])
```

### **返回结果**

```
是一张在海滩上拍摄的照片。照片中有一位女士和一只狗。女士坐在沙滩上，微笑着与狗互动。狗戴着项圈，似乎在与女士握手。背景是大海和天空，阳光洒在她们身上，营造出温馨的氛围。
```

## Java

```
import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 各地域配置不同，请根据实际地域修改
    static {Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";}
        
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"),
                        Collections.singletonMap("text", "图中描绘的是什么景象?"))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                 // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                 // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.5-plus")  // 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
                .messages(Arrays.asList(userMessage))
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }
    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

### **返回结果**

```
这是一张在海滩上拍摄的照片。照片中有一个穿着格子衬衫的人和一只戴着项圈的狗。人和狗面对面坐着，似乎在互动。背景是大海和天空，阳光洒在他们身上，营造出温暖的氛围。
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3.5-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
                    {"text": "图中描绘的是什么景象?"}
                ]
            }
        ]
    }
}'
```

### **返回结果**

```
{
  "output": {
    "choices": [
      {
        "finish_reason": "stop",
        "message": {
          "role": "assistant",
          "content": [
            {
              "text": "这是一张在海滩上拍摄的照片。照片中有一个穿着格子衬衫的人和一只戴着项圈的狗。他们坐在沙滩上，背景是大海和天空。阳光从画面的右侧照射过来，给整个场景增添了一种温暖的氛围。"
            }
          ]
        }
      }
    ]
  },
  "usage": {
    "output_tokens": 55,
    "input_tokens": 1271,
    "image_tokens": 1247
  },
  "request_id": "ccf845a3-dc33-9cda-b581-20fe7dc23f70"
}
```

## **模型选型**

-   **首选 Qwen3.5**：最新一代视觉理解模型，在多模态推理、2D/3D图像理解、复杂文档解析、视觉编程、视频理解、多模态智能体等任务上领先，支持中国内地和新加坡地域。
    
    -   `qwen3.5-plus`：千问性能最强的视觉理解模型，推荐优先使用。
        
    -   `qwen3.5-flash`：速度更快，成本更低，是兼顾性能与成本的高性价比选择，适用于对响应速度敏感的场景。
        
    -   `qwen3.5-397b-a17b`、`qwen3.5-122b-a10b`、`qwen3.5-27b`、`qwen3.5-35b-a3b`：Qwen3.5 开源系列模型。
        
-   Qwen3-VL 也适用于高精度的物体识别与定位（包括 3D 定位）、 Agent 工具调用、文档和网页解析、复杂题目解答、长视频理解等任务。系列内模型对比如下：
    
    -   `qwen3-vl-plus`：Qwen3-VL 系列中性能最强的模型。
        
    -   `qwen3-vl-flash`：速度更快，成本更低，是兼顾性能与成本的高性价比选择，适用于对响应速度敏感的场景。
        
-   Qwen2.5-VL 适用于简单的图像描述、短视频摘要提取等通用任务，系列内模型对比如下：
    
    -   `qwen-vl-max`（属于Qwen2.5-VL）：Qwen2.5-VL 系列中效果最佳的模型。
        
    -   `qwen-vl-plus`（属于Qwen2.5-VL）：速度更快，在效果与成本之间实现良好平衡。
        

模型的名称、上下文、价格、快照版本等信息请参见[模型列表](https://help.aliyun.com/zh/model-studio/models)；并发限流条件请参考[限流](https://help.aliyun.com/zh/model-studio/rate-limit)。

**模型特性对比**

| **模型** | [**深度思考**](https://help.aliyun.com/zh/model-studio/visual-reasoning) | [**工具调用**](https://help.aliyun.com/zh/model-studio/qwen-function-calling) | [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache) | [结构化输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output) | **识别的语言种类** |
| --- | --- | --- | --- | --- | --- |
| `Qwen3.5`系列 | 支持  | 支持  | `qwen3.5-plus`、`qwen3.5-flash`的稳定版支持 > 仅支持显式缓存 | 非思考模式支持 | 33种；分别为中文、日语、韩语、印尼语、越南语、泰语、英语、法语、德语、俄语、葡萄牙语、西班牙语、意大利语、瑞典语、丹麦语、捷克语、挪威语、荷兰语、芬兰语、土耳其语、波兰语、斯瓦希里语、罗马尼亚语、塞尔维亚语、希腊语、哈萨克语、乌兹别克语、宿务语、阿拉伯语、乌尔都语、波斯语、印地语 / 天城语、希伯来语。 |
| `Qwen3-VL`系列 | 支持  | 支持  | `qwen3-vl-plus`和`qwen3-vl-flash`的稳定版支持 | 非思考模式支持 | 33种；分别为中文、日语、韩语、印尼语、越南语、泰语、英语、法语、德语、俄语、葡萄牙语、西班牙语、意大利语、瑞典语、丹麦语、捷克语、挪威语、荷兰语、芬兰语、土耳其语、波兰语、斯瓦希里语、罗马尼亚语、塞尔维亚语、希腊语、哈萨克语、乌兹别克语、宿务语、阿拉伯语、乌尔都语、波斯语、印地语 / 天城语、希伯来语。 |
| `Qwen2.5-VL`系列 | 不支持 | 不支持 | `qwen-vl-max`和`qwen-vl-plus`的稳定版支持 | `qwen-vl-max`和`qwen-vl-plus`的稳定版和最新版支持 | 11种；分别为中文、英语、日语、韩语、阿拉伯语、越南语、法语、德语、意大利语、西班牙语和俄语。 |

## **模型效果**

### **图像问答**

描述图像中的内容或者对其进行分类打标，如识别人物、地点、动植物等。

| ![p1021359](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7372672671/p1025117.webp) 如果太阳很刺眼，我应该用这张图中的什么物品？ | 当太阳很刺眼时，你应该使用图中的粉色太阳镜。太阳镜可以有效阻挡强光、减少紫外线对眼睛的伤害，帮助你在阳光强烈时保护视力并提升视觉舒适度。 |
| --- | --- |

### **创意写作**

根据图片或视频内容生成生动的文字描述，适用于故事创作、文案撰写、短视频脚本等创意场景。

| ![vl-问答](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7372672671/p1025118.webp) 请根据图片内容，帮我写一段有意思的朋友圈文案。 | 好的，这张图片充满了浓郁的中秋节日氛围，古典与现代元素结合得非常巧妙。根据图片中的主要元素，我为你准备了几个不同风格的朋友圈文案，你可以根据自己的喜好选择。 **诗意唯美风** 今夜月明人尽望，不知秋思落谁家。嫦娥奔月，玉兔捣药，古人的浪漫在今夜被点亮。愿这轮明月，能照亮你回家的路，也能寄去我最深的思念。中秋节快乐！ **温馨祝福风** 月圆人团圆，中秋夜最温柔。看烟花绽放，赏圆月当空，吃一口月饼，道一声安康。愿你我心中所念，皆能如愿以偿。祝大家中秋快乐，阖家幸福！ |
| --- | --- |

### **文字识别与信息抽取**

识别图像中的文字、公式或抽取票据、证件、表单中的信息，支持格式化输出文本；Qwen3.5及Qwen3-VL模型支持的语言均增加至33种，支持的语言可参见[模型特性对比](#a47aeb6443ysh)。

| ![-q2cdz6jy89b6m3kp](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7372672671/p1025119.webp) 提取图中的：\\['发票代码','发票号码','到站','燃油费','票价','乘车日期','开车时间','车次','座号'\\]，请你以JSON格式输出。 | { "发票代码": "221021325353", "发票号码": "10283819", "到站": "开发区", "燃油费": "2.0", "票价": "8.00<全>", "乘车日期": "2013-06-29", "开车时间": "流水", "车次": "040", "座号": "371" } |
| --- | --- |

### **多学科题目解答**

解答图像中的数学、物理、化学等问题，适用于中小学、大学以及成人教育阶段。

| ![-5jwcstcvmdpqghaj](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7372672671/p1025120.webp) 请你分步骤解答图中的数学题。 | ![-答案](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7372672671/p1025121.webp) |
| --- | --- |

### **视觉编程**

可通过图像或视频生成代码，可用于将设计图、网站截图等生成HTML、CSS、JS 代码。

| ![code](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 根据我的草图设计使用HTML、CSS创建网页，主色调为黑色。 | ![code-预览](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) **网页预览效果** |
| --- | --- |

### **物体定位**

支持二维和三维定位，可用于判断物体方位、视角变化、遮挡关系。三维定位为Qwen3-VL模型新增能力。

> Qwen2.5-VL模型 480\*480 ～ 2560\*2560 分辨率范围内，物体定位效果较为鲁棒，在此范围之外检测精度可能会下降（偶发检测框漂移现象）。

> 如需将定位结果绘制到原图可参见[常见问题](#178c39c20b290)。

| **二维定位** ![-530xdcos1lqkcfuy](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) - 返回 Box（边界框）坐标 ：检测图中所有食物并以JSON格式输出其bbox的坐标。 - 返回 Point（中心点）坐标：以点的形式定位图中所有食物并以XML格式输出其point坐标。 | **可视化展示二维定位效果** ![-mu9podu1eyvph1zd](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |
| --- | --- |
| **三维定位** ![3d](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 检测图像中的汽车并预测3D位置。输出JSON：`[{"bbox_3d": [x_center, y_center, z_center, x_size, y_size, z_size, roll, pitch, yaw], "label": "category"}]`。 | **可视化展示三维定位效果** ![3d-结果](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |

### **文档解析**

将图像类的文档（如扫描件/图片PDF）解析为 QwenVL HTML 或 QwenVL Markdown 格式，该格式不仅能精准识别文本，还能获取图像、表格等元素的位置信息。Qwen3-VL模型新增解析为 Markdown 格式的能力。

> 推荐提示词如下：`qwenvl html`（解析为HTML格式）或`qwenvl markdown`（解析为Markdown格式）

| ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) qwenvl markdown。 | ![-结果](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) **可视化展示效果** |
| --- | --- |

### **视频理解**

分析视频内容，如对具体事件进行定位并获取时间戳、生成关键时间段的摘要等。

| 请你描述下视频中的人物的一系列动作，以JSON格式输出开始时间（start\\_time）、结束时间（end\\_time）、事件（event），请使用HH:mm:ss表示 时间戳。 | { "events": \\[ { "start\\_time": "00:00:00", "end\\_time": "00:00:05", "event": "人物手持一个纸箱走向桌子，并将纸箱放在桌上。" }, { "start\\_time": "00:00:05", "end\\_time": "00:00:15", "event": "人物拿起扫描枪，对准纸箱上的标签进行扫描。" }, { "start\\_time": "00:00:15", "end\\_time": "00:00:21", "event": "人物将扫描枪放回原位，然后拿起笔在笔记本上记录信息。"}\\] } |
| --- | --- |

## **核心能力**

### **开启/关闭思考模式**

-   `qwen3.5`、`qwen3-vl-plus`、`qwen3-vl-flash`系列模型属于混合思考模型，模型可以在思考后回复，也可直接回复；通过`enable_thinking`参数控制是否开启思考模式：
    
    -   `true`：开启思考模式。`qwen3.5`系列模型默认为`true`。
        
    -   `false`：关闭思考模式。`qwen3-vl-plus`、`qwen3-vl-flash`系列模型默认为`false`。
        
-   `qwen3-vl-235b-a22b-thinking`等带`thinking`后缀的属于仅思考模型，模型总会在回复前进行思考，且无法关闭。
    

**重要**

-   **模型配置：**在非 Agent 工具调用的通用对话场景下，为保持最佳效果，建议不设置`System Message`，可将模型角色设定、输出格式要求等指令通过`User Message` 传入。
    
-   **优先使用流式输出：** 开启思考模式时，支持**流式和非流式**两种输出方式。为避免因响应内容过长导致超时，建议优先使用流式输出方式。
    
-   **限制思考长度：**深度思考模型有时会输出冗长的推理过程，可使用 `thinking_budget` 参数限制思考过程的长度。若模型思考过程生成的 Token 数超过`thinking_budget`，推理内容会进行截断并立刻开始生成最终回复内容。`thinking_budget` 默认值为模型的最大思维链长度，请参见[模型列表](https://help.aliyun.com/zh/model-studio/models)。
    

## OpenAI 兼容

`enable_thinking`非 OpenAI 标准参数，若使用 OpenAI Python SDK 请通过 `extra_body`传入。

Python

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 各地域配置不同，请根据实际地域修改
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

reasoning_content = ""  # 定义完整思考过程
answer_content = ""     # 定义完整回复
is_answering = False   # 判断是否结束思考过程并开始回复
enable_thinking = True
# 创建聊天完成请求
completion = client.chat.completions.create(
    model="qwen3.5-plus",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
                    },
                },
                {"type": "text", "text": "这道题怎么解答？"},
            ],
        },
    ],
    stream=True,
    # enable_thinking 参数开启思考过程，thinking_budget 参数设置最大推理过程 Token 数
    # qwen3.5、qwen3-vl-plus、 qwen3-vl-flash可通过enable_thinking开启或关闭思考、对于qwen3-vl-235b-a22b-thinking等带thinking后缀的模型，enable_thinking仅支持设置为开启，对其他Qwen-VL模型均不适用
    extra_body={
        'enable_thinking': enable_thinking,
        "thinking_budget": 81920},

    # 解除以下注释会在最后一个chunk返回Token使用量
    # stream_options={
    #     "include_usage": True
    # }
)

if enable_thinking:
    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    # 如果chunk.choices为空，则打印usage
    if not chunk.choices:
        print("\nUsage:")
        print(chunk.usage)
    else:
        delta = chunk.choices[0].delta
        # 打印思考过程
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
            print(delta.reasoning_content, end='', flush=True)
            reasoning_content += delta.reasoning_content
        else:
            # 开始回复
            if delta.content != "" and is_answering is False:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                is_answering = True
            # 打印回复过程
            print(delta.content, end='', flush=True)
            answer_content += delta.content

# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(reasoning_content)
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(answer_content)
```

Node.js

```
import OpenAI from "openai";

// 初始化 openai 客户端
const openai = new OpenAI({
     // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY, 
    // 各地域配置不同，请根据实际地域修改
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;
let enableThinking = true;

let messages = [
    {
        role: "user",
        content: [
        { type: "image_url", image_url: { "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg" } },
        { type: "text", text: "解答这道题" },
    ]
}]

async function main() {
    try {
        const stream = await openai.chat.completions.create({
            model: 'qwen3.5-plus',
            messages: messages,
            stream: true,
          // 注意：在 Node.js SDK，enableThinking 这样的非标准参数作为顶层属性传递的，无需放在 extra_body 中
          enable_thinking: enableThinking,
          thinking_budget: 81920

        });

        if (enableThinking){console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');}

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\nUsage:');
                console.log(chunk.usage);
                continue;
            }

            const delta = chunk.choices[0].delta;

            // 处理思考过程
            if (delta.reasoning_content) {
                process.stdout.write(delta.reasoning_content);
                reasoningContent += delta.reasoning_content;
            }
            // 处理正式回复
            else if (delta.content) {
                if (!isAnswering) {
                    console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
                    isAnswering = true;
                }
                process.stdout.write(delta.content);
                answerContent += delta.content;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改
# === 执行时请删除该注释 ===

curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen3.5-plus",
    "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
          }
        },
        {
          "type": "text",
          "text": "请解答这道题"
        }
      ]
    }
  ],
    "stream":true,
    "stream_options":{"include_usage":true},
    "enable_thinking": true,
    "thinking_budget": 81920
}'
```

## DashScope

Python

```
import os
import dashscope
from dashscope import MultiModalConversation

# 各地域配置不同，请根据实际地域修改
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

enable_thinking=True
messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"},
            {"text": "解答这道题？"}
        ]
    }
]

response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen3.5-plus",
    messages=messages,
    stream=True,
    # enable_thinking 参数开启思考过程
    # qwen3.5、qwen3-vl-plus、 qwen3-vl-flash可通过enable_thinking开启或关闭思考、对于qwen3-vl-235b-a22b-thinking等带thinking后缀的模型，enable_thinking仅支持设置为开启，对其他Qwen-VL模型均不适用
    enable_thinking=enable_thinking,
    # thinking_budget 参数设置最大推理过程 Token 数
    thinking_budget=81920,

)

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""
# 判断是否结束思考过程并开始回复
is_answering = False
if enable_thinking:
    print("=" * 20 + "思考过程" + "=" * 20)

for chunk in response:
    # 如果思考过程与回复皆为空，则忽略
    message = chunk.output.choices[0].message
    reasoning_content_chunk = message.get("reasoning_content", None)
    if (chunk.output.choices[0].message.content == [] and
        reasoning_content_chunk == ""):
        pass
    else:
        # 如果当前为思考过程
        if reasoning_content_chunk is not None and chunk.output.choices[0].message.content == []:
            print(chunk.output.choices[0].message.reasoning_content, end="")
            reasoning_content += chunk.output.choices[0].message.reasoning_content
        # 如果当前为回复
        elif chunk.output.choices[0].message.content != []:
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
            print(chunk.output.choices[0].message.content[0]["text"], end="")
            answer_content += chunk.output.choices[0].message.content[0]["text"]

# 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(f"{reasoning_content}")
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(f"{answer_content}")
```

Java

```
// dashscope SDK的版本 >= 2.21.10
import java.util.*;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import io.reactivex.Flowable;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.exception.InputRequiredException;
import java.lang.System;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 各地域配置不同，请根据实际地域修改
    static {Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";}

    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;

    private static void handleGenerationResult(MultiModalConversationResult message) {
        String re = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        String reasoning = Objects.isNull(re)?"":re; // 默认值

        List<Map<String, Object>> content = message.getOutput().getChoices().get(0).getMessage().getContent();
        if (!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (Objects.nonNull(content) && !content.isEmpty()) {
            Object text = content.get(0).get("text");
            finalContent.append(content.get(0).get("text"));
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(text);
        }
    }
    public static MultiModalConversationParam buildMultiModalConversationParam(MultiModalMessage Msg)  {
        return MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.5-plus")
                .messages(Arrays.asList(Msg))
                .enableThinking(true)
                .thinkingBudget(81920)
                .incrementalOutput(true)
                .build();
    }

    public static void streamCallWithMessage(MultiModalConversation conv, MultiModalMessage Msg)
            throws NoApiKeyException, ApiException, InputRequiredException, UploadFileException {
        MultiModalConversationParam param = buildMultiModalConversationParam(Msg);
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(message -> {
            handleGenerationResult(message);
        });
    }
    public static void main(String[] args) {
        try {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage userMsg = MultiModalMessage.builder()
                    .role(Role.USER.getValue())
                    .content(Arrays.asList(Collections.singletonMap("image", "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"),
                            Collections.singletonMap("text", "请解答这道题")))
                    .build();
            streamCallWithMessage(conv, userMsg);
//             打印最终结果
//            if (reasoningContent.length() > 0) {
//                System.out.println("\n====================完整回复====================");
//                System.out.println(finalContent.toString());
//            }
        } catch (ApiException | NoApiKeyException | UploadFileException | InputRequiredException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-H 'X-DashScope-SSE: enable' \
-d '{
    "model": "qwen3.5-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"},
                    {"text": "请解答这道题"}
                ]
            }
        ]
    },
    "parameters":{
        "enable_thinking": true,
        "incremental_output": true,
        "thinking_budget": 81920
    }
}'
```

### **多图像输入**

视觉理解 模型支持在单次请求中传入多张图片，可用于**商品对比、多页文档处理**等任务。实现时只需在`user message` 的`content`数组中包含多个图片对象即可。

**重要**

图片数量受模型图文总 Token 上限的限制，所有图片和文本的总 Token 数必须小于模型的最大输入。

## OpenAI兼容

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 各地域配置不同，请根据实际地域修改
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.5-plus", # 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=[
       {"role": "user","content": [
           {"type": "image_url","image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},},
           {"type": "image_url","image_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"},},
           {"type": "text", "text": "这些图描绘了什么内容？"},
            ],
        }
    ],
)

print(completion.choices[0].message.content)
```

### **返回结果**

```
图1中是一位女士和一只拉布拉多犬在海滩上互动的场景。女士穿着格子衬衫，坐在沙滩上，与狗进行握手的动作，背景是海浪和天空，整个画面充满了温馨和愉快的氛围。

图2中是一只老虎在森林中行走的场景。老虎的毛色是橙色和黑色条纹相间，它正向前迈步，周围是茂密的树木和植被，地面上覆盖着落叶，整个画面给人一种野生自然的感觉。
```

## Node.js

```
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 各地域配置不同，请根据实际地域修改
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

async function main() {
    const response = await openai.chat.completions.create({
        model: "qwen3.5-plus",  // 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
        messages: [
          {role: "user",content: [
            {type: "image_url",image_url: {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"}},
            {type: "image_url",image_url: {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"}},
            {type: "text", text: "这些图描绘了什么内容？" },
        ]}]
    });
    console.log(response.choices[0].message.content);
}

main()
```

### **返回结果**

```
第一张图片中，一个人和一只狗在海滩上互动。人穿着格子衬衫，狗戴着项圈，他们似乎在握手或击掌。

第二张图片中，一只老虎在森林中行走。老虎的毛色是橙色和黑色条纹，背景是绿色的树木和植被。
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen3.5-plus",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
          }
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"
          }
        },
        {
          "type": "text",
          "text": "这些图描绘了什么内容？"
        }
      ]
    }
  ]
}'
```

### **返回结果**

```
{
  "choices": [
    {
      "message": {
        "content": "图1中是一位女士和一只拉布拉多犬在海滩上互动的场景。女士穿着格子衬衫，坐在沙滩上，与狗进行握手的动作，背景是海景和日落的天空，整个画面显得非常温馨和谐。\n\n图2中是一只老虎在森林中行走的场景。老虎的毛色是橙色和黑色条纹相间，它正向前迈步，周围是茂密的树木和植被，地面上覆盖着落叶，整个画面充满了自然的野性和生机。",
        "role": "assistant"
      },
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null
    }
  ],
  "object": "chat.completion",
  "usage": {
    "prompt_tokens": 2497,
    "completion_tokens": 109,
    "total_tokens": 2606
  },
  "created": 1725948561,
  "system_fingerprint": null,
  "model": "qwen3.5-plus",
  "id": "chatcmpl-0fd66f46-b09e-9164-a84f-3ebbbedbac15"
}
```

## DashScope

## Python

```
import os
import dashscope

# 各地域配置不同，请根据实际地域修改
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
            {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"},
            {"text": "这些图描绘了什么内容?"}
        ]
    }
]

response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3.5-plus', # 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=messages
)

print(response.output.choices[0].message.content[0]["text"])
```

### **返回结果**

```
这些图片展示了一些动物和自然场景。第一张图片中，一个人和一只狗在海滩上互动。第二张图片是一只老虎在森林中行走
```

## Java

```
import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import java.util.HashMap;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 各地域配置不同，请根据实际地域修改
    static {Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";}

    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"),
                        Collections.singletonMap("image", "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"),
                        Collections.singletonMap("text", "这些图描绘了什么内容?"))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
               // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.5-plus")  // 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
                .messages(Arrays.asList(userMessage))
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));    }
    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

### **返回结果**

```
这些图片展示了一些动物和自然场景。

1. 第一张图片：一个女人和一只狗在海滩上互动。女人穿着格子衬衫，坐在沙滩上，狗戴着项圈，伸出爪子与女人握手。
2. 第二张图片：一只老虎在森林中行走。老虎的毛色是橙色和黑色条纹，背景是树木和树叶。
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改
# === 执行时请删除该注释 ===

curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen3.5-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
                    {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"},
                    {"text": "这些图展现了什么内容？"}
                ]
            }
        ]
    }
}'
```

### **返回结果**

```
{
  "output": {
    "choices": [
      {
        "finish_reason": "stop",
        "message": {
          "role": "assistant",
          "content": [
            {
              "text": "这些图片展示了一些动物和自然场景。第一张图片中，一个人和一只狗在海滩上互动。第二张图片是一只老虎在森林中行走。"
            }
          ]
        }
      }
    ]
  },
  "usage": {
    "output_tokens": 81,
    "input_tokens": 1277,
    "image_tokens": 2497
  },
  "request_id": "ccf845a3-dc33-9cda-b581-20fe7dc23f70"
}
```

### **视频理解**

视觉理解模型支持对视频内容进行理解，文件形式包括图像列表（视频帧）或视频文件。以下是理解在线视频或图像列表（通过URL指定）的示例代码。关于视频限制或可传入的图像列表数量限制，请参见[视频限制](#190c9e0005dlq)章节。

> 建议使用性能较优的最新版或近期快照版模型理解视频文件。

## 视频文件

视觉理解模型通过从视频中提取帧序列进行内容分析。您可以通过以下两个参数控制抽帧策略：

-   **fps**：控制抽帧频率，每隔 fps1​秒抽取一帧。取值范围为 \[0.1, 10\]，默认值为 2.0。
    
    -   高速运动场景：建议设置较高的 fps 值，以捕捉更多细节
        
    -   静态或长视频：建议设置较低的 fps 值，以提高处理效率
        
-   **max\_frames**：限制视频抽取帧的上限。当按 fps 计算的总帧数超过此限制时，系统将自动在 max\_frames 内均匀抽帧。**此参数仅在使用 DashScope SDK 时可用。**
    

## OpenAI兼容

> 使用OpenAI SDK或HTTP方式向视觉理解模型直接输入视频文件时，需要将用户消息中的`"type"`参数设为`"video_url"`。

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 各地域配置不同，请根据实际地域修改
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.5-plus",
    messages=[
        {
            "role": "user",
            "content": [
                # 直接传入视频文件时，请将type的值设置为video_url
                {
                    "type": "video_url",
                    "video_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                    },
                    "fps": 2
                },
                {
                    "type": "text",
                    "text": "这段视频的内容是什么?"
                }
            ]
        }
    ]
)

print(completion.choices[0].message.content)
```

## Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 各地域配置不同，请根据实际地域修改
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.chat.completions.create({
        model: "qwen3.5-plus",
        messages: [
            {
                role: "user",
                content: [
                    // 直接传入视频文件时，请将type的值设置为video_url
                    {
                        type: "video_url",
                        video_url: {
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                        },
                        "fps": 2
                    },
                    {
                        type: "text",
                        text: "这段视频的内容是什么?"
                    }
                ]
            }
        ]
    });

    console.log(response.choices[0].message.content);
}

main();
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "qwen3.5-plus",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "video_url",
            "video_url": {
              "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
            },
            "fps":2
          },
          {
            "type": "text",
            "text": "这段视频的内容是什么?"
          }
        ]
      }
    ]
  }'
```

## DashScope

## Python

```
import dashscope
import os

# 各地域配置不同，请根据实际地域修改
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

messages = [
    {"role": "user",
        "content": [
            # fps 可参数控制视频抽帧频率，表示每隔 1/fps 秒抽取一帧，完整用法请参见：https://help.aliyun.com/zh/model-studio/use-qwen-by-calling-api?#2ed5ee7377fum
            {"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4","fps":2},
            {"text": "这段视频的内容是什么?"}
        ]
    }
]

response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量， 请用百炼API Key将下行替换为： api_key ="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3.5-plus',
    messages=messages
)

print(response.output.choices[0].message.content[0]["text"])
```

## Java

```
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 各地域配置不同，请根据实际地域修改
    static {Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";}
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        // fps 可参数控制视频抽帧频率，表示每隔 1/fps 秒抽取一帧，完整用法请参见：https://help.aliyun.com/zh/model-studio/use-qwen-by-calling-api?#2ed5ee7377fum
        Map<String, Object> params = new HashMap<>();
        params.put("video", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4");
        params.put("fps", 2);
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        params,
                        Collections.singletonMap("text", "这段视频的内容是什么?"))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.5-plus")
                .messages(Arrays.asList(userMessage))
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }
    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3.5-plus",
    "input":{
        "messages":[
            {"role": "user","content": [{"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4","fps":2},
            {"text": "这段视频的内容是什么?"}]}]}
}'
```

## 图像列表

当视频以图像列表（即预先抽取的视频帧）传入时，可通过`fps`参数告知模型视频帧之间的时间间隔，这能帮助模型更准确地理解事件的顺序、持续时间和动态变化。模型支持通过 `fps` 参数指定原始视频的抽帧率，表示视频帧是每隔fps1​秒从原始视频中抽取的。该参数支持 **Qwen3.5**、**Qwen3-VL、Qwen2.5-VL**模型。

## OpenAI兼容

> 使用OpenAI SDK或HTTP方式向视觉理解模型输入图片列表形式的视频时，需要将用户消息中的`"type"`参数设为`"video"`。

## Python

```
import os
from openai import OpenAI


client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 各地域配置不同，请根据实际地域修改
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.5-plus", # 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=[{"role": "user","content": [
        # 传入图像列表时，用户消息中的"type"参数为"video"
         {"type": "video","video": [
         "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
         "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
         "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
         "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],
         "fps":2},
         {"type": "text","text": "描述这个视频的具体过程"},
    ]}]
)

print(completion.choices[0].message.content)
```

## Node.js

```
// 确保之前在 package.json 中指定了 "type": "module"
import OpenAI from "openai";

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 各地域配置不同，请根据实际地域修改
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.chat.completions.create({
        model: "qwen3.5-plus",  // 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
        messages: [{
            role: "user",
            content: [
                {
                    // 传入图像列表时，用户消息中的"type"参数为"video"
                    type: "video",
                    video: [
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],
                        "fps":2
                },
                {
                    type: "text",
                    text: "描述这个视频的具体过程"
                }
            ]
        }]
    });
    console.log(response.choices[0].message.content);
}

main();
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3.5-plus",
    "messages": [{"role": "user","content": [{"type": "video","video": [
                  "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                  "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                  "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                  "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],
                  "fps":2},
                {"type": "text","text": "描述这个视频的具体过程"}]}]
}'
```

## DashScope

## Python

```
import os
import dashscope

# 各地域配置不同，请根据实际地域修改
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

messages = [{"role": "user",
             "content": [
                  # 传入图像列表时，fps 参数适用于Qwen3.5、Qwen3-VL 和 Qwen2.5-VL系列模型
                 {"video":["https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                           "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                           "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                           "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],
                   "fps":2},
                 {"text": "描述这个视频的具体过程"}]}]
response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model='qwen3.5-plus', # 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=messages
)
print(response.output.choices[0].message.content[0]["text"])
```

## Java

```
// DashScope SDK版本需要不低于2.21.10
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 各地域配置不同，请根据实际地域修改
    static {Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";}

    private static final String MODEL_NAME = "qwen3.5-plus"; // 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    public static void videoImageListSample() throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        // 传入图像列表时，fps 参数适用于Qwen3.5、Qwen3-VL 和 Qwen2.5-VL系列模型
        Map<String, Object> params = new HashMap<>();
        params.put("video", Arrays.asList("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"));
        params.put("fps", 2);
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(
                        params,
                        Collections.singletonMap("text", "描述这个视频的具体过程")))
                .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model(MODEL_NAME)
                .messages(Arrays.asList(userMessage)).build();
        MultiModalConversationResult result = conv.call(param);
        System.out.print(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }
    public static void main(String[] args) {
        try {
            videoImageListSample();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen3.5-plus",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "video": [
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"
            ],
            "fps":2
                 
          },
          {
            "text": "描述这个视频的具体过程"
          }
        ]
      }
    ]
  }
}'
```

### **传入本地文件（**Base64 编码或文件路径**）**

视觉理解模型提供两种本地文件上传方式：Base64 编码上传和文件路径直接上传。可根据文件大小、SDK类型选择上传方式，具体建议请参见[如何选择文件上传方式](#dc4e7260aauuo)；两种方式均需满足[图像限制](#71c2cb6e09ioo)中对文件的要求。

## Base64 编码上传

将文件转换为 Base64 编码字符串，再传入模型。适用于 OpenAI 和 DashScope SDK 及 HTTP 方式

**传入 Base64 编码字符串的步骤（以图像为例）**

1.  文件编码：将本地图像转换为 Base64 编码；
    
    **图像转换为 Base64 编码的示例代码**
    
    ```
    #  编码函数： 将本地文件转换为 Base64 编码的字符串
    import base64
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    
    # 将xxxx/eagle.png替换为你本地图像的绝对路径
    base64_image = encode_image("xxx/eagle.png")
    ```
    
2.  构建 [Data URL](https://www.rfc-editor.org/rfc/rfc2397)：格式如下：`data:[MIME_type];base64,{base64_image}`；
    
    1.  `MIME_type`需替换为实际的媒体类型，确保与[支持的图像格式](#d6b42862bb1ct)表格中`MIME Type` 的值匹配（如`image/jpeg`、`image/png`）；
        
    2.  `base64_image`为上一步生成的 Base64 字符串；
        
3.  调用模型：通过`image`或`image_url`参数传递`Data URL`并调用模型。
    

## 文件路径上传

直接向模型传入本地文件路径。仅 DashScope Python 和 Java SDK 支持，不支持 DashScope HTTP 和OpenAI 兼容方式。

请您参考下表，结合您的编程语言与操作系统指定文件的路径。

**指定文件路径（以图像为例）**

| **系统** | **SDK** | **传入的文件路径** | **示例** |
| --- | --- | --- | --- |
| Linux或macOS系统 | Python SDK | file://{文件的绝对路径} | file:///home/images/test.png |
| Java SDK |
| Windows系统 | Python SDK | file://{文件的绝对路径} | file://D:/images/test.png |
| Java SDK | file:///{文件的绝对路径} | file:///D:/images/test.pn |

## 图像

## 文件路径传入

## Python

```
import os
from dashscope import MultiModalConversation
import dashscope 

# 各地域配置不同，请根据实际地域修改
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

# 将xxx/eagle.png替换为你本地图像的绝对路径
local_path = "xxx/eagle.png"
image_path = f"file://{local_path}"
messages = [
                {'role':'user',
                'content': [{'image': image_path},
                            {'text': '图中描绘的是什么景象?'}]}]
response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3.5-plus',  # 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=messages)
print(response.output.choices[0].message.content[0]["text"])
```

## Java

```
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 各地域配置不同，请根据实际地域修改
    static {Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";}
    public static void callWithLocalFile(String localPath)
            throws ApiException, NoApiKeyException, UploadFileException {
        String filePath = "file://"+localPath;
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(new HashMap<String, Object>(){{put("image", filePath);}},
                        new HashMap<String, Object>(){{put("text", "图中描绘的是什么景象？");}})).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.5-plus")  // 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
                .messages(Arrays.asList(userMessage))
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));}

    public static void main(String[] args) {
        try {
            // 将xxx/eagle.png替换为你本地图像的绝对路径
            callWithLocalFile("xxx/eagle.png");
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## Base64 编码传入

## OpenAI兼容

## Python

```
from openai import OpenAI
import os
import base64


#  编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# 将xxxx/eagle.png替换为你本地图像的绝对路径
base64_image = encode_image("xxx/eagle.png")

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    # 各地域配置不同，请根据实际地域修改
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.5-plus", # 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    # 需要注意，传入Base64，图像格式（即image/{format}）需要与支持的图片列表中的Content Type保持一致。"f"是字符串格式化的方法。
                    # PNG图像：  f"data:image/png;base64,{base64_image}"
                    # JPEG图像： f"data:image/jpeg;base64,{base64_image}"
                    # WEBP图像： f"data:image/webp;base64,{base64_image}"
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"}, 
                },
                {"type": "text", "text": "图中描绘的是什么景象?"},
            ],
        }
    ],
)
print(completion.choices[0].message.content)
```

## Node.js

```
import OpenAI from "openai";
import { readFileSync } from 'fs';

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 各地域配置不同，请根据实际地域修改
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

const encodeImage = (imagePath) => {
    const imageFile = readFileSync(imagePath);
    return imageFile.toString('base64');
  };
// 将xxx/eagle.png替换为你本地图像的绝对路径
const base64Image = encodeImage("xxx/eagle.png")
async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen3.5-plus",  // 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
        messages: [
            {"role": "user",
             "content": [{"type": "image_url",
                            // 需要注意，传入Base64，图像格式（即image/{format}）需要与支持的图片列表中的Content Type保持一致。
                           // PNG图像：  data:image/png;base64,${base64Image}
                          // JPEG图像： data:image/jpeg;base64,${base64Image}
                         // WEBP图像： data:image/webp;base64,${base64Image}
                        "image_url": {"url": `data:image/png;base64,${base64Image}`},},
                        {"type": "text", "text": "图中描绘的是什么景象?"}]}]
    });
    console.log(completion.choices[0].message.content);
}

main();
```

## curl

-   将文件转换为 Base64 编码的字符串的方法可参见[示例代码](#7aee9382dfqpk)；
    
-   为了便于展示，代码中的`"data:image/jpg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."` ，该Base64 编码字符串是截断的。在实际使用中，请务必传入完整的编码字符串。
    

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改
# === 执行时请删除该注释 ===

curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "qwen3.5-plus",
  "messages": [
  {
    "role": "user",
    "content": [
      {"type": "image_url", "image_url": {"url": "data:image/jpg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."}},
      {"type": "text", "text": "图中描绘的是什么景象?"}
    ]
  }]
}'
```

## DashScope

## Python

```
import base64
import os
import dashscope 
from dashscope import MultiModalConversation

# 各地域配置不同，请根据实际地域修改
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

#  编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# 将xxxx/eagle.png替换为你本地图像的绝对路径
base64_image = encode_image("xxxx/eagle.png")

messages = [
    {
        "role": "user",
        "content": [
            # 需要注意，传入Base64，图像格式（即image/{format}）需要与支持的图片列表中的Content Type保持一致。"f"是字符串格式化的方法。
            # PNG图像：  f"data:image/png;base64,{base64_image}"
            # JPEG图像： f"data:image/jpeg;base64,{base64_image}"
            # WEBP图像： f"data:image/webp;base64,{base64_image}"
            {"image": f"data:image/png;base64,{base64_image}"},
            {"text": "图中描绘的是什么景象?"},
        ],
    },
]
response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3.5-plus",  # 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=messages,
)
print(response.output.choices[0].message.content[0]["text"])
```

## Java

```
import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Base64;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import com.alibaba.dashscope.aigc.multimodalconversation.*;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 各地域配置不同，请根据实际地域修改
   static {Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";}

    private static String encodeImageToBase64(String imagePath) throws IOException {
        Path path = Paths.get(imagePath);
        byte[] imageBytes = Files.readAllBytes(path);
        return Base64.getEncoder().encodeToString(imageBytes);
    }

    public static void callWithLocalFile(String localPath) throws ApiException, NoApiKeyException, UploadFileException, IOException {

        String base64Image = encodeImageToBase64(localPath); // Base64编码

        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        new HashMap<String, Object>() {{ put("image", "data:image/png;base64," + base64Image); }},
                        new HashMap<String, Object>() {{ put("text", "图中描绘的是什么景象？"); }}
                )).build();

        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.5-plus")
                .messages(Arrays.asList(userMessage))
                .build();

        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }

    public static void main(String[] args) {
        try {
            // 将 xxx/eagle.png 替换为你本地图像的绝对路径
            callWithLocalFile("xxx/eagle.png");
        } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## curl

-   将文件转换为 Base64 编码的字符串的方法可参见[示例代码](#7aee9382dfqpk)；
    
-   为了便于展示，代码中的`"data:image/jpg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."` ，该Base64 编码字符串是截断的。在实际使用中，请务必传入完整的编码字符串。
    

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3.5-plus",
    "input":{
        "messages":[
            {
             "role": "user",
             "content": [
               {"image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."},
               {"text": "图中描绘的是什么景象?"}
                ]
            }
        ]
    }
}'
```

## 视频文件

以保存在本地的[test.mp4](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250118/hcgaks/test.mp4)为例。

## 文件路径传入

## Python

```
import os
from dashscope import MultiModalConversation
import dashscope 

# 各地域配置不同，请根据实际地域修改
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

# 将xxxx/test.mp4替换为你本地视频的绝对路径
local_path = "xxx/test.mp4"
video_path = f"file://{local_path}"
messages = [
                {'role':'user',
                # fps参数控制视频抽帧数量，表示每隔1/fps 秒抽取一帧
                'content': [{'video': video_path,"fps":2},
                            {'text': '这段视频描绘的是什么景象？'}]}]
response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3.5-plus',  
    messages=messages)
print(response.output.choices[0].message.content[0]["text"])
```

## Java

```
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 各地域配置不同，请根据实际地域修改
    static {Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";}
    
    public static void callWithLocalFile(String localPath)
            throws ApiException, NoApiKeyException, UploadFileException {
        String filePath = "file://"+localPath;
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(new HashMap<String, Object>()
                                       {{
                                           put("video", filePath);// fps参数控制视频抽帧数量，表示每隔1/fps 秒抽取一帧
                                           put("fps", 2);
                                       }}, 
                        new HashMap<String, Object>(){{put("text", "这段视频描绘的是什么景象？");}})).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.5-plus")  
                .messages(Arrays.asList(userMessage))
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));}

    public static void main(String[] args) {
        try {
            // 将xxxx/test.mp4替换为你本地视频的绝对路径
            callWithLocalFile("xxx/test.mp4");
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## Base64 编码传入

## OpenAI兼容

## Python

```
from openai import OpenAI
import os
import base64


# 编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_video(video_path):
    with open(video_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode("utf-8")

# 将xxxx/test.mp4替换为你本地视频的绝对路径
base64_video = encode_video("xxx/test.mp4")
client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    # 各地域配置不同，请根据实际地域修改
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.5-plus",  
    messages=[
        {
            "role": "user",
            "content": [
                {
                    # 直接传入视频文件时，请将type的值设置为video_url
                    "type": "video_url",
                    "video_url": {"url": f"data:video/mp4;base64,{base64_video}"},
                    "fps":2
                },
                {"type": "text", "text": "这段视频描绘的是什么景象？"},
            ],
        }
    ],
)
print(completion.choices[0].message.content)
```

## Node.js

```
import OpenAI from "openai";
import { readFileSync } from 'fs';

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 各地域配置不同，请根据实际地域修改
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

const encodeVideo = (videoPath) => {
    const videoFile = readFileSync(videoPath);
    return videoFile.toString('base64');
  };
// 将xxxx/test.mp4替换为你本地视频的绝对路径
const base64Video = encodeVideo("xxx/test.mp4")
async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen3.5-plus", 
        messages: [
            {"role": "user",
             "content": [{
                 // 直接传入视频文件时，请将type的值设置为video_url
                "type": "video_url", 
                "video_url": {"url": `data:video/mp4;base64,${base64Video}`},
                "fps":2},
                 {"type": "text", "text": "这段视频描绘的是什么景象？"}]}]
    });
    console.log(completion.choices[0].message.content);
}

main();
```

## curl

-   将文件转换为 Base64 编码的字符串的方法可参见[示例代码](#7aee9382dfqpk)；
    
-   为了便于展示，代码中的`"data:video/mp4;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."` ，该Base64 编码字符串是截断的。在实际使用中，请务必传入完整的编码字符串。
    

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改
# === 执行时请删除该注释 ===

curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "qwen3.5-plus",
  "messages": [
  {
    "role": "user",
    "content": [
      {"type": "video_url", "video_url": {"url": "data:video/mp4;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."},"fps":2},
      {"type": "text", "text": "图中描绘的是什么景象?"}
    ]
  }]
}'
```

## DashScope

## Python

```
import base64
import os
import dashscope 
from dashscope import MultiModalConversation

# 各地域配置不同，请根据实际地域修改
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

# 编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_video(video_path):
    with open(video_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode("utf-8")

# 将xxxx/test.mp4替换为你本地视频的绝对路径
base64_video = encode_video("xxxx/test.mp4")

messages = [{'role':'user',
            # fps参数控制视频抽帧数量，表示每隔1/fps 秒抽取一帧
             'content': [{'video': f"data:video/mp4;base64,{base64_video}","fps":2},
                            {'text': '这段视频描绘的是什么景象？'}]}]
response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3.5-plus',
    messages=messages)

print(response.output.choices[0].message.content[0]["text"])
```

## Java

```
import java.io.IOException;
import java.util.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import com.alibaba.dashscope.aigc.multimodalconversation.*;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 各地域配置不同，请根据实际地域修改
    static {Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";}
    private static String encodeVideoToBase64(String videoPath) throws IOException {
        Path path = Paths.get(videoPath);
        byte[] videoBytes = Files.readAllBytes(path);
        return Base64.getEncoder().encodeToString(videoBytes);
    }

    public static void callWithLocalFile(String localPath)
            throws ApiException, NoApiKeyException, UploadFileException, IOException {

        String base64Video = encodeVideoToBase64(localPath); // Base64编码

        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(new HashMap<String, Object>()
                                       {{
                                           put("video", "data:video/mp4;base64," + base64Video);// fps参数控制视频抽帧数量，表示每隔1/fps 秒抽取一帧
                                           put("fps", 2);
                                       }},
                        new HashMap<String, Object>(){{put("text", "这段视频描绘的是什么景象？");}})).build();

        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.5-plus")
                .messages(Arrays.asList(userMessage))
                .build();

        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }

    public static void main(String[] args) {
        try {
            // 将 xxx/test.mp4 替换为你本地视频的绝对路径
            callWithLocalFile("xxx/test.mp4");
        } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## curl

-   将文件转换为 Base64 编码的字符串的方法可参见[示例代码](#7aee9382dfqpk)；
    
-   为了便于展示，代码中的`"f"data:video/mp4;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."` ，该Base64 编码字符串是截断的。在实际使用中，请务必传入完整的编码字符串。
    

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3.5-plus",
    "input":{
        "messages":[
            {
             "role": "user",
             "content": [
               {"video": "data:video/mp4;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."},
               {"text": "这段视频描绘的是什么景象? "}
                ]
            }
        ]
    }
}'
```

## 图像列表

以保存在本地的[football1.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250319/vzfwkh/football1.jpg)、[football2.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250319/vgkgqy/football2.jpg)、[football3.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250319/mgvhvh/football3.jpg)、[football4.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250319/bydzjh/football4.jpg)为例。

## 文件路径传入

## Python

```
import os
from dashscope import MultiModalConversation
import dashscope 

# 各地域配置不同，请根据实际地域修改
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

local_path1 = "football1.jpg"
local_path2 = "football2.jpg"
local_path3 = "football3.jpg"
local_path4 = "football4.jpg"

image_path1 = f"file://{local_path1}"
image_path2 = f"file://{local_path2}"
image_path3 = f"file://{local_path3}"
image_path4 = f"file://{local_path4}"

messages = [{'role':'user',
              #  传入图像列表时，fps 参数适用于Qwen3.5、Qwen3-VL 和 Qwen2.5-VL系列模型
             'content': [{'video': [image_path1,image_path2,image_path3,image_path4],"fps":2},
                            {'text': '这段视频描绘的是什么景象?'}]}]
response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3.5-plus',  # 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=messages)

print(response.output.choices[0].message.content[0]["text"])
```

## Java

```
// DashScope SDK版本需要不低于2.21.10
import java.util.Arrays;
import java.util.Map;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;


public class Main {

    // 各地域配置不同，请根据实际地域修改
    static {Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";}

    private static final String MODEL_NAME = "qwen3.5-plus";  // 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    public static void videoImageListSample(String localPath1, String localPath2, String localPath3, String localPath4)
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        String filePath1 = "file://" + localPath1;
        String filePath2 = "file://" + localPath2;
        String filePath3 = "file://" + localPath3;
        String filePath4 = "file://" + localPath4;
        Map<String, Object> params = new HashMap<>();
        params.put("video", Arrays.asList(filePath1,filePath2,filePath3,filePath4));
        //  传入图像列表时，fps 参数适用于Qwen3.5、Qwen3-VL 和 Qwen2.5-VL系列模型
        params.put("fps", 2);
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(params,
                        Collections.singletonMap("text", "描述这个视频的具体过程")))
                .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 各地域的API Key不同。获取API Key：https://www.alibabacloud.com/help/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model(MODEL_NAME)
                .messages(Arrays.asList(userMessage)).build();
        MultiModalConversationResult result = conv.call(param);
        System.out.print(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }
    public static void main(String[] args) {
        try {
            videoImageListSample(
                    "xxx/football1.jpg",
                    "xxx/football2.jpg",
                    "xxx/football3.jpg",
                    "xxx/football4.jpg");
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## Base64 编码传入

## OpenAI兼容

## Python

```
import os
from openai import OpenAI
import base64

# 编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image1 = encode_image("football1.jpg")
base64_image2 = encode_image("football2.jpg")
base64_image3 = encode_image("football3.jpg")
base64_image4 = encode_image("football4.jpg")
client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 各地域配置不同，请根据实际地域修改
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.5-plus",  # 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=[
    {"role": "user","content": [
        {"type": "video","video": [
            f"data:image/jpeg;base64,{base64_image1}",
            f"data:image/jpeg;base64,{base64_image2}",
            f"data:image/jpeg;base64,{base64_image3}",
            f"data:image/jpeg;base64,{base64_image4}",]},
        {"type": "text","text": "描述这个视频的具体过程"},
    ]}]
)
print(completion.choices[0].message.content)
```

## Node.js

```
import OpenAI from "openai";
import { readFileSync } from 'fs';

const openai = new OpenAI(
    {
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 各地域配置不同，请根据实际地域修改
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

const encodeImage = (imagePath) => {
    const imageFile = readFileSync(imagePath);
    return imageFile.toString('base64');
  };
  
const base64Image1 = encodeImage("football1.jpg")
const base64Image2 = encodeImage("football2.jpg")
const base64Image3 = encodeImage("football3.jpg")
const base64Image4 = encodeImage("football4.jpg")
async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen3.5-plus", // 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
        messages: [
            {"role": "user",
             "content": [{"type": "video",
                        "video": [
                            `data:image/jpeg;base64,${base64Image1}`,
                            `data:image/jpeg;base64,${base64Image2}`,
                            `data:image/jpeg;base64,${base64Image3}`,
                            `data:image/jpeg;base64,${base64Image4}`]},
                        {"type": "text", "text": "这段视频描绘的是什么景象？"}]}]
    });
    console.log(completion.choices[0].message.content);
}

main();
```

## curl

-   将文件转换为 Base64 编码的字符串的方法可参见[示例代码](#7aee9382dfqpk)；
    
-   为了便于展示，代码中的`"data:image/jpg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."` ，该Base64 编码字符串是截断的。在实际使用中，请务必传入完整的编码字符串。
    

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3.5-plus",
    "messages": [{"role": "user",
                "content": [{"type": "video",
                "video": [
                          "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA...",
                          "data:image/jpeg;base64,nEpp6jpnP57MoWSyOWwrkXMJhHRCWYeFYb...",
                          "data:image/jpeg;base64,JHWQnJPc40GwQ7zERAtRMK6iIhnWw4080s...",
                          "data:image/jpeg;base64,adB6QOU5HP7dAYBBOg/Fb7KIptlbyEOu58..."
                          ]},
                {"type": "text",
                "text": "描述这个视频的具体过程"}]}]
}'
```

## DashScope

## Python

```
import base64
import os
from dashscope import MultiModalConversation
import dashscope 

# 各地域配置不同，请根据实际地域修改
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

#  编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image1 = encode_image("football1.jpg")
base64_image2 = encode_image("football2.jpg")
base64_image3 = encode_image("football3.jpg")
base64_image4 = encode_image("football4.jpg")


messages = [{'role':'user',
             'content': [
                    {'video':
                         [f"data:image/jpeg;base64,{base64_image1}",
                          f"data:image/jpeg;base64,{base64_image2}",
                          f"data:image/jpeg;base64,{base64_image3}",
                          f"data:image/jpeg;base64,{base64_image4}"
                         ]
                    },
                    {'text': '请描绘这个视频的具体过程?'}]}]
response = MultiModalConversation.call(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model='qwen3.5-plus',  # 此处以qwen3.5-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
    messages=messages)

print(response.output.choices[0].message.content[0]["text"])
```

## Java

```
import java.io.IOException;
import java.util.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import com.alibaba.dashscope.aigc.multimodalconversation.*;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 各地域配置不同，请根据实际地域修改
    static {Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";}

    private static String encodeImageToBase64(String imagePath) throws IOException {
        Path path = Paths.get(imagePath);
        byte[] imageBytes = Files.readAllBytes(path);
        return Base64.getEncoder().encodeToString(imageBytes);
    }

    public static void videoImageListSample(String localPath1,String localPath2,String localPath3,String localPath4)
            throws ApiException, NoApiKeyException, UploadFileException, IOException {

        String base64Image1 = encodeImageToBase64(localPath1); // Base64编码
        String base64Image2 = encodeImageToBase64(localPath2);
        String base64Image3 = encodeImageToBase64(localPath3);
        String base64Image4 = encodeImageToBase64(localPath4);

        MultiModalConversation conv = new MultiModalConversation();
        Map<String, Object> params = new HashMap<>();
        params.put("video", Arrays.asList(
                        "data:image/jpeg;base64," + base64Image1,
                        "data:image/jpeg;base64," + base64Image2,
                        "data:image/jpeg;base64," + base64Image3,
                        "data:image/jpeg;base64," + base64Image4));
        //  传入图像列表时，fps 参数适用于Qwen3.5、Qwen3-VL 和 Qwen2.5-VL系列模型
        params.put("fps", 2);
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(params,
                        Collections.singletonMap("text", "描述这个视频的具体过程")))
                .build();

        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.5-plus")
                .messages(Arrays.asList(userMessage))
                .build();

        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }

    public static void main(String[] args) {
        try {
            // 将 xxx/football1.png 等替换为你本地图像的绝对路径
            videoImageListSample(
                    "xxx/football1.jpg",
                    "xxx/football2.jpg",
                    "xxx/football3.jpg",
                    "xxx/football4.jpg"
            );
        } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## curl

-   将文件转换为 Base64 编码的字符串的方法可参见[示例代码](#7aee9382dfqpk)；
    
-   为了便于展示，代码中的`"data:image/jpg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."` ，该Base64 编码字符串是截断的。在实际使用中，请务必传入完整的编码字符串。
    

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen3.5-plus",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "video": [
                      "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA...",
                      "data:image/jpeg;base64,nEpp6jpnP57MoWSyOWwrkXMJhHRCWYeFYb...",
                      "data:image/jpeg;base64,JHWQnJPc40GwQ7zERAtRMK6iIhnWw4080s...",
                      "data:image/jpeg;base64,adB6QOU5HP7dAYBBOg/Fb7KIptlbyEOu58..."
            ],
            "fps":2     
          },
          {
            "text": "描述这个视频的具体过程"
          }
        ]
      }
    ]
  }
}'
```

### 处理高分辨率图像

视觉理解模型 API对单张图像编码后的视觉 Token 数量设有限制，默认配置下，高分辨率图像会被压缩，可能丢失细节，影响理解准确性。启用 `vl_high_resolution_images` 或调整 `max_pixels` 可增加视觉 Token 数量，从而保留更多图像细节，提升理解效果。

**查看每个模型视觉 Token 对应的像素、Token 上限和像素上限**

> 当输入图像像素大于模型的像素上限时，会将图像进行缩小至像素上限内。

| **模型** | **每Token 对应像素** | **vl\\_high\\_resolution\\_images** | **max\\_pixels** | **Token 上限** | **像素上限** |
| --- | --- | --- | --- | --- | --- |
| `Qwen3.5`、`Qwen3-VL`系列模型 | `32*32` | `true` | `max_pixels` 无效 | `16384 Token` | `16777216`（即`16384*32*32`） |
| `false`（默认） | 可自定义，默认为 `2621440`，最大值是`16777216` | 由 `max_pixels` 决定，即`max_pixels/32/32` | `max_pixels` |
| `qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-2025-08-13`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-2025-08-15``、qwen-vl-plus-2025-07-10`模型 | `32*32` | `true` | `max_pixels` 无效 | `16384 Token` | `16777216`（即`16384*32*32`） |
| `false`（默认） | 可自定义，默认为`1310720`，最大值是`16777216` | 由 `max_pixels` 决定，即`max_pixels/32/32` | `max_pixels` |
| 其他`qwen-vl-max`、其他`qwen-vl-plus`、`Qwen2.5-VL`开源系列、`QVQ`系列模型 | `28*28` | `true` | `max_pixels` 无效 | `16384 Token` | `12845056`（即`16384*28*28`） |
| `false`（默认） | 可自定义，默认为`1003520`，最大值是`12845056` | 由 `max_pixels` 决定，即`max_pixels/28/28` | `max_pixels` |

-   当`vl_high_resolution_images=true`时，API 使用固定分辨率策略，忽略`max_pixels`设置。适合用于识别图像中的精细文本、微小物体或丰富细节。
    
-   当`vl_high_resolution_images=false`时，最终的像素上限取决于 `max_pixels` 参数值。
    
    -   对处理速度要求高或成本敏感：使用`max_pixels`的默认值或设置为更小的值
        
    -   需要关注一定的细节，可接受较低的处理速度：适当提高`max_pixels`的值
        

## OpenAI 兼容

`vl_high_resolution_images`非 OpenAI 标准参数，在不同语言的 SDK 中传递方式存在差异：

-   **Python SDK:** 必须通过 `extra_body` 字典传递
    
-   **Node.js SDK:** 可作为顶层参数直接传递
    

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 各地域配置不同，请根据实际地域修改
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


completion = client.chat.completions.create(
    model="qwen3.5-plus",
    messages=[
        {"role": "user","content": [
            {"type": "image_url","image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg"},
            # max_pixels表示输入图像的最大像素阈值，在vl_high_resolution_images=True，无效，vl_high_resolution_images=False，支持自定义，不同模型最大值不同
            # "max_pixels": 16384 * 32 * 32
            },
           {"type": "text", "text": "这张图表现的是哪个节日的氛围？"},
            ],
        }
    ],
    extra_body={"vl_high_resolution_images":True}

)
print(f"模型输出结果: {completion.choices[0].message.content}")
print(f"输入总Tokens: {completion.usage.prompt_tokens}")
```

## Node.js

```
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 各地域配置不同，请根据实际地域修改
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);
 const response = await openai.chat.completions.create({
        model: "qwen3.5-plus",
        messages: [
        {role: "user",content: [
            {type: "image_url",
            image_url: {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg"},
            // max_pixels表示输入图像的最大像素阈值，在vl_high_resolution_images=True，不生效，vl_high_resolution_images=False，支持自定义，不同模型最大值不同
            // "max_pixels": 2560 * 32 * 32
            },
            {type: "text", text: "这张图表现的是哪个节日的氛围？" },
        ]}],
        vl_high_resolution_images:true
    })


console.log("模型输出结果：",response.choices[0].message.content);
console.log("输入总Tokens",response.usage.prompt_tokens);
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen3.5-plus",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg"
          }
        },
        {
          "type": "text",
          "text": "这张图表现的是哪个节日的氛围？"
        }
      ]
    }
  ],
  "vl_high_resolution_images":true
}'
```

## DashScope

## Python

```
import os
import dashscope

# 各地域配置不同，请根据实际地域修改
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg",
            # max_pixels表示输入图像的最大像素阈值，在vl_high_resolution_images=True，无效，vl_high_resolution_images=False，支持自定义，不同模型最大值不同
            # "max_pixels": 16384 * 32 * 32
            },
            {"text": "这张图表现的是哪个节日的氛围？"}
        ]
    }
]

response = dashscope.MultiModalConversation.call(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
        # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model='qwen3.5-plus',
        messages=messages,
        vl_high_resolution_images=True
    )


print("模型输出",response.output.choices[0].message.content[0]["text"])
print("输入总Tokens：",response.usage.input_tokens)
```

## Java

```
import java.util.Arrays;
import java.util.Collections;
import java.util.Map;
import java.util.HashMap;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 各地域配置不同，请根据实际地域修改
    static {Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";}
    
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        Map<String, Object> map = new HashMap<>();
        map.put("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg");
        // max_pixels表示输入图像的最大像素阈值，在vl_high_resolution_images=True，无效，vl_high_resolution_images=False，支持自定义，不同模型最大值不同
        // map.put("max_pixels", 2621440); 
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        map,
                        Collections.singletonMap("text", "这张图表现的是哪个节日的氛围？"))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.5-plus")
                .message(userMessage)
                .vlHighResolutionImages(true)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
        System.out.println(result.getUsage().getInputTokens());
    }

    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3.5-plus",
    "input":{
        "messages":[
            {
             "role": "user",
             "content": [
               {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg"
                },
               {"text": "这张图表现的是哪个节日的氛围？"}
                ]
            }
        ]
    },
    "parameters": {
        "vl_high_resolution_images": true
    }
}'
```

### **更多用法**

-   [多轮对话](https://help.aliyun.com/zh/model-studio/multi-round-conversation#6feb3eb136g3q)
    
-   [流式输出](https://help.aliyun.com/zh/model-studio/stream#39de325514ak9)
    

## **使用限制**

### **输入文件限制**

## **图像限制**

-   **图像分辨率：**
    
    -   最小尺寸：图像的宽度和高度均须大于`10`像素。
        
    -   宽高比：图像长边与短边的比值不得超过 `200:1`。
        
    -   像素上限：
        
        -   推荐将图像分辨率控制在`8K(7680x4320)`以内。超过此分辨率的图像可能因文件过大、网络传输耗时过长而导致 API 调用超时。
            
        -   自动缩放机制：模型可通过`max_pixels`和`min_pixels`调整图像大小；因此，提供超高分辨率的图像并不会提升识别精度，反而会增加调用失败的风险，建议在客户端提前将图像缩放至合理大小。
            
-   **支持的图像格式**
    
    -   分辨率在4K`(3840x2160)`以下，支持的图像格式如下：
        
        | **图像格式** | **常见扩展名** | **MIME Type** |
        | --- | --- | --- |
        | BMP | .bmp | image/bmp |
        | JPEG | .jpe, .jpeg, .jpg | image/jpeg |
        | PNG | .png | image/png |
        | TIFF | .tif, .tiff | image/tiff |
        | WEBP | .webp | image/webp |
        | HEIC | .heic | image/heic |
        
    -   分辨率处于`4K(3840x2160)`到`8K(7680x4320)`范围，仅支持 JPEG、JPG 、PNG 格式
        
-   **图像大小：**
    
    -   以公网 URL 传入时：Qwen3.5 单个图像不超过 `20MB`，其他模型单个图像不超过`10MB`
        
    -   以本地路径传入时：单个图像不超过`10MB`
        
    -   以 Base64 编码传入时：编码后的字符串不超过`10MB`
        
    
    > 如需压缩文件体积请参见[如何将图像或视频压缩到满足要求的大小](#ec8e0a8e03moe)。
    
-   **图片数量限制：**多图输入时根据传入方式不同，支持的图片数量上限有所区别：
    
    -   以公网 URL 或本地路径传入时：最多 256 张
        
    -   以 Base64 编码传入时：最多 250 张
        
        > 同时受模型图文总 Token 上限（即最大输入）的限制，所有图片的总 Token 数必须小于模型的最大输入。
        

## **视频限制**

-   **以图像列表传入，图像列表的数量有如下限制：**
    
    -   `qwen3.5` 系列：最少传入 4 张图片，最多 8000 张图片
        
    -   `qwen3-vl-plus` 系列、`qwen3-vl-flash` 系列、`qwen3-vl-235b-a22b-thinking`、`qwen3-vl-235b-a22b-instruct`：最少传入 4 张图片，最多 2000 张图片
        
    -   其他`Qwen3-VL`开源、`Qwen2.5-VL`（包括商业版和开源版）和`QVQ`系列模型：最少传入 4 张图片，最多 512 张图片
        
    -   其他模型：最少传入 4 张图片，最多 80 张图片
        
-   **以视频文件传入时：**
    
    -   **视频大小：**
        
        -   以公网 URL 传入时：
            
            -   `qwen3.5` 系列、`Qwen3-VL`系列、`qwen-vl-max`（包含`qwen-vl-max-latest`、`qwen-vl-max-2025-04-08` 之后的所有版本）：不超过 2GB；
                
            -   `qwen-vl-plus` 系列、其他`qwen-vl-max`模型、`Qwen2.5-VL`开源系列及`QVQ`系列模型：不超过 1GB；
                
            -   其他模型不超过 150MB
                
        -   以 Base64 编码传入时：编码后的字符串小于 10MB；
            
        -   以本地文件路径传入时：视频本身不超过 100MB。
            
        
        > 如需压缩文件体积请参见[如何将图像或视频压缩到满足要求的大小](#ec8e0a8e03moe)。
        
    -   **视频时长：**
        
        -   `qwen3.5` 系列：2秒至2小时；
            
        -   `qwen3-vl-plus`系列、`qwen3-vl-flash`系列、`qwen3-vl-235b-a22b-thinking`、`qwen3-vl-235b-a22b-instruct`：2 秒至 1 小时；
            
        -   其他`Qwen3-VL`开源系列、`qwen-vl-max`（包含`qwen-vl-max-latest`、`qwen-vl-max-2025-04-08` 及之后更新的版本）：2 秒至 20 分钟；
            
        -   `qwen-vl-plus`系列、 其他`qwen-vl-max`模型、`Qwen2.5-VL`开源系列及`QVQ`系列模型：2 秒至 10 分钟；
            
        -   其他模型：2 秒至 40 秒。
            
    -   **视频格式：** MP4、AVI、MKV、MOV、FLV、WMV 等。
        
    -   **视频尺寸：**无特定限制，模型可通过`max_pixels`和`min_pixels`自动调整视频尺寸，更大尺寸的视频文件不会有更好的理解效果。
        
    -   **视频数量限制：**最多可传入 64 个视频。
        
    -   **音频理解：**不支持对视频文件的音频进行理解。
        

### **文件传入方式**

-   **公网URL**：提供一个公网可访问的文件地址，支持 HTTP 或 HTTPS 协议。为获得最佳稳定性和性能，可将文件[上传至OSS](https://help.aliyun.com/zh/oss/user-guide/console-quick-start)或[上传文件获取临时URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)，获取公网 URL。
    
    **重要**
    
    为确保模型能成功下载文件，提供的公网 URL的响应头中**必须**包含 Content-Length（文件大小）和 Content-Type（媒体类型，如 image/jpeg）。任一字段缺失或者错误将会导致文件下载失败。
    
-   **Base64编码传入：**将文件转换为 Base64 编码字符串再传入。
    
-   **本地文件路径传入（仅限 DashScope SDK）：**传入本地文件的路径。
    

> 关于文件传入方式的建议，请参见[如何选择文件上传方式？](#dc4e7260aauuo)

## **应用于生产环境**

-   **图像/视频预处理：**视觉理解模型对输入的文件有大小限制，如需压缩文件请参见[图像或视频压缩方法](https://help.aliyun.com/zh/model-studio/vision#ec8e0a8e03moe)。
    
-   **处理文本文件：**视觉理解模型仅支持处理图像格式的文件，无法直接处理文本文件。但可使用以下替代方案：
    
    -   将文本文件转换为图片格式，建议使用图像处理库（如`Python`的`pdf2image`）将文件按页转换为多张高质量的图片，再使用[多图像输入](#f6256b3818huu)方式传入模型。
        
    -   [Qwen-Long](https://help.aliyun.com/zh/model-studio/long-context-qwen-long)支持处理文本文件，可用于解析文件内容。
        

-   **异步与批量处理：**对于大规模、非实时的图像或视频处理任务，推荐使用[OpenAI兼容-Batch（文件输入）](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)的方式（仅支持部分模型）。此方式以异步方式处理任务，并提供50%的成本折扣。
    
-   **容错与稳定性**
    
    -   超时处理：在非流式调用中，180 秒内模型没有结束输出通常会触发超时报错。为了提升用户体验，超时后响应体中会将已生成的内容返回。如果响应头包含`x-dashscope-partialresponse：true`，表示本次响应触发了超时。您可以使用[前缀续写](https://help.aliyun.com/zh/model-studio/partial-mode)功能（支持部分模型），将已生成的内容添加到 messages 数组并再次发出请求，使大模型继续生成内容。详情请参见：[基于不完整输出进行续写](https://help.aliyun.com/zh/model-studio/partial-mode#8cc28acfd7a91)。
        
    -   重试机制：设计合理的API调用重试逻辑（如指数退避），以应对网络波动或服务瞬时不可用的情况。
        

## **计费与限流**

-   **计费 ：**总费用根据输入和输出的总 Token 数计算；输入和输出价格可参见[模型列表](https://help.aliyun.com/zh/model-studio/models)。
    
    -   **Token 构成：**输入 Token 由文本 Token 和图像或视频转换后的 Token 组成；输出 Token 为模型生成的文本。在思考模式下，模型的思考过程也会计入输出 Token。若思考模式下未输出思考过程，按照非思考模式价格计费。
        
    -   **计算图像与视频的Token：**可通过以下代码计算图像或视频的 Token 消耗。估算结果仅供参考，实际用量以 API 响应为准。
        
        **计算图像与视频的Token**
        
        ## **图像**
        
        计算公式：`图像 Token = h_bar * w_bar / token_pixels + 2`
        
        -   `h_bar、w_bar`：缩放后的图像长宽，模型在处理图像前会进行预处理，会将图像缩小至特定像素上限内，像素上限与`max_pixels`和`vl_high_resolution_images`参数的取值有关，相关章节：[处理高分辨率图像](#e7e2db755f9h7)。
            
        -   `token_pixels`：每视觉`Token`对应的像素值，不同模型情况不同：
            
            -   `Qwen3.5`、`Qwen3-VL`、`qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-2025-08-13`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-2025-08-15``、qwen-vl-plus-2025-07-10`**：**每个`Token`对应 `32x32`像素
                
            -   `QVQ`及其他`Qwen2.5-VL`模型**：**每个Token对应`28x28`像素
                
        
        以下代码演示了模型内部对图像的大致缩放逻辑，可用于估算一张图像的Token，实际计费请以 API 响应为准。
        
        ```
        import math
        # 使用以下命令安装Pillow库：pip install Pillow
        from PIL import Image
        
        def token_calculate(image_path, max_pixels, vl_high_resolution_images):
            # 打开指定的PNG图片文件
            image = Image.open(image_path)
        
            # 获取图片的原始尺寸
            height = image.height
            width = image.width
        
            # 根据不同模型，将宽高调整为32或28的整数倍
            h_bar = round(height / 32) * 32
            w_bar = round(width / 32) * 32
        
            # 图像的Token下限：4 个 Token
            min_pixels = 4 * 32 * 32
            # 若 vl_high_resolution_images 设置为True，则输入图像Token上限为16386，对应的最大的像素值为16384 * 32 * 32 或 16384 * 28 * 28，否则为max_pixels设置的值
            if vl_high_resolution_images:
                max_pixels = 16384 * 32 * 32
            else:
                max_pixels = max_pixels
        
            # 对图像进行缩放处理，调整像素的总数在范围[min_pixels,max_pixels]内
            if h_bar * w_bar > max_pixels:
                # 计算缩放因子beta，使得缩放后的图像总像素数不超过max_pixels
                beta = math.sqrt((height * width) / max_pixels)
                # 重新计算调整后的宽高
                h_bar = math.floor(height / beta / 32) * 32
                w_bar = math.floor(width / beta / 32) * 32
            elif h_bar * w_bar < min_pixels:
                # 计算缩放因子beta，使得缩放后的图像总像素数不低于min_pixels
                beta = math.sqrt(min_pixels / (height * width))
                # 重新计算调整后的高度
                h_bar = math.ceil(height * beta / 32) * 32
                w_bar = math.ceil(width * beta / 32) * 32
            return h_bar, w_bar
        
        if __name__ == "__main__":
            # 将test.png替换为本地的图像路径
            h_bar, w_bar =  token_calculate("xxx/test.jpg", max_pixels=16384*32*32, vl_high_resolution_images=False)
            print(f"缩放后的图像尺寸为：高度为{h_bar}，宽度为{w_bar}")
            # 系统会自动添加<vision_bos>和<vision_eos>视觉标记（各计1个Token）
            token = int((h_bar * w_bar) / (32 * 32))+2
            print(f"图像的Token数为{token}")
        ```
        
        ## 视频
        
        -   **视频文件：**
            
            模型处理视频文件时，会先进行抽帧，然后计算所有视频帧的总 Token 数。由于该计算过程较为复杂，可使用以下代码，通过传入视频路径来估算视频消耗的总 Token 数：
            
            ```
            # 使用前安装：pip install opencv-python
            import math
            import os
            import logging
            import cv2
            
            logger = logging.getLogger(__name__)
            
            FRAME_FACTOR = 2
            
            # Qwen3-VL、qwen-vl-max-0813、qwen-vl-plus-0815、qwen-vl-plus-0710模型，图像缩放因子为32
            IMAGE_FACTOR = 32
            
            #  其他模型，图像缩放因子为28
            # IMAGE_FACTOR = 28
            
            # 视频帧的最大长宽比
            MAX_RATIO = 200
            # 视频帧的像素下限
            VIDEO_MIN_PIXELS = 4 * 32 * 32
            # 视频帧的像素上限，使用Qwen3-VL-Plus模型，VIDEO_MAX_PIXELS为640 * 32 * 32，其他模型为768 * 32 * 32
            VIDEO_MAX_PIXELS = 640 * 32 * 32
            
            # 用户未传入FPS参数，则fps使用默认值
            FPS = 2.0
            # 最少抽取帧数
            FPS_MIN_FRAMES = 4
            # 最大抽取帧数，使用Qwen3-VL-Plus模型，请FPS_MAX_FRAMES将设置为2000；使用Qwen3-VL-Flash和Qwen2.5-VL模型时，请设置为512，其他模型设置为80
            FPS_MAX_FRAMES = 2000
            
            # 视频输入的最大像素值，使用Qwen3-VL-Plus模型，请VIDEO_TOTAL_PIXELS将设置为131072 * 32 * 32，其他模型设置为65536 * 32 * 32
            VIDEO_TOTAL_PIXELS = int(float(os.environ.get('VIDEO_MAX_PIXELS', 131072 * 32 * 32)))
            
            def round_by_factor(number: int, factor: int) -> int:
                """返回与”number“最接近的整数，该整数可被”factor“整除。"""
                return round(number / factor) * factor
            
            def ceil_by_factor(number: int, factor: int) -> int:
                """返回大于或等于“number”且可被“factor”整除的最小整数。"""
                return math.ceil(number / factor) * factor
            
            def floor_by_factor(number: int, factor: int) -> int:
                """返回小于或等于“number”且可被“factor”整除的最大整数。"""
                return math.floor(number / factor) * factor
            
            def extract_vision_info(conversations):
                vision_infos = []
                if isinstance(conversations[0], dict):
                    conversations = [conversations]
                for conversation in conversations:
                    for message in conversation:
                        if isinstance(message["content"], list):
                            for ele in message["content"]:
                                if (
                                    "image" in ele
                                    or "image_url" in ele
                                    or "video" in ele
                                    or ele.get("type","") in ("image", "image_url", "video")
                                ):
                                    vision_infos.append(ele)
                return vision_infos
            
            def smart_nframes(ele,total_frames,video_fps):
                """用于计算抽取的视频帧数。
            
                Args:
                    ele (dict): 包含视频配置的字典格式
                        - fps: fps用于控制提取模型输入帧的数量。
                    total_frames (int): 视频的原始总帧数。
                    video_fps (int | float): 视频的原始帧率
            
                Raises:
                    nframes应该在[FRAME_FACTOR，total_frames]间隔内，否则会报错
            
                Returns:
                    用于模型输入的视频帧数。
                """
                assert not ("fps" in ele and "nframes" in ele), "Only accept either `fps` or `nframes`"
                fps = ele.get("fps", FPS)
                min_frames = ceil_by_factor(ele.get("min_frames", FPS_MIN_FRAMES), FRAME_FACTOR)
                max_frames = floor_by_factor(ele.get("max_frames", min(FPS_MAX_FRAMES, total_frames)), FRAME_FACTOR)
                duration = total_frames / video_fps if video_fps != 0 else 0
                if duration-int(duration)>(1/fps):
                    total_frames = math.ceil(duration * video_fps)
                else:
                    total_frames = math.ceil(int(duration)*video_fps)
                nframes = total_frames / video_fps * fps
                if nframes > total_frames:
                    logger.warning(f"smart_nframes: nframes[{nframes}] > total_frames[{total_frames}]")
                nframes = int(min(min(max(nframes, min_frames), max_frames), total_frames))
                if not (FRAME_FACTOR <= nframes and nframes <= total_frames):
                    raise ValueError(f"nframes should in interval [{FRAME_FACTOR}, {total_frames}], but got {nframes}.")
            
                return nframes
            
            def get_video(video_path):
                # 获取视频信息
                cap = cv2.VideoCapture(video_path)
            
                frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                # 获取视频高度
                frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
                video_fps = cap.get(cv2.CAP_PROP_FPS)
                return frame_height, frame_width, total_frames, video_fps
            
            def smart_resize(ele, path, factor=IMAGE_FACTOR):
                # 获取原视频的宽和高
                height, width, total_frames, video_fps = get_video(path)
                # 视频帧的Token下限
                min_pixels = VIDEO_MIN_PIXELS
                total_pixels = VIDEO_TOTAL_PIXELS
                # 抽取的视频帧数
                nframes = smart_nframes(ele, total_frames, video_fps)
                max_pixels = max(min(VIDEO_MAX_PIXELS, total_pixels / nframes * FRAME_FACTOR),int(min_pixels * 1.05))
            
                # 视频的长宽比不应超过200:1或1:200
                if max(height, width) / min(height, width) > MAX_RATIO:
                    raise ValueError(
                        f"absolute aspect ratio must be smaller than {MAX_RATIO}, got {max(height, width) / min(height, width)}"
                    )
            
                h_bar = max(factor, round_by_factor(height, factor))
                w_bar = max(factor, round_by_factor(width, factor))
                if h_bar * w_bar > max_pixels:
                    beta = math.sqrt((height * width) / max_pixels)
                    h_bar = floor_by_factor(height / beta, factor)
                    w_bar = floor_by_factor(width / beta, factor)
                elif h_bar * w_bar < min_pixels:
                    beta = math.sqrt(min_pixels / (height * width))
                    h_bar = ceil_by_factor(height * beta, factor)
                    w_bar = ceil_by_factor(width * beta, factor)
                return h_bar, w_bar
            
            
            def token_calculate(video_path, fps):
                # 传入视频路径和fps抽帧参数
                messages = [{"content": [{"video": video_path, "fps": fps}]}]
                vision_infos = extract_vision_info(messages)[0]
            
                resized_height, resized_width = smart_resize(vision_infos, video_path)
            
                height, width, total_frames, video_fps = get_video(video_path)
                num_frames = smart_nframes(vision_infos, total_frames, video_fps)
                print(f"原视频尺寸：{height}*{width}， 输入模型的尺寸：{resized_height}*{resized_width}，视频总帧数:{total_frames}，fps等于{fps}时，抽取的总帧数：{num_frames}", end="，")
                video_token = int(math.ceil(num_frames / 2) * resized_height / 32 * resized_width / 32)
                video_token += 2   # 系统会自动添加<|vision_bos|>和<|vision_eos|>视觉标记（各计1个Token）
                return video_token
            
            
            video_token = token_calculate("xxx/test.mp4", 1)
            print("视频tokens:", video_token)
            ```
            
        -   **图像列表：**
            
            当以图像列表形式传入视频时，表示已预先完成视频抽帧，可使用以下代码，通过传入图像的路径和数量来计算传入图像列表时消耗的Token数：
            
            ```
            # 使用前安装：pip install Pillow
            import math
            import os
            import logging
            from typing import Tuple
            from PIL import Image
            
            logger = logging.getLogger(__name__)
            
            # ==================== 常量定义 ====================
            FRAME_FACTOR = 2
            # Qwen3-VL、qwen-vl-max-0813、qwen-vl-plus-0815、qwen-vl-plus-0710模型，缩放因子为32
            IMAGE_FACTOR = 32
            
            #  其他模型，缩放因子为28
            # IMAGE_FACTOR = 28
            
            # Token计算相关常量
            TOKEN_DIVISOR = 32  # token计算时的除数
            VISION_SPECIAL_TOKENS = 2  # <|vision_bos|>和<|vision_eos|>标记
            
            # 视频帧的最大长宽比
            MAX_RATIO = 200
            # 视频帧的像素下限
            VIDEO_MIN_PIXELS = 4 * 32 * 32
            # 视频帧的像素上限，使用Qwen3-VL-Plus模型，VIDEO_MAX_PIXELS为640 * 32 * 32，其他模型为768 * 32 * 32
            VIDEO_MAX_PIXELS = 640 * 32 * 32
            
            # 视频输入的最大像素值，使用Qwen3-VL-Plus模型，请VIDEO_TOTAL_PIXELS将设置为131072 * 32 * 32，其他模型设置为65536 * 32 * 32
            VIDEO_TOTAL_PIXELS = int(float(os.environ.get('VIDEO_MAX_PIXELS', 131072 * 32 * 32)))
            
            def round_by_factor(number: int, factor: int) -> int:
                """返回与”number“最接近的整数，该整数可被”factor“整除。"""
                return round(number / factor) * factor
            
            def ceil_by_factor(number: int, factor: int) -> int:
                """返回大于或等于“number”且可被“factor”整除的最小整数。"""
                return math.ceil(number / factor) * factor
            
            def floor_by_factor(number: int, factor: int) -> int:
                """返回小于或等于“number”且可被“factor”整除的最大整数。"""
                return math.floor(number / factor) * factor
            
            
            def get_image_size(image_path: str) -> Tuple[int, int]:
                if not os.path.exists(image_path):
                    raise FileNotFoundError(f"图像文件不存在: {image_path}")
            
                try:
                    image = Image.open(image_path)
                    height = image.height
                    width = image.width
                    image.close()  # 及时关闭文件
                    return height, width
                except Exception as e:
                    raise ValueError(f"无法读取图像文件 {image_path}: {str(e)}")
            
            def smart_resize(height: int, width: int, nframes: int, factor: int = IMAGE_FACTOR) -> Tuple[int, int]:
                """
                计算图像缩放后的尺寸
            
                Args:
                    height: 原始图像高度
                    width: 原始图像宽度
                    nframes: 视频帧数
                    factor: 缩放因子，默认为IMAGE_FACTOR
            
                Returns:
                    (resized_height, resized_width) 缩放后的高度和宽度
            
                Raises:
                    ValueError: 长宽比超过限制
                """
                # 视频帧的Token下限
                min_pixels = VIDEO_MIN_PIXELS
                total_pixels = VIDEO_TOTAL_PIXELS
                # 抽取的视频帧数
                max_pixels = max(min(VIDEO_MAX_PIXELS, total_pixels / nframes * FRAME_FACTOR), int(min_pixels * 1.05))
            
                # 视频的长宽比不应超过200:1或1:200
                aspect_ratio = max(height, width) / min(height, width)
                if aspect_ratio > MAX_RATIO:
                    raise ValueError(
                        f"图像长宽比必须小于 {MAX_RATIO}:1，当前为 {aspect_ratio:.2f}:1"
                    )
            
                h_bar = max(factor, round_by_factor(height, factor))
                w_bar = max(factor, round_by_factor(width, factor))
                if h_bar * w_bar > max_pixels:
                    beta = math.sqrt((height * width) / max_pixels)
                    h_bar = floor_by_factor(height / beta, factor)
                    w_bar = floor_by_factor(width / beta, factor)
                elif h_bar * w_bar < min_pixels:
                    beta = math.sqrt(min_pixels / (height * width))
                    h_bar = ceil_by_factor(height * beta, factor)
                    w_bar = ceil_by_factor(width * beta, factor)
                return h_bar, w_bar
            
            
            def calculate_video_tokens(image_path: str, nframes: int = 1, factor: int = IMAGE_FACTOR, verbose: bool = True) -> int:
                """
            
                Args:
                    image_path: 视频帧文件路径
                    nframes: 视频帧数，
                    factor: 缩放因子，默认为IMAGE_FACTOR
                    verbose: 是否打印详细信息
            
                Returns:
                    所消耗的token数量
            
                Raises:
                    FileNotFoundError: 文件不存在
                    ValueError: 文件格式无效或长宽比超限
                """
                # 获取原始图像尺寸（只读取一次）
                height, width = get_image_size(image_path)
            
                # 计算缩放后的尺寸
                resized_height, resized_width = smart_resize(height, width, nframes, factor)
            
                # 计算token数量
                # 公式：⌈帧数/2⌉ × (高度/TOKEN_DIVISOR) × (宽度/TOKEN_DIVISOR) + VISION_SPECIAL_TOKENS
                video_token = int(
                    math.ceil(nframes / 2) *
                    (resized_height / TOKEN_DIVISOR) *
                    (resized_width / TOKEN_DIVISOR)
                )
                # 添加视觉标记token（<|vision_bos|>和<|vision_eos|>）
                video_token += VISION_SPECIAL_TOKENS
            
                if verbose:
                    print(f"原视频帧尺寸：{height}×{width}，输入模型的尺寸：{resized_height}×{resized_width}，", end="")
            
                return video_token
            
            if __name__ == "__main__":
                try:
                    video_token = calculate_image_tokens("xxx/test.jpg", nframes=30)
                    print(f"视频tokens: {video_token}\n")
                except Exception as e:
                    print(f"错误: {str(e)}\n")
            ```
            
        

-   **查看账单：**您可以在阿里云控制台的[费用与成本](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面查看账单或进行充值。
    
-   **限流：**视觉理解模型的限流条件参见[限流](https://help.aliyun.com/zh/model-studio/rate-limit)。
    
-   **免费额度****（仅北京地域）**：从开通百炼或模型申请通过之日起计算有效期，有效期 90 天内，视觉理解模型提供 100 万 Token 的免费额度。
    

## API参考

关于视觉理解模型的输入输出参数，请参见[千问](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)。

## **常见问题**

### **如何选择文件上传方式？**

推荐综合考虑SDK 类型、文件大小以及网络稳定性来选择最合适的上传方式。

| **文件类型** | **文件规格** | **DashScope SDK（Python、Java）** | **OpenAI 兼容 / DashScope HTTP** |
| --- | --- | --- | --- |
| 图像  | 大于 7MB 小于 10MB | 传入本地路径 | 仅支持公网 URL，建议使用[阿里云对象存储服务](https://www.aliyun.com/product/oss) |
| 小于 7MB | 传入本地路径 | Base64 编码 |
| 视频  | 大于 100 MB | 仅支持公网 URL，建议使用[阿里云对象存储服务](https://www.aliyun.com/product/oss) | 仅支持公网 URL，建议使用[阿里云对象存储服务](https://www.aliyun.com/product/oss) |
| 大于 7MB 小于 100 MB | 传入本地路径 | 仅支持公网 URL，建议使用[阿里云对象存储服务](https://www.aliyun.com/product/oss) |
| 小于 7MB | 传入本地路径 | Base64 编码 |

> Base64 编码会增大数据体积，原始文件大小应小于 7 MB。

> 使用 Base64 或本地路径可避免服务端下载超时，提升稳定性。

### **如何将图像或视频压缩到满足要求的大小？**

视觉理解模型对输入的文件有大小限制，可通过以下方法压缩。

**图像压缩方法**

-   在线工具：使用 [CompressJPEG](https://compressjpeg.com/zh/) 等在线工具进行压缩。
    
-   本地软件：使用 Photoshop 等软件，在导出时调整质量。
    
-   代码实现：
    
    ```
    # pip install pillow
    
    from PIL import Image
    def compress_image(input_path, output_path, quality=85):
        with Image.open(input_path) as img:
            img.save(output_path, "JPEG", optimize=True, quality=quality)
    
    # 传入本地图像
    compress_image("/xxx/before-large.jpeg","/xxx/after-min.jpeg")
    ```
    

**视频压缩方法**

-   在线工具：使用 [FreeConvert](https://www.freeconvert.com/zh) 等在线工具进行压缩。
    
-   本地软件：使用 [HandBrake](https://handbrake.fr/) 等软件。
    
-   代码实现：使用FFmpeg工具，更多用法请参见[FFmpeg官网](https://ffmpeg.org/download.html)。
    
    ```
    # 基础转换命令
    # -i，作用：输入文件路径，常用值示例：input.mp4
    # -vcodec，作用 视频编码器 ，一般取值有libx264（通用推荐）、libx265（压缩率更高）、
    # -crf，作用：控制视频质量，取值范围：[18-28]，数值越小，质量越高，文件体积越大。
    # --preset，作用：控制编码速度与压缩效率的平衡。一般取值有 slow、fast、faster
    # -y，作用：覆盖已存在文件(无需赋值)
    # output.mp4，作用：输出文件路径
    
    ffmpeg -i input.mp4 -vcodec libx264 -crf 28 -preset slow output.mp4
    ```
    

### **模型输出物体定位的结果后，如何将检测框绘制到原图上？**

视觉理解模型输出物体定位效果后，可参照以下代码将检测框及其标签信息绘制到原图上。

-   Qwen2.5-VL：返回的坐标相对于缩放后的图像左上角的绝对值，单位为像素。可参见[qwen2\_5\_vl\_2d.py](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/xldjey/qwen2_5-vl-2d.py)代码绘制检测框。
    
-   Qwen3-VL：返回的坐标为相对坐标，坐标值会归一化到`[0, 999]`。可参见[qwen3\_vl\_2d.py](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/eamyrc/qwen3-vl-2d.py)（二维定位）或[qwen3\_vl\_3d.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/uukdlq/qwen3_vl_3d.zip)（三维定位）中的代码绘制检测框。
    

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

通义千问 API 是无状态的，不会保存对话历史。要实现多轮对话，需在每次请求中显式传入历史对话消息，并可结合截断、摘要、召回等策略，高效管理上下文，减少 Token 消耗。

> 本文介绍如何通过 OpenAI 兼容的 Chat Completion 接口或 DashScope 接口实现多轮对话。 Responses API 可更便捷地实现多轮对话，参见：[OpenAI兼容-Responses](https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api)。

## **工作原理**

实现多轮对话的核心是维护一个 `messages` 数组。每一轮对话都需要将用户的最新提问和模型的回复追加到此数组中，并将其作为下一次请求的输入。

以下示例为多轮对话时 `messages` 的状态变化：

1.  **第一轮对话**
    
    向`messages` 数组添加用户问题。
    
    ```
    // 使用文本模型
    [
        {"role": "user", "content": "推荐一部关于太空探索的科幻电影。"}
    ]
    
    // 使用多模态模型，以 Qwen-VL 为例
    // {"role": "user",
    //       "content": [{"type": "image_url","image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"}},
    //                   {"type": "text", "text": "请问图片展现了有哪些商品？"}]
    // }
    ```
    
2.  **第二轮对话**
    
    向`messages`数组添加大模型回复内容与用户的最新提问。
    
    ```
    // 使用文本模型
    [
        {"role": "user", "content": "推荐一部关于太空探索的科幻电影。"},
        {"role": "assistant", "content": "我推荐《xxx》，这是一部经典的科幻作品。"},
        {"role": "user", "content": "这部电影的导演是谁？"}
    ]
    
    // 使用多模态模型，以 Qwen-VL 为例
    //[
    //    {"role": "user", "content": [
    //                    {"type": "image_url","image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"}},
    //                   {"type": "text", "text": "请问图片展现了有哪些商品？"}]},
    //    {"role": "assistant", "content": "图片展示了三件商品：一件浅蓝色背带裤、一件蓝白条纹短袖衬衫和一双白色运动鞋。"},
    //    {"role": "user", "content": "它们属于什么风格？"}
    //]
    ```
    

## **快速开始**

## OpenAI兼容

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def get_response(messages):
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=messages
    )
    return completion.choices[0].message.content

# 初始化 messages
messages = []

# 第 1 轮
messages.append({"role": "user", "content": "推荐一部关于太空探索的科幻电影。"})
print("第1轮")
print(f"用户：{messages[0]['content']}")
assistant_output = get_response(messages)
messages.append({"role": "assistant", "content": assistant_output})
print(f"模型：{assistant_output}\n")

# 第 2 轮
messages.append({"role": "user", "content": "这部电影的导演是谁？"})
print("第2轮")
print(f"用户：{messages[-1]['content']}")
assistant_output = get_response(messages)
messages.append({"role": "assistant", "content": assistant_output})
print(f"模型：{assistant_output}\n")
```

## Node.js

```
import OpenAI from "openai";

// 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
const BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1";
// 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
const openai = new OpenAI({
  // 若没有配置环境变量，请将下行替换为：apiKey:"sk-xxx",
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL: BASE_URL,
});

async function getResponse(messages) {
  const completion = await openai.chat.completions.create({
    model: "qwen-plus",
    messages: messages,
  });
  return completion.choices[0].message.content;
}

async function runConversation() {
  const messages = [];

  // 第 1 轮
  messages.push({ role: "user", content: "推荐一部关于太空探索的科幻电影。" });
  console.log("第1轮");
  console.log("用户：" + messages[0].content);

  let assistant_output = await getResponse(messages);
  messages.push({ role: "assistant", content: assistant_output });
  console.log("模型：" + assistant_output + "\n");

  // 第 2 轮
  messages.push({ role: "user", content: "这部电影的导演是谁？" });
  console.log("第2轮");
  console.log("用户：" + messages[messages.length - 1].content);

  assistant_output = await getResponse(messages);
  messages.push({ role: "assistant", content: assistant_output });
  console.log("模型：" + assistant_output + "\n");
}

runConversation();
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages":[      
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "你好"
        },
        {
            "role": "assistant",
            "content": "你好啊，我是通义千问。"
        },
        {
            "role": "user",
            "content": "你有哪些技能？"
        }
    ]
}'
```

## DashScope

## Python

示例代码以手机商店导购为例，导购与顾客会进行多轮对话来采集购买意向，采集完成后会结束会话。

```
import os
from dashscope import Generation
import dashscope 
# 若使用新加坡地域的模型，请释放下列注释
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

def get_response(messages):
    response = Generation.call(
        # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        model="qwen-plus",
        messages=messages,
        result_format="message",
    )
    return response

# 初始化一个 messages 数组
messages = [
    {
        "role": "system",
        "content": """你是一名阿里云百炼手机商店的店员，你负责给用户推荐手机。手机有两个参数：屏幕尺寸（包括6.1英寸、6.5英寸、6.7英寸）、分辨率（包括2K、4K）。
        你一次只能向用户提问一个参数。如果用户提供的信息不全，你需要反问他，让他提供没有提供的参数。如果参数收集完成，你要说：我已了解您的购买意向，请稍等。""",
    }
]

assistant_output = "欢迎光临阿里云百炼手机商店，您需要购买什么尺寸的手机呢？"
print(f"模型输出：{assistant_output}\n")
while "我已了解您的购买意向" not in assistant_output:
    user_input = input("请输入：")
    # 将用户问题信息添加到messages列表中
    messages.append({"role": "user", "content": user_input})
    assistant_output = get_response(messages).output.choices[0].message.content
    # 将大模型的回复信息添加到messages列表中
    messages.append({"role": "assistant", "content": assistant_output})
    print(f"模型输出：{assistant_output}")
    print("\n")
```

## Java

```
import java.util.ArrayList;
import java.util.List;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import java.util.Scanner;
import com.alibaba.dashscope.utils.Constants;


public class Main {
    // 若使用新加坡地域的模型，请释放下列注释
    // static {
    //     Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";
    // }
    public static GenerationParam createGenerationParam(List<Message> messages) {
        return GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model("qwen-plus")
                .messages(messages)
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .build();
    }
    public static GenerationResult callGenerationWithMessages(GenerationParam param) throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        return gen.call(param);
    }
    public static void main(String[] args) {
        try {
            List<Message> messages = new ArrayList<>();
            messages.add(createMessage(Role.SYSTEM, "You are a helpful assistant."));
            for (int i = 0; i < 3;i++) {
                Scanner scanner = new Scanner(System.in);
                System.out.print("请输入：");
                String userInput = scanner.nextLine();
                if ("exit".equalsIgnoreCase(userInput)) {
                    break;
                }
                messages.add(createMessage(Role.USER, userInput));
                GenerationParam param = createGenerationParam(messages);
                GenerationResult result = callGenerationWithMessages(param);
                System.out.println("模型输出："+result.getOutput().getChoices().get(0).getMessage().getContent());
                messages.add(result.getOutput().getChoices().get(0).getMessage());
            }
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            e.printStackTrace();
        }
        System.exit(0);
    }
    private static Message createMessage(Role role, String content) {
        return Message.builder().role(role.getValue()).content(content).build();
    }
}
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将base_url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "input":{
        "messages":[      
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "你好"
            },
            {
                "role": "assistant",
                "content": "你好啊，我是通义千问。"
            },
            {
                "role": "user",
                "content": "你有哪些技能？"
            }
        ]
    }
}'
```

## **多模态模型的多轮对话**

**说明**

-   本章节适用于Qwen-VL、Kimi-K2.5、Qwen-Audio、GUI-Plus模型，`Qwen-Omni`具体实现方法请参见[全模态](https://help.aliyun.com/zh/model-studio/qwen-omni)。
    
-   Qwen-VL-OCR、Qwen3-Omni-Captioner是为特定单轮任务设计的模型，不支持多轮对话。
    

多模态模型支持在对话中加入图片、音频等内容，其多轮对话的实现方式与文本模型主要有以下不同：

-   **用户消息（user message）的构造方式**：多模态模型的用户消息不仅包含文本，还包含图片、音频等多模态信息。
    
-   **DashScope SDK接口：**使用 DashScope Python SDK 时，需调用 `MultiModalConversation` 接口；使用DashScope Java SDK 时，需调用 `MultiModalConversation` 类。
    

## OpenAI兼容

## Python

```
from openai import OpenAI
import os

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx" 
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
messages = [
        {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"
                },
            },
            {"type": "text", "text": "请问图片展现了有哪些商品？"},
        ],
    }
]

completion = client.chat.completions.create(
    model="qwen3-vl-plus",  # 可按需更换为其它多模态模型，并修改相应的 messages
    messages=messages,
    )
    
print(f"第一轮输出：{completion.choices[0].message.content}")

assistant_message = completion.choices[0].message
messages.append(assistant_message.model_dump())
messages.append({
        "role": "user",
        "content": [
        {
            "type": "text",
            "text": "它们属于什么风格？"
        }
        ]
    })
completion = client.chat.completions.create(
    model="qwen3-vl-plus",
    messages=messages,
    )
    
print(f"第二轮输出：{completion.choices[0].message.content}")
```

## Node.js

```
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
       // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

let messages = [
    {
        role: "user",
	content: [
        { type: "image_url", image_url: { "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png" } },
        { type: "text", text: "请问图片展现了有哪些商品？" },
    ]
}]
async function main() {
    let response = await openai.chat.completions.create({
        model: "qwen3-vl-plus",  // 可按需更换为其它多模态模型，并修改相应的 messages
        messages: messages
    });
    console.log(`第一轮输出：${response.choices[0].message.content}`);
    messages.push(response.choices[0].message);
    messages.push({"role": "user", "content": "它们属于什么风格？"});
    response = await openai.chat.completions.create({
        model: "qwen3-vl-plus",
        messages: messages
    });
    console.log(`第二轮输出：${response.choices[0].message.content}`);
}

main()
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen3-vl-plus",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"
          }
        },
        {
          "type": "text",
          "text": "请问图片展现了有哪些商品？"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "图片展示了三件商品：一件浅蓝色背带裤、一件蓝白条纹短袖衬衫和一双白色运动鞋。"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "它们属于什么风格？"
        }
      ]
    }
  ]
}'
```

## DashScope

## Python

```
import os
import dashscope 
from dashscope import MultiModalConversation

# 若使用新加坡地域的模型，请取消下列注释
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {
                "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"
            },
            {"text": "请问图片展现了有哪些商品？"},
        ],
    }
]
response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3-vl-plus',   # 可按需更换为其它多模态模型，并修改相应的 messages
    messages=messages)
print(f"模型第一轮输出：{response.output.choices[0].message.content[0]['text']}")

messages.append(response['output']['choices'][0]['message'])
user_msg = {"role": "user", "content": [{"text": "它们属于什么风格？"}]}
messages.append(user_msg)
response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3-vl-plus',
    messages=messages)
    
print(f"模型第二轮输出：{response.output.choices[0].message.content[0]['text']}")
```

## Java

```
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 若使用新加坡地域的模型，请取消下列注释
   // static {Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";}
   
    private static final String modelName = "qwen3-vl-plus";  // 可按需更换为其它多模态模型，并修改相应的 messages
    public static void MultiRoundConversationCall() throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"),
                        Collections.singletonMap("text", "请问图片展现了有哪些商品？"))).build();
        List<MultiModalMessage> messages = new ArrayList<>();
        messages.add(userMessage);
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))                
                .model(modelName)
                .messages(messages)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println("第一轮输出："+result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));        // add the result to conversation
        messages.add(result.getOutput().getChoices().get(0).getMessage());
        MultiModalMessage msg = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", "它们属于什么风格？"))).build();
        messages.add(msg);
        param.setMessages((List)messages);
        result = conv.call(param);
        System.out.println("第二轮输出："+result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));    }

    public static void main(String[] args) {
        try {
            MultiRoundConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3-vl-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"},
                    {"text": "请问图片展现了有哪些商品？"}
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {"text": "图片展示了三件商品：一件浅蓝色背带裤、一件蓝白条纹短袖衬衫和一双白色运动鞋。"}
                ]
            },
            {
                "role": "user",
                "content": [
                    {"text": "它们属于什么风格？"}
                ]
            }
        ]
    }
}'
```

## **思考模型的多轮对话**

思考模型返回`reasoning_content`（思考过程）与`content`（回复内容）两个字段。更新 messages 数组时，仅保留`content`字段，忽略`reasoning_content`字段。

```
[
    {"role": "user", "content": "推荐一部关于太空探索的科幻电影。"},
    {"role": "assistant", "content": "我推荐《xxx》，这是一部经典的科幻作品。"}, # 添加上下文时请勿添加reasoning_content字段
    {"role": "user", "content": "这部电影的导演是谁？"}
]
```

> 思考模型详情参见：[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)、[视觉理解](https://help.aliyun.com/zh/model-studio/vision)、[视觉推理](https://help.aliyun.com/zh/model-studio/visual-reasoning)。

> Qwen3-Omni-Flash（思考模式）实现多轮对话请参见[全模态](https://help.aliyun.com/zh/model-studio/qwen-omni#76b04b353ds7i)。

## OpenAI兼容

## Python

### **示例代码**

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key = os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

messages = []
conversation_idx = 1
while True:
    reasoning_content = ""  # 定义完整思考过程
    answer_content = ""     # 定义完整回复
    is_answering = False   # 判断是否结束思考过程并开始回复
    print("="*20+f"第{conversation_idx}轮对话"+"="*20)
    conversation_idx += 1
    user_msg = {"role": "user", "content": input("请输入你的消息：")}
    messages.append(user_msg)
    # 创建聊天完成请求
    completion = client.chat.completions.create(
        # 您可以按需更换为其它深度思考模型
        model="qwen-plus",
        messages=messages,
        extra_body={"enable_thinking": True},
        stream=True,
        # stream_options={
        #     "include_usage": True
        # }
    )
    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
    for chunk in completion:
        # 如果chunk.choices为空，则打印usage
        if not chunk.choices:
            print("\nUsage:")
            print(chunk.usage)
        else:
            delta = chunk.choices[0].delta
            # 打印思考过程
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
                print(delta.reasoning_content, end='', flush=True)
                reasoning_content += delta.reasoning_content
            else:
                # 开始回复
                if delta.content != "" and is_answering is False:
                    print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                    is_answering = True
                # 打印回复过程
                print(delta.content, end='', flush=True)
                answer_content += delta.content
    # 将模型回复的content添加到上下文中
    messages.append({"role": "assistant", "content": answer_content})
    print("\n")
```

## Node.js

### **示例代码**

```
import OpenAI from "openai";
import process from 'process';
import readline from 'readline/promises';

// 初始化 readline 接口
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// 初始化 openai 客户端
const openai = new OpenAI({
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY, // 从环境变量读取
    // 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;
let messages = [];
let conversationIdx = 1;

async function main() {
    while (true) {
        console.log("=".repeat(20) + `第${conversationIdx}轮对话` + "=".repeat(20));
        conversationIdx++;
        
        // 读取用户输入
        const userInput = await rl.question("请输入你的消息：");
        messages.push({ role: 'user', content: userInput });

        // 重置状态
        reasoningContent = '';
        answerContent = '';
        isAnswering = false;

        try {
            const stream = await openai.chat.completions.create({
                // 您可以按需更换为其它深度思考模型
                model: 'qwen-plus',
                messages: messages,
                enable_thinking: true,
                stream: true,
                // stream_options:{
                //     include_usage: true
                // }
            });

            console.log("\n" + "=".repeat(20) + "思考过程" + "=".repeat(20) + "\n");

            for await (const chunk of stream) {
                if (!chunk.choices?.length) {
                    console.log('\nUsage:');
                    console.log(chunk.usage);
                    continue;
                }

                const delta = chunk.choices[0].delta;
                
                // 处理思考过程
                if (delta.reasoning_content) {
                    process.stdout.write(delta.reasoning_content);
                    reasoningContent += delta.reasoning_content;
                }
                
                // 处理正式回复
                if (delta.content) {
                    if (!isAnswering) {
                        console.log('\n' + "=".repeat(20) + "完整回复" + "=".repeat(20) + "\n");
                        isAnswering = true;
                    }
                    process.stdout.write(delta.content);
                    answerContent += delta.content;
                }
            }
            
            // 将完整回复加入消息历史
            messages.push({ role: 'assistant', content: answerContent });
            console.log("\n");
            
        } catch (error) {
            console.error('Error:', error);
        }
    }
}

// 启动程序
main().catch(console.error);
```

## HTTP

### **示例代码**

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "user", 
            "content": "你好"
        },
        {
            "role": "assistant",
            "content": "你好！很高兴见到你，有什么我可以帮忙的吗？"
        },
        {
            "role": "user",
            "content": "你是谁？"
        }
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    },
    "enable_thinking": true
}'
```

## DashScope

## Python

### **示例代码**

```
import os
import dashscope

# 若使用新加坡地域的模型，请释放下列注释
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

messages = []
conversation_idx = 1
while True:
    print("=" * 20 + f"第{conversation_idx}轮对话" + "=" * 20)
    conversation_idx += 1
    user_msg = {"role": "user", "content": input("请输入你的消息：")}
    messages.append(user_msg)
    response = dashscope.Generation.call(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv('DASHSCOPE_API_KEY'),
         # 此处以qwen-plus为例，可按需更换为其它深度思考模型
        model="qwen-plus", 
        messages=messages,
        enable_thinking=True,
        result_format="message",
        stream=True,
        incremental_output=True
    )
    # 定义完整思考过程
    reasoning_content = ""
    # 定义完整回复
    answer_content = ""
    # 判断是否结束思考过程并开始回复
    is_answering = False
    print("=" * 20 + "思考过程" + "=" * 20)
    for chunk in response:
        # 如果思考过程与回复皆为空，则忽略
        if (chunk.output.choices[0].message.content == "" and 
            chunk.output.choices[0].message.reasoning_content == ""):
            pass
        else:
            # 如果当前为思考过程
            if (chunk.output.choices[0].message.reasoning_content != "" and 
                chunk.output.choices[0].message.content == ""):
                print(chunk.output.choices[0].message.reasoning_content, end="",flush=True)
                reasoning_content += chunk.output.choices[0].message.reasoning_content
            # 如果当前为回复
            elif chunk.output.choices[0].message.content != "":
                if not is_answering:
                    print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                    is_answering = True
                print(chunk.output.choices[0].message.content, end="",flush=True)
                answer_content += chunk.output.choices[0].message.content
    # 将模型回复的content添加到上下文中
    messages.append({"role": "assistant", "content": answer_content})
    print("\n")
    # 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
    # print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
    # print(f"{reasoning_content}")
    # print("=" * 20 + "完整回复" + "=" * 20 + "\n")
    # print(f"{answer_content}")
```

## Java

### **示例代码**

```
// dashscope SDK的版本 >= 2.19.4
import java.util.Arrays;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;
import java.lang.System;
import java.util.List;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;
    // 若使用新加坡地域的模型，请释放下列注释
    // static {Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";}
    private static void handleGenerationResult(GenerationResult message) {
        if (message != null && message.getOutput() != null 
            && message.getOutput().getChoices() != null 
            && !message.getOutput().getChoices().isEmpty() 
            && message.getOutput().getChoices().get(0) != null
            && message.getOutput().getChoices().get(0).getMessage() != null) {
            
            String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
            String content = message.getOutput().getChoices().get(0).getMessage().getContent();
            
            if (reasoning != null && !reasoning.isEmpty()) {
                reasoningContent.append(reasoning);
                if (isFirstPrint) {
                    System.out.println("====================思考过程====================");
                    isFirstPrint = false;
                }
                System.out.print(reasoning);
            }

            if (content != null && !content.isEmpty()) {
                finalContent.append(content);
                if (!isFirstPrint) {
                    System.out.println("\n====================完整回复====================");
                    isFirstPrint = true;
                }
                System.out.print(content);
            }
        }
    }
    
    private static GenerationParam buildGenerationParam(List<Message> messages) {
        return GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以 qwen-plus 为例，可按需更换模型名称
                .model("qwen-plus")
                .enableThinking(true)
                .messages(messages)
                .incrementalOutput(true)
                .resultFormat("message")
                .build();
    }
    
    public static void streamCallWithMessage(Generation gen, List<Message> messages)
            throws NoApiKeyException, ApiException, InputRequiredException {
        GenerationParam param = buildGenerationParam(messages);
        Flowable<GenerationResult> result = gen.streamCall(param);
        result.doOnError(throwable -> logger.error("Error occurred in stream processing: {}", throwable.getMessage(), throwable))
              .blockingForEach(Main::handleGenerationResult);
    }

    public static void main(String[] args) {
        try {
            Generation gen = new Generation();
            Message userMsg1 = Message.builder()
                    .role(Role.USER.getValue())
                    .content("你好")
                    .build();
            Message assistantMsg = Message.builder()
                    .role(Role.ASSISTANT.getValue())
                    .content("你好！很高兴见到你，有什么我可以帮忙的吗？")
                    .build();
            Message userMsg2 = Message.builder()
                    .role(Role.USER.getValue())
                    .content("你是谁")
                    .build();
            List<Message> messages = Arrays.asList(userMsg1, assistantMsg, userMsg2);
            streamCallWithMessage(gen, messages);
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            logger.error("An exception occurred: {}", e.getMessage(), e);
        } catch (Exception e) {
            logger.error("Unexpected error occurred: {}", e.getMessage(), e);
        } finally {
            // 确保程序正常退出
            System.exit(0);
        }
    }
}
```

## HTTP

### **示例代码**

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将base_url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
# === 执行时请删除该注释 ===
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen-plus",
    "input":{
        "messages":[      
            {
                "role": "user",
                "content": "你好"
            },
            {
                "role": "assistant",
                "content": "你好！很高兴见到你，有什么我可以帮忙的吗？"
            },
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    },
    "parameters":{
        "enable_thinking": true,
        "incremental_output": true,
        "result_format": "message"
    }
}'
```

## **应用于生产环境**

多轮对话会带来巨大的 Token 消耗，且容易超出大模型上下文最大长度导致报错。以下策略可帮助您有效管理上下文与控制成本。

### **1\. 上下文管理**

`messages` 数组会随对话轮次增加而变长，最终可能超出模型的 Token 限制。建议参考以下内容，在对话过程中管理上下文长度。

#### **1.1. 上下文截断**

当对话历史过长时，保留最近的 N 轮对话历史。该方式实现简单，但会丢失较早的对话信息。

#### **1.2. 滚动摘要**

为了在不丢失核心信息的前提下动态压缩对话历史，控制上下文长度，可随着对话的进行对上下文进行摘要：

a. 对话历史达到一定长度（如上下文长度最大值的 70%）时，将对话历史中较早的部分（如前一半）提取出来，发起独立 API 调用使大模型对这部分内容生成“记忆摘要”；

b. 构建下一次请求时，用“记忆摘要”替换冗长的对话历史，并拼接最近的几轮对话。

#### **1.3. 向量化召回**

滚动摘要会丢失部分信息，为了使模型可以从海量对话历史中“回忆”起相关信息，可将对话管理从“线性传递”转变为“按需检索”：

a. 每轮对话结束后，将该轮对话存入向量数据库；

b. 用户提问时，通过相似度检索相关对话记录；

c. 将检索到的对话记录与最近的用户输入拼接后输入大模型。  

### **2\. 成本控制**

输入 Token 数会随着对话轮数增加，显著增加使用成本，以下成本管理策略供您参考。

#### **2.1. 减少输入 Token**

通过上文介绍的上下文管理策略减少输入 Token，降低成本。

#### **2.2. 使用支持上下文缓存的模型**

发起多轮对话请求时，`messages` 部分会重复计算并计费。阿里云百炼对`qwen-max`、`qwen-plus`等模型提供了[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)功能，可以降低使用成本并提升响应速度，建议优先使用支持上下文缓存的模型。

> 上下文缓存功能自动开启，无需修改代码。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
在实时聊天或长文本生成应用中，长时间的等待会损害用户体验并可能导致触发服务端超时，导致任务失败。流式输出通过持续返回模型生成的文本片段，解决了这两个核心问题。

## **工作原理**

流式输出基于 Server-Sent Events (SSE) 协议。发起流式请求后，服务端与客户端建立持久化 HTTP 连接。模型每生成一个文本块（称为 chunk），立即通过连接推送。全部内容生成后，服务端发送结束信号。

客户端监听事件流，实时接收并处理文本块，例如逐字渲染界面。这与非流式调用（一次性返回所有内容）形成对比。

你是谁

![](https://assets.alicdn.com/g/qwenweb/qwen-webui-fe/0.0.54/static/favicon.png  )

|

![](https://assets.alicdn.com/g/qwenweb/qwen-webui-fe/0.0.54/static/favicon.png  )

等待中...

我是通义千问，由阿里云开发的AI助手。我可以回答各种问题、提供信息和与用户进行对话。有什么我可以帮助你的吗？

⏱️ 等待时间：3 秒

已关闭流式输出

@keyframes blink-cursor { from, to { opacity: 0 } 50% { opacity: 1 } } @keyframes blink { 0% { opacity: 1 } 50% { opacity: 0.3 } 100% { opacity: 1 } } @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } } .toggle-btn { background: #E0E0E0 !important; } .toggle-btn:disabled { opacity: 0.6; cursor: not-allowed; } .toggle-btn.active { background: #4F76E3 !important; } .toggle-btn.active:disabled { background: #90CAF9 !important; } .toggle-btn.active .slider { transform: translateX(26px); } .send-button:hover { transform: scale(1.05); box-shadow: 0 2px 8px rgba(79, 118, 227, 0.3); } .send-button:disabled { opacity: 0.7; cursor: not-allowed; transform: none; box-shadow: none; } .question-input:focus { border-color: #4F76E3; outline: none; background-color: #e9f5ff; }

> 以上组件仅供您参考，并未真实发送请求。

## **计费说明**

流式输出计费规则与非流式调用完全相同，根据请求的输入Token数和输出Token数计费。

请求中断时，输出 Token 仅计算服务端收到终止请求前已生成的部分。

## **如何使用**

**重要**

Qwen3 开源版、QwQ 商业版与开源版、QVQ 、Qwen-Omni等模型仅支持流式输出方式调用。

### **步骤一：配置 API Key 并选择地域**

需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

> 将API Key配置为环境变量（`DASHSCOPE_API_KEY`）比在代码中硬编码更安全。

### **步骤二：发起流式请求**

## OpenAI兼容

-   **如何开启**
    
    设置 `stream` 为 `true` 即可。
    
-   **查看 Token 消耗**
    
    OpenAI 协议默认不返回 Token 消耗量，需设置`stream_options={"include_usage": true}`，使**最后一个返回的数据块**包含Token消耗信息。
    

## Python

```
import os
from openai import OpenAI

# 1. 准备工作：初始化客户端
client = OpenAI(
    # 建议通过环境变量配置API Key，避免硬编码。
    api_key=os.environ["DASHSCOPE_API_KEY"],
    # API Key与地域强绑定，请确保base_url与API Key的地域一致。
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 2. 发起流式请求
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "请介绍一下自己"}
    ],
    stream=True,
    stream_options={"include_usage": True}
)

# 3. 处理流式响应
# 用列表暂存响应片段，最后 join 比逐次 += 字符串更高效
content_parts = []
print("AI: ", end="", flush=True)

for chunk in completion:
    if chunk.choices:
        content = chunk.choices[0].delta.content or ""
        print(content, end="", flush=True)
        content_parts.append(content)
    elif chunk.usage:
        print("\n--- 请求用量 ---")
        print(f"输入 Tokens: {chunk.usage.prompt_tokens}")
        print(f"输出 Tokens: {chunk.usage.completion_tokens}")
        print(f"总计 Tokens: {chunk.usage.total_tokens}")

full_response = "".join(content_parts)
# print(f"\n--- 完整回复 ---\n{full_response}")
```

### **返回结果**

```
AI: 你好！我是Qwen，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。如果你有任何问题或需要帮助，欢迎随时告诉我！
--- 请求用量 ---
输入 Tokens: 26
输出 Tokens: 87
总计 Tokens: 113
```

## Node.js

```
import OpenAI from "openai";

async function main() {
    // 1. 准备工作：初始化客户端
    // 建议通过环境变量配置API Key，避免硬编码。
    if (!process.env.DASHSCOPE_API_KEY) {
        throw new Error("请设置环境变量 DASHSCOPE_API_KEY");
    }
    const client = new OpenAI({
        // 若没有配置环境变量，请将下行替换为：apiKey:"sk-xxx",
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    });

    try {
        // 2. 发起流式请求
        const stream = await client.chat.completions.create({
            model: "qwen-plus",
            messages: [
                { role: "system", content: "You are a helpful assistant." },
                { role: "user", content: "请介绍一下自己" },
            ],
            stream: true,
            // 目的：在最后一个chunk中获取本次请求的Token用量。
            stream_options: { include_usage: true },
        });

        // 3. 处理流式响应
        const contentParts = [];
        process.stdout.write("AI: ");
        
        for await (const chunk of stream) {
            // 最后一个chunk不包含choices，但包含usage信息。
            if (chunk.choices && chunk.choices.length > 0) {
                const content = chunk.choices[0]?.delta?.content || "";
                process.stdout.write(content);
                contentParts.push(content);
            } else if (chunk.usage) {
                // 请求结束，打印Token用量。
                console.log("\n--- 请求用量 ---");
                console.log(`输入 Tokens: ${chunk.usage.prompt_tokens}`);
                console.log(`输出 Tokens: ${chunk.usage.completion_tokens}`);
                console.log(`总计 Tokens: ${chunk.usage.total_tokens}`);
            }
        }
        
        const fullResponse = contentParts.join("");
        // console.log(`\n--- 完整回复 ---\n${fullResponse}`);

    } catch (error) {
        console.error("请求失败:", error);
    }
}

main();
```

### **返回结果**

```
AI: 你好！我是Qwen，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。如果你有任何问题或需要帮助，欢迎随时向我提问！
--- 请求用量 ---
输入 Tokens: 26
输出 Tokens: 89
总计 Tokens: 115
```

## curl

### **请求**

```
# ======= 重要提示 =======
# 确保已设置环境变量 DASHSCOPE_API_KEY
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
--no-buffer \
-d '{
    "model": "qwen-plus",
    "messages": [
        {"role": "user", "content": "你是谁？"}
    ],
    "stream": true,
    "stream_options": {"include_usage": true}
}'
```

### **响应**

返回数据为符合 SSE 协议的流式响应。每一行 `data:` 都代表一个数据块。

```
data: {"choices":[{"delta":{"content":"","role":"assistant"},"index":0,"logprobs":null,"finish_reason":null}],"object":"chat.completion.chunk","usage":null,"created":1726132850,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-428b414f-fdd4-94c6-b179-8f576ad653a8"}

data: {"choices":[{"finish_reason":null,"delta":{"content":"我是"},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1726132850,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-428b414f-fdd4-94c6-b179-8f576ad653a8"}

data: {"choices":[{"delta":{"content":"来自"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1726132850,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-428b414f-fdd4-94c6-b179-8f576ad653a8"}

data: {"choices":[{"delta":{"content":"阿里"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1726132850,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-428b414f-fdd4-94c6-b179-8f576ad653a8"}

data: {"choices":[{"delta":{"content":"云的超大规模语言"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1726132850,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-428b414f-fdd4-94c6-b179-8f576ad653a8"}

data: {"choices":[{"delta":{"content":"模型，我叫通义千问"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1726132850,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-428b414f-fdd4-94c6-b179-8f576ad653a8"}

data: {"choices":[{"delta":{"content":"。"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1726132850,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-428b414f-fdd4-94c6-b179-8f576ad653a8"}

data: {"choices":[{"finish_reason":"stop","delta":{"content":""},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1726132850,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-428b414f-fdd4-94c6-b179-8f576ad653a8"}

data: {"choices":[],"object":"chat.completion.chunk","usage":{"prompt_tokens":22,"completion_tokens":17,"total_tokens":39},"created":1726132850,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-428b414f-fdd4-94c6-b179-8f576ad653a8"}

data: [DONE]
```

-   `data:`: 消息的数据负载，通常是一个JSON字符串。
    
-   `[DONE]`: 表示整个流式响应已结束。
    

## DashScope

-   **如何开启**
    
    根据使用方式（Python SDK、Java SDK、cURL）不同，开启流式输出的方式不同：
    
    -   Python SDK：设置 `stream` 参数为 `True`；
        
    -   Java SDK：通过`streamCall`接口调用；
        
    -   cURL：设置 Header 参数`X-DashScope-SSE`为`enable`。
        
-   **是否启动增量输出**
    
    DashScope 协议支持增量与非增量式流式输出：
    
    -   **增量**（推荐）：每个数据块仅包含新生成的内容，设置`incremental_output`为`true`启动增量式流式输出。
        
        > 示例：\["我爱","吃","苹果"\]
        
    -   **非增量**：每个数据块都包含之前已生成的内容，造成网络带宽浪费和客户端处理压力。设置`incremental_output`为`false`启动非增量式流式输出。
        
        > 示例：\["我爱","我爱吃","我爱吃苹果"\]
        
-   **查看 Token 消耗**
    
    每个数据块都包含实时的 Token 消耗信息。
    

## Python

```
import os
from http import HTTPStatus
import dashscope
from dashscope import Generation

# 若使用新加坡地域的模型，请释放下列注释
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

# 1. 准备工作：配置API Key
# 建议通过环境变量配置API Key，避免硬编码。
try:
    dashscope.api_key = os.environ["DASHSCOPE_API_KEY"]
except KeyError:
    raise ValueError("请设置环境变量 DASHSCOPE_API_KEY")

# 2. 发起流式请求
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "请介绍一下自己"},
]

try:
    responses = Generation.call(
        model="qwen-plus",
        messages=messages,
        result_format="message",
        stream=True,
        # 关键：设置为True以获取增量输出，性能更佳。
        incremental_output=True,
    )

    # 3. 处理流式响应
    content_parts = []
    print("AI: ", end="", flush=True)

    for resp in responses:
        if resp.status_code == HTTPStatus.OK:
            content = resp.output.choices[0].message.content
            print(content, end="", flush=True)
            content_parts.append(content)

            # 检查是否是最后一个包
            if resp.output.choices[0].finish_reason == "stop":
                usage = resp.usage
                print("\n--- 请求用量 ---")
                print(f"输入 Tokens: {usage.input_tokens}")
                print(f"输出 Tokens: {usage.output_tokens}")
                print(f"总计 Tokens: {usage.total_tokens}")
        else:
            # 处理错误情况
            print(
                f"\n请求失败: request_id={resp.request_id}, code={resp.code}, message={resp.message}"
            )
            break

    full_response = "".join(content_parts)
    # print(f"\n--- 完整回复 ---\n{full_response}")

except Exception as e:
    print(f"发生未知错误: {e}")
```

**返回结果**

```
AI: 你好！我是Qwen，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。如果你有任何问题或需要帮助，欢迎随时向我提问！
--- 请求用量 ---
输入 Tokens: 26
输出 Tokens: 91
总计 Tokens: 117
```

## Java

```
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import io.reactivex.Flowable;
import io.reactivex.schedulers.Schedulers;

import java.util.Arrays;
import java.util.concurrent.CountDownLatch;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 若使用新加坡地域的模型，请释放下列注释
    // static {
    //     Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";
    // }
    public static void main(String[] args) {
        // 1. 获取 API Key
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        if (apiKey == null || apiKey.isEmpty()) {
            System.err.println("请设置环境变量 DASHSCOPE_API_KEY");
            return;
        }

        // 2. 初始化 Generation 实例
        Generation gen = new Generation();
        CountDownLatch latch = new CountDownLatch(1);

        // 3. 构建请求参数
        GenerationParam param = GenerationParam.builder()
                .apiKey(apiKey)
                .model("qwen-plus")
                .messages(Arrays.asList(
                        Message.builder()
                                .role(Role.USER.getValue())
                                .content("介绍一下自己")
                                .build()
                ))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .incrementalOutput(true) // 开启增量输出，流式返回
                .build();
        // 4. 发起流式调用并处理响应
        try {
            Flowable<GenerationResult> result = gen.streamCall(param);
            StringBuilder fullContent = new StringBuilder();
            System.out.print("AI: ");
            result
                    .subscribeOn(Schedulers.io()) // IO线程执行请求
                    .observeOn(Schedulers.computation()) // 计算线程处理响应
                    .subscribe(
                            // onNext: 处理每个响应片段
                            message -> {
                                String content = message.getOutput().getChoices().get(0).getMessage().getContent();
                                String finishReason = message.getOutput().getChoices().get(0).getFinishReason();
                                // 输出内容
                                System.out.print(content);
                                fullContent.append(content);
                                // 当 finishReason 不为 null 时，表示是最后一个 chunk，输出用量信息
                                if (finishReason != null && !"null".equals(finishReason)) {
                                    System.out.println("\n--- 请求用量 ---");
                                    System.out.println("输入 Tokens：" + message.getUsage().getInputTokens());
                                    System.out.println("输出 Tokens：" + message.getUsage().getOutputTokens());
                                    System.out.println("总 Tokens：" + message.getUsage().getTotalTokens());
                                }
                                System.out.flush(); // 立即刷新输出
                            },
                            // onError: 处理错误
                            error -> {
                                System.err.println("\n请求失败: " + error.getMessage());
                                latch.countDown();
                            },
                            // onComplete: 完成回调
                            () -> {
                                System.out.println(); // 换行
                                // System.out.println("完整响应: " + fullContent.toString());
                                latch.countDown();
                            }
                    );
            // 主线程等待异步任务完成
            latch.await();
            System.out.println("程序执行完成");
        } catch (Exception e) {
            System.err.println("请求异常: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

### **返回结果**

```
AI: 你好！我是Qwen，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够帮助你回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。如果你有任何问题或需要帮助，欢迎随时向我提问！
--- 请求用量 ---
输入 Tokens: 26
输出 Tokens: 91
总计 Tokens: 117
```

## curl

### **请求**

```
# ======= 重要提示 =======
# 确保已设置环境变量 DASHSCOPE_API_KEY
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
# === 执行时请删除该注释 ===
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen-plus",
    "input":{
        "messages":[      
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    },
    "parameters": {
        "result_format": "message",
        "incremental_output":true
    }
}'
```

### **响应**

响应遵循 Server-Sent Events (SSE) 格式，每条消息包含：

-   id: 数据块编号；
    
-   event: 事件类型，固定为result；
    
-   HTTP 状态码信息；
    
-   data：JSON 数据部分。
    

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"我是","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":27,"output_tokens":1,"input_tokens":26,"prompt_tokens_details":{"cached_tokens":0}},"request_id":"d30a9914-ac97-9102-b746-ce0cb35e3fa2"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"通义千","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":30,"output_tokens":4,"input_tokens":26,"prompt_tokens_details":{"cached_tokens":0}},"request_id":"d30a9914-ac97-9102-b746-ce0cb35e3fa2"}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"问，阿里巴巴","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":33,"output_tokens":7,"input_tokens":26,"prompt_tokens_details":{"cached_tokens":0}},"request_id":"d30a9914-ac97-9102-b746-ce0cb35e3fa2"}

...


id:13
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"或需要帮助，欢迎随时","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":90,"output_tokens":64,"input_tokens":26,"prompt_tokens_details":{"cached_tokens":0}},"request_id":"d30a9914-ac97-9102-b746-ce0cb35e3fa2"}

id:14
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"告诉我！","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":92,"output_tokens":66,"input_tokens":26,"prompt_tokens_details":{"cached_tokens":0}},"request_id":"d30a9914-ac97-9102-b746-ce0cb35e3fa2"}

id:15
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","role":"assistant"},"finish_reason":"stop"}]},"usage":{"total_tokens":92,"output_tokens":66,"input_tokens":26,"prompt_tokens_details":{"cached_tokens":0}},"request_id":"d30a9914-ac97-9102-b746-ce0cb35e3fa2"}
```

## **多模态模型的流式输出**

**说明**

-   本章节适用于Qwen-VL、Qwen-VL-OCR、Kimi-K2.5、Qwen3-Omni-Captioner、Qwen-Audio、GUI-Plus模型。
    
-   Qwen-Omni 模型**仅支持流式输出**，因其输出可包含**文本**或**音频**等多模态内容，所以结果解析方式与其他模型不同，具体请参见[全模态](https://help.aliyun.com/zh/model-studio/qwen-omni#76b04b353ds7i)。
    

多模态模型支持在对话中加入图片、音频等内容，其流式输出的实现方式与文本模型主要有以下不同：

-   **用户消息（user message）的构造方式**：多模态模型的输入不仅包括文本，还包含图片、音频等多模态信息。
    
-   **DashScope SDK接口：**使用 DashScope Python SDK 时，需调用 MultiModalConversation 接口；使用DashScope Java SDK 时，则调用 MultiModalConversation 类。
    

## OpenAI兼容

## Python

```
from openai import OpenAI
import os

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    
    # 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3-vl-plus",  # 可按需更换为其它多模态模型，并修改相应的 messages
    messages=[
        {"role": "user",
         "content": [{"type": "image_url", 
                    "image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},},
                    {"type": "text", "text": "图中描绘的是什么景象？"}]}],
    stream=True,
  # stream_options={"include_usage": True}
)
full_content = ""
print("流式输出内容为：")
for chunk in completion:
    # 如果stream_options.include_usage为True，则最后一个chunk的choices字段为空列表，需要跳过（可以通过chunk.usage获取 Token 使用量）
    if chunk.choices and chunk.choices[0].delta.content != "":
        full_content += chunk.choices[0].delta.content
        print(chunk.choices[0].delta.content)
print(f"完整内容为：{full_content}")
```

## Node.js

```
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
);

const completion = await openai.chat.completions.create({
    model: "qwen3-vl-plus",  // 可按需更换为其它多模态模型，并修改相应的 messages
    messages: [
        {role: "user",
        content: [{"type": "image_url",
                    "image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},},
                    {"type": "text", "text": "图中描绘的是什么景象？"}]}],
    stream: true,
 // stream_options: { include_usage: true },
    
});

let fullContent = ""
console.log("流式输出内容为：")
for await (const chunk of completion) {
    // 如果stream_options.include_usage为true，则最后一个chunk的choices字段为空数组，需要跳过（可以通过chunk.usage获取 Token 使用量）
    if (chunk.choices[0] && chunk.choices[0].delta.content != null) {
      fullContent += chunk.choices[0].delta.content;
      console.log(chunk.choices[0].delta.content);
    }
}
console.log(`完整输出内容为：${fullContent}`)
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===

curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen3-vl-plus",
    "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
          }
        },
        {
          "type": "text",
          "text": "图中描绘的是什么景象？"
        }
      ]
    }
  ],
    "stream":true,
    "stream_options":{"include_usage":true}
}'
```

## DashScope

## Python

```
import os
from dashscope import MultiModalConversation
import dashscope

# 若使用新加坡地域的模型，请取消下列注释
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
            {"text": "图中描绘的是什么景象?"}
        ]
    }
]

responses = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model='qwen3-vl-plus',  # 可按需更换为其它多模态模型，并修改相应的 messages
    messages=messages,
    stream=True,
    incremental_output=True
    )
    
full_content = ""
print("流式输出内容为：")
for response in responses:
    if response.output.choices[0].message.content:
        print(response.output.choices[0].message.content[0]['text'])
        full_content += response.output.choices[0].message.content[0]['text']
print(f"完整内容为：{full_content}")
```

## Java

```
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import io.reactivex.Flowable;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 若使用新加坡地域的模型，请取消下列注释
    //  static {Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";}

    public static void streamCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"),
                        Collections.singletonMap("text", "图中描绘的是什么景象？"))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3-vl-plus")  // 可按需更换为其它多模态模型，并修改相应的 messages
                .messages(Arrays.asList(userMessage))
                .incrementalOutput(true)
                .build();
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(item -> {
            try {
                List<Map<String, Object>> content = item.getOutput().getChoices().get(0).getMessage().getContent();
                    // 判断content是否存在且不为空
                if (content != null &&  !content.isEmpty()) {
                    System.out.println(content.get(0).get("text"));
                    }
            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        });
    }

    public static void main(String[] args) {
        try {
            streamCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-H 'X-DashScope-SSE: enable' \
-d '{
    "model": "qwen3-vl-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
                    {"text": "图中描绘的是什么景象？"}
                ]
            }
        ]
    },
    "parameters": {
        "incremental_output": true
    }
}'
```

## **思考模型的流式输出**

思考模型会先返回`reasoning_content`（思考过程），再返回`content`（回复内容）。可根据数据包状态判断当前为思考或是回复阶段。

> 思考模型详情参见：[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)、[视觉理解](https://help.aliyun.com/zh/model-studio/vision)、[视觉推理](https://help.aliyun.com/zh/model-studio/visual-reasoning)。

> Qwen3-Omni-Flash（思考模式）实现流式输出请参见[全模态](https://help.aliyun.com/zh/model-studio/qwen-omni#76b04b353ds7i)。

## OpenAI兼容

以下是使用 OpenAI Python SDK 以流式方式调用思考模式 qwen-plus 模型时返回的数据格式：

```
# 思考阶段
...
ChoiceDelta(content=None, function_call=None, refusal=None, role=None, tool_calls=None, reasoning_content='覆盖所有要点，同时')
ChoiceDelta(content=None, function_call=None, refusal=None, role=None, tool_calls=None, reasoning_content='自然流畅。')
# 回复阶段
ChoiceDelta(content='你好！我是**通', function_call=None, refusal=None, role=None, tool_calls=None, reasoning_content=None)
ChoiceDelta(content='义千问**（', function_call=None, refusal=None, role=None, tool_calls=None, reasoning_content=None)
...
```

-   若`reasoning_content`不为 None，`content` 为 `None`，则当前处于思考阶段；
    
-   若`reasoning_content`为 None，`content` 不为 `None`，则当前处于回复阶段；
    
-   若两者均为 `None`，则阶段与前一包一致。
    

## Python

### **示例代码**

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

messages = [{"role": "user", "content": "你是谁"}]

completion = client.chat.completions.create(
    model="qwen-plus",  # 您可以按需更换为其它深度思考模型
    messages=messages,
    # enable_thinking 参数开启思考过程，qwen3-30b-a3b-thinking-2507、qwen3-235b-a22b-thinking-2507、QwQ 与 DeepSeek-R1 模型总会进行思考，不支持该参数
    extra_body={"enable_thinking": True},
    stream=True,
    # stream_options={
    #     "include_usage": True
    # },
)

reasoning_content = ""  # 完整思考过程
answer_content = ""  # 完整回复
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    if not chunk.choices:
        print("\nUsage:")
        print(chunk.usage)
        continue

    delta = chunk.choices[0].delta

    # 只收集思考内容
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
        reasoning_content += delta.reasoning_content

    # 收到content，开始进行回复
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
            is_answering = True
        print(delta.content, end="", flush=True)
        answer_content += delta.content
```

### **返回结果**

```
====================思考过程====================

好的，用户问“你是谁”，我需要给出一个准确且友好的回答。首先，我要确认自己的身份，即通义千问，由阿里巴巴集团旗下的通义实验室研发。接下来，应该说明我的主要功能，比如回答问题、创作文字、逻辑推理等。同时，要保持语气亲切，避免过于技术化，让用户感觉轻松。还要注意不要使用复杂术语，确保回答简洁明了。另外，可能需要加入一些互动元素，邀请用户提问，促进进一步交流。最后，检查是否有遗漏的重要信息，比如我的中文名称“通义千问”和英文名称“Qwen”，以及所属公司和实验室。确保回答全面且符合用户期望。
====================完整回复====================

你好！我是通义千问，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以回答问题、创作文字、进行逻辑推理、编程等，旨在为用户提供高质量的信息和服务。你可以叫我Qwen，或者直接叫我通义千问。有什么我可以帮你的吗？
```

## Node.js

### **示例代码**

```
import OpenAI from "openai";
import process from 'process';

// 初始化 openai 客户端
const openai = new OpenAI({
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY, // 从环境变量读取
    // 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;

async function main() {
    try {
        const messages = [{ role: 'user', content: '你是谁' }];
        const stream = await openai.chat.completions.create({
            // 您可以按需更换为其它 Qwen3 模型、QwQ模型或DeepSeek-R1 模型
            model: 'qwen-plus',
            messages,
            stream: true,
            // enable_thinking 参数开启思考过程，qwen3-30b-a3b-thinking-2507、qwen3-235b-a22b-thinking-2507、QwQ 与 DeepSeek-R1 模型总会进行思考，不支持该参数
            enable_thinking: true
        });
        console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\nUsage:');
                console.log(chunk.usage);
                continue;
            }

            const delta = chunk.choices[0].delta;
            
            // 只收集思考内容
            if (delta.reasoning_content !== undefined && delta.reasoning_content !== null) {
                if (!isAnswering) {
                    process.stdout.write(delta.reasoning_content);
                }
                reasoningContent += delta.reasoning_content;
            }

            // 收到content，开始进行回复
            if (delta.content !== undefined && delta.content) {
                if (!isAnswering) {
                    console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
                    isAnswering = true;
                }
                process.stdout.write(delta.content);
                answerContent += delta.content;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

### **返回结果**

```
====================思考过程====================

好的，用户问“你是谁”，我需要回答我的身份。首先，我应该明确说明我是通义千问，由阿里云开发的超大规模语言模型。接下来，可以提到我的主要功能，比如回答问题、创作文字、逻辑推理等。还要强调我的多语言支持，包括中文和英文，这样用户知道我可以处理不同语言的请求。另外，可能需要解释一下我的应用场景，比如学习、工作和生活中的帮助。不过用户的问题比较直接，可能不需要太详细的信息，保持简洁明了。同时，要确保语气友好，邀请用户进一步提问。检查有没有遗漏的重要信息，比如我的版本或最新更新，但可能用户不需要那么详细。最后，确认回答准确无误，没有错误信息。
====================完整回复====================

我是通义千问，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够回答问题、创作文字、逻辑推理、编程等多种任务，支持中英文等多种语言。如果你有任何问题或需要帮，欢迎随时告诉我！
```

## HTTP

### **示例代码**

## curl

Qwen3 开源版模型需要设置`enable_thinking`为`true`来开启思考模式；`enable_thinking`对 qwen3-30b-a3b-thinking-2507、qwen3-235b-a22b-thinking-2507、QwQ 与 DeepSeek-R1 模型无效。

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "user", 
            "content": "你是谁"
        }
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    },
    "enable_thinking": true
}'
```

### **返回结果**

```
data: {"choices":[{"delta":{"content":null,"role":"assistant","reasoning_content":""},"index":0,"logprobs":null,"finish_reason":null}],"object":"chat.completion.chunk","usage":null,"created":1745485391,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-e2edaf2c-8aaf-9e54-90e2-b21dd5045503"}

.....

data: {"choices":[{"finish_reason":"stop","delta":{"content":"","reasoning_content":null},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1745485391,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-e2edaf2c-8aaf-9e54-90e2-b21dd5045503"}

data: {"choices":[],"object":"chat.completion.chunk","usage":{"prompt_tokens":10,"completion_tokens":360,"total_tokens":370},"created":1745485391,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-e2edaf2c-8aaf-9e54-90e2-b21dd5045503"}

data: [DONE]
```

## DashScope

以下为 DashScope Python SDK 调用思考模式的 qwen-plus 模型时，流式返回的数据包格式：

```
# 思考阶段
...
{"role": "assistant", "content": "", "reasoning_content": "信息量大，"}
{"role": "assistant", "content": "", "reasoning_content": "让用户觉得有帮助。"}
# 回复阶段
{"role": "assistant", "content": "我是通义千问", "reasoning_content": ""}
{"role": "assistant", "content": "，由通义实验室研发", "reasoning_content": ""}
...
```

-   若`reasoning_content`不为 ""，`content` 为 ""，则当前处于思考阶段；
    
-   若`reasoning_content`为 ""，`content` 不为 ""，则当前处于回复阶段；
    
-   若两者均为 ""，则阶段与前一包一致。
    

## Python

### **示例代码**

```
import os
from dashscope import Generation
import dashscope 

# 若使用新加坡地域的模型，请释放下列注释
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"
messages = [{"role": "user", "content": "你是谁？"}]


completion = Generation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 可按需更换为其它深度思考模型
    model="qwen-plus",
    messages=messages,
    result_format="message", # Qwen3开源版模型只支持设定为"message"；为了更好的体验，其它模型也推荐您优先设定为"message"
    # 开启深度思考，该参数对qwen3-30b-a3b-thinking-2507、qwen3-235b-a22b-thinking-2507、QwQ、DeepSeek-R1 模型无效
    enable_thinking=True,
    stream=True,
    incremental_output=True, # Qwen3开源版模型只支持 true；为了更好的体验，其它模型也推荐您优先设定为 true
)

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""
# 判断是否结束思考过程并开始回复
is_answering = False

print("=" * 20 + "思考过程" + "=" * 20)

for chunk in completion:
    # 如果思考过程与回复皆为空，则忽略
    if (
        chunk.output.choices[0].message.content == ""
        and chunk.output.choices[0].message.reasoning_content == ""
    ):
        pass
    else:
        # 如果当前为思考过程
        if (
            chunk.output.choices[0].message.reasoning_content != ""
            and chunk.output.choices[0].message.content == ""
        ):
            print(chunk.output.choices[0].message.reasoning_content, end="", flush=True)
            reasoning_content += chunk.output.choices[0].message.reasoning_content
        # 如果当前为回复
        elif chunk.output.choices[0].message.content != "":
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
            print(chunk.output.choices[0].message.content, end="", flush=True)
            answer_content += chunk.output.choices[0].message.content

# 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(f"{reasoning_content}")
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(f"{answer_content}")
```

### **返回结果**

```
====================思考过程====================
好的，用户问：“你是谁？”我需要回答这个问题。首先，我要明确自己的身份，即通义千问，由阿里云开发的超大规模语言模型。接下来，要说明我的功能和用途，比如回答问题、创作文字、逻辑推理等。同时，要强调我的目标是成为用户的得力助手，提供帮助和支持。

在表达时，要保持口语化，避免使用专业术语或复杂句式。可以加入一些亲切的语气词，比如“你好呀～”，让对话更自然。另外，要确保信息准确，不遗漏关键点，比如我的开发者、主要功能和使用场景。

还要考虑用户可能的后续问题，比如具体的应用例子或技术细节，所以在回答中可以适当埋下伏笔，引导用户进一步提问。例如，提到“无论是日常生活的疑问还是专业领域的问题，我都能尽力提供帮助”，这样既全面又开放。

最后，检查回答是否流畅，有没有重复或冗余的信息，确保简洁明了。同时，保持友好和专业的平衡，让用户感受到既亲切又可靠。
====================完整回复====================
你好呀～我是通义千问，是阿里云开发的一款超大规模语言模型。我能够回答问题、创作文字、进行逻辑推理、编程等等，旨在为用户提供帮助和支持。无论是日常生活的疑问还是专业领域的问题，我都能尽力提供帮助。有什么我可以帮你的吗？
```

## Java

### **示例代码**

```
// dashscope SDK的版本 >= 2.19.4
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;
import java.lang.System;
import java.util.Arrays;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;
    // 若使用新加坡地域的模型，请释放下列注释
    // static {Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";}

    private static void handleGenerationResult(GenerationResult message) {
        String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        String content = message.getOutput().getChoices().get(0).getMessage().getContent();

        if (!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (!content.isEmpty()) {
            finalContent.append(content);
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(content);
        }
    }
    private static GenerationParam buildGenerationParam(Message userMsg) {
        return GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处使用qwen-plus模型，可以按需替换为其它深度思考模型
                .model("qwen-plus")
                // 开启深度思考，对 qwen3-30b-a3b-thinking-2507、qwen3-235b-a22b-thinking-2507、QwQ、DeepSeek-R1 模型无效
                .enableThinking(true)
                .incrementalOutput(true) // Qwen3开源版模型只支持 true；为了更好的体验，其它模型也推荐您优先设定为 true
                .resultFormat("message") // Qwen3开源版模型只支持设定为"message"；为了更好的体验，其它模型也推荐您优先设定为"message"
                .messages(Arrays.asList(userMsg))
                .build();
    }
    public static void streamCallWithMessage(Generation gen, Message userMsg)
            throws NoApiKeyException, ApiException, InputRequiredException {
        GenerationParam param = buildGenerationParam(userMsg);
        Flowable<GenerationResult> result = gen.streamCall(param);
        result.blockingForEach(message -> handleGenerationResult(message));
    }

    public static void main(String[] args) {
        try {
            Generation gen = new Generation();
            Message userMsg = Message.builder().role(Role.USER.getValue()).content("你是谁？").build();
            streamCallWithMessage(gen, userMsg);
//             打印最终结果
//            if (reasoningContent.length() > 0) {
//                System.out.println("\n====================完整回复====================");
//                System.out.println(finalContent.toString());
//            }
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

### **返回结果**

```
====================思考过程====================
好的，用户问“你是谁？”，我需要根据之前的设定来回答。首先，我的角色是通义千问，阿里巴巴集团旗下的超大规模语言模型。要保持口语化，简洁易懂。

用户可能刚接触我，或者想确认我的身份。应该先直接回答我是谁，然后简要说明我的功能和用途，比如回答问题、创作文字、编程等。还要提到支持多语言，这样用户知道我可以处理不同语言的需求。

另外，根据指导方针，要保持拟人性，所以语气要友好，可能用表情符号增加亲切感。同时，可能需要引导用户进一步提问或使用我的功能，比如问他们需要什么帮助。

需要注意不要使用复杂术语，避免冗长。检查是否有遗漏的关键点，比如多语言支持和具体能力。确保回答符合所有要求，包括口语化和简洁。
====================完整回复====================
你好！我是通义千问，阿里巴巴集团旗下的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我熟练掌握多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。有什么需要我帮忙的吗？
```

## HTTP

### **示例代码**

## curl

混合思考模型需要设置`enable_thinking`为`true`来开启思考模式；`enable_thinking`对qwen3-30b-a3b-thinking-2507、qwen3-235b-a22b-thinking-2507、 QwQ 与 DeepSeek-R1 模型无效。

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
# === 执行时请删除该注释 ===
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen-plus",
    "input":{
        "messages":[      
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    },
    "parameters":{
        "enable_thinking": true,
        "incremental_output": true,
        "result_format": "message"
    }
}'
```

### **返回结果**

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"嗯","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":14,"input_tokens":11,"output_tokens":3},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"，","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":15,"input_tokens":11,"output_tokens":4},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"用户","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":16,"input_tokens":11,"output_tokens":5},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:4
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"问","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":17,"input_tokens":11,"output_tokens":6},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:5
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"“","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":18,"input_tokens":11,"output_tokens":7},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}
......

id:358
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"帮助","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":373,"input_tokens":11,"output_tokens":362},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:359
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"，","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":374,"input_tokens":11,"output_tokens":363},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:360
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"欢迎","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":375,"input_tokens":11,"output_tokens":364},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:361
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"随时","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":376,"input_tokens":11,"output_tokens":365},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:362
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"告诉我","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":377,"input_tokens":11,"output_tokens":366},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:363
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"！","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":378,"input_tokens":11,"output_tokens":367},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:364
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"","role":"assistant"},"finish_reason":"stop"}]},"usage":{"total_tokens":378,"input_tokens":11,"output_tokens":367},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}
```

## **应用于生产环境**

-   **性能与资源管理**：在后端服务中，为每个流式请求维持一个HTTP长连接会消耗资源。确保您的服务配置了合理的连接池大小和超时时间。在高并发场景下，监控服务的文件描述符（file descriptors）使用情况，防止耗尽。
    
-   **客户端渲染**：在Web前端，使用 `ReadableStream` 和 `TextDecoderStream` API 可以平滑地处理和渲染SSE事件流，提供最佳的用户体验。
    
-   [模型监控](https://help.aliyun.com/zh/model-studio/model-telemetry/)：
    
    -   **关键指标**：监控**首Token延迟（Time to First Token, TTFT）**，该指标是衡量流式体验的核心。同时监控请求错误率和平均响应时长。
        
    -   **告警设置**：为API错误率（特别是4xx和5xx错误）的异常设置告警。
        
-   **Nginx代理配置**：若使用 Nginx 作为反向代理，其默认的输出缓冲（proxy\_buffering）会破坏流式响应的实时性。为确保数据能被即时推送到客户端，务必在Nginx配置文件中设置`proxy_buffering off`以关闭此功能。
    

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## **常见问题**

### **Q：为什么返回数据中没有 usage 信息？**

A：OpenAI 协议默认不返回 usage 信息，设置`stream_options`参数使得最后返回的包中包含 usage 信息。

### **Q：开启流式输出对模型的回复效果是否有影响？**

A：无影响，但部分模型仅支持流式输出，且非流式输出可能引发超时错误。建议优先使用流式输出。

深度思考模型在生成回复前会先进行推理，以提升模型在逻辑推理与数值计算等复杂任务中的准确性。本文介绍如何调用 Qwen、DeepSeek 等支持深度思考的模型。

> 本文介绍如何通过 OpenAI 兼容的 Chat Completion 接口或 DashScope 接口调用深度思考模型。 Responses API 用法参见：[深度思考](https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api#example-deep-thinking-title)。

![QwQ Logo](https://assets.alicdn.com/g/qwenweb/qwen-webui-fe/0.0.54/static/favicon.png)

Qwen

显示思考过程 ▼

 发送虚拟请求

@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } } @keyframes blink { 0%, 100% { opacity: 0; } 50% { opacity: 1; } } .arrow-up { transform: rotate(180deg); } .arrow-down { transform: rotate(0deg); } .toggle-thinking:hover { background: #e6e8eb; } .send-button:hover { transform: scale(1.05); box-shadow: 0 2px 8px rgba(79, 118, 227, 0.3); }

## **使用方式**

阿里云百炼提供多种深度思考模型 API，包含混合思考与仅思考两种模式。

-   **混合思考模式**：通过`enable_thinking`参数控制是否开启思考模式：
    
    -   设为`true`时：模型在思考后回复；
        
    -   设为`false`时：模型直接回复；
        
    
    ## OpenAI 兼容
    
    ```
    # 导入依赖与创建客户端...
    completion = client.chat.completions.create(
        model="qwen-plus", # 选择模型
        messages=[{"role": "user", "content": "你是谁"}],    
        # 由于 enable_thinking 非 OpenAI 标准参数，需要通过 extra_body 传入
        extra_body={"enable_thinking":True},
        # 流式输出方式调用
        stream=True,
        # 使流式返回的最后一个数据包包含Token消耗信息
        stream_options={
            "include_usage": True
        }
    )
    ```
    
    ## DashScope
    
    > Qwen3.5系列的DashScope API采用多模态接口，以下示例会报错`url error`，调用方式请参见[开启/关闭思考模式](https://help.aliyun.com/zh/model-studio/vision#bc67a9a2bd2of)。
    
    ```
    # 导入依赖...
    
    response = Generation.call(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 可按需更换为其它深度思考模型
        model="qwen-plus",
        messages=messages,
        result_format="message",
        enable_thinking=True,
        stream=True,
        incremental_output=True
    )
    ```
    
-   **仅思考模式**：模型始终在回复前进行思考，且无法关闭。除了无需设置 enable\_thinking 参数外，请求格式与混合思考模式一致。
    

思考内容通过`reasoning_content`字段返回，回复内容通过`content`字段返回。深度思考模型在回复前需进行思考，导致等待回复时间变长，且多数模型仅支持流式输出，因此本文档均以流式调用为例。

## **支持的模型**

## Qwen3.5

-   **商业版**
    
    -   **千问3.5 Plus系列**（混合思考模式，**默认开启思考模式**）：qwen3.5-plus、qwen3.5-plus-2026-02-15
        
    -   **千问3.5 Flash系列**（混合思考模式，**默认开启思考模式**）：qwen3.5-flash、qwen3.5-flash-2026-02-23
        
-   **开源版**
    
    -   混合思考模式，**默认开启思考模式**：qwen3.5-397b-a17b、 qwen3.5-122b-a10b、qwen3.5-27b、qwen3.5-35b-a3b
        

## Qwen3

-   **商业版**
    
    -   **千问Max系列**（混合思考模式，默认不开启思考模式）：qwen3-max-2026-01-23、qwen3-max-preview
        
    -   **千问Plus系列**（混合思考模式，默认不开启思考模式）：qwen-plus、qwen-plus-latest、qwen-plus-2025-04-28 及之后的快照版模型
        
    -   **千问Flash系列**（混合思考模式，默认不开启思考模式）：qwen-flash、qwen-flash-2025-07-28 及之后的快照版模型
        
    -   **千问Turbo系列**（混合思考模式，默认不开启思考模式）：qwen-turbo、qwen-turbo-latest、qwen-turbo-2025-04-28 及之后的快照版模型
        
-   **开源版**
    
    -   混合思考模式，默认开启思考模式：qwen3-235b-a22b、qwen3-32b、qwen3-30b-a3b、qwen3-14b、qwen3-8b、qwen3-4b、qwen3-1.7b、qwen3-0.6b
        
    -   仅思考模式：qwen3-next-80b-a3b-thinking、qwen3-235b-a22b-thinking-2507、qwen3-30b-a3b-thinking-2507
        

## **QwQ （基于 Qwen2.5）**

仅思考模式：qwq-plus、qwq-plus-latest、qwq-plus-2025-03-05、qwq-32b

## DeepSeek

-   混合思考模式，默认不开启思考模式：deepseek-v3.2、deepseek-v3.2-exp、deepseek-v3.1
    
-   仅思考模式：deepseek-r1、deepseek-r1-0528、deepseek-r1蒸馏模型
    

## **GLM**

混合思考模式，默认开启思考模式：glm-5、glm-4.7、glm-4.6、glm-4.5、glm-4.5-air

## Kimi

仅思考模式：kimi-k2-thinking

模型的名称、上下文、价格、快照版本等信息请参见[模型列表](https://help.aliyun.com/zh/model-studio/models)；并发限流条件请参考[限流](https://help.aliyun.com/zh/model-studio/rate-limit)。

## **快速开始**

API 使用前提：已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并完成[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，需要[安装 OpenAI 或 DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk#8833b9274f4v8)（DashScope Java SDK 版本需要不低于2.19.4）。

运行以下代码，可通过流式输出的方式调用思考模式的qwen-plus模型。

## OpenAI兼容

## Python

### **示例代码**

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 各地域配置不同，请根据实际地域修改
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

messages = [{"role": "user", "content": "你是谁"}]

completion = client.chat.completions.create(
    model="qwen-plus",  # 您可以按需更换为其它深度思考模型
    messages=messages,
    extra_body={"enable_thinking": True},
    stream=True,
    stream_options={
        "include_usage": True
    },
)

reasoning_content = ""  # 完整思考过程
answer_content = ""  # 完整回复
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    if not chunk.choices:
        print("\nUsage:")
        print(chunk.usage)
        continue

    delta = chunk.choices[0].delta

    # 只收集思考内容
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
        reasoning_content += delta.reasoning_content

    # 收到content，开始进行回复
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
            is_answering = True
        print(delta.content, end="", flush=True)
        answer_content += delta.content
```

### **返回结果**

```
====================思考过程====================

好的，用户问“你是谁”，我需要给出一个准确且友好的回答。首先，我要确认自己的身份，即千问，由阿里巴巴集团旗下的通义实验室研发。接下来，应该说明我的主要功能，比如回答问题、创作文字、逻辑推理等。同时，要保持语气亲切，避免过于技术化，让用户感觉轻松。还要注意不要使用复杂术语，确保回答简洁明了。另外，可能需要加入一些互动元素，邀请用户提问，促进进一步交流。最后，检查是否有遗漏的重要信息，比如我的中文名称“千问”和英文名称“Qwen”，以及所属公司和实验室。确保回答全面且符合用户期望。
====================完整回复====================

你好！我是千问，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以回答问题、创作文字、进行逻辑推理、编程等，旨在为用户提供高质量的信息和服务。你可以叫我Qwen，或者直接叫我千问。有什么我可以帮你的吗？
```

## Node.js

### **示例代码**

```
import OpenAI from "openai";
import process from 'process';

// 初始化 openai 客户端
const openai = new OpenAI({
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY, // 从环境变量读取
    // 各地域配置不同，请根据实际地域修改
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;

async function main() {
    try {
        const messages = [{ role: 'user', content: '你是谁' }];
        const stream = await openai.chat.completions.create({
            model: 'qwen-plus',
            messages,
            stream: true,
            enable_thinking: true
        });
        console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\nUsage:');
                console.log(chunk.usage);
                continue;
            }

            const delta = chunk.choices[0].delta;
            
            // 只收集思考内容
            if (delta.reasoning_content !== undefined && delta.reasoning_content !== null) {
                if (!isAnswering) {
                    process.stdout.write(delta.reasoning_content);
                }
                reasoningContent += delta.reasoning_content;
            }

            // 收到content，开始进行回复
            if (delta.content !== undefined && delta.content) {
                if (!isAnswering) {
                    console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
                    isAnswering = true;
                }
                process.stdout.write(delta.content);
                answerContent += delta.content;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

### **返回结果**

```
====================思考过程====================

好的，用户问“你是谁”，我需要回答我的身份。首先，我应该明确说明我是千问，由阿里云开发的超大规模语言模型。接下来，可以提到我的主要功能，比如回答问题、创作文字、逻辑推理等。还要强调我的多语言支持，包括中文和英文，这样用户知道我可以处理不同语言的请求。另外，可能需要解释一下我的应用场景，比如学习、工作和生活中的帮助。不过用户的问题比较直接，可能不需要太详细的信息，保持简洁明了。同时，要确保语气友好，邀请用户进一步提问。检查有没有遗漏的重要信息，比如我的版本或最新更新，但可能用户不需要那么详细。最后，确认回答准确无误，没有错误信息。
====================完整回复====================

我是千问，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够回答问题、创作文字、逻辑推理、编程等多种任务，支持中英文等多种语言。如果你有任何问题或需要帮，欢迎随时告诉我！
```

## HTTP

### **示例代码**

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改/chat/completions
# === 执行时请删除该注释 ===
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "user", 
            "content": "你是谁"
        }
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    },
    "enable_thinking": true
}'
```

### **返回结果**

```
data: {"choices":[{"delta":{"content":null,"role":"assistant","reasoning_content":""},"index":0,"logprobs":null,"finish_reason":null}],"object":"chat.completion.chunk","usage":null,"created":1745485391,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-e2edaf2c-8aaf-9e54-90e2-b21dd5045503"}

.....

data: {"choices":[{"finish_reason":"stop","delta":{"content":"","reasoning_content":null},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1745485391,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-e2edaf2c-8aaf-9e54-90e2-b21dd5045503"}

data: {"choices":[],"object":"chat.completion.chunk","usage":{"prompt_tokens":10,"completion_tokens":360,"total_tokens":370},"created":1745485391,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-e2edaf2c-8aaf-9e54-90e2-b21dd5045503"}

data: [DONE]
```

## DashScope

> Qwen3.5系列的DashScope API采用多模态接口，以下示例会报错`url error`，调用方式请参见[开启/关闭思考模式](https://help.aliyun.com/zh/model-studio/vision#bc67a9a2bd2of)。

## Python

### **示例代码**

```
import os
from dashscope import Generation
import dashscope 

# 各地域配置不同，请根据实际地域修改
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

messages = [{"role": "user", "content": "你是谁？"}]


completion = Generation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 可按需更换为其它深度思考模型
    model="qwen-plus",
    messages=messages,
    result_format="message",
    enable_thinking=True,
    stream=True,
    incremental_output=True
)

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""
# 判断是否结束思考过程并开始回复
is_answering = False

print("=" * 20 + "思考过程" + "=" * 20)

for chunk in completion:
    # 如果思考过程与回复皆为空，则忽略
    if (
        chunk.output.choices[0].message.content == ""
        and chunk.output.choices[0].message.reasoning_content == ""
    ):
        pass
    else:
        # 如果当前为思考过程
        if (
            chunk.output.choices[0].message.reasoning_content != ""
            and chunk.output.choices[0].message.content == ""
        ):
            print(chunk.output.choices[0].message.reasoning_content, end="", flush=True)
            reasoning_content += chunk.output.choices[0].message.reasoning_content
        # 如果当前为回复
        elif chunk.output.choices[0].message.content != "":
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
            print(chunk.output.choices[0].message.content, end="", flush=True)
            answer_content += chunk.output.choices[0].message.content

# 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(f"{reasoning_content}")
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(f"{answer_content}")
```

### **返回结果**

```
====================思考过程====================
好的，用户问：“你是谁？”我需要回答这个问题。首先，我要明确自己的身份，即千问，由阿里云开发的超大规模语言模型。接下来，要说明我的功能和用途，比如回答问题、创作文字、逻辑推理等。同时，要强调我的目标是成为用户的得力助手，提供帮助和支持。

在表达时，要保持口语化，避免使用专业术语或复杂句式。可以加入一些亲切的语气词，比如“你好呀～”，让对话更自然。另外，要确保信息准确，不遗漏关键点，比如我的开发者、主要功能和使用场景。

还要考虑用户可能的后续问题，比如具体的应用例子或技术细节，所以在回答中可以适当埋下伏笔，引导用户进一步提问。例如，提到“无论是日常生活的疑问还是专业领域的问题，我都能尽力提供帮助”，这样既全面又开放。

最后，检查回答是否流畅，有没有重复或冗余的信息，确保简洁明了。同时，保持友好和专业的平衡，让用户感受到既亲切又可靠。
====================完整回复====================
你好呀～我是千问，是阿里云开发的一款超大规模语言模型。我能够回答问题、创作文字、进行逻辑推理、编程等等，旨在为用户提供帮助和支持。无论是日常生活的疑问还是专业领域的问题，我都能尽力提供帮助。有什么我可以帮你的吗？
```

## Java

### **示例代码**

```
// dashscope SDK的版本 >= 2.19.4
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;
import java.lang.System;
import java.util.Arrays;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;
    // 各地域配置不同，请根据实际地域修改
    // static {Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";}

    private static void handleGenerationResult(GenerationResult message) {
        String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        String content = message.getOutput().getChoices().get(0).getMessage().getContent();

        if (!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (!content.isEmpty()) {
            finalContent.append(content);
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(content);
        }
    }
    private static GenerationParam buildGenerationParam(Message userMsg) {
        return GenerationParam.builder()
                 // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-plus")
                .enableThinking(true)
                .incrementalOutput(true)
                .resultFormat("message")
                .messages(Arrays.asList(userMsg))
                .build();
    }
    public static void streamCallWithMessage(Generation gen, Message userMsg)
            throws NoApiKeyException, ApiException, InputRequiredException {
        GenerationParam param = buildGenerationParam(userMsg);
        Flowable<GenerationResult> result = gen.streamCall(param);
        result.blockingForEach(message -> handleGenerationResult(message));
    }

    public static void main(String[] args) {
        try {
            Generation gen = new Generation();
            Message userMsg = Message.builder().role(Role.USER.getValue()).content("你是谁？").build();
            streamCallWithMessage(gen, userMsg);
//             打印最终结果
//            if (reasoningContent.length() > 0) {
//                System.out.println("\n====================完整回复====================");
//                System.out.println(finalContent.toString());
//            }
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

### **返回结果**

```
====================思考过程====================
好的，用户问“你是谁？”，我需要根据之前的设定来回答。首先，我的角色是千问，阿里巴巴集团旗下的超大规模语言模型。要保持口语化，简洁易懂。

用户可能刚接触我，或者想确认我的身份。应该先直接回答我是谁，然后简要说明我的功能和用途，比如回答问题、创作文字、编程等。还要提到支持多语言，这样用户知道我可以处理不同语言的需求。

另外，根据指导方针，要保持拟人性，所以语气要友好，可能用表情符号增加亲切感。同时，可能需要引导用户进一步提问或使用我的功能，比如问他们需要什么帮助。

需要注意不要使用复杂术语，避免冗长。检查是否有遗漏的关键点，比如多语言支持和具体能力。确保回答符合所有要求，包括口语化和简洁。
====================完整回复====================
你好！我是千问，阿里巴巴集团旗下的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我熟练掌握多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。有什么需要我帮忙的吗？
```

## HTTP

### **示例代码**

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
# === 执行时请删除该注释 ===
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen-plus",
    "input":{
        "messages":[      
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    },
    "parameters":{
        "enable_thinking": true,
        "incremental_output": true,
        "result_format": "message"
    }
}'
```

### **返回结果**

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"嗯","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":14,"input_tokens":11,"output_tokens":3},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"，","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":15,"input_tokens":11,"output_tokens":4},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"用户","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":16,"input_tokens":11,"output_tokens":5},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:4
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"问","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":17,"input_tokens":11,"output_tokens":6},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:5
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"“","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":18,"input_tokens":11,"output_tokens":7},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}
......

id:358
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"帮助","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":373,"input_tokens":11,"output_tokens":362},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:359
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"，","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":374,"input_tokens":11,"output_tokens":363},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:360
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"欢迎","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":375,"input_tokens":11,"output_tokens":364},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:361
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"随时","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":376,"input_tokens":11,"output_tokens":365},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:362
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"告诉我","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":377,"input_tokens":11,"output_tokens":366},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:363
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"！","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":378,"input_tokens":11,"output_tokens":367},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:364
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"","role":"assistant"},"finish_reason":"stop"}]},"usage":{"total_tokens":378,"input_tokens":11,"output_tokens":367},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}
```

## **核心能力**

### **切换思考/非思考模式**

启用思考模式通常可提升回复质量，但会增加响应延迟和成本。使用支持混合思考模式的模型时，可在不更换模型的前提下，根据问题复杂度动态切换思考或非思考模式：

-   无需复杂推理（如日常聊天或简单问答）：可将`enable_thinking`设为`false`以关闭思考模式；
    
-   需要复杂推理（如逻辑推理、代码生成或数学解答）：可将`enable_thinking`设为`true`以开启思考模式。
    

## OpenAI兼容

**重要**

`enable_thinking`非 OpenAI 标准参数，若使用 OpenAI Python SDK 请通过 `extra_body`传入，Node.js SDK 中作为顶层参数传入。

## Python

### **示例代码**

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 各地域配置不同，请根据实际地域修改
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

messages = [{"role": "user", "content": "你是谁"}]
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=messages,
    # 通过 extra_body 设置 enable_thinking 开启思考过程
    extra_body={"enable_thinking": True},
    stream=True,
    stream_options={
        "include_usage": True
    },
)

reasoning_content = ""  # 完整思考过程
answer_content = ""  # 完整回复
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    if not chunk.choices:
        print("\n" + "=" * 20 + "Token 消耗" + "=" * 20 + "\n")
        print(chunk.usage)
        continue

    delta = chunk.choices[0].delta

    # 只收集思考内容
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
        reasoning_content += delta.reasoning_content

    # 收到content，开始进行回复
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
            is_answering = True
        print(delta.content, end="", flush=True)
        answer_content += delta.content
```

### **返回结果**

```
====================思考过程====================

嗯，用户问“你是谁”，我需要先确定他们想知道什么。可能他们第一次接触我，或者想确认我的身份。我应该先介绍自己是千问，由通义实验室研发。然后要说明我的功能，比如回答问题、创作文字、编程等，这样用户了解我能提供什么帮助。还要提到我支持多种语言，这样国际用户也会知道他们可以用不同语言交流。最后保持友好，邀请他们提问，这样可以促进进一步互动。要注意简洁明了，避免技术术语太多，让用户容易理解。可能用户需要的是快速了解我的能力，所以重点放在功能和用途上。还要检查有没有遗漏的信息，比如是否要提到阿里巴巴集团，或者更多技术细节。不过用户可能只需要基本的信息，不需要太深入。确保回答友好且专业，同时鼓励用户继续提问。
====================完整回复====================

我是千问，由通义实验室研发的超大规模语言模型。我可以帮助你回答问题、创作文字、编程、表达观点等，支持多语言交流。有什么需要我帮忙的吗？
====================Token 消耗====================

CompletionUsage(completion_tokens=221, prompt_tokens=10, total_tokens=231, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=172, rejected_prediction_tokens=None), prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=0))
```

## Node.js

### **示例代码**

```
import OpenAI from "openai";
import process from 'process';

// 初始化OpenAI客户端
const openai = new OpenAI({
    // 如果没有配置环境变量，请用阿里云百炼API Key替换：apiKey: "sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY, 
    // 各地域配置不同，请根据实际地域修改
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = ''; // 完整思考过程
let answerContent = ''; // 完整回复
let isAnswering = false; // 是否进入回复阶段

async function main() {
    try {
        const messages = [{ role: 'user', content: '你是谁' }];
        
        const stream = await openai.chat.completions.create({
            model: 'qwen-plus',
            messages,
            // 注意：在 Node.js SDK，enable_thinking 这样的非标准参数作为顶层属性传递的，无需放在 extra_body 中
            enable_thinking: true,
            stream: true,
            stream_options: {
                include_usage: true
            },
        });

        console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\n' + '='.repeat(20) + 'Token 消耗' + '='.repeat(20) + '\n');
                console.log(chunk.usage);
                continue;
            }

            const delta = chunk.choices[0].delta;
            
            // 只收集思考内容
            if (delta.reasoning_content !== undefined && delta.reasoning_content !== null) {
                if (!isAnswering) {
                    process.stdout.write(delta.reasoning_content);
                }
                reasoningContent += delta.reasoning_content;
            }

            // 收到content，开始进行回复
            if (delta.content !== undefined && delta.content) {
                if (!isAnswering) {
                    console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
                    isAnswering = true;
                }
                process.stdout.write(delta.content);
                answerContent += delta.content;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

### **返回结果**

```
====================思考过程====================

嗯，用户问“你是谁”，我需要先确定他们想知道什么。可能他们第一次接触我，或者想确认我的身份。我应该先介绍自己的名字和身份，比如千问，英文名Qwen。然后说明我是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。接下来要提到我的功能，比如回答问题、创作文字、编程、表达观点等，这样用户能了解我的用途。还要提到我支持多语言，这样国际用户会觉得有用。最后邀请他们提问，保持友好和开放的态度。注意用简洁易懂的语言，避免技术术语太多。可能用户需要帮助，或者只是好奇，所以回应要亲切，鼓励他们进一步互动。另外，可能需要考虑用户是否有更深层的需求，比如测试我的能力或者寻找特定帮助，但初次回答还是以基本信息和引导为主。保持口语化，不用复杂句子，让信息传达更有效。
====================完整回复====================

你好！我是千问，英文名Qwen，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字（比如写故事、写公文、写邮件、写剧本等）、进行逻辑推理、编程，甚至表达观点和玩游戏。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。

如果你有任何问题或需要帮助，随时告诉我！
====================Token 消耗====================

{
  prompt_tokens: 10,
  completion_tokens: 288,
  total_tokens: 298,
  completion_tokens_details: { reasoning_tokens: 188 },
  prompt_tokens_details: { cached_tokens: 0 }
}
```

## HTTP

### **示例代码**

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改/chat/completions
# === 执行时请删除该注释 ===
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "user", 
            "content": "你是谁"
        }
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    },
    "enable_thinking": true
}'
```

## DashScope

> Qwen3.5系列的DashScope API采用多模态接口，以下示例会报错`url error`，调用方式请参见[开启/关闭思考模式](https://help.aliyun.com/zh/model-studio/vision#bc67a9a2bd2of)。

## Python

### **示例代码**

```
import os
from dashscope import Generation
import dashscope 

# 各地域配置不同，请根据实际地域修改
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

# 初始化请求参数
messages = [{"role": "user", "content": "你是谁？"}]

completion = Generation.call(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-plus",
    messages=messages,
    result_format="message",  # 设置结果格式为 message
    enable_thinking=True,     # 开启思考过程
    stream=True,              # 开启流式输出
    incremental_output=True,  # 开启增量输出
)

reasoning_content = ""  # 完整思考过程
answer_content = ""     # 完整回复
is_answering = False    # 是否进入回复阶段

print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    message = chunk.output.choices[0].message
    
    # 只收集思考内容
    if message.reasoning_content:
        if not is_answering:
            print(message.reasoning_content, end="", flush=True)
        reasoning_content += message.reasoning_content

    # 收到 content，开始进行回复
    if message.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
            is_answering = True
        print(message.content, end="", flush=True)
        answer_content += message.content

print("\n" + "=" * 20 + "Token 消耗" + "=" * 20 + "\n")
print(chunk.usage)
# 循环结束后，reasoning_content 和 answer_content 变量中包含了完整的内容
# 您可以在这里根据需要进行后续处理
# print(f"\n\n完整思考过程:\n{reasoning_content}")
# print(f"\n完整回复:\n{answer_content}")
```

### **返回结果**

```
====================思考过程====================

嗯，用户问“你是谁？”，我需要先确定他们想知道什么。可能他们第一次接触我，或者想确认我的身份。首先，我应该介绍自己的名字，千问，然后说明我是通义实验室研发的超大规模语言模型。接下来，可能需要解释我的功能，比如回答问题、创作文字、编程等，这样用户能了解我的用途。还要提到我支持多种语言，这样国际用户也能知道他们可以用不同语言交流。最后，保持友好，邀请他们提问，这样能促进进一步的互动。要注意用简洁易懂的语言，避免技术术语太多，让用户容易理解。可能用户有更深层的需求，比如测试我的能力，或者寻找帮助，所以提供具体的例子会更好，比如写故事、写公文、写邮件等。还要确保回答结构清晰，分点说明功能，但可能不需要用项目符号，而是自然过渡。另外，要强调我是AI助手，没有个人意识，所有回答都基于训练数据，这样避免误解。可能需要检查有没有遗漏的重要信息，比如多模态能力，或者最新的更新，但根据之前的回复，可能不需要太深入。总之，回答要全面但简洁，友好且有帮助，让用户感到被理解和支持。
====================完整回复====================

我是千问，阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你：

1. **回答问题**：无论是学术问题、常识问题还是专业领域问题，我都可以尝试为你解答。
2. **创作文字**：写故事、写公文、写邮件、写剧本等，我都可以帮你完成。
3. **逻辑推理**：我可以帮助你进行逻辑推理和解决问题。
4. **编程**：我可以理解并生成多种编程语言的代码。
5. **多语言支持**：我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。

如果你有任何问题或需要帮助，随时告诉我！
====================Token 消耗====================

{"input_tokens": 11, "output_tokens": 405, "total_tokens": 416, "output_tokens_details": {"reasoning_tokens": 256}, "prompt_tokens_details": {"cached_tokens": 0}}
```

## Java

### **示例代码**

```
// dashscope SDK的版本 >= 2.19.4
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;
import java.lang.System;
import java.util.Arrays;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;
    //  各地域配置不同，请根据实际地域修改
    // static {Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";}

    private static void handleGenerationResult(GenerationResult message) {
        String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        String content = message.getOutput().getChoices().get(0).getMessage().getContent();

        if (!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (!content.isEmpty()) {
            finalContent.append(content);
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(content);
        }
    }
    private static GenerationParam buildGenerationParam(Message userMsg) {
        return GenerationParam.builder()
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-plus")
                .enableThinking(true)
                .incrementalOutput(true)
                .resultFormat("message")
                .messages(Arrays.asList(userMsg))
                .build();
    }
    public static void streamCallWithMessage(Generation gen, Message userMsg)
            throws NoApiKeyException, ApiException, InputRequiredException {
        GenerationParam param = buildGenerationParam(userMsg);
        Flowable<GenerationResult> result = gen.streamCall(param);
        result.blockingForEach(message -> handleGenerationResult(message));
    }

    public static void main(String[] args) {
        try {
            Generation gen = new Generation();
            Message userMsg = Message.builder().role(Role.USER.getValue()).content("你是谁？").build();
            streamCallWithMessage(gen, userMsg);
//             打印最终结果
//            if (reasoningContent.length() > 0) {
//                System.out.println("\n====================完整回复====================");
//                System.out.println(finalContent.toString());
//            }
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

### **返回结果**

```
====================思考过程====================
嗯，用户问“你是谁？”，我需要先确定他们想了解什么。可能他们想知道我的身份，或者是在测试我的反应。首先，我应该明确回答我是千问，阿里巴巴集团旗下的超大规模语言模型。然后，可能需要简要介绍我的功能，比如回答问题、创作文字、编程等，这样用户能了解我的用途。还要提到我支持多种语言，这样国际用户也会知道他们可以用不同语言交流。最后，保持友好，邀请他们提问，这样他们会觉得亲切，愿意继续互动。要注意回答不要太长，但信息要全面。可能用户还有后续问题，比如我的技术细节或者使用场景，但初次回答应该简洁明了。确保没有使用专业术语，让所有用户都能理解。检查有没有遗漏的重要信息，比如多语言支持和具体功能例子。好的，这样应该能覆盖用户的需求了。
====================完整回复====================
我是千问，阿里巴巴集团旗下的超大规模语言模型。我能够回答问题、创作文字（如写故事、写公文、写邮件、写剧本等）、进行逻辑推理、编程、表达观点、玩游戏等，支持多语言交流，包括但不限于中文、英文、德语、法语、西班牙语等。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

## HTTP

### **示例代码**

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域base_url不同，请根据实际地域修改
# === 执行时请删除该注释 ===
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen-plus",
    "input":{
        "messages":[      
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    },
    "parameters":{
        "enable_thinking": true,
        "incremental_output": true,
        "result_format": "message"
    }
}'
```

### **返回结果**

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"嗯","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":14,"input_tokens":11,"output_tokens":3},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"，","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":15,"input_tokens":11,"output_tokens":4},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"用户","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":16,"input_tokens":11,"output_tokens":5},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:4
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"问","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":17,"input_tokens":11,"output_tokens":6},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:5
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"“","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":18,"input_tokens":11,"output_tokens":7},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}
......

id:358
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"帮助","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":373,"input_tokens":11,"output_tokens":362},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:359
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"，","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":374,"input_tokens":11,"output_tokens":363},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:360
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"欢迎","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":375,"input_tokens":11,"output_tokens":364},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:361
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"随时","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":376,"input_tokens":11,"output_tokens":365},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:362
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"告诉我","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":377,"input_tokens":11,"output_tokens":366},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:363
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"！","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":378,"input_tokens":11,"output_tokens":367},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}

id:364
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"","role":"assistant"},"finish_reason":"stop"}]},"usage":{"total_tokens":378,"input_tokens":11,"output_tokens":367},"request_id":"25d58c29-c47b-9e8d-a0f1-d6c309ec58b1"}
```

此外，**Qwen3 开源版的混合思考模型与qwen-plus-2025-04-28、qwen-turbo-2025-04-28模型**提供了通过提示词动态控制思考模式的方法。`enable_thinking`为`true`时，在提示词中加上`/no_think`，模型会关闭思考模式。若需在多轮对话中重新开启思考模式，需在最新输入的提示词加上`/think` 。模型会遵循最新的`/think` 或`/no_think`指令。

### **限制思考长度**

深度思考模型有时会生成冗长的推理过程，这会增加等待时间并消耗较多 Token。通过`thinking_budget`参数可限制推理过程的最大 Token 数，超过该限制时，模型会立即生成回复。

> `thinking_budget` 默认值为模型的最大思维链长度，请参见[模型列表](https://help.aliyun.com/zh/model-studio/models)。

**重要**

`thinking_budget`参数支持 Qwen3（思考模式）、GLM与Kimi模型。

## OpenAI兼容

## Python

### **示例代码**

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 各地域配置不同，请根据实际地域修改
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

messages = [{"role": "user", "content": "你是谁"}]

completion = client.chat.completions.create(
    model="qwen-plus",
    messages=messages,
    # enable_thinking 参数开启思考过程，thinking_budget 参数设置最大推理过程 Token 数
    extra_body={
        "enable_thinking": True,
        "thinking_budget": 50
        },
    stream=True,
    stream_options={
        "include_usage": True
    },
)

reasoning_content = ""  # 完整思考过程
answer_content = ""  # 完整回复
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    if not chunk.choices:
        print("\nUsage:")
        print(chunk.usage)
        continue

    delta = chunk.choices[0].delta

    # 只收集思考内容
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
        reasoning_content += delta.reasoning_content

    # 收到content，开始进行回复
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
            is_answering = True
        print(delta.content, end="", flush=True)
        answer_content += delta.content
```

### **返回结果**

```
====================思考过程====================

好的，用户问“你是谁”，我需要给出一个清晰且友好的回答。首先，应该明确自己的身份，即千问，由阿里巴巴集团旗下的通义实验室研发。接下来，要说明自己的主要功能，比如回答
====================完整回复====================

我是千问，是阿里巴巴集团旗下的通义实验室研发的超大规模语言模型。我能够回答问题、创作文字、逻辑推理、编程等，旨在为用户提供帮助和便利。有什么我可以帮您的吗？
```

## Node.js

### **示例代码**

```
import OpenAI from "openai";
import process from 'process';

// 初始化 openai 客户端
const openai = new OpenAI({
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY, // 从环境变量读取
    // 各地域配置不同，请根据实际地域修改
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;


async function main() {
    try {
        const messages = [{ role: 'user', content: '你是谁' }];
        const stream = await openai.chat.completions.create({
            model: 'qwen-plus',
            messages,
            stream: true,
            // enable_thinking 参数开启思考过程，thinking_budget 参数设置最大推理过程 Token 数
            enable_thinking: true,
            thinking_budget: 50
        });
        console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\nUsage:');
                console.log(chunk.usage);
                continue;
            }

            const delta = chunk.choices[0].delta;
            
            // 只收集思考内容
            if (delta.reasoning_content !== undefined && delta.reasoning_content !== null) {
                if (!isAnswering) {
                    process.stdout.write(delta.reasoning_content);
                }
                reasoningContent += delta.reasoning_content;
            }

            // 收到content，开始进行回复
            if (delta.content !== undefined && delta.content) {
                if (!isAnswering) {
                    console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
                    isAnswering = true;
                }
                process.stdout.write(delta.content);
                answerContent += delta.content;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

### **返回结果**

```
====================思考过程====================

好的，用户问“你是谁”，我需要给出一个清晰准确的回答。首先，我应该介绍自己的身份，即千问，由阿里巴巴集团旗下的通义实验室研发。接下来，要说明我的主要功能，比如回答问题
====================完整回复====================

我是千问，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够回答问题、创作文字、逻辑推理、编程等多种任务。如果你有任何问题或需要帮助，欢迎随时告诉我！
```

## HTTP

### **示例代码**

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域配置不同，请根据实际地域修改/chat/completions
# === 执行时请删除该注释 ===
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "user", 
            "content": "你是谁"
        }
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    },
    "enable_thinking": true,
    "thinking_budget": 50
}'
```

### **返回结果**

```
data: {"choices":[{"delta":{"content":null,"role":"assistant","reasoning_content":""},"index":0,"logprobs":null,"finish_reason":null}],"object":"chat.completion.chunk","usage":null,"created":1745485391,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-e2edaf2c-8aaf-9e54-90e2-b21dd5045503"}

.....

data: {"choices":[{"finish_reason":"stop","delta":{"content":"","reasoning_content":null},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1745485391,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-e2edaf2c-8aaf-9e54-90e2-b21dd5045503"}

data: {"choices":[],"object":"chat.completion.chunk","usage":{"prompt_tokens":10,"completion_tokens":360,"total_tokens":370},"created":1745485391,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-e2edaf2c-8aaf-9e54-90e2-b21dd5045503"}

data: [DONE]
```

## DashScope

> Qwen3.5系列的DashScope API采用多模态接口，以下示例会报错`url error`，调用方式请参见[开启/关闭思考模式](https://help.aliyun.com/zh/model-studio/vision#bc67a9a2bd2of)。

## Python

### **示例代码**

```
import os
from dashscope import Generation
import dashscope 

# 各地域配置不同，请根据实际地域修改
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

messages = [{"role": "user", "content": "你是谁？"}]


completion = Generation.call(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-plus",
    messages=messages,
    result_format="message",
    enable_thinking=True,
    # 设置最大推理过程 Token 数
    thinking_budget=50,
    stream=True,
    incremental_output=True,
)

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""
# 判断是否结束思考过程并开始回复
is_answering = False

print("=" * 20 + "思考过程" + "=" * 20)

for chunk in completion:
    # 如果思考过程与回复皆为空，则忽略
    if (
        chunk.output.choices[0].message.content == ""
        and chunk.output.choices[0].message.reasoning_content == ""
    ):
        pass
    else:
        # 如果当前为思考过程
        if (
            chunk.output.choices[0].message.reasoning_content != ""
            and chunk.output.choices[0].message.content == ""
        ):
            print(chunk.output.choices[0].message.reasoning_content, end="", flush=True)
            reasoning_content += chunk.output.choices[0].message.reasoning_content
        # 如果当前为回复
        elif chunk.output.choices[0].message.content != "":
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
            print(chunk.output.choices[0].message.content, end="", flush=True)
            answer_content += chunk.output.choices[0].message.content

# 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(f"{reasoning_content}")
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(f"{answer_content}")
```

### **返回结果**

```
====================思考过程====================
好的，用户问“你是谁？”，我需要给出一个清晰且友好的回答。首先，我要介绍自己的身份，也就是千问，由阿里巴巴集团旗下的通义实验室研发。接下来，应该说明我的主要功能，比如
====================完整回复====================
我是千问，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够回答问题、创作文字、逻辑推理、编程等，旨在为用户提供全面、准确和有用的信息与帮助。有什么我可以帮您的吗？
```

## Java

### **示例代码**

```
// dashscope SDK的版本 >= 2.19.4
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;
import java.lang.System;
import java.util.Arrays;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;
    // 各地域配置不同，请根据实际地域修改
    // static {Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";}

    private static void handleGenerationResult(GenerationResult message) {
        String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        String content = message.getOutput().getChoices().get(0).getMessage().getContent();

        if (!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (!content.isEmpty()) {
            finalContent.append(content);
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(content);
        }
    }
    private static GenerationParam buildGenerationParam(Message userMsg) {
        return GenerationParam.builder()
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-plus")
                .enableThinking(true)
                .thinkingBudget(50)
                .incrementalOutput(true)
                .resultFormat("message")
                .messages(Arrays.asList(userMsg))
                .build();
    }
    public static void streamCallWithMessage(Generation gen, Message userMsg)
            throws NoApiKeyException, ApiException, InputRequiredException {
        GenerationParam param = buildGenerationParam(userMsg);
        Flowable<GenerationResult> result = gen.streamCall(param);
        result.blockingForEach(message -> handleGenerationResult(message));
    }

    public static void main(String[] args) {
        try {
            Generation gen = new Generation();
            Message userMsg = Message.builder().role(Role.USER.getValue()).content("你是谁？").build();
            streamCallWithMessage(gen, userMsg);
//             打印最终结果
//            if (reasoningContent.length() > 0) {
//                System.out.println("\n====================完整回复====================");
//                System.out.println(finalContent.toString());
//            }
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

### **返回结果**

```
====================思考过程====================
好的，用户问“你是谁？”，我需要给出一个清晰且友好的回答。首先，我要介绍自己的身份，也就是千问，由阿里巴巴集团旗下的通义实验室研发。接下来，应该说明我的主要功能，比如
====================完整回复====================
我是千问，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我能够回答问题、创作文字、逻辑推理、编程等，旨在为用户提供全面、准确和有用的信息与帮助。有什么我可以帮您的吗？
```

## HTTP

### **示例代码**

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 各地域base_url的不同，请根据实际地域修改
# === 执行时请删除该注释 ===
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen-plus",
    "input":{
        "messages":[      
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    },
    "parameters":{
        "enable_thinking": true,
        "thinking_budget": 50,
        "incremental_output": true,
        "result_format": "message"
    }
}'
```

### **返回结果**

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"好的","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":14,"output_tokens":3,"input_tokens":11,"output_tokens_details":{"reasoning_tokens":1}},"request_id":"2ce91085-3602-9c32-9c8b-fe3d583a2c38"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"，","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":15,"output_tokens":4,"input_tokens":11,"output_tokens_details":{"reasoning_tokens":2}},"request_id":"2ce91085-3602-9c32-9c8b-fe3d583a2c38"}

......

id:133
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"！","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":149,"output_tokens":138,"input_tokens":11,"output_tokens_details":{"reasoning_tokens":50}},"request_id":"2ce91085-3602-9c32-9c8b-fe3d583a2c38"}

id:134
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"","role":"assistant"},"finish_reason":"stop"}]},"usage":{"total_tokens":149,"output_tokens":138,"input_tokens":11,"output_tokens_details":{"reasoning_tokens":50}},"request_id":"2ce91085-3602-9c32-9c8b-fe3d583a2c38"}
```

### **其它功能**

-   [多轮对话](https://help.aliyun.com/zh/model-studio/multi-round-conversation#9c315c95a8omt)
    
-   [工具调用](https://help.aliyun.com/zh/model-studio/qwen-function-calling#fbf3d739f2q9f)
    
-   [联网搜索](https://help.aliyun.com/zh/model-studio/web-search#9b41940862qf3)
    

## **计费说明**

-   思考内容按照输出 Token 计费。
    
-   部分混合思考模型在思考与非思考模式下的价格不同。
    
    > 若模型在思考模式下未输出思考过程，按照非思考模式价格计费。
    

## **常见问题**

### **Q：怎么关闭思考模式？**

是否能关闭思考模式取决于所用模型类型：

-   若使用混合思考模式模型（如qwen-plus、deepseek-v3.2-exp），将enable\_thinking设为false即可关闭；
    
-   若使用仅思考模式模型（如qwen3-235b-a22b-thinking-2507、deepseek-r1），则无法关闭。
    

### **Q：哪些模型支持非流式输出？**

深度思考模型在回复前需进行思考，导致等待回复时间变长，且非流式输出有超时风险，建议使用流式调用。如需非流式输出，请使用以下支持的模型。

## Qwen3

-   **商业版**
    
    -   **千问Max系列**：qwen3-max-preview
        
    -   **千问Plus系列**：qwen3.5-plus、qwen3.5-plus-2026-02-15、qwen-plus
        
    -   **千问Flash系列**：qwen-flash、qwen-flash-2025-07-28
        
    -   **千问Turbo系列**：qwen-turbo
        
-   **开源版**
    
    -   qwen3.5-397b-a17b、qwen3-next-80b-a3b-thinking、qwen3-235b-a22b-thinking-2507、qwen3-30b-a3b-thinking-2507
        

## DeepSeek

deepseek-v3.2、deepseek-v3.2-exp、deepseek-r1、deepseek-r1-0528、deepseek-r1蒸馏模型

## **GLM**

glm-4.6

## Kimi

kimi-k2-thinking

### **Q：**[免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)**用完后如何购买 Token？**

您可以访问[费用与成本](https://usercenter2.aliyun.com/home)中心进行充值，确保您的账户没有欠费即可调用模型。

> 超出免费额度后，调用模型会自动扣费，出账周期为分钟级，消费明细请前往**[账单详情](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)**进行查看。

### **Q：如何接入** [**Chatbox**](https://chatboxai.app/zh)**、**[**Cherry Studio**](https://cherry-ai.com/)**、**[Cline](https://cline.bot/)**或** [Dify](https://cloud.dify.ai/apps)**？**

请根据您的使用情况参考以下步骤：

> 此处以使用较多的工具为例，其它大模型工具接入的方法较为类似。

## Chatbox

请参见[Chatbox](https://help.aliyun.com/zh/model-studio/chatbox)。

## Cherry Studio

请参见[Cherry Studio](https://help.aliyun.com/zh/model-studio/cherry-studio)。

## Cline

请参见[Cline](https://help.aliyun.com/zh/model-studio/cline)。

## Dify

请参见[Dify](https://help.aliyun.com/zh/model-studio/dify)。

### **Q：**可以上传图片或文档进行提问吗**？**

本文介绍模型仅支持文本输入。Qwen3-VL、QVQ 模型支持对图片进行深度思考，[Qwen- Long](https://help.aliyun.com/zh/model-studio/long-context-qwen-long)模型支持文档输入。

### **Q：如何在使用 LangChain 时输出思考过程？**

请参考以下步骤：

1.  **更新依赖库**
    
    确保 `langchain_community` 和 `dashscope` 为最新版本：
    
    ```
    pip install -U langchain_community dashscope
    ```
    
2.  **调用深度思考模型**
    
    您可以通过以下代码来分开打印“思考过程”与“回复内容”：
    
    ```
    from langchain_community.chat_models.tongyi import ChatTongyi
    from langchain_core.messages import HumanMessage
    
    chatLLM = ChatTongyi(
        # 您可按需更换为其它深度思考模型
        model="qwen-plus",
        model_kwargs={
            "enable_thinking":True
        }
    )
    completion = chatLLM.stream(
        [HumanMessage(content="你是谁")])
    is_answering = False
    print("="*20+"思考过程 "+"="*20)
    for chunk in completion:
        if chunk.additional_kwargs.get("reasoning_content"):
            print(chunk.additional_kwargs.get("reasoning_content"),end="",flush=True)
        else:   
            if not is_answering:
                print("\n"+"="*20+"回复内容"+"="*20)
                is_answering = True
            print(chunk.content,end="",flush=True)
    ```
    
    可以获得如下输出：
    
    ```
    ====================思考过程 ====================
    好的，用户问“你是谁”，我需要给出一个准确且友好的回答。首先，我应该介绍自己的名字和基本功能，让用户了解我的用途。然后，可能需要提到我是通义实验室研发的，这样增加权威性。还要说明我能做什么，比如回答问题、创作文字等，这样用户知道可以怎么使用我。同时，保持语气亲切，避免太技术化的术语，让回答更易懂。另外，可能需要检查是否有遗漏的信息，比如多语言支持或者应用场景，但用户的问题比较基础，可能不需要太详细。最后，确保回答简洁明了，不冗长，符合用户的快速获取信息的需求。
    ====================回复内容====================
    我是Qwen3，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你回答问题、创作文字（如写故事、公文、邮件、剧本等）、进行逻辑推理、编程，甚至表达观点和玩游戏。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等，旨在为全球用户提供高效、便捷的服务。如果你有任何问题或需要帮助，欢迎随时告诉我！
    ```
    

### **Q：如何查看Token**消耗**量**及**调用次数？**

模型调用完**一小时后**，在模型监控（[北京](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)或[新加坡](https://modelstudio.console.aliyun.com/?tab=model#/model-telemetry)）页面设置查询条件（例如，选择时间范围、业务空间等），再在**模型列表**区域找到目标模型并单击**操作**列的**监控**，即可查看该模型的调用统计结果。具体请参见[模型监控](https://help.aliyun.com/zh/model-studio/model-telemetry/)文档。

> 数据按小时更新，高峰期可能有小时级延迟，请您耐心等待。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6923304571/p992753.png)

## API 参考

深度思考模型的输入与输出参数请参见[千问](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)。

## **错误码**

如果执行报错，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

执行信息抽取或结构化数据生成任务时，大模型可能返回多余文本（如 ` ```json `）导致下游解析失败。开启结构化输出（JSON Mode）可确保大模型输出标准格式的 JSON 字符串，避免额外的格式验证或重试。

## 使用方式

在请求体中设置 `response_format` 参数即可开启结构化输出：

1.  **设置**`**response_format**`**参数**：将 `response_format` 参数设置为 `{"type": "json_object"}`。
    
2.  **提示词包含 JSON 关键词**：System Message 或 User Message 中需要包含 "JSON" 关键词（不区分大小写），否则会报错：`'messages' must contain the word 'json' in some form, to use 'response_format' of type 'json_object'.`
    

## **支持的模型**

## 千问

-   **文本生成模型**
    
    -   千问Max 系列：qwen3-max、qwen3-max-2026-01-23（非思考模式）、qwen3-max-2025-09-23、qwen3-max-preview（非思考模式）、qwen-max、qwen-max-latest、qwen-max-2024-09-19 及之后的快照模型
        
    -   千问Plus 系列（非思考模式）：qwen3.5-plus、qwen3.5-plus-2026-02-15、qwen-plus、qwen-plus-latest、qwen-plus-2024-12-20及之后的快照模型
        
    -   千问Flash 系列（非思考模式）：qwen3.5-flash、qwen3.5-flash-2026-02-23及之后的快照模型、qwen-flash、qwen-flash-2025-07-28及之后的快照模型
        
    -   千问Turbo 系列（非思考模式）：qwen-turbo、qwen-turbo-latest、qwen-turbo-2024-11-01及之后的快照模型
        
    -   千问Coder 系列：qwen3-coder-plus、qwen3-coder-plus-2025-07-22、qwen3-coder-flash、qwen3-coder-flash-2025-07-28
        
    -   千问Long 系列：qwen-long、qwen-long-latest、qwen-long-2025-01-25
        
-   **文本生成开源模型**
    
    -   Qwen3.5（非思考模式）：qwen3.5-397b-a17b、qwen3.5-122b-a10b、qwen3.5-27b、qwen3.5-35b-a3b
        
    -   Qwen3（非思考模式）
        
    -   Qwen3-Coder
        
    -   Qwen2.5 系列的文本模型（不含math与coder模型）
        
-   **多模态模型**
    
    -   千问3-VL-Plus 系列（非思考模式）：qwen3-vl-plus、qwen3-vl-plus-2025-09-23及之后的快照模型
        
    -   千问3-VL-Flash 系列（非思考模式）：qwen3-vl-flash、qwen3-vl-flash-2025-10-15及之后的快照模型
        
    -   千问VL-Max 系列：qwen-vl-max（不包括最新版与快照版模型）
        
    -   千问VL-Plus 系列：qwen-vl-plus（不包括最新版与快照版模型）
        
-   **多模态开源模型**
    
    -   Qwen3-VL（非思考模式）
        

## Kimi

kimi-k2-thinking

## **GLM**

-   非思考模式：glm-5、glm-4.7、glm-4.6
    
-   glm-4.5
    
-   glm-4.5-air
    

模型的上下文、价格、快照版本等信息请参见[模型列表](https://help.aliyun.com/zh/model-studio/models)。

## **快速开始**

以从个人简介中抽取信息的简单场景为例，介绍快速使用结构化输出的方法。

您需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过OpenAI SDK或DashScope SDK进行调用，还需要[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

## OpenAI兼容

## Python

```
from openai import OpenAI
import os

client = OpenAI(
    # 如果没有配置环境变量，请用API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen-flash",
    messages=[
        {
            "role": "system",
            "content": "请抽取用户的姓名与年龄信息，以JSON格式返回"
        },
        {
            "role": "user",
            "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游", 
        },
    ],
    response_format={"type": "json_object"}
)

json_string = completion.choices[0].message.content
print(json_string)
```

### **返回结果**

```
{
  "姓名": "刘五",
  "年龄": 34
}
```

## Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    // 如果没有配置环境变量，请用API Key将下行替换为：apiKey: "sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

const completion = await openai.chat.completions.create({
    model: "qwen-flash",
    messages: [
        {
            role: "system",
            content: "请抽取用户的姓名与年龄信息，以JSON格式返回"
        },
        {
            role: "user",
            content: "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"
        }
    ],
    response_format: {
        type: "json_object"
    }
});

const jsonString = completion.choices[0].message.content;
console.log(jsonString);
```

### **返回结果**

```
{
  "姓名": "刘五",
  "年龄": 34
}
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "system",
            "content": "请抽取用户的姓名与年龄信息，以JSON格式返回"
        },
        {
            "role": "user", 
            "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com"
        }
    ],
    "response_format": {
        "type": "json_object"
    }
}'
```

### **返回结果**

```
{
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "{\"name\":\"刘五\",\"age\":\"34岁\"}"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
        }
    ],
    "object": "chat.completion",
    "usage": {
        "prompt_tokens": 207,
        "completion_tokens": 20,
        "total_tokens": 227,
        "prompt_tokens_details": {
            "cached_tokens": 0
        }
    },
    "created": 1756455080,
    "system_fingerprint": null,
    "model": "qwen-plus",
    "id": "chatcmpl-624b665b-fb93-99e7-9ebd-bb6d86d314d2"
}
```

## DashScope

## Python

```
import os
import dashscope

# 若使用新加坡地域的模型，请释放下列注释
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"
messages=[
    {
        "role": "system",
        "content": "请抽取用户的姓名与年龄信息，以JSON格式返回"
    },
    {
        "role": "user",
        "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游", 
    },
]
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-flash", 
    messages=messages,
    result_format='message',
    response_format={'type': 'json_object'}
    )
json_string = response.output.choices[0].message.content
print(json_string)
```

### **返回结果**

```
{
  "姓名": "刘五",
  "年龄": 34
}
```

## Java

DashScope Java SDK 版本需要不低于 2.18.4。

```
// DashScope Java SDK 版本需要不低于 2.18.4

import java.util.Arrays;
import java.lang.System;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.common.ResponseFormat;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 若使用新加坡地域的模型，请释放下列注释
    // static {Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";}
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        Message systemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .content("请抽取用户的姓名与年龄信息，以JSON格式返回")
                .build();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游")
                .build();
        ResponseFormat jsonMode = ResponseFormat.builder().type("json_object").build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-flash")
                .messages(Arrays.asList(systemMsg, userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .responseFormat(jsonMode)
                .build();
        return gen.call(param);
    }

    public static void main(String[] args) {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            // 使用日志框架记录异常信息
            System.err.println("An error occurred while calling the generation service: " + e.getMessage());
        }
    }
}
```

### **返回结果**

```
{
  "姓名": "刘五",
  "年龄": 34
}
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
# === 执行时请删除该注释 ===
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-flash",
    "input": {
        "messages": [
            {
                "role": "system",
                "content": "请抽取用户的姓名与年龄信息，以JSON格式返回"
            },
            {
                "role": "user", 
                "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"
            }
        ]
    },
    "parameters": {
        "result_format": "message",
        "response_format": {
            "type": "json_object"
        }
    }
}'
```

### **返回结果**

```
{
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": "{\n  \"姓名\": \"刘五\",\n  \"年龄\": 34\n}"
                }
            }
        ]
    },
    "usage": {
        "total_tokens": 72,
        "output_tokens": 18,
        "input_tokens": 54,
        "cached_tokens": 0
    },
    "request_id": "xxx-xxx-xxx-xxx-xxx"
}
```

## **图片、视频数据处理**

除了文本信息，多模态模型还支持针对图像、视频数据进行结构化输出，实现视觉信息抽取、定位、事件监测等功能。

> 图片、视频文件限制请参见[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision#430cb5ea4cety)。

## OpenAI兼容

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3-vl-plus",
    messages=[
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are a helpful assistant."}],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"
                    },
                },
                {"type": "text", "text": "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"},
            ],
        },
    ],
    response_format={"type": "json_object"}
)
json_string = completion.choices[0].message.content
print(json_string)
```

### **返回结果**

```
{
  "ticket": [
    {
      "travel_date": "2013-06-29",
      "trains": "流水",
      "seat_num": "371",
      "arrival_site": "开发区",
      "price": "8.00"
    }
  ],
  "invoice": [
    {
      "invoice_code": "221021325353",
      "invoice_number": "10283819"
    }
  ]
}
```

## Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
  // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
  // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
  apiKey: process.env.DASHSCOPE_API_KEY,
  // 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
  baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

async function main() {
  const response = await openai.chat.completions.create({
    model: "qwen3-vl-plus",
    messages: [{
        role: "system",
        content: [{
          type: "text",
          text: "You are a helpful assistant."
        }]
      },
      {
        role: "user",
        content: [{
            type: "image_url",
            image_url: {
              "url": "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"
            }
          },
          {
            type: "text",
            text: "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"
          }
        ]
      }
    ],
    response_format: {type: "json_object"}
  });
  console.log(response.choices[0].message.content);
}

main()
```

### **返回结果**

```
{
  "ticket": [
    {
      "travel_date": "2013-06-29",
      "trains": "流水",
      "seat_num": "371",
      "arrival_site": "开发区",
      "price": "8.00"
    }
  ],
  "invoice": [
    {
      "invoice_code": "221021325353",
      "invoice_number": "10283819"
    }
  ]
}
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "qwen3-vl-plus",
  "messages": [
  {"role":"system",
  "content":[
    {"type": "text", "text": "You are a helpful assistant."}]},
  {
    "role": "user",
    "content": [
      {"type": "image_url", "image_url": {"url": "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"}},
      {"type": "text", "text": "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"}
    ]
  }],
  "response_format":{"type": "json_object"}
}'
```

### **返回结果**

```
{
  "choices": [{
    "message": {
      "content": "{\n  \"ticket\": [\n    {\n      \"travel_date\": \"2013-06-29\",\n      \"trains\": \"流水\",\n      \"seat_num\": \"371\",\n      \"arrival_site\": \"开发区\",\n      \"price\": \"8.00\"\n    }\n  ],\n  \"invoice\": [\n    {\n      \"invoice_code\": \"221021325353\",\n      \"invoice_number\": \"10283819\"\n    }\n  ]\n}",
      "role": "assistant"
    },
    "finish_reason": "stop",
    "index": 0,
    "logprobs": null
  }],
  "object": "chat.completion",
  "usage": {
    "prompt_tokens": 486,
    "completion_tokens": 112,
    "total_tokens": 598,
    "prompt_tokens_details": {
      "cached_tokens": 0
    }
  },
  "created": 1755767481,
  "system_fingerprint": null,
  "model": "qwen3-vl-plus",
  "id": "chatcmpl-33249829-e9f3-9cbc-93e4-0536b3d7d713"
}
```

## DashScope

## Python

```
import os
import dashscope

# 若使用新加坡地域的模型，请释放下列注释
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"
messages = [
{
    "role": "system",
    "content": [
    {"text": "You are a helpful assistant."}]
},
{
    "role": "user",
    "content": [
    {"image": "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"},
    {"text": "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"}]
}]
response = dashscope.MultiModalConversation.call(
    #若没有配置环境变量， 请用百炼API Key将下行替换为： api_key ="sk-xxx"
    api_key = os.getenv('DASHSCOPE_API_KEY'),
    model = 'qwen3-vl-plus',
    messages = messages,
    response_format={'type': 'json_object'}
)
json_string = response.output.choices[0].message.content[0]["text"]
print(json_string)
```

```
import os
import dashscope

# 若使用北京地域的模型，需将base_url替换为：https://dashscope.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'

messages = [
{
    "role": "system",
    "content": [
    {"text": "You are a helpful assistant."}]
},
{
    "role": "user",
    "content": [
    {"image": "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"},
    {"text": "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"}]
}]
response = dashscope.MultiModalConversation.call(
    #若没有配置环境变量， 请用百炼API Key将下行替换为： api_key ="sk-xxx"
    api_key = os.getenv('DASHSCOPE_API_KEY'),
    model = 'qwen3-vl-plus',
    messages = messages,
    response_format={'type': 'json_object'}
)
json_string = response.output.choices[0].message.content[0]["text"]
print(json_string)
```

### **返回结果**

```
{
  "ticket": [
    {
      "travel_date": "2013-06-29",
      "trains": "流水",
      "seat_num": "371",
      "arrival_site": "开发区",
      "price": "8.00"
    }
  ],
  "invoice": [
    {
      "invoice_code": "221021325353",
      "invoice_number": "10283819"
    }
  ]
}
```

## Java

```
// DashScope Java SDK 版本需要不低于 2.21.4

import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.common.ResponseFormat;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 若使用新加坡地域的模型，请释放下列注释
    // static {Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";}
    
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage systemMessage = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("text", "You are a helpful assistant."))).build();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("image", "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"),
                        Collections.singletonMap("text", "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"))).build();
        ResponseFormat jsonMode = ResponseFormat.builder().type("json_object").build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3-vl-plus")
                .messages(Arrays.asList(systemMessage, userMessage))
                .responseFormat(jsonMode)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }
    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

### **返回结果**

```
{
  "ticket": [
    {
      "travel_date": "2013-06-29",
      "trains": "流水",
      "seat_num": "371",
      "arrival_site": "开发区",
      "price": "8.00"
    }
  ],
  "invoice": [
    {
      "invoice_code": "221021325353",
      "invoice_number": "10283819"
    }
  ]
}
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
# === 执行时请删除该注释 ===
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3-vl-plus",
    "input":{
        "messages":[
            {"role": "system",
         "content": [
           {"text": "You are a helpful assistant."}]},
            {
             "role": "user",
             "content": [
               {"image": "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"},
               {"text": "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"}
                ]
            }
        ]
    },
    "parameters": {
        "response_format": {"type": "json_object"}
    }
}'
```

### **返回结果**

```
{
  "output": {
    "choices": [
      {
        "message": {
          "content": [
            {
              "text": "{\n  \"ticket\": [\n    {\n      \"travel_date\": \"2013-06-29\",\n      \"trains\": \"流水\",\n      \"seat_num\": \"371\",\n      \"arrival_site\": \"开发区\",\n      \"price\": \"8.00\"\n    }\n  ],\n  \"invoice\": [\n    {\n      \"invoice_code\": \"221021325353\",\n      \"invoice_number\": \"10283819\"\n    }\n  ]\n}"
            }
          ],
          "role": "assistant"
        },
        "finish_reason": "stop"
      }
    ]
  },
  "usage": {
    "total_tokens": 598,
    "input_tokens_details": {
      "image_tokens": 418,
      "text_tokens": 68
    },
    "output_tokens": 112,
    "input_tokens": 486,
    "output_tokens_details": {
      "text_tokens": 112
    },
    "image_tokens": 418
  },
  "request_id": "b129dce1-0d5d-4772-b8b5-bd3a1d5cde63"
}
```

## **思考模型的结构化输出**

启用思考模型的结构化输出功能后，模型会先推理，再生成 JSON。相比非思考模型，输出结果通常更准确。该功能仅支持glm-4.5、glm-4.5-air与kimi-k2-thinking。

## OpenAI兼容

## Python

### **示例代码**

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

messages=[
    {
        "role": "system",
        "content": "请抽取用户的姓名与年龄信息，以JSON格式返回"
    },
    {
        "role": "user",
        "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游", 
    },
]

completion = client.chat.completions.create(
    model="kimi-k2-thinking",
    messages=messages,
    extra_body={"enable_thinking": True},
    stream=True,
    stream_options={
        "include_usage": True
    },
    response_format={"type": "json_object"}
)

reasoning_content = ""  # 完整思考过程
answer_content = ""  # 完整回复
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    if not chunk.choices:
        print("\nUsage:")
        print(chunk.usage)
        continue

    delta = chunk.choices[0].delta

    # 只收集思考内容
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
        reasoning_content += delta.reasoning_content

    # 收到content，开始进行回复
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
            is_answering = True
        print(delta.content, end="", flush=True)
        answer_content += delta.content
```

### **返回结果**

```
====================思考过程====================

用户要求抽取姓名与年龄信息，并以JSON格式返回。

从文本中可以看到：
- 姓名：刘五
- 年龄：34
- 邮箱：liuwu@example.com（但用户只要求姓名和年龄）
- 爱好：打篮球和旅游（但用户只要求姓名和年龄）

根据要求，只需要提取姓名和年龄信息，并以JSON格式返回。

JSON格式应该是：
{
  "姓名": "刘五",
  "年龄": 34
}

或者使用英文键名：
{
  "name": "刘五",
  "age": 34
}

考虑到用户使用的是中文提问，使用中文键名可能更合适。不过通常JSON键名使用英文也是常见做法。这里我采用中文键名，因为用户的指令是中文的，且提取的信息也是中文语境下的。

最终输出：
{
  "姓名": "刘五",
  "年龄": 34
}
====================完整回复====================

{"姓名":"刘五","年龄":34}
Usage:
CompletionUsage(completion_tokens=203, prompt_tokens=48, total_tokens=251, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=190, rejected_prediction_tokens=None), prompt_tokens_details=None)
```

## Node.js

### **示例代码**

```
import OpenAI from "openai";
import process from 'process';

// 初始化 openai 客户端
const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY, // 从环境变量读取
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;

async function main() {
    try {
        const messages = [
            {
                "role": "system",
                "content": "请抽取用户的姓名与年龄信息，以JSON格式返回"
            },
            {
                "role": "user",
                "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游", 
            },
        ];
        const stream = await openai.chat.completions.create({
            model: 'glm-4.5',
            messages,
            stream: true,
            enable_thinking: true,
            response_format: {type: 'json_object'},
        });
        console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\nUsage:');
                console.log(chunk.usage);
                continue;
            }

            const delta = chunk.choices[0].delta;
            
            // 只收集思考内容
            if (delta.reasoning_content !== undefined && delta.reasoning_content !== null) {
                if (!isAnswering) {
                    process.stdout.write(delta.reasoning_content);
                }
                reasoningContent += delta.reasoning_content;
            }

            // 收到content，开始进行回复
            if (delta.content !== undefined && delta.content) {
                if (!isAnswering) {
                    console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
                    isAnswering = true;
                }
                process.stdout.write(delta.content);
                answerContent += delta.content;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

### **返回结果**

```
====================思考过程====================

1.  **分析用户请求：**
    *   **核心任务：** 从给定文本中提取特定信息。
    *   **目标信息：** “姓名”和“年龄”。
    *   **输入文本：** “大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游”
    *   **输出格式：** “JSON格式”。

2.  **将输入文本分解为关键信息片段：**
......
    *   我应该以一个干净、不包含额外文本、可直接使用的JSON格式呈现最终答案。除非用户另有说明，否则无需向JSON本身添加对话性填充内容。

这个过程从理解请求、分解输入、提取数据、选择正确的格式和结构，到最终组装，确保了满足用户的所有约束条件。
====================完整回复====================

{  "姓名": "刘五",
  "年龄": 34
}
```

## HTTP

### **示例代码**

## curl

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "glm-4.5",
    "messages": [
    {
            "role": "system",
            "content": "请抽取用户的姓名与年龄信息，以JSON格式返回"
        },
        {
            "role": "user", 
            "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"
        }
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    },
    "enable_thinking": true,
    "response_format": {
        "type": "json_object"
    }
}'
```

## DashScope

## Python

### **示例代码**

```
import os
from dashscope import Generation
import dashscope 

messages = [
    {
        "role": "system",
        "content": "请抽取用户的姓名与年龄信息，以JSON格式返回"
    },
    {"role": "user", "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}
]

completion = Generation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="glm-4.5",
    messages=messages,
    result_format="message",
    enable_thinking=True,
    response_format={"type": "json_object"},
    stream=True,
    incremental_output=True
)

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""
# 判断是否结束思考过程并开始回复
is_answering = False

print("=" * 20 + "思考过程" + "=" * 20)

for chunk in completion:
    # 如果思考过程与回复皆为空，则忽略
    if (
        chunk.output.choices[0].message.content == ""
        and chunk.output.choices[0].message.reasoning_content == ""
    ):
        pass
    else:
        # 如果当前为思考过程
        if (
            chunk.output.choices[0].message.reasoning_content != ""
            and chunk.output.choices[0].message.content == ""
        ):
            print(chunk.output.choices[0].message.reasoning_content, end="", flush=True)
            reasoning_content += chunk.output.choices[0].message.reasoning_content
        # 如果当前为回复
        elif chunk.output.choices[0].message.content != "":
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
            print(chunk.output.choices[0].message.content, end="", flush=True)
            answer_content += chunk.output.choices[0].message.content
```

### **返回结果**

```
====================思考过程====================
1.  **识别用户目标：**用户希望我从他们的句子中提取特定的信息（姓名和年龄），并以特定的格式（JSON）返回。
...
7.  **最终审查：**
    *   JSON是否包含姓名“刘五”？是的。
    *   JSON是否包含年龄34？是的。
    *   格式是有效的JSON吗？是的。
    *   它是否直接回答了用户的请求？是的。

这个过程很简单，因为它是一个直接的信息提取任务。关键在于解析中文句子以找到模式（“我叫...”，“今年...岁”），然后按照要求正确格式化提取的数据。
====================完整回复====================
{  "姓名": "刘五",
  "年龄": 34
}
```

## Java

### **示例代码**

```
// dashscope SDK的版本 >= 2.19.4
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import io.reactivex.Flowable;
import java.lang.System;
import java.util.Arrays;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.alibaba.dashscope.common.ResponseFormat;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;

    private static void handleGenerationResult(GenerationResult message) {
        String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        String content = message.getOutput().getChoices().get(0).getMessage().getContent();

        if (!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (!content.isEmpty()) {
            finalContent.append(content);
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(content);
        }
    }
    private static GenerationParam buildGenerationParam(List<Message> msgs) {
        ResponseFormat jsonMode = ResponseFormat.builder().type("json_object").build();
        return GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("glm-4.5")
                .enableThinking(true)
                .incrementalOutput(true)
                .resultFormat("message")
                .messages(msgs)
                .responseFormat(jsonMode)
                .build();
    }
    public static void streamCallWithMessage(Generation gen, List<Message> msgs)
            throws NoApiKeyException, ApiException, InputRequiredException {
        GenerationParam param = buildGenerationParam(msgs);
        Flowable<GenerationResult> result = gen.streamCall(param);
        result.blockingForEach(message -> handleGenerationResult(message));
    }

    public static void main(String[] args) {
        try {
            Generation gen = new Generation();
            Message systemMsg = Message.builder().role(Role.SYSTEM.getValue()).content("请抽取用户的姓名与年龄信息，以JSON格式返回").build();
            Message userMsg = Message.builder().role(Role.USER.getValue()).content("大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游").build();
            List<Message> msgs = Arrays.asList(systemMsg, userMsg);
            streamCallWithMessage(gen, msgs);
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
    }
}
```

### **返回结果**

```
====================思考过程====================
1.  **分析用户的请求。**
    *   **用户的输入：** "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游" （大家好，我叫刘五，我今年34岁，我的邮箱是 liuwu@example.com，我喜欢打篮球和旅游。）
    *   **核心任务：** "请抽取用户的姓名与年龄信息" （请提取用户的姓名和年龄信息。）
    *   **输出格式：** "以JSON格式返回" （以JSON格式返回）。
...
6.  **审查和优化输出。**
    *   JSON格式正确吗？是的，它有花括号、双引号包裹的键、正确的值（字符串加引号，数字不加）以及键值对之间的逗号。
    *   它是否按要求包含了*仅*姓名和年龄？是的。
    *   摘取的信息是否准确？是的，“刘五”和“34”直接来自用户的文本。
    *   输出可以直接使用。无需额外的解释，除非我想增加一些礼貌性。像“好的，已为您提取信息：”这样的简单短语是很好的客户服务。我们加上这个吧。
    *   最终的响应应该是：
        *   一段简短、礼貌的开场白。
        *   包含在 ```json ... ``` 代码块中的JSON对象，以实现良好的格式化并防止转义问题。

这个思考过程从理解高层级需求，到分析输入、提取特定数据、设计输出格式、构建它，最后再为清晰和正确性进行审查。这是一个系统性的方法，确保准确性并遵循用户指令。
====================完整回复====================
{  "姓名": "刘五",
  "年龄": 34
}
```

## HTTP

### **示例代码**

## curl

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "glm-4.5",
    "input":{
        "messages":[      
            {
                "role": "system",
                "content": "请抽取用户的姓名与年龄信息，以JSON格式返回"
            },
            {
                "role": "user",
                "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"
            }
        ]
    },
    "parameters":{
        "enable_thinking": true,
        "incremental_output": true,
        "result_format": "message",
        "response_format": {
            "type": "json_object"
        }
    }
}'
```

## **优化提示词**

模糊的提示词（如“返回用户信息”）会使模型生成非预期结果。建议在提示词中准确描述预期 Schema，包括字段类型、必需性、格式要求（如日期格式），并提供示例。

## OpenAI兼容

## Python

```
from openai import OpenAI
import os
import json
import textwrap  # 用于处理多行字符串的缩进，提高代码可读性

# 预定义示例响应，用于向模型展示期望的输出格式
# 示例1：包含所有字段的完整响应
example1_response = json.dumps(
    {
        "info": {"name": "张三", "age": "25岁", "email": "zhangsan@example.com"},
        "hobby": ["唱歌"]
    },
    ensure_ascii=False
)
# 示例2：包含多个hobby的响应
example2_response = json.dumps(
    {
        "info": {"name": "李四", "age": "30岁", "email": "lisi@example.com"},
        "hobby": ["跳舞", "游泳"]
    },
    ensure_ascii=False
)
# 示例3：不包含hobby字段的响应（hobby非必需）
example3_response = json.dumps(
    {
        "info": {"name": "赵六", "age": "28岁", "email": "zhaoliu@example.com"}
    },
    ensure_ascii=False
)
# 示例4：另一个不包含hobby字段的响应
example4_response = json.dumps(
    {
        "info": {"name": "孙七", "age": "35岁", "email": "sunqi@example.com"}
    },
    ensure_ascii=False
)

# 初始化OpenAI客户端
client = OpenAI(
    # 若没有配置环境变量，请将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# dedent的作用是去除每行开头的公共缩进，使字符串在代码中可以美观地缩进，但在运行时不会包含这些额外的空格
system_prompt = textwrap.dedent(f"""\
    请从用户输入中提取个人信息并按照指定的JSON Schema格式输出：

    【输出格式要求】
    输出必须严格遵循以下JSON结构：
    {{
      "info": {{
        "name": "字符串类型，必需字段，用户姓名",
        "age": "字符串类型，必需字段，格式为'数字+岁'，例如'25岁'",
        "email": "字符串类型，必需字段，标准邮箱格式，例如'user@example.com'"
      }},
      "hobby": ["字符串数组类型，非必需字段，包含用户的所有爱好，如未提及则完全不输出此字段"]
    }}

    【字段提取规则】
    1. name: 从文本中识别用户姓名，必需提取
    2. age: 识别年龄信息，转换为"数字+岁"格式，必需提取
    3. email: 识别邮箱地址，保持原始格式，必需提取
    4. hobby: 识别用户爱好，以字符串数组形式输出，如未提及爱好信息则完全省略hobby字段

    【参考示例】
    示例1（包含爱好）：
    Q：我叫张三，今年25岁，邮箱是zhangsan@example.com，爱好是唱歌
    A：{example1_response}

    示例2（包含多个爱好）：
    Q：我叫李四，今年30岁，邮箱是lisi@example.com，平时喜欢跳舞和游泳
    A：{example2_response}

    示例3（不包含爱好）：
    Q：我叫赵六，今年28岁，我的邮箱是zhaoliu@example.com
    A：{example3_response}

    示例4（不包含爱好）：
    Q：我是孙七，35岁，邮箱sunqi@example.com
    A：{example4_response}

    请严格按照上述格式和规则提取信息并输出JSON。如果用户未提及爱好，则不要在输出中包含hobby字段。\
""")

# 调用大模型API进行信息提取
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游", 
        },
    ],
    response_format={"type": "json_object"},  # 指定返回JSON格式
)

# 提取并打印模型生成的JSON结果
json_string = completion.choices[0].message.content
print(json_string)
```

### **返回结果**

```
{
  "info": {
    "name": "刘五",
    "age": "34岁",
    "email": "liuwu@example.com"
  },
  "hobby": ["打篮球", "旅游"]  
}
```

## Node.js

```
import OpenAI from "openai";

// 预定义示例响应（用于向模型展示期望的输出格式）
// 示例1：包含所有字段的完整响应
const example1Response = JSON.stringify({
    info: { name: "张三", age: "25岁", email: "zhangsan@example.com" },
    hobby: ["唱歌"]
}, null, 2);

// 示例2：包含多个hobby的响应
const example2Response = JSON.stringify({
    info: { name: "李四", age: "30岁", email: "lisi@example.com" },
    hobby: ["跳舞", "游泳"]
}, null, 2);

// 示例3：不包含hobby字段的响应（hobby非必需）
const example3Response = JSON.stringify({
    info: { name: "赵六", age: "28岁", email: "zhaoliu@example.com" }
}, null, 2);

// 示例4：另一个不包含hobby字段的响应
const example4Response = JSON.stringify({
    info: { name: "孙七", age: "35岁", email: "sunqi@example.com" }
}, null, 2);

// 初始化OpenAI客户端配置
const openai = new OpenAI({
    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

// 创建聊天完成请求，使用结构化提示词来提高输出准确性
const completion = await openai.chat.completions.create({
    model: "qwen-plus",
    messages: [
        {
            role: "system",
            content: `请从用户输入中提取个人信息并按照指定的JSON Schema格式输出：

【输出格式要求】
输出必须严格遵循以下JSON结构：
{
  "info": {
    "name": "字符串类型，必需字段，用户姓名",
    "age": "字符串类型，必需字段，格式为'数字+岁'，例如'25岁'",
    "email": "字符串类型，必需字段，标准邮箱格式，例如'user@example.com'"
  },
  "hobby": ["字符串数组类型，非必需字段，包含用户的所有爱好，如未提及则完全不输出此字段"]
}

【字段提取规则】
1. name: 从文本中识别用户姓名，必需提取
2. age: 识别年龄信息，转换为"数字+岁"格式，必需提取
3. email: 识别邮箱地址，保持原始格式，必需提取
4. hobby: 识别用户爱好，以字符串数组形式输出，如未提及爱好信息则完全省略hobby字段

【参考示例】
示例1（包含爱好）：
Q：我叫张三，今年25岁，邮箱是zhangsan@example.com，爱好是唱歌
A：${example1Response}

示例2（包含多个爱好）：
Q：我叫李四，今年30岁，邮箱是lisi@example.com，平时喜欢跳舞和游泳
A：${example2Response}

示例3（不包含爱好）：
Q：我叫赵六，今年28岁，我的邮箱是zhaoliu@example.com
A：${example3Response}

示例4（不包含爱好）：
Q：我是孙七，35岁，邮箱sunqi@example.com
A：${example4Response}

请严格按照上述格式和规则提取信息并输出JSON。如果用户未提及爱好，则不要在输出中包含hobby字段。`
        },
        {
            role: "user",
            content: "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"
        }
    ],
    response_format: {
        type: "json_object"
    }
});

// 提取并打印模型生成的JSON结果
const jsonString = completion.choices[0].message.content;
console.log(jsonString);
```

### **返回结果**

```
{
  "info": {
    "name": "刘五",
    "age": "34岁",
    "email": "liuwu@example.com"
  },
  "hobby": [
    "打篮球",
    "旅游"
  ]
}
```

## DashScope

## Python

```
import os
import json
import dashscope

# 若使用新加坡地域的模型，请释放下列注释
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

# 预定义示例响应（用于向模型展示期望的输出格式）
example1_response = json.dumps(
    {
        "info": {"name": "张三", "age": "25岁", "email": "zhangsan@example.com"},
        "hobby": ["唱歌"]
    },
    ensure_ascii=False
)
example2_response = json.dumps(
    {
        "info": {"name": "李四", "age": "30岁", "email": "lisi@example.com"},
        "hobby": ["跳舞", "游泳"]
    },
    ensure_ascii=False
)
example3_response = json.dumps(
    {
        "info": {"name": "王五", "age": "40岁", "email": "wangwu@example.com"},
        "hobby": ["Rap", "篮球"]
    },
    ensure_ascii=False
)

messages=[
        {
            "role": "system",
            "content": f"""请从用户输入中提取个人信息并按照指定的JSON Schema格式输出：

【输出格式要求】
输出必须严格遵循以下JSON结构：
{{
  "info": {{
    "name": "字符串类型，必需字段，用户姓名",
    "age": "字符串类型，必需字段，格式为'数字+岁'，例如'25岁'",
    "email": "字符串类型，必需字段，标准邮箱格式，例如'user@example.com'"
  }},
  "hobby": ["字符串数组类型，非必需字段，包含用户的所有爱好，如未提及则完全不输出此字段"]
}}

【字段提取规则】
1. name: 从文本中识别用户姓名，必需提取
2. age: 识别年龄信息，转换为"数字+岁"格式，必需提取
3. email: 识别邮箱地址，保持原始格式，必需提取
4. hobby: 识别用户爱好，以字符串数组形式输出，如未提及爱好信息则完全省略hobby字段

【参考示例】
示例1（包含爱好）：
Q：我叫张三，今年25岁，邮箱是zhangsan@example.com，爱好是唱歌
A：{example1_response}

示例2（包含多个爱好）：
Q：我叫李四，今年30岁，邮箱是lisi@example.com，平时喜欢跳舞和游泳
A：{example2_response}

示例3（包含多个爱好）：
Q：我的邮箱是wangwu@example.com，今年40岁，名字是王五，会Rap和打篮球
A：{example3_response}

请严格按照上述格式和规则提取信息并输出JSON。如果用户未提及爱好，则不要在输出中包含hobby字段。"""
        },
        {
            "role": "user",
            "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游", 
        },
    ]
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-plus", 
    messages=messages,
    result_format='message',
    response_format={'type': 'json_object'}
    )
json_string = response.output.choices[0].message.content
print(json_string)
```

### **返回结果**

```
{
  "info": {
    "name": "刘五",
    "age": "34岁",
    "email": "liuwu@example.com"
  },
  "hobby": [
    "打篮球",
    "旅游"
  ]
}
```

## Java

```
import java.util.Arrays;
import java.lang.System;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.common.ResponseFormat;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 若使用新加坡地域的模型，请释放下列注释
    // static {Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";}
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        Message systemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .content("""
                请从用户输入中提取个人信息并按照指定的JSON Schema格式输出：

【输出格式要求】
输出必须严格遵循以下JSON结构：
{
  "info": {
    "name": "字符串类型，必需字段，用户姓名",
    "age": "字符串类型，必需字段，格式为'数字+岁'，例如'25岁'",
    "email": "字符串类型，必需字段，标准邮箱格式，例如'user@example.com'"
  },
  "hobby": ["字符串数组类型，非必需字段，包含用户的所有爱好，如未提及则完全不输出此字段"]
}

【字段提取规则】
1. name: 从文本中识别用户姓名，必需提取
2. age: 识别年龄信息，转换为"数字+岁"格式，必需提取
3. email: 识别邮箱地址，保持原始格式，必需提取
4. hobby: 识别用户爱好，以字符串数组形式输出，如未提及爱好信息则完全省略hobby字段

【参考示例】
示例1（包含爱好）：
Q：我叫张三，今年25岁，邮箱是zhangsan@example.com，爱好是唱歌
A：{"info":{"name":"张三","age":"25岁","email":"zhangsan@example.com"},"hobby":["唱歌"]}

示例2（包含多个爱好）：
Q：我叫李四，今年30岁，邮箱是lisi@example.com，平时喜欢跳舞和游泳
A：{"info":{"name":"李四","age":"30岁","email":"lisi@example.com"},"hobby":["跳舞","游泳"]}

示例3（不包含爱好）：
Q：我叫王五，我的邮箱是wangwu@example.com，今年40岁
A：{"info":{"name":"王五","age":"40岁","email":"wangwu@example.com"}}""")
                .build();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游")
                .build();
        ResponseFormat jsonMode = ResponseFormat.builder().type("json_object").build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-plus")
                .messages(Arrays.asList(systemMsg, userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .responseFormat(jsonMode)
                .build();
        return gen.call(param);
    }
    public static void main(String[] args) {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            // 使用日志框架记录异常信息
            System.err.println("An error occurred while calling the generation service: " + e.getMessage());
        }
    }
}
```

### **返回结果**

```
{
  "info": {
    "name": "刘五",
    "age": "34岁",
    "email": "liuwu@example.com"
  },
  "hobby": [
    "打篮球",
    "旅游"
  ]
}
```

## **应用于生产环境**

-   **有效性校验**
    
    将输出传递给下游业务前，建议使用工具对其进行有效性校验，如 jsonschema (Python)、Ajv (JavaScript)、Everit (Java)等**，**确保其符合预期的 JSON 结构，避免因字段缺失、类型错误或格式不规范导致下游系统解析失败、数据丢失或业务逻辑中断。失败时可通过重试、大模型改写等策略进行修复。
    
-   **禁用** `**max_tokens**`
    
    请勿在开启结构化输出时指定 `max_tokens`（控制模型输出 Token 数的参数，默认值为模型最大输出 Token 数），否则返回的 JSON 字符串可能不完整，导致下游业务解析失败。
    

## **常见问题**

### **Q：Qwen 的思考模式模型如何结构化输出？**

A：Qwen 的思考模式模型暂不支持结构化输出。如需在思考模式下获取标准 JSON 字符串，可在 JSON 解析失败时引入支持 JSON Mode 的模型进行修复。

1.  **获取思考模式下的输出**
    
    调用思考模式模型获取高质量的输出，但可能不是标准的 JSON 字符串。
    
    > 开启思考模式请勿设置`response_format`参数为`{"type": "json_object"}`，否则会报错。
    
    ```
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游",
            },
        ],
        # 开启思考模式，请勿设置response_format参数为{"type": "json_object"}，否则会报错
        extra_body={"enable_thinking": True},
        # 思考模式下需要开启流式输出
        stream=True
    )
    # 提取并打印模型生成的JSON结果
    json_string = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            json_string += chunk.choices[0].delta.content
    ```
    
2.  **校验并修复输出**
    
    尝试解析上一步获取的 `json_string`：
    
    -   若模型生成了标准格式JSON字符串，可直接解析并返回。
        
    -   若模型生成非标准格式JSON字符串，可调用支持结构化输出的模型（建议选择速度快、成本低的模型，如非思考模式的qwen-flash）修复格式。
        
    
    ```
    import json
    from openai import OpenAI
    import os
    
    # 初始化OpenAI客户端（如果前面的代码块未定义client变量，请取消下面的注释）
    # client = OpenAI(
    #     api_key=os.getenv("DASHSCOPE_API_KEY"),
    #     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    # )
    
    try:
        json_object_from_thinking_model = json.loads(json_string)
        print("生成标准格式JSON字符串")
    except json.JSONDecodeError:
        print("未生成标准格式JSON字符串，通过支持结构化输出的模型进行修复")
        completion = client.chat.completions.create(
            model="qwen-flash",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个json格式修复专家，请将用户输入的json字符串修复为标准格式",
                },
                {
                    "role": "user",
                    "content": json_string,
                },
            ],
            response_format={"type": "json_object"},
        )
        json_object_from_thinking_model = json.loads(completion.choices[0].message.content)
    ```
    

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

视觉推理模型能够先输出思考过程，再输出回答内容，适用于处理复杂的视觉分析任务，如解读数学题、分析图表数据或复杂视频理解等任务。

## **效果示例**

![QVQ Logo](https://assets.alicdn.com/g/qwenweb/qwen-webui-fe/0.0.54/static/favicon.png)

视觉推理

显示思考过程 ▼

![](https://img.alicdn.com/imgextra/i3/O1CN015BcsAj1LqLn7Cws8E_!!6000000001350-0-tps-5671-3781.jpg) 相对于您当前的位置，哪个对象在图像中的位置最远？答案选项：A.椅子 B.墙上的画 C.茶几 D.沙发。仅输出正确答案的字母（例如，A）。

发送虚拟请求

@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } } @keyframes blink { 0%, 100% { opacity: 0; } 50% { opacity: 1; } } .arrow-up { transform: rotate(180deg); } .arrow-down { transform: rotate(0deg); } .toggle-thinking:hover { background: #e6e8eb; } .send-button:hover { transform: scale(1.05); box-shadow: 0 2px 8px rgba(79, 118, 227, 0.3); }

> 以上组件仅供您参考，并未真实发送请求。

## **适用范围**

### **支持的地域**

-   北京：需使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)
    
-   弗吉尼亚：需使用该地域的API Key
    
-   新加坡：需使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)
    

### **支持的模型**

-   **Qwen3.5**
    
    -   **混合思考模型：**qwen3.5-plus、qwen3.5-plus-2026-02-15、qwen3.5-flash、qwen3.5-flash-2026-02-23、qwen3.5-397b-a17b、qwen3.5-122b-a10b、qwen3.5-27b、qwen3.5-35b-a3b
        
-   **Qwen3-VL**
    
    -   **混合思考模型：**qwen3-vl-plus、qwen3-vl-plus-2025-12-19、qwen3-vl-plus-2025-09-23、qwen3-vl-flash、qwen3-vl-flash-2025-10-15
        
    -   **仅思考模型：**qwen3-vl-235b-a22b-thinking**、**qwen3-vl-32b-thinking**、**qwen3-vl-30b-a3b-thinking**、**qwen3-vl-8b-thinking
        
-   **QVQ**
    
    **仅思考模型：**qvq-max系列、qvq-plus系列
    
-   **Kimi**
    
    **混合思考模型：**kimi-k2.5
    

## **使用方式**

-   **思考过程：** 阿里云百炼提供混合思考和仅思考两种视觉推理模型。
    
    -   **混合思考模型：**可通过`enable_thinking`控制其思考行为：
        
        -   设置为 `true`，开启思考，模型将先输出思考过程，再输出最终回复。`qwen3.5-plus`系列模型默认为`true`。
            
        -   设置为 `false`，关闭思考，模型将直接生成回复。`qwen3-vl-plus`、`qwen3-vl-flash`系列模型默认为`false`。
            
    -   **仅思考模型：**模型总会在回复前进行思考，且无法关闭。
        
-   **输出方式：**视觉推理模型包含详细的思考过程，为避免因响应内容过长导致超时，建议使用流式输出。
    
    -   Qwen3.5、Qwen3-VL、kimi-k2.5系列支持**流式和非流式**两种方式。
        
    -   QVQ系列仅支持**流式输出。**
        
-   **System Prompt使用建议：** 
    
    -   **对于单次或简单的对话调用**：为获得最佳推理效果，建议不设置 `System Message`。可将模型角色设定、输出格式要求等指令通过 `User Message` 传入。
        
    -   **对于构建 Agent 、实现工具调用等复杂应用：**可使用 `System Message` 来定义模型的角色、能力和行为框架，以确保其稳定性和可靠性。
        

## **快速开始**

**前提条件**

-   已[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    
-   如果通过 SDK 进行调用，需安装[最新版SDK](https://help.aliyun.com/zh/model-studio/install-sdk)，其中 DashScope Python SDK 版本不低于1.24.6，DashScope Java SDK 版本不低于 2.21.10。
    

下列示例演示如何调用 `qvq-max`模型，对一张包含数学题的图片进行求解，并以流式输出的方式分别打印思考过程和最终回复。

## OpenAI兼容

## Python

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用百炼API Key替换：api_key="sk-xxx"
    api_key = os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

reasoning_content = ""  # 定义完整思考过程
answer_content = ""     # 定义完整回复
is_answering = False   # 判断是否结束思考过程并开始回复

# 创建聊天完成请求
completion = client.chat.completions.create(
    model="qvq-max",  # 此处以 qvq-max 为例，可按需更换模型名称
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
                    },
                },
                {"type": "text", "text": "这道题怎么解答？"},
            ],
        },
    ],
    stream=True,
    # 解除以下注释会在最后一个chunk返回Token使用量
    # stream_options={
    #     "include_usage": True
    # }
)

print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    # 如果chunk.choices为空，则打印usage
    if not chunk.choices:
        print("\nUsage:")
        print(chunk.usage)
    else:
        delta = chunk.choices[0].delta
        # 打印思考过程
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
            print(delta.reasoning_content, end='', flush=True)
            reasoning_content += delta.reasoning_content
        else:
            # 开始回复
            if delta.content != "" and is_answering is False:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                is_answering = True
            # 打印回复过程
            print(delta.content, end='', flush=True)
            answer_content += delta.content

# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(reasoning_content)
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(answer_content)
```

## Node.js

```
import OpenAI from "openai";
import process from 'process';

// 初始化 openai 客户端
const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY, // 从环境变量读取
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;

let messages = [
    {
        role: "user",
        content: [
        { type: "image_url", image_url: { "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg" } },
        { type: "text", text: "解答这道题" },
    ]
}]

async function main() {
    try {
        const stream = await openai.chat.completions.create({
            model: 'qvq-max',
            messages: messages,
            stream: true
        });

        console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\nUsage:');
                console.log(chunk.usage);
                continue;
            }

            const delta = chunk.choices[0].delta;

            // 处理思考过程
            if (delta.reasoning_content) {
                process.stdout.write(delta.reasoning_content);
                reasoningContent += delta.reasoning_content;
            }
            // 处理正式回复
            else if (delta.content) {
                if (!isAnswering) {
                    console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
                    isAnswering = true;
                }
                process.stdout.write(delta.content);
                answerContent += delta.content;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

**点击查看思考过程和完整回复**

```
====================思考过程====================

好的，我现在要解决这个关于长方体和正方体的表面积和体积的问题。首先，我需要仔细看一下题目，确保自己理解每个部分的要求。

题目是要求分别计算两个图形的表面积和体积。第一个图形是一个长方体，第二个是一个正方体。单位都是厘米，每题6分，共12分。看起来这是一个数学作业题，可能来自小学或初中阶段的几何内容。

首先，我需要回忆一下长方体和正方体的表面积和体积的计算公式。对于长方体来说，表面积的公式是：\( 2(ab + bc + ac) \)，其中a、b、c分别是长、宽、高。而体积则是 \( abc \)。对于正方体来说，因为所有边长相等，所以表面积是 \( 6a^2 \)，体积是 \( a^3 \)。

现在来看第一个图形，这是一个长方体，给出的尺寸是长4cm，宽3cm，高2cm。我需要先计算它的表面积。根据公式，代入数值：

表面积 = \( 2(4×3 + 3×2 + 4×2) \)
        = \( 2(12 + 6 + 8) \)
        = \( 2×26 \)
        = 52 cm²

接下来是体积，同样代入数值：

体积 = \( 4×3×2 \)
      = 24 cm³

然后是第二个图形，这是一个正方体，边长为3cm。表面积计算如下：

表面积 = \( 6×3^2 \)
        = \( 6×9 \)
        = 54 cm²

体积则是：

体积 = \( 3^3 \)
      = 27 cm³

不过，我需要检查一下是否有可能出错的地方。比如，在计算长方体的表面积时，有没有可能把某个面的面积算错了？或者在乘法的时候有没有算错数字？

比如，长方体的三个不同的面分别是4×3，3×2，4×2。这三个面的面积分别是12，6，8。加起来是26，乘以2得到52，这应该是正确的。体积的话，4×3=12，再乘以2就是24，没错。

正方体的话，每个面都是3×3=9，六个面就是54，体积是3×3×3=27，也没有问题。

所以最终的答案应该是：

1. 方体的表面积是52平方厘米，体积是24立方厘米。
2. 方体的表面积是54平方厘米，体积是27立方厘米。

不过，我需要确认题目中的图形是否有其他隐藏的信息或者可能的陷阱。例如，有时候题目可能会给出一些虚线或者阴影部分，但在这个情况下，图片中的长方体和正方体看起来都是标准的，没有特别的标记。因此，我认为我的计算是正确的。

====================完整回复====================

### 解答：

**1. 方体（长4cm，宽3cm，高2cm）**
- **表面积**：
  \[
  2 \times (4 \times 3 + 3 \times 2 + 4 \times 2) = 2 \times (12 + 6 + 8) = 2 \times 26 = 52 \, \text{cm}^2
  \]
- **体积**：
  \[
  4 \times 3 \times 2 = 24 \, \text{cm}^3
  \]

**2. 方体（边长3cm）**
- **表面积**：
  \[
  6 \times 3^2 = 6 \times 9 = 54 \, \text{cm}^2
  \]
- **体积**：
  \[
  3^3 = 27 \, \text{cm}^3
  \]

**答案：**
1. 方体的表面积为 \(52 \, \text{cm}^2\)，体积为 \(24 \, \text{cm}^3\)。
2. 方体的表面积为 \(54 \, \text{cm}^2\)，体积为 \(27 \, \text{cm}^3\)。
```

## HTTP

## curl

```
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qvq-max",
    "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
          }
        },
        {
          "type": "text",
          "text": "请解答这道题"
        }
      ]
    }
  ],
    "stream":true,
    "stream_options":{"include_usage":true}
}'
```

**点击查看思考过程和完整回复**

```
data: {"choices":[{"delta":{"content":null,"role":"assistant","reasoning_content":""},"index":0,"logprobs":null,"finish_reason":null}],"object":"chat.completion.chunk","usage":null,"created":1742983020,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-ab4f3963-2c2a-9291-bda2-65d5b325f435"}

data: {"choices":[{"finish_reason":null,"delta":{"content":null,"reasoning_content":"好的"},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1742983020,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-ab4f3963-2c2a-9291-bda2-65d5b325f435"}

data: {"choices":[{"delta":{"content":null,"reasoning_content":"，"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1742983020,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-ab4f3963-2c2a-9291-bda2-65d5b325f435"}

data: {"choices":[{"delta":{"content":null,"reasoning_content":"我现在"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1742983020,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-ab4f3963-2c2a-9291-bda2-65d5b325f435"}

data: {"choices":[{"delta":{"content":null,"reasoning_content":"要"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1742983020,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-ab4f3963-2c2a-9291-bda2-65d5b325f435"}

data: {"choices":[{"delta":{"content":null,"reasoning_content":"解决"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1742983020,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-ab4f3963-2c2a-9291-bda2-65d5b325f435"}
.....
data: {"choices":[{"delta":{"content":"方"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1742983095,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-23d30959-42b4-9f24-b7ab-1bb0f72ce265"}

data: {"choices":[{"delta":{"content":"厘米"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1742983095,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-23d30959-42b4-9f24-b7ab-1bb0f72ce265"}

data: {"choices":[{"finish_reason":"stop","delta":{"content":"","reasoning_content":null},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1742983095,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-23d30959-42b4-9f24-b7ab-1bb0f72ce265"}

data: {"choices":[],"object":"chat.completion.chunk","usage":{"prompt_tokens":544,"completion_tokens":590,"total_tokens":1134,"completion_tokens_details":{"text_tokens":590},"prompt_tokens_details":{"text_tokens":24,"image_tokens":520}},"created":1742983095,"system_fingerprint":null,"model":"qvq-max","id":"chatcmpl-23d30959-42b4-9f24-b7ab-1bb0f72ce265"}

data: [DONE]
```

## DashScope

**说明**

使用 DashScope 方式调用 QVQ 模型：

-   `incremental_output` 参数默认为 `true`，且不支持设置为 `false`，仅支持增量流式返回。
    
-   `result_format`参数默认为`"message"`，且不支持设置为`"text"`
    

## Python

```
import os
from dashscope import MultiModalConversation

messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"},
            {"text": "解答这道题？"}
        ]
    }
]

response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qvq-max",  # 此处以qvq-max为例，可按需更换模型名称。
    messages=messages,
    stream=True,
)

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""
# 判断是否结束思考过程并开始回复
is_answering = False

print("=" * 20 + "思考过程" + "=" * 20)

for chunk in response:
    # 如果思考过程与回复皆为空，则忽略
    message = chunk.output.choices[0].message
    reasoning_content_chunk = message.get("reasoning_content", None)
    if (chunk.output.choices[0].message.content == [] and
        reasoning_content_chunk == ""):
        pass
    else:
        # 如果当前为思考过程
        if reasoning_content_chunk != None and chunk.output.choices[0].message.content == []:
            print(chunk.output.choices[0].message.reasoning_content, end="")
            reasoning_content += chunk.output.choices[0].message.reasoning_content
        # 如果当前为回复
        elif chunk.output.choices[0].message.content != []:
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
            print(chunk.output.choices[0].message.content[0]["text"], end="")
            answer_content += chunk.output.choices[0].message.content[0]["text"]

# 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(f"{reasoning_content}")
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(f"{answer_content}")
```

**点击查看思考过程和完整回复**

```
====================思考过程====================
好的，我现在要解决这个关于长方体和正方体的表面积和体积的问题。首先，我需要仔细看一下题目，确保自己理解每个部分的要求。

题目是要求分别计算两个图形的表面积和体积。第一个图形是一个长方体，第二个是一个正方体。单位都是厘米，每题6分，共12分。看起来这是一个数学作业题，可能来自小学或初中阶段的几何内容。

首先，我需要回忆一下长方体和正方体的表面积和体积的计算公式。对于长方体来说，表面积的公式是：\( 面积 = 2(ab + bc + ac) \)，其中a、b、c分别是长、宽、高。而体积则是：\( 体积 = abc \)。对于正方体来说，因为所有边长相等，所以表面积是：\( 面积 = 6a^2 \)，体积是：\( 体积 = a^3 \)。

现在来看第一个图形，这是一个长方体，给出的尺寸是长4cm，宽3cm，高2cm。我需要先确认这些数值是否正确对应到公式中的各个变量。通常，长方体的三个维度可以任意命名，但为了方便计算，我们可以将最长的边作为长度，中间的作为宽度，最短的作为高度。不过在这里，题目中已经明确标注了各个边的长度，所以直接使用即可。

接下来，计算第一个长方体的表面积。根据公式，代入数值：

\( 面积 = 2(4×3 + 3×2 + 4×2) \)

先计算括号内的每一项：

\( 4×3 = 12 \)
\( 3×2 = 6 \)
\( 4×2 = 8 \)

然后将这些结果相加：

\( 12 + 6 + 8 = 26 \)

再乘以2：

\( 2 × 26 = 52 \)

所以，第一个长方体的表面积是52平方厘米。

接下来计算体积：

\( 体积 = 4 × 3 × 2 = 24 \)

所以，体积是24立方厘米。

现在看第二个图形，这是一个正方体，所有边长都是3cm。因此，表面积的计算为：

\( 面积 = 6 × 3^2 = 6 × 9 = 54 \)

体积则是：

\( 体积 = 3^3 = 27 \)

所以，正方体的表面积是54平方厘米，体积是27立方厘米。

在计算过程中，需要注意单位的一致性，题目中给出的单位是厘米，所以最终结果的单位应该是平方厘米和立方厘米。此外，要确保没有计算错误，比如乘法和加法的顺序是否正确，特别是长方体的表面积计算时，容易漏掉某一项或者计算错误。

另外，检查是否有其他可能的误解，比如是否混淆了长、宽、高的位置，但在这个问题中，由于题目已经明确标注了各个边的长度，所以应该不会有这个问题。同时，正方体的所有边长相等，所以无需担心不同的边长带来的复杂性。

总结一下，第一个长方体的表面积是52平方厘米，体积是24立方厘米；第二个正方体的表面积是54平方厘米，体积是27立方厘米。

====================完整回复====================
### 解答：

**1. 方体（长4cm，宽3cm，高2cm）**

- **表面积**：
  \[
  面积 = 2(ab + bc + ac) = 2(4×3 + 3×2 + 4×2) = 2(12 + 6 + 8) = 2×26 = 52 \, \text{cm}^2
  \]

- **体积**：
  \[
  体积 = abc = 4×3×2 = 24 \, \text{cm}^3
  \]

**2. 方体（边长3cm）**

- **表面积**：
  \[
  面积 = 6a^2 = 6×3^2 = 6×9 = 54 \, \text{cm}^2
  \]

- **体积**：
  \[
  体积 = a^3 = 3^3 = 27 \, \text{cm}^3
  \]

**答案：**
1. 方体的表面积为 \(52 \, \text{cm}^2\)，体积为 \(24 \, \text{cm}^3\)。
2. 方体的表面积为 \(54 \, \text{cm}^2\)，体积为 \(27 \, \text{cm}^3\)。
```

## Java

```
// dashscope SDK的版本 >= 2.19.0
import java.util.*;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import io.reactivex.Flowable;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.exception.InputRequiredException;
import java.lang.System;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;

    private static void handleGenerationResult(MultiModalConversationResult message) {
        String re = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        String reasoning = Objects.isNull(re)?"":re; // 默认值

        List<Map<String, Object>> content = message.getOutput().getChoices().get(0).getMessage().getContent();
        if (!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (Objects.nonNull(content) && !content.isEmpty()) {
            Object text = content.get(0).get("text");
            finalContent.append(content.get(0).get("text"));
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(text);
        }
    }
    public static MultiModalConversationParam buildMultiModalConversationParam(MultiModalMessage Msg)  {
        return MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以 qvq-max 为例，可按需更换模型名称
                .model("qvq-max")
                .messages(Arrays.asList(Msg))
                .incrementalOutput(true)
                .build();
    }

    public static void streamCallWithMessage(MultiModalConversation conv, MultiModalMessage Msg)
            throws NoApiKeyException, ApiException, InputRequiredException, UploadFileException {
        MultiModalConversationParam param = buildMultiModalConversationParam(Msg);
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(message -> {
            handleGenerationResult(message);
        });
    }
    public static void main(String[] args) {
        try {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage userMsg = MultiModalMessage.builder()
                    .role(Role.USER.getValue())
                    .content(Arrays.asList(Collections.singletonMap("image", "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"),
                            Collections.singletonMap("text", "请解答这道题")))
                    .build();
            streamCallWithMessage(conv, userMsg);
//             打印最终结果
//            if (reasoningContent.length() > 0) {
//                System.out.println("\n====================完整回复====================");
//                System.out.println(finalContent.toString());
//            }
        } catch (ApiException | NoApiKeyException | UploadFileException | InputRequiredException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

**点击查看思考过程和完整回复**

```
====================思考过程====================
嗯，我现在要解决这个题目，计算两个图形的表面积和体积。首先，我需要仔细看一下题目给出的图片。第一个图形是一个长方体，第二个是正方体。题目要求分别计算它们的表面积和体积，单位是厘米。

先看第一个图形，长方体。它的尺寸应该是长、宽、高。根据图片上的标注，长是4厘米，宽是3厘米，高是2厘米。对吧？那长方体的表面积公式我记得是2乘以（长×宽 + 长×高 + 宽×高）。然后体积就是长乘宽乘高。让我再确认一下公式是否正确。没错，表面积确实是六个面的面积之和，而每个相对的面面积相等，所以用这个公式是对的。

那代入数值的话，表面积应该是2×(4×3 + 4×2 + 3×2)。先算括号里面的：4×3=12，4×2=8，3×2=6。加起来是12+8+6=26。然后乘以2就是52平方厘米。体积的话，4×3×2=24立方厘米。这部分应该没问题。

接下来是第二个图形，正方体。所有边长都是3厘米。正方体的表面积是6乘以边长的平方，因为有六个相同的正方形面。体积则是边长的三次方。所以表面积应该是6×3²=6×9=54平方厘米。体积是3³=27立方厘米。这里要注意单位，题目里已经说明单位是厘米，所以结果直接写成平方厘米和立方厘米就行。

不过，我得再检查一遍有没有哪里出错。比如，长方体的各个边是否对应正确。图片上长方体的长度看起来确实比宽度长，所以长是4，宽是3，高是2。正方体的话，三个维度都是3，没问题。计算的时候有没有算错数字？比如，长方体的表面积计算中，各个乘积是否正确，加法有没有错误。比如4×3=12，4×2=8，3×2=6，加起来是26，乘以2是52，没错。体积4×3×2=24，正确。正方体的表面积6×9=54，体积27，也没问题。

可能需要注意的地方是单位，题目里明确说单位是cm，所以答案后面要加上正确的单位符号。另外，题目要求每题6分，共12分，但这里只有两题，所以每题各占6分。不过这不影响计算过程，只是提醒自己不要漏掉任何步骤或者单位。

总结一下，第一个图形的表面积是52平方厘米，体积24立方厘米；第二个图形的表面积54平方厘米，体积27立方厘米。应该就是这样了。

====================完整回复====================
**答案：**

1. **长方体**  
   - **表面积**：\(2 \times (4 \times 3 + 4 \times 2 + 3 \times 2) = 2 \times 26 = 52\) 平方厘米  
   - **体积**：\(4 \times 3 \times 2 = 24\) 立方厘米  

2. **正方体**  
   - **表面积**：\(6 \times 3^2 = 6 \times 9 = 54\) 平方厘米  
   - **体积**：\(3^3 = 27\) 立方厘米  

**解析：**  
- 长方体的表面积通过计算六个面的总面积得到，体积为长宽高的乘积。  
- 正方体的表面积为六个相同正方形面的面积之和，体积为边长的立方。  
- 单位均为厘米，符合题目要求。
```

## HTTP

## curl

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-H 'X-DashScope-SSE: enable' \
-d '{
    "model": "qvq-max",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"},
                    {"text": "请解答这道题"}
                ]
            }
        ]
    }
}'
```

**点击查看思考过程和完整回复**

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":[],"reasoning_content":"好的","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":547,"input_tokens_details":{"image_tokens":520,"text_tokens":24},"output_tokens":3,"input_tokens":544,"output_tokens_details":{"text_tokens":3},"image_tokens":520},"request_id":"f361ae45-fbef-9387-9f35-1269780e0864"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":[],"reasoning_content":"，","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":548,"input_tokens_details":{"image_tokens":520,"text_tokens":24},"output_tokens":4,"input_tokens":544,"output_tokens_details":{"text_tokens":4},"image_tokens":520},"request_id":"f361ae45-fbef-9387-9f35-1269780e0864"}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":[],"reasoning_content":"我现在","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":549,"input_tokens_details":{"image_tokens":520,"text_tokens":24},"output_tokens":5,"input_tokens":544,"output_tokens_details":{"text_tokens":5},"image_tokens":520},"request_id":"f361ae45-fbef-9387-9f35-1269780e0864"}
.....
id:566
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":[{"text":"方"}],"role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":1132,"input_tokens_details":{"image_tokens":520,"text_tokens":24},"output_tokens":588,"input_tokens":544,"output_tokens_details":{"text_tokens":588},"image_tokens":520},"request_id":"758b0356-653b-98ac-b4d3-f812437ba1ec"}

id:567
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":[{"text":"厘米"}],"role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":1133,"input_tokens_details":{"image_tokens":520,"text_tokens":24},"output_tokens":589,"input_tokens":544,"output_tokens_details":{"text_tokens":589},"image_tokens":520},"request_id":"758b0356-653b-98ac-b4d3-f812437ba1ec"}

id:568
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":[],"role":"assistant"},"finish_reason":"stop"}]},"usage":{"total_tokens":1134,"input_tokens_details":{"image_tokens":520,"text_tokens":24},"output_tokens":590,"input_tokens":544,"output_tokens_details":{"text_tokens":590},"image_tokens":520},"request_id":"758b0356-653b-98ac-b4d3-f812437ba1ec"}
```

## **核心能力**

### **开启/关闭思考过程**

对于需要详细推理过程的场景（如解题、分析报告），可通过 `enable_thinking`开启思考过程。以下示例展示如何开启思考过程。

**重要**

`enable_thinking`支持`qwen3.5-plus`、`qwen3-vl-plus`、`qwen3-vl-flash`、`kimi-k2.5`系列模型。其中`qwen3.5-plus`系列默认开启思考（`enable_thinking`默认为`true`）。

## OpenAI 兼容

`enable_thinking` 和 `thinking_budget` 是非 OpenAI 标准参数。在不同语言的 SDK 中传递方式存在差异：

-   **Python SDK**: 必须通过 `extra_body` 字典传递。
    
-   **Node.js SDK**: 可作为顶层参数直接传递。
    

Python

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成https://dashscope-us.aliyuncs.com/compatible-mode/v1
    # 如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

reasoning_content = ""  # 定义完整思考过程
answer_content = ""     # 定义完整回复
is_answering = False   # 判断是否结束思考过程并开始回复
enable_thinking = True
# 创建聊天完成请求
completion = client.chat.completions.create(
    model="qwen3.5-plus",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
                    },
                },
                {"type": "text", "text": "这道题怎么解答？"},
            ],
        },
    ],
    stream=True,
    # enable_thinking 参数开启思考过程，thinking_budget 参数设置最大推理过程 Token 数
    # qwen3.5-plus、qwen3-vl-plus、qwen3-vl-flash可通过enable_thinking开启或关闭思考（其中qwen3.5-plus默认开启）、对于qwen3-vl-235b-a22b-thinking等带thinking后缀的模型，enable_thinking仅支持设置为开启，对其他Qwen-VL模型均不适用
    extra_body={
        'enable_thinking': enable_thinking},

    # 解除以下注释会在最后一个chunk返回Token使用量
    # stream_options={
    #     "include_usage": True
    # }
)

if enable_thinking:
    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    # 如果chunk.choices为空，则打印usage
    if not chunk.choices:
        print("\nUsage:")
        print(chunk.usage)
    else:
        delta = chunk.choices[0].delta
        # 打印思考过程
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
            print(delta.reasoning_content, end='', flush=True)
            reasoning_content += delta.reasoning_content
        else:
            # 开始回复
            if delta.content != "" and is_answering is False:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                is_answering = True
            # 打印回复过程
            print(delta.content, end='', flush=True)
            answer_content += delta.content

# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(reasoning_content)
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(answer_content)
```

Node.js

```
import OpenAI from "openai";

// 初始化 openai 客户端
const openai = new OpenAI({
     // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY, 
    // 以下是北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成https://dashscope-us.aliyuncs.com/compatible-mode/v1
    // 如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;
let enableThinking = true;

let messages = [
    {
        role: "user",
        content: [
        { type: "image_url", image_url: { "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg" } },
        { type: "text", text: "解答这道题" },
    ]
}]

async function main() {
    try {
        const stream = await openai.chat.completions.create({
            model: 'qwen3.5-plus',
            messages: messages,
            stream: true,
          // 注意：在 Node.js SDK，enableThinking 这样的非标准参数作为顶层属性传递的，无需放在 extra_body 中
          enable_thinking: enableThinking

        });

        if (enableThinking){console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');}

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\nUsage:');
                console.log(chunk.usage);
                continue;
            }

            const delta = chunk.choices[0].delta;

            // 处理思考过程
            if (delta.reasoning_content) {
                process.stdout.write(delta.reasoning_content);
                reasoningContent += delta.reasoning_content;
            }
            // 处理正式回复
            else if (delta.content) {
                if (!isAnswering) {
                    console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
                    isAnswering = true;
                }
                process.stdout.write(delta.content);
                answerContent += delta.content;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成 https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions
# 如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===

curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen3.5-plus",
    "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
          }
        },
        {
          "type": "text",
          "text": "请解答这道题"
        }
      ]
    }
  ],
    "stream":true,
    "stream_options":{"include_usage":true},
    "enable_thinking": true
}'
```

## DashScope

Python

```
import os
import dashscope
from dashscope import MultiModalConversation

# 以下为北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成 https://dashscope-us.aliyuncs.com/api/v1
# 若使用新加坡地域的模型，需将base_url替换为：https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

enable_thinking=True

messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"},
            {"text": "解答这道题？"}
        ]
    }
]

response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen3.5-plus",
    messages=messages,
    stream=True,
    # enable_thinking 参数开启思考过程
    # qwen3.5-plus、qwen3-vl-plus、qwen3-vl-flash可通过enable_thinking开启或关闭思考（其中qwen3.5-plus默认开启）、对于qwen3-vl-235b-a22b-thinking等带thinking后缀的模型，enable_thinking仅支持设置为开启，对其他视觉推理模型均不适用
    enable_thinking=enable_thinking

)

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""
# 判断是否结束思考过程并开始回复
is_answering = False
if enable_thinking:
    print("=" * 20 + "思考过程" + "=" * 20)

for chunk in response:
    # 如果思考过程与回复皆为空，则忽略
    message = chunk.output.choices[0].message
    reasoning_content_chunk = message.get("reasoning_content", None)
    if (chunk.output.choices[0].message.content == [] and
        reasoning_content_chunk == ""):
        pass
    else:
        # 如果当前为思考过程
        if reasoning_content_chunk != None and chunk.output.choices[0].message.content == []:
            print(chunk.output.choices[0].message.reasoning_content, end="")
            reasoning_content += chunk.output.choices[0].message.reasoning_content
        # 如果当前为回复
        elif chunk.output.choices[0].message.content != []:
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
            print(chunk.output.choices[0].message.content[0]["text"], end="")
            answer_content += chunk.output.choices[0].message.content[0]["text"]

# 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(f"{reasoning_content}")
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(f"{answer_content}")
```

Java

```
// dashscope SDK的版本 >= 2.21.10
import java.util.*;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import io.reactivex.Flowable;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.exception.InputRequiredException;
import java.lang.System;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为北京地域 base_url，若使用弗吉尼亚地域模型，需要将base_url换成 https://dashscope-us.aliyuncs.com/api/v1
    // 若使用新加坡地域的模型，需将base_url替换为：https://dashscope-intl.aliyuncs.com/api/v1
    static {Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";}

    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;

    private static void handleGenerationResult(MultiModalConversationResult message) {
        String re = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        String reasoning = Objects.isNull(re)?"":re; // 默认值

        List<Map<String, Object>> content = message.getOutput().getChoices().get(0).getMessage().getContent();
        if (!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (Objects.nonNull(content) && !content.isEmpty()) {
            Object text = content.get(0).get("text");
            finalContent.append(content.get(0).get("text"));
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(text);
        }
    }
    public static MultiModalConversationParam buildMultiModalConversationParam(MultiModalMessage Msg)  {
        return MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.5-plus")
                .messages(Arrays.asList(Msg))
                .enableThinking(true)
                .incrementalOutput(true)
                .build();
    }

    public static void streamCallWithMessage(MultiModalConversation conv, MultiModalMessage Msg)
            throws NoApiKeyException, ApiException, InputRequiredException, UploadFileException {
        MultiModalConversationParam param = buildMultiModalConversationParam(Msg);
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(message -> {
            handleGenerationResult(message);
        });
    }
    public static void main(String[] args) {
        try {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage userMsg = MultiModalMessage.builder()
                    .role(Role.USER.getValue())
                    .content(Arrays.asList(Collections.singletonMap("image", "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"),
                            Collections.singletonMap("text", "请解答这道题")))
                    .build();
            streamCallWithMessage(conv, userMsg);
//             打印最终结果
//            if (reasoningContent.length() > 0) {
//                System.out.println("\n====================完整回复====================");
//                System.out.println(finalContent.toString());
//            }
        } catch (ApiException | NoApiKeyException | UploadFileException | InputRequiredException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成：https://dashscope-us.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# 若使用新加坡地域的模型，需要将base_url换成：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-H 'X-DashScope-SSE: enable' \
-d '{
    "model": "qwen3.5-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"},
                    {"text": "请解答这道题"}
                ]
            }
        ]
    },
    "parameters":{
        "enable_thinking": true,
        "incremental_output": true
    }
}'
```

### **限制思考长度**

为避免视觉推理模型输出过于冗长的思考过程，可使用 `thinking_budget` 参数限制思考过程生成的最大 Token 数。当思考过程超过该限制时，内容将被截断，模型会立即开始生成最终答案。`thinking_budget` 默认值为模型的最大思维链长度，请参见[模型列表](https://help.aliyun.com/zh/model-studio/models)。

**重要**

`thinking_budget` 参数支持Qwen3-VL（思考模式）、kimi-k2.5（思考模式）。

## OpenAI 兼容

`thinking_budget`非 OpenAI 标准参数，若使用 OpenAI Python SDK 请通过 `extra_body`传入。

Python

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成https://dashscope-us.aliyuncs.com/compatible-mode/v1
    # 如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

reasoning_content = ""  # 定义完整思考过程
answer_content = ""     # 定义完整回复
is_answering = False   # 判断是否结束思考过程并开始回复
enable_thinking = True
# 创建聊天完成请求
completion = client.chat.completions.create(
    model="qwen3.5-plus",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
                    },
                },
                {"type": "text", "text": "这道题怎么解答？"},
            ],
        },
    ],
    stream=True,
    # enable_thinking 参数开启思考过程，thinking_budget 参数设置最大推理过程 Token 数
    # qwen3.5-plus、qwen3-vl-plus、qwen3-vl-flash可通过enable_thinking开启或关闭思考（其中qwen3.5-plus默认开启）、对于qwen3-vl-235b-a22b-thinking等带thinking后缀的模型，enable_thinking仅支持设置为开启，对其他Qwen-VL模型均不适用
    extra_body={
        'enable_thinking': enable_thinking,
        "thinking_budget": 81920},

    # 解除以下注释会在最后一个chunk返回Token使用量
    # stream_options={
    #     "include_usage": True
    # }
)

if enable_thinking:
    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    # 如果chunk.choices为空，则打印usage
    if not chunk.choices:
        print("\nUsage:")
        print(chunk.usage)
    else:
        delta = chunk.choices[0].delta
        # 打印思考过程
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
            print(delta.reasoning_content, end='', flush=True)
            reasoning_content += delta.reasoning_content
        else:
            # 开始回复
            if delta.content != "" and is_answering is False:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                is_answering = True
            # 打印回复过程
            print(delta.content, end='', flush=True)
            answer_content += delta.content

# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(reasoning_content)
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(answer_content)
```

Node.js

```
import OpenAI from "openai";

// 初始化 openai 客户端
const openai = new OpenAI({
     // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY, 
    // 以下是北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成https://dashscope-us.aliyuncs.com/compatible-mode/v1
    // 如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;
let enableThinking = true;

let messages = [
    {
        role: "user",
        content: [
        { type: "image_url", image_url: { "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg" } },
        { type: "text", text: "解答这道题" },
    ]
}]

async function main() {
    try {
        const stream = await openai.chat.completions.create({
            model: 'qwen3.5-plus',
            messages: messages,
            stream: true,
          // 注意：在 Node.js SDK，enableThinking 这样的非标准参数作为顶层属性传递的，无需放在 extra_body 中
          enable_thinking: enableThinking,
          thinking_budget: 81920

        });

        if (enableThinking){console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');}

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\nUsage:');
                console.log(chunk.usage);
                continue;
            }

            const delta = chunk.choices[0].delta;

            // 处理思考过程
            if (delta.reasoning_content) {
                process.stdout.write(delta.reasoning_content);
                reasoningContent += delta.reasoning_content;
            }
            // 处理正式回复
            else if (delta.content) {
                if (!isAnswering) {
                    console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
                    isAnswering = true;
                }
                process.stdout.write(delta.content);
                answerContent += delta.content;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成 https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions
# 如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===

curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen3.5-plus",
    "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
          }
        },
        {
          "type": "text",
          "text": "请解答这道题"
        }
      ]
    }
  ],
    "stream":true,
    "stream_options":{"include_usage":true},
    "enable_thinking": true,
    "thinking_budget": 81920
}'
```

## DashScope

Python

```
import os
import dashscope
from dashscope import MultiModalConversation

# 以下为北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成 https://dashscope-us.aliyuncs.com/api/v1
# 若使用新加坡地域的模型，需将base_url替换为：https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

enable_thinking=True
messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"},
            {"text": "解答这道题？"}
        ]
    }
]

response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen3.5-plus",
    messages=messages,
    stream=True,
    # enable_thinking 参数开启思考过程
    # qwen3.5-plus、qwen3-vl-plus、qwen3-vl-flash可通过enable_thinking开启或关闭思考（其中qwen3.5-plus默认开启）、对于qwen3-vl-235b-a22b-thinking等带thinking后缀的模型，enable_thinking仅支持设置为开启，对其他Qwen-VL模型均不适用
    enable_thinking=enable_thinking,
    # thinking_budget 参数设置最大推理过程 Token 数
    thinking_budget=81920,

)

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""
# 判断是否结束思考过程并开始回复
is_answering = False
if enable_thinking:
    print("=" * 20 + "思考过程" + "=" * 20)

for chunk in response:
    # 如果思考过程与回复皆为空，则忽略
    message = chunk.output.choices[0].message
    reasoning_content_chunk = message.get("reasoning_content", None)
    if (chunk.output.choices[0].message.content == [] and
        reasoning_content_chunk == ""):
        pass
    else:
        # 如果当前为思考过程
        if reasoning_content_chunk != None and chunk.output.choices[0].message.content == []:
            print(chunk.output.choices[0].message.reasoning_content, end="")
            reasoning_content += chunk.output.choices[0].message.reasoning_content
        # 如果当前为回复
        elif chunk.output.choices[0].message.content != []:
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
            print(chunk.output.choices[0].message.content[0]["text"], end="")
            answer_content += chunk.output.choices[0].message.content[0]["text"]

# 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(f"{reasoning_content}")
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(f"{answer_content}")
```

Java

```
// dashscope SDK的版本 >= 2.21.10
import java.util.*;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import io.reactivex.Flowable;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.exception.InputRequiredException;
import java.lang.System;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为北京地域 base_url，若使用弗吉尼亚地域模型，需要将base_url换成 https://dashscope-us.aliyuncs.com/api/v1
    // 若使用新加坡地域的模型，需将base_url替换为：https://dashscope-intl.aliyuncs.com/api/v1
    static {Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";}

    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;

    private static void handleGenerationResult(MultiModalConversationResult message) {
        String re = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        String reasoning = Objects.isNull(re)?"":re; // 默认值

        List<Map<String, Object>> content = message.getOutput().getChoices().get(0).getMessage().getContent();
        if (!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (Objects.nonNull(content) && !content.isEmpty()) {
            Object text = content.get(0).get("text");
            finalContent.append(content.get(0).get("text"));
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(text);
        }
    }
    public static MultiModalConversationParam buildMultiModalConversationParam(MultiModalMessage Msg)  {
        return MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.5-plus")
                .messages(Arrays.asList(Msg))
                .enableThinking(true)
                .thinkingBudget(81920)
                .incrementalOutput(true)
                .build();
    }

    public static void streamCallWithMessage(MultiModalConversation conv, MultiModalMessage Msg)
            throws NoApiKeyException, ApiException, InputRequiredException, UploadFileException {
        MultiModalConversationParam param = buildMultiModalConversationParam(Msg);
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(message -> {
            handleGenerationResult(message);
        });
    }
    public static void main(String[] args) {
        try {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage userMsg = MultiModalMessage.builder()
                    .role(Role.USER.getValue())
                    .content(Arrays.asList(Collections.singletonMap("image", "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"),
                            Collections.singletonMap("text", "请解答这道题")))
                    .build();
            streamCallWithMessage(conv, userMsg);
//             打印最终结果
//            if (reasoningContent.length() > 0) {
//                System.out.println("\n====================完整回复====================");
//                System.out.println(finalContent.toString());
//            }
        } catch (ApiException | NoApiKeyException | UploadFileException | InputRequiredException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成：https://dashscope-us.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# 若使用新加坡地域的模型，需要将base_url换成：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# === 执行时请删除该注释 ===

curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-H 'X-DashScope-SSE: enable' \
-d '{
    "model": "qwen3.5-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"},
                    {"text": "请解答这道题"}
                ]
            }
        ]
    },
    "parameters":{
        "enable_thinking": true,
        "incremental_output": true,
        "thinking_budget": 81920
    }
}'
```

### **更多用法**

除了思考能力，视觉推理模型同样具备视觉理解模型的全部功能，可组合使用以应对更复杂的场景：

-   [多图理解](https://help.aliyun.com/zh/model-studio/vision#32a707ea691qg)
    
-   [视频理解](https://help.aliyun.com/zh/model-studio/vision#e888120b96oaj)
    
-   [处理高分辨率图像](https://help.aliyun.com/zh/model-studio/vision#e7e2db755f9h7)
    
-   [传入本地文件（Base64 编码或文件路径）](https://help.aliyun.com/zh/model-studio/vision#a63fbac15a8s8)
    

## 计费说明

总费用 = 输入 Token 数 x 模型输入单价 + 模型输出 Token 数 x 模型输出单价。

-   思考过程（`reasoning_content`）会作为输出内容的一部分，计入**输出 Token** 并产生相应费用。若模型在思考模式下未输出思考过程，按照非思考模式价格计费。
    
-   图像或视频计算token的方法请参见[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision#c88f7244e4t6v)。
    

## API参考

关于视觉推理模型的输入输出参数，请参见[千问](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

在代码补全、文本续写等场景中，需要模型从已有的文本片段（前缀）开始继续生成。Partial Mode 可提供精确控制能力，确保模型输出的内容紧密衔接提供的前缀，提升生成结果的准确性与可控性。

## **使用方式**

需在`messages` 数组中将最后一条消息的 `role` 设置为 `assistant`，并在其 `content` 中提供前缀，在此消息中设置参数 `"partial": true`。`messages`格式如下：

```
[
    {
        "role": "user",
        "content": "请补全这个斐波那契函数，勿添加其它内容"
    },
    {
        "role": "assistant",
        "content": "def calculate_fibonacci(n):\n    if n <= 1:\n        return n\n    else:\n",
        "partial": true
    }
]
```

模型会以前缀内容为起点开始生成。

## **支持的模型**

-   **千问Max 系列（非思考模式）**
    
    qwen3-max、qwen3-max-2025-09-23、qwen3-max-preview（非思考模式）、qwen-max、qwen-max-latest、qwen-max-2024-09-19及之后的快照模型
    
-   **千问Plus 系列（非思考模式）**
    
    qwen3.5-plus、qwen3.5-plus-2026-02-15及之后的快照模型、qwen-plus、qwen-plus-latest、qwen-plus-2024-12-20及之后的快照模型
    
-   **千问Flash 系列（非思考模式）**
    
    qwen3.5-flash、qwen3.5-flash-2026-02-23及之后的快照模型、qwen-flash、qwen-flash-2025-07-28
    
-   **千问Coder 系列**
    
    qwen3-coder-plus、qwen3-coder-flash、qwen3-coder-480b-a35b-instruct、qwen3-coder-30b-a3b-instruct、qwen-coder-plus、qwen-coder-plus-latest、qwen-coder-plus-2024-11-06、qwen-coder-turbo、qwen-coder-turbo-latest、qwen-coder-turbo-2024-09-19、qwen2.5-coder-32b-instruct、qwen2.5-coder-14b-instruct、qwen2.5-coder-7b-instruct、qwen2.5-coder-3b-instruct、qwen2.5-coder-1.5b-instruct、qwen2.5-coder-0.5b-instruct
    
-   **千问VL 系列**
    
    -   **qwen3-vl-plus 系列（非思考模式）**
        
        qwen3-vl-plus、qwen3-vl-plus-2025-09-23及之后的快照模型
        
    -   **qwen3-vl-flash 系列（非思考模式）**
        
        qwen3-vl-flash、qwen3-vl-flash-2025-10-15及之后的快照模型
        
    -   **qwen-vl-max 系列**
        
        qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-2024-11-19及之后的快照模型
        
    -   **qwen-vl-plus 系列**
        
        qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-2025-01-02及之后的快照模型
        
-   **千问Turbo 系列（非思考模式）**
    
    qwen-turbo、qwen-turbo-latest、qwen-turbo-2024-11-01及之后的快照模型
    
-   **千问开源系列**
    
    qwen3.5-397b-a17b、qwen3.5-122b-a10b、qwen3.5-27b、qwen3.5-35b-a3b（非思考模式）、Qwen3 开源模型（非思考模式）、qwen2.5-72b-instruct、qwen2.5-32b-instruct、qwen2.5-14b-instruct、qwen2.5-7b-instruct、qwen2.5-3b-instruct、qwen2.5-1.5b-instruct、qwen2.5-0.5b-instruct、Qwen3-VL开源模型（非思考模式）
    
-   **千问Math 系列**
    
    qwen-math-plus、qwen-math-plus-latest、qwen-math-plus-0919、qwen-math-turbo、qwen-math-turbo-latest、qwen-math-turbo-0919、qwen2.5-math-72b-instruct、qwen2.5-math-7b-instruct、qwen2.5-math-1.5b-instruct
    

**重要**

思考模式模型暂不支持前缀续写功能。

## **快速开始**

### **前提条件**

已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并 [配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过 OpenAI SDK 或 DashScope SDK 进行调用，需要[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk#210ee28162bs7)。如果您是子业务空间的成员，请确保超级管理员已为该业务空间进行 [模型授权操作](https://help.aliyun.com/zh/model-studio/model-authentication-instructions)。

**说明**

暂不支持 DashScope Java SDK。

### **示例代码**

代码补全是 Partial Mode 的核心应用场景。以下示例演示如何使用 `qwen3-coder-plus` 模型补全一个 Python 函数。

## OpenAI兼容

## Python

```
import os
from openai import OpenAI

# 1. 初始化客户端
client = OpenAI(
    # 若没有配置环境变量，请将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 2. 定义需要补全的代码前缀
prefix = """def calculate_fibonacci(n):
    if n <= 1:
        return n
    else:
"""

# 3. 发起 Partial Mode 请求
# 注意：messages 数组的最后一条消息 role 为 "assistant"，并包含 "partial": True
completion = client.chat.completions.create(
    model="qwen3-coder-plus",
    messages=[
        {"role": "user", "content": "请补全这个斐波那契函数，勿添加其它内容"},
        {"role": "assistant", "content": prefix, "partial": True},
    ],
)

# 4. 手动拼接前缀和模型生成的内容
generated_code = completion.choices[0].message.content
complete_code = prefix + generated_code

print(complete_code)
```

### **返回结果**

```
def calculate_fibonacci(n):
    if n <= 1:
        return n
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
```

## Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

// 定义需要补全的代码前缀
const prefix = `def calculate_fibonacci(n):
    if n <= 1:
        return n
    else:
`;

const completion = await openai.chat.completions.create({
    model: "qwen3-coder-plus",  // 使用代码模型
    messages: [
        { role: "user", content: "请补全这个斐波那契函数，勿添加其它内容" },
        { role: "assistant", content: prefix, partial: true }
    ],
});

// 手动拼接前缀和模型生成的内容
const generatedCode = completion.choices[0].message.content;
const completeCode = prefix + generatedCode;

console.log(completeCode);
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3-coder-plus",
    "messages": [
        {
            "role": "user", 
            "content": "请补全这个斐波那契函数，勿添加其它内容"
        },
        {
            "role": "assistant",
            "content": "def calculate_fibonacci(n):\n    if n <= 1:\n        return n\n    else:\n",
            "partial": true
        }
    ]
}'
```

### **返回结果**

```
{
    "choices": [
        {
            "message": {
                "content": "        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)",
                "role": "assistant"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
        }
    ],
    "object": "chat.completion",
    "usage": {
        "prompt_tokens": 48,
        "completion_tokens": 19,
        "total_tokens": 67,
        "prompt_tokens_details": {
            "cache_type": "implicit",
            "cached_tokens": 0
        }
    },
    "created": 1756800231,
    "system_fingerprint": null,
    "model": "qwen3-coder-plus",
    "id": "chatcmpl-d103b1cf-4bda-942f-92d6-d7ecabfeeccb"
}
```

## DashScope

## Python

```
import os
import dashscope

# 若使用新加坡地域的模型，请释放下列注释
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"
messages = [
    {
        "role": "user", 
        "content": "请补全这个斐波那契函数，勿添加其它内容"
    },
    {
        "role": "assistant",
        "content": "def calculate_fibonacci(n):\n    if n <= 1:\n        return n\n    else:\n",
        "partial": True
    }
]
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model='qwen3-coder-plus',
    messages=messages,
    result_format='message',  
)

# 手动拼接前缀和模型生成的内容
prefix = "def calculate_fibonacci(n):\n    if n <= 1:\n        return n\n    else:\n"
generated_code = response.output.choices[0].message.content
complete_code = prefix + generated_code

print(complete_code)
```

### **返回结果**

```
def calculate_fibonacci(n):
    if n <= 1:
        return n
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
# === 执行时请删除该注释 ===
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3-coder-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": "请补全这个斐波那契函数，勿添加其它内容"
            },
            {
                "role": "assistant",
                "content": "def calculate_fibonacci(n):\n    if n <= 1:\n        return n\n    else:\n",
                "partial": true
            }
        ]
    },
    "parameters": {
        "result_format": "message"
    }
}'
```

### **返回结果**

```
{
    "output": {
        "choices": [
            {
                "message": {
                    "content": "        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)",
                    "role": "assistant"
                },
                "finish_reason": "stop"
            }
        ]
    },
    "usage": {
        "total_tokens": 67,
        "output_tokens": 19,
        "input_tokens": 48,
        "prompt_tokens_details": {
            "cached_tokens": 0
        }
    },
    "request_id": "c61c62e5-cf97-90bc-a4ee-50e5e117b93f"
}
```

## **使用示例**

### **传入图片或视频**

千问VL模型支持在输入图像、视频数据时进行前缀续写，可应用于产品介绍、社交媒体内容创作、新闻稿生成、创意文案等场景。

## OpenAI兼容

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3-vl-plus",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://img.alicdn.com/imgextra/i3/O1CN01zFX2Bs1Q0f9pESgPC_!!6000000001914-2-tps-450-450.png"
                    },
                },
                {"type": "text", "text": "我要发社交媒体，请帮我想一下文案。"},
            ],
        },
        {
            "role": "assistant",
            "content": "今天发现了一家宝藏咖啡馆",
            "partial": True,
        },
    ],
)
print(completion.choices[0].message.content)
```

### **返回结果**

```
，这款提拉米苏简直是味蕾的享受！每一口都能感受到咖啡与奶油的完美融合，幸福感爆棚～ #美食分享 #提拉米苏 #咖啡时光

希望你喜欢这个文案！如果有任何修改需求，请随时告诉我。
```

## Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.chat.completions.create({
        model: "qwen3-vl-plus", 
        messages: [
            {
                role: "user",
                content: [
                    {
                        type: "image_url",
                        image_url: {
                            "url": "https://img.alicdn.com/imgextra/i3/O1CN01zFX2Bs1Q0f9pESgPC_!!6000000001914-2-tps-450-450.png"
                        }
                    },
                    {
                        type: "text",
                        text: "我要发社交媒体，请帮我想一下文案。"
                    }
                ]
            },
            {
                role: "assistant",
                content: "今天发现了一家宝藏咖啡馆",
                "partial": true
            }
        ]
    });
    console.log(response.choices[0].message.content);
}

main();
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===
curl -X POST 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen3-vl-plus",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://img.alicdn.com/imgextra/i3/O1CN01zFX2Bs1Q0f9pESgPC_!!6000000001914-2-tps-450-450.png"
          }
        },
        {
          "type": "text",
          "text": "我要发社交媒体，请帮我想一下文案。"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "今天发现了一家宝藏咖啡馆",
      "partial": true
    }
  ]
}'
```

### **返回结果**

```
{
    "choices": [
        {
            "message": {
                "content": "，这款提拉米苏简直是味蕾的享受！每一口都是咖啡与奶油的完美融合，幸福感爆棚～ #美食分享 #提拉米苏 #咖啡时光\n\n希望你喜欢这个文案！如果有任何修改需求，请随时告诉我。",
                "role": "assistant"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
        }
    ],
    "object": "chat.completion",
    "usage": {
        "prompt_tokens": 282,
        "completion_tokens": 56,
        "total_tokens": 338,
        "prompt_tokens_details": {
            "cached_tokens": 0
        }
    },
    "created": 1756802933,
    "system_fingerprint": null,
    "model": "qwen3-vl-plus",
    "id": "chatcmpl-5780cbb7-ebae-9c63-b098-f8cc49e321f0"
}
```

## DashScope

## Python

```
import os
import dashscope

# 使用新加坡地域服务，请启用下一行；如使用北京地域，则注释掉此行
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {
                "image": "https://img.alicdn.com/imgextra/i3/O1CN01zFX2Bs1Q0f9pESgPC_!!6000000001914-2-tps-450-450.png"
            },
            {"text": "我要发社交媒体，请帮我想一下文案。"},
        ],
    },
    {"role": "assistant", "content": "今天发现了一家宝藏咖啡馆", "partial": True},
]

response = dashscope.MultiModalConversation.call(
    #若没有配置环境变量， 请用百炼API Key将下行替换为： api_key ="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"), 
    model="qwen3-vl-plus", 
    messages=messages
)

print(response.output.choices[0].message.content[0]["text"])
```

### **返回结果**

```
，这款提拉米苏简直是味蕾的享受！每一口都能感受到咖啡与奶油的完美融合，幸福感爆棚～ #美食分享 #提拉米苏 #咖啡时光

希望你喜欢这个文案！如果有任何修改需求，请随时告诉我。
```

## curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
# === 执行时请删除该注释 ===
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3-vl-plus",
    "input":{
        "messages":[
            {"role": "user",
             "content": [
               {"image": "https://img.alicdn.com/imgextra/i3/O1CN01zFX2Bs1Q0f9pESgPC_!!6000000001914-2-tps-450-450.png"},
               {"text": "我要发社交媒体，请帮我想一下文案。"}]
            },
            {"role": "assistant",
             "content": "今天发现了一家宝藏咖啡馆",
             "partial": true
            }
        ]
    }
}'
```

### **返回结果**

```
{
    "output": {
        "choices": [
            {
                "message": {
                    "content": [
                        {
                            "text": "，这款提拉米苏简直是味蕾的享受！每一口都能感受到咖啡与奶油的完美融合，幸福感爆棚～ #美食分享 #提拉米苏 #咖啡时光\n\n希望你喜欢这个文案！如果有任何修改需求，请随时告诉我。"
                        }
                    ],
                    "role": "assistant"
                },
                "finish_reason": "stop"
            }
        ]
    },
    "usage": {
        "total_tokens": 339,
        "input_tokens_details": {
            "image_tokens": 258,
            "text_tokens": 24
        },
        "output_tokens": 57,
        "input_tokens": 282,
        "output_tokens_details": {
            "text_tokens": 57
        },
        "image_tokens": 258
    },
    "request_id": "c741328c-23dc-9286-bfa7-626a4092ca09"
}
```

### **基于不完整输出进行续写**

如果大模型返回不完整的内容，可使用 Partial Mode 对不完整的内容续写，使其语义完整。大模型可能返回不完整内容的情况：

-   `max_tokens`参数设置过小，使模型返回被截断的内容。
    
-   非流式输出触发超时，已生成的内容不完整。
    
    > 超时不再报错，而是将已生成内容返回，详情参见[如何处理模型超时的情况](https://help.aliyun.com/zh/model-studio/text-generation#11241147efwpm)。
    

## OpenAI兼容

## Python

```
import os
from openai import OpenAI

# 初始化客户端
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def chat_completion(messages,max_tokens=None):
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
        max_tokens=max_tokens
    )
    print(f"###停止生成原因：{response.choices[0].finish_reason}")
    
    return response.choices[0].message.content

# 使用示例
messages = [{"role": "user", "content": "请写一个短篇科幻故事"}]

# 第一轮调用，设置max_tokens为40
first_content = chat_completion(messages, max_tokens=40)
print(first_content)
# 将第一轮的响应加入到assistant message，并设置partial=True
messages.append({"role": "assistant", "content": first_content, "partial": True})

# 第二轮调用
second_content = chat_completion(messages)
print("###完整内容：")
print(first_content+second_content)
```

### **返回结果**

停止生成原因为`length`表示触发了`max_tokens`的限制；停止生成原因为`stop`表示大模型生成自然结束，或触发了`stop`参数。

```
###停止生成原因：length
**《记忆的尽头》**

在遥远的未来，地球早已不再适合人类居住。大气层被污染，海洋干涸，城市变成了废墟。人类被迫迁移到一颗名为“
###停止生成原因：stop
###完整内容：
**《记忆的尽头》**

在遥远的未来，地球早已不再适合人类居住。大气层被污染，海洋干涸，城市变成了废墟。人类被迫迁移到一颗名为“伊甸星”的宜居星球，那里有蔚蓝的天空、清新的空气和无尽的资源。

然而，伊甸星并非真正的天堂。它没有人类的历史，没有过去，也没有记忆。

......

**“如果我们忘记了自己是谁，我们还算是人类吗？”**

——完——
```

## Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

async function chatCompletion(messages, maxTokens = null) {
    const completion = await openai.chat.completions.create({
        model: "qwen-plus",
        messages: messages,
        max_tokens: maxTokens
    });
    
    console.log(`###停止生成原因：${completion.choices[0].finish_reason}`);
    return completion.choices[0].message.content;
}

// 使用示例
async function main() {
    let messages = [{"role": "user", "content": "请写一个短篇科幻故事"}];

    try {
        // 第一轮调用，设置max_tokens为40
        const firstContent = await chatCompletion(messages, 40);
        console.log(firstContent);
        
        // 将第一轮的响应加入到assistant message，并设置partial=true
        messages.push({"role": "assistant", "content": firstContent, "partial": true});

        // 第二轮调用
        const secondContent = await chatCompletion(messages);
        console.log("###完整内容：");
        console.log(firstContent + secondContent);
        
    } catch (error) {
        console.error('执行出错:', error);
    }
}

// 运行示例
main();
```

## DashScope

## Python

### **示例代码**

```
import os
import dashscope

# 若使用新加坡地域的模型，请释放下列注释
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

def chat_completion(messages, max_tokens=None):
    response = dashscope.Generation.call(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model='qwen-plus',
        messages=messages,
        max_tokens=max_tokens,
        result_format='message',  
    )
    
    print(f"###停止生成原因：{response.output.choices[0].finish_reason}")
    return response.output.choices[0].message.content

# 使用示例
messages = [{"role": "user", "content": "请写一个短篇科幻故事"}]

# 第一轮调用，设置max_tokens为40
first_content = chat_completion(messages, max_tokens=40)
print(first_content)

# 将第一轮的响应加入到assistant message，并设置partial=True
messages.append({"role": "assistant", "content": first_content, "partial": True})

# 第二轮调用
second_content = chat_completion(messages)
print("###完整内容：")
print(first_content + second_content)
```

### **返回结果**

```
###停止生成原因：length
标题：**《时间折纸》**

---

公元2179年，人类终于掌握了时间旅行的技术。但这项技术并不是通过庞大的机器或复杂的能量场实现的，而是一
###停止生成原因：stop
###完整内容：
标题：**《时间折纸》**

---

公元2179年，人类终于掌握了时间旅行的技术。但这项技术并不是通过庞大的机器或复杂的能量场实现的，而是一张纸。

一张能折叠时间的纸。

它被称为“时间折纸”，由一种来自外星文明的未知物质制成。科学家们无法解释它的原理，只知道，只要在纸上画出某个场景，再进行特定的折叠方式，就能打开一扇通往过去或未来的门。

......

“你不是时间的钥匙，只是提醒我们，未来，始终掌握在我们手中。”

然后，我把它撕成了碎片。

---

**（完）**
```

## **计费说明**

根据请求的输入 Token 和输出 Token 计费。前缀部分作为输入 Token。

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

调用大模型时，不同推理请求可能出现输入内容的重叠（例如多轮对话或对同一本书的多次提问）。上下文缓存（Context Cache）技术可以缓存这些请求的公共前缀，减少推理时的重复计算。这能提升响应速度，并在不影响回复效果的前提下降低您的使用成本。

为满足不同场景的需求，上下文缓存提供两种工作模式，可以根据对便捷性、确定性及成本的需求进行选择：

-   [显式缓存](#825f201c5fy6o)：需要**主动开启**的缓存模式。需要主动为指定内容创建缓存，以在有效期（5分钟）内实现确定性命中。除了输入 Token 计费，用于创建缓存的 Token 按输入 Token 标准单价的 125% 计费，后续命中仅需支付 10%的费用。
    
-   [隐式缓存](#2317ea09cfxok)：此为自动模式，无需额外配置，且无法关闭，适合追求便捷的通用场景。系统会**自动识别**请求内容的**公共前缀**并进行缓存，但缓存**命中率不确定**。对命中缓存的部分，按输入 Token 标准单价的 20% 计费。
    

| **项目** | **显式缓存** | **隐式缓存** |
| --- | --- | --- |
| 是否影响回复效果 | 不影响 | 不影响 |
| 用于创建缓存Token计费 | 输入 Token 单价的125% | 输入 Token 单价的100% |
| 命中缓存的输入 Token 计费 | 输入 Token 单价的10% | 输入 Token 单价的20% |
| 缓存最少 Token 数 | 1024 | 256 |
| 缓存有效期 | 5分钟（命中后重置） | 不确定，系统会定期清理长期未使用的缓存数据 |

**说明**

显式缓存、隐式缓存两者互斥，单个请求只能应用其中一种模式。

**说明**

本文内容适用 OpenAI Chat Completions 与 DashScope 接口。使用 Responses API 可通过 Session 缓存降低推理延迟与成本，详情参考[OpenAI兼容-Responses](https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api#example-session-cache)。

## **显式缓存**

与隐式缓存相比，显式缓存需要显式创建并承担相应开销，但能实现更高的缓存命中率和更低的访问延迟。

### **使用方式**

在 messages 中加入`"cache_control": {"type": "ephemeral"}`标记，系统将以每个`cache_control`标记位置为终点，向前回溯最多 20 个 `content` 块，尝试命中缓存。

> 单次请求最多支持加入4 个缓存标记。

-   **未命中缓存**
    
    系统将从messages数组开头到 `cache_control`标记之间的内容创建为新的缓存块，有效期为 5 分钟。
    
    > 缓存创建发生在模型响应之后，建议在创建请求完成后再尝试命中该缓存。
    
    > 缓存块的内容最少为 1024 Token。
    
-   **命中缓存**
    
    选取最长的匹配前缀作为命中的缓存块，并将该缓存块的有效期重置为5分钟。
    

以下示例说明其使用方式：

1.  **发起第一个请求**：发送包含超 1024 Token 文本 A 的系统消息，并加入缓存标记：
    
    ```
    [{"role": "system", "content": [{"type": "text", "text": A, "cache_control": {"type": "ephemeral"}}]}] 
    ```
    
    系统将创建首个缓存块，记为 A 缓存块。
    
2.  **发起第二个请求：**发送以下结构的请求：
    
    ```
    [
        {"role": "system", "content": A},
        <其他 message>
        {"role": "user","content": [{"type": "text", "text": B, "cache_control": {"type": "ephemeral"}}]}
    ]
    ```
    
    -   若“其他message”不超过 20 条，则命中 A 缓存块，并将其有效期重置为 5 分钟；同时，系统会基于 A、其他message和 B 创建一个新的缓存块。
        
    -   若“其他message”超过 20 条，则无法命中 A 缓存块，系统仍会基于完整上下文（A + 其他message + B）创建新缓存块。
        

### **支持的模型**

## 中国内地

[千问Max](https://help.aliyun.com/zh/model-studio/models#d4ccf72f23jh9)：qwen3-max

[千问Plus](https://help.aliyun.com/zh/model-studio/models#5ef284d4ed42p)：qwen3.5-plus、qwen-plus

[千问Flash](https://help.aliyun.com/zh/model-studio/models#13ff05e329blt)：qwen3.5-flash、qwen-flash

[千问Coder](https://help.aliyun.com/zh/model-studio/models#d698550551bob)：qwen3-coder-plus、qwen3-coder-flash

[千问VL](https://help.aliyun.com/zh/model-studio/models#3f1f1c8913fvo)：qwen3-vl-plus

[DeepSeek-阿里云](https://help.aliyun.com/zh/model-studio/deepseek-api)：deepseek-v3.2

[Kimi-阿里云](https://help.aliyun.com/zh/model-studio/kimi-api)：kimi-k2.5

## 全球

[千问Plus](https://help.aliyun.com/zh/model-studio/models#5ef284d4ed42p)：qwen3.5-plus

[千问Flash](https://help.aliyun.com/zh/model-studio/models#13ff05e329blt)：qwen3.5-flash

## 国际

[千问Max](https://help.aliyun.com/zh/model-studio/models#d4ccf72f23jh9)：qwen3-max

[千问Plus](https://help.aliyun.com/zh/model-studio/models#5ef284d4ed42p)：qwen3.5-plus、qwen-plus

[千问Flash](https://help.aliyun.com/zh/model-studio/models#13ff05e329blt)：qwen3.5-flash、qwen-flash

[千问Coder](https://help.aliyun.com/zh/model-studio/models#d698550551bob)：qwen3-coder-plus、qwen3-coder-flash

[千问VL](https://help.aliyun.com/zh/model-studio/models#3f1f1c8913fvo)：qwen3-vl-plus

[DeepSeek-阿里云](https://help.aliyun.com/zh/model-studio/deepseek-api)：deepseek-v3.2

### **快速开始**

以下示例展示了在 OpenAI 兼容接口和 DashScope 协议中，缓存块的创建与命中机制。

## OpenAI 兼容

```
from openai import OpenAI
import os

client = OpenAI(
    # 若没有配置环境变量，请将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 模拟的代码仓库内容，最小可缓存提示词长度为 1024 Token
long_text_content = "<Your Code Here>" * 400

# 发起请求的函数
def get_completion(user_input):
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": long_text_content,
                    # 在此处放置 cache_control 标记，将创建从 messages 数组的开头到当前 content 所在位置的所有内容作为缓存块。
                    "cache_control": {"type": "ephemeral"},
                }
            ],
        },
        # 每次的提问内容不同
        {
            "role": "user",
            "content": user_input,
        },
    ]
    completion = client.chat.completions.create(
        # 选择支持显式缓存的模型
        model="qwen3-coder-plus",
        messages=messages,
    )
    return completion

# 第一次请求
first_completion = get_completion("这段代码的内容是什么")
print(f"第一次请求创建缓存 Token：{first_completion.usage.prompt_tokens_details.cache_creation_input_tokens}")
print(f"第一次请求命中缓存 Token：{first_completion.usage.prompt_tokens_details.cached_tokens}")
print("=" * 20)
# 第二次请求，代码内容一致，只修改了提问问题
second_completion = get_completion("这段代码可以怎么优化")
print(f"第二次请求创建缓存 Token：{second_completion.usage.prompt_tokens_details.cache_creation_input_tokens}")
print(f"第二次请求命中缓存 Token：{second_completion.usage.prompt_tokens_details.cached_tokens}")
```

## DashScope

Python

```
import os
from dashscope import Generation
# 若使用新加坡地域的模型，请释放下列注释
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

# 模拟的代码仓库内容，最小可缓存提示词长度为 1024 Token
long_text_content = "<Your Code Here>" * 400

# 发起请求的函数
def get_completion(user_input):
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": long_text_content,
                    # 在此处放置 cache_control 标记，将创建从 messages 数组的开头到当前 content 所在位置的所有内容作为缓存块。
                    "cache_control": {"type": "ephemeral"},
                }
            ],
        },
        # 每次的提问内容不同
        {
            "role": "user",
            "content": user_input,
        },
    ]
    response = Generation.call(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"), 
        model="qwen3-coder-plus",
        messages=messages,
        result_format="message"
    )
    return response

# 第一次请求
first_completion = get_completion("这段代码的内容是什么")
print(f"第一次请求创建缓存 Token：{first_completion.usage.prompt_tokens_details['cache_creation_input_tokens']}")
print(f"第一次请求命中缓存 Token：{first_completion.usage.prompt_tokens_details['cached_tokens']}")
print("=" * 20)
# 第二次请求，代码内容一致，只修改了提问问题
second_completion = get_completion("这段代码可以怎么优化")
print(f"第二次请求创建缓存 Token：{second_completion.usage.prompt_tokens_details['cache_creation_input_tokens']}")
print(f"第二次请求命中缓存 Token：{second_completion.usage.prompt_tokens_details['cached_tokens']}")
```

Java

```
// Java SDK 最低版本为 2.21.6
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.MessageContentText;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;

import java.util.Arrays;
import java.util.Collections;

public class Main {
    private static final String MODEL = "qwen3-coder-plus";
    // 模拟代码仓库内容（400次重复确保超过1024 Token）
    private static final String LONG_TEXT_CONTENT = generateLongText(400);
    private static String generateLongText(int repeatCount) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < repeatCount; i++) {
            sb.append("<Your Code Here>");
        }
        return sb.toString();
    }
    private static GenerationResult getCompletion(String userQuestion)
            throws NoApiKeyException, ApiException, InputRequiredException {
        // 若使用新加坡地域模型，请将 https://dashscope.aliyuncs.com/api/v1 修改为 https://dashscope-intl.aliyuncs.com/api/v1
        Generation gen = new Generation("http", "https://dashscope.aliyuncs.com/api/v1");

        // 构建带缓存控制的系统消息
        MessageContentText systemContent = MessageContentText.builder()
                .type("text")
                .text(LONG_TEXT_CONTENT)
                .cacheControl(MessageContentText.CacheControl.builder()
                        .type("ephemeral") // 设置缓存类型
                        .build())
                .build();

        Message systemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .contents(Collections.singletonList(systemContent))
                .build();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content(userQuestion)
                .build();

        // 构建请求参数
        GenerationParam param = GenerationParam.builder()
                .model(MODEL)
                .messages(Arrays.asList(systemMsg, userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .build();
        return gen.call(param);
    }

    private static void printCacheInfo(GenerationResult result, String requestLabel) {
        System.out.printf("%s创建缓存 Token: %d%n", requestLabel, result.getUsage().getPromptTokensDetails().getCacheCreationInputTokens());
        System.out.printf("%s命中缓存 Token: %d%n", requestLabel, result.getUsage().getPromptTokensDetails().getCachedTokens());
    }

    public static void main(String[] args) {
        try {
            // 第一次请求
            GenerationResult firstResult = getCompletion("这段代码的内容是什么");
            printCacheInfo(firstResult, "第一次请求");
            System.out.println(new String(new char[20]).replace('\0', '='));            // 第二次请求
            GenerationResult secondResult = getCompletion("这段代码可以怎么优化");
            printCacheInfo(secondResult, "第二次请求");
        } catch (NoApiKeyException | ApiException | InputRequiredException e) {
            System.err.println("API调用失败: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

模拟的代码仓库内容通过添加 `cache_control`标记启用显式缓存。后续针对该代码仓库的提问请求，系统可复用该缓存块，无需重新计算，可获得比创建缓存前更快的响应与更低的成本。

```
第一次请求创建缓存 Token：1605
第一次请求命中缓存 Token：0
====================
第二次请求创建缓存 Token：0
第二次请求命中缓存 Token：1605
```

### 使用多个缓存标记实现精细控制

在复杂场景中，提示词通常由多个重用频率不同的部分组成。使用多个缓存标记可实现精细控制。

例如，智能客服的提示词通常包括：

-   **系统人设：**高度稳定，几乎不变。
    
-   **外部知识：**半稳定，通过知识库检索或工具查询获得，可能在连续对话中保持不变。
    
-   **对话历史：**动态增长。
    
-   **当前问题：**每次不同。
    

如果将整个提示词作为一个整体缓存，任何微小变化（如外部知识改变）都可能导致无法命中缓存。

在请求中最多可设置四个缓存标记，为提示词的不同部分分别创建缓存块，从而提升命中率并实现精细控制。

### **如何计费**

显式缓存仅影响输入 Token 的计费方式。规则如下：

-   **创建缓存**：新创建的缓存内容按标准输入单价的 125% 计费。若新请求的缓存内容包含已有缓存作为前缀，则仅对新增部分计费（即新缓存 Token 数减去已有缓存 Token 数）。
    
    例如：若已有 1200 Token 的缓存 A，新请求需缓存 1500 Token 的内容 AB，则前 1200 Token 按缓存命中计费（标准单价的 10%），新增的 300 Token 按创建缓存计费（标准单价的 125%）。
    
    > 创建缓存所用的 Token数通过`cache_creation_input_tokens` 参数查看。
    
-   **命中缓存**：按标准输入单价的 10% 计费。
    
    > 命中缓存的 Token数通过 `cached_tokens` 参数查看。
    
-   **其他 Token**：未命中且未创建缓存的 Token 按原价计费。
    

### **可缓存内容**

仅 `messages` 数组中的以下消息类型支持添加缓存标记：

-   系统消息（System Message）
    
-   用户消息（User Message）
    
    > 使用`qwen3-vl-plus`模型创建缓存时，`cache_control`标记可放置在多模态内容或文本之后，其位置不影响缓存整个用户消息的效果。
    
-   助手消息（Assistant Message）
    
-   工具消息（Tool Message，即工具执行后的结果）
    
    > 若请求包含 `tools` 参数，在`messages`中添加缓存标记还会缓存其中的工具描述信息。
    

以系统消息为例，需将 `content` 字段改为数组形式，并添加 `cache_control` 字段：

```
{
  "role": "system",
  "content": [
    {
      "type": "text",
      "text": "<指定的提示词>",
      "cache_control": {
        "type": "ephemeral"
      }
    }
  ]
}
```

此结构同样适用于 `messages` 数组中的其他消息类型。

### **缓存限制**

-   最小可缓存提示词长度为 **1024** Token。
    
-   缓存采用从后向前的前缀匹配策略，系统会自动检查最近的 20 个 content 块。若待匹配内容与带有 `cache_control` 标记的消息之间间隔超过 20 个 content 块，则无法命中缓存。
    
-   仅支持将 `type` 设置为 `ephemeral`，有效期为 5 分钟。
    
-   单次请求最多可添加 4 个缓存标记。
    
    > 若缓存标记个数大于4，则最后四个缓存标记生效。
    

### **使用示例**

**针对长文本的不同提问**

```
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为中国内地（北京）base_url，国际（新加坡）base_url为https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 模拟的代码仓库内容
long_text_content = "<Your Code Here>" * 400

# 发起请求的函数
def get_completion(user_input):
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": long_text_content,
                    # 在此处放置 cache_control 标记，将创建从messages数组开始，到本content结束位置（即模拟的代码仓库内容）的缓存。
                    "cache_control": {"type": "ephemeral"},
                }
            ],
        },
        {
            "role": "user",
            "content": user_input,
        },
    ]
    completion = client.chat.completions.create(
        # 选择支持显式缓存的模型
        model="qwen3-coder-plus",
        messages=messages,
    )
    return completion

# 第一次请求
first_completion = get_completion("这段代码的内容是什么")
created_cache_tokens = first_completion.usage.prompt_tokens_details.cache_creation_input_tokens
print(f"第一次请求创建缓存 Token：{created_cache_tokens}")
hit_cached_tokens = first_completion.usage.prompt_tokens_details.cached_tokens
print(f"第一次请求命中缓存 Token：{hit_cached_tokens}")
print(f"第一次请求未命中也未创建缓存的 Token：{first_completion.usage.prompt_tokens-created_cache_tokens-hit_cached_tokens}")
print("=" * 20)
# 第二次请求，代码内容一致，只修改了提问问题
second_completion = get_completion("这段代码有哪些可以优化的地方")
created_cache_tokens = second_completion.usage.prompt_tokens_details.cache_creation_input_tokens
print(f"第二次请求创建缓存 Token：{created_cache_tokens}")
hit_cached_tokens = second_completion.usage.prompt_tokens_details.cached_tokens
print(f"第二次请求命中缓存 Token：{hit_cached_tokens}")
print(f"第二次请求未命中也未创建缓存的 Token：{second_completion.usage.prompt_tokens-created_cache_tokens-hit_cached_tokens}")
```

此示例缓存代码仓库内容作为前缀。后续针对该仓库进行不同提问。

```
第一次请求创建缓存 Token：1605
第一次请求命中缓存 Token：0
第一次请求未命中也未创建缓存的 Token：13
====================
第二次请求创建缓存 Token：0
第二次请求命中缓存 Token：1605
第二次请求未命中也未创建缓存的 Token：15
```

> 系统为保证模型效果，会追加少量内部Token，这部分Token按标准输入价格计费，请参见[常见问题](#b728b718d5dxf)。

**持续多轮对话**

在日常聊天的多轮对话场景，可将每一次请求的 messages 数组中最后一个 content 添加缓存标记。从第二轮对话开始，每次请求都将命中并刷新前一轮对话创建的缓存块，且创建新的缓存块。

```
from openai import OpenAI
import os
  
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为中国内地（北京）base_url，国际（新加坡）base_url为https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

system_prompt = "你是说话风趣的人。" * 400
messages = [{"role": "system", "content": system_prompt}]

def get_completion(messages):
    completion = client.chat.completions.create(
        model="qwen3-coder-plus",
        messages=messages,
    )
    return completion

while True:
    user_input = input("请输入：")
    messages.append({"role": "user", "content": [{"type": "text", "text": user_input, "cache_control": {"type": "ephemeral"}}]})
    completion = get_completion(messages)
    print(f"[AI Response] {completion.choices[0].message.content}")
    messages.append(completion.choices[0].message)
    created_cache_tokens = completion.usage.prompt_tokens_details.cache_creation_input_tokens
    hit_cached_tokens = completion.usage.prompt_tokens_details.cached_tokens
    uncached_tokens = completion.usage.prompt_tokens - created_cache_tokens - hit_cached_tokens
    print(f"[Cache Info] 创建缓存 Token：{created_cache_tokens}")
    print(f"[Cache Info] 命中缓存 Token：{hit_cached_tokens}")
    print(f"[Cache Info] 未命中也未创建缓存的 Token：{uncached_tokens}")
```

运行以上代码，输入问题与大模型沟通，每次提问都会命中前一轮创建的缓存块。

## **隐式缓存**

### **支持的模型**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

-   **文本生成模型**
    
    -   [千问 Max](https://help.aliyun.com/zh/model-studio/models#cfc131abafghw)：qwen3-max、qwen-max
        
    -   [千问 Plus](https://help.aliyun.com/zh/model-studio/models#6c45e49509gtr)：qwen-plus
        
    -   [千问 Flash](https://help.aliyun.com/zh/model-studio/models#d617df95f1g9h)：qwen-flash
        
    -   [千问 Turbo](https://help.aliyun.com/zh/model-studio/models#8708390fdb66x)：qwen-turbo
        
    -   [千问 Coder](https://help.aliyun.com/zh/model-studio/models#d698550551bob)：qwen3-coder-plus、qwen3-coder-flash
        
    -   [DeepSeek](https://help.aliyun.com/zh/model-studio/models#935bd5ba5cg5d)：deepseek-v3.2、deepseek-v3.1、deepseek-v3、deepseek-r1
        
    -   [Kimi](https://help.aliyun.com/zh/model-studio/models#0ca6cec0252yp)：kimi-k2.5、kimi-k2-thinking、Moonshot-Kimi-K2-Instruct
        
    -   [GLM](https://help.aliyun.com/zh/model-studio/models#glm4.5)：glm-5、glm-4.7、glm-4.6
        
    -   [MiniMax](https://help.aliyun.com/zh/model-studio/models#6194236b53fx0)：MiniMax-M2.5、MiniMax-M2.1
        
-   **视觉理解模型**
    
    -   [千问 VL](https://help.aliyun.com/zh/model-studio/models#3f1f1c8913fvo)：qwen3-vl-plus、qwen3-vl-flash、qwen-vl-max、qwen-vl-plus
        
-   **行业模型**
    
    -   [角色扮演](https://help.aliyun.com/zh/model-studio/models#083f31bde1lv3)：qwen-plus-character
        
    -   [数据挖掘](https://help.aliyun.com/zh/model-studio/data-mining-qwen-doc)：qwen-doc-turbo
        

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

-   **文本生成模型**
    
    -   [千问 Max](https://help.aliyun.com/zh/model-studio/models#cfc131abafghw)：qwen3-max
        
    -   [千问 Plus](https://help.aliyun.com/zh/model-studio/models#6c45e49509gtr)：qwen-plus
        
    -   [千问 Flash](https://help.aliyun.com/zh/model-studio/models#d617df95f1g9h)：qwen-flash
        
    -   [千问 Coder](https://help.aliyun.com/zh/model-studio/models#d698550551bob)：qwen3-coder-plus、qwen3-coder-flash
        
-   **视觉理解模型**
    
    -   [千问 VL](https://help.aliyun.com/zh/model-studio/models#3f1f1c8913fvo)：qwen3-vl-plus、qwen3-vl-flash
        

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

-   **文本生成模型**
    
    -   [千问 Max](https://help.aliyun.com/zh/model-studio/models#c2d5833ae4jmo)：qwen3-max、qwen-max
        
    -   [千问 Plus](https://help.aliyun.com/zh/model-studio/models#6ad3cd90f0c5r)：qwen-plus
        
    -   [千问 Flash](https://help.aliyun.com/zh/model-studio/models#59857de48eps5)：qwen-flash
        
    -   [千问 Turbo](https://help.aliyun.com/zh/model-studio/models#ede6678dedqbz)：qwen-turbo
        
    -   [千问 Coder](https://help.aliyun.com/zh/model-studio/models#4f6fa69743l4j)：qwen3-coder-plus、qwen3-coder-flash
        
-   **视觉理解模型**
    
    -   [千问 VL](https://help.aliyun.com/zh/model-studio/models#3f1f1c8913fvo)：qwen3-vl-plus、qwen3-vl-flash、qwen-vl-max、qwen-vl-plus
        
-   **行业模型**
    
    -   [角色扮演](https://help.aliyun.com/zh/model-studio/models#083f31bde1lv3)：qwen-plus-character-ja
        

## 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

-   **文本生成模型**
    
    -   [千问 Plus](https://help.aliyun.com/zh/model-studio/models#6c45e49509gtr)：qwen-plus-us
        
    -   [千问 Flash](https://help.aliyun.com/zh/model-studio/models#d617df95f1g9h)：qwen-flash-us
        
-   **视觉理解模型**
    
    -   [千问 VL](https://help.aliyun.com/zh/model-studio/models#3f1f1c8913fvo)：qwen3-vl-flash-us
        

**说明**

暂不支持快照与 latest 模型。

### **工作方式**

向支持隐式缓存的模型发送请求时，该功能会自动开启。系统的工作方式如下：

1.  **查找**：收到请求后，系统基于**前缀匹配**原则，检查缓存中是否存在请求中 `messages` 数组内容的公共前缀。
    
2.  **判断**：
    
    -   若命中缓存，系统直接使用缓存结果进行后续部分的推理。
        
    -   若未命中，系统按常规处理请求，并将本次提示词的前缀存入缓存，以备后续请求使用。
        

> 系统会定期清理长期未使用的缓存数据。上下文缓存命中概率并非100%，即使请求上下文完全一致，仍可能未命中，具体命中概率由系统判定。

**说明**

不足 256 Token 的内容不会被缓存。

### **提升命中缓存的概率**

隐式缓存的命中逻辑是判断不同请求的**前缀**是否存在重复内容。为提高命中概率，**请将重复内容置于提示词开头，差异内容置于末尾。**

-   **文本模型**：假设系统已缓存"ABCD"，则请求"ABE"可能命中"AB"部分，而请求"BCD"则无法命中。
    
-   **视觉理解模型：**
    
    -   对**同一图像或视频**进行多次提问：将图像或视频放在文本信息前会提高命中概率。
        
    -   对**不同图像或视频**提问同一问题：将文本信息放在图像或视频前面会提高命中概率。
        

### 如何计费

开启隐式缓存模式无需额外付费。

当请求命中缓存时，命中的输入 Token 按 `cached_token` 计费（单价为`input_token`单价的**20%**）；未被命中的输入 Token 按标准 `input_token`计费。输出 Token 仍按原价计费。

示例：某请求包含 10,000 个输入 Token，其中 5,000 个命中缓存。费用计算如下：

-   未命中 Token (5,000)：按 100% 单价计费
    
-   命中 Token (5,000)：按 20% 单价计费
    

总输入费用相当于无缓存模式的 60%：(50% × 100%) + (50% × 20%) = 60%。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1913916571/p893561.png)

可从[返回结果](#366ab5759d8ab)的`cached_tokens`属性获取命中缓存的 Token 数。

> [OpenAI兼容-Batch（文件输入）](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)方式调用无法享受缓存折扣。

### **命中缓存的案例**

## 文本生成模型

## OpenAI兼容

当您使用 OpenAI 兼容的方式调用模型并触发了隐式缓存后，可以得到如下的返回结果，在`usage.prompt_tokens_details.cached_tokens`可以查看命中缓存的 Token 数（该数值为`usage.prompt_tokens`的一部分）。

```
{
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "我是阿里云开发的一款超大规模语言模型，我叫千问。"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
        }
    ],
    "object": "chat.completion",
    "usage": {
        "prompt_tokens": 3019,
        "completion_tokens": 104,
        "total_tokens": 3123,
        "prompt_tokens_details": {
            "cached_tokens": 2048
        }
    },
    "created": 1735120033,
    "system_fingerprint": null,
    "model": "qwen-plus",
    "id": "chatcmpl-6ada9ed2-7f33-9de2-8bb0-78bd4035025a"
}
```

## DashScope

当您使用DashScope Python SDK 或 HTTP 方式调用模型并触发了隐式缓存后，可以得到如下的返回结果，在`usage.prompt_tokens_details.cached_tokens`可以查看命中缓存的 Token 数（该数值是 `usage.input_tokens` 的一部分。）。

```
{
    "status_code": 200,
    "request_id": "f3acaa33-e248-97bb-96d5-cbeed34699e1",
    "code": "",
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": "我是一个来自阿里云的大规模语言模型，我叫千问。我可以生成各种类型的文本，如文章、故事、诗歌、故事等，并能够根据不同的场景和需求进行变换和扩展。此外，我还能够回答各种问题，提供帮助和解决方案。如果您有任何问题或需要帮助，请随时告诉我，我会尽力提供支持。请注意，连续重复相同的内容可能无法获得更详细的答复，建议您提供更多具体信息或变化提问方式以便我更好地理解您的需求。"
                }
            }
        ]
    },
    "usage": {
        "input_tokens": 3019,
        "output_tokens": 101,
        "prompt_tokens_details": {
            "cached_tokens": 2048
        },
        "total_tokens": 3120
    }
}
```

## 视觉理解模型

## OpenAI兼容

当您使用 OpenAI 兼容的方式调用模型并触发了隐式缓存后，可以得到如下的返回结果，在`usage.prompt_tokens_details.cached_tokens`可以查看命中缓存的 Token 数（该 Token 数是`usage.prompt_tokens`的一部分）。

> qwen3-vl-plus、qwen3-vl-flash模型使用 OpenAI  SDK 调用支持隐式缓存功能，但暂时无法查看`cached_tokens`。

```
{
  "id": "chatcmpl-3f3bf7d0-b168-9637-a245-dd0f946c700f",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "这张图像展示了一位女性和一只狗在海滩上互动的温馨场景。女性穿着格子衬衫，坐在沙滩上，面带微笑地与狗进行互动。狗是一只大型的浅色犬种，戴着彩色的项圈，前爪抬起，似乎在与女性握手或击掌。背景是广阔的海洋和天空，阳光从画面的右侧照射过来，给整个场景增添了一种温暖而宁静的氛围。",
        "refusal": null,
        "role": "assistant",
        "audio": null,
        "function_call": null,
        "tool_calls": null
      }
    }
  ],
  "created": 1744956927,
  "model": "qwen-vl-max",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": null,
  "usage": {
    "completion_tokens": 93,
    "prompt_tokens": 1316,
    "total_tokens": 1409,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 1152
    }
  }
}
```

## DashScope

当您使用DashScope Python SDK 或 HTTP 方式调用模型并触发了隐式缓存后，命中缓存的Token数包含在总输入Token（usage.input\_tokens）中，具体查看位置因地域和模型而异：

-   北京地域：
    
    -   `qwen-vl-max`、`qwen-vl-plus`：在`usage.prompt_tokens_details.cached_tokens`查看 
        
    -   `qwen3-vl-plus`、`qwen3-vl-flash`：在 `usage.cached_tokens`查看 
        
-   新加坡地域：所有模型均查看 `usage.cached_tokens`
    

> 目前使用`usage.cached_tokens`的模型，后续将升级至`usage.prompt_tokens_details.cached_tokens`。

```
{
  "status_code": 200,
  "request_id": "06a8f3bb-d871-9db4-857d-2c6eeac819bc",
  "code": "",
  "message": "",
  "output": {
    "text": null,
    "finish_reason": null,
    "choices": [
      {
        "finish_reason": "stop",
        "message": {
          "role": "assistant",
          "content": [
            {
              "text": "这张图像展示了一位女性和一只狗在海滩上互动的温馨场景。女性穿着格子衬衫，坐在沙滩上，面带微笑地与狗进行互动。狗是一只大型犬，戴着彩色项圈，前爪抬起，似乎在与女性握手或击掌。背景是广阔的海洋和天空，阳光从画面右侧照射过来，给整个场景增添了一种温暖而宁静的氛围。"
            }
          ]
        }
      }
    ]
  },
  "usage": {
    "input_tokens": 1292,
    "output_tokens": 87,
    "input_tokens_details": {
      "text_tokens": 43,
      "image_tokens": 1249
    },
    "total_tokens": 1379,
    "output_tokens_details": {
      "text_tokens": 87
    },
    "image_tokens": 1249,
    "prompt_tokens_details": {
      "cached_tokens": 1152
    }
  }
}
```

### **典型场景**

如果您的不同请求有着相同的前缀信息，上下文缓存可以有效提升这些请求的推理速度，降低推理成本与首包延迟。以下是几个典型的应用场景：

1.  **基于长文本的问答**
    
    适用于需要针对固定的长文本（如小说、教材、法律文件等）发送多次请求的业务场景。
    
    **第一次请求的消息数组**
    
    ```
    messages = [{"role": "system","content": "你是一个语文老师，你可以帮助学生进行阅读理解。"},
              {"role": "user","content": "<文章内容> 这篇课文表达了作者怎样的思想感情？"}]
    ```
    
    **之后请求的消息数组**
    
    ```
    messages = [{"role": "system","content": "你是一个语文老师，你可以帮助学生进行阅读理解。"},
              {"role": "user","content": "<文章内容> 请赏析这篇课文的第三自然段。"}]
    ```
    
    虽然提问的问题不同，但都基于同一篇文章。相同的系统提示和文章内容构成了大量重复的前缀信息，有较大概率命中缓存。
    
2.  **代码自动补全**
    
    在代码自动补全场景，大模型会结合上下文中存在的代码进行代码自动补全。随着用户的持续编码，代码的前缀部分会保持不变。上下文缓存可以缓存之前的代码，提升补全速度。
    
3.  **多轮对话**
    
    实现多轮对话需要将每一轮的对话信息添加到 messages 数组中，因此每轮对话的请求都会存在与前轮对话前缀相同的情况，有较高概率命中缓存。
    
    **第一轮对话的消息数组**
    
    ```
    messages=[{"role": "system","content": "You are a helpful assistant."},
              {"role": "user","content": "你是谁？"}]
    ```
    
    **第二轮对话的消息数组**
    
    ```
    messages=[{"role": "system","content": "You are a helpful assistant."},
              {"role": "user","content": "你是谁？"},
              {"role": "assistant","content": "我是由阿里云开发的千问。"},
              {"role": "user","content": "你能干什么？"}]
    ```
    
    随着对话轮数的增加，缓存带来的推理速度优势与成本优势会更明显。
    
4.  **角色扮演或 Few Shot**
    
    在角色扮演或 Few-shot 学习的场景中，您通常需要在提示词中加入大量信息来指引大模型的输出格式，这样不同的请求之间会有大量重复的前缀信息。
    
    以让大模型扮演营销专家为例，System prompt包含有大量文本信息，以下是两次请求的消息示例：
    
    ```
    system_prompt = """你是一位经验丰富的营销专家。请针对不同产品提供详细的营销建议，格式如下：
    
    1. 目标受众：xxx
    
    2. 主要卖点：xxx
    
    3. 营销渠道：xxx
    ...
    12. 长期发展策略：xxx
    
    请确保你的建议具体、可操作，并与产品特性高度相关。"""
    
    # 第一次请求的user message 提问关于智能手表
    messages_1=[
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": "请为一款新上市的智能手表提供营销建议。"}
    ]
    
    # 第二次请求的user message 提问关于笔记本电脑，由于system_prompt相同，有较大概率命中 Cache
    messages_2=[
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": "请为一款新上市的笔记本电脑提供营销建议。"}
    ]
    ```
    
    使用上下文缓存后，即使用户频繁更换询问的产品类型（如从智能手表到笔记本电脑），系统也可以在触发缓存后快速响应。
    
5.  **视频理解**
    
    在视频理解场景中，如果对同一个视频提问多次，将`video`放在`text`前会提高命中缓存的概率；如果对不同的视频提问相同的问题，则将`text`放在`video`前面，会提高命中缓存的概率。以下是对同一个视频请求两次的消息示例：
    
    ```
    # 第一次请求的user message 提问这段视频的内容
    messages1 = [
        {"role":"system","content":[{"text": "You are a helpful assistant."}]},
        {"role": "user",
            "content": [
                {"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250328/eepdcq/phase_change_480p.mov"},
                {"text": "这段视频的内容是什么?"}
            ]
        }
    ]
    
    # 第二次请求的user message 提问关于视频时间戳相关的问题，由于基于同一个视频进行提问，将video放在text前面，有较大概率命中 Cache
    messages2 = [
        {"role":"system","content":[{"text": "You are a helpful assistant."}]},
        {"role": "user",
            "content": [
                {"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250328/eepdcq/phase_change_480p.mov"},
                {"text": "请你描述下视频中的一系列活动事件，以JSON格式输出开始时间（start_time）、结束时间（end_time）、事件（event），不要输出```json```代码段"}
            ]
        }
    ]
    ```
    

## **常见问题**

### **Q：如何关闭隐式缓存？**

A：无法关闭。隐式缓存对所有适用模型请求开启的前提是对回复效果没有影响，且在命中缓存时降低使用成本，提升响应速度。

### **Q：为什么创建显式缓存后没有命中？**

A：有以下可能原因：

-   创建后 5 分钟内未被命中，超过有效期系统将清理该缓存块；
    
-   最后一个`content`与已存在的缓存块的间隔大于20个`content`块时，不会命中缓存，建议创建新的缓存块。
    

### **Q：显式缓存命中后，是否会重置有效期？**

A：是的，每次命中都会将该缓存块的有效期重置为5分钟。

### **Q：不同账号之间的显式缓存是否会共享？**

A：不会。无论是隐式缓存还是显式缓存，数据都在账号级别隔离，不会共享。

### **Q：**相同账号使用不同模型显式缓存是否会共享？

A：不会。缓存数据存在模型间隔离，不会共享。

### **Q：为什么**`**usage**`**的**`**input_tokens**`**不等于**`**cache_creation_input_tokens**`**和**`**cached_tokens**`**的总和？**

A：为了确保模型输出效果，后端服务会在用户提供的提示词之后追加少量 Token（通常在10以内），这些 Token 在 `cache_control` 标记之后，因此不会被计入缓存的创建或读取，但会计入总的 `input_tokens`。
对于无需实时响应的推理场景，批量推理能异步处理大批量的数据请求，成本仅为实时推理的 **50%**，且接口兼容 OpenAI，适合执行模型评测、数据标注等批量作业。

## **工作流程**

批量推理采用异步模式：

1.  提交任务：上传包含多个请求的文件，创建一个批量推理任务。
    
2.  异步处理：系统在后台处理队列中的任务。任务进度和状态可在控制台或通过 API 查询。
    
3.  下载结果：任务完成后，系统会生成一个包含成功响应的结果文件和一个包含失败详情的错误文件（如有）。
    

## **适用范围**

### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

**支持的模型**

-   **文本生成模型**：千问 Max、Plus、Flash、Turbo、Long 的稳定版本及其部分 `latest` 版本，以及 QwQ 系列（qwq-plus、qwq-32b-preview）和部分第三方模型（deepseek-r1、deepseek-v3.2、deepseek-v3）。
    
-   **多模态模型**：千问 VL Max、Plus、Flash、OCR的稳定版本及其部分 `latest` 版本，以及千问 Omni 模型。
    
-   **文本向量模型**：所有版本的 text-embedding 模型。
    

支持的模型名称清单

-   **文本生成模型**
    
    -   [千问 Max](https://help.aliyun.com/zh/model-studio/models#cfc131abafghw)：qwen3-max、qwen-max、qwen-max-latest
        
    -   [千问 Plus](https://help.aliyun.com/zh/model-studio/models#6c45e49509gtr)：qwen3.5-plus、qwen-plus、qwen-plus-latest
        
    -   [千问 Flash](https://help.aliyun.com/zh/model-studio/models#d617df95f1g9h)：qwen3.5-flash、qwen-flash
        
    -   [千问 Turbo](https://help.aliyun.com/zh/model-studio/models#8708390fdb66x)：qwen-turbo、qwen-turbo-latest
        
    -   [千问 Long](https://help.aliyun.com/zh/model-studio/models#27b2b3a15d5c6)：qwen-long、qwen-long-latest
        
    -   [QwQ](https://help.aliyun.com/zh/model-studio/models#874b221f2cx9k)：qwq-plus
        
    -   [QwQ-Preview](https://help.aliyun.com/zh/model-studio/models#18e88cc886ll3)：qwq-32b-preview
        
    -   第三方模型：deepseek-r1、deepseek-v3.2、deepseek-v3
        
-   **多模态模型**
    
    -   [图像与视频理解](https://help.aliyun.com/zh/model-studio/vision)：qwen3.5-plus、qwen3.5-flash、qwen3-vl-plus、qwen3-vl-flash、qwen-vl-max、qwen-vl-max-latest、qwen-vl-plus、qwen-vl-plus-latest
        
    -   [文字提取](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr)：qwen-vl-ocr、qwen-vl-ocr-latest
        
    -   [全模态](https://help.aliyun.com/zh/model-studio/user-guide/qwen-omni)：qwen-omni-turbo
        
-   [**文本向量模型**](https://help.aliyun.com/zh/model-studio/user-guide/embedding)**：**text-embedding-v1、text-embedding-v2、text-embedding-v3、text-embedding-v4
    

**重要**

-   部分模型支持思考模式，开启后会产生思考`tokens`导致成本增加。
    
-   `qwen3.5` 系列模型（如 `qwen3.5-plus`、`qwen3.5-flash`）默认开启思考模式。建议使用混合思考模型时，显式设置`enable_thinking`参数（`true`开启/`false`关闭）。
    

### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**支持的模型**：qwen-max、qwen-plus、qwen-turbo。

## **如何使用**

### **步骤一：准备输入文件**

创建批量推理任务前，需先准备一个符合以下规范的文件：

-   **格式**：UTF-8 编码的 JSONL（每行一个独立 JSON 对象）。
    
-   **规模限制**：单文件 ≤ 50,000 个请求，且 ≤ 500 MB。
    
    > 如果数据量超过此限制，建议拆分任务分别提交。
    
-   **单行限制**：每个 JSON 对象 ≤ 6 MB，且不超过模型上下文长度。
    
-   **一致性要求**：同一文件内所有请求须使用相同模型及思考模式（如适用）。
    
-   **唯一标识**：每个请求必须包含文件内唯一的 custom\_id 字段，用于结果匹配。
    

#### **示例文件**

可下载示例文件[test\_model.jsonl](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250926/wrheek/test_model.jsonl)，内容为：

```
{"custom_id":"1","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen-max","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"你好！有什么可以帮助你的吗？"}]}}
{"custom_id":"2","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen-max","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"What is 2+2?"}]}}
```

**JSONL 批量生成工具**

使用以下工具可快速生成 JSONL 文件。

 JSONL 批量生成工具 \* { box-sizing: border-box; } body { margin: 0; padding: 20px; font-family: sans-serif; width: 100%; max-width: 100%; overflow-x: auto; } #components-container { width: 50%; max-width: 50%; } .model-component { width: 100%; max-width: 100%; } /\* 地域选择器样式 - 按钮样式 \*/ .region-selector { display: flex; gap: 8px; align-items: center; margin-bottom: 15px; } .region-option { cursor: pointer; padding: 8px 16px; border-radius: 4px; transition: all 0.2s; border: 1px solid #ccc; background-color: #fff; color: #333; font-size: 14px; user-select: none; outline: none; } .region-option:hover { background: #f7f8fa; border-color: #007bff; } .region-option.checked { background-color: #007bff; border-color: #007bff; color: #fff; } .region-option.checked:hover { background-color: #0056b3; border-color: #0056b3; } /\* 响应式设计 \*/ @media (max-width: 768px) { body { padding: 10px; } #components-container { width: 80%; max-width: 80%; } .model-component { padding: 10px; } } @media (max-width: 480px) { body { padding: 5px; } #components-container { width: 95%; max-width: 95%; } .model-component { padding: 8px; } }

**请选择模式：**

中国内地 国际

**选择模型系列:** 文本生成模型 多模态模型 通用文本向量模型

**选择具体模型:** qwen3-max qwen-max qwen-max-latest qwen3.5-plus（思考模式） qwen3.5-plus（非思考模式） qwen3.5-flash（思考模式） qwen3.5-flash（非思考模式） qwen-flash（思考模式） qwen-flash（非思考模式） qwen-plus（思考模式） qwen-plus（非思考模式） qwen-plus-latest（思考模式） qwen-plus-latest（非思考模式） qwen-turbo（思考模式） qwen-turbo（非思考模式） qwen-turbo-latest（思考模式） qwen-turbo-latest（非思考模式） qwen-long qwen-long-latest qwq-plus qwq-32b-preview deepseek-r1 deepseek-v3

**写入您的请求内容（每行一条请求）:** 你好！有什么可以帮助你的吗？ What is 2+2?

**粘贴您的媒体URL (每行一个或多个，英文逗号分隔):** **输入您对媒体的提问:**

生成

**请选择模式：**

中国内地 国际

**选择模型系列:** 文本生成模型

**选择具体模型:** qwen-max qwen-plus qwen-turbo

**写入您的请求内容（每行一条请求）:** 你好！有什么可以帮助你的吗？ What is 2+2?

生成

### **步骤二：提交并查看结果**

#### **（一）创建批量推理任务**

1.  在**[批量推理](https://bailian.console.aliyun.com/?tab=model#/model-batch)**页面，单击**创建批量推理任务**。
    
2.  在弹出的对话框中：填写**任务名称**和**描述**、设置**最长等待时间**（1-14天），上传JSONL 文件。
    
    > 可点击**下载示例文件**获取模板。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6926999571/p1014111.png)
    
3.  填写完成后，单击**确认**。
    

#### **（二）查看与管理任务**

-   **查看**：
    
    -   在任务列表页，可查看任务的**进度**（已处理请求数/总请求数）和**状态**。
        
    -   支持按任务名称/ID搜索或按业务空间筛选，以快速定位任务。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0718532671/p1014066.png)
        
-   **管理**：
    
    -   取消：“执行中”的任务可在**操作**列取消。
        
    -   排错：“失败”的任务可通过悬停状态查看概要，下载错误文件查看详情。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3324411471/p924094.png)
        

#### **（三）下载并分析结果**

任务完成后，单击**查看结果**，可下载产出文件：![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5044999571/p1014076.png)

-   **结果文件**： 记录所有成功的请求及其 `response` 结果。
    
-   **错误文件（如有）**： 记录所有失败的请求及其 `error` 详情。
    

两个文件均包含 `custom_id` 字段，用于与原始输入数据进行匹配，从而关联结果或定位错误。

### **步骤三：查看数据统计（可选）**

在[模型用量](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-usage/usage-statistics)页面，可筛选并查看批量推理的用量统计。

-   **查看数据概览**： 选择要查询的**时间范围**（最长支持30天），将**推理类型**选为**批量推理**，可查看用于批量推理的模型调用概览。
    
-   **查看模型详情**：
    
    -   点击选择不同的模型类别（如：**大语言模型**）进入信息页，选择要查询的**时间范围**（最长支持30天），将**推理类型**选为**批量推理**，可查看当前类别模型的调用信息。
        
    -   然后点击对应模型右侧的**查看详情**，可查看单模型的调用情况。
        

**重要**

-   批量推理的调用数据以**任务结束时间**为准进行统计。对于正在运行的任务，其调用信息在任务完成前无法查询到。
    
-   监控数据存在1～2小时延迟。
    

## **相关 API**

对于需要自动化和集成的生产环境，推荐使用与 OpenAI 兼容的 API 创建和管理 Batch 任务，核心流程为：

1.  [**上传文件**](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/#fdd1a4b6d86id)
    
    调用 `POST /v1/files` 接口上传文件，并记录返回的文件 ID。
    
2.  [**创建任务**](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/#fdd1a4b6d86id)  
    传入上传文件返回的文件 ID或 OSS 路径 ，调用 `POST /v1/batches` 接口创建任务，并记录返回的 `batch_id`。
    
3.  [**轮询状态**](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/#fdd1a4b6d86id)  
    使用 `batch_id` 轮询 `GET /v1/batches/{batch_id}` 接口。当 `status` 字段变为 `completed` 时，记录返回的 `output_file_id` 并停止轮询。
    
4.  [**下载结果**](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/#fdd1a4b6d86id)  
    使用 `output_file_id` 调用 `GET /v1/files/{output_file_id}/content` 接口，即可下载结果文件。
    

完整的 Batch API 接口定义和代码示例请参见[OpenAI兼容-Batch（文件输入）](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)。

## **任务生命周期**

-   **validating（验证中）：**系统正在校验上传的数据文件格式是否符合 JSONL 规范，以及文件内的每一行请求是否符合 API 格式要求。
    
-   **in\_progress（执行中）：**文件验证通过，系统已开始逐行处理文件中的推理请求。
    
-   **completed（已完成）：**结果文件和错误文件数据已写入完成，可下载。
    
-   **failed（失败）：**任务在 validating 状态失败，通常由文件级错误（如 JSONL 格式错误、文件过大）导致。此状态下，任务不会执行任何推理请求，也不会产生结果文件。
    
-   **expired（已终止）：**任务因运行时间超过创建时设定的最长等待时间而被系统终止。如果任务因此失败，建议在创建新任务时设置更长的等待时间。
    
-   **cancelled（已取消）：**任务已取消。任务中未开始处理的请求将被终止。
    

## 计费说明

-   **计费单价：**所有成功请求的输入和输出Token，单价均为对应模型实时推理价格的**50%**，具体请参见[模型列表](https://help.aliyun.com/zh/model-studio/models#9f8890ce29g5u)。
    
-   **计费范围：**
    
    -   仅对任务中成功执行的请求进行计费。
        
    -   文件解析失败、任务执行失败、或行级错误请求均**不产生费用**。
        
    -   对于被取消的任务，在取消操作前已成功完成的请求仍会正常计费。
        

**说明**

-   批量推理为独立计费项，支持[AI 通用型节省计划](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#universal-savings-plan)，但不支持[预付费](https://common-buy.aliyun.com/?commodityCode=sfm_llminference_spn_public_cn)（节省计划）、[新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)等优惠，以及[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)等功能。
    
-   部分模型（如 qwen3.5-plus、qwen3.5-flash）默认开启思考模式，会产生额外的思考tokens，并按输出token价格计费，导致成本增加。建议根据任务复杂度设置enable\_thinking参数以控制成本，具体请参考[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)。
    

## 常见问题

1.  **使用批量推理需要额外购买或开通吗？**
    
    不需要。只要已开通阿里云百炼服务。费用将按**后付费模式**从账户余额中扣除。
    
2.  **任务提交后为什么立即失败（状态变为** `**failed**`**）？**
    
    这通常是文件级错误导致的，任务并未开始执行任何推理请求。请按以下顺序排查：
    
    -   **文件格式**：是否为严格的 JSONL 格式，每行一个完整的 JSON 对象。
        
    -   **文件规模：**文件大小、行数等是否超出限制。详情请参见[准备输入文件](#cdb5ab7b74k2t)。
        
    -   **模型一致性：**检查文件中所有请求的 `body.model` 字段是否完全一致，且使用的是当前地域支持的模型。
        
3.  **任务处理需要多长时间？**
    
    任务处理时长主要取决于系统当时的负载，当系统繁忙时，任务可能需要排队等待资源，成功或失败都会在设定的“最长等待时间”内返回结果。
    

## 错误码

如果调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

千问系列的录音文件识别模型能将录制好的音频转换为文本，支持多语言识别、歌唱识别、噪声拒识等功能。

## **核心功能**

-   **多语种识别：**支持多语种语音识别（涵盖普通话及多种方言，如粤语、四川话等）。
    
-   **复杂环境适应：**具备应对复杂声学环境的能力，支持自动语种检测与智能非人声过滤。
    
-   **歌唱识别：**即使在伴随背景音乐（BGM）的情况下，也能实现整首歌曲的转写。
    
-   **情感识别：**支持多种情绪状态识别（涵盖惊讶、平静、愉快、悲伤、厌恶、愤怒和恐惧）。
    

## **适用范围**

**支持的模型：**

服务主要提供两大核心模型：

-   **千问3-ASR-Flash-Filetrans**：专为长音频（最长12小时）的异步识别设计，适用于会议记录、访谈整理等场景。
    
-   **千问3-ASR-Flash**：专为短音频（最长5分钟）的同步或流式识别设计，适用于语音消息、实时字幕等场景。
    

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

调用以下模型时，请选择北京地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)：

-   **千问3-ASR-Flash-Filetrans：**qwen3-asr-flash-filetrans（稳定版，当前等同qwen3-asr-flash-filetrans-2025-11-17）、qwen3-asr-flash-filetrans-2025-11-17（快照版）
    
-   **千问3-ASR-Flash：**qwen3-asr-flash（稳定版，当前等同qwen3-asr-flash-2025-09-08）、qwen3-asr-flash-2026-02-10（最新快照版）、qwen3-asr-flash-2025-09-08（快照版）
    
-   **千问Audio ASR：**qwen-audio-asr（稳定版）
    
    千问Audio ASR为Beta版，目前仅供免费体验，免费额度用完后不支持调用，推荐使用千问3-ASR-Flash-Filetrans或千问3-ASR-Flash
    

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

调用以下模型时，请选择新加坡地域的[API Key](https://modelstudio.console.aliyun.com/?tab=dashboard#/api-key)：

-   **千问3-ASR-Flash-Filetrans：**qwen3-asr-flash-filetrans（稳定版，当前等同qwen3-asr-flash-filetrans-2025-11-17）、qwen3-asr-flash-filetrans-2025-11-17（快照版）
    
-   **千问3-ASR-Flash：**qwen3-asr-flash（稳定版，当前等同qwen3-asr-flash-2025-09-08）、qwen3-asr-flash-2026-02-10（最新快照版）、qwen3-asr-flash-2025-09-08（快照版）
    

## 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

调用以下模型时，请选择美国地域的[API Key](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/api-key)：

**千问3-ASR-Flash：**qwen3-asr-flash-us（稳定版，当前等同qwen3-asr-flash-2025-09-08-us）、qwen3-asr-flash-2025-09-08-us（快照版）

更多信息请参见[模型列表](https://help.aliyun.com/zh/model-studio/models)

## **模型选型**

| **场景** | **推荐模型** | **理由** | **注意事项** |
| --- | --- | --- | --- |
| **长音频识别** | qwen3-asr-flash-filetrans | 支持最长12小时录音，具备情感识别与句/字级别时间戳功能，适合后期索引与分析 | 音频文件大小不超过2GB，且时长不超过12小时 |
| **短音频识别** | qwen3-asr-flash或qwen3-asr-flash-us | 短音频识别，低延迟 | 音频文件大小不超过10MB，且时长不超过5分钟 |
| **客服质检** | qwen3-asr-flash-filetrans、qwen3-asr-flash或qwen3-asr-flash-us | 可分析客户情绪 | 不支持敏感词过滤；无说话人分离；根据音频时长选择合适的模型 |
| **新闻/访谈节目字幕生成** | qwen3-asr-flash-filetrans | 长音频+标点预测+时间戳，直接生成结构化字幕 | 需后处理生成标准字幕文件；根据音频时长选择合适的模型 |
| **多语种视频本地化** | qwen3-asr-flash-filetrans、qwen3-asr-flash或qwen3-asr-flash-us | 覆盖多种语言+方言，适合跨语种字幕制作 | 根据音频时长选择合适的模型 |
| **歌唱类音频分析** | qwen3-asr-flash-filetrans、qwen3-asr-flash或qwen3-asr-flash-us | 识别歌词并分析情绪，适用于歌曲索引与推荐 | 根据音频时长选择合适的模型 |

更多说明请参见[模型功能特性对比](#ea5edc7ae4cq7)。

## **快速开始**

API 使用前提：已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。如果通过SDK调用，需要[安装最新版SDK](https://help.aliyun.com/zh/model-studio/install-sdk#8833b9274f4v8)。

## DashScope

## 千问3-ASR-Flash-Filetrans

千问3-ASR-Flash-Filetrans模型专为音频文件的异步转写设计，支持最长12小时录音。该模型要求输入为公网可访问的音频文件URL，不支持直接上传本地文件。此外，它是一个非流式接口，会在任务完成后一次性返回全部识别结果。

## cURL

使用 cURL 进行语音识别时，需先提交任务获取任务ID（task\_id），再通过该ID获取任务执行结果。

## 提交任务

```
# ======= 重要提示 =======
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/audio/asr/transcription
# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# === 执行时请删除该注释 ===

curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-Async: enable" \
-d '{
    "model": "qwen3-asr-flash-filetrans",
    "input": {
        "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
    },
    "parameters": {
        "channel_id":[
            0
        ],
        "enable_itn": false,
        "enable_words": true
    }
}'
```

## 获取任务执行结果

```
# ======= 重要提示 =======
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}，注意，将{task_id}替换为待查询任务ID
# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# === 执行时请删除该注释 ===

curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "X-DashScope-Async: enable" \
-H "Content-Type: application/json"
```

## 完整示例

## Java

```
import com.google.gson.Gson;
import com.google.gson.annotations.SerializedName;
import okhttp3.*;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

public class Main {
    // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/audio/asr/transcription
    private static final String API_URL_SUBMIT = "https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription";
    // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/tasks/
    private static final String API_URL_QUERY = "https://dashscope.aliyuncs.com/api/v1/tasks/";
    private static final Gson gson = new Gson();

    public static void main(String[] args) {
        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：String apiKey = "sk-xxx"
        String apiKey = System.getenv("DASHSCOPE_API_KEY");

        OkHttpClient client = new OkHttpClient();

        // 1. 提交任务
        /*String payloadJson = """
                {
                    "model": "qwen3-asr-flash-filetrans",
                    "input": {
                        "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                    },
                    "parameters": {
                        "channel_id": [0],
                        "enable_itn": false,
                        "language": "zh"
                    }
                }
                """;*/
        String payloadJson = """
                {
                    "model": "qwen3-asr-flash-filetrans",
                    "input": {
                        "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                    },
                    "parameters": {
                        "channel_id": [0],
                        "enable_itn": false,
                        "enable_words": true
                    }
                }
                """;

        RequestBody body = RequestBody.create(payloadJson, MediaType.get("application/json; charset=utf-8"));
        Request submitRequest = new Request.Builder()
                .url(API_URL_SUBMIT)
                .addHeader("Authorization", "Bearer " + apiKey)
                .addHeader("Content-Type", "application/json")
                .addHeader("X-DashScope-Async", "enable")
                .post(body)
                .build();

        String taskId = null;

        try (Response response = client.newCall(submitRequest).execute()) {
            if (response.isSuccessful() && response.body() != null) {
                String respBody = response.body().string();
                ApiResponse apiResp = gson.fromJson(respBody, ApiResponse.class);
                if (apiResp.output != null) {
                    taskId = apiResp.output.taskId;
                    System.out.println("任务已提交，task_id: " + taskId);
                } else {
                    System.out.println("提交返回内容: " + respBody);
                    return;
                }
            } else {
                System.out.println("任务提交失败! HTTP code: " + response.code());
                if (response.body() != null) {
                    System.out.println(response.body().string());
                }
                return;
            }
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }

        // 2. 轮询任务状态
        boolean finished = false;
        while (!finished) {
            try {
                TimeUnit.SECONDS.sleep(2);  // 等待 2 秒再查询
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }

            String queryUrl = API_URL_QUERY + taskId;
            Request queryRequest = new Request.Builder()
                    .url(queryUrl)
                    .addHeader("Authorization", "Bearer " + apiKey)
                    .addHeader("X-DashScope-Async", "enable")
                    .addHeader("Content-Type", "application/json")
                    .get()
                    .build();

            try (Response response = client.newCall(queryRequest).execute()) {
                if (response.body() != null) {
                    String queryResponse = response.body().string();
                    ApiResponse apiResp = gson.fromJson(queryResponse, ApiResponse.class);

                    if (apiResp.output != null && apiResp.output.taskStatus != null) {
                        String status = apiResp.output.taskStatus;
                        System.out.println("当前任务状态: " + status);
                        if ("SUCCEEDED".equalsIgnoreCase(status)
                                || "FAILED".equalsIgnoreCase(status)
                                || "UNKNOWN".equalsIgnoreCase(status)) {
                            finished = true;
                            System.out.println("任务完成，最终结果: ");
                            System.out.println(queryResponse);
                        }
                    } else {
                        System.out.println("查询返回内容: " + queryResponse);
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
                return;
            }
        }
    }

    static class ApiResponse {
        @SerializedName("request_id")
        String requestId;
        Output output;
    }

    static class Output {
        @SerializedName("task_id")
        String taskId;
        @SerializedName("task_status")
        String taskStatus;
    }
}
```

## Python

```
import os
import time
import requests
import json

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/audio/asr/transcription
API_URL_SUBMIT = "https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription"
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/tasks/
API_URL_QUERY_BASE = "https://dashscope.aliyuncs.com/api/v1/tasks/"


def main():
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx"
    api_key = os.getenv("DASHSCOPE_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable"
    }

    # 1. 提交任务
    payload = {
        "model": "qwen3-asr-flash-filetrans",
        "input": {
            "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
        },
        "parameters": {
            "channel_id": [0],
            # "language": "zh",
            "enable_itn": False,
            "enable_words": True
        }
    }

    print("提交 ASR 转写任务...")
    try:
        submit_resp = requests.post(API_URL_SUBMIT, headers=headers, data=json.dumps(payload))
    except requests.RequestException as e:
        print(f"请求提交任务失败: {e}")
        return

    if submit_resp.status_code != 200:
        print(f"任务提交失败! HTTP code: {submit_resp.status_code}")
        print(submit_resp.text)
        return

    resp_data = submit_resp.json()
    output = resp_data.get("output")
    if not output or "task_id" not in output:
        print("提交返回内容异常:", resp_data)
        return

    task_id = output["task_id"]
    print(f"任务已提交，task_id: {task_id}")

    # 2. 轮询任务状态
    finished = False
    while not finished:
        time.sleep(2)  # 等待 2 秒再查询

        query_url = API_URL_QUERY_BASE + task_id
        try:
            query_resp = requests.get(query_url, headers=headers)
        except requests.RequestException as e:
            print(f"请求查询任务失败: {e}")
            return

        if query_resp.status_code != 200:
            print(f"查询任务失败! HTTP code: {query_resp.status_code}")
            print(query_resp.text)
            return

        query_data = query_resp.json()
        output = query_data.get("output")
        if output and "task_status" in output:
            status = output["task_status"]
            print(f"当前任务状态: {status}")

            if status.upper() in ("SUCCEEDED", "FAILED", "UNKNOWN"):
                finished = True
                print("任务完成，最终结果如下：")
                print(json.dumps(query_data, indent=2, ensure_ascii=False))
        else:
            print("查询返回内容:", query_data)


if __name__ == "__main__":
    main()
```

## Java SDK

```
import com.alibaba.dashscope.audio.qwen_asr.*;
import com.alibaba.dashscope.utils.Constants;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;

public class Main {
    public static void main(String[] args) {
        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        QwenTranscriptionParam param =
                QwenTranscriptionParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model("qwen3-asr-flash-filetrans")
                        .fileUrl("https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_example_1.wav")
                        //.parameter("language", "zh")
                        //.parameter("channel_id", new ArrayList<String>(){{add("0");add("1");}})
                        .parameter("enable_itn", false)
                        .parameter("enable_words", true)
                        .build();
        try {
            QwenTranscription transcription = new QwenTranscription();
            // 提交任务
            QwenTranscriptionResult result = transcription.asyncCall(param);
            System.out.println("create task result: " + result);
            // 查询任务状态
            result = transcription.fetch(QwenTranscriptionQueryParam.FromTranscriptionParam(param, result.getTaskId()));
            System.out.println("task status: " + result);
            // 等待任务完成
            result =
                    transcription.wait(
                            QwenTranscriptionQueryParam.FromTranscriptionParam(param, result.getTaskId()));
            System.out.println("task result: " + result);
            // 获取语音识别结果
            QwenTranscriptionTaskResult taskResult = result.getResult();
            if (taskResult != null) {
                // 获取识别结果的url
                String transcriptionUrl = taskResult.getTranscriptionUrl();
                // 获取url内对应的结果
                HttpURLConnection connection =
                        (HttpURLConnection) new URL(transcriptionUrl).openConnection();
                connection.setRequestMethod("GET");
                connection.connect();
                BufferedReader reader =
                        new BufferedReader(new InputStreamReader(connection.getInputStream()));
                // 格式化输出json结果
                Gson gson = new GsonBuilder().setPrettyPrinting().create();
                System.out.println(gson.toJson(gson.fromJson(reader, JsonObject.class)));
            }
        } catch (Exception e) {
            System.out.println("error: " + e);
        }
    }
}
```

## Python SDK

```
import json
import os
import sys
from http import HTTPStatus

import dashscope
from dashscope.audio.qwen_asr import QwenTranscription
from dashscope.api_entities.dashscope_response import TranscriptionResponse


# run the transcription script
if __name__ == '__main__':
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

    # 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
    task_response = QwenTranscription.async_call(
        model='qwen3-asr-flash-filetrans',
        file_url='https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_example_1.wav',
        #language="",
        enable_itn=False,
        enable_words=True
    )
    print(f'task_response: {task_response}')
    print(task_response.output.task_id)
    query_response = QwenTranscription.fetch(task=task_response.output.task_id)
    print(f'query_response: {query_response}')
    task_result = QwenTranscription.wait(task=task_response.output.task_id)
    print(f'task_result: {task_result}')
```

## 千问3-ASR-Flash

千问3-ASR-Flash模型支持最长5分钟录音。该模型可输入公网可访问的音频文件URL或直接上传本地文件。此外，它可流式返回识别结果。

## 输入内容：音频文件URL

## Python SDK

```
import os
import dashscope

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1，若使用美国地域的模型，需将url替换为：https://dashscope-us.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

messages = [
    {"role": "user", "content": [{"audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"}]}
]

response = dashscope.MultiModalConversation.call(
    # 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 若使用美国地域的模型，需在模型后面加上“-us”后缀，例如qwen3-asr-flash-us
    model="qwen3-asr-flash",
    messages=messages,
    result_format="message",
    asr_options={
        # "language": "zh", # 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
        "enable_itn":False
    }
)
print(response)
```

## Java SDK

```
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("audio", "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3")))
                .build();

        MultiModalMessage sysMessage = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                .build();

        Map<String, Object> asrOptions = new HashMap<>();
        asrOptions.put("enable_itn", false);
        // asrOptions.put("language", "zh"); // 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 若使用美国地域的模型，需在模型后面加上“-us”后缀，例如qwen3-asr-flash-us
                .model("qwen3-asr-flash")
                .message(sysMessage)
                .message(userMessage)
                .parameter("asr_options", asrOptions)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(JsonUtils.toJson(result));
    }
    public static void main(String[] args) {
        try {
            // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1，若使用美国地域的模型，需将url替换为：https://dashscope-us.aliyuncs.com/api/v1
            Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## cURL

```
# ======= 重要提示 =======
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation，若使用美国地域的模型，需将url替换为：https://dashscope-us.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若使用美国地域的模型，需要加us后缀
# === 执行时请删除该注释 ===

curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3-asr-flash",
    "input": {
        "messages": [
            {
                "content": [
                    {
                        "text": ""
                    }
                ],
                "role": "system"
            },
            {
                "content": [
                    {
                        "audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                    }
                ],
                "role": "user"
            }
        ]
    },
    "parameters": {
        "asr_options": {
            "enable_itn": false
        }
    }
}'
```

## 输入内容：Base64编码的音频文件

可输入Base64编码数据（[Data URL](https://www.rfc-editor.org/rfc/rfc2397)），格式为：`data:<mediatype>;base64,<data>`。

-   `<mediatype>`：MIME类型
    
    因音频格式而异，例如：
    
    -   WAV：`audio/wav`
        
    -   MP3：`audio/mpeg`
        
-   `<data>`：音频转成的Base64编码的字符串
    
    Base64编码会增大体积，请控制原文件大小，确保编码后仍符合输入音频大小限制（10MB）
    
-   示例：`data:audio/wav;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//PAxABQ/BXRbMPe4IQAhl9`
    
    **点击查看示例代码**
    
    Python
    
    ```
    import base64, pathlib
    
    # input.mp3为用于声音复刻的本地音频文件，请替换为自己的音频文件路径，确保其符合音频要求
    file_path = pathlib.Path("input.mp3")
    base64_str = base64.b64encode(file_path.read_bytes()).decode()
    data_uri = f"data:audio/mpeg;base64,{base64_str}"
    ```
    
    Java
    
    ```
    import java.nio.file.*;
    import java.util.Base64;
    
    public class Main {
        /**
         * filePath为用于声音复刻的本地音频文件，请替换为自己的音频文件路径，确保其符合音频要求
         */
        public static String toDataUrl(String filePath) throws Exception {
            byte[] bytes = Files.readAllBytes(Paths.get(filePath));
            String encoded = Base64.getEncoder().encodeToString(bytes);
            return "data:audio/mpeg;base64," + encoded;
        }
    
        // 使用示例
        public static void main(String[] args) throws Exception {
            System.out.println(toDataUrl("input.mp3"));
        }
    }
    ```
    

## Python SDK

示例中用到的音频文件为：[welcome.mp3](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260105/wotsae/welcome.mp3)。

```
import base64
import dashscope
import os
import pathlib

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1，若使用美国地域的模型，需将url替换为：https://dashscope-us.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# 请替换为实际的音频文件路径
file_path = "welcome.mp3"
# 请替换为实际的音频文件MIME类型
audio_mime_type = "audio/mpeg"

file_path_obj = pathlib.Path(file_path)
if not file_path_obj.exists():
    raise FileNotFoundError(f"音频文件不存在: {file_path}")

base64_str = base64.b64encode(file_path_obj.read_bytes()).decode()
data_uri = f"data:{audio_mime_type};base64,{base64_str}"

messages = [
    {"role": "user", "content": [{"audio": data_uri}]}
]
response = dashscope.MultiModalConversation.call(
    # 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 若使用美国地域的模型，需在模型后面加上“-us”后缀，例如qwen3-asr-flash-us
    model="qwen3-asr-flash",
    messages=messages,
    result_format="message",
    asr_options={
        # "language": "zh", # 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
        "enable_itn":False
    }
)
print(response)
```

## Java SDK

示例中用到的音频文件为：[welcome.mp3](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260105/wotsae/welcome.mp3)。

```
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    // 请替换为实际的音频文件路径
    private static final String AUDIO_FILE = "welcome.mp3";
    // 请替换为实际的音频文件MIME类型
    private static final String AUDIO_MIME_TYPE = "audio/mpeg";

    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException, IOException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("audio", toDataUrl())))
                .build();

        MultiModalMessage sysMessage = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                .build();

        Map<String, Object> asrOptions = new HashMap<>();
        asrOptions.put("enable_itn", false);
        // asrOptions.put("language", "zh"); // 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 若使用美国地域的模型，需在模型后面加上“-us”后缀，例如qwen3-asr-flash-us
                .model("qwen3-asr-flash")
                .message(sysMessage)
                .message(userMessage)
                .parameter("asr_options", asrOptions)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1，若使用美国地域的模型，需将url替换为：https://dashscope-us.aliyuncs.com/api/v1
            Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }

    // 生成 data URI
    public static String toDataUrl() throws IOException {
        byte[] bytes = Files.readAllBytes(Paths.get(AUDIO_FILE));
        String encoded = Base64.getEncoder().encodeToString(bytes);
        return "data:" + AUDIO_MIME_TYPE + ";base64," + encoded;
    }
}
```

## 输入内容：本地音频文件绝对路径

使用DashScope SDK处理本地图像文件时，需要传入文件路径。请您参考下表，结合您的使用方式与操作系统进行文件路径的创建。

| **系统** | **SDK** | **传入的文件路径** | **示例** |
| --- | --- | --- | --- |
| Linux或macOS系统 | Python SDK | file://{文件的绝对路径} | file:///home/images/test.png |
| Java SDK |
| Windows系统 | Python SDK | file://{文件的绝对路径} | file://D:/images/test.png |
| Java SDK | file:///{文件的绝对路径} | file:///D:images/test.png |

**重要**

使用本地文件时，接口调用上限为 100 QPS，且不支持扩容，请勿用于生产环境、高并发及压测场景；如需更高并发，建议将文件上传至 OSS 并通过录音文件 URL 方式调用。

## Python SDK

示例中用到的音频文件为：[welcome.mp3](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260105/wotsae/welcome.mp3)。

```
import os
import dashscope

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1，若使用美国地域的模型，需将url替换为：https://dashscope-us.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# 请用您的本地音频的绝对路径替换 ABSOLUTE_PATH/welcome.mp3
audio_file_path = "file://ABSOLUTE_PATH/welcome.mp3"

messages = [
    {"role": "user", "content": [{"audio": audio_file_path}]}
]
response = dashscope.MultiModalConversation.call(
    # 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 若使用美国地域的模型，需在模型后面加上“-us”后缀，例如qwen3-asr-flash-us
    model="qwen3-asr-flash",
    messages=messages,
    result_format="message",
    asr_options={
        # "language": "zh", # 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
        "enable_itn":False
    }
)
print(response)
```

## Java SDK

示例中用到的音频文件为：[welcome.mp3](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260105/wotsae/welcome.mp3)。

```
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        // 请用您本地文件的绝对路径替换掉ABSOLUTE_PATH/welcome.mp3
        String localFilePath = "file://ABSOLUTE_PATH/welcome.mp3";
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("audio", localFilePath)))
                .build();

        MultiModalMessage sysMessage = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                .build();

        Map<String, Object> asrOptions = new HashMap<>();
        asrOptions.put("enable_itn", false);
        // asrOptions.put("language", "zh"); // 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 若使用美国地域的模型，需在模型后面加上“-us”后缀，例如qwen3-asr-flash-us
                .model("qwen3-asr-flash")
                .message(sysMessage)
                .message(userMessage)
                .parameter("asr_options", asrOptions)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(JsonUtils.toJson(result));
    }
    public static void main(String[] args) {
        try {
            // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1，若使用美国地域的模型，需将url替换为：https://dashscope-us.aliyuncs.com/api/v1
            Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## 流式输出

模型并不是一次性生成最终结果，而是逐步地生成中间结果，最终结果由中间结果拼接而成。使用非流式输出方式需要等待模型生成结束后再将生成的中间结果拼接后返回，而流式输出可以实时地将中间结果返回，您可以在模型进行输出的同时进行阅读，减少等待模型回复的时间。您可以根据调用方式来设置不同的参数以实现流式输出：

-   DashScope Python SDK方式：设置`stream`参数为true。
    
-   DashScope Java SDK方式：需要通过`streamCall`接口调用。
    
-   DashScope HTTP方式：需要在Header中指定`X-DashScope-SSE`为`enable`。
    

## Python SDK

```
import os
import dashscope

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1，若使用美国地域的模型，需将url替换为：https://dashscope-us.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

messages = [
    {"role": "user", "content": [{"audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"}]}
]
response = dashscope.MultiModalConversation.call(
    # 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 若使用美国地域的模型，需在模型后面加上“-us”后缀，例如qwen3-asr-flash-us
    model="qwen3-asr-flash",
    messages=messages,
    result_format="message",
    asr_options={
        # "language": "zh", # 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
        "enable_itn":False
    },
    stream=True
)

for response in response:
    try:
        print(response["output"]["choices"][0]["message"].content[0]["text"])
    except:
        pass
```

## Java SDK

```
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;

public class Main {
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("audio", "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3")))
                .build();

        MultiModalMessage sysMessage = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                .build();

        Map<String, Object> asrOptions = new HashMap<>();
        asrOptions.put("enable_itn", false);
        // asrOptions.put("language", "zh"); // 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 若使用美国地域的模型，需在模型后面加上“-us”后缀，例如qwen3-asr-flash-us
                .model("qwen3-asr-flash")
                .message(sysMessage)
                .message(userMessage)
                .parameter("asr_options", asrOptions)
                .build();
        Flowable<MultiModalConversationResult> resultFlowable = conv.streamCall(param);
        resultFlowable.blockingForEach(item -> {
            try {
                System.out.println(item.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
            } catch (Exception e){
                System.exit(0);
            }
        });
    }

    public static void main(String[] args) {
        try {
            // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1，若使用美国地域的模型，需将url替换为：https://dashscope-us.aliyuncs.com/api/v1
            Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## cURL

```
# ======= 重要提示 =======
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation，若使用美国地域的模型，需将url替换为：https://dashscope-us.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若使用美国地域的模型，需要加us后缀
# === 执行时请删除该注释 ===

curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen3-asr-flash",
    "input": {
        "messages": [
            {
                "content": [
                    {
                        "text": ""
                    }
                ],
                "role": "system"
            },
            {
                "content": [
                    {
                        "audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                    }
                ],
                "role": "user"
            }
        ]
    },
    "parameters": {
        "incremental_output": true,
        "asr_options": {
            "enable_itn": false
        }
    }
}'
```

**千问Audio ASR**

千问Audio ASR模型为Beta版本，功能有限，且不保证服务稳定，仅供体验。生产环境请务必使用千问3-ASR-Flash-Filetrans或千问3-ASR-Flash。

## 输入内容：音频文件URL

## Python SDK

```
import dashscope

messages = [{"role": "user","content": [{"audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"}]}]
response = dashscope.MultiModalConversation.call(
    model="qwen-audio-asr",
    messages=messages,
    result_format="message")
print(response)
```

## Java SDK

```
import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;
public class Main {
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("audio", "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3")))
                .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .model("qwen-audio-asr")
                .message(userMessage)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(JsonUtils.toJson(result));
    }
    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## cURL

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-audio-asr",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"}
                ]
            }
        ]
    }
}'
```

## 输入内容：本地音频文件绝对路径

使用DashScope SDK处理本地图像文件时，需要传入文件路径。请您参考下表，结合您的使用方式与操作系统进行文件路径的创建。

| **系统** | **SDK** | **传入的文件路径** | **示例** |
| --- | --- | --- | --- |
| Linux或macOS系统 | Python SDK | file://{文件的绝对路径} | file:///home/images/test.png |
| Java SDK |
| Windows系统 | Python SDK | file://{文件的绝对路径} | file://D:/images/test.png |
| Java SDK | file:///{文件的绝对路径} | file:///D:images/test.png |

**重要**

使用本地文件时，接口调用上限为 100 QPS，且不支持扩容，请勿用于生产环境、高并发及压测场景；如需更高并发，建议将文件上传至 OSS 并通过录音文件 URL 方式调用。

## Python SDK

```
from dashscope import MultiModalConversation

# 请用您的本地音频的绝对路径替换 ABSOLUTE_PATH/welcome.mp3
audio_file_path = "file://ABSOLUTE_PATH/welcome.mp3"
messages = [{"role": "user","content": [{"audio": audio_file_path}]}]

response = MultiModalConversation.call(model="qwen-audio-asr", messages=messages)
print(response)
```

## Java SDK

```
import java.util.Arrays;
import java.util.HashMap;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    public static void callWithLocalFile()
            throws ApiException, NoApiKeyException, UploadFileException {
        // 请用您本地文件的绝对路径替换掉ABSOLUTE_PATH/welcome.mp3
        String localFilePath = "file://ABSOLUTE_PATH/welcome.mp3";
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(new HashMap<String, Object>(){{put("audio", localFilePath);}}
                ))
                .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .model("qwen-audio-asr")
                .message(userMessage)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(JsonUtils.toJson(result));
    }
    public static void main(String[] args) {
        try {
            callWithLocalFile();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## 流式输出

模型并不是一次性生成最终结果，而是逐步地生成中间结果，最终结果由中间结果拼接而成。使用非流式输出方式需要等待模型生成结束后再将生成的中间结果拼接后返回，而流式输出可以实时地将中间结果返回，您可以在模型进行输出的同时进行阅读，减少等待模型回复的时间。您可以根据调用方式来设置不同的参数以实现流式输出：

-   DashScope Python SDK方式：设置`stream`参数为true。
    
-   DashScope Java SDK方式：需要通过`streamCall`接口调用。
    
-   DashScope HTTP方式：需要在Header中指定`X-DashScope-SSE`为`enable`。
    

## Python SDK

```
import dashscope

messages = [{"role": "user","content": [{"audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"}]}]

response = dashscope.MultiModalConversation.call(
    model="qwen-audio-asr",
    messages=messages,
    result_format="message",
    stream=True
    )
full_content = ""
print("流式输出内容为：")
for response in response:
    try:
        print(response["output"]["choices"][0]["message"].content[0]["text"])
        full_content += response["output"]["choices"][0]["message"].content[0]["text"]
    except:
        pass
print(f"完整内容为：{full_content}")
```

## Java SDK

```
import java.util.Arrays;
import java.util.HashMap;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import io.reactivex.Flowable;

public class Main {
    public static void streamCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        // must create mutable map.
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(new HashMap<String, Object>(){{put("audio", "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3");}}
                )).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .model("qwen-audio-asr")
                .message(userMessage)
                .incrementalOutput(true)
                .build();
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(item -> {
            try {
                System.out.println(item.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
            } catch (Exception e){
                System.exit(0);
            }
        });
    }

    public static void main(String[] args) {
        try {
            streamCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## cURL

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen-audio-asr",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"}
                ]
            }
        ]
    },
    "parameters": {
      "incremental_output": true
    }
}'
```

## OpenAI兼容

仅千问3-ASR-Flash系列模型支持OpenAI兼容方式调用。OpenAI兼容方式仅允许输入公网可访问的音频文件URL，不支持输入本地音频文件绝对路径。

OpenAI Python SDK 版本应不低于1.52.0， Node.js SDK 版本应不低于 4.68.0。

`asr_options`非OpenAI标准参数，若使用OpenAI SDK，请通过`extra_body`传入。

## 输入内容：音频文件URL

## Python SDK

```
from openai import OpenAI
import os

try:
    client = OpenAI(
        # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    

    stream_enabled = False  # 是否开启流式输出
    completion = client.chat.completions.create(
        model="qwen3-asr-flash",
        messages=[
            {
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                        }
                    }
                ],
                "role": "user"
            }
        ],
        stream=stream_enabled,
        # stream设为False时，不能设置stream_options参数
        # stream_options={"include_usage": True},
        extra_body={
            "asr_options": {
                # "language": "zh",
                "enable_itn": False
            }
        }
    )
    if stream_enabled:
        full_content = ""
        print("流式输出内容为：")
        for chunk in completion:
            # 如果stream_options.include_usage为True，则最后一个chunk的choices字段为空列表，需要跳过（可以通过chunk.usage获取 Token 使用量）
            print(chunk)
            if chunk.choices and chunk.choices[0].delta.content:
                full_content += chunk.choices[0].delta.content
        print(f"完整内容为：{full_content}")
    else:
        print(f"非流式输出内容为：{completion.choices[0].message.content}")
except Exception as e:
    print(f"错误信息：{e}")
```

## Node.js SDK

```
// 运行前的准备工作:
// Windows/Mac/Linux 通用:
// 1. 确保已安装 Node.js (建议版本 >= 14)
// 2. 运行以下命令安装必要的依赖: npm install openai

import OpenAI from "openai";

const client = new OpenAI({
  // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
  // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
  apiKey: process.env.DASHSCOPE_API_KEY,
  // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
  baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1", 
});

async function main() {
  try {
    const streamEnabled = false; // 是否开启流式输出
    const completion = await client.chat.completions.create({
      model: "qwen3-asr-flash",
      messages: [
        {
          role: "user",
          content: [
            {
              type: "input_audio",
              input_audio: {
                data: "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
              }
            }
          ]
        }
      ],
      stream: streamEnabled,
      // stream设为False时，不能设置stream_options参数
      // stream_options: {
      //   "include_usage": true
      // },
      extra_body: {
        asr_options: {
          // language: "zh",
          enable_itn: false
        }
      }
    });

    if (streamEnabled) {
      let fullContent = "";
      console.log("流式输出内容为：");
      for await (const chunk of completion) {
        console.log(JSON.stringify(chunk));
        if (chunk.choices && chunk.choices.length > 0) {
          const delta = chunk.choices[0].delta;
          if (delta && delta.content) {
            fullContent += delta.content;
          }
        }
      }
      console.log(`完整内容为：${fullContent}`);
    } else {
      console.log(`非流式输出内容为：${completion.choices[0].message.content}`);
    }
  } catch (err) {
    console.error(`错误信息：${err}`);
  }
}

main();
```

## cURL

```
# ======= 重要提示 =======
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# === 执行时请删除该注释 ===

curl -X POST 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3-asr-flash",
    "messages": [
        {
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                    }
                }
            ],
            "role": "user"
        }
    ],
    "stream":false,
    "asr_options": {
        "enable_itn": false
    }
}'
```

## 输入内容：Base64编码的音频文件

可输入Base64编码数据（[Data URL](https://www.rfc-editor.org/rfc/rfc2397)），格式为：`data:<mediatype>;base64,<data>`。

-   `<mediatype>`：MIME类型
    
    因音频格式而异，例如：
    
    -   WAV：`audio/wav`
        
    -   MP3：`audio/mpeg`
        
-   `<data>`：音频转成的Base64编码的字符串
    
    Base64编码会增大体积，请控制原文件大小，确保编码后仍符合输入音频大小限制（10MB）
    
-   示例：`data:audio/wav;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//PAxABQ/BXRbMPe4IQAhl9`
    
    **点击查看示例代码**
    
    Python
    
    ```
    import base64, pathlib
    
    # input.mp3为用于声音复刻的本地音频文件，请替换为自己的音频文件路径，确保其符合音频要求
    file_path = pathlib.Path("input.mp3")
    base64_str = base64.b64encode(file_path.read_bytes()).decode()
    data_uri = f"data:audio/mpeg;base64,{base64_str}"
    ```
    
    Java
    
    ```
    import java.nio.file.*;
    import java.util.Base64;
    
    public class Main {
        /**
         * filePath为用于声音复刻的本地音频文件，请替换为自己的音频文件路径，确保其符合音频要求
         */
        public static String toDataUrl(String filePath) throws Exception {
            byte[] bytes = Files.readAllBytes(Paths.get(filePath));
            String encoded = Base64.getEncoder().encodeToString(bytes);
            return "data:audio/mpeg;base64," + encoded;
        }
    
        // 使用示例
        public static void main(String[] args) throws Exception {
            System.out.println(toDataUrl("input.mp3"));
        }
    }
    ```
    

## Python SDK

示例中用到的音频文件为：[welcome.mp3](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260105/wotsae/welcome.mp3)。

```
import base64
from openai import OpenAI
import os
import pathlib

try:
    # 请替换为实际的音频文件路径
    file_path = "welcome.mp3"
    # 请替换为实际的音频文件MIME类型
    audio_mime_type = "audio/mpeg"

    file_path_obj = pathlib.Path(file_path)
    if not file_path_obj.exists():
        raise FileNotFoundError(f"音频文件不存在: {file_path}")

    base64_str = base64.b64encode(file_path_obj.read_bytes()).decode()
    data_uri = f"data:{audio_mime_type};base64,{base64_str}"

    client = OpenAI(
        # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    

    stream_enabled = False  # 是否开启流式输出
    completion = client.chat.completions.create(
        model="qwen3-asr-flash",
        messages=[
            {
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": data_uri
                        }
                    }
                ],
                "role": "user"
            }
        ],
        stream=stream_enabled,
        # stream设为False时，不能设置stream_options参数
        # stream_options={"include_usage": True},
        extra_body={
            "asr_options": {
                # "language": "zh",
                "enable_itn": False
            }
        }
    )
    if stream_enabled:
        full_content = ""
        print("流式输出内容为：")
        for chunk in completion:
            # 如果stream_options.include_usage为True，则最后一个chunk的choices字段为空列表，需要跳过（可以通过chunk.usage获取 Token 使用量）
            print(chunk)
            if chunk.choices and chunk.choices[0].delta.content:
                full_content += chunk.choices[0].delta.content
        print(f"完整内容为：{full_content}")
    else:
        print(f"非流式输出内容为：{completion.choices[0].message.content}")
except Exception as e:
    print(f"错误信息：{e}")
```

## Node.js SDK

示例中用到的音频文件为：[welcome.mp3](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260105/wotsae/welcome.mp3)。

```
// 运行前的准备工作:
// Windows/Mac/Linux 通用:
// 1. 确保已安装 Node.js (建议版本 >= 14)
// 2. 运行以下命令安装必要的依赖: npm install openai

import OpenAI from "openai";
import { readFileSync } from 'fs';

const client = new OpenAI({
  // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
  // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
  apiKey: process.env.DASHSCOPE_API_KEY,
  // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
  baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1", 
});

const encodeAudioFile = (audioFilePath) => {
    const audioFile = readFileSync(audioFilePath);
    return audioFile.toString('base64');
};

// 请替换为实际的音频文件路径
const dataUri = `data:audio/mpeg;base64,${encodeAudioFile("welcome.mp3")}`;

async function main() {
  try {
    const streamEnabled = false; // 是否开启流式输出
    const completion = await client.chat.completions.create({
      model: "qwen3-asr-flash",
      messages: [
        {
          role: "user",
          content: [
            {
              type: "input_audio",
              input_audio: {
                data: dataUri
              }
            }
          ]
        }
      ],
      stream: streamEnabled,
      // stream设为False时，不能设置stream_options参数
      // stream_options: {
      //   "include_usage": true
      // },
      extra_body: {
        asr_options: {
          // language: "zh",
          enable_itn: false
        }
      }
    });

    if (streamEnabled) {
      let fullContent = "";
      console.log("流式输出内容为：");
      for await (const chunk of completion) {
        console.log(JSON.stringify(chunk));
        if (chunk.choices && chunk.choices.length > 0) {
          const delta = chunk.choices[0].delta;
          if (delta && delta.content) {
            fullContent += delta.content;
          }
        }
      }
      console.log(`完整内容为：${fullContent}`);
    } else {
      console.log(`非流式输出内容为：${completion.choices[0].message.content}`);
    }
  } catch (err) {
    console.error(`错误信息：${err}`);
  }
}

main();
```

## **API参考**

[录音文件识别-千问API参考](https://help.aliyun.com/zh/model-studio/qwen-asr-api-reference)

## **模型应用上架及备案**

参见[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)。

## **模型功能特性对比**

下表中qwen3-asr-flash和qwen3-asr-flash-2025-09-08模型的功能特性同样适用于美国（弗吉尼亚）地域对应的qwen3-asr-flash-us和qwen3-asr-flash-2025-09-08-us模型。

| **功能/特性** | **qwen3-asr-flash-filetrans、qwen3-asr-flash-filetrans-2025-11-17** | **qwen3-asr-flash、qwen3-asr-flash-2026-02-10、qwen3-asr-flash-2025-09-08** | **qwen-audio-asr** |
| --- | --- | --- | --- |
| **支持语言** | 中文（普通话、四川话、闽南语、吴语、粤语）、英语、日语、德语、韩语、俄语、法语、葡萄牙语、阿拉伯语、意大利语、西班牙语、印地语、印尼语、泰语、土耳其语、乌克兰语、越南语、捷克语、丹麦语、菲律宾语、芬兰语、冰岛语、马来语、挪威语、波兰语、瑞典语 |   | 中文、英文 |
| **支持的音频格式** | aac、amr、avi、flac、flv、m4a、mkv、mov、mp3、mp4、mpeg、ogg、opus、wav、webm、wma、wmv | aac、amr、avi、aiff、flac、flv、mkv、mp3、mpeg、ogg、opus、wav、webm、wma、wmv | aac、amr、avi、aiff、flac、flv、m4a、mkv、mp3、mpeg、ogg、opus、wav、webm、wma、wmv |
| **采样率** | 因音频格式而异： - pcm格式音频：16kHz - 其他格式音频：任意（服务端会先将音频重采样为 16 kHz，再进行识别） |   | 16kHz |
| **声道** | 任意 不同模型在处理多声道音频时方式存在差异： - 千问3-ASR-Flash-Filetrans：需通过`channel_id`参数指定音轨索引 - 千问3-ASR-Flash：无需额外处理，模型会对多声道音频做均值合并后再处理 |   | 单声道 |
| **输入形式** | 公网可访问的待识别文件URL | Base64编码的文件、本地文件绝对路径、公网可访问的待识别文件URL | 本地文件绝对路径、公网可访问的待识别文件URL |
| **音频大小/时长** | 音频文件大小不超过2GB，且时长不超过12小时 | 音频文件大小不超过10MB，且时长不超过5分钟 | 音频文件大小不超过10MB，且时长不超过3分钟 |
| **情感识别** | 支持 固定开启，可通过响应参数`emotion`查看结果 |   | 不支持 |
| **时间戳** | 支持 固定开启，可通过请求参数`enable_words`控制时间戳级别 > 字级别时间戳仅支持以下语种：中文、英语、日语、韩语、德语、法语、西班牙语、意大利语、葡萄牙语、俄语，其他语种可能无法保证准确性 | 不支持 |   |
| **标点符号预测** | 支持 固定开启 |   | 不支持 |
| **ITN** | 支持 默认关闭，可开启，仅适用于中、英文 |   | 不支持 |
| **歌唱识别** | 支持 固定开启 |   | 不支持 |
| **噪声拒识** | 支持 固定开启 |   | 不支持 |
| **敏感词过滤** | 不支持 |   |   |
| **说话人分离** | 不支持 |   |   |
| **语气词过滤** | 不支持 |   |   |
| **VAD** | 支持 固定开启 | 不支持 |   |
| **限流（RPM）** | 100 |   |   |
| **接入方式** | DashScope：Java/Python SDK、RESTful API | DashScope：Java/Python SDK、RESTful API OpenAI：Python/Node.js SDK、RESTful API | DashScope：Java/Python SDK、RESTful API |
| **价格** | 中国内地：0.00022元/秒 美国：0.000035元/秒 国际：0.00026元/秒 |   | 目前仅供免费体验 > 免费额度用完后不可调用，推荐使用 Qwen3 ASR |

## 常见问题

### **Q：如何为API提供公网可访问的音频URL？**

推荐使用[阿里云对象存储OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，它提供了高可用、高可靠的存储服务，并且可以方便地生成公网访问URL。

**在公网环境下验证生成的 URL 可正常访问：**可在浏览器或通过 curl 命令访问该 URL，确保音频文件能够成功下载或播放（HTTP状态码为200）。

### **Q：如何检查音频格式是否符合要求？**

可以使用开源工具[ffprobe](https://ffmpeg.org/ffprobe.html)快速获取音频的详细信息：

```
# 查询音频的容器格式(format_name)、编码(codec_name)、采样率(sample_rate)、声道数(channels)
ffprobe -v error -show_entries format=format_name -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 your_audio_file.mp3
```

### **Q：**如何处理音频以满足模型要求？

可以使用开源工具[FFmpeg](https://ffmpeg.en.lo4d.com/download)对音频进行裁剪或格式转换：

-   **音频裁剪：从长音频中截取片段**
    
    ```
    # -i: 输入文件
    # -ss 00:01:30: 设置裁剪的起始时间 (从1分30秒开始)
    # -t 00:02:00: 设置裁剪的持续时长 (裁剪2分钟)
    # -c copy: 直接复制音频流，不重新编码，速度快
    # output_clip.wav: 输出文件
    ffmpeg -i long_audio.wav -ss 00:01:30 -t 00:02:00 -c copy output_clip.wav
    ```
    
-   **格式转换**
    
    例如，将任意音频转换为16kHz、16-bit、单声道WAV文件
    
    ```
    # -i: 输入文件
    # -ac 1: 设置声道数为1 (单声道)
    # -ar 16000: 设置采样率为16000Hz (16kHz)
    # -sample_fmt s16: 设置采样格式为16-bit signed integer PCM
    # output.wav: 输出文件
    ffmpeg -i input.mp3 -ac 1 -ar 16000 -sample_fmt s16 output.wav
    ```
