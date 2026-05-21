阿里云百炼支持通过API调用大模型，涵盖OpenAI兼容接口、DashScope SDK等接入方式。

**说明**

-   若您熟悉大模型调用，可直接查看API参考文档[千问](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)。
    
-   若您不熟悉编程，可参考[Chatbox](https://help.aliyun.com/zh/model-studio/chatbox)，通过图形化界面与千问模型对话。
    

本文以千问为例，引导您完成大模型API调用。您将了解到：

-   如何获取 API Key
    
-   如何配置本地开发环境
    
-   如何调用千问 API
    

## 账号设置

1.  **注册账号**：若无阿里云账号，需首先[注册](https://account.alibabacloud.com/register/intl_register.htm)。
    
    > 如遇问题，请参见[注册阿里云账号](https://help.aliyun.com/zh/account/step-1-register-an-alibaba-cloud-account)。
    
2.  **开通阿里云百炼：**使用**阿里云主账号**前往[阿里云百炼大模型服务平台](https://bailian.console.aliyun.com/?tab=model#/model-market)，阅读并同意协议后，将自动开通阿里云百炼，如果未弹出服务协议，则表示您已经开通。
    
    > 如果开通服务时提示“您尚未进行实名认证”，请先进行[实名认证](https://help.aliyun.com/zh/account/verify-your-identity-individual-account)。
    
3.  **获取API Key：**前往[密钥管理](https://bailian.console.aliyun.com/?tab=model#/api-key)页面，单击**创建API Key****，**即可通过API KEY调用大模型。
    

## **配置API Key到环境变量**

建议您把API Key配置到环境变量，避免在代码里显式地配置API Key，降低泄露风险。

**配置步骤**

### Linux系统

#### 添加永久性环境变量

如果您希望API Key环境变量在当前用户的所有新会话中生效，可以添加永久性环境变量。

1.  执行以下命令来将环境变量设置追加到`~/.bashrc` 文件中。
    
    ```
    # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
    echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.bashrc
    ```
    
    也可以手动修改`~/.bashrc` 文件。
    
    **手动修改**
    
    执行以下命令，打开`~/.bashrc` 文件。
    
    ```
    nano ~/.bashrc
    ```
    
    在配置文件中添加以下内容。
    
    ```
    # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
    export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
    ```
    
    在nano编辑器中，按Ctrl + X，接着按Y，再按Enter以保存并关闭文件。
    
2.  执行以下命令，使变更生效。
    
    ```
    source ~/.bashrc
    ```
    
3.  重新打开一个终端窗口，运行以下命令检查环境变量是否生效。
    
    ```
    echo $DASHSCOPE_API_KEY
    ```
    

#### 添加临时性环境变量

如果您仅希望在当前会话中使用该环境变量，可以添加临时性环境变量。

1.  执行以下命令。
    
    ```
    # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
    export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
    ```
    
2.  执行以下命令，验证该环境变量是否生效。
    
    ```
    echo $DASHSCOPE_API_KEY
    ```
    

### macOS系统

#### 添加永久性环境变量

如果您希望API Key环境变量在当前用户的所有新会话中生效，可以添加永久性环境变量。

1.  在终端中执行以下命令，查看默认Shell类型。
    
    ```
    echo $SHELL
    ```
    
2.  根据默认Shell类型进行操作。
    
    ##### **Zsh**
    
    1.  执行以下命令来将环境变量设置追加到 `~/.zshrc` 文件中。
        
        ```
        # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
        echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.zshrc
        ```
        
        也可以手动修改`~/.zshrc` 文件。
        
        **手动修改**
        
        执行以下命令，打开Shell配置文件。
        
        ```
        nano ~/.zshrc
        ```
        
        在配置文件中添加以下内容。
        
        ```
        # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
        export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
        ```
        
        在nano编辑器中，按Ctrl + X，接着按Y，再按Enter以保存并关闭文件。
        
    2.  执行以下命令，使变更生效。
        
        ```
        source ~/.zshrc
        ```
        
    3.  重新打开一个终端窗口，运行以下命令检查环境变量是否生效。
        
        ```
        echo $DASHSCOPE_API_KEY
        ```
        
    
    ##### **Bash**
    
    1.  执行以下命令来将环境变量设置追加到 `~/.bash_profile` 文件中。
        
        ```
        # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
        echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.bash_profile
        ```
        
        也可以手动修改`~/.bash_profile` 文件。
        
        **手动修改**
        
        执行以下命令，打开Shell配置文件。
        
        ```
        nano ~/.bash_profile
        ```
        
        在配置文件中添加以下内容。
        
        ```
        # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
        export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
        ```
        
        在nano编辑器中，按Ctrl + X，接着按Y，再按Enter以保存并关闭文件。
        
    2.  执行以下命令，使变更生效。
        
        ```
        source ~/.bash_profile
        ```
        
    3.  重新打开一个终端窗口，运行以下命令检查环境变量是否生效。
        
        ```
        echo $DASHSCOPE_API_KEY
        ```
        
    

#### 添加临时性环境变量

如果您仅希望在当前会话中使用该环境变量，可以添加临时性环境变量。

> 以下命令适用于 Zsh 和 Bash。

1.  执行以下命令。
    
    ```
    # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
    export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
    ```
    
2.  执行以下命令，验证该环境变量是否生效。
    
    ```
    echo $DASHSCOPE_API_KEY
    ```
    

### Windows系统

在Windows系统中，您可以通过系统属性、CMD或PowerShell配置环境变量。

#### **系统属性**

**说明**

-   此方式配置的环境变量永久生效。
    
-   修改系统环境变量需具备管理员权限。
    
-   配置环境变量后不会立即影响已经打开的命令窗口、IDE或其他正在运行的应用程序。您需要重新启动这些程序或者打开新的命令行使环境变量生效。
    

1.  在Windows系统桌面中按`Win+Q`键，在搜索框中搜索**编辑系统环境变量**，单击打开**系统属性**界面。
    
2.  在**系统属性**窗口，单击**环境变量**，然后在**系统变量**区域下单击**新建**，**变量名**填入`DASHSCOPE_API_KEY`，**变量值**填入您的DashScope API Key。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8252115371/p894015.png)
    
3.  依次单击三个窗口的**确定**，关闭系统属性配置页面，完成环境变量配置。
    
4.  打开CMD（命令提示符）窗口或Windows PowerShell窗口，执行如下命令检查环境变量是否生效。
    
    -   CMD查询命令：
        
        ```
        echo %DASHSCOPE_API_KEY%
        ```
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1317988371/p912522.png)
        
    -   Windows PowerShell查询命令：
        
        ```
        echo $env:DASHSCOPE_API_KEY
        ```
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1317988371/p912525.png)
        

#### **CMD**

##### **添加永久性环境变量**

如果您希望API Key环境变量在当前用户的所有新会话中生效，可以按如下操作。

1.  在CMD中运行以下命令。
    
    ```
    # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
    setx DASHSCOPE_API_KEY "YOUR_DASHSCOPE_API_KEY"
    ```
    
2.  打开一个新的CMD窗口。
    
3.  在新的CMD窗口运行以下命令，检查环境变量是否生效。
    
    ```
    echo %DASHSCOPE_API_KEY%
    ```
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1317988371/p912522.png)
    

##### **添加临时性环境变量**

如果您仅希望在当前会话中使用该环境变量，可以在CMD中运行以下命令。

```
# 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
set DASHSCOPE_API_KEY=YOUR_DASHSCOPE_API_KEY
```

您可以在当前会话运行以下命令检查环境变量是否生效。

```
echo %DASHSCOPE_API_KEY%
```

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1317988371/p912522.png)

#### **PowerShell**

##### **添加永久性环境变量**

如果您希望API Key环境变量在当前用户的所有新会话中生效，可以按如下操作。

1.  在PowerShell中运行以下命令。
    
    ```
    # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
    [Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "YOUR_DASHSCOPE_API_KEY", [EnvironmentVariableTarget]::User)
    ```
    
2.  打开一个新的PowerShell窗口。
    
3.  在新的PowerShell窗口运行以下命令，检查环境变量是否生效。
    
    ```
    echo $env:DASHSCOPE_API_KEY
    ```
    
    ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    

##### 添加临时性环境变量

如果您仅希望在当前会话中使用该环境变量，可以在PowerShell中运行以下命令。

```
# 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
$env:DASHSCOPE_API_KEY = "YOUR_DASHSCOPE_API_KEY"
```

您可以在当前会话运行以下命令检查环境变量是否生效。

```
echo $env:DASHSCOPE_API_KEY
```

![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)

## **选择开发语言**

选择您熟悉的语言或工具，用于调用大模型API。

## Python

### **步骤 1：配置Python环境**

### **检查您的Python版本**

您可以在终端中输入以下命令查看当前计算环境是否安装了Python和pip：

您的Python需要为3.8或以上版本，请您参考[安装Python](https://help.aliyun.com/zh/sdk/developer-reference/installing-python)进行安装。

```
python -V
pip --version
```

以Windows的CMD为例：

![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)

#### **常见问题**

Q：执行`python -V`、`pip --version`报错：

-   `'python' 不是内部或外部命令，也不是可运行的程序或批处理文件。`
    
-   `'pip' 不是内部或外部命令，也不是可运行的程序或批处理文件。`
    
-   `-bash: python: command not found`
    
-   `-bash: pip: command not found`
    

解决办法如下：

##### **Windows系统**

1.  请确认是否已参考[安装Python](https://help.aliyun.com/zh/sdk/developer-reference/installing-python)，在您的计算环境中安装Python，并将python.exe添加至环境变量PATH中。![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    
2.  如果已安装了Python并添加了环境变量，仍报此错，请关闭当前终端，重新打开一个新的终端窗口，再进行尝试。
    

## Linux、macOS系统

1.  请确认是否已参考[安装Python](https://help.aliyun.com/zh/sdk/developer-reference/installing-python)，在您的计算环境中安装的Python。
    
2.  如果已安装Python后，仍报此错，请输入`which python pip`命令查询系统中是否有`python`、`pip`。
    
    -   如果返回如下结果，请关闭当前连接终端，重新打开一个新的终端窗口，再进行尝试。
        
        ```
        /usr/bin/python
        /usr/bin/pip
        ```
        
    -   如果返回如下结果，则再次输入`which python3 pip3`查询。
        
        ```
        /usr/bin/which: no python in (/root/.local/bin:/root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin)
        /usr/bin/which: no pip in (/root/.local/bin:/root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin)
        ```
        
        如果返回结果如下，则使用`python3 -V`、`pip3 --version`查询版本。
        
        ```
        /usr/bin/python3
        /usr/bin/pip3
        ```
        

### **配置虚拟环境（可选）**

如果您的Python已安装完成，可以创建一个虚拟环境来安装OpenAI Python SDK或DashScope Python SDK，这可以帮助您避免与其它项目发生依赖冲突。

1.  **创建虚拟环境**
    
    您可以运行以下命令，创建一个命名为**.venv**的虚拟环境：
    
    ```
    # 如果运行失败，您可以将python替换成python3再运行
    python -m venv .venv
    ```
    
2.  **激活虚拟环境**
    
    若您使用Windows系统，请运行以下命令来激活虚拟环境：
    
    ```
    .venv\Scripts\activate
    ```
    
    如果您使用macOS或者Linux系统，请运行以下命令来激活虚拟环境：
    
    ```
    source .venv/bin/activate
    ```
    

### **安装**OpenAI Python SDK或DashScope Python SDK

您可以通过OpenAI的Python SDK或DashScope的Python SDK来调用阿里云百炼平台上的模型。

## 安装 OpenAI Python SDK

通过运行以下命令安装或升级 OpenAI Python SDK：

```
# 如果运行失败，您可以将pip替换成pip3再运行
pip install -U openai
```

![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)

当终端出现`Successfully installed ... openai-x.x.x`的提示后，表示您已经成功安装OpenAI Python SDK。

## 安装 DashScope Python SDK

通过运行以下命令安装或升级 DashScope Python SDK：

```
# 如果运行失败，您可以将pip替换成pip3再运行
pip install -U dashscope
```

![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)

当终端出现`Successfully installed ... dashscope-x.x.x`的提示后，表示您已经成功安装DashScope Python SDK。

### **步骤 2：调用大模型API**

## OpenAI Python SDK

如果您安装完成了Python以及OpenAI的Python SDK，可以参考以下步骤发送您的API请求。

1.  新建一个文件，命名为`hello_qwen.py`。
    
2.  将以下代码复制到`hello_qwen.py`中并保存。
    
    ```
    import os
    from openai import OpenAI
    
    try:
        client = OpenAI(
            # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为: api_key="sk-xxx",
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
    
        completion = client.chat.completions.create(
            model="qwen-plus",  # 模型列表: https://help.aliyun.com/model-studio/getting-started/models
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': '你是谁？'}
            ]
        )
        print(completion.choices[0].message.content)
    except Exception as e:
        print(f"错误信息：{e}")
        print("请参考文档：https://help.aliyun.com/model-studio/developer-reference/error-code")
    ```
    
3.  通过命令行运行`python hello_qwen.py`或`python3 hello_qwen.py`。
    
    > 若提示`No such file or directory`，则需在文件名前指定具体文件路径。
    
    运行后您将会看到输出结果：
    
    ```
    我是阿里云开发的一款超大规模语言模型，我叫千问。
    ```
    
    ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    

## DashScope Python SDK

如果您安装完成了Python以及DashScope的Python SDK，可以参考以下步骤发送您的API请求。

1.  新建一个文件，命名为`hello_qwen.py`。
    
2.  将以下代码复制到`hello_qwen.py`中并保存。
    
    ```
    import os
    from dashscope import Generation
    import dashscope 
    
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}
    ]
    response = Generation.call(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"), 
        model="qwen-plus",   # 模型列表：https://help.aliyun.com/model-studio/getting-started/models
        messages=messages,
        result_format="message"
    )
    
    if response.status_code == 200:
        print(response.output.choices[0].message.content)
    else:
        print(f"HTTP返回码：{response.status_code}")
        print(f"错误码：{response.code}")
        print(f"错误信息：{response.message}")
        print("请参考文档：https://help.aliyun.com/model-studio/developer-reference/error-code")
    ```
    
3.  通过命令行运行`python hello_qwen.py`或`python3 hello_qwen.py`。
    
    **说明**
    
    本示例使用的运行命令需在Python文件所在目录执行，如果想要在任意位置执行，请在文件名前指定具体文件路径。
    
    运行后您将会看到输出结果：
    
    ```
    我是来自阿里云的大规模语言模型，我叫千问。
    ```
    
    ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    

## Node.js

### **步骤 1：配置Node.js环境**

### 检查Node.js安装状态

您可以在终端中输入以下命令查看当前计算环境是否安装了Node.js和npm：

```
node -v
npm -v
```

以Windows的CMD为例：

![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)

这将打印出您当前Node.js 版本。如果您的环境中没有Node.js，请访问[Node.js官网](https://nodejs.org/en/download/package-manager)进行下载。

### 安装模型调用SDK

您可以在终端运行以下命令：

```
npm install --save openai
# 或者
yarn add openai
```

**说明**

如果安装失败，您可以通过配置镜像源的方法来完成安装，如：

```
npm config set registry https://registry.npmmirror.com/
```

配置镜像源后，您可以重新运行安装SDK的命令。

![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)

当终端出现`added xx package in xxs`的提示后，表示您已经成功安装OpenAI SDK。您可以使用`npm list openai`查询具体版本信息。

### 步骤 2：调用大模型API

1.  新建一个`hello_qwen.mjs`文件。
    
2.  将以下代码复制到文件中。
    
    ```
    import OpenAI from "openai";
    
    try {
        const openai = new OpenAI(
            {
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为: apiKey: "sk-xxx",
                // 新加坡和北京地域的API Key不同。获取API Key: https://help.aliyun.com/model-studio/get-api-key
                apiKey: process.env.DASHSCOPE_API_KEY,
                // 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为: https://dashscope-intl.aliyuncs.com/compatible-mode/v1
                baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
            }
        );
        const completion = await openai.chat.completions.create({
            model: "qwen-plus",  //模型列表: https://help.aliyun.com/model-studio/getting-started/models
            messages: [
                { role: "system", content: "You are a helpful assistant." },
                { role: "user", content: "你是谁？" }
            ],
        });
        console.log(completion.choices[0].message.content);
    } catch (error) {
        console.log(`错误信息：${error}`);
        console.log("请参考文档：https://help.aliyun.com/model-studio/developer-reference/error-code");
    }
    ```
    
3.  通过命令行运行以下命令来发送API请求：
    
    ```
    node hello_qwen.mjs
    ```
    
    **说明**
    
    -   本示例使用的运行命令需在`hello_qwen.mjs`文件所在目录执行，如果想要在任意位置执行，请在文件名前指定具体文件路径。
        
    -   请确保已在`hello_qwen.mjs`文件所在目录中安装了SDK，如果SDK与文件不在同一目录下，则会报错`Cannot find package 'openai' imported from xxx`。
        
    
    运行成功后您将会看到输出结果：
    
    ```
    我是来自阿里云的语言模型，我叫千问。
    ```
    
    ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    

## Java

### **步骤 1：配置Java环境**

### **检查您的Java版本**

您可以在终端运行以下命令：

```
java -version
# （可选）如果使用maven管理和构建java项目，还需确保maven已正确安装到您的开发环境中
mvn --version
```

以Windows的CMD为例：

![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)

为了使用DashScope Java SDK，您的Java需要在Java 8或以上版本。您可以查看打印信息中的第一行确认Java版本，例如打印信息：`openjdk version "16.0.1" 2021-04-20`表明当前Java版本为Java 16。如果您当前计算环境没有Java，或版本低于Java 8，请前往[Java下载](https://www.oracle.com/cn/java/technologies/downloads/)进行下载与安装。

### **安装模型调用SDK**

如果您的环境中已安装Java，请安装DashScope Java SDK。SDK的版本请参考：[DashScope Java SDK](https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java)。执行以下命令来添加 Java SDK 依赖，并将 `the-latest-version` 替换为最新的版本号。

## XML

1.  打开您的Maven项目的`pom.xml`文件。
    
2.  在`<dependencies>`标签内添加以下依赖信息。
    
    ```
    <dependency>
        <groupId>com.alibaba</groupId>
        <artifactId>dashscope-sdk-java</artifactId>
        <!-- 请将 'the-latest-version' 替换为最新版本号：https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java -->
        <version>the-latest-version</version>
    </dependency>
    ```
    
3.  保存`pom.xml`文件。
    
4.  使用Maven命令（如`mvn compile`或`mvn clean install`）来更新项目依赖，这样Maven会自动下载并添加DashScope Java SDK到您的项目中。
    

以Windows的IDEA集成开发环境为例：

![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)

## Gradle

1.  打开您的Gradle项目的`build.gradle`文件。
    
2.  在`dependencies`块内添加以下依赖信息。
    
    ```
    dependencies {
        // 请将 'the-latest-version' 替换为最新版本号：https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
        implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: 'the-latest-version'
    }
    ```
    
3.  保存`build.gradle`文件。
    
4.  在命令行中，切换到您的项目根目录，执行以下Gradle命令来更新项目依赖。这将会自动下载并添加DashScope Java SDK到您的项目中。
    
    ```
    ./gradlew build --refresh-dependencies
    ```
    

以Windows的IDEA集成开发环境为例：

![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)

### **步骤 2：调用大模型API**

您可以运行以下代码来调用大模型API。

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
import com.alibaba.dashscope.utils.Constants;

public class Main {
    //  若使用新加坡地域的模型，请释放下列注释
    //  static {Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";}
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
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
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 模型列表：https://help.aliyun.com/model-studio/getting-started/models
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
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("错误信息："+e.getMessage());
            System.out.println("请参考文档：https://help.aliyun.com/model-studio/developer-reference/error-code");
        }
        System.exit(0);
    }
}
```

运行后您将会看到对应的输出结果：

```
我是阿里云开发的一款超大规模语言模型，我叫千问。
```

## curl

您可以通过OpenAI兼容的HTTP方式或DashScope的HTTP方式来调用阿里云百炼平台上的模型。模型列表请参考：[模型列表](https://help.aliyun.com/zh/model-studio/models)。

**说明**

若没有配置环境变量，请用阿里云百炼API Key将：-H "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\ 换为：-H "Authorization: Bearer sk-xxx" \\ 。

## OpenAI兼容-HTTP

您可以运行以下命令发送API请求：

**Windows**

在CMD（命令提示符）中执行如下命令：

```
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key: https://help.aliyun.com/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为: https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===
curl -X POST "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions" ^
-H "Authorization: Bearer %DASHSCOPE_API_KEY%" ^
-H "Content-Type: application/json" ^
-d "{
    \"model\": \"qwen-plus\",
    \"messages\": [
        {
            \"role\": \"system\",
            \"content\": \"You are a helpful assistant.\"
        },
        {
            \"role\": \"user\",
            \"content\": \"你是谁？\"
        }
    ]
}"
```

**Linux/macOS**

在Terminal（终端）中执行如下命令：

```
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key: https://help.aliyun.com/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为: https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
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

发送API请求后，可以得到以下回复：

```
{
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "我是来自阿里云的大规模语言模型，我叫千问。"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
        }
    ],
    "object": "chat.completion",
    "usage": {
        "prompt_tokens": 22,
        "completion_tokens": 16,
        "total_tokens": 38
    },
    "created": 1728353155,
    "system_fingerprint": null,
    "model": "qwen-plus",
    "id": "chatcmpl-39799876-eda8-9527-9e14-2214d641cf9a"
}
```

## DashScope-HTTP

您可以运行以下命令发送API请求：

**Windows**

在CMD（命令提示符）中执行如下命令：

```
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key: https://help.aliyun.com/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
# === 执行时请删除该注释 ===
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" ^
-H "Authorization: Bearer %DASHSCOPE_API_KEY%" ^
-H "Content-Type: application/json" ^
-d "{
  \"model\": \"qwen-plus\",
  \"input\": {
    \"messages\": [
      {
        \"role\": \"system\",
        \"content\": \"You are a helpful assistant.\"
      },
      {
        \"role\": \"user\",
        \"content\": \"你是谁？\"
      }
    ]
  },
  \"parameters\": {
    \"result_format\": \"message\"
  }
}"
```

**Linux/macOS**

在Terminal（终端）中执行如下命令：

```
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
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
                "content": "你是谁？"
            }
        ]
    },
    "parameters": {
        "result_format":"message"
    }
}'
```

发送API请求后，可以得到以下回复：

```
{
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": "我是来自阿里云的大规模语言模型，我叫千问。"
                }
            }
        ]
    },
    "usage": {
        "total_tokens": 38,
        "output_tokens": 16,
        "input_tokens": 22
    },
    "request_id": "87f776d7-3c82-9d39-b238-d1ad38c9b6a9"
}
```

## 其它语言

**调用大模型API**

Go

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

type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}
type RequestBody struct {
	Model    string    `json:"model"`
	Messages []Message `json:"messages"`
}

func main() {
	// 创建 HTTP 客户端
	client := &http.Client{}
	// 构建请求体
	requestBody := RequestBody{
		// 模型列表：https://help.aliyun.com/model-studio/getting-started/models
		Model: "qwen-plus",
		Messages: []Message{
			{
				Role:    "system",
				Content: "You are a helpful assistant.",
			},
			{
				Role:    "user",
				Content: "你是谁？",
			},
		},
	}
	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		log.Fatal(err)
	}
	// 创建 POST 请求
	// 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
	req, err := http.NewRequest("POST", "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions", bytes.NewBuffer(jsonData))
	if err != nil {
		log.Fatal(err)
	}
	// 设置请求头
	// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey := "sk-xxx"
	// 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/model-studio/get-api-key
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
	bodyText, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}
	// 打印响应内容
	fmt.Printf("%s\n", bodyText)
}
```

PHP

```
<?php
// 设置请求的URL
// 以下是北京地域url，如果使用新加坡地域的模型，需要将url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
$url = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions';
// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：$apiKey = "sk-xxx";
// 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/model-studio/get-api-key
$apiKey = getenv('DASHSCOPE_API_KEY');
// 设置请求头
$headers = [
    'Authorization: Bearer '.$apiKey,
    'Content-Type: application/json'
];
// 设置请求体
$data = [
    // 模型列表：https://help.aliyun.com/model-studio/getting-started/models
    "model" => "qwen-plus",
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
if (curl_errno($ch)) {
    echo 'Curl error: ' . curl_error($ch);
}
// 关闭cURL资源
curl_close($ch);
// 输出响应结果
echo $response;
?>
```

C#

```
using System.Net.Http.Headers;
using System.Text;

class Program
{
    private static readonly HttpClient httpClient = new HttpClient();

    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：string? apiKey = "sk-xxx";
        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/model-studio/get-api-key
        string? apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY");

        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine("API Key 未设置。请确保环境变量 'DASHSCOPE_API_KEY' 已设置。");
            return;
        }
        // 以下是北京地域url，如果使用新加坡地域的模型，需要将url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
        string url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions";
        // 模型列表：https://help.aliyun.com/model-studio/getting-started/models
        string jsonContent = @"{
            ""model"": ""qwen-plus"",
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

        // 发送请求并获取响应
        string result = await SendPostRequestAsync(url, jsonContent, apiKey);

        // 输出结果
        Console.WriteLine(result);
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

## **API参考**

-   关于千问API的输入输出参数，请参见[千问](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)。
    
-   关于其他模型，请参见[模型列表](https://help.aliyun.com/zh/model-studio/models)。
    

## **常见问题**

### [**免费额度**](https://bailian.console.aliyun.com/#/model-market/detail/qwen-max-latest)**用完后如何购买 Token？**

A：您可以访问[费用与成本](https://usercenter2.aliyun.com/home)中心，确保您的账户没有欠费即可调用千问模型。

> 调用千问模型会自动扣费，出账周期为分钟级（即一条账单代表一分钟内的费用）。消费明细请前往**[账单详情](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)**进行查看。

### **调用大模型API后报错**`**Model.AccessDenied**`**，如何处理？**

A：该报错是因为您使用子业务空间的API Key，子业务空间无法访问**主账号空间**的应用或模型。使用子空间API Key需由主账号管理员为对应子空间开通模型授权（如本文使用`千问-Plus`模型）。详细操作步骤请参见[设置模型调用权限](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l)。

### **如何接入** [**Chatbox**](https://chatboxai.app/zh)**、**[**Cherry Studio**](https://cherry-ai.com/)**、**[Cline](https://cline.bot/)**或** [Dify](https://cloud.dify.ai/apps)**？**

A：请根据您的使用情况参考以下步骤：

> 此处以使用较多的工具为例，其它大模型工具接入的方法较为类似。

## Chatbox

请参见[Chatbox](https://help.aliyun.com/zh/model-studio/chatbox)。

## Cherry Studio

1.  单击左下角的设置按钮，在**模型服务**栏中找到**阿里云百炼**，**API 密钥**输入您的 API Key，获取方法请参见：[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)；**API 地址**填入`https://dashscope.aliyuncs.com/compatible-mode/v1/`；单击**添加**。
    
    ![image.png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    
2.  在**模型 ID**填入您需要使用的千问模型，此处以 qwen-max-latest 为例（更多可用的模型请参考[模型列表](https://help.aliyun.com/zh/model-studio/models)中的千问模型）； **模型名称**与**分组名称**会自动生成。
    
    ![image.png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    
3.  在界面上方选中添加的模型，部分模型支持联网搜索，打开输入框处的联网搜索按钮。输入“杭州天气咋样？”进行测试：
    
    ![image.png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=)
    

## Cline

请参见[Cline](https://help.aliyun.com/zh/model-studio/cline)。

## Dify

请参见[Dify](https://help.aliyun.com/zh/model-studio/dify)。

## **下一步**

| **查看更多模型** | 示例代码以 qwen-plus 模型为例，阿里云百炼还支持其他千问模型与 DeepSeek、Llama 等第三方模型，**支持的模型**以及对应的**API参考**文档请参见[模型列表](https://help.aliyun.com/zh/model-studio/models)。 |
| --- | --- |
| **了解进阶用法** | 示例代码仅完成了简单问答，如果您想了解千问 API 的更多用法，如[流式输出](https://help.aliyun.com/zh/model-studio/stream)、[结构化输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output)、[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)等，请参见[文本生成模型概述](https://help.aliyun.com/zh/model-studio/text-generation)目录。 |
| **在线体验大模型** | 如果您想像[千问官网](https://tongyi.aliyun.com/qianwen/)一样，通过**对话框**与大模型互动，请访问模型体验（[北京](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/text)或[新加坡](https://modelstudio.console.aliyun.com/?tab=dashboard#/efm/model_experience_center/text)）。 > 千问官网将千问 API 与联网搜索、网页解析等工具进行了集成，与直接调用千问 API 效果略有差异。 |
| **0代码进行大模型微调** | 通常来说，对大模型微调需要有人工智能知识背景与工程能力，阿里云百炼提供了0代码对大模型进行微调的功能，您仅需提供数据集即可。详情请参见[在控制台进行模型调优](https://help.aliyun.com/zh/model-studio/model-training-on-console)。 |

阿里云百炼提供了丰富多样的模型选择，它集成了千问系列大模型和第三方大模型，涵盖文本、图像、音视频等不同模态。

## 旗舰模型

## **中国内地**

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

Qwen3.5-Plus 支持文本、图像和视频输入，纯文本表现媲美 Qwen3-Max，速度更快、成本更低；多模态能力也显著优于 Qwen3-VL 系列。

| **旗舰模型** | ![new](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4297966571/p838707.png) **Qwen3-Max** 适合复杂任务，能力最强 | ![new](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4297966571/p838707.png) **Qwen3.5-Plus** 效果、速度、成本均衡 | ![new](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4297966571/p838707.png) **Qwen3.5-Flash** 适合简单任务，速度快、成本低 |
| --- | --- | --- | --- |
| 最大上下文长度 （Token数） | 262,144 | 1,000,000 | 1,000,000 |
| 最低输入价格 （每百万 Token） | 2.5元 | 0.8元 | 0.2元 |
| 最低输出价格 （每百万 Token） | 10元 | 4.8元 | 2元  |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

Qwen3.5-Plus 支持文本、图像和视频输入，纯文本表现媲美 Qwen3-Max，速度更快、成本更低；多模态能力也显著优于 Qwen3-VL 系列。

| **旗舰模型** | ![new](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4297966571/p838707.png) **Qwen3-Max** 适合复杂任务，能力最强 | ![new](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4297966571/p838707.png) **Qwen3.5-Plus** 效果、速度、成本均衡 | ![new](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) **Qwen3.5-Flash** 适合简单任务，速度快、成本低 |
| --- | --- | --- | --- |
| 最大上下文长度 （Token数） | 262,144 | 1,000,000 | 1,000,000 |
| 最低输入价格 （每百万 Token） | 2.5元 | 0.8元 | 0.2元 |
| 最低输出价格 （每百万 Token） | 10元 | 4.8元 | 2元  |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

Qwen3.5-Plus 支持文本、图像和视频输入，纯文本表现媲美 Qwen3-Max，速度更快、成本更低；多模态能力也显著优于 Qwen3-VL 系列。

| **旗舰模型** | ![new](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) **Qwen3-Max** 适合复杂任务，能力最强 | ![new](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) **Qwen3.5-Plus** 效果、速度、成本均衡 | ![new](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) **Qwen3.5-Flash** 适合简单任务，速度快、成本低 |
| --- | --- | --- | --- |
| 最大上下文长度 （Token数） | 262,144 | 1,000,000 | 1,000,000 |
| 最低输入价格 （每百万 Token） | 8.807元 | 2.936元 | 0.734元 |
| 最低输出价格 （每百万 Token） | 44.035元 | 17.614元 | 2.936元 |

## 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

| **旗舰模型** | ![new](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) **千问Plus** 效果、速度、成本均衡 | ![new](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) **千问Flash** 适合简单任务，速度快、成本低 |
| --- | --- | --- |
| 最大上下文长度 （Token数） | 1,000,000 | 1,000,000 |
| 最低输入价格 （每百万 Token） | 2.936元 | 0.367元 |
| 最低输出价格 （每百万 Token） | 8.807元 | 2.936元 |

> 关于详细参数以及更多大模型，请查看下方的表格。

## **模型总览**

## **中国内地**

| **类别** | **子类别** | **说明** |
| 文本生成 | [通用大语言模型](#9f8890ce29g5u) | - 千问大语言模型： - 商业版：[千问Max](#d4ccf72f23jh9)、[千问Plus](#5ef284d4ed42p)（已升级至Qwen3.5）、[千问Flash](#13ff05e329blt)（已升级至Qwen3.5） - 开源版：[Qwen3.5](#479d0567e1a8z)、[Qwen3](#94410dcf1al50)、[Qwen2.5](#15f2bdc5dd3zd) - 第三方模型：[DeepSeek](#935bd5ba5cg5d)、[Kimi](#2363cbf60fe6m)、[GLM](#059d6a5d1chfp)、[MiniMax](#6194236b53fx0)等。 |
| [多模态模型](#5e79514e7cqp5) | 视觉理解模型（[千问Plus](#5ef284d4ed42p)、[千问VL](#3f1f1c8913fvo)、[QVQ](#40e07d9a04nx8)）、音频理解模型[千问Audio](#e176089a74849)、全模态模型[千问Omni](#90e80b9e42ged)、实时多模态模型[千问Omni-Realtime](#a162110bff6c4) |
| [领域模型](#543aadfcc9ziv) | [代码模型](#d698550551bob)、[长文本处理模型](#27b2b3a15d5c6)、[数学模型](#543aadfcc9ziv)、[翻译模型](#b51e22f4b036h)、[法律模型](#f0436273ef1xm)、[数据挖掘模型](#531dbf3f1addx)、[深入研究模型](#af665c3673n6e)、[意图理解模型](#85209145a5r68)、[角色扮演模型](#083f31bde1lv3)、[对话分析模型](#067fbf0cceu7d) |
| 图像生成 | [文生图](#96837528cdqes) | 通用模型： - [千问文生图](#96837528cdqes)：在处理复杂指令、渲染中英文本及生成高清写实图片方面表现突出，支持根据效率与质量需求选择不同模型。 - 万相文生图： - [基础文生图](#d9510a8d75x8f)：适用于生成证件照、电商主图、模特图、各种风格人像图（动漫、国风、二次元等）。 - [图文混排输出](#157125edeb9tx)：先生成一段文字描述，随后紧接生成对应的图像，实现“文+图”的连贯输出。 - [Z-Image](#d7ef4964cd1vk)：轻量级文生图模型，可快速生成高质量图像，支持中英双语渲染、复杂语义理解和多风格题材。 - 第三方模型：[Stable Diffusion](#a4321a2dc7zg7)、[FLUX](#8b57fb1fbf2op)和 [可灵-图像生成](#e36820d56d3km)。 更多模型：[创意海报生成](#8a3d8eb0e8afq)、[创意文字生成-WordArt锦书](#e9cc0a9c44sdv)。 |
| [图像编辑](#bfe15d8aa2lxh) | 通用模型： - [千问图像编辑](#bfe15d8aa2lxh)：支持中英文提示词输入，可实现风格迁移、文字修改、物体编辑等复杂图文编辑操作。同时支持多图融合，适配广泛多样的工业化应用场景。 - [万相图像编辑](#157125edeb9tx)：适用于多图融合、风格迁移、目标检测、图像修复、去水印等场景。模型系列包括：[万相2.6](#157125edeb9tx)、[万相2.5](#4ba45a8357xdh)、[万相2.1](#8d5f5532099th)。 更多模型：[千问图像翻译](https://help.aliyun.com/zh/model-studio/qwen-mt-image-api)、[万相涂鸦作画](#5a4a19ad53er2)、[万相图像局部重绘](#d1cc07f214l3u)、[人像风格重绘](#c831fed18dhqv)、[图像背景生成](#60547f06c6qrm)、[图像画面扩展](#8e9b6350c62zt)、[人物实例分割](#8241c12baef0w)、[图像擦除补全](#1bc8993067cot)、[虚拟模特](#c5467902ebwjo)、[鞋靴模特](#e739c93771efr)、[人物写真生成-FaceChain](#4eba270341qlv)、[AI试衣](#b11d85fe06ogg) |
| 语音合成与识别 | [语音合成](#b9e5744149hd6) | [千问实时语音合成](#05782f7968r7g)、[千问语音合成](#e62b64f642k63)、[CosyVoice语音合成](#7a960cc042zwt)和[Sambert语音合成](#95be68362c11b)可实现文本转语音，适用于智能语音客服、有声读物、车载导航、教育辅导等场景。 |
| [语音识别/翻译](#696c1bf328gf9) | [千问实时语音识别](#04625778f9jd5)、[千问录音文件识别](#8017a37ad5a66)、[Fun-ASR语音识别](#140159cc9b5iz)、[Gummy语音识别/翻译](#9e21336740rk2)、[Paraformer语音识别](#c018769cd7y88)和[SenseVoice语音识别](#511fe328d19af)可实现语音转文本，适用于实时会议记录、实时直播字幕、电话客服等场景。此外，[Gummy语音识别/翻译](#9e21336740rk2)还支持语音翻译。 |
| 视频编辑与生成 | [文生视频](#7a13292788yvp) | [文生视频](#7a13292788yvp)：一句话生成视频，视频风格丰富，画质细腻。 更多模型：[爱诗-文生视频](#0f70069440fuf)、[Vidu-文生视频](#601c240fcd9nw)。 |
| [图生视频](#af6bc5a9c3cp9) | - [首帧生视频](#af6bc5a9c3cp9)：以输入图像作为视频首帧，结合提示词生成完整视频。 - [首尾帧生视频](#90cb98a2b9s2q)：提供首帧与尾帧图像，结合提示词生成过渡自然的视频。 - [多图生视频](#f7de663db89xi)：支持输入一张或多张图片，参考图片中的主体或背景，并结合提示词生成视频。 - 图+动作模板生成舞蹈视频：[舞动人像AnimateAnyone](#a54957baf9exo)基于人物图片和动作视频生成舞蹈视频。 - 图+音频生成对口型视频 - [万相-数字人](#3bff5da885yx3)基于人物**图片**和音频，动作幅度大且自然，支持全身、半身、肖像等多种画幅，适合唱歌、表演等场景。 - [悦动人像EMO](#c6384886fd3s8)基于人物**图片**和音频，口型与表情表现力强，支持肖像、半身，适合人物特写场景。 - [灵动人像LivePortrait](#45109ade609nr)基于人物**图片**和音频，适合语音播报场景。 - 图+表情模板生成表情包视频：[表情包Emoji](#f62472e1b6m3b)基于人脸图片和预设的人脸动态模板，生成人脸表情包视频。 更多模型：[爱诗-图生视频-基于首帧](#62b5c1d4d6ijo)、[爱诗-图生视频-基于首尾帧](#4e4ebc10f7cvw)、[可灵-视频生成](#93251aa4ebi3q)、[Vidu-图生视频-基于首帧](#e9c949c200dw7)、[Vidu-图生视频-基于首尾帧](#ba9aa2e28dyq0)。 |
| [参考生视频](#62b53b525bud3) | [参考生视频](#62b53b525bud3)：参考输入视频或图像的角色形象，同时可参考视频中的音色，结合提示词生成表演视频。 更多模型：[爱诗-参考生视频](#0080eb1384z27)、 [可灵-视频生成](#93251aa4ebi3q)、[Vidu-参考生视频](#9e43ea149dw8k)。 |
| [视频编辑](#f7de663db89xi) | - [通用视频编辑](#f7de663db89xi)：基于输入的文本提示词、图片和视频，可执行多种视频编辑任务。例如，通过提取输入视频的运动特征，并结合提示词生成新的视频。 - 视频口型替换：[声动人像VideoRetalk](#3714ddc2e6a0p)基于人物**视频**和音频，适合短视频制作、视频翻译等场景。 - 视频风格转换：[视频风格重绘](#21cd0ccad2ota)可将视频转换为日式漫画、美式漫画等风格。 更多模型：[可灵-视频生成](#93251aa4ebi3q)。 |
| 向量  | [文本向量](#3383780daf8hw) | 将文本转换成一组可以代表文字的数字，用于搜索、聚类、推荐、分类等。 |
| [多模态向量](#9bda215aa7mko) | 将文本、图像、语音转换成一组数字，用于音视频分类、图像分类、图文检索等。 |
| 行业  | [通义法睿](#f0436273ef1xm) | 适用于法律咨询、案例分析和法规解读等。 |
| [意图理解](#85209145a5r68) | [意图理解模型](#85209145a5r68)能够在毫秒级时间内解析用户意图，并选择合适工具来解决用户问题。 |

## 全球

| **类别** | **子类别** | **说明** |
| --- | --- | --- |
| 文本生成 | [通用大语言模型](#9f8890ce29g5u) | 千问大语言模型： - 商业版：[千问Max](#d4ccf72f23jh9)、[千问Plus](#5ef284d4ed42p)、[千问Flash](#13ff05e329blt) - 开源版：[Qwen3](#94410dcf1al50) |
| [多模态模型](#5e79514e7cqp5) | 视觉理解模型[千问VL](#3f1f1c8913fvo) |
| [领域模型](#543aadfcc9ziv) | [代码模型](#d698550551bob)、[翻译模型](#b51e22f4b036h) |
| 图像生成 | [文生图](#96837528cdqes) | - 万相文生图： - [基础文生图](#d9510a8d75x8f)：适用于生成证件照、电商主图、模特图、各种风格人像图（动漫、国风、二次元等）。 - [图文混排输出](#157125edeb9tx)：先生成一段文字描述，随后紧接生成对应的图像，实现“文+图”的连贯输出。 |
| [图像编辑](#bfe15d8aa2lxh) | - [万相图像编辑](#157125edeb9tx)：适用于多图融合、风格迁移、目标检测、图像修复、去水印等场景。模型系列：[万相2.6](#157125edeb9tx) |
| 视频编辑与生成 | [文生视频](#7a13292788yvp) | - [文生视频](#7a13292788yvp)：一句话生成视频，视频风格丰富，画质细腻。 |
| [图生视频](#af6bc5a9c3cp9) | [首帧生视频](#af6bc5a9c3cp9)：以输入图像作为视频首帧，结合提示词生成完整视频。 |
| [视频生视频](#62b53b525bud3) | [参考生视频](#62b53b525bud3)：参考输入视频或图像的角色形象，同时可参考视频中的音色，结合提示词生成表演视频。 |

## 国际

| **类别** | **子类别** | **说明** |
| --- | --- | --- |
| 文本生成 | [通用大语言模型](#9f8890ce29g5u) | 千问大语言模型： - 商业版：[千问Max](#d4ccf72f23jh9)、[千问Plus](#5ef284d4ed42p)（已升级至Qwen3.5）、[千问Flash](#13ff05e329blt)（已升级至Qwen3.5） - 开源版：[Qwen3.5](#479d0567e1a8z)、[Qwen3](#94410dcf1al50)、[Qwen2.5](#15f2bdc5dd3zd) |
| [多模态模型](#5e79514e7cqp5) | 视觉理解模型（[千问Plus](#5ef284d4ed42p)、[千问VL](#3f1f1c8913fvo)、[QVQ](#40e07d9a04nx8)）、全模态模型[千问Omni](#90e80b9e42ged)、实时多模态模型[千问Omni-Realtime](#a162110bff6c4) |
| [领域模型](#543aadfcc9ziv) | [代码模型](#d698550551bob)、[翻译模型](#b51e22f4b036h)、[角色扮演模型](#083f31bde1lv3) |
| 图像生成 | [文生图](#96837528cdqes) | - [千问文生图](#96837528cdqes)：在处理复杂指令、渲染中英文本及生成高清写实图片方面表现突出，支持根据效率与质量需求选择不同模型。 - 万相文生图： - [基础文生图](#d9510a8d75x8f)：适用于生成证件照、电商主图、模特图、各种风格人像图（动漫、国风、二次元等）。 - [图文混排输出](#157125edeb9tx)：先生成一段文字描述，随后紧接生成对应的图像，实现“文+图”的连贯输出。 - [Z-Image](#d7ef4964cd1vk)：轻量级文生图模型，可快速生成高质量图像，支持中英双语渲染、复杂语义理解和多风格题材。 |
| [图像编辑](#bfe15d8aa2lxh) | [千问图像编辑](#bfe15d8aa2lxh)：支持中英文提示词输入，可实现风格迁移、文字修改、物体编辑等复杂图文编辑操作。同时支持多图融合，适配广泛多样的工业化应用场景。 [万相图像编辑](#157125edeb9tx)：适用于多图融合、风格迁移、目标检测、图像修复、去水印等场景。模型系列包括：[万相2.6](#157125edeb9tx)、[万相2.5](#4ba45a8357xdh)。 |
| 视频生成 | [文生视频](#7a13292788yvp) | [文生视频](#7a13292788yvp)：一句话生成视频，视频风格丰富，画质细腻。 |
| [图生视频](#af6bc5a9c3cp9) | - [首帧生视频](#af6bc5a9c3cp9)：以输入图像作为视频首帧，结合提示词生成完整视频。 - [首尾帧生视频](#90cb98a2b9s2q)：提供首帧与尾帧图像，结合提示词生成过渡自然的视频。 - [多图生视频](#f7de663db89xi)：支持输入一张或多张图片，参考图片中的主体或背景，并结合提示词生成视频。 |
| [视频生视频](#62b53b525bud3) | [参考生视频](#62b53b525bud3)：参考输入视频或图像的角色形象，同时可参考视频中的音色，结合提示词生成表演视频。 |
| [视频编辑](#f7de663db89xi) | [通用视频编辑](#f7de663db89xi)：基于输入的文本提示词、图片和视频，可执行多种视频编辑任务。例如，通过提取输入视频的运动特征，并结合提示词生成新的视频。 |
| 向量  | [文本向量](#3383780daf8hw) | 将文本转换成一组可以代表文字的数字，用于搜索、聚类、推荐、分类等。 |

## 美国

| **类别** | **子类别** | **说明** |
| --- | --- | --- |
| 文本生成 | [文本生成-千问](#9f8890ce29g5u) | 千问大语言模型：商业版（[千问Plus](#5ef284d4ed42p)、[千问Flash](#13ff05e329blt)） |
| [千问VL](#3f1f1c8913fvo) | 视觉理解模型[千问VL](#3f1f1c8913fvo) |
| 视频生成 | [文生视频](#7a13292788yvp) | 一句话生成视频，视频风格丰富，画质细腻。 |
| [图生视频](#af6bc5a9c3cp9) | [首帧生视频](#af6bc5a9c3cp9)：将输入图片作为视频首帧，并根据提示词生成视频。 |
| 语音识别 | [语音识别](#696c1bf328gf9) | [千问录音文件识别](#8017a37ad5a66)可实现语音转文本，适用于会议记录、直播字幕等场景。 |

## **文本生成-千问**

以下为千问商业版模型。相比开源版，商业版具有更新的能力和优化。

> 商业版暂不透出参数规模。

> 若有高并发需求，建议优先使用稳定版或最新版，[限流](https://help.aliyun.com/zh/model-studio/rate-limit)条件更宽松。

> 稳定版模型会不定期更新升级。若需使用固定版本，请选择快照版本。

### **千问Max**

千问系列效果最好的模型，适合复杂、多步骤的任务。[使用方法](https://help.aliyun.com/zh/model-studio/text-generation#24e54b27d4agt)｜[思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)｜[API参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)｜[在线体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/text?currentTab=textChat&modelId=qwen3-max)

#### **中国内地**

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **模式** | **上下文长度** | **最大输入** | **最长思维链** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| qwen3-max > 当前与qwen3-max-2026-01-23能力相同 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 > 支持[调用内置工具](https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api#11cd08d0ffnxw) | 稳定版 | 思考  | 262,144 | 258,048 | 81,920 | 32,768 | 阶梯计价，请参见表格下方说明。 |   | 各100万Token 有效期：百炼开通后90天内 |
| 非思考 | \\- | 65,536 |
| qwen3-max-2026-01-23 > 思考模式为[Qwen3-Max-Thinking](https://qwen.ai/blog?id=qwen3-max-thinking) > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 > 支持[调用内置工具](https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api#11cd08d0ffnxw) | 快照版 | 思考  | 81,920 | 32,768 |
| 非思考 | \\- | 65,536 |
| qwen3-max-2025-09-23 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 快照版 | 仅非思考 |
| qwen3-max-preview > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 预览版 | 思考  | 81,920 | 32,768 |
| 非思考 | \\- | 65,536 |

以上模型根据本次请求的输入 Token数，采取阶梯计费。

| **模型名称** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链+回答** |
| --- | --- | --- | --- |
| qwen3-max > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 0<Token≤32K | 2.5元 | 10元 |
| 32K<Token≤128K | 4元  | 16元 |
| 128K<Token≤252K | 7元  | 28元 |
| qwen3-max-2026-01-23 | 0<Token≤32K | 2.5元 | 10元 |
| 32K<Token≤128K | 4元  | 16元 |
| 128K<Token≤252K | 7元  | 28元 |
| qwen3-max-2025-09-23 | 0<Token≤32K | 6元  | 24元 |
| 32K<Token≤128K | 10元 | 40元 |
| 128K<Token≤252K | 15元 | 60元 |
| qwen3-max-preview > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 0<Token≤32K | 6元  | 24元 |
| 32K<Token≤128K | 10元 | 40元 |
| 128K<Token≤252K | 15元 | 60元 |

**更多模型**

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen-max** > 当前与qwen-max-2024-09-19能力相同 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 稳定版 | 32,768 | 30,720 | 8,192 | 2.4元 | 9.6元 | 各100万Token 有效期：百炼开通后90天内 |
| **qwen-max-latest** > 始终与最新快照版能力相同 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 最新版 | 131,072 | 129,024 |
| qwen-max-2025-01-25 > 又称qwen-max-0125、[Qwen2.5-Max](https://qwenlm.github.io/zh/blog/qwen2.5-max/) | 快照版 |
| qwen-max-2024-09-19 > 又称qwen-max-0919 | 32,768 | 30,720 | 20元 | 60元 |
| qwen-max-2024-04-28 > 又称qwen-max-0428 | 快照版 | 8,000 | 6,000 | 2,000 | 40元 | 120元 |

#### 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **版本** | **模式** | **上下文长度** | **最大输入** | **最长思维链** | **最大输出** | **输入成本** | **输出成本** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| qwen3-max > 当前与qwen3-max-2025-09-23能力相同 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 稳定版 | 仅非思考 | 262,144 | 258,048 | \\- | 65,536 | 阶梯计价，请参见表格下方说明。 |   |
| qwen3-max-2025-09-23 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 快照版 | 仅非思考 |
| qwen3-max-preview > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系 | 预览版 | 思考  | 81,920 | 32,768 |
| 非思考 | \\- | 65,536 |

以上模型根据本次请求的输入 Token数，采取阶梯计费。

| **模型名称** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链+回答** |
| --- | --- | --- | --- |
| qwen3-max > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 0<Token≤32K | 2.5元 | 10元 |
| 32K<Token≤128K | 4元  | 16元 |
| 128K<Token≤252K | 7元  | 28元 |
| qwen3-max-2025-09-23 | 0<Token≤32K | 6元  | 24元 |
| 32K<Token≤128K | 10元 | 40元 |
| 128K<Token≤252K | 15元 | 60元 |
| qwen3-max-preview > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 0<Token≤32K | 6元  | 24元 |
| 32K<Token≤128K | 10元 | 40元 |
| 128K<Token≤252K | 15元 | 60元 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **版本** | **模式** | **上下文长度** | **最大输入** | **最长思维链** | **最大输出** | **输入成本** | **输出成本** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| qwen3-max > 当前与qwen3-max-2026-01-23能力相同 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 > 支持[调用内置工具](https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api#11cd08d0ffnxw) | 稳定版 | 思考  | 262,144 | 258,048 | 81,920 | 32,768 | 阶梯计价，请参见表格下方说明。 |   |
| 非思考 | \\- | 65,536 |
| qwen3-max-2026-01-23 > 思考模式为[Qwen3-Max-Thinking](https://qwen.ai/blog?id=qwen3-max-thinking) > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 > 支持[调用内置工具](https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api#11cd08d0ffnxw) | 快照版 | 思考  | 81,920 | 32,768 |
| 非思考 | \\- | 65,536 |
| qwen3-max-2025-09-23 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 快照版 | 仅非思考 |
| qwen3-max-preview > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 预览版 | 思考  | 81,920 | 32,768 |
| 非思考 | \\- | 65,536 |

以上模型根据本次请求的输入 Token数，采取阶梯计费。

| **单次请求的输入Token数** | **输入价格（每百万Token）** > qwen3-max、qwen3-max-preview 支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。 | **输出价格（每百万Token）** |
| --- | --- | --- |
| 0<Token≤32K | 8.807元 | 44.035元 |
| 32K<Token≤128K | 17.614元 | 88.071元 |
| 128K<Token≤252K | 22.018元 | 110.089元 |

**更多模型**

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen-max** > 当前与qwen-max-2025-01-25能力相同 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 稳定版 | 32,768 | 30,720 | 8,192 | 11.743元 | 46.971元 | 无免费额度 |
| **qwen-max-latest** > 始终与最新快照版能力相同 | 最新版 | 11.743元 | 46.971元 |
| qwen-max-2025-01-25 > 又称qwen-max-0125、[Qwen2.5-Max](https://qwenlm.github.io/zh/blog/qwen2.5-max/) | 快照版 |

> qwen3-max-2026-01-23 模型的思考模式：相较于 2025 年 9 月 23 日的快照版本，有效融合了思考模式与非思考模式，显著提升了模型的整体性能。在思考模式下，模型集成了 Web 搜索、网页信息提取和代码解释器三项工具，通过在思考过程中引入外部工具，在复杂问题上实现更高的准确率。

qwen3-max与qwen3-max-2026-01-23、qwen3-max-2025-09-23模型原生支持search agent，请参见[联网搜索](https://help.aliyun.com/zh/model-studio/web-search)。

### **千问Plus**

能力均衡，推理效果、成本和速度介于千问Max和千问Flash之间，适合中等复杂任务。[使用方法](https://help.aliyun.com/zh/model-studio/text-generation#24e54b27d4agt)｜[思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)｜[API参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)｜[在线体验](https://bailian.console.aliyun.com/?#/efm/model_experience_center/text?currentTab=textChat&modelId=qwen3.5-plus)

> Qwen3.5 Plus 支持文本、图像和视频输入。在纯文本任务上的效果可媲美 Qwen3 Max，性能更优且成本更低。在多模态能力上，相比 Qwen3 VL 系列有显著提升。

#### **中国内地**

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **模式** | **上下文长度** | **最大输入** | **最长思维链** | **最大输出** | **输入成本** | **输出成本** > **思维链+输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| **qwen3.5-plus** > 当前与qwen3.5-plus-2026-02-15能力相同 > 默认开启思考模式 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 稳定版 | 思考  | 1,000,000 | 983,616 | 81,920 | 65,536 | 阶梯计价，请参见表格下方说明。 |   | 各100万Token 有效期：百炼开通后90天内 |
| 非思考 | 991,808 | \\- |
| qwen3.5-plus-2026-02-15 > 默认开启思考模式 | 快照版 | 思考  | 983,616 | 81,920 |
| 非思考 | 991,808 | \\- |
| **qwen-plus** > 当前与qwen-plus-2025-12-01能力相同 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 稳定版 | 思考  | 995,904 | 81,920 | 32,768 |
| 非思考 | 997,952 | \\- |
| **qwen-plus-latest** > 当前与qwen-plus-2025-12-01能力相同 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 最新版 | 思考  | 995,904 | 81,920 |
| 非思考 | 997,952 | \\- |
| qwen-plus-2025-12-01 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 快照版 | 思考  | 995,904 | 81,920 |
| 非思考 | 997,952 | \\- |
| qwen-plus-2025-09-11 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 思考  | 995,904 | 81,920 |
| 非思考 | 997,952 | \\- |
| qwen-plus-2025-07-28 > 又称qwen-plus-0728 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 思考  | 995,904 | 81,920 |
| 非思考 | 997,952 | \\- |
| qwen-plus-2025-07-14 > 又称qwen-plus-0714 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 思考  | 131,072 | 98,304 | 38,912 | 16,384 | 0.8元 | 8元  |
| 非思考 | 129,024 | \\- | 2元  |
| qwen-plus-2025-04-28 > 又称qwen-plus-0428 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 思考  | 98,304 | 38,912 | 8元  |
| 非思考 | 129,024 | \\- | 2元  |

以上模型根据本次请求输入的 Token数，采取阶梯计费。

##### **Qwen3.5-Plus**

| **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- |
| 0<Token≤128K | 0.8元 | 4.8元 |
| 128K<Token≤256K | 2元  | 12元 |
| 256K<Token≤1M | 4元  | 24元 |

##### Qwen-Plus

| **单次请求的输入Token数** | **模式** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- | --- |
| 0<Token≤128K | 非思考模式 | 0.8元 | 2元  |
| 思考模式 | 8元  |
| 128K<Token≤256K | 非思考模式 | 2.4元 | 20元 |
| 思考模式 | 24元 |
| 256K<Token≤1M | 非思考模式 | 4.8元 | 48元 |
| 思考模式 | 64元 |

上述模型支持思考模式和非思考模式，通过 `enable_thinking` 参数实现两种模式的切换。

**更多模型**

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| qwen-plus-2025-01-25 > 又称qwen-plus-0125 | 快照版 | 131,072 | 129,024 | 8,192 | 0.8元 | 2元  | 各100万Token 有效期：百炼开通后90天内 |
| qwen-plus-2025-01-12 > 又称qwen-plus-0112 |
| qwen-plus-2024-12-20 > 又称qwen-plus-1220 |

#### 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **版本** | **模式** | **上下文长度** | **最大输入** | **最长思维链** | **最大输出** | **输入成本** | **输出成本** > **思维链+输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| **qwen3.5-plus** > 当前与qwen3.5-plus-2026-02-15能力相同 > 默认开启思考模式 | 稳定版 | 思考  | 1,000,000 | 983,616 | 81,920 | 65,536 | 阶梯计价，请参见表格下方说明。 |   | 无   |
| 非思考 | 991,808 | \\- |
| qwen3.5-plus-2026-02-15 > 默认开启思考模式 | 快照版 | 思考  | 983,616 | 81,920 |
| 非思考 | 991,808 | \\- |
| **qwen-plus** > 当前与qwen-plus-2025-12-01能力相同 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 稳定版 | 思考  | 995,904 | 81,920 | 32,768 |
| 非思考 | 997,952 | \\- |
| qwen-plus-2025-12-01 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 快照版 | 思考  | 995,904 | 81,920 |
| 非思考 | 997,952 | \\- |
| qwen-plus-2025-09-11 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 思考  | 995,904 | 81,920 |
| 非思考 | 997,952 | \\- |
| qwen-plus-2025-07-28 > 又称qwen-plus-0728 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 思考  | 995,904 | 81,920 |
| 非思考 | 997,952 | \\- |

以上模型根据本次请求输入的 Token数，采取阶梯计费。

##### **Qwen3.5-Plus**

| **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- |
| 0<Token≤128K | 0.8元 | 4.8元 |
| 128K<Token≤256K | 2元  | 12元 |
| 256K<Token≤1M | 4元  | 24元 |

##### Qwen-Plus

| **单次请求的输入Token数** | **模式** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- | --- |
| 0<Token≤128K | 非思考模式 | 0.8元 | 2元  |
| 思考模式 | 8元  |
| 128K<Token≤256K | 非思考模式 | 2.4元 | 20元 |
| 思考模式 | 24元 |
| 256K<Token≤1M | 非思考模式 | 4.8元 | 48元 |
| 思考模式 | 64元 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen3.5-plus** > 当前与qwen3.5-plus-2026-02-15能力相同 > 默认开启思考模式 | 稳定版 | 1,000,000 | **思考模式** 983,616 **非思考模式** 991,808 | 65,536 > 思维链最长81,920 | 阶梯计价，请参见表格下方说明。 |   | 无免费额度 |
| qwen3.5-plus-2026-02-15 > 默认开启思考模式 | 快照版 | **思考模式** 983,616 **非思考模式** 991,808 | 65,536 > 思维链最长81,920 |
| **qwen-plus** > 当前与qwen-plus-2025-12-01能力相同 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 稳定版 | **思考模式** 995,904 **非思考模式** 997,952 | 32,768 > 思维链最长81,920 |
| **qwen-plus-latest** > 当前与qwen-plus-2025-12-01能力相同 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 最新版 | **思考模式** 995,904 **非思考模式** 997,952 |
| qwen-plus-2025-12-01 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 快照版 | **思考模式** 995,904 **非思考模式** 997,952 |
| qwen-plus-2025-09-11 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 |
| qwen-plus-2025-07-28 > 又称qwen-plus-0728 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 |
| qwen-plus-2025-07-14 > 又称qwen-plus-0714 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 131,072 | **思考模式** 98,304 **非思考模式** 129,024 | 16,384 > 思维链最长38,912 | 2.936元 | 思考模式 29.357元 非思考模式 8.807元 |
| qwen-plus-2025-04-28 > 又称qwen-plus-0428 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 |
| qwen-plus-2025-01-25 > 又称qwen-plus-0125 | 129,024 | 8,192 | 8.807元 |

qwen3.5-plus、qwen3.5-plus-2026-02-15、qwen-plus、qwen-plus-latest、qwen-plus-2025-12-01、qwen-plus-2025-09-11和qwen-plus-2025-07-28 根据本次请求输入的 Token数，采取阶梯计费。

##### **Qwen3.5-Plus**

| **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- |
| 0<Token≤256K | 2.936元 | 17.614元 |
| 256K<Token≤1M | 3.67元 | 22.018元 |

##### Qwen-Plus

| **单次请求的输入Token数** | **输入价格（每百万Token）** | **模式** | **输出价格（每百万Token）** |
| --- | --- | --- | --- |
| 0<Token≤256K | 2.936元 | 非思考模式 | 8.807元 |
| 思考模式 | 29.357元 |
| 256K<Token≤1M | 8.807元 | 非思考模式 | 26.421元 |
| 思考模式 | 88.071元 |

#### 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen-plus-us** > 当前与 **qwen-plus-2025-12-01-us** 能力相同 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 稳定版 | 1,000,000 | **思考模式** 995,904 **非思考模式** 997,952 | 32,768 > 思维链最长81,920 | 阶梯计价，请参见表格下方说明。 |   | 无   |
| **qwen-plus-2025-12-01-us** > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 快照版 | **思考模式** 995,904 **非思考模式** 997,952 |

以上模型根据本次请求输入的 Token数采取阶梯计费，其中qwen-plus-us支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。

| **单次请求的输入Token数** | **输入价格（每百万Token）** | **模式** | **输出价格（每百万Token）** |
| --- | --- | --- | --- |
| 0<Token≤256K | 2.936元 | 非思考模式 | 8.807元 |
| 思考模式 | 29.357元 |
| 256K<Token≤1M | 8.807元 | 非思考模式 | 26.421元 |
| 思考模式 | 88.071元 |

### **千问Flash**

千问系列速度最快、成本极低的模型，适合简单任务。千问Flash采用灵活的阶梯定价，相比千问Turbo计费更合理。[使用方法](https://help.aliyun.com/zh/model-studio/text-generation#24e54b27d4agt) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/) | [在线体验](https://bailian.console.aliyun.com/?#/efm/model_experience_center/text?currentTab=textChat&modelId=qwen-flash) | [思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)

#### **中国内地**

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **模式** | **上下文长度** | **最大输入** | **最长思维链** | **最大输出** | **输入成本** | **输出成本** > **思维链+输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| **qwen3.5-flash** > 当前与 qwen3.5-flash-2026-02-23能力相同 > 默认开启思考模式 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 稳定版 | 思考  | 1,000,000 | 983,616 | 81,920 | 65,536 | 阶梯计价，请参见表格下方说明。 |   | 各100万Token 有效期：百炼开通后90天内 |
| 非思考 | 991,808 | \\- |
| **qwen3.5-flash-2026-02-23** > 默认开启思考模式 | 快照版 | 思考  | 983,616 | 81,920 |
| 非思考 | 991,808 | \\- |
| **qwen-flash** > 当前与 qwen-flash-2025-07-28能力相同 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 稳定版 | 思考  | 995,904 | 81,920 | 32,768 | 阶梯计价，请参见表格下方说明。 |   |
| 非思考 | 997,952 | \\- |
| **qwen-flash-2025-07-28** > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 快照版 | 思考  | 995,904 | 81,920 |
| 非思考 | 997,952 | \\- |

以上模型根据本次请求输入的 Token数采取阶梯计费。其中qwen3.5-flash、qwen-flash支持[缓存](https://help.aliyun.com/zh/model-studio/context-cache)和 [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)。

**qwen3.5-flash、qwen3.5-flash-2026-02-23 阶梯价格**

| **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- |
| 0<Token≤128K | 0.2元 | 2元  |
| 128K<Token≤256K | 0.8元 | 8元  |
| 256K<Token≤1M | 1.2元 | 12元 |

**qwen-flash、qwen-flash-2025-07-28 阶梯价格**

| **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- |
| 0<Token≤128K | 0.15元 | 1.5元 |
| 128K<Token≤256K | 0.6元 | 6元  |
| 256K<Token≤1M | 1.2元 | 12元 |

上述模型均支持思考模式和非思考模式，可通过 `enable_thinking` 参数实现两种模式的切换。

#### 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **版本** | **模式** | **上下文长度** | **最大输入** | **最长思维链** | **最大输出** | **输入成本** | **输出成本** > **思维链+输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| **qwen3.5-flash** > 当前与 qwen3.5-flash-2026-02-23能力相同 > 默认开启思考模式 | 稳定版 | 思考  | 1,000,000 | 983,616 | 81,920 | 65,536 | 阶梯计价，请参见表格下方说明。 |   | 无   |
| 非思考 | 991,808 | \\- |
| **qwen3.5-flash-2026-02-23** > 默认开启思考模式 | 快照版 | 思考  | 983,616 | 81,920 |
| 非思考 | 991,808 | \\- |
| **qwen-flash** > 当前与 qwen-flash-2025-07-28能力相同 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 稳定版 | 思考  | 995,904 | 81,920 | 32,768 |
| 非思考 | 997,952 | \\- |
| **qwen-flash-2025-07-28** > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 快照版 | 思考  | 995,904 | 81,920 |
| 非思考 | 997,952 | \\- |

以上模型根据本次请求输入的 Token数采取阶梯计费。

**qwen3.5-flash、qwen3.5-flash-2026-02-23 阶梯价格**

| **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- |
| 0<Token≤128K | 0.2元 | 2元  |
| 128K<Token≤256K | 0.8元 | 8元  |
| 256K<Token≤1M | 1.2元 | 12元 |

**qwen-flash、qwen-flash-2025-07-28 阶梯价格**

| **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- |
| 0<Token≤128K | 0.15元 | 1.5元 |
| 128K<Token≤256K | 0.6元 | 6元  |
| 256K<Token≤1M | 1.2元 | 12元 |

上述模型均支持思考模式和非思考模式，可通过 `enable_thinking` 参数实现两种模式的切换。

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **版本** | **模式** | **上下文长度** | **最大输入** | **最长思维链** | **最大输出** | **输入成本** | **输出成本** > **思维链+输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| **qwen3.5-flash** > 当前与 qwen3.5-flash-2026-02-23能力相同 > 属于[Qwen3.5](https://qwenlm.github.io/zh/blog/qwen3.5/)系列 > 默认开启思考模式 | 稳定版 | 思考  | 1,000,000 | 983,616 | 81,920 | 65,536 | 0.734元 | 2.936元 | 无   |
| 非思考 | 991,808 | \\- |
| **qwen3.5-flash-2026-02-23** > 属于[Qwen3.5](https://qwenlm.github.io/zh/blog/qwen3.5/)系列 > 默认开启思考模式 | 快照版 | 思考  | 983,616 | 81,920 |
| 非思考 | 991,808 | \\- |
| **qwen-flash** > 当前与 qwen-flash-2025-07-28能力相同 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 > 支持[缓存](https://help.aliyun.com/zh/model-studio/context-cache)和 [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/) | 稳定版 | 思考  | 995,904 | 81,920 | 32,768 | 阶梯计价，请参见表格下方说明。 |   |
| 非思考 | 997,952 | \\- |
| **qwen-flash-2025-07-28** > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 快照版 | 思考  | 995,904 | 81,920 |
| 非思考 | 997,952 | \\- |

qwen-flash、qwen-flash-2025-07-28按下方价格计费，其中qwen-flash支持[缓存](https://help.aliyun.com/zh/model-studio/context-cache)和 [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)。

| **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- |
| 0<Token≤256K | 0.367元 | 2.936元 |
| 256K<Token≤1M | 1.835元 | 14.678元 |

上述模型均支持思考模式和非思考模式，可通过 `enable_thinking` 参数实现两种模式的切换。

#### 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

| **模型名称** | **版本** | **模式** | **上下文长度** | **最大输入** | **最长思维链** | **最大输出** | **输入成本** | **输出成本** > **思维链+输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| **qwen-flash-us** > 当前与 qwen-flash-2025-07-28-us能力相同 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 稳定版 | 思考  | 1,000,000 | 995,904 | 81,920 | 32,768 | 阶梯计价，请参见表格下方说明。 |   | 各100万Token 有效期：百炼开通后90天内 |
| 非思考 | 997,952 | \\- |
| **qwen-flash-2025-07-28-us** > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 快照版 | 思考  | 995,904 | 81,920 |
| 非思考 | 997,952 | \\- |

以上模型根据本次请求输入的 Token数采取阶梯计费，其中qwen-flash支持[缓存](https://help.aliyun.com/zh/model-studio/context-cache)。

| **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- |
| 0<Token≤256K | 0.367元 | 2.936元 |
| 256K<Token≤1M | 1.835元 | 14.678元 |

上述模型均支持思考模式和非思考模式，可通过 `enable_thinking` 参数实现两种模式的切换。

### **千问Turbo**

千问Turbo 后续不再更新，建议替换为千问Flash。千问Flash采用灵活的阶梯定价，计费更合理。[使用方法](https://help.aliyun.com/zh/model-studio/text-generation#24e54b27d4agt) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/) | [在线体验](https://bailian.console.aliyun.com/?#/efm/model_experience_center/text?currentTab=textChat&modelId=qwen-turbo)｜[思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)

#### **中国内地**

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |     | **（每百万Token）** |   |
| **qwen-turbo** > 当前与 qwen-turbo-2025-04-28能力相同 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 稳定版 | **思考模式** 131,072 **非思考模式** 1,000,000 | **思考模式** 98,304 **非思考模式** 1,000,000 | 16,384 > 思维链最长38,912 | 0.3元 | **思考模式** 3元 **非思考模式** 0.6元 | 各100万Token 有效期：百炼开通后90天内 |
| **qwen-turbo-latest** > 始终与最新快照版能力相同 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 最新版 |
| qwen-turbo-2025-07-15 > 又称qwen-turbo-0715 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 快照版 |
| qwen-turbo-2025-04-28 > 又称qwen-turbo-0428 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen-turbo** > 当前与qwen-turbo-2025-04-28能力相同 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 稳定版 | **思考模式** 131,072 **非思考模式** 1,000,000 | **思考模式** 98,304 **非思考模式** 1,000,000 | 16,384 > 思维链最长38,912 | 0.367元 | 思考模式：3.67元 非思考模式：1.468元 | 无免费额度 |
| **qwen-turbo-latest** > 始终与最新快照版能力相同 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 最新版 | 0.367元 | 思考模式：3.67元 非思考模式：1.468元 |
| qwen-turbo-2025-04-28 > 又称qwen-turbo-0428 > 属于[Qwen3](https://qwenlm.github.io/zh/blog/qwen3/)系列 | 快照版 |
| qwen-turbo-2024-11-01 > 又称qwen-turbo-1101 | 1,000,000 | 1,000,000 | 8,192 | 1.468元 |

上述模型均支持思考模式和非思考模式，可通过 `enable_thinking` 参数实现两种模式的切换。开启思考模式时如果没有输出思考过程，按非思考模式价格进行收费。

**更多模型**

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |     | **（每百万Token）** |   |
| qwen-turbo-2025-02-11 > 又称qwen-turbo-0211 | 快照版 | 1,000,000 | 1,000,000 | 8,192 | 0.3元 | 0.6元 | 各100万Token 有效期：百炼开通后90天内 |
| qwen-turbo-2024-11-01 > 又称qwen-turbo-1101 | 1000万Token 有效期：百炼开通后90天内 |

### **QwQ**

基于 Qwen2.5 模型训练的 QwQ 推理模型，通过强化学习大幅度提升了模型推理能力。模型数学代码等核心指标（AIME 24/25、LiveCodeBench）以及部分通用指标（IFEval、LiveBench等）达到DeepSeek-R1 满血版水平。[使用方法](https://help.aliyun.com/zh/model-studio/deep-thinking)

#### **中国内地**

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** > **思维链+输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| **qwq-plus** > 当前与qwq-plus-2025-03-05能力相同 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 稳定版 | 131,072 | 98,304 | 32,768 | 8,192 | 1.6元 | 4元  | 各100万 Token 有效期：百炼开通后90天内 |
| **qwq-plus-latest** > 始终与最新快照版能力相同 | 最新版 | 1.6元 | 4元  |
| qwq-plus-2025-03-05 > 又称qwq-plus-0305 | 快照版 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| **qwq-plus** | 稳定版 | 131,072 | 98,304 | 32,768 | 8,192 | 5.871元 | 17.614元 | 无免费额度 |

### 千问Long

千问系列上下文窗口最长，能力均衡且成本较低的模型，适合长文本分析、信息抽取、总结摘要和分类打标等任务。[使用方法](https://help.aliyun.com/zh/model-studio/long-context-qwen-long#72cee64e7ff13) | [在线体验](https://bailian.console.aliyun.com/#/model-market/detail/qwen-long)

#### **中国内地**

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen-long** > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 稳定版 | 10,000,000 | 10,000,000 | 32,768 | 0.5元 | 2元  | 各100万Token 有效期：百炼开通后90天内 |
| **qwen-long-latest** > 始终与最新快照版能力相同 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 最新版 |
| qwen-long-2025-01-25 > 又称qwen-long-0125 | 快照版 | 0.5元 | 2元  |

### **千问Omni**

Qwen-Omni 模型能够接收文本、图片、音频、视频等多种模态的组合输入，并生成文本或语音形式的回复， 提供多种拟人音色，支持多语言和方言的语音输出，可应用于文本创作、视觉识别、语音助手等场景。[使用方法](https://help.aliyun.com/zh/model-studio/qwen-omni)｜[API 参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)

#### **中国内地**

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **模式** | **上下文长度** | **最大输入** | **最长思维链** | **最大输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   |
| **qwen3.5-omni-plus** > 当前与qwen3.5-omni-plus-2026-03-15能力相同 | 稳定版 | 非思考模式 | 262,144 | 196,608 | \\- | 65,536 | 各100万Token（不区分模态） 有效期：百炼开通后90天内 |
| qwen3.5-omni-plus-2026-03-15 | 快照版 | 非思考模式 | 262,144 | 196,608 | \\- | 65,536 |
| **qwen3.5-omni-flash** > 当前与qwen3.5-omni-flash-2026-03-15能力相同 | 稳定版 | 非思考模式 | 262,144 | 196,608 | \\- | 65,536 |
| qwen3.5-omni-flash-2026-03-15 | 快照版 | 非思考模式 | 262,144 | 196,608 | \\- | 65,536 |
| **qwen3-omni-flash** > 当前与qwen3-omni-flash-2025-12-01能力相同 | 稳定版 | 思考模式 | 65,536 | 16,384 | 32,768 | 16,384 |
| 非思考模式 | 49,152 | \\- |
| qwen3-omni-flash-2025-12-01 | 快照版 | 思考模式 | 65,536 | 16,384 | 32,768 | 16,384 |
| 非思考模式 | 49,152 | \\- |
| qwen3-omni-flash-2025-09-15 > 又称qwen3-omni-flash-0915 | 思考模式 | 65,536 | 16,384 | 32,768 | 16,384 |
| 非思考模式 | 49,152 | \\- |

免费额度用完后，输入与输出的计费规则如下：

##### **Qwen3.5-Omni-Plus**

当输入为文本、图片或视频时，采取阶梯计费。

| \\| **输入计费项** \\| **单次请求的输入Token数** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| --- \\| \\| 输入：文本/图片/视频 \\| 0<Token≤128K \\| 0.8元 \\| \\| 128<Token≤256K \\| 2元 \\| \\| 输入：音频 \\| \\\\- \\| 4.96元 \\| | \\| **输出计费项** \\| **单次请求的输入Token数** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| --- \\| \\| 输出：文本 \\| 0<Token≤128K \\| 9.6元 \\| \\| 128<Token≤256K \\| 24元 \\| \\| 输出：文本+音频 \\| \\\\- \\| 61.322元 > 输出的文本不计费。 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

##### **Qwen3.5-Omni-Flash**

当输入为文本、图片或视频时，采取阶梯计费。

| \\| **输入计费项** \\| **单次请求的输入Token数** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| --- \\| \\| 输入：文本/图片/视频 \\| 0<Token≤128K \\| 0.2元 \\| \\| 128<Token≤256K \\| 0.8元 \\| \\| 输入：音频 \\| \\\\- \\| 1.24元 \\| | \\| **输出计费项** \\| **单次请求的输入Token数** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| --- \\| \\| 输出：文本 \\| 0<Token≤128K \\| 4元 \\| \\| 128<Token≤256K \\| 16元 \\| \\| 输出：文本+音频 \\| \\\\- \\| 25.551元 > 输出的文本不计费。 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

##### Qwen3-Omni-Flash

思考与非思考模式的计费相同，且思考模式下不支持输出音频。

| \\| **输入计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输入：文本 \\| 1.8元 \\| \\| 输入：音频 \\| 15.8元 \\| \\| 输入：图片/视频 \\| 3.3元 \\| | \\| **输出计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输出：文本 \\| 6.9元（输入仅包含文本时） 12.7元（输入包含图片/视频/音频时） \\| \\| 输出：文本+音频 > 思考模式下无此项计费 \\| 62.6元（音频） > 输出的文本不计费。 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

**更多模型**

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |
| **qwen-omni-turbo** > 当前与qwen-omni-turbo-2025-03-26能力相同 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 稳定版 | 32,768 | 30,720 | 2,048 | 各100万Token（不区分模态） 有效期：百炼开通后90天内 |
| **qwen-omni-turbo-latest** > 始终与最新快照版 能力相同 | 最新版 |
| qwen-omni-turbo-2025-03-26 > 又称qwen-omni-turbo-0326 | 快照版 |
| qwen-omni-turbo-2025-01-19 > 又称qwen-omni-turbo-0119 |

免费额度用完后，输入与输出的计费规则如下，思考与非思考模式的计费相同，且思考模式下不支持输出音频。

| \\| **输入计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输入：文本 \\| 0.4元 \\| \\| 输入：音频 \\| 25元 \\| \\| 输入：图片/视频 \\| 1.5元 \\| | \\| **输出计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输出：文本 \\| 1.6元（输入仅包含文本时） 4.5元（输入包含图片/视频/音频时） \\| \\| 输出：文本+音频 > 思考模式下无此项计费 \\| 50元（音频） > 输出的文本不计费。 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **版本** | **模式** | **上下文长度** | **最大输入** | **最长思维链** | **最大输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   |
| **qwen3.5-omni-plus** > 当前与qwen3.5-omni-plus-2026-03-15能力相同 | 稳定版 | 非思考模式 | 262,144 | 196,608 | \\- | 65,536 | 无免费额度 |
| qwen3.5-omni-plus-2026-03-15 | 快照版 | 非思考模式 | 262,144 | 196,608 | \\- | 65,536 |
| **qwen3.5-omni-flash** > 当前与qwen3.5-omni-flash-2026-03-15能力相同 | 稳定版 | 非思考模式 | 262,144 | 196,608 | \\- | 65,536 |
| qwen3.5-omni-flash-2026-03-15 | 快照版 | 非思考模式 | 262,144 | 196,608 | \\- | 65,536 |
| **qwen3-omni-flash** > 当前与qwen3-omni-flash-2025-12-01能力相同 | 稳定版 | 思考模式 | 65,536 | 16,384 | 32,768 | 16,384 |
| 非思考模式 | 49,152 | \\- |
| qwen3-omni-flash-2025-12-01 | 快照版 | 思考模式 | 65,536 | 16,384 | 32,768 | 16,384 |
| 非思考模式 | 49,152 | \\- |
| qwen3-omni-flash-2025-09-15 > 又称qwen3-omni-flash-0915 | 快照版 | 思考模式 | 65,536 | 16,384 | 32,768 | 16,384 |
| 非思考模式 | 49,152 | \\- |

##### **Qwen3.5-Omni-Plus**

当输入为文本、图片或视频时，采取阶梯计费。

| \\| **输入计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输入：文本/图片/视频 \\| 2.998元 \\| \\| 输入：音频 \\| 18.878元 \\| | \\| **输出计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输出：文本 \\| 35.972元 \\| \\| 输出：文本+音频 \\| 230.313元 > 输出的文本不计费 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

##### **Qwen3.5-Omni-Flash**

当输入为文本、图片或视频时，采取阶梯计费。

| \\| **输入计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输入：文本/图片/视频 \\| 0.749元 \\| \\| 输入：音频 \\| 4.719元 \\| | \\| **输出计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输出：文本 \\| 5.995元 \\| \\| 输出：文本+音频 \\| 38.386元 > 输出的文本不计费 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

##### Qwen3-Omni-Flash

| \\| 输入计费项 \\| 单价（每百万Token） \\| \\| --- \\| --- \\| \\| 输入：文本 \\| 3.156元 \\| \\| 输入：音频 \\| 27.962元 \\| \\| 输入：图片/视频 \\| 3.3元 \\| | \\| **输出计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输出：文本 \\| 12.183元（输入仅包含文本时） 22.458元（输入包含图片/视频/音频时） \\| \\| 输出：文本+音频 \\| 110.896元（音频） > 输出的文本不计费。 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

**更多模型**

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |
| **qwen-omni-turbo** > 当前与qwen-omni-turbo-2025-03-26能力相同 | 稳定版 | 32,768 | 30,720 | 2,048 | 无免费额度 |
| **qwen-omni-turbo-latest** > 始终与最新快照版 > 能力相同 | 最新版 |
| qwen-omni-turbo-2025-03-26 > 又称qwen-omni-turbo-0326 | 快照版 |

商业版模型的免费额度用完后，输入与输出的计费规则如下：

| \\| 输入计费项 \\| 单价（每百万Token） \\| \\| --- \\| --- \\| \\| 输入：文本 \\| 0.514元 \\| \\| 输入：音频 \\| 32.586元 \\| \\| 输入：图片/视频 \\| 1.541元 \\| | \\| 输出计费项 \\| 单价（每百万Token） \\| \\| --- \\| --- \\| \\| 输出：文本 \\| 1.982元（输入仅包含文本时） 4.624元（输入包含图片/视频/音频时） \\| \\| 输出：文本+音频 \\| 65.246元（音频） > 输出的文本不计费。 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

### **千问Omni-Realtime**

相比于[千问Omni](https://help.aliyun.com/zh/model-studio/models#5e79514e7cqp5)，支持音频的流式输入，且内置 VAD（Voice Activity Detection，语音活动检测）功能，可自动检测用户语音的开始和结束。[使用方法](https://help.aliyun.com/zh/model-studio/realtime)｜[客户端事件](https://help.aliyun.com/zh/model-studio/client-events)｜[服务端事件](https://help.aliyun.com/zh/model-studio/server-events)｜[在线体验](https://help.aliyun.com/zh/model-studio/realtime#14a119f447ehf)

#### **中国内地**

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |
| **qwen3.5-omni-plus-realtime** > 当前与qwen3.5-omni-plus-realtime-2026-03-15能力相同 | 稳定版 | 262,144 | 196,608 | 65,536 | 各100万Token（不区分模态） 有效期：百炼开通后90天内 |
| qwen3.5-omni-plus-realtime-2026-03-15 | 快照版 | 262,144 | 196,608 | 65,536 |
| **qwen3.5-omni-flash-realtime** > 当前与qwen3.5-omni-flash-realtime-2026-03-15能力相同 | 稳定版 | 262,144 | 196,608 | 65,536 |
| qwen3.5-omni-flash-realtime-2026-03-15 | 快照版 | 262,144 | 196,608 | 65,536 |
| **qwen3-omni-flash-realtime** > 当前与qwen3-omni-flash-realtime**\\-**2025-12-01能力相同 | 稳定版 | 65,536 | 49,152 | 16,384 |
| qwen3-omni-flash-realtime**\\-**2025-12-01 | 快照版 |
| qwen3-omni-flash-realtime**\\-**2025-09-15 |

##### **Qwen3.5-Omni-Plus-Realtime**

当输入为文本、图片时，采取阶梯计费。

| \\| **输入计费项** \\| **单次会话的输入Token数** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| --- \\| \\| 输入：文本/图片 \\| 0<Token≤128K \\| 0.96元 \\| \\| \\\\>128K \\| 2.4元 \\| \\| 输入：音频 \\| \\\\- \\| 5.95元 \\| | \\| **输出计费项** \\| **单次会话的输入Token数** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| --- \\| \\| 输出：文本 \\| 0<Token≤128K \\| 11.52元 \\| \\| \\\\>128K \\| 28.8元 \\| \\| 输出：文本+音频 \\| \\\\- \\| 73.587元 > 输出的文本不计费 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

##### **Qwen3.5-Omni-Flash-Realtime**

当输入为文本、图片时，采取阶梯计费。

| \\| **输入计费项** \\| **单次会话的输入Token数** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| --- \\| \\| 输入：文本/图片 \\| 0<Token≤128K \\| 0.24元 \\| \\| \\\\>128K \\| 0.96元 \\| \\| 输入：音频 \\| \\\\- \\| 1.49元 \\| | \\| **输出计费项** \\| **单次会话的输入Token数** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| --- \\| \\| 输出：文本 \\| 0<Token≤128K \\| 4.8元 \\| \\| \\\\>128K \\| 19.2元 \\| \\| 输出：文本+音频 \\| \\\\- \\| 30.661元 > 输出的文本不计费 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

##### Qwen3-Omni-Flash**\-Realtime**

思考与非思考模式的计费相同，且思考模式下不支持输出音频。

| \\| **输入计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输入：文本 \\| 2.2元 \\| \\| 输入：音频 \\| 18.9元 \\| \\| 输入：图片 \\| 3.9元 \\| | \\| **输出计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输出：文本 \\| 8.3元（输入仅包含文本时） 15.2元（输入包含图片/音频时） \\| \\| 输出：文本+音频 \\| 75.1元（音频） > 输出的文本不计费。 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

**更多模型**

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |
| **qwen-omni-turbo-realtime** > 当前能力等同 qwen-omni-turbo-realtime**\\-**2025-05-08 | 稳定版 | 32,768 | 30,720 | 2,048 | 各100万Token（不区分模态） 有效期：百炼开通后90天内 |
| **qwen-omni-turbo-realtime-latest** > 能力始终等同最新快照版 | 最新版 |
| qwen-omni-turbo-realtime**\\-**2025-05-08 | 快照版 |

免费额度用完后，输入与输出的计费规则如下：

| \\| **输入计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输入：文本 \\| 1.6元 \\| \\| 输入：音频 \\| 25元 \\| \\| 输入：图片 \\| 6元 \\| | \\| **输出计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输出：文本 \\| 6.4元（输入仅包含文本时） 18元（输入包含图片/音频时） \\| \\| 输出：文本+音频 \\| 50元（音频） > 输出的文本不计费。 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |
| **qwen3.5-omni-plus-realtime** > 当前与qwen3.5-omni-plus-realtime-2026-03-15能力相同 | 稳定版 | 262,144 | 196,608 | 65,536 | 无免费额度 |
| qwen3.5-omni-plus-realtime-2026-03-15 | 快照版 | 262,144 | 196,608 | 65,536 |
| **qwen3.5-omni-flash-realtime** > 当前与qwen3.5-omni-flash-realtime-2026-03-15能力相同 | 稳定版 | 262,144 | 196,608 | 65,536 |
| qwen3.5-omni-flash-realtime-2026-03-15 | 快照版 | 262,144 | 196,608 | 65,536 |
| **qwen3-omni-flash-realtime** > 当前与qwen3-omni-flash-realtime**\\-**2025-12-01能力相同 | 稳定版 | 65,536 | 49,152 | 16,384 |
| qwen3-omni-flash-realtime**\\-**2025-12-01 | 快照版 |
| qwen3-omni-flash-realtime**\\-**2025-09-15 |

##### **Qwen3.5-Omni-Plus**\-**Realtime**

当输入为文本、图片，采取阶梯计费。

| \\| **输入计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输入：文本/图片 \\| 3.597元 \\| \\| 输入：音频 \\| 22.654元 \\| | \\| **输出计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输出：文本 \\| 43.167元 \\| \\| 输出：文本+音频 \\| 276.376元 > 输出的文本不计费 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

##### **Qwen3.5-Omni-Flash**\-**Realtime**

当输入为文本、图片时，采取阶梯计费。

| \\| **输入计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输入：文本/图片 \\| 0.899元 \\| \\| 输入：音频 \\| 5.663元 \\| | \\| **输出计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输出：文本 \\| 7.194元 \\| \\| 输出：文本+音频 \\| 46.063元 > 输出的文本不计费 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

##### Qwen3-Omni-Flash-**Realtime**

| \\| 输入计费项 \\| 单价（每百万Token） \\| \\| --- \\| --- \\| \\| 输入：文本 \\| 3.816元 \\| \\| 输入：音频 \\| 33.54元 \\| \\| 输入：图片 \\| 6.899元 \\| | \\| **输出计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输出：文本 \\| 14.605元（输入仅包含文本时） 26.935元（输入包含图片/音频时） \\| \\| 输出：文本+音频 \\| 133.06元（音频） > 输出的文本不计费。 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

**更多模型**

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |
| **qwen-omni-turbo-realtime** > 当前能力等同 qwen-omni-turbo-realtime**\\-**2025-05-08 | 稳定版 | 32,768 | 30,720 | 2,048 | 无免费额度 |
| **qwen-omni-turbo-realtime-latest** > 能力始终等同最新快照版 | 最新版 |
| qwen-omni-turbo-realtime**\\-**2025-05-08 | 快照版 |

输入与输出的计费规则如下：

| \\| **输入计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输入：文本 \\| 1.982元 \\| \\| 输入：音频 \\| 32.586元 \\| \\| 输入：图片 \\| 6.165元 \\| | \\| **输出计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输出：文本 \\| 7.853元（输入仅包含文本时） 18.495元（输入包含图片/音频时） \\| \\| 输出：文本+音频 \\| 65.246元（音频） > 输出的文本不计费。 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

### **QVQ**

QVQ是视觉推理模型，支持视觉输入及思维链输出，在数学、编程、视觉分析、创作以及通用任务上都表现了更强的能力。[使用方法](https://help.aliyun.com/zh/model-studio/visual-reasoning) | [在线体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/vision?currentTab=imageComprehend&modelId=qvq-max)

#### **中国内地**

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| **qvq-max** > 相比 qvq-plus 具有更强的视觉推理和指令遵循能力，在更多复杂任务中提供最佳性能。 > 当前与qvq-max-2025-03-25能力相同 | 稳定版 | 131,072 | 106,496 > 单图最大16384 | 16,384 | 8,192 | 8元  | 32元 | 各100万 Token 有效期：百炼开通后90天内 |
| **qvq-max-latest** > 始终与最新快照版能力相同 | 最新版 |
| qvq-max-2025-05-15 > 又称qvq-max-0515 | 快照版 |
| qvq-max-2025-03-25 > 又称qvq-max-0325 |
| **qvq-plus** > 当前与qvq-plus-2025-05-15能力相同 | 稳定版 | 2元  | 5元  |
| **qvq-plus-latest** > 始终与最新快照版能力相同 | 最新版 |
| qvq-plus-2025-05-15 > 又称qvq-plus-0515 | 快照版 |

#### 国际

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| **qvq-max** > 当前与 qvq-max-2025-03-25能力相同 | 稳定版 | 131,072 | 106,496 > 单图最大16384 | 16,384 | 8,192 | 8.807元 | 35.228元 | 无免费额度 |
| **qvq-max-latest** > 始终与最新快照版能力相同 | 最新版 |
| qvq-max-2025-03-25 > 又称qvq-max-0325 | 快照版 |

### 千问VL

千问VL是具有视觉（图像）理解能力的文本生成模型，不仅能进行OCR（图片文字识别），还能进一步总结和推理，例如从商品照片中提取属性，根据习题图进行解题等。[使用方法](https://help.aliyun.com/zh/model-studio/vision) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/#cde3eb109flda) | [在线体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/vision?currentTab=imageComprehend&modelId=qwen3-vl-plus)

> 千问VL模型按输入和输出的总Token数进行计费。图像Token的计算规则请参见[图像与视频理解](https://help.aliyun.com/zh/model-studio/vision#7487c7f6eakzl)。

#### **中国内地**

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **模式** | **上下文长度** | **最大输入** | **最长思维链** | **最大输出** | **输入成本** | **输出成本** > **思维链+输出** | **免费额度** [**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| **qwen3-vl-plus** > 当前与qwen3-vl-plus-2025-12-19能力相同 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 稳定版 | 思考  | 262,144 | 258,048 > 单图最大16384 | 81,920 | 32,768 | 阶梯计价，请参见表格下方说明。 |   | 各100万Token 有效期：百炼开通后90天内 |
| 非思考 | 260,096 > 单图最大16384 | \\- |
| qwen3-vl-plus-2025-12-19 | 快照版 | 思考  | 258,048 > 单图最大16384 | 81,920 |
| 非思考 | 260,096 > 单图最大16384 | \\- |
| qwen3-vl-plus-2025-09-23 | 快照版 | 思考  | 258,048 > 单图最大16384 | 81,920 |
| 非思考 | 260,096 > 单图最大16384 | \\- |
| **qwen3-vl-flash** > 当前与qwen3-vl-flash-2025-10-15能力相同 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 稳定版 | 思考  | 258,048 > 单图最大16384 | 81,920 |
| 非思考 | 260,096 > 单图最大16384 | \\- |
| qwen3-vl-flash-2026-01-22 | 快照版 | 思考  | 258,048 > 单图最大16384 | 81,920 |
| 非思考 | 260,096 > 单图最大16384 | \\- |
| qwen3-vl-flash-2025-10-15 | 快照版 | 思考  | 258,048 > 单图最大16384 | 81,920 |
| 非思考 | 260,096 > 单图最大16384 | \\- |

以上模型根据本次请求输入的 Token数，采取阶梯计费。思考模式与非思考模式的输入输出价格相同，其中`qwen3-vl-plus`和`qwen3-vl-flash`模型支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。

##### **qwen3-vl-plus**系列

| **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- |
| 0<Token≤32K | 1元  | 10元 |
| 32K<Token≤128K | 1.5元 | 15元 |
| 128K<Token≤256K | 3元  | 30元 |

##### **qwen3-vl-flash系列**

| **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- |
| 0<Token≤32K | 0.15元 | 1.5元 |
| 32K<Token≤128K | 0.3元 | 3元  |
| 128K<Token≤256K | 0.6元 | 6元  |

**更多模型**

##### 千问VL-Max系列

> `qwen-vl-max-2025-01-25`及以后更新的模型均属于[Qwen2.5-VL](https://qwenlm.github.io/blog/qwen2.5-vl/)系列，其中`qwen-vl-max`模型支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen-vl-max** > 相比qwen-vl-plus再次提升视觉推理和指令遵循能力，在更多复杂任务中提供**最佳性能**。 > 当前与qwen-vl-max-2025-08-13能力相同 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 稳定版 | 131,072 | 129,024 > 单图最大16384 | 8,192 | 1.6元 | 4元  | 各100万Token 有效期：百炼开通后90天内 |
| **qwen-vl-max-latest** > 始终与最新快照版能力相同 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 最新版 |
| qwen-vl-max-2025-08-13 > 又称qwen-vl-max-0813 > 视觉理解指标全面提升，数学、推理、物体识别、多语言处理能力显著增强。 | 快照版 | 1.6元 | 4元  |
| qwen-vl-max-2025-04-08 > 又称qwen-vl-max-0408 > 增强数学和推理能力 | 3元  | 9元  |
| qwen-vl-max-2025-04-02 > 又称qwen-vl-max-0402 > 显著提高解决复杂数学问题的准确性 |
| qwen-vl-max-2025-01-25 > 又称qwen-vl-max-0125 > 升级至[Qwen2.5-VL](https://qwenlm.github.io/blog/qwen2.5-vl/)系列，扩展上下文至128k，显著增强图像和视频的理解能力 |
| qwen-vl-max-2024-12-30 > 又称qwen-vl-max-1230 | 32,768 | 30,720 > 单图最大16384 | 2,048 | 3元  | 9元  |
| qwen-vl-max-2024-11-19 > 又称qwen-vl-max-1119 |

##### 千问VL-Plus系列

> `qwen-vl-plus-2025-01-25`及以后更新的模型均属于[Qwen2.5-VL](https://qwenlm.github.io/blog/qwen2.5-vl/)系列，其中`qwen-vl-plus`模型支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen-vl-plus** > 当前与qwen-vl-plus-2025-08-15能力相同 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 稳定版 | 131,072 | 129,024 > 单图最大16384 | 8,192 | 0.8元 | 2元  | 各100万Token 有效期：百炼开通后90天内 |
| **qwen-vl-plus-latest** > 始终与最新快照版能力相同 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 最新版 |
| qwen-vl-plus-2025-08-15 > 又称qwen-vl-plus-0815 > 在物体识别与定位、多语言处理的能力上有显著提升 | 快照版 | 0.8元 | 2元  |
| qwen-vl-plus-2025-07-10 > 又称qwen-vl-plus-0710 > 进一步提升监控视频内容的理解能力 | 32,768 | 30,720 > 单图最大16384 | 0.15元 | 1.5元 |
| qwen-vl-plus-2025-05-07 > 又称qwen-vl-plus-0507 > 显著提升数学、推理、监控视频内容的理解能力 | 131,072 | 129,024 > 单图最大16384 | 1.5元 | 4.5元 |
| qwen-vl-plus-2025-01-25 > 又称qwen-vl-plus-0125 > 升级至[Qwen2.5-VL](https://qwenlm.github.io/blog/qwen2.5-vl/)系列，扩展上下文至128k，显著增强图像和视频理解能力 |
| qwen-vl-plus-2025-01-02 > 又称qwen-vl-plus-0102 | 32,768 | 30,720 > 单图最大16384 | 2,048 | 1.5元 | 4.5元 |

#### 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **版本** | **模式** | **上下文长度** | **最大输入** | **最长思维链** | **最大输出** | **输入成本** | **输出成本** > **思维链+输出** | **免费额度** [**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| **qwen3-vl-plus** > 当前与qwen3-vl-plus-2025-12-19能力相同 | 稳定版 | 思考  | 262,144 | 258,048 > 单图最大16384 | 81,920 | 32,768 | 阶梯计价，请参见表格下方说明。 |   | 无免费额度 |
| 非思考 | 260,096 > 单图最大16384 | \\- |
| qwen3-vl-plus-2025-09-23 | 快照版 | 思考  | 258,048 > 单图最大16384 | 81,920 |
| 非思考 | 260,096 > 单图最大16384 | \\- |
| **qwen3-vl-flash** > 当前与qwen3-vl-flash-2025-10-15能力相同 | 稳定版 | 思考  | 258,048 > 单图最大16384 | 81,920 |
| 非思考 | 260,096 > 单图最大16384 | \\- |
| qwen3-vl-flash-2025-10-15 | 快照版 | 思考  | 258,048 > 单图最大16384 | 81,920 |
| 非思考 | 260,096 > 单图最大16384 | \\- |

以上模型根据本次请求输入的 Token数，采取阶梯计费。思考模式与非思考模式的输入输出价格相同，其中`qwen3-vl-plus`和`qwen3-vl-flash`模型支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。

##### **qwen3-vl-plus**系列

| **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- |
| 0<Token≤32K | 1元  | 10元 |
| 32K<Token≤128K | 1.5元 | 15元 |
| 128K<Token≤256K | 3元  | 30元 |

##### **qwen3-vl-flash系列**

| **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- |
| 0<Token≤32K | 0.15元 | 1.5元 |
| 32K<Token≤128K | 0.3元 | 3元  |
| 128K<Token≤256K | 0.6元 | 6元  |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **版本** | **模式** | **上下文长度** | **最大输入** | **最长思维链** | **最大输出** | **输入成本** | **输出成本** > **思维链+输出** | **免费额度** [**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| **qwen3-vl-plus** > 当前与qwen3-vl-plus-2025-12-19能力相同 | 稳定版 | 思考  | 262,144 | 258,048 > 单图最大16384 | 81,920 | 32,768 | 阶梯计价，请参见表格下方说明。 |   | 无免费额度 |
| 非思考 | 260,096 > 单图最大16384 | \\- |
| qwen3-vl-plus-2025-12-19 | 快照版 | 思考  | 258,048 > 单图最大16384 | 81,920 |
| 非思考 | 260,096 > 单图最大16384 | \\- |
| qwen3-vl-plus-2025-09-23 | 快照版 | 思考  | 258,048 > 单图最大16384 | 81,920 |
| 非思考 | 260,096 > 单图最大16384 | \\- |
| **qwen3-vl-flash** > 当前与qwen3-vl-flash-2025-10-15能力相同 | 稳定版 | 思考  | 258,048 > 单图最大16384 | 81,920 |
| 非思考 | 260,096 > 单图最大16384 | \\- |
| qwen3-vl-flash-2026-01-22 | 快照版 | 思考  | 258,048 > 单图最大16384 | 81,920 |
| 非思考 | 260,096 > 单图最大16384 | \\- |
| qwen3-vl-flash-2025-10-15 | 快照版 | 思考  | 258,048 > 单图最大16384 | 81,920 |
| 非思考 | 260,096 > 单图最大16384 | \\- |

以上模型根据本次请求输入的 Token数，采取阶梯计费。思考模式与非思考模式的输入输出价格相同，其中`qwen3-vl-plus`和`qwen3-vl-flash`模型支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。

##### **qwen3-vl-plus**系列

| **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- |
| 0<Token≤32K | 1.468元 | 11.743元 |
| 32K<Token≤128K | 2.202元 | 17.614 元 |
| 128K<Token≤256K | 4.404元 | 35.228元 |

##### **qwen3-vl-flash系列**

| **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- |
| 0<Token≤32K | 0.367元 | 2.936元 |
| 32K<Token≤128K | 0.55元 | 4.404元 |
| 128K<Token≤256K | 0.881元 | 7.046元 |

**更多模型**

##### 千问VL-Max系列

> 以下模型均属于[Qwen2.5-VL](https://qwenlm.github.io/blog/qwen2.5-vl/)系列，其中`qwen-vl-max`模型支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen-vl-max** > 相比qwen-vl-plus再次提升视觉推理和指令遵循能力，在更多复杂任务中提供最佳性能。 > 当前与qwen-vl-max-2025-08-13能力相同 | 稳定版 | 131,072 | 129,024 > 单图最大16384 | 8,192 | 5.871元 | 23.486元 | 无免费额度 |
| **qwen-vl-max-latest** > 始终与最新快照版能力相同 | 最新版 | 5.871元 | 23.486元 |
| qwen-vl-max-2025-08-13 > 又称qwen-vl-max-0813 > 视觉理解指标全面提升，数学、推理、物体识别、多语言处理能力显著增强。 | 快照版 |
| qwen-vl-max-2025-04-08 > 又称qwen-vl-max-0408 > 属于[Qwen2.5-VL](https://qwenlm.github.io/blog/qwen2.5-vl/)系列模型，扩展上下文至128k，显著增强数学和推理能力。 |

##### 千问VL-Plus系列

> 以下模型均属于[Qwen2.5-VL](https://qwenlm.github.io/blog/qwen2.5-vl/)系列，其中`qwen-vl-plus`模型支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen-vl-plus** > 当前与qwen-vl-plus-2025-08-15能力相同 | 稳定版 | 131,072 | 129,024 > 单图最大16384 | 8,192 | 1.541元 | 4.624元 | 无免费额度 |
| **qwen-vl-plus-latest** > 始终与最新快照版能力相同 | 最新版 | 1.541元 | 4.624元 |
| qwen-vl-plus-2025-08-15 > 又称qwen-vl-plus-0815 > 在物体识别与定位、多语言处理的能力上有显著提升 | 快照版 |
| qwen-vl-plus-2025-05-07 > 又称qwen-vl-plus-0507 > 显著提升数学、推理、监控视频内容的理解能力 |
| qwen-vl-plus-2025-01-25 > 又称qwen-vl-plus-0125 > 属于[Qwen2.5-VL](https://qwenlm.github.io/blog/qwen2.5-vl/)系列模型，扩展上下文至128k，显著增强图像和视频的理解能力。 |

> qwen3-vl-flash-2026-01-22模型有效融合了思考模式与非思考模式，相较于 2025 年 10 月 15 日的快照版本，显著提升了模型的整体性能，在通用视觉识别、安防、巡店、巡检、拍照解题等业务场景中实现了更高准确率的推理。

#### 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

| **模型名称** | **版本** | **模式** | **上下文长度** | **最大输入** | **最长思维链** | **最大输出** | **输入成本** | **输出成本** > **思维链+输出** | **免费额度** [**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| **qwen3-vl-flash-us** > 当前与qwen3-vl-flash-2025-10-15-us能力相同 | 稳定版 | 思考  | 262,144 | 258,048 > 单图最大16384 | 81,920 | 32,768 | 阶梯计价，请参见表格下方说明。 | 无免费额度 |
| 非思考 | 260,096 > 单图最大16384 | \\- |
| qwen3-vl-flash-2025-10-15-us | 快照版 | 思考  | 258,048 > 单图最大16384 | 81,920 |
| 非思考 | 260,096 > 单图最大16384 | \\- |

以上模型根据本次请求输入的 Token数，采取阶梯计费。思考模式与非思考模式的输入输出价格相同，其中`qwen3-vl-flash-us`模型支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)。

| **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- |
| 0<Token≤32K | 0.367元 | 2.936元 |
| 32K<Token≤128K | 0.55元 | 4.404元 |
| 128K<Token≤256K | 0.881元 | 7.046元 |

> qwen3-vl-flash-2026-01-22模型有效融合了思考模式与非思考模式，相较于 2025 年 10 月 15 日的快照版本，显著提升了模型的整体性能，在通用视觉识别、安防、巡店、巡检、拍照解题等业务场景中实现了更高准确率的推理。

### 千问OCR

千问OCR模型是专用于文字提取的模型。相较于千问VL模型，它更专注于文档、表格、试题、手写体文字等类型图像的文字提取能力。它能够识别多种语言，包括英语、法语、日语、韩语、德语、俄语和意大利语等。[使用方法](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr-api-reference)｜[在线体验](https://bailian.console.aliyun.com/#/model-market/detail/qwen-vl-ocr)

#### **中国内地**

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入单价** | **输出单价** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen-vl-ocr** > 当前与qwen-vl-ocr-2025-11-20能力相同 > [Batch 调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 稳定版 | 38,192 | 30,000 > 单图最大30000 | 8,192 | 0.3元 | 0.5元 | 各100万Token 有效期：百炼开通后90天内 |
| **qwen-vl-ocr-latest** > 始终与最新版能力相同 > [Batch 调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 最新版 |
| qwen-vl-ocr-2025-11-20 > 基于Qwen3-VL架构，大幅提升文档解析、文字定位能力。 | 快照版 |
| qwen-vl-ocr-2025-08-28 > 又称qwen-vl-ocr-0828 | 34,096 | 4,096 | 5元  | 5元  |
| qwen-vl-ocr-2025-04-13 > 又称qwen-vl-ocr-0413 |
| qwen-vl-ocr-2024-10-28 > 又称qwen-vl-ocr-1028 |

#### 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入单价** | **输出单价** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen-vl-ocr** > 当前与qwen-vl-ocr-2025-11-20能力相同 | 稳定版 | 38,192 | 30,000 > 单图最大30000 | 8,192 | 0.3元 | 0.5元 | 无免费额度 |
| qwen-vl-ocr-2025-11-20 > 又称qwen-vl-ocr-1120 > 基于Qwen3-VL架构，大幅提升文档解析、文字定位能力。 | 快照版 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入单价** | **输出单价** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen-vl-ocr** > 当前与qwen-vl-ocr-2025-11-20能力相同 | 稳定版 | 38,192 | 30,000 > 单图最大30000 | 8,192 | 0.514元 | 1.174元 | 无免费额度 |
| qwen-vl-ocr-2025-11-20 > 又称qwen-vl-ocr-1120 > 基于Qwen3-VL架构，大幅提升文档解析、文字定位能力。 | 快照版 |

### 千问Audio

千问Audio是音频理解模型，支持输入多种音频（人类语音、自然音、音乐、歌声）和文本，并输出文本。该模型不仅能对输入的音频进行转录，还具备更深层次的语义理解、情感分析、音频事件检测等能力。[使用方法](https://help.aliyun.com/zh/model-studio/audio-language-model)

> 千问Audio模型按输入和输出的总Token数进行计费。

> 音频转换为Token的规则：每一秒钟的音频对应25个Token。若音频时长不足1秒，则按25个Token计算。

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| qwen-audio-turbo | 稳定版 | 8,000 | 6,000 | 1,500 | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐使用[Qwen-Omni](https://help.aliyun.com/zh/model-studio/qwen-omni)作为替代模型 |   | 10万Token 有效期：阿里云百炼开通后90天内 |
| qwen-audio-turbo-latest | 最新版 | 8,192 | 6,144 | 2,048 |

### 千问数学模型

千问数学模型是专门用于数学解题的语言模型。[使用方法](https://help.aliyun.com/zh/model-studio/math-language-model) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/) | [在线体验](https://bailian.console.aliyun.com/#/model-market/detail/qwen-math-plus)

**说明**

仅支持中国内地（北京）地域。

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输入价格** | **输出价格** | **上下文长度** | **最大输入** | **最大输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（每百万Token）** |   | **（Token数）** |   |   |
| **qwen-math-plus** | 4元  | 12元 | 4,096 | 3,072 | 3,072 | 各100万Token 有效期：百炼开通后90天内 |
| **qwen-math-turbo** | 2元  | 6元  |

### 千问Coder

千问代码模型。最新的 Qwen3-Coder-Plus 系列模型是基于 Qwen3 的代码生成模型，具有强大的Coding Agent能力，擅长工具调用和环境交互，能够实现自主编程，代码能力卓越的同时兼具通用能力。[使用方法](https://help.aliyun.com/zh/model-studio/qwen-coder) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/) | [在线体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/text?currentTab=textChat&modelId=qwen3-coder-plus)

#### **中国内地**

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen3-coder-plus** > 当前与qwen3-coder-plus-2025-09-23能力相同 | 稳定版 | 1,000,000 | 997,952 | 65,536 | 阶梯计价，请参见表格下方说明。 |   | 各100万Token 有效期：百炼开通后90天内 |
| qwen3-coder-plus-2025-09-23 | 快照版 |
| qwen3-coder-plus-2025-07-22 | 快照版 |
| **qwen3-coder-flash** > 当前与qwen3-coder-flash-2025-07-28能力相同 | 稳定版 |
| qwen3-coder-flash-2025-07-28 | 快照版 |

上述模型根据本次请求输入的Token数，采取阶梯计费。

##### qwen3-coder-plus系列

qwen3-coder-plus、qwen3-coder-plus-2025-09-23和qwen3-coder-plus-2025-07-22价格如下，其中 qwen3-coder-plus 支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)，命中**隐式缓存**的输入文本按单价的 20% 计费，命中**显式缓存**的输入文本按单价的 10% 计费。

| **单次请求的输入Token数** | **输入成本（每百万Token）** | **输出成本（每百万Token）** |
| --- | --- | --- |
| 0<Token≤32K | 4元  | 16元 |
| 32K<Token≤128K | 6元  | 24元 |
| 128K<Token≤256K | 10元 | 40元 |
| 256K<Token≤1M | 20元 | 200元 |

##### qwen3-coder-flash系列

qwen3-coder-flash 和 qwen3-coder-flash-2025-07-28 价格如下，其中 qwen3-coder-flash 支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)，命中**隐式缓存**的输入文本按单价的 20% 计费，命中**显式缓存**的输入文本按单价的 10% 计费。

| **单次请求的输入Token数** | **输入成本（每百万Token）** | **输出成本（每百万Token）** |
| --- | --- | --- |
| 0<Token≤32K | 1元  | 4元  |
| 32K<Token≤128K | 1.5元 | 6元  |
| 128K<Token≤256K | 2.5元 | 10元 |
| 256K<Token≤1M | 5元  | 25元 |

**更多模型**

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen-coder-plus** > 当前与qwen-coder-plus-2024-11-06能力相同 | 稳定版 | 131,072 | 129,024 | 8,192 | 3.5元 | 7元  | 各100万Token 有效期：百炼开通后90天内 |
| **qwen-coder-plus-latest** > 与qwen-coder-plus的最新快照版能力相同 | 最新版 |
| qwen-coder-plus-2024-11-06 > 又称qwen-coder-plus-1106 | 快照版 |
| **qwen-coder-turbo** > 当前与qwen-coder-turbo-2024-09-19能力相同 | 稳定版 | 131,072 | 129,024 | 8,192 | 2元  | 6元  |
| **qwen-coder-turbo-latest** > 与qwen-coder-turbo的最新快照版能力相同 | 最新版 |
| qwen-coder-turbo-2024-09-19 > 又称qwen-coder-turbo-0919 | 快照版 |

#### 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen3-coder-plus** > 当前与qwen3-coder-plus-2025-09-23能力相同 | 稳定版 | 1,000,000 | 997,952 | 65,536 | 阶梯计价，请参见表格下方说明。 |   | 无免费额度 |
| qwen3-coder-plus-2025-09-23 | 快照版 |
| qwen3-coder-plus-2025-07-22 | 快照版 |
| **qwen3-coder-flash** > 当前与qwen3-coder-flash-2025-07-28能力相同 | 稳定版 |
| qwen3-coder-flash-2025-07-28 | 快照版 |

上述模型根据本次请求输入的Token数，采取阶梯计费。

##### qwen3-coder-plus系列

qwen3-coder-plus、qwen3-coder-plus-2025-09-23 和 qwen3-coder-plus-2025-07-22 价格如下，其中 qwen3-coder-plus 支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)，命中**隐式缓存**的输入文本按单价的 20% 计费，命中**显式缓存**的输入文本按单价的 10% 计费。

| **单次请求的输入Token数** | **输入成本（每百万Token）** | **输出成本（每百万Token）** |
| --- | --- | --- |
| 0<Token≤32K | 4元  | 16元 |
| 32K<Token≤128K | 6元  | 24元 |
| 128K<Token≤256K | 10元 | 40元 |
| 256K<Token≤1M | 20元 | 200元 |

##### qwen3-coder-flash系列

qwen3-coder-flash 和 qwen3-coder-flash-2025-07-28 价格如下，其中 qwen3-coder-flash 支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)，命中**隐式缓存**的输入文本按单价的 20% 计费，命中**显式缓存**的输入文本按单价的 10% 计费。

| **单次请求的输入Token数** | **输入成本（每百万Token）** | **输出成本（每百万Token）** |
| --- | --- | --- |
| 0<Token≤32K | 1元  | 4元  |
| 32K<Token≤128K | 1.5元 | 6元  |
| 128K<Token≤256K | 2.5元 | 10元 |
| 256K<Token≤1M | 5元  | 25元 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen3-coder-plus** > 当前与qwen3-coder-plus-2025-09-23能力相同 | 稳定版 | 1,000,000 | 997,952 | 65,536 | 阶梯计价，请参见表格下方说明。 |   | 无免费额度 |
| qwen3-coder-plus-2025-09-23 | 快照版 |
| qwen3-coder-plus-2025-07-22 | 快照版 |
| **qwen3-coder-flash** > 当前与qwen3-coder-flash-2025-07-28能力相同 | 稳定版 |
| qwen3-coder-flash-2025-07-28 | 快照版 |

上述模型根据本次请求输入的Token数，采取阶梯计费。

##### qwen3-coder-plus系列

qwen3-coder-plus、qwen3-coder-plus-2025-09-23 和 qwen3-coder-plus-2025-07-22 价格如下，其中 qwen3-coder-plus 支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)，命中**隐式缓存**的输入文本按单价的 20% 计费，命中**显式缓存**的输入文本按单价的 10% 计费。

| **单次请求的输入Token数** | **输入成本（每百万Token）** | **输出成本（每百万Token）** |
| --- | --- | --- |
| 0<Token≤32K | 7.339元 | 36.696元 |
| 32K<Token≤128K | 13.211元 | 66.053元 |
| 128K<Token≤256K | 22.018元 | 110.089元 |
| 256K<Token≤1M | 44.035元 | 440.354元 |

##### qwen3-coder-flash系列

qwen3-coder-flash 和 qwen3-coder-flash-2025-07-28 价格如下，其中 qwen3-coder-flash 支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)，命中**隐式缓存**的输入文本按单价的 20% 计费，命中**显式缓存**的输入文本按单价的 10% 计费。

| **单次请求的输入Token数** | **输入成本（每百万Token）** | **输出成本（每百万Token）** |
| --- | --- | --- |
| 0<Token≤32K | 2.202元 | 11.009元 |
| 32K<Token≤128K | 3.67元 | 18.348元 |
| 128K<Token≤256K | 5.871元 | 29.357元 |
| 256K<Token≤1M | 11.743元 | 70.457元 |

### **千问翻译模型**

基于 Qwen 3全面升级的旗舰级翻译大模型，支持92个语种（包括中、英、日、韩、法、西、德、泰、印尼、越、阿等）互译，模型性能和翻译效果全面升级，提供更稳定的术语定制、格式还原度、领域提示能力，让译文更精准、自然。[使用方法](https://help.aliyun.com/zh/model-studio/machine-translation) | [在线体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/text?currentTab=textChat&modelId=qwen-mt-plus)

#### **中国内地**

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen-mt-plus** > 属于[Qwen3-MT](https://bailian.console.aliyun.com/cn-beijing?tab=model#/efm/model_experience_center/text/debug?modelId=qwen-mt-plus) | 16,384 | 8,192 | 8,192 | 1.8元 | 5.4元 | 各100万Token 有效期：百炼开通后90天内 |
| **qwen-mt-flash** > 属于[Qwen3-MT](https://bailian.console.aliyun.com/cn-beijing?tab=model#/efm/model_experience_center/text/debug?modelId=qwen-mt-flash) | 0.7元 | 1.95元 |
| **qwen-mt-lite** > 属于[Qwen3-MT](https://bailian.console.aliyun.com/cn-beijing?tab=model#/efm/model_experience_center/text/debug?modelId=qwen-mt-lite) | 0.6元 | 1.6元 |
| qwen-mt-turbo > 属于[Qwen3-MT](https://bailian.console.aliyun.com/cn-beijing?tab=model#/efm/model_experience_center/text/debug?modelId=qwen-mt-turbo) | 0.7元 | 1.95元 |

#### 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen-mt-plus** > 属于[Qwen3-MT](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/efm/model_experience_center/text/debug?modelId=qwen-mt-plus) | 16,384 | 8,192 | 8,192 | 1.8元 | 5.4元 | 无免费额度 |
| **qwen-mt-flash** > 属于[Qwen3-MT](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/efm/model_experience_center/text/debug?modelId=qwen-mt-flash) | 0.7元 | 1.95元 |
| **qwen-mt-lite** > 属于[Qwen3-MT](https://modelstudio.console.aliyun.com/us-east-1?tab=dashboard#/efm/model_experience_center/text/debug?modelId=qwen-mt-lite) | 0.6元 | 1.6元 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| **qwen-mt-plus** > 属于[Qwen3-MT](https://modelstudio.console.aliyun.com/ap-southeast-1?tab=dashboard#/efm/model_experience_center/text/debug?modelId=qwen-mt-plus) | 16,384 | 8,192 | 8,192 | 18.055元 | 54.09元 | 无免费额度 |
| **qwen-mt-flash** > 属于[Qwen3-MT](https://modelstudio.console.aliyun.com/ap-southeast-1?tab=dashboard#/efm/model_experience_center/text/debug?modelId=qwen-mt-flash) | 1.174元 | 3.596元 |
| **qwen-mt-lite** > 属于[Qwen3-MT](https://modelstudio.console.aliyun.com/ap-southeast-1?tab=dashboard#/efm/model_experience_center/text/debug?modelId=qwen-mt-lite) | 0.881元 | 2.642元 |
| qwen-mt-turbo > 属于[Qwen3-MT](https://modelstudio.console.aliyun.com/ap-southeast-1?tab=dashboard#/efm/model_experience_center/text/debug?modelId=qwen-mt-turbo) | 1.174元 | 3.596元 |

### 千问数据挖掘模型

千问数据挖掘模型可以提取文档中的结构化信息并用于数据标注和内容审核等领域。[使用方法](https://help.aliyun.com/zh/model-studio/data-mining-qwen-doc) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)

**说明**

仅支持中国内地（北京）地域。

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| qwen-doc-turbo | 262,144 | 253,952 | 32,768 | 0.6元 | 1元  | 无免费额度 |

### 千问深入研究模型

千问深入研究模型可以拆解复杂问题，结合互联网搜索进行推理分析并生成研究报告。[使用方法](https://help.aliyun.com/zh/model-studio/qwen-deep-research) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-deep-research-api)

**说明**

仅支持中国内地（北京）地域。

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| qwen-deep-research | 1,000,000 | 997,952 | 32,768 | 54元 | 163元 | 无免费额度 |

### **通义晓蜜对话分析模型**

通义晓蜜对话分析专注于对话信息抽取、场景分类、满意度判定等分析需求，擅长处理复杂业务逻辑的质检规则，支持自定义分析标准，具备强大的多轮对话理解和语义推理能力。[使用方法](https://help.aliyun.com/zh/model-studio/dialogue-analysis) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| tongyi-xiaomi-analysis-flash | 32,768 | 28,672 | 4,096 | 0.2元 | 0.4元 | 各100万Token 有效期：百炼开通后90天内 |
| tongyi-xiaomi-analysis-pro | 1.0元 | 2.7元 |

## 文本生成-千问-开源版

-   模型名称中，xxb表示参数规模，例如qwen2-72b-instruct表示参数规模为72B，即720亿。
    
-   百炼支持调用千问的开源版，您无需本地部署模型。对于开源版，建议使用Qwen3模型。
    

### **Qwen3.5**

支持文本、图像和视频输入。在纯文本任务上的效果可媲美 Qwen3 Max，性能更优且成本更低。在多模态能力上，相比 Qwen3 VL 系列有显著提升。

| **模型名称** | **模式** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** > **思维链+输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| qwen3.5-397b-a17b > 默认开启思考模式 | 思考模式 | 262,144 | 258,048 | 81,920 | 65,536 | 阶梯计价，请参见表格下方说明。 |   | 各100万 Token 有效期：百炼开通后90天内 > 仅中国内地 |
| 非思考模式 | 260,096 | \\- |
| qwen3.5-122b-a10b > 默认开启思考模式 | 思考模式 | 262,144 | 258,048 | 81,920 |
| 非思考模式 | 260,096 | \\- |
| qwen3.5-27b > 默认开启思考模式 | 思考模式 | 262,144 | 258,048 | 81,920 |
| 非思考模式 | 260,096 | \\- |
| qwen3.5-35b-a3b > 默认开启思考模式 | 思考模式 | 262,144 | 258,048 | 81,920 |
| 非思考模式 | 260,096 | \\- |

qwen3.5-397b-a17b、qwen3.5-122b-a10b、qwen3.5-27b和qwen3.5-35b-a3b根据本次请求输入的Token数，采取阶梯计费。

#### 中国内地

| **模型名称** | **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- | --- |
| qwen3.5-397b-a17b | 0<Token≤128K | 1.2元 | 7.2元 |
| 128K<Token≤256K | 3元  | 18元 |
| qwen3.5-122b-a10b | 0<Token≤128K | 0.8元 | 6.4元 |
| 128K<Token≤256K | 2元  | 16元 |
| qwen3.5-27b | 0<Token≤128K | 0.6元 | 4.8元 |
| 128K<Token≤256K | 1.8元 | 14.4元 |
| qwen3.5-35b-a3b | 0<Token≤128K | 0.4元 | 3.2元 |
| 128K<Token≤256K | 1.6元 | 12.8元 |

#### 全球

| **模型名称** | **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- | --- |
| qwen3.5-397b-a17b | 0<Token≤128K | 1.2元 | 7.2元 |
| 128K<Token≤256K | 3元  | 18元 |
| qwen3.5-122b-a10b | 0<Token≤128K | 0.8元 | 6.4元 |
| 128K<Token≤256K | 2元  | 16元 |
| qwen3.5-27b | 0<Token≤128K | 0.6元 | 4.8元 |
| 128K<Token≤256K | 1.8元 | 14.4元 |
| qwen3.5-35b-a3b | 0<Token≤128K | 0.4元 | 3.2元 |
| 128K<Token≤256K | 1.6元 | 12.8元 |

#### 国际

| **模型名称** | **单次请求的输入Token数** | **输入价格（每百万Token）** | **输出价格（每百万Token）** |
| --- | --- | --- | --- |
| qwen3.5-397b-a17b | 0<Token≤256K | 4.404元 | 26.421元 |
| qwen3.5-122b-a10b | 0<Token≤256K | 2.936元 | 23.486元 |
| qwen3.5-27b | 0<Token≤256K | 2.202元 | 17.614元 |
| qwen3.5-35b-a3b | 0<Token≤256K | 1.835元 | 14.678元 |

### **Qwen3**

2025 年 9月发布的 qwen3-next-80b-a3b-thinking 仅支持思考模式，相较于qwen3-235b-a22b-thinking-2507提升了指令遵循能力，总结回复更加精简。

2025 年 9月发布的 qwen3-next-80b-a3b-instruct 仅支持非思考模式，相较于qwen3-235b-a22b-instruct-2507增强了中文理解、逻辑推理及文本生成能力。

2025 年 7月发布的 qwen3-235b-a22b-thinking-2507、qwen3-30b-a3b-thinking-2507 模型仅支持思考模式，是qwen3-235b-a22b（思考模式）与qwen3-30b-a3b （思考模式）的升级版。

2025 年 7月发布的 qwen3-235b-a22b-instruct-2507、qwen3-30b-a3b-instruct-2507 模型仅支持非思考模式，是qwen3-235b-a22b（非思考模式）与qwen3-30b-a3b （非思考模式）的升级版。

2025 年 4月发布的 Qwen3 模型支持思考模式和非思考模式，您可以通过 `enable_thinking` 参数实现两种模式的切换。除此之外，Qwen3 模型的能力得到了大幅提升：

1.  **推理能力**：在数学、代码和逻辑推理等评测中，显著超过 QwQ 和同尺寸的非推理模型，达到同规模业界顶尖水平。
    
2.  **人类偏好能力**：创意写作、角色扮演、多轮对话、指令遵循能力均大幅提升，通用能力显著超过同尺寸模型。
    
3.  **Agent 能力**：在推理、非推理两种模式下都达到业界领先水平，能精准调用外部工具。
    
4.  **多语言能力**：支持100多种语言和方言，多语言翻译、指令理解、常识推理能力都明显提升。
    
    **支持的语言**
    
    | 英语（English） |
    | --- |
    | 简体中文（Simplified Chinese） |
    | 繁体中文（Traditional Chinese） |
    | 法语（French） |
    | 西班牙语（Spanish） |
    | 阿拉伯语（Arabic），使用阿拉伯字母。是众多阿拉伯国家的官方语言。 |
    | 俄语（Russian），使用西里尔字母。在俄罗斯及其他一些国家是官方语言。 |
    | 葡萄牙语（Portuguese），使用拉丁字母。在葡萄牙、巴西和其他葡萄牙语国家是官方语言。 |
    | 德语（German），使用拉丁字母。在德国和奥地利等地是官方语言。 |
    | 意大利语（Italian），使用拉丁字母。在意大利、圣马力诺以及瑞士的部分地区是官方语言。 |
    | 荷兰语（Dutch），使用拉丁字母。在荷兰、比利时部分地区（弗拉芒地区）和苏里南是官方语言。 |
    | 丹麦语（Danish），使用拉丁字母。在丹麦是官方语言。 |
    | 爱尔兰语（Irish），使用拉丁字母。在爱尔兰是官方语言之一。 |
    | 威尔士语（Welsh），使用拉丁字母。在威尔士使用，是官方语言之一。 |
    | 芬兰语（Finnish），使用拉丁字母。在芬兰是官方语言。 |
    | 冰岛语（Icelandic），使用拉丁字母。在冰岛是官方语言。 |
    | 瑞典语（Swedish），使用拉丁字母。是瑞典的官方语言。 |
    | 新挪威语（Norwegian Nynorsk），使用拉丁字母。在挪威与书面挪威语共同使用，属主流语言的一部分。 |
    | 书面挪威语（Norwegian Bokmål），使用拉丁字母。在挪威使用，是主流语言的一部分。 |
    | 日语（Japanese），使用日文字母。在日本是官方语言。 |
    | 朝鲜语/韩语（Korean），使用韩字（Hangul）。在韩国和朝鲜是官方语言。 |
    | 越南语（Vietnamese），使用拉丁字母。在越南是官方语言。 |
    | 泰语（Thai），使用泰文字母。在泰国是官方语言。 |
    | 印度尼西亚语（Indonesian），使用拉丁字母。是印度尼西亚的官方语言。 |
    | 马来语（Malay），使用拉丁字母。是马来西亚等地的主要语言。 |
    | 缅甸语（Burmese），使用缅甸字母。在缅甸是官方语言。 |
    | 他加禄语（Tagalog），使用拉丁字母。菲律宾的主要语言之一。 |
    | 高棉语（Khmer），使用高棉字母。在柬埔寨是官方语言。 |
    | 老挝语（Lao），使用老挝字母。在老挝是官方语言。 |
    | 印地语（Hindi），使用天城文（Devanagari）。是印度的官方语言之一。 |
    | 孟加拉语（Bengali），使用孟加拉字母。在孟加拉国和印度西孟加拉邦是官方语言。 |
    | 乌尔都语（Urdu），使用阿拉伯字母。在巴基斯坦是官方语言之一，也在印度使用。 |
    | 尼泊尔语（Nepali），使用天城字母。在尼泊尔是官方语言。 |
    | 希伯来语（Hebrew），使用希伯来字母。在以色列是官方语言。 |
    | 土耳其语（Turkish），使用拉丁字母。在土耳其和塞浦路斯北部是官方语言。 |
    | 波斯语（Persian），使用阿拉伯字母。在伊朗和塔吉克斯坦等地是官方语言。 |
    | 波兰语（Polish），使用拉丁字母。在波兰是官方语言。 |
    | 乌克兰语（Ukrainian），使用西里尔字母。在乌克兰是官方语言。 |
    | 捷克语（Czech），使用拉丁字母。在捷克是官方语言。 |
    | 罗马尼亚语（Romanian），使用拉丁字母。在罗马尼亚和摩尔多瓦是官方语言。 |
    | 保加利亚语（Bulgarian），使用西里尔字母。在保加利亚是官方语言。 |
    | 斯洛伐克语（Slovak），使用拉丁字母。在斯洛伐克是官方语言。 |
    | 匈牙利语（Hungarian），使用拉丁字母。在匈牙利是官方语言。 |
    | 斯洛文尼亚语（Slovenian），使用拉丁字母。在斯洛文尼亚是官方语言。 |
    | 拉脱维亚语（Latvian），使用拉丁字母。在拉脱维亚是官方语言。 |
    | 爱沙尼亚语（Estonian），使用拉丁字母。在爱沙尼亚是官方语言。 |
    | 立陶宛语（Lithuanian），使用拉丁字母。在立陶宛是官方语言。 |
    | 白俄罗斯语（Belarusian），使用西里尔字母。在白俄罗斯是官方语言之一。 |
    | 希腊语（Greek），使用希腊字母。在希腊和塞浦路斯是官方语言。 |
    | 克罗地亚语（Croatian），使用拉丁字母。在克罗地亚是官方语言。 |
    | 马其顿语（Macedonian），使用西里尔字母。是北马其顿的官方语言。 |
    | 马耳他语（Maltese），使用拉丁字母。在马耳他是官方语言。 |
    | 塞尔维亚语（Serbian），使用西里尔字母。在塞尔维亚是官方语言。 |
    | 波斯尼亚语（Bosnian），使用拉丁字母。在波斯尼亚和黑塞哥维那是官方语言之一。 |
    | 格鲁吉亚语（Georgian），使用格鲁吉亚字母（Georgian script）。在格鲁吉亚是官方语言。 |
    | 亚美尼亚语（Armenian），使用亚美尼亚字母。在亚美尼亚是官方语言。 |
    | 北阿塞拜疆语（North Azerbaijani），使用拉丁字母。在阿塞拜疆是官方语言。 |
    | 哈萨克语（Kazakh），使用西里尔字母。在哈萨克斯坦是官方语言。 |
    | 北乌兹别克语（Northern Uzbek），使用拉丁字母。在乌兹别克斯坦是官方语言。 |
    | 塔吉克语（Tajik），使用西里尔字母。在塔吉克斯坦是官方语言。 |
    | 斯瓦西里语（Swahili），使用拉丁字母。在东非许多国家是通用语或官方语言。 |
    | 南非语（Afrikaans），使用拉丁字母。主要在南非和纳米比亚使用。 |
    | 粤语（Cantonese），使用繁体字。主要在中国广东省、香港和澳门使用，是这些地区的主要语言之一。 |
    | 卢森堡语（Luxembourgish），使用拉丁字母。在卢森堡和德国部分地区使用，是官方语言之一。 |
    | 林堡语（Limburgish），使用拉丁字母。主要在荷兰、比利时和德国部分地区使用。 |
    | 加泰罗尼亚语（Catalan），使用拉丁字母。在加泰罗尼亚和其他部分西班牙地区使用。 |
    | 加利西亚语（Galician），使用拉丁字母。主要在西班牙加利西亚地区使用。 |
    | 阿斯图里亚斯语（Asturian），使用拉丁字母。主要在西班牙阿斯图里亚斯地区使用。 |
    | 巴斯克语（Basque），使用拉丁字母。主要在西班牙和法国的巴斯克地区使用，是西班牙巴斯克自治区的官方语言之一。 |
    | 奥克语（Occitan），使用拉丁字母。主要在法国南部地区使用。 |
    | 威尼斯语（Venetian），使用拉丁字母。主要在意大利威尼斯地区使用。 |
    | 撒丁语（Sardinian），使用拉丁字母。主要在意大利撒丁岛使用。 |
    | 西西里语（Sicilian），使用拉丁字母。主要在意大利西西里岛使用。 |
    | 弗留利语（Friulian），使用拉丁字母。主要在意大利弗留利-威尼斯朱利亚使用。 |
    | 隆巴底语（Lombard），使用拉丁字母。主要在意大利伦巴第地区使用。 |
    | 利古里亚语（Ligurian），使用拉丁字母。主要在意大利利古里亚地区使用。 |
    | 法罗语（Faroese），使用拉丁字母。主要在法罗群岛使用，是法罗群岛的官方语言之一。 |
    | 托斯克阿尔巴尼亚语（Tosk Albanian），使用拉丁字母。主要是阿尔巴尼亚南部方言。 |
    | 西里西亚语（Silesian），使用拉丁字母。主要在波兰使用。 |
    | 巴什基尔语（Bashkir），使用西里尔字母。主要在俄罗斯巴什科尔托斯坦使用。 |
    | 鞑靼语（Tatar），使用西里尔字母。主要在俄罗斯塔塔尔斯坦使用。 |
    | 美索不达米亚阿拉伯语（Mesopotamian Arabic），使用阿拉伯字母。主要在伊拉克使用。 |
    | 内志阿拉伯语（Najdi Arabic），使用阿拉伯字母。主要在沙特阿拉伯的内志地区使用。 |
    | 埃及阿拉伯语（Egyptian Arabic），使用阿拉伯字母。主要在埃及使用。 |
    | 黎凡特阿拉伯语（Levantine Arabic），使用阿拉伯字母。主要在叙利亚和黎巴嫩使用。 |
    | 闪米特阿拉伯语（Ta'izzi-Adeni Arabic），使用阿拉伯字母。主要在也门和沙特阿拉伯的哈德拉莫区域使用。 |
    | 达里语（Dari），使用阿拉伯字母。在阿富汗是官方语言之一。 |
    | 突尼斯阿拉伯语（Tunisian Arabic），使用阿拉伯字母。主要在突尼斯使用。 |
    | 摩洛哥阿拉伯语（Moroccan Arabic），使用阿拉伯字母。主要在摩洛哥使用。 |
    | 克里奥尔语（Kabuverdianu），使用拉丁字母。主要在佛得角使用。 |
    | 托克皮辛语（Tok Pisin），使用拉丁字母。在巴布亚新几内亚是主要的通用语之一。 |
    | 意第绪（Eastern Yiddish），使用希伯来字母。主要在犹太社区中使用。 |
    | 信德阿拉伯语（Sindhi），使用阿拉伯字母。在巴基斯坦信德省是官方语言之一。 |
    | 僧伽罗语（Sinhala），使用僧伽罗字母。在斯里兰卡是官方语言之一。 |
    | 泰卢固语（Telugu），使用泰卢固字母。在印度安得拉邦和特伦甘纳邦是官方语言之一。 |
    | 旁遮普语（Punjabi），使用古尔穆奇字母。在印度旁遮普邦使用，是印度的官方语言之一。 |
    | 泰米尔语（Tamil），使用泰米尔字母。在印度泰米尔纳德邦和斯里兰卡是官方语言之一。 |
    | 古吉拉特语（Gujarati），使用古吉拉特字母。在印度古吉拉特邦是官方语言之一。 |
    | 马拉雅拉姆语（Malayalam），使用马拉雅拉姆字母。在印度喀拉拉邦是官方语言之一。 |
    | 马拉地语（Marathi），使用天城字母。在印度马哈拉施特拉邦是官方语言之一。 |
    | 卡纳达语（Kannada），使用卡纳达字母。在印度卡纳塔克邦是官方语言之一。 |
    | 马加拉语（Magahi），使用天城文本。主要在印度比哈尔邦使用。 |
    | 奥里亚语（Oriya），使用乌尔都语字母。在印度奥迪沙邦是官方语言之一。 |
    | 阿瓦德语（Awadhi），使用天城字母。主要在印度北方邦使用。 |
    | 迈蒂利语（Maithili），使用天城字母。在印度比哈尔邦和尼泊尔特莱平原使用，是印度的官方语言之一。 |
    | 阿萨姆语（Assamese），使用孟加拉字母。在印度阿萨姆邦是官方语言之一。 |
    | 切蒂斯格尔语（Chhattisgarhi），使用天城字母。主要在印度切蒂斯格尔邦使用。 |
    | 比哈尔语（Bhojpuri），使用天城字母。在印度和尼泊尔部分地区使用。 |
    | 米南加保语（Minangkabau），使用拉丁字母。主要在印度尼西亚苏门答腊岛使用。 |
    | 巴厘语（Balinese），使用拉丁字母。主要在印度尼西亚巴厘岛使用。 |
    | 爪哇语（Javanese），使用拉丁字母（也惯用爪哇文字）。在印度尼西亚爪哇岛广泛使用。 |
    | 班章语（Banjar），使用拉丁字母。主要在印度尼西亚加里曼丹岛使用。 |
    | 巽他语（Sundanese），使用拉丁字母（虽然传统上使用巽他文字）。主要在印度尼西亚爪哇岛的西部使用。 |
    | 宿务语（Cebuano），使用拉丁字母。主要在菲律宾宿务地区使用。 |
    | 邦阿西楠语（Pangasinan），使用拉丁字母。主要在菲律宾邦阿西楠语省使用。 |
    | 伊洛卡诺语（Iloko），使用拉丁字母。主要在菲律宾使用。 |
    | 瓦莱语（Waray (Philippines)），使用拉丁字母。主要在菲律宾使用。 |
    | 海地语（Haitian），使用拉丁字母。在海地是官方语言之一。 |
    | 帕皮阿门托语（Papiamento），使用拉丁字母。主要在加勒比地区如阿鲁巴岛和库拉索岛使用。 |
    
5.  **回复格式**：修复了之前版本存在的回复格式的问题，如异常 Markdown、中间截断、错误输出 boxed 等问题。
    

> 2025 年 4月发布的Qwen3 开源模型在思考模式下不支持非流式输出方式。

[思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking) | [非思考模式](https://help.aliyun.com/zh/model-studio/stream) | [API 参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **模式** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** > **思维链+输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| qwen3-next-80b-a3b-thinking | 仅思考模式 | 131,072 | 126,976 | 81,920 | 32,768 | 1元  | 10元 | 各100万 Token 有效期：百炼开通后90天内 |
| qwen3-next-80b-a3b-instruct | 仅非思考模式 | 129,024 | \\- | 4元  |
| qwen3-235b-a22b-thinking-2507 | 仅思考模式 | 126,976 | 81,920 | 2元  | 20元 |
| qwen3-235b-a22b-instruct-2507 | 仅非思考模式 | 129,024 | \\- | 8元  |
| qwen3-30b-a3b-thinking-2507 | 仅思考模式 | 126,976 | 81,920 | 0.75元 | 7.5元 |
| qwen3-30b-a3b-instruct-2507 | 仅非思考模式 | 129,024 | \\- | 3元  |
| qwen3-235b-a22b > 本模型与以下模型均于2025 年 4月发布 | 非思考 | 129,024 | \\- | 16,384 | 2元  | 8元  |
| 思考  | 98,304 | 38,912 | 20元 |
| qwen3-32b | 非思考 | 129,024 | \\- | 2元  | 8元  |
| 思考  | 98,304 | 38,912 | 20元 |
| qwen3-30b-a3b | 非思考 | 129,024 | \\- | 0.75元 | 3元  |
| 思考  | 98,304 | 38,912 | 7.5元 |
| qwen3-14b | 非思考 | 129,024 | \\- | 8,192 | 1元  | 4元  |
| 思考  | 98,304 | 38,912 | 10元 |
| qwen3-8b | 非思考 | 129,024 | \\- | 0.5元 | 2元  |
| 思考  | 98,304 | 38,912 | 5元  |
| qwen3-4b | 非思考 | 129,024 | \\- | 0.3元 | 1.2元 |
| 思考  | 98,304 | 38,912 | 3元  |
| qwen3-1.7b | 非思考 | 32,768 | 30,720 | \\- | 1.2元 |
| 思考  | 28,672 | 与输入相加不超过30,720 | 3元  |
| qwen3-0.6b | 非思考 | 30,720 | \\- | 1.2元 |
| 思考  | 28,672 | 与输入相加不超过30,720 | 3元  |

#### **全球**

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **模式** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** > **思维链+输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| qwen3-next-80b-a3b-thinking | 仅支持思考模式 | 131,072 | 126,976 | 81,920 | 32,768 | 1元  | 10元 | 无免费额度 |
| qwen3-next-80b-a3b-instruct | 仅非思考模式 | 129,024 | \\- | 4元  |
| qwen3-235b-a22b-thinking-2507 | 仅支持思考模式 | 126,976 | 81,920 | 1.688元 | 16.88元 |
| qwen3-235b-a22b-instruct-2507 | 仅非思考模式 | 129,024 | \\- | 6.752元 |
| qwen3-30b-a3b-thinking-2507 | 仅支持思考模式 | 126,976 | 81,920 | 0.75元 | 7.5元 |
| qwen3-30b-a3b-instruct-2507 | 仅非思考模式 | 129,024 | \\- | 3元  |
| qwen3-235b-a22b | 非思考 | 129,024 | \\- | 16,384 | 2元  | 8元  |
| 思考  | 98,304 | 38,912 | 20元 |
| qwen3-32b | 非思考 | 129,024 | \\- | 1.174元 | 4.697元 |
| 思考  | 98,304 | 38,912 |
| qwen3-30b-a3b | 非思考 | 129,024 | \\- | 0.75元 | 3元  |
| 思考  | 98,304 | 38,912 | 7.5元 |
| qwen3-14b | 非思考 | 129,024 | \\- | 8,192 | 1元  | 4元  |
| 思考  | 98,304 | 38,912 | 10元 |
| qwen3-8b | 非思考 | 129,024 | \\- | 0.5元 | 2元  |
| 思考  | 98,304 | 38,912 | 5元  |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **模式** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** > **思维链+输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| qwen3-next-80b-a3b-thinking | 仅支持思考模式 | 131,072 | 126,976 | 81,920 | 32,768 | 1.101元 | 8.807元 | 无免费额度 |
| qwen3-next-80b-a3b-instruct | 仅非思考模式 | 129,024 | \\- |
| qwen3-235b-a22b-thinking-2507 | 仅支持思考模式 | 126,976 | 81,920 | 1.688元 | 16.88元 |
| qwen3-235b-a22b-instruct-2507 | 仅非思考模式 | 129,024 | \\- | 6.752元 |
| qwen3-30b-a3b-thinking-2507 | 仅支持思考模式 | 126,976 | 81,920 | 1.468元 | 17.614元 |
| qwen3-30b-a3b-instruct-2507 | 仅非思考模式 | 129,024 | \\- | 5.871元 |
| qwen3-235b-a22b > 本模型与以下模型均于2025 年 4月发布 | 非思考 | 129,024 | \\- | 16,384 | 5.137元 | 20.55元 |
| 思考  | 98,304 | 38,912 | 61.65元 |
| qwen3-32b | 非思考 | 129,024 | \\- | 1.174元 | 4.697元 |
| 思考  | 98,304 | 38,912 |
| qwen3-30b-a3b | 非思考 | 129,024 | \\- | 1.468元 | 5.871元 |
| 思考  | 98,304 | 38,912 | 17.614元 |
| qwen3-14b | 非思考 | 129,024 | \\- | 8,192 | 2.569元 | 10.275元 |
| 思考  | 98,304 | 38,912 | 30.825元 |
| qwen3-8b | 非思考 | 129,024 | \\- | 1.321元 | 5.137元 |
| 思考  | 98,304 | 38,912 | 15.412元 |
| qwen3-4b | 非思考 | 129,024 | \\- | 0.807元 | 3.082元 |
| 思考  | 98,304 | 38,912 | 9.247元 |
| qwen3-1.7b | 非思考 | 32,768 | 30,720 | \\- | 3.082元 |
| 思考  | 28,672 | 与输入相加不超过30,720 | 9.247元 |
| qwen3-0.6b | 非思考 | 30,720 | \\- | 3.082元 |
| 思考  | 28,672 | 与输入相加不超过30,720 | 9.247元 |

对于 Qwen3 模型，开启思考模式时如果没有输出思考过程，按非思考模式价格进行收费。

### **QwQ-开源版**

基于 Qwen2.5-32B 模型训练的 QwQ 推理模型，通过强化学习大幅度提升了模型推理能力。模型数学代码等核心指标（AIME 24/25、LiveCodeBench）以及部分通用指标（IFEval、LiveBench等）达到DeepSeek-R1 满血版水平，各指标均显著超过同样基于 Qwen2.5-32B 的 DeepSeek-R1-Distill-Qwen-32B。[使用方法](https://help.aliyun.com/zh/model-studio/deep-thinking)｜[API 参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| qwq-32b | 131,072 | 98,304 | 32,768 | 8,192 | 2元  | 6元  | 100万 Token 有效期：百炼开通后90天内 |

### **QwQ-Preview**

qwq-32b-preview 模型是由 Qwen 团队于2024年开发的实验性研究模型，专注于增强 AI 推理能力，尤其是数学和编程领域。qwq-32b-preview 模型的局限性请参见[QwQ官方博客](https://qwenlm.github.io/zh/blog/qwq-32b-preview/#%E6%A8%A1%E5%9E%8B%E5%B1%80%E9%99%90%E6%80%A7)。[使用方法](https://help.aliyun.com/zh/model-studio/text-generation#24e54b27d4agt) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)｜[在线体验](https://bailian.console.aliyun.com/#/efm/model_experience_center/text?currentTab=textChat&modelId=qwq-32b-preview)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| qwq-32b-preview > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 32,768 | 30,720 | 16,384 | 2元  | 6元  | 100万Token 有效期：百炼开通后90天内 |

### **Qwen2.5**

Qwen2.5是Qwen大型语言模型系列。针对Qwen2.5，我们发布了一系列基础语言模型和指令调优语言模型，参数规模从5亿到720亿不等。Qwen2.5在Qwen2基础上进行了以下改进：

-   在我们最新的大规模数据集上进行预训练，包含多达18万亿个Token。
    
-   由于我们在这些领域的专业专家模型，模型的知识显著增多，编码和数学能力也大幅提高。
    
-   在遵循指令、生成长文本（超过8K个标记）、理解结构化数据（例如表格）和生成结构化输出（尤其是JSON）方面有显著改进。对系统提示的多样性更具弹性，增强了聊天机器人的角色扮演实现和条件设置。
    
-   支持超过29种语言，包括中文、英语、法语、西班牙语、葡萄牙语、德语、意大利语、俄语、日语、韩语、越南语、泰语、阿拉伯语等。
    

[使用方法](https://help.aliyun.com/zh/model-studio/text-generation#24e54b27d4agt) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/) | [在线体验](https://bailian.console.aliyun.com/#/model-market/detail/qwen2.5-72b-instruct)

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| qwen2.5-14b-instruct-1m | 1,000,000 | 1,000,000 | 8,192 | 1元  | 3元  | 各100万Token 有效期：百炼开通后90天内 |
| qwen2.5-7b-instruct-1m | 0.5元 | 1元  |
| qwen2.5-72b-instruct | 131,072 | 129,024 | 4元  | 12元 |
| qwen2.5-32b-instruct | 2元  | 6元  |
| qwen2.5-14b-instruct | 1元  | 3元  |
| qwen2.5-7b-instruct | 0.5元 | 1元  |
| qwen2.5-3b-instruct | 32,768 | 30,720 | 0.3元 | 0.9元 |
| qwen2.5-1.5b-instruct | 目前仅供免费体验 > 免费额度用完后不可调用，推荐使用[Qwen3](https://help.aliyun.com/zh/model-studio/deep-thinking)、[DeepSeek-阿里云](https://help.aliyun.com/zh/model-studio/deepseek-api)、[Kimi-阿里云](https://help.aliyun.com/zh/model-studio/kimi-api)作为替代模型 |   |
| qwen2.5-0.5b-instruct |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| qwen2.5-14b-instruct-1m | 1,008,192 | 1,000,000 | 8,192 | 5.908元 | 23.632元 | 无免费额度 |
| qwen2.5-7b-instruct-1m | 2.701元 | 10.789元 |
| qwen2.5-72b-instruct | 131,072 | 129,024 | 10.275元 | 41.1元 |
| qwen2.5-32b-instruct | 5.137元 | 20.55元 |
| qwen2.5-14b-instruct | 2.569元 | 10.275元 |
| qwen2.5-7b-instruct | 1.284元 | 5.137元 |

### **Qwen2**

阿里云的千问2-开源版。[使用方法](https://help.aliyun.com/zh/model-studio/text-generation#24e54b27d4agt) | [API参考](https://help.aliyun.com/zh/model-studio/videos/use-open-source-qwen-by-calling-api) | [在线体验](https://bailian.console.aliyun.com/#/model-market/detail/qwen2-72b-instruct)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万 Token）** |   |
| qwen2-72b-instruct | 131,072 | 128,000 | 6,144 | 4元  | 12元 | 各100万Token 有效期：百炼开通后90天内 |
| qwen2-57b-a14b-instruct | 65,536 | 63,488 | 3.5元 | 7元  |
| qwen2-7b-instruct | 131,072 | 128,000 | 1元  | 2元  |
| qwen2-1.5b-instruct | 32,768 | 30,720 | 限时免费 |   |   |
| qwen2-0.5b-instruct |

### **Qwen1.5**

阿里云的千问1.5-开源版。[使用方法](https://help.aliyun.com/zh/model-studio/text-generation#24e54b27d4agt) | [API参考](https://help.aliyun.com/zh/model-studio/videos/use-open-source-qwen-by-calling-api) | [在线体验](https://bailian.console.aliyun.com/#/model-market/detail/qwen1.5-110b-chat)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万 Token）** |   |
| qwen1.5-110b-chat | 32,000 | 30,000 | 8,000 | 7元  | 14元 | 各100万Token 有效期：百炼开通后90天内 |
| qwen1.5-72b-chat | 2,000 | 5元  | 10元 |
| qwen1.5-32b-chat | 3.5元 | 7元  |
| qwen1.5-14b-chat | 8,000 | 6,000 | 2元  | 4元  |
| qwen1.5-7b-chat | 1元  | 2元  |
| qwen1.5-1.8b-chat | 32,000 | 30,000 | 限时免费 |   |   |
| qwen1.5-0.5b-chat |

### **QVQ**

qvq-72b-preview模型是由 Qwen 团队开发的实验性研究模型，专注于提升视觉推理能力，尤其在数学推理领域。qvq-72b-preview模型的局限性请参见[QVQ官方博客](https://qwenlm.github.io/blog/qvq-72b-preview/)。[使用方法](https://help.aliyun.com/zh/model-studio/vision) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/#15ef0a40798a3)

> 如果希望模型先输出思考过程再输出回答内容，请使用商业版模型[QVQ](#40e07d9a04nx8)。

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万 Token）** |   |
| qvq-72b-preview | 32,768 | 16,384 > 单图最大16384 | 16,384 | 12元 | 36元 | 10万Token 有效期：百炼开通后90天内 |

### **Qwen-Omni**

基于Qwen2.5训练的全新多模态理解生成大模型，支持文本、图像、语音、视频输入理解，具备文本和语音同时流式生成的能力，多模态内容理解速度显著提升。[使用方法](https://help.aliyun.com/zh/model-studio/qwen-omni)｜[API 参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| **（Token数）** |   |   |
| qwen2.5-omni-7b | 32,768 | 30,720 | 2,048 | 100万Token（不区分模态） 有效期：百炼开通后90天 |

开源版模型的免费额度用完后，输入与输出的计费规则如下：

| \\| **输入计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输入：文本 \\| 0.6元 \\| \\| 输入：音频 \\| 38元 \\| \\| 输入：图片/视频 \\| 2元 \\| | \\| **输出计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输出：文本 \\| 2.4元（输入仅包含文本时） 6元（输入包含图片/音频/视频时） \\| \\| 输出：文本+音频 \\| 76元（音频） > 输出的文本不计费。 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 计费示例：某次请求输入了100万 Token 的文本和100万 Token 的图片，输出了100万 Token 的文本和100万 Token 的音频，则该请求花费：0.6元（文本输入）+ 2元（图片输入）+ 76元（音频输出）= 78.6元。 |   |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| **（Token数）** |   |   |
| qwen2.5-omni-7b | 32,768 | 30,720 | 2,048 | 无免费额度 |

输入与输出的计费规则如下：

| \\| **输入计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输入：文本 \\| 0.734元 \\| \\| 输入：音频 \\| 49.613元 \\| \\| 输入：图片/视频 \\| 2.055元 \\| | \\| **输出计费项** \\| **单价（每百万Token）** \\| \\| --- \\| --- \\| \\| 输出：文本 \\| 2.936元（输入仅包含文本时） 6.165元（输入包含图片/音频/视频时） \\| \\| 输出：文本+音频 \\| 99.153元（音频） > 输出的文本不计费。 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

### **Qwen3-Omni-C**aptioner

Qwen3-Omni-Captioner以千问3-Omni为基座的开源模型，无需任何提示，自动为复杂语音、环境声、音乐、影视声效等生成精准、全面的描述，能识别说话人情绪、音乐元素（如风格、乐器）、敏感信息等，适用于音频内容分析、安全审核、意图识别、音频剪辑等多个领域。[使用方法](https://help.aliyun.com/zh/model-studio/qwen3-omni-captioner) | [API 参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| qwen3-omni-30b-a3b-captioner | 65,536 | 32,768 | 32,768 | 15.8元 | 12.7元 | 100万Token 有效期：阿里云百炼开通后90天内 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| qwen3-omni-30b-a3b-captioner | 65,536 | 32,768 | 32,768 | 27.962元 | 22.458元 | 无免费额度 |

### **Qwen-VL**

阿里云的千问VL开源版。[使用方法](https://help.aliyun.com/zh/model-studio/vision) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/#15ef0a40798a3)

相较于Qwen2.5-VL，Qwen3-VL模型能力有极大提升：

-   **智能体交互：**可操作电脑或手机界面，识别 GUI 元素、理解功能、调用工具执行任务，在 OS World 等评测中达到顶尖水平。
    
-   **视觉编码：**可通过图像或视频生成代码，用于将设计图、网站截图等生成HTML、CSS、JS 代码。
    
-   **空间感知：**支持二维和三维定位，精准判断物体方位、视角变化、遮挡关系。
    
-   **长视频理解：**支持长达20分钟的视频内容理解，并能精确定位到秒级时刻。
    
-   **深度思考：**具有深度思考能力， 擅长捕捉细节、分析因果，在 MathVista、MMMU 等评测中达到顶尖水平。
    
-   **文字识别：**支持语言扩展至 33种，在复杂光线、模糊、倾斜等场景下表现更稳定；显著提升生僻字、古籍字、专业术语的识别准确率。
    
    **支持的语言**
    
    支持的语言共33种，分别为中文、日语、韩语、印尼语、越南语、泰语、英语、法语、德语、俄语、葡萄牙语、西班牙语、意大利语、瑞典语、丹麦语、捷克语、挪威语、荷兰语、芬兰语、土耳其语、波兰语、斯瓦希里语、罗马尼亚语、塞尔维亚语、希腊语、哈萨克语、乌兹别克语、宿务语、阿拉伯语、乌尔都语、波斯语、印地语 / 天城语、希伯来语。
    

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **模式** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** > **思维链+输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| qwen3-vl-235b-a22b-thinking | 仅思考模式 | 131,072 | 126,976 | 81,920 | 32,768 | 2元  | 20元 | 各100万 Token 有效期：百炼开通后90天内 |
| qwen3-vl-235b-a22b-instruct | 仅非思考模式 | 129,024 | \\- | 8元  |
| qwen3-vl-32b-thinking | 仅思考模式 | 126,976 | 81,920 | 2元  | 20元 |
| qwen3-vl-32b-instruct | 仅非思考模式 | 129,024 | \\- | 8元  |
| qwen3-vl-30b-a3b-thinking | 仅思考模式 | 126,976 | 81,920 | 0.75元 | 7.5元 |
| qwen3-vl-30b-a3b-instruct | 仅非思考模式 | 129,024 | \\- | 3元  |
| qwen3-vl-8b-thinking | 仅思考模式 | 126,976 | 81,920 | 0.5元 | 5元  |
| qwen3-vl-8b-instruct | 仅非思考模式 | 129,024 | \\- | 2元  |

**更多模型**

Qwen2.5-VL是视觉理解系列大模型，在Qwen2-VL的基础上做了如下改进：

-   **感知更丰富的世界：**Qwen2.5-VL不仅擅长识别常见物体，如花、鸟、鱼和昆虫等，还能分析图像中的文本、图表、图标、图形和布局等。
    
-   **长视频理解能力：**支持对长视频文件（最长10分钟）进行理解，具备通过精准定位相关视频片段来捕捉事件的新能力
    
-   **视觉定位：**Qwen2.5-VL可通过生成bounding box（矩形框的左上角和右下角坐标）或者point（矩形框的中心点坐标）来准确定位图像中的物体，并能够为坐标和属性提供稳定的JSON输出。
    
-   **结构化输出：**可支持对发票、表单、表格等数据进行结构化输出，惠及金融、商业等领域的应用。
    

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| qwen2.5-vl-72b-instruct | 131,072 | 129,024 > 单图最大16384 | 8,192 | 16元 | 48元 | 各100万Token 有效期：百炼开通后90天内 |
| qwen2.5-vl-32b-instruct | 8元  | 24元 |
| qwen2.5-vl-7b-instruct | 2元  | 5元  |
| qwen2.5-vl-3b-instruct | 1.2元 | 3.6元 |
| qwen2-vl-72b-instruct | 32,768 | 30,720 > 单图最大16384 | 2,048 | 16元 | 48元 |
| qwen2-vl-7b-instruct | 32,000 | 30,000 > 单图最大16384 | 2,000 | 目前仅供免费体验。 > 免费额度用完后不可调用，建议改用qwen-vl-max、qwen-vl-plus模型。 |   | 各10万Token 有效期：百炼开通后90天内 |
| qwen2-vl-2b-instruct | 限时免费 |   |
| qwen-vl-v1 | 8,000 | 6,000 > 单图最大1280 | 1,500 | 目前仅供免费体验。 > 免费额度用完后不可调用，建议改用qwen-vl-max、qwen-vl-plus模型。 |   |
| qwen-vl-chat-v1 |

#### **全球**

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **模式** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** > **思维链+输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| qwen3-vl-235b-a22b-thinking | 仅思考模式 | 131,072 | 126,976 | 81,920 | 32,768 | 2元  | 20元 | 无免费额度 |
| qwen3-vl-235b-a22b-instruct | 仅非思考模式 | 129,024 | \\- | 8元  |
| qwen3-vl-32b-thinking | 仅思考模式 | 126,976 | 81,920 | 1.174元 | 4.697元 |
| qwen3-vl-32b-instruct | 仅非思考模式 | 129,024 | \\- |
| qwen3-vl-30b-a3b-thinking | 仅思考模式 | 126,976 | 81,920 | 0.75元 | 7.5元 |
| qwen3-vl-30b-a3b-instruct | 仅非思考模式 | 129,024 | \\- | 3元  |
| qwen3-vl-8b-thinking | 仅思考模式 | 126,976 | 81,920 | 0.5元 | 5元  |
| qwen3-vl-8b-instruct | 仅非思考模式 | 129,024 | \\- | 2元  |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **模式** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** > **思维链+输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万Token）** |   |
| qwen3-vl-235b-a22b-thinking | 仅思考模式 |     | 126,976 | 81,920 |     | 2.936元 | 29.357元 | 无免费额度 |
| qwen3-vl-235b-a22b-instruct | 仅非思考模式 | 129,024 | \\- | 11.743元 |
| qwen3-vl-32b-thinking | 仅思考模式 | 131,072 | 126,976 | 81,920 | 32,768 | 1.174元 | 4.697元 |
| qwen3-vl-32b-instruct | 仅非思考模式 | 129,024 | \\- | 4.697元 |
| qwen3-vl-30b-a3b-thinking | 仅思考模式 | 126,976 | 81,920 | 1.468元 | 17.614元 |
| qwen3-vl-30b-a3b-instruct | 仅非思考模式 | 129,024 | \\- | 5.871元 |
| qwen3-vl-8b-thinking | 仅思考模式 | 126,976 | 81,920 | 1.321元 | 15.412元 |
| qwen3-vl-8b-instruct | 仅非思考模式 | 129,024 | \\- | 5.137元 |

**更多模型**

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| qwen2.5-vl-72b-instruct | 131,072 | 129,024 > 单图最大16384 | 8,192 | 20.55元 | 61.65元 | 无免费额度 |
| qwen2.5-vl-32b-instruct | 10.275元 | 30.825元 |
| qwen2.5-vl-7b-instruct | 2.569元 | 7.706元 |
| qwen2.5-vl-3b-instruct | 1.541元 | 4.624元 |

### **Qwen-Audio**

阿里云的千问Audio开源版。[使用方法](https://help.aliyun.com/zh/model-studio/audio-language-model)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万 Token）** |   |
| qwen2-audio-instruct > 相比qwen-audio-chat提升了音频理解能力，且新增了语音聊天能力。 | 8,000 | 6,000 | 1,500 | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐使用[Qwen-Omni](https://help.aliyun.com/zh/model-studio/qwen-omni)作为替代模型 |   | 10万Token 有效期：阿里云百炼开通后90天内 |
| qwen-audio-chat |

### Qwen-Math

基于Qwen模型构建的专门用于数学解题的语言模型。Qwen2.5-Math支持**中文**和**英文**，并整合了多种推理方法，包括CoT（Chain of Thought）、PoT（Program of Thought）和 TIR（Tool-Integrated Reasoning）。[使用方法](https://help.aliyun.com/zh/model-studio/math-language-model) | [API参考](https://help.aliyun.com/zh/document_detail/2844170.html) | [在线体验](https://bailian.console.aliyun.com/#/model-market/detail/qwen2.5-math-72b-instruct)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输入价格** | **输出价格** | **上下文长度** | **最大输入** | **最大输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（每百万Token）** |   | **（Token数）** |   |   |
| qwen2.5-math-72b-instruct | 4元  | 12元 | 4,096 | 3,072 | 3,072 | 各100万Token 有效期：百炼开通后90天内 |
| qwen2.5-math-7b-instruct | 1元  | 2元  |
| qwen2.5-math-1.5b-instruct | 限时免费 |   | 限时免费 |

### Qwen-Coder

千问代码模型开源版。最新的 Qwen3-Coder系列具有强大的Coding Agent能力，擅长工具调用和环境交互，能够实现自主编程、代码能力卓越的同时兼具通用能力。[使用方法](https://help.aliyun.com/zh/model-studio/qwen-coder) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/) | [在线体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/text?currentTab=textChat&modelId=qwen3-coder-480b-a35b-instruct)

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| qwen3-coder-next | 262,144 | 204,800 | 65,536 | 阶梯计价，请参见表格下方说明。 |   | 各100万Token 有效期：百炼开通后90天内 |
| qwen3-coder-480b-a35b-instruct |
| qwen3-coder-30b-a3b-instruct |

上述模型根据本次请求输入的 Token数，采取阶梯计费。

| **模型名称** | **单次请求的输入 Token 数** | **输入成本（每百万Token）** | **输出成本（每百万Token）** |
| --- | --- | --- | --- |
| qwen3-coder-next | 0<Token≤32K | 1元  | 4元  |
| 32K<Token≤128K | 1.5元 | 6元  |
| 128K<Token≤256K | 2.5元 | 10元 |
| qwen3-coder-480b-a35b-instruct | 0<Token≤32K | 6元  | 24元 |
| 32K<Token≤128K | 9元  | 36元 |
| 128K<Token≤200K | 15元 | 60元 |
| qwen3-coder-30b-a3b-instruct | 0<Token≤32K | 1.5元 | 6元  |
| 32K<Token≤128K | 2.25元 | 9元  |
| 128K<Token≤200K | 3.75元 | 15元 |

**更多模型**

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| qwen2.5-coder-32b-instruct | 131,072 | 129,024 | 8,192 | 2元  | 6元  | 各100万Token 有效期：百炼开通后90天内 |
| qwen2.5-coder-14b-instruct |
| qwen2.5-coder-7b-instruct | 1元  | 2元  |
| qwen2.5-coder-3b-instruct | 32,768 | 30,720 | 限时免费体验 |   |   |
| qwen2.5-coder-1.5b-instruct |
| qwen2.5-coder-0.5b-instruct |

#### 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| qwen3-coder-480b-a35b-instruct | 262,144 | 204,800 | 65,536 | 阶梯计价，请参见表格下方说明。 |   | 无免费额度 |
| qwen3-coder-30b-a3b-instruct |

qwen3-coder-480b-a35b-instruct 与 qwen3-coder-30b-a3b-instruct 根据本次请求输入的 Token数，采取阶梯计费。

| **模型名称** | **单次请求的输入 Token 数** | **输入成本（每百万Token）** | **输出成本（每百万Token）** |
| --- | --- | --- | --- |
| qwen3-coder-480b-a35b-instruct | 0<Token≤32K | 6元  | 24元 |
| 32K<Token≤128K | 9元  | 36元 |
| 128K<Token≤200K | 15元 | 60元 |
| qwen3-coder-30b-a3b-instruct | 0<Token≤32K | 1.5元 | 6元  |
| 32K<Token≤128K | 2.25元 | 9元  |
| 128K<Token≤200K | 3.75元 | 15元 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| qwen3-coder-next | 262,144 | 204,800 | 65,536 | 阶梯计价，请参见表格下方说明。 |   | 无免费额度 |
| qwen3-coder-480b-a35b-instruct |
| qwen3-coder-30b-a3b-instruct |

上述模型根据本次请求输入的 Token数，采取阶梯计费。

| **模型名称** | **单次请求的输入 Token 数** | **输入成本（每百万Token）** | **输出成本（每百万Token）** |
| --- | --- | --- | --- |
| qwen3-coder-next | 0<Token≤32K | 2.202元 | 11.009元 |
| 32K<Token≤128K | 3.67元 | 18.348元 |
| 128K<Token≤256K | 5.871元 | 29.357元 |
| qwen3-coder-480b-a35b-instruct | 0<Token≤32K | 11.009元 | 55.044元 |
| 32K<Token≤128K | 19.816元 | 99.08元 |
| 128K<Token≤200K | 33.027元 | 165.133元 |
| qwen3-coder-30b-a3b-instruct | 0<Token≤32K | 3.303元 | 16.513元 |
| 32K<Token≤128K | 5.504元 | 27.522元 |
| 128K<Token≤200K | 8.807元 | 44.035元 |

## 文本生成-第三方模型

### **DeepSeek**

DeepSeek 是由深度求索公司推出的大语言模型。[API参考](https://help.aliyun.com/zh/model-studio/deepseek-api) | [在线体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/text?currentTab=textChat&modelId=deepseek-r1)

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** | **免费额度** [查看剩余额度](https://help.aliyun.com/zh/model-studio/new-free-quota#view-quota) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万 Token）** |   |
| deepseek-v3.2 > 685B 满血版 > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 131,072 | 98,304 | 32,768 | 65,536 | 2元  | 3元  | 各100万Token 有效期：百炼开通后90天内 |
| deepseek-v3.2-exp > 685B 满血版 | 131,072 | 98,304 | 32,768 | 65,536 | 2元  | 3元  |
| deepseek-v3.1 > 685B 满血版 | 4元  | 12元 |
| deepseek-r1 > 685B 满血版 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 16,384 | 4元  | 16元 |
| deepseek-r1-0528 > 685B 满血版 | 4元  | 16元 |
| deepseek-v3 > 671B 满血版 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 131,072 | 不涉及 | 2元  | 8元  |
| deepseek-r1-distill-qwen-1.5b > 基于 Qwen2.5-Math-1.5B | 32,768 | 32,768 | 16,384 | 16,384 | 限时免费体验 |   |   |
| deepseek-r1-distill-qwen-7b > 基于 Qwen2.5-Math-7B | 0.5元 | 1元  | 各100万Token 有效期：百炼开通后90天内 |
| deepseek-r1-distill-qwen-14b > 基于 Qwen2.5-14B | 1元  | 3元  |
| deepseek-r1-distill-qwen-32b > 基于 Qwen2.5-32B | 2元  | 6元  |
| deepseek-r1-distill-llama-8b > 基于 Llama-3.1-8B | 限时免费体验 |   |   |
| deepseek-r1-distill-llama-70b > 基于 Llama-3.3-70B | 目前仅供免费体验 > 免费额度用完后不可调用，推荐使用[Qwen3](https://help.aliyun.com/zh/model-studio/deep-thinking)、[deepseek-v3.1](https://help.aliyun.com/zh/model-studio/deepseek-api)、[Kimi-阿里云](https://help.aliyun.com/zh/model-studio/kimi-api)作为替代模型 |   | 各100万Token 有效期：百炼开通后90天内 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** | **免费额度** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万 Token）** |   |
| deepseek-v3.2 > 685B 满血版 > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 131,072 | 98,304 | 32,768 | 65,536 | 4.272元 | 12.815元 | 无   |

### **DeepSeek-硅基流动**

由硅基流动供应商提供的 DeepSeek 推理服务。[使用方法](https://help.aliyun.com/zh/model-studio/siliconflow-deepseek-api)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。

| **模型名称** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** | **免费额度** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万 Token）** |   |
| siliconflow/deepseek-v3.2 | 163,840 | 163,840 | 65,536 | 65,536 | 2元  | 3元  | 无   |
| siliconflow/deepseek-v3.1-terminus | 4元  | 12元 |
| siliconflow/deepseek-r1-0528 | 32,768 | 4元  | 16元 |
| siliconflow/deepseek-v3-0324 | \\- | 163,840 | 2元  | 8元  |

### **Kimi**

Kimi-K2 是由月之暗面公司推出的大语言模型，具有卓越的编码和工具调用能力。[使用方法](https://help.aliyun.com/zh/model-studio/kimi-api) | [在线体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/text?currentTab=textChat&modelId=Moonshot-Kimi-K2-Instruct)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **模式** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** | **免费额度** [查看剩余额度](https://help.aliyun.com/zh/model-studio/new-free-quota#view-quota) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | **（Token数）** |   |   |   | **（每百万 Token）** |   |
| kimi-k2.5 | 思考模式 | 262,144 | 258,048 | 81,920 | 98,304 | 4元  | 21元 | 各100万Token 有效期：百炼开通后90天内 |
| 非思考模式 | 262,144 | 260,096 | \\- | 98,304 |
| kimi-k2-thinking | 思考模式 | 262,144 | 229,376 | 32,768 | 16,384 | 4元  | 16元 |
| Moonshot-Kimi-K2-Instruct | 非思考模式 | 131,072 | 131,072 | \\- | 8,192 | 4元  | 16元 |

### **Kimi-月之暗面**

由月之暗面（Moonshot AI）直供的模型推理服务。[使用方法](https://help.aliyun.com/zh/model-studio/kimi-api-by-moonshot-ai) | [在线体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/text?currentTab=textChat&modelId=Moonshot-Kimi-K2-Instruct)

> 以下 Kimi 模型的推理服务由月之暗面（Moonshot AI）直接提供，非百炼平台部署。

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。

| **模型名称** | **模式** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** | **免费额度** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | **（Token数）** |   |   |   | **（每百万 Token）** |   |
| kimi/kimi-k2.5 | 思考模式 | 262,144 | 262,144 | 262,144 | 262,144 | 4元  | 21元 | 无   |
| 非思考模式 | \\- |

### **GLM**

GLM系列模型是智谱AI专为智能体设计的混合推理模型，提供思考与非思考两种模式。[GLM](https://help.aliyun.com/zh/model-studio/glm)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** | **免费额度** [查看剩余额度](https://help.aliyun.com/zh/model-studio/new-free-quota#view-quota) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万 Token）** |   |
| glm-5 | 202,752 | 202,752 | 32,768 | 16,384 | 阶梯计费，请参见下方表格 |   | 各100万Token 有效期：百炼开通后90天内 |
| glm-4.7 | 169,984 |
| glm-4.6 |
| glm-4.5 | 131,072 | 98,304 |
| glm-4.5-air |

以上模型根据请求输入的 Token数，采取阶梯计费。

| **模型名称** | **单次请求的输入 Token 数** | **输入成本（每百万 Token）** | **输出成本（每百万 Token）** |
| --- | --- | --- | --- |
| glm-5 | 0<Token<=32K | 4元  | 18元 |
| 32K<Token<=198K | 6元  | 22元 |
| glm-4.7 | 0<Token<=32K | 3元  | 14元 |
| 32K<Token<=166K | 4元  | 16元 |
| glm-4.6 | 0<Token<=32K | 3元  | 14元 |
| 32K<Token<=166K | 4元  | 16元 |
| glm-4.5 | 0<Token<=32K | 3元  | 14元 |
| 32K<Token<=96K | 4元  | 16元 |
| glm-4.5-air | 0<Token<=32K | 0.8元 | 6元  |
| 32K<Token<=96K | 1.2元 | 8元  |

> 以上模型非集成第三方服务，均部署在阿里云百炼服务器上。

> GLM 模型思考与非思考模式同价。

### **GLM-智谱**

由智谱直供的模型推理服务。[GLM-智谱](https://help.aliyun.com/zh/model-studio/glm-zhipu)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。

| **模型名称** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** | **免费额度** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |   | **（每百万 Token）** |   |
| ZHIPU/GLM-5 | 204,800 | 203,776 | 131,072 | 131,072 > 默认65,536，可通过max\\_tokens调整。 | 6元  | 22元 | 无   |

### **MiniMax**

MiniMax 是由稀宇科技（MiniMax）公司推出的大语言模型，聚焦真实世界复杂任务，其核心优势包括多语言编程和 Agent 任务处理能力。[使用方法](https://help.aliyun.com/zh/model-studio/minimax-api)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大思维链长度+回复长度** > **不支持thinking\\_budget参数** | **输入成本** | **输出成本** | **免费额度** [查看剩余额度](https://help.aliyun.com/zh/model-studio/new-free-quota#view-quota) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万 Token）** |   |
| MiniMax-M2.5 | 196,608 | 196,601 | 32,768 | 2.1元 | 8.4元 | 100万Token 有效期：百炼开通后90天内 |
| MiniMax-M2.1 | 204,800 | 172,032 |

### **MiniMax-稀宇科技**

由稀宇科技（MiniMax）直供的模型推理服务。[使用方法](https://help.aliyun.com/zh/model-studio/minimax-api-by-minimax)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大思维链长度+回复长度** > **不支持thinking\\_budget参数** | **输入成本** > **命中**[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)**的折扣为10%** | **输出成本** | **免费额度** |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **每百万 Token** |   |     |
| MiniMax/MiniMax-M2.7 | 204,800 | 204,800 | 131,072 | 2.1元 | 8.4元 | 无   |
| MiniMax/MiniMax-M2.5 |
| MiniMax/MiniMax-M2.1 |

### **MiniMax-abab**

MiniMax推出的大语言模型。[API参考](https://help.aliyun.com/zh/model-studio/minimax-llm-api) | [在线体验](https://bailian.console.aliyun.com/#/model-market/detail/abab6.5s-chat)（需申请）

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **说明** | **上下文长度** | **最大输入** | **输入输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |
| abab6.5g-chat | 适合英文场景 | 8,000 | 8,000 | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐使用[Qwen3](https://help.aliyun.com/zh/model-studio/deep-thinking)、[DeepSeek-阿里云](https://help.aliyun.com/zh/model-studio/deepseek-api)、[Kimi-阿里云](https://help.aliyun.com/zh/model-studio/kimi-api) 等作为替代模型 | 各100万Token（需申请） 有效期：申请通过后90天内 |
| abab6.5t-chat | 适合中文场景 |
| abab6.5s-chat | 适合超长文本场景 | 245,000 | 245,000 |

## **图像生成**

### **千问文生图**

千问文生图模型在**文本渲染**方面表现突出，特别是**中文文本渲染**。[API参考](https://help.aliyun.com/zh/model-studio/qwen-image-api)

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单价** | **免费额度** |
| --- | --- | --- |
| qwen-image-2.0-pro > 当前与qwen-image-2.0-pro-2026-03-03能力相同 | 0.5元/张 | [新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)：各100张 有效期：阿里云百炼开通后90天内 |
| qwen-image-2.0-pro-2026-03-03 | 0.5元/张 |
| qwen-image-2.0 > 当前与qwen-image-2.0-2026-03-03能力相同 | 0.2元/张 |
| qwen-image-2.0-2026-03-03 | 0.2元/张 |
| qwen-image-max > 当前与qwen-image-max-2025-12-30能力相同 | 0.5元/张 |
| qwen-image-max-2025-12-30 | 0.5元/张 |
| qwen-image-plus > 当前与qwen-image能力相同 | 0.2元/张 |
| qwen-image-plus-2026-01-09 | 0.2元/张 |
| qwen-image | 0.25元/张 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **单价** | **免费额度** |
| --- | --- | --- |
| qwen-image-2.0-pro > 当前与qwen-image-2.0-pro-2026-03-03能力相同 | 0.550443元/张 | 无免费额度 |
| qwen-image-2.0-pro-2026-03-03 | 0.550443元/张 |
| qwen-image-2.0 > 当前与qwen-image-2.0-2026-03-03能力相同 | 0.256873元/张 |
| qwen-image-2.0-2026-03-03 | 0.256873元/张 |
| qwen-image-max > 当前与qwen-image-max-2025-12-30能力相同 | 0.550443元/张 |
| qwen-image-max-2025-12-30 | 0.550443元/张 |
| qwen-image-plus > 当前与qwen-image能力相同 | 0.220177元/张 |
| qwen-image-plus-2026-01-09 | 0.220177元/张 |
| qwen-image | 0.256873元/张 |

| **输入提示词** | **输出图像** |
| --- | --- |
| 一副典雅庄重的对联悬挂于厅堂之中，房间是个安静古典的中式布置，桌子上放着一些青花瓷，对联上左书“义本生知人机同道善思新”，右书“通云赋智乾坤启数高志远”， 横批“智启千问”，字体飘逸，在中间挂着一幅中国风的画作，内容是岳阳楼。 | ![qwen-image-max-case](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |

### **千问图像编辑**

千问图像编辑模型支持精准的中英双语文字编辑、调色、细节增强、风格迁移、增删物体等操作，可实现复杂的图文编辑。[使用方法](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)｜ [API参考](https://help.aliyun.com/zh/model-studio/qwen-image-edit-api)

计费规则：按成功生成的**图片张数**计费，失败不计费也不占用免费额度。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| qwen-image-2.0-pro > 当前与qwen-image-2.0-pro-2026-03-03能力相同 | 0.5元/张 | 各100张 有效期：阿里云百炼开通后90天内 |
| qwen-image-2.0-pro-2026-03-03 | 0.5元/张 |
| qwen-image-2.0 > 当前与qwen-image-2.0-2026-03-03能力相同 | 0.2元/张 |
| qwen-image-2.0-2026-03-03 | 0.2元/张 |
| qwen-image-edit-max > 当前与qwen-image-edit-max-2026-01-16能力相同 | 0.5元/张 |
| qwen-image-edit-max-2026-01-16 | 0.5元/张 |
| qwen-image-edit-plus > 当前与qwen-image-edit-plus-2025-10-30能力相同 | 0.2元/张 |
| qwen-image-edit-plus-2025-12-15 | 0.2元/张 |
| qwen-image-edit-plus-2025-10-30 | 0.2元/张 |
| qwen-image-edit | 0.3元/张 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **单价** | **免费额度** |
| --- | --- | --- |
| qwen-image-2.0-pro > 当前与qwen-image-2.0-pro-2026-03-03能力相同 | 0.550443元/张 | 无免费额度 |
| qwen-image-2.0-pro-2026-03-03 | 0.550443元/张 |
| qwen-image-2.0 > 当前与qwen-image-2.0-2026-03-03能力相同 | 0.256873元/张 |
| qwen-image-2.0-2026-03-03 | 0.256873元/张 |
| qwen-image-edit-max > 当前与qwen-image-edit-max-2026-01-16能力相同 | 0.550443元/张 |
| qwen-image-edit-max-2026-01-16 | 0.550443元/张 |
| qwen-image-edit-plus > 当前与qwen-image-edit-plus-2025-10-30能力相同 | 0.220177元/张 |
| qwen-image-edit-plus-2025-12-15 | 0.220177元/张 |
| qwen-image-edit-plus-2025-10-30 | 0.220177元/张 |
| qwen-image-edit | 0.330266元/张 |

| ![dog_and_girl (1)](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 原图 | ![狗修改图](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 将图中的人物改为站立姿势，弯腰握住狗的前爪 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 原图 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 将字母块上的单词'HEALTH INSURANCE’ 替换为'明天会更好' |
| --- | --- | --- | --- |
| ![5](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 原图 | ![5out](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 用浅蓝色衬衫替换圆点衬衫 | ![6](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 原图 | ![6out](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 将图中背景改为南极 |
| ![7](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 原图 | ![7out](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 生成人物的卡通头像 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 原图 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 删除餐盘上的头发 |

### **千问图像翻译**

千问图像翻译模型支持将**11种**语言图片的文字翻译成中文或英文，能精准保留原始排版与内容信息，并提供术语定义、敏感词过滤、图像主体检测等自定义功能。[API参考](https://help.aliyun.com/zh/model-studio/qwen-mt-image-api)

计费规则：按成功生成的**图片张数**计费，失败不计费也不占用免费额度。

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- |
| qwen-mt-image | 0.003元/张 | 100张 |

| ![en](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 原图 | ![ja](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 日语 |
| --- | --- |
| ![es](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 葡语 | ![ar](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 阿拉伯语 |

### **Z-Image**

Z-Image 是一款轻量级文生图模型，可快速生成高质量图像，支持中英双语渲染、复杂语义理解和多风格题材，并可灵活适配多种分辨率与宽高比。[API参考](https://help.aliyun.com/zh/model-studio/z-image-api-reference)

计费规则：按成功生成的**图片张数**计费，失败不计费也不占用免费额度。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- |
| z-image-turbo | 关闭提示词改写（`prompt_extend=false`）：0.1元/张 开启提示词改写（`prompt_extend=true`）：0.2元/张 | 100张 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- |
| z-image-turbo | 关闭提示词改写（`prompt_extend=false`）：0.110089元/张 开启提示词改写（`prompt_extend=true`）：0.220177元/张 | 无免费额度 |

| **输入提示词** | **输出图像** |
| --- | --- |
| film grain, analog film texture, soft film lighting, Kodak Portra 400 style, cinematic grainy texture, photorealistic details, subtle noise, (film grain:1.2)。采用近景特写镜头拍摄的东亚年轻女性，呈现户外雪地场景。她体型纤瘦，呈站立姿势，身体微微向右侧倾斜，头部抬起看向画面上方，姿态自然放松。她的面部是典型东亚长相，肤色白皙，脸颊带有自然的红润感，五官清秀：眼睛是深棕色，眼型偏圆，眼神略带惊讶地望向上方，眼白部分可见；眉毛是深黑色，形状自然弯长；鼻子小巧挺直，嘴唇涂有红色口红，唇瓣微张，表情带着轻微的惊讶或好奇。她的头发是深黑色长直发，发丝被风吹得略显凌乱，部分垂在脸颊两侧，头顶佩戴一顶深灰色的头盔，头盔边缘露出少量发丝。服装是蓝白拼接的厚重外套，外套材质看起来是毛绒与布料结合，显得温暖厚实，适合雪地环境。背景是被白雪覆盖的户外场景，远处可见模糊的树木轮廓，天空是明亮的浅蓝色，带有少量白云，光线是强烈的自然日光，照亮人物面部与头发，形成清晰的光影，色调以蓝、白、黑为主，整体风格清新自然。画面顶部有黑色提示框，内有“**Press esc to exit full screen**”的白色文字。镜头的近景视角放大了人物的表情与细节，营造出户外雪地的真实氛围。 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |

### **万相文生图**

**文生图V2版**

万相文生图模型根据文本生成精美的图片。推荐选择最新版的模型开启文生图创作。[使用方法](https://help.aliyun.com/zh/model-studio/text-to-image) ｜ [API参考](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference) ｜ [在线体验](https://tongyi.aliyun.com/wan/generate/video/image-to-video?model=wan2.5)

计费规则：按成功生成的**图片张数**计费，失败不计费也不占用免费额度。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **说明** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- | --- |
| wan2.6-t2i `**推荐**` | 万相2.6。支持新增的同步接口，同时支持在总像素面积与宽高比约束内，自由选尺寸。 | 0.20元/张 | 50张 |
| wan2.5-t2i-preview `**推荐**` | 万相2.5 preview。取消单边限制，在总像素面积与宽高比约束内，自由选尺寸。 | 0.20元/张 | 50张 |
| wan2.2-t2i-plus | 万相2.2专业版。在创意性、稳定性、写实质感上全面升级。 | 0.20元/张 | 100张 |
| wan2.2-t2i-flash | 万相2.2极速版。在创意性、稳定性、写实质感上全面升级。 | 0.14元/张 | 100张 |
| wanx2.1-t2i-plus | 万相2.1专业版。支持多种风格，生成图像细节丰富。 | 0.20元/张 | 500张 |
| wanx2.1-t2i-turbo | 万相2.1极速版。支持多种风格，生成速度快。 | 0.14元/张 | 500张 |
| wanx2.0-t2i-turbo | 万相2.0极速版。擅长质感人像与创意设计，性价比高。 | 0.04元/张 | 500张 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **说明** | **单价** | **免费额度** |
| --- | --- | --- | --- |
| wan2.6-t2i `**推荐**` | 万相2.6。支持新增的同步接口，同时支持在总像素面积与宽高比约束内，自由选尺寸。 | 0.20元/张 | 无免费额度 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **说明** | **单价** | **免费额度** |
| --- | --- | --- | --- |
| wan2.6-t2i `**推荐**` | 万相2.6。支持新增的同步接口，同时支持在总像素面积与宽高比约束内，自由选尺寸。 | 0.220177元/张 | 无免费额度 |
| wan2.5-t2i-preview `**推荐**` | 万相2.5 preview。取消单边限制，在总像素面积与宽高比约束内，自由选尺寸。 | 0.220177元/张 | 无免费额度 |
| wan2.2-t2i-plus | 万相2.2专业版。在创意性、稳定性、写实质感上全面升级。 | 0.366962元/张 | 无免费额度 |
| wan2.2-t2i-flash | 万相2.2极速版。在创意性、稳定性、写实质感上全面升级。 | 0.183481元/张 | 无免费额度 |
| wan2.1-t2i-plus | 万相2.1专业版。支持多种风格，生成图像细节丰富。 | 0.366962元/张 | 无免费额度 |
| wan2.1-t2i-turbo | 万相2.1极速版。支持多种风格，生成速度快。 | 0.183481元/张 | 无免费额度 |

**文生图V1版**

**说明**

-   推荐使用全面升级的[文生图V2版模型](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)。
    
-   仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。
    

可以基于输入的文本生成图片。此外，还支持输入参考图片，并参考图片内容或者图片风格进行图片生成。[API参考](https://help.aliyun.com/zh/model-studio/text-to-image-api-reference) | [在线体验](https://bailian.console.aliyun.com/#/model-market/detail/wanx-v1)

| **模型名称** | **示例输入** | **示例输出** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| wanx-v1 | ![参考图](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 提示词：一只小狗在笑 | ![小狗在笑](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 0.16元/张 | 500张 有效期：百炼开通后90天内 |

### **万相图像生成与编辑2.6**

万相图像生成模型支持图像编辑、图文混排输出，满足多样化生成与集成需求。[API参考](https://help.aliyun.com/zh/model-studio/wan-image-generation-api-reference)

计费规则：按成功生成的**图片张数**计费，失败不计费也不占用免费额度。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- |
| wan2.6-image | 0.20元/张 | 50张 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **单价** | **免费额度** |
| --- | --- | --- |
| wan2.6-image | 0.20元/张 | 无免费额度 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **单价** | **免费额度** |
| --- | --- | --- |
| wan2.6-image | 0.220177元/张 | 无免费额度 |

### **万相通用图像编辑2.5**

万相-通用图像编辑2.5模型支持输入文本、单图或多图实现基于主体一致性的图像编辑、多图融合创作等能力。[API参考](https://help.aliyun.com/zh/model-studio/wan2-5-image-edit-api-reference)

计费规则：按成功生成的**图片张数**计费，失败不计费也不占用免费额度。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- |
| wan2.5-i2i-preview | 0.20元/张 | 50张 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **单价** | **免费额度** |
| --- | --- | --- |
| wan2.5-i2i-preview | 0.220177元/张 | 无免费额度 |

| **模型功能** | **输入示例** | **输出图像** |
| --- | --- | --- |
| 单图编辑 | ![damotest2023_Portrait_photography_outdoors_fashionable_beauty_409ae3c1-19e8-4515-8e50-b3c9072e1282_2-转换自-png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | ![a26b226d-f044-4e95-a41c-d1c0d301c30b-转换自-png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 将花卉连衣裙换成一件复古风格的蕾丝长裙，领口和袖口有精致的刺绣细节。 |
| 多图融合 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | ![p1028883](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 将图1中的闹钟放置到图2的餐桌的花瓶旁边位置 |

### **万相通用图像编辑2.1**

万相-通用图像编辑模型通过简单的指令即可实现多样化的图像编辑，适用于扩图、去水印、风格迁移、图像修复、图像美化等场景。[使用方法](https://help.aliyun.com/zh/model-studio/wanx-image-edit)| [API参考](https://help.aliyun.com/zh/model-studio/wanx-image-edit-api-reference)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **计费单价** | **免费额度** |
| --- | --- | --- |
| wanx2.1-imageedit | 0.14元/张 | [新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)：500张 有效期：百炼开通后90天内 |

目前通用图像编辑支持以下功能：

| **模型功能** | **输入图像** | **输入提示词** | **输出图像** |
| --- | --- | --- | --- |
| **全局风格化** | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 转换成法国绘本风格 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |
| **局部风格化** | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 把房子变成木板风格。 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |
| **指令编辑** | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 把女孩的头发修改为红色。 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |
| **局部重绘** | 输入图像 ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 涂抹区域图像（白色为涂抹区域） ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 一只陶瓷兔子抱着一朵陶瓷花。 | 输出图像 ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |
| **去文字水印** | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 去除图像中的文字。 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |
| **扩图** | ![20250319105917](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 一位绿色仙子。 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |
| **图像超分** | 模糊图像 ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 图像超分。 | 清晰图像 ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |
| **图像上色** | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 蓝色背景，黄色的叶子。 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |
| **线稿生图** | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 北欧极简风格的客厅。 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |
| **垫图** | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 卡通形象小心翼翼地探出头，窥视着房间内一颗璀璨的蓝色宝石。 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |

### **万相涂鸦作画**

基于输入的手绘图加文字描述，即可生成精美的涂鸦绘画作品。[API参考](https://help.aliyun.com/zh/model-studio/wanx-sketch-to-image-api-reference)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **示例输入** | **示例输出** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| wanx-sketch-to-image-lite | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 提示词：一棵参天大树 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 0.06元/张 | 500张 有效期：百炼开通后90天内 |

### **万相图像局部重绘**

根据用户输入的原始图片和局部涂抹图、prompt提示词文字内容，生成符合语义描述的多样化风格的局部重绘图像。[API参考](https://help.aliyun.com/zh/model-studio/vary-region-api-reference)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **示例输入** | **示例输出** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| wanx-x-painting | ![output16](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 布局涂抹图： ![output30](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 提示词：一只狗戴着红色眼镜 | ![output17](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)或[图像编辑-万相2.5](https://help.aliyun.com/zh/model-studio/wan-image-edit-2-5)获取替代方案。 | 500张 有效期：百炼开通后90天内 |

### **人像风格重绘**

人像风格重绘可以将输入的人物图像进行多种风格化的重绘生成，使新生成的图像在兼顾原始人物相貌的同时，带来不同风格的绘画效果。[API参考](https://help.aliyun.com/zh/model-studio/portrait-style-redraw-api-reference)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **示例输入** | **示例输出** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| wanx-style-repaint-v1 | ![o1](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 风格：清雅国风 | ![o2](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 0.12元/张 | 500张 有效期：百炼开通后90天内 |

### **图像背景生成**

图像背景生成可以基于输入的前景图像素材拓展生成背景信息，实现自然的光影融合效果，与细腻的写实画面生成。支持文本描述、图像引导等多种方式，同时支持对生成的图像智能添加文字内容。[API参考](https://help.aliyun.com/zh/model-studio/wanx-background-generation-api-reference)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **示例输入** | **示例输出** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| wanx-background-generation-v2 | ![output19](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 提示词：在桌面上，旁边有插着花朵的花瓶，背后是纯色高级的背景墙。 | ![output20](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 0.08元/张 | 500张 有效期：百炼开通后90天内 |

### **图像画面扩展**

图像画面大模型，对输入图像进行画面自由扩展，支持旋转画面，支持按照扩展系数和扩展像素数两种方式进行扩图。用户可以通过指定宽度、高度画面扩展比例或者左、右、上、下的扩展的像素值来控制画面扩展，可用于创意娱乐、辅助作图、画面设计、影视后期制作等场景。[API参考](https://help.aliyun.com/zh/model-studio/image-scaling-api)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **示例输入** | **示例输出** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| image-out-painting | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 0.18元/张 | 500张 有效期：百炼开通后90天内 |

### 人物实例分割

输入人物图像，模型识别出图像中的不同人物对象并画出每个对象边界的像素级掩码。[API参考](https://help.aliyun.com/zh/model-studio/image-instance-segmentation-api-reference)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **示例输入** | **示例输出** | **单价** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| image-instance-segmentation | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 输出结果1：像素级掩码图像 ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 输出结果2：可视化图像 ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 目前仅供免费体验。 > 免费额度用完后不可调用，敬请关注后续动态。 | 500张 有效期：百炼开通后90天内 |

### 图像擦除补全

输入图像并指定待擦除区域掩码图像以及保留区域掩码图像，模型在保留原图背景的同时擦除指定图像区域。[API参考](https://help.aliyun.com/zh/model-studio/image-erase-completion-api-reference)

针对人物图像的擦除、补全，推荐通过人物实例分割得到图像中不同人物对象的图像掩码，选择完整的人物图像掩码擦除一个或多个人物。

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **示例输入** | **示例输出** | **单价** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| image-erase-completion | 原图 ![图片擦除2-原图.png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 待擦除区域 ![图片擦除2-擦除.png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 保留区域 ![图片擦除2-保留.png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 输出图像 ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)或[图像编辑-万相2.5](https://help.aliyun.com/zh/model-studio/wan-image-edit-2-5)获取替代方案。 | 500张 有效期：百炼开通后90天内 |

### **虚拟模特**

可以对上传的真人实拍商品展示图进行智能生成，将其中的模特和背景替换为心仪的内容，在保持人物姿态不变的情况下，使用虚拟模特对商品进行更加精美、多样的展示。支持各种与模特产生互动的商品，如手持小商品、服装、鞋靴、配饰等。[API参考](https://help.aliyun.com/zh/model-studio/virtual-model-api-details)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **模型简介** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| wanx-virtualmodel | V1  | - 支持真人实拍图上传 - 图片短边：512像素或1024像素 | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)或[图像编辑-万相2.5](https://help.aliyun.com/zh/model-studio/wan-image-edit-2-5)获取替代方案。 | 500张 有效期：百炼开通后90天内 |
| virtualmodel-v2 | V2  | - 支持真人、人台实拍图上传 - 图片短边为：1024像素或2048像素 - 支持改变图片的长宽比 - 文本引导效果更准确 |

| **输入图** | **参数配置** | **输出图** |
| --- | --- | --- |
| v1 真人图 ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | "prompt":"一位年轻男性站着摆拍，在空荡的卧室里，窗户旁边，阳光照射进来，highly detailed，8K，极简主义风格" "face\\_prompt":"英俊的男性，脸好，脸美，质量上乘，杰作，（逼真度：1.4）" "predefined\\_face\\_id":"boy3" | v1输出 ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |
| v2人台图 ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | "prompt":"A woman stands beside a luxurious swimming pool, her attire and posture suggesting leisure and relaxation. The pool's calm, crystal-clear waters reflect the surrounding opulent setting, with elegant lounge chairs inviting moments of repose under the sun. Perhaps it's a high-end resort or an upscale private villa, where the tiled pool deck and meticulously landscaped greenery speak of exclusivity and refinement." "face\\_prompt":"good face, beautiful face, best quality." "aspect\\_ratio":"4:3" "realPerson":false | v2输出 ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |

### **鞋靴模特**

鞋靴模特支持输入多视角鞋靴系列图片，同时对输入模特模板图的鞋子区域进行鞋靴AI试穿，实现模特鞋靴布局重绘生成，最终生成图片的效果，布局自然、细节丰富、画面细腻、试穿结果逼真。可用于模特商品图设计、新鞋AI试穿、模特穿戴布局重绘等场景。[API参考](https://help.aliyun.com/zh/model-studio/shoe-model-api)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **示例输入** | **示例输出** | **单价** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| shoemodel-v1 | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 目前仅供免费体验。 > 免费额度用完后不可调用，敬请关注后续动态。 | 500张 有效期：百炼开通后90天内 |

### **创意海报生成**

根据您的要求自动生成海报的背景和文字排版，支持多种海报风格。无需设计基础，轻松制作出彩作品，让创意触手可及。[API参考](https://help.aliyun.com/zh/model-studio/creative-poster-generation-api)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **示例输入** | **示例输出** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| wanx-poster-generation-v1 | "title":"元宵节", "sub\\_title":"正月十五", "body\\_text":"团圆时节，汤圆香甜，祝你幸福美满！", "prompt\\_text\\_zh":"灯笼，小猫，梅花", "wh\\_ratios":"竖版", "lora\\_name":"童话油画", | ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)或[图像编辑-万相2.5](https://help.aliyun.com/zh/model-studio/wan-image-edit-2-5)获取替代方案。 | 500张 有效期：百炼开通后90天内 |

### **人物写真生成-**FaceChain

-   人物图像检测：对用户上传的人物图像进行检测，判断其中所包含的人脸是否符合Facechain微调所需的标准，检测维度包括人脸数量、大小、角度、光照、清晰度等多维度，支持图像组输入，并返回每张图像对应的检测结果。[API参考](https://help.aliyun.com/zh/model-studio/facechain-face-detection-api)
    
-   人物形象训练：对上传的图像进行模型训练，从而获得该图像中对应人物的resource，基于该resource可以实现人物的写真生成。[API参考](https://help.aliyun.com/zh/model-studio/facechain-finetune-api)
    
-   人物写真生成：基于人物形象训练已经得到的形象，可以继续通过人物生成写真模型完成该形象的写真生成，支持多种预设风格，包括证件照、商务写真等。[API参考](https://help.aliyun.com/zh/model-studio/facechain-generation)
    

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **说明** | **示例输入** | **示例输出** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| facechain-facedetect | 人物图像检测 | ![output21](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 风格：商务写真 | ![output22](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 限时免费 | 限时免费 |
| facechain-finetune | 人物形象训练 | 2.5元/次 | 50次 有效期：申请通过后90天内 |
| facechain-generation | 人物写真生成 | 0.18元/张 | 500张 有效期：申请通过后90天内 |

### **创意文字生成-**WordArt锦书

-   文字纹理生成：可以对输入的文字内容或文字图片进行创意设计，根据提示词内容对文字添加材质和纹理，实现立体凸显或场景融合的效果，生成效果精美、风格多样的艺术字，结合背景可以直接作为文字海报使用。[API参考](https://help.aliyun.com/zh/model-studio/fill-texture-effect-api)
    
-   文字变形：可以对输入的文字边缘轮廓进行创意变形，根据提示词内容进行边缘变化，实现一种字体的更多种创意用法，返回带有文字内容的黑底白色mask图。[API参考](https://help.aliyun.com/zh/model-studio/word-transformer)
    

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **说明** | **示例输入** | **示例输出** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| wordart-texture | 文字纹理生成 | ![output23](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 提示词：精美玉石 风格类型：立体材质 | ![output24](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 0.08元/张 | 各500张 有效期：百炼开通后90天内 |
| wordart-semantic | 文字变形 | 文字：桂林山水 提示词：山峦叠嶂、漓江蜿蜒、岩石奇秀 | ![output25](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 0.24元/张 |

### **AI试衣**

-   AI试衣-基础版是一款虚拟试衣图片生成模型，基于人像照片及服装图生成穿着后的试衣图片。[API参考](https://help.aliyun.com/zh/model-studio/outfitanyone-api) | [在线体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/vision?currentTab=imageGenerate)
    
-   AI试衣-Plus版相较于基础版模型，在图片清晰度、服饰纹理细节和logo还原效果等方面均有提升，但生成耗时较长，适用于对时效性要求不高的场景。[API参考](https://help.aliyun.com/zh/model-studio/aitryon-plus-api) | [在线体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/vision?currentTab=imageGenerate)
    
-   AI试衣-图片分割支持对模特图、服饰图进行分割，可用于AI试衣图片的前后处理。[API参考](https://help.aliyun.com/zh/model-studio/aitryon-parsing-api)
    
-   AI试衣-图片精修是对AI试衣生成的效果图进行二次生成，输出还原度更高的精修试衣效果图。[API参考](https://help.aliyun.com/zh/model-studio/ai-fitting-picture-finishing-api-details)
    

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **说明** | **示例输入** | **示例输出** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| aitryon | AI试衣-基础版 | ![output26](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | ![output29](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 各400张 有效期：百炼开通后90天内 |
| aitryon-plus | AI试衣-Plus版 |
| aitryon-parsing-v1 | AI试衣-图片分割 |
| aitryon-refiner | AI试衣-图片精修 | 100张 有效期：百炼开通后90天内 |

**AI试衣计费单价**

| **模型服务** | **模型名称** | **计量单价** | **折扣** | **阶梯层级** |
| --- | --- | --- | --- | --- |
| AI试衣-基础版 | aitryon | 0.20元/张 | 无   | 无   |
| AI试衣-Plus版 | aitryon-plus | 0.50元/张 | 无   | 无   |
| AI试衣-图片分割 | aitryon-parsing-v1 | 0.004元/张 | 无   | 无   |
| AI试衣-图片精修 | aitryon-refiner | 0.30元/张 | 无   | 生成数量 ≤ 25张 |
| 0.275元/张 | 9.2折 | 25张 ＜ 生成数量 ≤ 125张 |
| 0.25元/张 | 8.4折 | 125张 ＜ 生成数量 ≤ 250张 |
| 0.225元/张 | 7.5折 | 250张 ＜ 生成数量 ≤ 1250张 |
| 0.2元/张 | 6.7折 | 1250张 ＜ 生成数量 ≤ 2500张 |
| 0.175元/张 | 5.8折 | 2500张 ＜ 生成数量 ≤ 2.5万张 |
| 0.15元/张 | 5折  | 生成数量 ＞ 2.5万张 |

## 图像生成-第三方模型

### **可灵-图像生成**

可灵-图像生成模型支持**文生图**、**参考图生图**两种任务。[API参考](https://help.aliyun.com/zh/model-studio/kling-image-generation-api-reference)

**说明**

-   仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。
    
-   中国内地部署模式的模型无免费额度。
    

| **模型名称** | **支持的能力** | **输出图像分辨率** | **输出单价** |
| kling/kling-v3-image-generation | - 文生图 - 参考图生图：仅支持单图 | 1K  | 0.2元/张 |
| 2K  | 0.2元/张 |
| kling/kling-v3-omni-image-generation | - 文生图 - 参考图生图：支持输入多图，输出组图 | 1K  | 0.2元/张 |
| 2K  | 0.2元/张 |
| 4K  | 0.4元/张 |

### **Stable Diffusion**

[API参考](https://help.aliyun.com/zh/model-studio/stable-diffusion-apis)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **说明** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| stable-diffusion-3.5-large | 具有8亿参数的多模态扩散变压器（MMDiT）文本到图像生成模型，具备卓越的图像质量和提示词匹配度，支持生成100万像素的高分辨率图像，且能够在普通消费级硬件上高效运行。相比于v1.5和xl，在图像质量、文本内容生成、复杂提示理解和资源效率方面均有显著提升。 | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐参考[文本生成图像](https://help.aliyun.com/zh/model-studio/text-to-image)获取替代方案 | 500张 有效期：申请通过后90天内 |
| stable-diffusion-3.5-large-turbo | 在stable-diffusion-3.5-large的基础上采用对抗性扩散蒸馏（ADD）技术的模型，具备更快的速度。 |
| stable-diffusion-xl | 相比v1.5做了重大改进，被认为是当前开源文生图模型的SOTA水准，具体改进包括：unet backbone是之前的3倍；增加了refinement模块用于改善生成图片的质量；更高效的训练技巧等。 |
| stable-diffusion-v1.5 | 通过clip模型将文本的embedding和图片embedding映射到相同空间，从而通过输入文本并结合unet的稳定扩散预测噪声的能力，生成图片。是一款基础的文生图模型，得到了业界广泛使用。 |

### **FLUX**

Black Forest Labs的开源文生图模型，尤其擅长生成包含文字、多主体、手部细节的图片。

[文生图FLUX](https://help.aliyun.com/zh/model-studio/flux-api-reference/) | [立即申请（flux-merged）](https://bailian.console.aliyun.com/#/model-market/detail/flux-merged) | [立即申请（flux-dev）](https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.bdd47d9dyPUeav#/model-market/detail/flux-dev) | [立即申请（flux-schnell）](https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.bdd47d9dyPUeav#/model-market/detail/flux-schnell)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **说明** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| flux-merged | 结合了flux-dev的深度和flux-schnell的快速执行。 | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐参考[文本生成图像](https://help.aliyun.com/zh/model-studio/text-to-image)获取替代方案 | 100张 有效期：百炼开通后90天内 |
| flux-dev | 开发者版，面向非商业应用，具有与专业版相近的图像质量和指令遵循能力，同时运行效率更高。 |
| flux-schnell | 快速版，轻量级模型。 |

## **语音合成（文本转语音）**

### **千问语音合成**

支持输入多语种混合文本，并流式输出音频。[使用方法](https://help.aliyun.com/zh/model-studio/qwen-tts)｜[API 参考](https://help.aliyun.com/zh/model-studio/qwen-tts-api)

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

##### **千问3-TTS-Instruct-Flash**

| **模型名称** | **版本** | **单价** | **最大输入字符数** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| qwen3-tts-instruct-flash > 当前能力等同 qwen3-tts-instruct-flash-2026-01-26 | 稳定版 | 0.8元/万字符 | 600 | 1万字符 有效期：阿里云百炼开通后90天内 |
| qwen3-tts-instruct-flash-2026-01-26 | 快照版 |

-   **支持的语种**：中文（普通话）、英文、西班牙语、俄语、意大利语、法语、韩语、日语、德语、葡萄牙语
    
-   **字符计算规则**：按输入的字符数计费，计算规则如下：
    
    -   一个汉字（包括简/繁体汉字、日文汉字和韩文汉字） = 2个字符
        
    -   其他，如一个英文字母、一个标点符号、一个空格 = 1个字符
        

##### **千问3-TTS-VD**

| **模型名称** | **版本** | **单价** | **最大输入字符数** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| qwen3-tts-vd-2026-01-26 | 快照版 | 0.8元/万字符 | 600 | 1万字符 有效期：阿里云百炼开通后90天内 |

-   **支持的语种**：中文（普通话）、英文、西班牙语、俄语、意大利语、法语、韩语、日语、德语、葡萄牙语
    
-   **字符计算规则**：按输入的字符数计费，计算规则如下：
    
    -   一个汉字（包括简/繁体汉字、日文汉字和韩文汉字） = 2个字符
        
    -   其他，如一个英文字母、一个标点符号、一个空格 = 1个字符
        

##### **千问3-TTS-VC**

| **模型名称** | **版本** | **单价** | **最大输入字符数** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| qwen3-tts-vc-2026-01-22 | 快照版 | 0.8元/万字符 | 600 | 1万字符 有效期：阿里云百炼开通后90天内 |

-   **支持的语种**：中文（普通话）、英文、西班牙语、俄语、意大利语、法语、韩语、日语、德语、葡萄牙语
    
-   **字符计算规则**：按输入的字符数计费，计算规则如下：
    
    -   一个汉字（包括简/繁体汉字、日文汉字和韩文汉字） = 2个字符
        
    -   其他，如一个英文字母、一个标点符号、一个空格 = 1个字符
        

##### 千问3-TTS-Flash

| **模型名称** | **版本** | **单价** | **最大输入字符数** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| qwen3-tts-flash > 当前能力等同 qwen3-tts-flash-2025-11-27 | 稳定版 | 0.8元/万字符 | 600 | 1万字符 有效期：阿里云百炼开通后90天内 |
| qwen3-tts-flash-2025-11-27 | 快照版 |
| qwen3-tts-flash-2025-09-18 | 快照版 | 2025年11月13日0点前开通阿里云百炼：2000字符 2025年11月13日0点后开通阿里云百炼：1万字符 有效期：阿里云百炼开通后90天内 |

-   **支持的语种**：中文（普通话、北京、上海、四川、南京、陕西、闽南、天津、粤语）、英文、西班牙语、俄语、意大利语、法语、韩语、日语、德语、葡萄牙语
    
-   **字符计算规则**：按输入的字符数计费，计算规则如下：
    
    -   一个汉字（包括简/繁体汉字、日文汉字和韩文汉字） = 2个字符
        
    -   其他，如一个英文字母、一个标点符号、一个空格 = 1个字符
        

##### 千问-TTS

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| qwen-tts > 当前与 qwen-tts-2025-04-10 能力相同 | 稳定版 | 8,192 | 512 | 7,680 | 1.6元 | 10元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen-tts-latest > 始终与最新快照版能力相同 | 最新版 |
| qwen-tts-2025-05-22 | 快照版 |
| qwen-tts-2025-04-10 |

音频转换为 Token 的规则：每1秒的音频对应 50个 Token 。若音频时长不足1秒，则按 50个 Token 计算。

#### **国际**

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

##### **千问3-TTS-Instruct-Flash**

| **模型名称** | **版本** | **单价** | **最大输入字符数** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| qwen3-tts-instruct-flash > 当前能力等同 qwen3-tts-instruct-flash-2026-01-26 | 稳定版 | 0.8元/万字符 | 600 | 无免费额度 |
| qwen3-tts-instruct-flash-2026-01-26 | 快照版 |

-   **支持的语种**：中文（普通话）、英文、西班牙语、俄语、意大利语、法语、韩语、日语、德语、葡萄牙语
    
-   **字符计算规则**：按输入的字符数计费，计算规则如下：
    
    -   一个汉字（包括简/繁体汉字、日文汉字和韩文汉字） = 2个字符
        
    -   其他，如一个英文字母、一个标点符号、一个空格 = 1个字符
        

##### **千问3-TTS-VD**

| **模型名称** | **版本** | **单价** | **最大输入字符数** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| qwen3-tts-vd-2026-01-26 | 快照版 | 0.8元/万字符 | 600 | 无免费额度 |

-   **支持的语种**：中文（普通话）、英文、西班牙语、俄语、意大利语、法语、韩语、日语、德语、葡萄牙语
    
-   **字符计算规则**：按输入的字符数计费，计算规则如下：
    
    -   一个汉字（包括简/繁体汉字、日文汉字和韩文汉字） = 2个字符
        
    -   其他，如一个英文字母、一个标点符号、一个空格 = 1个字符
        

##### **千问3-TTS-VC**

| **模型名称** | **版本** | **单价** | **最大输入字符数** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| qwen3-tts-vc-2026-01-22 | 快照版 | 0.8元/万字符 | 600 | 无免费额度 |

-   **支持的语种**：中文（普通话）、英文、西班牙语、俄语、意大利语、法语、韩语、日语、德语、葡萄牙语
    
-   **字符计算规则**：按输入的字符数计费，计算规则如下：
    
    -   一个汉字（包括简/繁体汉字、日文汉字和韩文汉字） = 2个字符
        
    -   其他，如一个英文字母、一个标点符号、一个空格 = 1个字符
        

##### 千问3-TTS-Flash

| **模型名称** | **版本** | **单价** | **最大输入字符数** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| qwen3-tts-flash > 当前能力等同 qwen3-tts-flash-2025-11-27 | 稳定版 | 0.733924元/万字符 | 600 | 无免费额度 |
| qwen3-tts-flash-2025-11-27 | 快照版 |
| qwen3-tts-flash-2025-09-18 | 快照版 |

-   **支持的语种**：中文（普通话、北京、上海、四川、南京、陕西、闽南、天津、粤语）、英文、西班牙语、俄语、意大利语、法语、韩语、日语、德语、葡萄牙语
    
-   **字符计算规则**：按输入的字符数计费，计算规则如下：
    
    -   一个汉字（包括简/繁体汉字、日文汉字和韩文汉字） = 2个字符
        
    -   其他，如一个英文字母、一个标点符号、一个空格 = 1个字符
        

### **千问实时语音合成**

支持文本的流式输入并流式输出音频，具有根据文本内容与标点符号自适应调节语音语速的能力。[使用方法](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-api-reference/)

千问3-TTS-Instruct-Flash-Realtime支持[指令控制](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime#12884a10929p9)，仅可使用默认音色，不支持使用声音复刻/设计音色。

千问3-TTS-VD-Realtime支持使用[声音设计（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design)音色进行实时语音合成，但不支持使用默认音色。

千问3-TTS-VC-Realtime支持使用[声音复刻（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning)音色进行实时语音合成，但不支持使用默认音色。

千问3-TTS-Flash-Realtime和千问-TTS-Realtime仅可使用默认音色，但不支持使用声音复刻/设计音色。

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

##### **千问3-TTS-Instruct-Flash-Realtime**

| **模型名称** | **版本** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-tts-instruct-flash-realtime > 当前能力等同 qwen3-tts-instruct-flash-realtime-2026-01-22 | 稳定版 | 1元/万字符 | 1万字符 有效期：阿里云百炼开通后90天内 |
| qwen3-tts-instruct-flash-realtime-2026-01-22 | 快照版 |

-   **支持的语种**：中文（普通话）、英文、西班牙语、俄语、意大利语、法语、韩语、日语、德语、葡萄牙语
    
-   **字符计算规则**：按输入的字符数计费，计算规则如下：
    
    -   一个汉字（包括简/繁体汉字、日文汉字和韩文汉字） = 2个字符
        
    -   其他，如一个英文字母、一个标点符号、一个空格 = 1个字符
        

##### 千问3-TTS-VD-Realtime

| **模型名称** | **版本** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-tts-vd-realtime-2026-01-15 | 快照版 | 1元/万字符 | 1万字符 有效期：阿里云百炼开通后90天内 |
| qwen3-tts-vd-realtime-2025-12-16 | 快照版 |

-   **支持的语种**：中文（普通话）、英文、西班牙语、俄语、意大利语、法语、韩语、日语、德语、葡萄牙语
    
-   **字符计算规则**：按输入的字符数计费，计算规则如下：
    
    -   一个汉字（包括简/繁体汉字、日文汉字和韩文汉字） = 2个字符
        
    -   其他，如一个英文字母、一个标点符号、一个空格 = 1个字符
        

##### 千问3-TTS-VC-Realtime

| **模型名称** | **版本** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-tts-vc-realtime-2026-01-15 | 快照版 | 1元/万字符 | 1万字符 有效期：阿里云百炼开通后90天内 |
| qwen3-tts-vc-realtime-2025-11-27 | 快照版 |

-   **支持的语种**：中文（普通话）、英文、西班牙语、俄语、意大利语、法语、韩语、日语、德语、葡萄牙语
    
-   **字符计算规则**：按输入的字符数计费，计算规则如下：
    
    -   一个汉字（包括简/繁体汉字、日文汉字和韩文汉字） = 2个字符
        
    -   其他，如一个英文字母、一个标点符号、一个空格 = 1个字符
        

##### 千问3-TTS-Flash-Realtime

| **模型名称** | **版本** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-tts-flash-realtime > 当前能力等同 qwen3-tts-flash-realtime-2025-11-27 | 稳定版 | 1元/万字符 | 1万字符 有效期：阿里云百炼开通后90天内 |
| qwen3-tts-flash-realtime-2025-11-27 | 快照版 |
| qwen3-tts-flash-realtime-2025-09-18 | 快照版 | 2025年11月13日0点前开通阿里云百炼：2000字符 2025年11月13日0点后开通阿里云百炼：1万字符 有效期：阿里云百炼开通后90天内 |

-   **支持的语种**：中文（普通话、北京、上海、四川、南京、陕西、闽南、天津、粤语）、英文、西班牙语、俄语、意大利语、法语、韩语、日语、德语、葡萄牙语
    
-   **字符计算规则**：按输入的字符数计费，计算规则如下：
    
    -   一个汉字（包括简/繁体汉字、日文汉字和韩文汉字） = 2个字符
        
    -   其他，如一个英文字母、一个标点符号、一个空格 = 1个字符
        

##### 千问-TTS-Realtime

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **支持的语种** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| qwen-tts-realtime > 当前能力等同 qwen-tts-realtime-2025-07-15 | 稳定版 | 8,192 | 512 | 7,680 | 2.4元 | 12元 | 中文、英文 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen-tts-realtime-latest > 当前能力等同 qwen-tts-realtime-2025-07-15 | 最新版 | 中文、英文 |
| qwen-tts-realtime-2025-07-15 | 快照版 | 中文、英文 |

音频转换为 Token 的规则：每1秒的音频对应 50个 Token 。若音频时长不足1秒，则按 50个 Token 计算。

#### **国际**

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

##### **千问3-TTS-Instruct-Flash-Realtime**

| **模型名称** | **版本** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-tts-instruct-flash-realtime > 当前能力等同 qwen3-tts-instruct-flash-realtime-2026-01-22 | 稳定版 | 1元/万字符 | 无免费额度 |
| qwen3-tts-instruct-flash-realtime-2026-01-22 | 快照版 |

-   **支持的语种**：中文（普通话）、英文、西班牙语、俄语、意大利语、法语、韩语、日语、德语、葡萄牙语
    
-   **字符计算规则**：按输入的字符数计费，计算规则如下：
    
    -   一个汉字（包括简/繁体汉字、日文汉字和韩文汉字） = 2个字符
        
    -   其他，如一个英文字母、一个标点符号、一个空格 = 1个字符
        

##### 千问3-TTS-VD-Realtime

| **模型名称** | **版本** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-tts-vd-realtime-2026-01-15 | 快照版 | 0.954101元/万字符 | 无免费额度 |
| qwen3-tts-vd-realtime-2025-12-16 | 快照版 |

-   **支持的语种**：中文（普通话）、英文、西班牙语、俄语、意大利语、法语、韩语、日语、德语、葡萄牙语
    
-   **字符计算规则**：按输入的字符数计费，计算规则如下：
    
    -   一个汉字（包括简/繁体汉字、日文汉字和韩文汉字） = 2个字符
        
    -   其他，如一个英文字母、一个标点符号、一个空格 = 1个字符
        

##### 千问3-TTS-VC-Realtime

| **模型名称** | **版本** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-tts-vc-realtime-2026-01-15 | 快照版 | 0.954101元/万字符 | 无免费额度 |
| qwen3-tts-vc-realtime-2025-11-27 | 快照版 |

-   **支持的语种**：中文（普通话）、英文、西班牙语、俄语、意大利语、法语、韩语、日语、德语、葡萄牙语
    
-   **字符计算规则**：按输入的字符数计费，计算规则如下：
    
    -   一个汉字（包括简/繁体汉字、日文汉字和韩文汉字） = 2个字符
        
    -   其他，如一个英文字母、一个标点符号、一个空格 = 1个字符
        

##### 千问3-TTS-Flash-Realtime

| **模型名称** | **版本** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-tts-flash-realtime > 当前能力等同 qwen3-tts-flash-realtime-2025-11-27 | 稳定版 | 0.954101元/万字符 | 无免费额度 |
| qwen3-tts-flash-realtime-2025-11-27 | 快照版 |
| qwen3-tts-flash-realtime-2025-09-18 | 快照版 |

-   **支持的语种**：中文（普通话、北京、上海、四川、南京、陕西、闽南、天津、粤语）、英文、西班牙语、俄语、意大利语、法语、韩语、日语、德语、葡萄牙语
    
-   **字符计算规则**：按输入的字符数计费，计算规则如下：
    
    -   一个汉字（包括简/繁体汉字、日文汉字和韩文汉字） = 2个字符
        
    -   其他，如一个英文字母、一个标点符号、一个空格 = 1个字符
        

### **千问声音复刻**

声音复刻依托大模型进行特征提取，无需训练即可复刻声音。仅需提供 10~20 秒的音频，即可生成高度相似且听感自然的定制音色。[使用方法](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning)

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| qwen-voice-enrollment | 0.01元/音色 | 1000个音色 有效期：阿里云百炼开通后90天内 |

#### **国际**

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| qwen-voice-enrollment | 0.01元/音色 | 无免费额度 |

### **千问声音设计**

声音设计通过文本描述生成定制化音色，支持多语言和多维度音色特征定义，适用于广告配音、角色塑造、有声内容创作等多种应用。[使用方法](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design)

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| qwen-voice-design | 0.2元/音色 | 10个音色 有效期：阿里云百炼开通后90天内 |

#### **国际**

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| qwen-voice-design | 0.2元/音色 | 无免费额度 |

### CosyVoice语音合成

CosyVoice是阿里云依托大规模预训练语言模型，深度融合文本理解和语音生成的新一代生成式语音合成大模型，支持文本至语音的实时流式合成。[使用方法](https://help.aliyun.com/zh/model-studio/text-to-speech) | [API参考](https://help.aliyun.com/zh/model-studio/cosyvoice-large-model-for-speech-synthesis/)

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| cosyvoice-v3.5-plus | 1.5元/万字符 | 1万字符 有效期：阿里云百炼开通后90天内 |
| cosyvoice-v3.5-flash | 0.8元/万字符 |
| cosyvoice-v3-plus | 2元/万字符 |
| cosyvoice-v3-flash | 1元/万字符 |
| cosyvoice-v2 | 2元/万字符 |
| cosyvoice-v1 |

字符计算规则：汉字（包括简/繁体汉字、日文汉字和韩文汉字）按2个字符计算，其他所有字符（如字母、数字、日韩文假名/谚文等）均按 1个字符计算。SSML标签内容不计费。

#### **国际**

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| cosyvoice-v3-plus | 1.9082元/万字符 | 无免费额度 |
| cosyvoice-v3-flash | 0.9541元/万字符 |

字符计算规则：汉字（包括简/繁体汉字、日文汉字和韩文汉字）按2个字符计算，其他所有字符（如字母、数字、日韩文假名/谚文等）均按 1个字符计算。SSML标签内容不计费。

### **Sambert语音合成**

Sambert语音合成API基于达摩院改良的自回归韵律模型，支持文本至语音的实时流式合成。[使用方法](https://help.aliyun.com/zh/model-studio/text-to-speech) | [API参考](https://help.aliyun.com/zh/model-studio/sambert-speech-synthesis/)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| 参见[模型（音色）列表](https://help.aliyun.com/zh/model-studio/sambert-java-sdk#57d33631f7doi) | 1元/万字符 > 根据待合成字符数计费（其中1个汉字算2个字符，英文、标点符号、空格均按照1个字符计费）。SSML标签内容不计费。 | 每主账号每模型每月3万字符。 |

### **MiniMax语音合成**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **语音合成单价（每万字符）** | [复刻一个音色](https://help.aliyun.com/zh/model-studio/mini-clone-api) | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| MiniMax/speech-2.8-hd | 3.5元 | 9.9元 （在首次使用复刻出来的音色进行语音合成的时候收取） | 无   |
| MiniMax/speech-02-hd | 3.5元 |
| MiniMax/speech-2.8-turbo | 2元  |
| MiniMax/speech-02-turbo | 2元  |

## **语音识别（语音转文本）与翻译（语音转成指定语种的文本）**

### 千问3-LiveTranslate-Flash

千问3-LiveTranslate-Flash 是基于 Qwen3-Omni 架构的音视频翻译模型，支持 18 种语言（包括中文、英文、俄文、法文等）互译。该模型可结合视觉上下文提升翻译准确性，并输出文本与语音。[使用方法](https://help.aliyun.com/zh/model-studio/qwen3-livetranslate-flash)｜[API 参考](https://help.aliyun.com/zh/model-studio/qwen3-livetranslate-flash-api)

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |
| **qwen3-livetranslate-flash** > 当前能力等同于qwen3-livetranslate-flash-2025-12-01 | 稳定版 | 53,248 | 49,152 | 4,096 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen3-livetranslate-flash-2025-12-01 | 快照版 |

免费额度用完后，输入与输出的计费规则如下：

| \\| **输入计费项** \\| **单价（每百万 Token）** \\| \\| --- \\| --- \\| \\| 音频 \\| 10元 \\| \\| 视频 > 音频部分单独计费。 \\| 4元 \\| | \\| **输出计费项** \\| **单价（每百万 Token）** \\| \\| --- \\| --- \\| \\| 音频 \\| 40元 \\| \\| 文本 \\| 10元 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

#### **国际**

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |
| **qwen3-livetranslate-flash** > 当前能力等同于qwen3-livetranslate-flash-2025-12-01 | 稳定版 | 53,248 | 49,152 | 4,096 | 无免费额度 |
| qwen3-livetranslate-flash-2025-12-01 | 快照版 |

输入与输出的计费规则如下：

| \\| **输入计费项** \\| **单价（每百万 Token）** \\| \\| --- \\| --- \\| \\| 音频 \\| 11.573元 \\| \\| 视频 > 音频部分单独计费。 \\| 4.629元 \\| | \\| **输出计费项** \\| **单价（每百万 Token）** \\| \\| --- \\| --- \\| \\| 音频 \\| 46.292元 \\| \\| 文本 \\| 11.573元 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

### 千问3-LiveTranslate-Flash-Realtime

qwen3-livetranslate-flash-realtime 是一款多语言音视频实时翻译模型，可识别 18 种语言，并实时翻译为 10 种语言的音频。

**核心特性：**

-   **多语言支持**：支持 18 种语言及 6 种汉语方言。包括中文、英文、法语、德语、俄语、日语、韩语等。支持普通话、粤语、四川话等方言。
    
-   **视觉增强**：利用视觉内容提升翻译准确性。模型通过分析口型、动作和画面中的文字，改善在嘈杂环境下或一词多义场景中的翻译效果。
    
-   **3秒延迟**：实现低至 3 秒的同传延迟。
    
-   **无损同传**：通过语义单元预测技术，解决跨语言语序问题。实时翻译质量接近离线翻译结果。
    
-   **音色自然**：生成音色自然的拟人语音。模型能根据源语音内容，自适应调节语气和情感。
    

[使用方法](https://help.aliyun.com/zh/model-studio/qwen3-livetranslate-flash-realtime) | [API参考](https://help.aliyun.com/zh/model-studio/live-translator-api/)

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |
| **qwen3-livetranslate-flash-realtime** > 当前能力等同 qwen3-livetranslate-flash-realtime-2025-09-22 | 稳定版 | 53,248 | 49,152 | 4,096 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen3-livetranslate-flash-realtime-2025-09-22 | 快照版 |

免费额度用完后，输入与输出的计费规则如下：

| \\| **输入计费项** \\| **单价（每百万 Token）** \\| \\| --- \\| --- \\| \\| 输入：音频 \\| 64元 \\| \\| 输入：图片 \\| 8元 \\| | \\| **输出计费项** \\| **单价（每百万 Token）** \\| \\| --- \\| --- \\| \\| 文本 \\| 64元 \\| \\| 音频 \\| 240元 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

**Token计算规则：**

-   **音频**：输入或输出每秒音频均消耗 12.5 Token
    
-   **图片**：每输入 28\*28 像素消耗 0.5 Token
    

#### **国际**

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **版本** | **上下文长度** | **最大输入** | **最大输出** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |
| **qwen3-livetranslate-flash-realtime** > 当前能力等同 qwen3-livetranslate-flash-realtime-2025-09-22 | 稳定版 | 53,248 | 49,152 | 4,096 | 无免费额度 |
| qwen3-livetranslate-flash-realtime-2025-09-22 | 快照版 |

输入与输出的计费规则如下：

| \\| **输入计费项** \\| **单价（每百万 Token）** \\| \\| --- \\| --- \\| \\| 输入：音频 \\| 73.392元 \\| \\| 输入：图片 \\| 9.541元 \\| | \\| **输出计费项** \\| **单价（每百万 Token）** \\| \\| --- \\| --- \\| \\| 文本 \\| 73.392元 \\| \\| 音频 \\| 278.891元 \\| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

**Token计算规则：**

-   **音频**：输入或输出每秒音频均消耗 12.5 Token
    
-   **图片**：每输入 28\*28 像素消耗 0.5 Token
    

### **千问录音文件识别**

基于千问多模态基座，支持多语言识别、歌唱识别、噪声拒识等功能。[使用方法](https://help.aliyun.com/zh/model-studio/qwen-speech-recognition) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-asr-api-reference)

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

##### 千问3-ASR-Flash-Filetrans

| **模型名称** | **版本** | **单价** | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-asr-flash-filetrans > 当前等同qwen3-asr-flash-filetrans-2025-11-17 | 稳定版 | 0.00022元/秒 | 36,000秒（10小时） 有效期：阿里云百炼开通后90天内 |
| qwen3-asr-flash-filetrans-2025-11-17 | 快照版 |

-   **支持的语种**：中文（普通话、四川话、闽南语、吴语、粤语）、英语、日语、德语、韩语、俄语、法语、葡萄牙语、阿拉伯语、意大利语、西班牙语、印地语、印尼语、泰语、土耳其语、乌克兰语、越南语、捷克语、丹麦语、菲律宾语、芬兰语、冰岛语、马来语、挪威语、波兰语、瑞典语
    
-   **支持的采样率**：任意
    

##### **千问3-ASR-Flash**

| **模型名称** | **版本** | **单价** | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-asr-flash > 当前等同qwen3-asr-flash-2025-09-08 | 稳定版 | 0.00022元/秒 | 36,000秒（10小时） 有效期：阿里云百炼开通后90天内 |
| qwen3-asr-flash-2026-02-10 | 快照版 |
| qwen3-asr-flash-2025-09-08 | 快照版 |

-   **支持的语种**：中文（普通话、四川话、闽南语、吴语、粤语）、英语、日语、德语、韩语、俄语、法语、葡萄牙语、阿拉伯语、意大利语、西班牙语、印地语、印尼语、泰语、土耳其语、乌克兰语、越南语、捷克语、丹麦语、菲律宾语、芬兰语、冰岛语、马来语、挪威语、波兰语、瑞典语
    
-   **支持的采样率**：任意
    

**更多模型**

基于`Qwen-Audio`训练，支持中英文识别，不建议用于生产环境。

**Token计算规则：**每秒音频转换为25个Token，不足1秒按1秒计算。

| **模型名称** | **版本** | **支持的语言** | **支持的格式** | **支持的采样率** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| qwen-audio-asr | 稳定版 | 中文、英文 | 音频  | 16kHz | 8,192 | 6,144 | 2,048 | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐使用 Qwen3 ASR。 |   | 10万Token 有效期：阿里云百炼开通后90天内 |
| qwen-audio-asr-latest | 最新版 |

#### **国际**

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

##### 千问3-ASR-Flash-Filetrans

| **模型名称** | **版本** | **单价** | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-asr-flash-filetrans > 当前等同qwen3-asr-flash-filetrans-2025-11-17 | 稳定版 | 0.00026元/秒 | 无免费额度 |
| qwen3-asr-flash-filetrans-2025-11-17 | 快照版 |

-   **支持的语种**：中文（普通话、四川话、闽南语、吴语、粤语）、英语、日语、德语、韩语、俄语、法语、葡萄牙语、阿拉伯语、意大利语、西班牙语、印地语、印尼语、泰语、土耳其语、乌克兰语、越南语、捷克语、丹麦语、菲律宾语、芬兰语、冰岛语、马来语、挪威语、波兰语、瑞典语
    
-   **支持的采样率**：任意
    

##### **千问3-ASR-Flash**

| **模型名称** | **版本** | **单价** | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-asr-flash > 当前等同qwen3-asr-flash-2025-09-08 | 稳定版 | 0.00026元/秒 | 无免费额度 |
| qwen3-asr-flash-2026-02-10 | 快照版 |
| qwen3-asr-flash-2025-09-08 | 快照版 |

-   **支持的语种**：中文（普通话、四川话、闽南语、吴语、粤语）、英语、日语、德语、韩语、俄语、法语、葡萄牙语、阿拉伯语、意大利语、西班牙语、印地语、印尼语、泰语、土耳其语、乌克兰语、越南语、捷克语、丹麦语、菲律宾语、芬兰语、冰岛语、马来语、挪威语、波兰语、瑞典语
    
-   **支持的采样率**：任意
    

#### 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

| **模型名称** | **版本** | **单价** | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-asr-flash-us > 当前等同qwen3-asr-flash-2025-09-08-us | 稳定版 | 0.000035元/秒 | 无免费额度 |
| qwen3-asr-flash-2025-09-08-us | 快照版 |

-   **支持的语种**：中文（普通话、四川话、闽南语、吴语、粤语）、英语、日语、德语、韩语、俄语、法语、葡萄牙语、阿拉伯语、意大利语、西班牙语、印地语、印尼语、泰语、土耳其语、乌克兰语、越南语、捷克语、丹麦语、菲律宾语、芬兰语、冰岛语、马来语、挪威语、波兰语、瑞典语
    
-   **支持的采样率**：任意
    

### **千问实时语音识别**

千问实时语音识别大模型具备自动语种识别功能，可识别 11 种语音类型，并能在复杂音频环境下较为准确地转录。[使用方法](https://help.aliyun.com/zh/model-studio/qwen-real-time-speech-recognition) | [API参考](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-api/)

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **单价** | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-asr-flash-realtime > 当前等同qwen3-asr-flash-realtime-2025-10-27 | 稳定版 | 0.00033元/秒 | 36,000秒（10小时） 有效期：阿里云百炼开通后90天内 |
| qwen3-asr-flash-realtime-2026-02-10 | 快照版 |
| qwen3-asr-flash-realtime-2025-10-27 | 快照版 |

-   **支持的语种**：中文（普通话、四川话、闽南语、吴语、粤语）、英语、日语、德语、韩语、俄语、法语、葡萄牙语、阿拉伯语、意大利语、西班牙语、印地语、印尼语、泰语、土耳其语、乌克兰语、越南语、捷克语、丹麦语、菲律宾语、芬兰语、冰岛语、马来语、挪威语、波兰语、瑞典语
    
-   **支持的采样率**：8kHz、16kHz
    

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **版本** | **单价** | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-asr-flash-realtime > 当前等同qwen3-asr-flash-realtime-2025-10-27 | 稳定版 | 0.00066元/秒 | 无免费额度 |
| qwen3-asr-flash-realtime-2026-02-10 | 快照版 |
| qwen3-asr-flash-realtime-2025-10-27 | 快照版 |

-   **支持的语种**：中文（普通话、四川话、闽南语、吴语、粤语）、英语、日语、德语、韩语、俄语、法语、葡萄牙语、阿拉伯语、意大利语、西班牙语、印地语、印尼语、泰语、土耳其语、乌克兰语、越南语、捷克语、丹麦语、菲律宾语、芬兰语、冰岛语、马来语、挪威语、波兰语、瑞典语
    
-   **支持的采样率**：8kHz、16kHz
    

### **Gummy语音识别/翻译**

Gummy大模型支持实时语音识别与翻译，提供长语音识别/翻译与短语音（一句话）识别/翻译两个版本。

**长语音识别/翻译**

使用方法（[语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition)、[语音翻译](https://help.aliyun.com/zh/model-studio/real-time-speech-translation)） | [API参考](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-and-translation-api-reference/)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单价** | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| gummy-realtime-v1 | 0.00015元/秒 | 36,000秒（10小时） 2025年1月17日0点前开通阿里云百炼：有效期至2025年7月15日 2025年1月17日0点起至9月8日11点前开通阿里云百炼：自开通日起90天有效 2025年9月8日11点后开通阿里云百炼：自开通日起90天有效 |

-   **支持的语种**：
    
    -   **语音识别支持语种：**中文（普通话、粤语）、英文、日语、韩语、德语、法语、俄语、西班牙语、意大利语、葡萄牙语、印尼语、阿拉伯语、泰语
        
    -   **支持的翻译语言对：**
        
        -   中文（普通话） → 英 / 日 / 韩 / 法 / 德 / 西班牙 / 俄 / 意大利
            
        -   中文（粤语） → 中 （普通话）/ 英
            
        -   英文 → 中（普通话、粤语） / 日 / 韩 / 葡萄牙 / 法 / 德 / 俄 / 越南 / 西班牙 / 荷兰 / 丹麦 / 阿拉伯 / 意大利 / 印地 / 土耳其 / 马来 / 乌尔都
            
        -   日语 → 泰 / 英 / 中 （普通话）/ 越南 / 法 / 意大利 / 德 / 西班牙
            
        -   韩语 → 泰 / 英 / 中 （普通话）/ 越南 / 法 / 西班牙 / 俄 / 德
            
        -   法语 → 泰 / 英 / 日 / 中（普通话） / 越南 / 德 / 意大利 / 西班牙 / 俄 / 葡萄牙
            
        -   德语 → 泰 / 英 / 日 / 中 （普通话）/ 法 / 越南 / 俄 / 西班牙 / 意大利 / 葡萄牙
            
        -   西班牙语 → 泰 / 英 / 日 / 中（普通话） / 法 / 越南 / 意大利 / 德 / 俄 / 葡萄牙
            
        -   俄语 → 泰 / 英 / 日 / 中 （普通话、粤语）/ 法 / 越南 / 德 / 西班牙 / 意大利 / 葡萄牙
            
        -   意大利语 → 泰 / 英 / 日 / 中（普通话） / 法 / 越南 / 西班牙 / 俄 / 德
            
        -   葡萄牙语 → 英
            
        -   印尼语 → 英
            
        -   阿拉伯语 → 英
            
        -   泰语 → 日 / 越南 / 法
            
        -   印地语 → 英
            
        -   丹麦语 → 英
            
        -   乌尔都语 → 英
            
        -   土耳其语 → 英
            
        -   荷兰语 → 英
            
        -   马来语 → 英
            
        -   越南语 → 日 / 法
            
        
    
-   **支持的采样率**：16kHz及以上
    
-   **支持的音频格式**：pcm、wav、mp3、opus、speex、aac、amr
    

**短语音（一句话）识别/翻译**

使用方法（[语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition)、[语音翻译](https://help.aliyun.com/zh/model-studio/real-time-speech-translation)） | [API参考](https://help.aliyun.com/zh/model-studio/sentence-recognition-and-translation-api-reference/)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单价** | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| gummy-chat-v1 | 0.00015元/秒 | 36,000秒（10小时） 2025年1月17日0点前开通阿里云百炼：有效期至2025年7月15日 2025年1月17日0点起至9月8日11点前开通阿里云百炼：自开通日起90天有效 2025年9月8日11点后开通阿里云百炼：自开通日起90天有效 |

-   **支持的语种**：
    
    -   **语音识别支持语种：**中文（普通话、粤语）、英文、日语、韩语、德语、法语、俄语、西班牙语、意大利语、葡萄牙语、印尼语、阿拉伯语、泰语
        
    -   **支持的翻译语言对：**
        
        -   中文（普通话） → 英 / 日 / 韩 / 法 / 德 / 西班牙 / 俄 / 意大利
            
        -   中文（粤语） → 中 （普通话）/ 英
            
        -   英文 → 中（普通话、粤语） / 日 / 韩 / 葡萄牙 / 法 / 德 / 俄 / 越南 / 西班牙 / 荷兰 / 丹麦 / 阿拉伯 / 意大利 / 印地 / 土耳其 / 马来 / 乌尔都
            
        -   日语 → 泰 / 英 / 中 （普通话）/ 越南 / 法 / 意大利 / 德 / 西班牙
            
        -   韩语 → 泰 / 英 / 中 （普通话）/ 越南 / 法 / 西班牙 / 俄 / 德
            
        -   法语 → 泰 / 英 / 日 / 中（普通话） / 越南 / 德 / 意大利 / 西班牙 / 俄 / 葡萄牙
            
        -   德语 → 泰 / 英 / 日 / 中 （普通话）/ 法 / 越南 / 俄 / 西班牙 / 意大利 / 葡萄牙
            
        -   西班牙语 → 泰 / 英 / 日 / 中（普通话） / 法 / 越南 / 意大利 / 德 / 俄 / 葡萄牙
            
        -   俄语 → 泰 / 英 / 日 / 中 （普通话、粤语）/ 法 / 越南 / 德 / 西班牙 / 意大利 / 葡萄牙
            
        -   意大利语 → 泰 / 英 / 日 / 中（普通话） / 法 / 越南 / 西班牙 / 俄 / 德
            
        -   葡萄牙语 → 英
            
        -   印尼语 → 英
            
        -   阿拉伯语 → 英
            
        -   泰语 → 日 / 越南 / 法
            
        -   印地语 → 英
            
        -   丹麦语 → 英
            
        -   乌尔都语 → 英
            
        -   土耳其语 → 英
            
        -   荷兰语 → 英
            
        -   马来语 → 英
            
        -   越南语 → 日 / 法
            
        
    
-   **支持的采样率**：16kHz
    
-   **支持的音频格式**：pcm、wav、mp3、opus、speex、aac、amr
    

### **Fun-ASR语音识别**

Fun-ASR语音识别模型提供录音文件识别和实时语音识别两个版本。

**录音文件识别**

[使用方法](https://help.aliyun.com/zh/model-studio/recording-file-recognition) | [API参考](https://help.aliyun.com/zh/model-studio/fun-asr-recorded-speech-recognition-api-reference/)

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **单价** | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| fun-asr > 当前等同fun-asr-2025-11-07 | 稳定版 | 0.00022元/秒 | 36,000秒（10小时） 有效期：阿里云百炼开通后90天 |
| fun-asr-2025-11-07 > 相较fun-asr-2025-08-25做了远场VAD优化，识别更准 | 快照版 |
| fun-asr-2025-08-25 |
| fun-asr-mtl > 当前等同fun-asr-mtl-2025-08-25 | 稳定版 |
| fun-asr-mtl-2025-08-25 | 快照版 |

-   **支持的语种**：
    
    -   fun-asr、fun-asr-2025-11-07：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英文、日语
        
    -   fun-asr-2025-08-25：中文（普通话）、英文
        
    -   fun-asr-mtl、fun-asr-mtl-2025-08-25：中文（普通话、粤语）、英文、日语、韩语、越南语、印尼语、泰语、马来语、菲律宾语、阿拉伯语、印地语、保加利亚语、克罗地亚语、捷克语、丹麦语、荷兰语、爱沙尼亚语、芬兰语、希腊语、匈牙利语、爱尔兰语、拉脱维亚语、立陶宛语、马耳他语、波兰语、葡萄牙语、罗马尼亚语、斯洛伐克语、斯洛文尼亚语、瑞典语
        
-   **支持的采样率**：任意
    
-   **支持的音频格式**：aac、amr、avi、flac、flv、m4a、mkv、mov、mp3、mp4、mpeg、ogg、opus、wav、webm、wma、wmv
    

#### **国际**

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **版本** | **单价** | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| fun-asr > 当前等同fun-asr-2025-11-07 | 稳定版 | 0.00026元/秒 | 无免费额度 |
| fun-asr-2025-11-07 > 相较fun-asr-2025-08-25做了远场VAD优化，识别更准 | 快照版 |
| fun-asr-2025-08-25 |
| fun-asr-mtl > 当前等同fun-asr-mtl-2025-08-25 | 稳定版 |
| fun-asr-mtl-2025-08-25 | 快照版 |

-   **支持的语种**：
    
    -   fun-asr、fun-asr-2025-11-07：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英文、日语
        
    -   fun-asr-2025-08-25：中文（普通话）、英文
        
    -   fun-asr-mtl、fun-asr-mtl-2025-08-25：中文（普通话、粤语）、英文、日语、韩语、越南语、印尼语、泰语、马来语、菲律宾语、阿拉伯语、印地语、保加利亚语、克罗地亚语、捷克语、丹麦语、荷兰语、爱沙尼亚语、芬兰语、希腊语、匈牙利语、爱尔兰语、拉脱维亚语、立陶宛语、马耳他语、波兰语、葡萄牙语、罗马尼亚语、斯洛伐克语、斯洛文尼亚语、瑞典语
        
-   **支持的采样率**：任意
    
-   **支持的音频格式**：aac、amr、avi、flac、flv、m4a、mkv、mov、mp3、mp4、mpeg、ogg、opus、wav、webm、wma、wmv
    

**实时语音识别**

[使用方法](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition) | [API参考](https://help.aliyun.com/zh/model-studio/fun-asr-real-time-speech-recognition-api-reference/)

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **版本** | **单价** | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| fun-asr-realtime > 当前等同fun-asr-realtime-2025-11-07 | 稳定版 | 0.00033元/秒 | 36,000秒（10小时） 有效期：阿里云百炼开通后90天 |
| fun-asr-realtime-2026-02-28 | 快照版 |
| fun-asr-realtime-2025-11-07 | 快照版 |
| fun-asr-realtime-2025-09-15 |
| fun-asr-flash-8k-realtime > 当前等同fun-asr-flash-8k-realtime-2026-01-28 | 稳定版 | 0.00022元/秒 |
| fun-asr-flash-8k-realtime-2026-01-28 | 快照版 |

-   **支持的语种**：
    
    -   fun-asr-realtime、fun-asr-realtime-2026-02-28、fun-asr-realtime-2025-11-07：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英文、日语
        
    -   fun-asr-realtime-2025-09-15：中文（普通话）、英文
        
-   **支持的采样率**：
    
    -   fun-asr-flash-8k-realtime、fun-asr-flash-8k-realtime-2026-01-28：8kHz
        
    -   其他模型：16kHz
        
-   **支持的音频格式**：pcm、wav、mp3、opus、speex、aac、amr
    

#### **国际**

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **版本** | **单价** | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| fun-asr-realtime > 当前等同fun-asr-realtime-2025-11-07 | 稳定版 | 0.00066元/秒 | 无免费额度 |
| fun-asr-realtime-2025-11-07 | 快照版 |

-   **支持的语种**：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英文、日语
    
-   **支持的采样率**：16kHz
    
-   **支持的音频格式**：pcm、wav、mp3、opus、speex、aac、amr
    

### **Paraformer****语音识别**

Paraformer语音识别模型提供录音文件识别和实时语音识别两个版本。

**录音文件识别**

[使用方法](https://help.aliyun.com/zh/model-studio/recording-file-recognition) | [API参考](https://help.aliyun.com/zh/model-studio/paraformer-recorded-speech-recognition-api-reference/)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单价** | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| paraformer-v2 | 0.00008元/秒 | 36,000秒（10小时） 每月1日0点自动发放 有效期1个月 |
| paraformer-8k-v2 |
| paraformer-v1 |
| paraformer-8k-v1 |
| paraformer-mtl-v1 |

-   **支持的语种**：
    
    -   paraformer-v2：中文（普通话、粤语、吴语、闽南语、东北话、甘肃话、贵州话、河南话、湖北话、湖南话、宁夏话、山西话、陕西话、山东话、四川话、天津话、江西话、云南话、上海话）、英文、日语、韩语、德语、法语、俄语
        
    -   paraformer-8k-v2：中文普通话
        
    -   paraformer-v1：中文普通话、英文
        
    -   paraformer-8k-v1：中文普通话
        
    -   paraformer-mtl-v1：中文（普通话、粤语、吴语、闽南语、东北话、甘肃话、贵州话、河南话、湖北话、湖南话、宁夏话、山西话、陕西话、山东话、四川话、天津话）、英文、日语、韩语、西班牙语、印尼语、法语、德语、意大利语、马来语
        
-   **支持的采样率**：
    
    -   paraformer-v2：任意
        
    -   paraformer-8k-v2：8kHz
        
    -   paraformer-v1：任意
        
    -   paraformer-8k-v1：8kHz
        
    -   paraformer-mtl-v1：16kHz及以上
        
-   **支持的音频格式**：aac、amr、avi、flac、flv、m4a、mkv、mov、mp3、mp4、mpeg、ogg、opus、wav、webm、wma、wmv
    

**实时语音识别**

[使用方法](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition) | [API参考](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-api-reference/)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单价** | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| paraformer-realtime-v2 | 0.00024元/秒 | 36,000秒（10小时） 每月1日0点自动发放 有效期1个月 |
| paraformer-realtime-v1 |
| paraformer-realtime-8k-v2 |
| paraformer-realtime-8k-v1 |

-   **支持的语种**：
    
    -   paraformer-realtime-v2：中文（普通话、粤语、吴语、闽南语、东北话、甘肃话、贵州话、河南话、湖北话、湖南话、宁夏话、山西话、陕西话、山东话、四川话、天津话、江西话、云南话、上海话）、英文、日语、韩语、德语、法语、俄语
        
    -   paraformer-realtime-v1、paraformer-realtime-8k-v2、paraformer-realtime-8k-v1：中文普通话
        
-   **支持的采样率**：
    
    -   paraformer-realtime-v2：任意
        
    -   paraformer-realtime-v1：16kHz
        
    -   paraformer-realtime-8k-v2、paraformer-realtime-8k-v1：8kHz
        
-   **支持的音频格式**：pcm、wav、mp3、opus、speex、aac、amr
    

### **SenseVoice****语音识别**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

**录音文件识别**

专注于高精度多语言语音识别，还能识别情绪（高兴、悲伤、生气等）和特定事件（背景音乐、歌唱、掌声和笑声等）。[API参考](https://help.aliyun.com/zh/model-studio/sensevoice-api)

> 只识别并转写音频中的语音内容，非语音内容不计费。实际转写时长通常短于原始音频时长。由于采用AI判断，可能存在少许误差。

> 默认情况下，仅转写并计费多轨音频文件的首轨。若指定转写多个音轨，则各音轨按语音时长单独计费。

> 关于实际计费时长，请查看返回结果中的content\_duration\_in\_milliseconds字段。

| **模型名称** | **支持的语言** | **支持的格式** | **单价** | **免费额度** |
| --- | --- | --- | --- | --- |
| sensevoice-v1 | 超过50种语言（中、英、日、韩、粤等） [附录：支持语言列表](https://help.aliyun.com/zh/model-studio/supported-languages) | 音频或视频：aac、amr、avi、flac、flv、m4a、mkv、mov、mp3、mp4、mpeg、ogg、opus、wav、webm、wma、wmv | 0.0007 元/秒 | 36,000秒（10小时） 每月1日0点自动发放 有效期1个月 |

## **视频生成-万相与视频编辑**

### **文生视频**

万相-文生视频模型通过一句话即可生成视频，视频呈现丰富的艺术风格及影视级画质。[API参考](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference) ｜ [在线体验](https://bailian.console.aliyun.com/?spm=5176.30275541.J_ZGek9Blx07Hclc3Ddt9dg.4.51f82f3dFlj82T&scm=20140722.S_card%40%40%E4%BA%A7%E5%93%81%40%402983180.S_new%7EUND%7Ecard.ID_card%40%40%E4%BA%A7%E5%93%81%40%402983180-RL_%E7%99%BE%E7%82%BC%E5%B9%B3%E5%8F%B0-LOC_2024SPSearchCard-OR_ser-PAR1_215043cb17587857714454653ea60a-V_4-RE_new7-P0_0-P1_0&tab=demohouse#/experience/t2v)

计费规则：按成功生成的**视频秒数**计费，失败不计费也不占用免费额度。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **说明** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- | --- |
| wan2.6-t2v`**推荐**` | 万相2.6。新增多镜头叙事能力，同时支持自动配音和传入自定义音频文件。 | 720P：0.6元/秒 1080P：1元/秒 | 50秒 |
| wan2.5-t2v-preview`**推荐**` | 万相2.5 preview。支持自动配音和传入自定义音频文件。 | 480P：0.3元/秒 720P：0.6元/秒 1080P：1元/秒 | 50秒 |
| wan2.2-t2v-plus | 万相2.2专业版。指令理解更准，运动稳定流畅生成，生成细节更丰富。 | 480P：0.14元/秒 1080P：0.70元/秒 | 50秒 |
| wanx2.1-t2v-turbo | 万相2.1极速版。性价比高。 | 0.24元/秒 | 200秒 |
| wanx2.1-t2v-plus | 万相2.1专业版。画面更具质感。 | 0.70元/秒 | 200秒 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **说明** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota) |
| --- | --- | --- | --- |
| wan2.6-t2v `**推荐**` | 万相2.6。新增多镜头叙事能力，同时支持自动配音和传入自定义音频文件。 | 720P：0.6元/秒 1080P：1元/秒 | 无免费额度 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **说明** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota) |
| --- | --- | --- | --- |
| wan2.6-t2v`**推荐**` | 万相2.6。新增多镜头叙事能力，同时支持自动配音和传入自定义音频文件。 | 720P：0.733924元/秒 1080P：1.100886元/秒 | 无免费额度 |
| wan2.5-t2v-preview`**推荐**` | 万相2.5 preview。支持自动配音和传入自定义音频文件。 | 480P：0.366961元/秒 720P：0.733923元/秒 1080P：1.100885元/秒 | 无免费额度 |
| wan2.2-t2v-plus | 万相2.2专业版。在画面细节表现、运动稳定性方面均有显著提升。 | 480P：0.146785元/秒 1080P：0.733924元/秒 | 无免费额度 |
| wan2.1-t2v-turbo | 万相2.1极速版。生成速度快，表现均衡。 | 0.264213元/秒 | 无免费额度 |
| wan2.1-t2v-plus | 万相2.1专业版。生成细节丰富，画面更具质感。 | 0.733924元/秒 | 无免费额度 |

## 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

| **模型名称** | **说明** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota) |
| --- | --- | --- | --- |
| wan2.6-t2v-us `**推荐**` | 万相2.6。新增多镜头叙事能力，同时支持自动配音和传入自定义音频文件。 | 720P：0.733924元/秒 1080P：1.100886元/秒 | 无免费额度 |

| **输入提示词** | **输出视频（wan2.6，多镜头视频）** |
| --- | --- |
| 一幅史诗级可爱的场景。一只小巧可爱的卡通小猫将军，身穿细节精致的金色盔甲，头戴一个稍大的头盔，勇敢地站在悬崖上。他骑着一匹虽小但英勇的战马，说：**“青海长云暗雪山，孤城遥望玉门关。黄沙百战穿金甲，不破楼兰终不还”**。悬崖下方，一支由老鼠组成的、数量庞大、无穷无尽的军队正带着临时制作的武器向前冲锋。这是一个戏剧性的、大规模的战斗场景，灵感来自中国古代的战争史诗。远处的雪山上空，天空乌云密布。整体氛围是“可爱”与“霸气”的搞笑和史诗般的融合。 |     |

### **图生视频-基于首帧**

万相-图生视频模型将输入图片作为视频首帧，再根据提示词生成视频。视频呈现丰富的艺术风格及影视级画质。[API参考](https://help.aliyun.com/zh/model-studio/image-to-video-api-reference/) ｜ [在线体验](https://bailian.console.aliyun.com/?spm=5176.30275541.J_ZGek9Blx07Hclc3Ddt9dg.4.51f82f3dFlj82T&scm=20140722.S_card%40%40%E4%BA%A7%E5%93%81%40%402983180.S_new%7EUND%7Ecard.ID_card%40%40%E4%BA%A7%E5%93%81%40%402983180-RL_%E7%99%BE%E7%82%BC%E5%B9%B3%E5%8F%B0-LOC_2024SPSearchCard-OR_ser-PAR1_215043cb17587857714454653ea60a-V_4-RE_new7-P0_0-P1_0&tab=demohouse#/experience/t2v)

计费规则：按成功生成的**视频秒数**计费，失败不计费也不占用免费额度。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **说明** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- | --- |
| wan2.6-i2v-flash `**推荐**` | 万相2.6。新增多镜头叙事能力，同时支持自动配音和传入自定义音频文件。 | 输出有声视频`audio=true`： - 720P：0.3元/秒 - 1080P：0.5元/秒 输出无声视频`audio=false`： - 720P：0.15元/秒 - 1080P：0.25元/秒 | 50秒 |
| wan2.6-i2v `**推荐**` | 万相2.6。新增多镜头叙事能力，同时支持自动配音和传入自定义音频文件。 | 720P：0.6元/秒 1080P：1元/秒 | 50秒 |
| wan2.5-i2v-preview | 万相2.5 preview。支持自动配音和传入自定义音频文件。 | 480P：0.3元/秒 720P：0.6元/秒 1080P：1元/秒 | 50秒 |
| wan2.2-i2v-flash | 万相2.2极速版。 极致生成速度，指令理解与运镜控制更准，画面元素保持一致，稳定性与成功率全面提升。 | 480P：0.10元/秒 720P：0.20元/秒 1080P：0.48元/秒 | 50秒 |
| wan2.2-i2v-plus | 万相2.2专业版。 指令理解更准，运镜可控，画面元素保持一致，稳定性与成功率全面提升，生成内容更丰富。 | 480P：0.14元/秒 1080P：0.70元/秒 | 50秒 |
| wanx2.1-i2v-turbo | 万相2.1极速版。性价比高。 | 0.24元/秒 | 200秒 |
| wanx2.1-i2v-plus | 万相2.1专业版。画面更具质感。 | 0.70元/秒 | 200秒 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **说明** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota) |
| --- | --- | --- | --- |
| wan2.6-i2v `**推荐**` | 万相2.6。新增多镜头叙事能力，同时支持自动配音和传入自定义音频文件。 | 720P：0.6元/秒 1080P：1元/秒 | 无免费额度 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **说明** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota) |
| --- | --- | --- | --- |
| wan2.6-i2v-flash `**推荐**` | 万相2.6。新增多镜头叙事能力，同时支持自动配音和传入自定义音频文件。 | 输出有声视频`audio=true`： - 720P：0.366962元/秒 - 1080P：0.550443元/秒 输出无声视频`audio=false`： - 720P：0.183481元/秒 - 1080P：0.275221元/秒 | 无免费额度 |
| wan2.6-i2v`**推荐**` | 万相2.6。新增多镜头叙事能力，同时支持自动配音和传入自定义音频文件。 | 720P：0.733924元/秒 1080P：1.100886元/秒 | 无免费额度 |
| wan2.5-i2v-preview`**推荐**` | 万相2.5 preview。支持自动配音和传入自定义音频文件。 | 480P：0.366961元/秒 720P：0.733923元/秒 1080P：1.100885元/秒 | 无免费额度 |
| wan2.2-i2v-flash | 万相2.2极速版。极致生成速度，在画面细节表现、运动稳定性方面均有显著提升。 | 480P：0.110089元/秒 720P：0.264213元/秒 | 无免费额度 |
| wan2.2-i2v-plus | 万相2.2专业版。在画面细节表现、运动稳定性方面均有显著提升。 | 480P：0.146785元/秒 1080P：0.733924元/秒 | 无免费额度 |
| wan2.1-i2v-turbo | 万相2.1极速版。生成速度快，表现均衡。 | 0.264213元/秒 | 无免费额度 |
| wan2.1-i2v-plus | 万相2.1专业版。生成细节丰富，画面更具质感。 | 0.733924元/秒 | 无免费额度 |

## 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

| **模型名称** | **说明** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota) |
| --- | --- | --- | --- |
| wan2.6-i2v-us `**推荐**` | 万相2.6。新增多镜头叙事能力，同时支持自动配音和传入自定义音频文件。 | 720P：0.733924元/秒 1080P：1.100886元/秒 | 无免费额度 |

| **输入提示词** | **输入首帧图像和音频** | **输出视频（wan2.6，多镜头视频）** |
| --- | --- | --- |
| 一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。 | ![rap-转换自-png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 输入音频： |     |

### **图生视频-基于首尾帧**

万相-首尾帧生视频模型，只需要提供首帧和尾帧图片，便能根据提示词生成一段丝滑流畅的动态视频。[API参考](https://help.aliyun.com/zh/model-studio/image-to-video-by-first-and-last-frame-api-reference) ｜ [在线体验](https://tongyi.aliyun.com/wanxiang/videoCreation?spm=a2c4g.11186623.0.0.e2034d9f2BocA8)

计费规则：按成功生成的**视频秒数**计费，失败不计费也不占用免费额度。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **说明** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- | --- |
| wan2.2-kf2v-flash | 万相2.2极速版 | 480P：0.10元/秒 720P：0.20元/秒 1080P：0.48元/秒 | 50秒 |
| wanx2.1-kf2v-plus | 万相2.1专业版 | 720P：0.70元/秒 | 200秒 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota) |
| --- | --- | --- |
| wan2.1-kf2v-plus | 0.733924元/秒 | 无免费额度 |

| **输入示例** |   |   | **输出视频** |
| --- | --- | --- | --- |
| **首帧图片** | **尾帧图片** | **提示词** |
| ![first_frame](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | ![last_frame](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍小猫好奇的眼神。 |     |

### **参考生视频**

万相-参考生视频模型支持参考输入视频或图像中的角色形象，同时可参考视频中的音色，搭配提示词生成表演视频。[API参考](https://help.aliyun.com/zh/model-studio/wan-video-to-video-api-reference)

计费规则：输入视频和输出视频均计费，按**视频秒数**计费，失败不计费也不占用免费额度。

-   计费公式：计费时长 = 输入视频时长（上限 5 秒）+ 输出视频时长。
    
    -   输入视频的计费时长不超过 **5 秒**，计算规则参见[万相-参考生视频](https://help.aliyun.com/zh/model-studio/wan-video-to-video-api-reference#f79461ca408qn)。
        
    -   输出视频的计费时长为**成功生成的视频秒数**。
        
-   定价说明：计费单价由分辨率档位和 audio（是否输出有声视频）决定，与输入视频的实际分辨率或音频状态无关。
    

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输出视频类型** | **输入和输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota) |
| --- | --- | --- | --- |
| wan2.6-r2v-flash `**推荐**` | 有声视频 `audio=true` | 720P：0.3元/秒 1080P：0.5元/秒 | 50秒 有效期：百炼开通后90天内 |
| 无声视频 `audio=false` | 720P：0.15元/秒 1080P：0.25元/秒 |
| wan2.6-r2v | 有声视频 | 720P：0.6元/秒 1080P：1元/秒 | 50秒 有效期：百炼开通后90天内 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **输出视频类型** | **输入和输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota) |
| --- | --- | --- | --- |
| wan2.6-r2v | 有声视频 | 720P：0.6元/秒 1080P：1元/秒 | 无免费额度 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **输出视频类型** | **输入和输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota) |
| --- | --- | --- | --- |
| wan2.6-r2v-flash `**推荐**` | 有声视频 `audio=true` | 720P：0.366962元/秒 1080P：0.550443元/秒 | 无免费额度 |
| 无声视频 `audio=false` | 720P：0.183481元/秒 1080P：0.275221元/秒 |
| wan2.6-r2v | 有声视频 | 720P：0.733924元/秒 1080P：1.100886元/秒 | 无免费额度 |

### **通用视频编辑**

万相-视频编辑统一模型支持多模态输入，包括文本、图像和视频，能够执行视频生成与通用编辑任务。[API参考](https://help.aliyun.com/zh/model-studio/wanx-vace-api-reference)

计费规则：按成功生成的**视频秒数**计费，失败不计费也不占用免费额度。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota) |
| --- | --- | --- |
| wanx2.1-vace-plus | 0.70元/秒 | 50秒 有效期：百炼开通后90天内 |

## 国际

| **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota) |
| --- | --- | --- |
| wan2.1-vace-plus | 0.733924元/秒 | 无免费额度 |

| **模型功能** | **输入参考图** | **输入提示词** | **输出视频** |
| --- | --- | --- | --- |
| **多图参考** | 参考图1（参考主体） ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 参考图2（参考背景） ![image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 视频中，一位女孩自晨雾缭绕的**古老森林深处款款走出**，她步伐轻盈，镜头捕捉她每一个灵动瞬间。当女孩站定，环顾四周葱郁林木时，她**脸上绽放出惊喜与喜悦交织的笑容**。这一幕，定格在了光影交错的瞬间，记录下女孩与大自然的美妙邂逅。 | 输出视频 |
| **视频重绘** |     | 视频展示了一辆黑色的**蒸汽朋克风格汽车**，绅士驾驶着，车辆装饰着齿轮和铜管。背景是蒸汽驱动的糖果工厂和复古元素，画面复古与趣味 |     |
| **局部编辑** | 输入视频 输入掩码图像（白色区域表示编辑区域） ![mask](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | 视频展示了一家巴黎风情的法式咖啡馆，一只**穿着西装的狮子**优雅地品着咖啡。它一手端着咖啡杯，轻轻啜饮，神情惬意。咖啡馆装饰雅致，柔和的色调与温暖灯光映照着狮子所在的区域。 | 根据提示词修改编辑区域的内容 |
| **视频延展** | 输入首片段视频（1秒） | 一只戴着墨镜的**狗在街道上滑板**，3D卡通。 | 输出延长后的视频（5秒） |
| **视频画面扩展** |     | 一位优雅的女士正在激情演奏小提琴，**她身后是一支完整的交响乐团**。 |     |

### **万相-数字人**

基于单张人物图片和音频，生成动作自然的说话、唱歌或表演视频。使用时需依次调用下述模型。[wan2.2-s2v 图像检测](https://help.aliyun.com/zh/model-studio/wan-s2v-detect-api) | [wan2.2-s2v 视频生成](https://help.aliyun.com/zh/model-studio/wan-s2v-api)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **模型简介** | **计费单价** | **免费额度** |
| --- | --- | --- | --- |
| wan2.2-s2v-detect | 检查输入图像是否满足要求（如清晰度、单人、正面）。 | 0.004元/张 | [新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)：200张 有效期：阿里云百炼开通后90天内 |
| wan2.2-s2v | 根据检测通过的图片和一段音频，生成人物动态视频。 | 480P：0.5元/秒 720P：0.9元/秒 | [新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)：100秒 有效期：阿里云百炼开通后90天内 |

| **输入示例** | **输出视频** |
| --- | --- |
| ![p1001125-转换自-jpeg](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 输入音频： |     |

### 万相-图生动作

提供标准和专业两种服务模式，基于人物图片和参考视频，将视频角色的动作、表情迁移到图片角色中，生成人物动作视频，赋予图片角色动态表现力。[API参考](https://help.aliyun.com/zh/model-studio/wan-animate-move-api)

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **模型服务** | **服务简介** | **计费单价** | **免费额度**[（查看）](https://help.aliyun.com/zh/model-studio/new-free-quota) |
| --- | --- | --- | --- | --- |
| wan2.2-animate-move | 标准模式`wan-std` | 生成速度快，满足基础动画演示等轻需求，性价比高。 | 0.4元/秒 | 两种服务共50秒 |
| 专业模式`wan-pro` | 动画流畅度高，动作表情过渡自然，效果更接近真实拍摄。 | 0.6元/秒 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **模型服务** | **服务简介** | **计费单价** | **免费额度**[（查看）](https://help.aliyun.com/zh/model-studio/new-free-quota) |
| --- | --- | --- | --- | --- |
| wan2.2-animate-move | 标准模式`wan-std` | 生成速度快，满足基础动画演示等轻需求，性价比高。 | 0.880709元/秒 | 无免费额度 |
| 专业模式`wan-pro` | 动画流畅度高，动作表情过渡自然，效果更接近真实拍摄。 | 1.321063元/秒 |

| **人物图片** | **参考视频** | **输出视频（标准模式）** | **输出视频（专业模式）** |
| --- | --- | --- | --- |
| ![move_input_image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |     |     |     |

### **万相-视频换人**

提供标准和专业两种服务模式，基于人物图片和参考视频，将视频中的主角替换为图片中的角色，同时保留原视频的场景、光照和色调。[API 参考](https://help.aliyun.com/zh/model-studio/wan-animate-mix-api)

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **模型服务** | **服务简介** | **计费单价** | **免费额度**[（查看）](https://help.aliyun.com/zh/model-studio/new-free-quota) |
| --- | --- | --- | --- | --- |
| wan2.2-animate-mix | 标准模式`wan-std` | 生成速度快，满足基础动画演示等轻需求，性价比高。 | 0.6元/秒 | 两种服务共50秒 |
| 专业模式`wan-pro` | 动画流畅度高，动作表情过渡自然，效果更接近真实拍摄。 | 0.9元/秒 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **模型服务** | **服务简介** | **计费单价** | **免费额度**[（查看）](https://help.aliyun.com/zh/model-studio/new-free-quota) |
| --- | --- | --- | --- | --- |
| wan2.2-animate-mix | 标准模式`wan-std` | 生成速度快，满足基础动画演示等轻需求，性价比高。 | 1.321063元/秒 | 无免费额度 |
| 专业模式`wan-pro` | 动画流畅度高，动作表情过渡自然，效果更接近真实拍摄。 | 1.908202元/秒 |

| **人物图片** | **参考视频** | **输出视频（标准模式）** | **输出视频（专业模式）** |
| --- | --- | --- | --- |
| ![mix_input_image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |     |     |     |

### 舞动人像AnimateAnyone

基于人物图片和人物动作模板，生成人物动作视频。直接使用时需依次调用下述三个模型。[AnimateAnyone图像检测 API详情](https://help.aliyun.com/zh/model-studio/animate-anyone-detect-api) | [AnimateAnyone 动作模板生成](https://help.aliyun.com/zh/model-studio/animate-anyone-template-api) | [AnimateAnyone视频生成API详情](https://help.aliyun.com/zh/model-studio/animateanyone-video-generation-api)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **说明** | **单价** | **免费额度** |
| --- | --- | --- | --- |
| animate-anyone-detect-gen2 | 检测输入的图片是否符合要求 | 0.004元/张 | 200张 有效期：百炼开通后90天内 |
| animate-anyone-template-gen2 | 从人物运动视频中提取人物动作并生成动作模板 | 0.08元/秒 | 各1800秒 有效期：百炼开通后90天内 |
| animate-anyone-gen2 | 基于人物图片和动作模板生成人物动作视频 |

下面两个模型支持独立部署。模型部署后，模型调用参考这两个API详情。[AnimateAnyone图像检测 API详情](https://help.aliyun.com/zh/model-studio/animate-anyone-detect-api) | [AnimateAnyone视频生成API详情](https://help.aliyun.com/zh/model-studio/animateanyone-video-generation-api)

| **模型名称** | **说明** | **单价** | **免费额度** |
| --- | --- | --- | --- |
| animate-anyone-detect | 检测输入图片是否符合要求 | 当前仅支持部署后调用，仅收取部署费用。部署单价： - 10000元/算力单元/月 - 20元/算力单元/小时 | 无   |
| animate-anyone | 基于人物图片和动作模板生成人物动作视频 |

| **输入：人物图片** | **输入：动作视频** | **输出（按图片背景生成）** | **输出（按视频背景生成）** |
| --- | --- | --- | --- |
| ![04-9_16](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |     |     |     |

**说明**

-   以上示例，由集成了“舞动人像AnimateAnyone”的APP生成。
    
-   舞动人像AnimateAnyone模型的生成内容为视频画面，不包含音频。
    

### 悦动人像EMO

基于人物肖像图片和人声音频文件，生成人物肖像动态视频。使用时需依次调用下述模型。[EMO 图像检测](https://help.aliyun.com/zh/model-studio/emo-detect-api) | [EMO 视频生成](https://help.aliyun.com/zh/model-studio/emo-api)

> emo-detect-v1与emo-detect、emo-v1与emo在调用方式及计费方式中有区别，模型效果完全相同。

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **说明** | **单价** | **免费额度** |
| --- | --- | --- | --- |
| emo-detect-v1 | 检测输入的图片是否符合要求，不需要部署，可直接调用 | 0.004元/张 | 200张 有效期：百炼开通后90天内 |
| emo-v1 | 生成人物肖像动态视频，不需要部署，可直接调用 | - 生成1:1画幅视频：0.08元/秒 - 生成3:4画幅视频：0.16元/秒 | 1800秒 有效期：百炼开通后90天内 |
| emo-detect | 检测输入的图片是否符合要求，仅支持部署后调用 | 当前仅支持部署后调用，仅收取部署费用。 部署单价：20元/算力单元/小时 | 无   |
| emo | 生成人物肖像动态视频，仅支持部署后调用 |

| **输入物：人物肖像图片+人声音频文件** | **输出物：人物肖像动态视频** |
| --- | --- |
| 人物肖像： ![上春山](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 人声音频：参见右侧视频 | 人物视频： 使用动作风格强度：活泼（"style\\_level": "active"） |

### 灵动人像LivePortrait

基于人物肖像图片和人声音频文件，**快速、轻量地**生成人物肖像动态视频。与悦动人像EMO模型相比，生成速度快、价格低，但是生成效果不如悦动人像EMO模型。使用时需依次调用下述两个模型。[LivePortrait 图像检测](https://help.aliyun.com/zh/model-studio/liveportrait-detect-api) | [LivePortrait 视频生成](https://help.aliyun.com/zh/model-studio/liveportrait-api)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **说明** | **单价** | **免费额度** |
| --- | --- | --- | --- |
| liveportrait-detect | 检测输入的图片是否符合要求 | 0.004元/张 | 200张 有效期：百炼开通后90天内 |
| liveportrait | 生成人物肖像动态视频 | 0.02元/秒 | 1800秒 有效期：百炼开通后90天内 |

| **输入物：人物肖像图片+人声音频文件** | **输出物：人物肖像动态视频** |
| --- | --- |
| 人物肖像： ![Emoji男孩](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) 人声音频：参见右侧视频 | 人物视频： |

### **表情包Emoji**

基于人脸图片和预设的人脸动态模板，生成人脸动态视频。该能力可用于表情包制作、视频素材生成等场景。使用时需依次调用下述模型。[Emoji 图像检测](https://help.aliyun.com/zh/model-studio/emoji-detect-api) | [Emoji 视频生成](https://help.aliyun.com/zh/model-studio/emoji-api)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **说明** | **单价** | **免费额度** |
| --- | --- | --- | --- |
| emoji-detect-v1 | 检测输入图片是否符合要求 | 0.004元/张 | 200张 有效期：百炼开通后90天内 |
| emoji-v1 | 基于人物肖像图片和指定的表情包模板生成人物同款表情 | 0.08元/秒 | 500秒 有效期：百炼开通后90天内 |

| **输入：人物肖像图片** | **输出：人物肖像动态视频** |
| --- | --- |
| ![image.png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) | “开心”表情的模板序列：（"input.driven\\_id": "mengwa\\_kaixin"） |

### 声动人像VideoRetalk

基于人物视频和人声音频，生成人物讲话口型与输入音频相匹配的视频。使用时需调用下述模型。[API参考](https://help.aliyun.com/zh/model-studio/videoretalk-api)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **说明** | **单价** | **免费额度** |
| --- | --- | --- | --- |
| videoretalk | 生成人物讲话口型与输入音频相匹配的新视频 | 0.08元/秒 | 1800秒 有效期：百炼开通后90天内 |

| **输入示例** | **输出示例** |
| --- | --- |
| 人声音频： |     |

### **视频风格重绘**

支持根据用户输入的文字内容，生成符合语义描述的不同风格的视频，或者根据用户输入的视频，进行视频风格重绘。[API参考](https://help.aliyun.com/zh/model-studio/video-style-transform-api-reference)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **说明** | **单价** |   | **免费额度** |
| --- | --- | --- | --- | --- |
| video-style-transform | 将输入视频转换为日式漫画、美式漫画等风格 | 720P | 0.5元/秒 | 600秒 有效期：百炼开通后90天内 |
| 540P | 0.2元/秒 |

| **输入视频** | **输出视频（日式漫画）** |
| --- | --- |
|     |     |

## **视频生成-第三方模型**

**爱诗-文生视频**

爱诗-文生视频模型通过一句话即可生成视频。[API参考](https://help.aliyun.com/zh/model-studio/pixverse-text-to-video-api-reference) ｜ [在线体验](https://bailian.console.aliyun.com/?spm=5176.30275541.J_ZGek9Blx07Hclc3Ddt9dg.4.51f82f3dFlj82T&scm=20140722.S_card%40%40%E4%BA%A7%E5%93%81%40%402983180.S_new%7EUND%7Ecard.ID_card%40%40%E4%BA%A7%E5%93%81%40%402983180-RL_%E7%99%BE%E7%82%BC%E5%B9%B3%E5%8F%B0-LOC_2024SPSearchCard-OR_ser-PAR1_215043cb17587857714454653ea60a-V_4-RE_new7-P0_0-P1_0&tab=demohouse#/experience/t2v)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输出视频类型** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| pixverse/pixverse-v5.6-t2v | 有声视频 | 360P | 0.47元/秒 | 无免费额度 |
| 540P | 0.47元/秒 |
| 720P | 0.53元/秒 |
| 1080P | 0.7元/秒 |
| 无声视频 | 360P | 0.21元/秒 |
| 540P | 0.21元/秒 |
| 720P | 0.27元/秒 |
| 1080P | 0.44元/秒 |

**爱诗-图生视频-基于首帧**

爱诗-图生视频模型输入视频首帧，再根据提示词生成视频。[API参考](https://help.aliyun.com/zh/model-studio/pixverse-image-to-video-api-reference) ｜ [在线体验](https://bailian.console.aliyun.com/?spm=5176.30275541.J_ZGek9Blx07Hclc3Ddt9dg.4.51f82f3dFlj82T&scm=20140722.S_card%40%40%E4%BA%A7%E5%93%81%40%402983180.S_new%7EUND%7Ecard.ID_card%40%40%E4%BA%A7%E5%93%81%40%402983180-RL_%E7%99%BE%E7%82%BC%E5%B9%B3%E5%8F%B0-LOC_2024SPSearchCard-OR_ser-PAR1_215043cb17587857714454653ea60a-V_4-RE_new7-P0_0-P1_0&tab=demohouse#/experience/t2v)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输出视频类型** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| pixverse/pixverse-v5.6-it2v | 有声视频 | 360P | 0.47元/秒 | 无免费额度 |
| 540P | 0.47元/秒 |
| 720P | 0.53元/秒 |
| 1080P | 0.7元/秒 |
| 无声视频 | 360P | 0.21元/秒 |
| 540P | 0.21元/秒 |
| 720P | 0.27元/秒 |
| 1080P | 0.44元/秒 |

**爱诗-图生视频-基于首尾帧**

爱诗-首尾帧生视频模型，只需提供首帧和尾帧图片，便能根据提示词生成一段丝滑流畅的动态视频。[API参考](https://help.aliyun.com/zh/model-studio/pixverse-keyframe-to-video-api-reference)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输出视频类型** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| pixverse/pixverse-v5.6-kf2v | 有声视频 | 360P | 0.47元/秒 | 无免费额度 |
| 540P | 0.47元/秒 |
| 720P | 0.53元/秒 |
| 1080P | 0.7元/秒 |
| 无声视频 | 360P | 0.21元/秒 |
| 540P | 0.21元/秒 |
| 720P | 0.27元/秒 |
| 1080P | 0.44元/秒 |

**爱诗-参考生视频**

爱诗-参考生视频模型支持参考输入图像中的角色形象，搭配提示词生成视频。[API参考](https://help.aliyun.com/zh/model-studio/pixverse-reference-to-video-api-reference)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输出视频类型** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| pixverse/pixverse-v5.6-r2v | 有声视频 | 360P | 0.47元/秒 | 无免费额度 |
| 540P | 0.47元/秒 |
| 720P | 0.53元/秒 |
| 1080P | 0.7元/秒 |
| 无声视频 | 360P | 0.21元/秒 |
| 540P | 0.21元/秒 |
| 720P | 0.27元/秒 |
| 1080P | 0.44元/秒 |

**可灵-视频生成**

可灵-视频生成模型支持**文生视频、图生视频-基于首帧、图生视频-基于首尾帧、参考生视频以及视频编辑**。[API参考](https://help.aliyun.com/zh/model-studio/kling-video-generation-api-reference/)｜ [在线体验](https://bailian.console.aliyun.com/?spm=5176.30275541.J_ZGek9Blx07Hclc3Ddt9dg.4.51f82f3dFlj82T&scm=20140722.S_card%40%40%E4%BA%A7%E5%93%81%40%402983180.S_new%7EUND%7Ecard.ID_card%40%40%E4%BA%A7%E5%93%81%40%402983180-RL_%E7%99%BE%E7%82%BC%E5%B9%B3%E5%8F%B0-LOC_2024SPSearchCard-OR_ser-PAR1_215043cb17587857714454653ea60a-V_4-RE_new7-P0_0-P1_0&tab=demohouse#/experience/t2v)

**说明**

-   仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。
    
-   中国内地部署模式的模型无免费额度。
    

| **模型名称** | **支持的能力** | **输出视频类型** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| kling/kling-v3-omni-video-generation `**推荐**` | - 文生视频 - 图生视频-基于首帧 - 图生视频-基于首尾帧 - 参考生视频 - 视频编辑 | 无声视频（无参考视频） | 720P | 0.6元/秒 | 无免费额度 |
| 1080P | 0.8元/秒 |
| 无声视频（有参考视频） | 720P | 0.9元/秒 |
| 1080P | 1.2元/秒 |
| 有声视频（无参考视频） | 720P | 0.9元/秒 |
| 1080P | 1.2元/秒 |
| kling/kling-v3-video-generation | - 文生视频 - 图生视频-基于首帧 - 图生视频-基于首尾帧 | 无声视频 | 720P | 0.6元/秒 |
| 1080P | 0.8元/秒 |
| 有声视频 | 720P | 0.9元/秒 |
| 1080P | 1.2元/秒 |

**Vidu-文生视频**

Vidu-文生视频模型通过一句话即可生成视频。[API参考](https://help.aliyun.com/zh/model-studio/vidu-text-to-video-api-reference) ｜ [在线体验](https://bailian.console.aliyun.com/?spm=5176.30275541.J_ZGek9Blx07Hclc3Ddt9dg.4.51f82f3dFlj82T&scm=20140722.S_card%40%40%E4%BA%A7%E5%93%81%40%402983180.S_new%7EUND%7Ecard.ID_card%40%40%E4%BA%A7%E5%93%81%40%402983180-RL_%E7%99%BE%E7%82%BC%E5%B9%B3%E5%8F%B0-LOC_2024SPSearchCard-OR_ser-PAR1_215043cb17587857714454653ea60a-V_4-RE_new7-P0_0-P1_0&tab=demohouse#/experience/t2v)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **支持的能力** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| vidu/viduq3-turbo\\_text2video `**推荐**` | 有声视频、无声视频 > 支持智能分镜，生成效果较好 | 540P | 0.25元/秒 | 无免费额度 |
| 720P | 0.375元/秒 |
| 1080P | 0.4375元/秒 |
| vidu/viduq3-pro\\_text2video | 有声视频、无声视频 > 支持智能分镜，生成速度较快 | 540P | 0.3125元/秒 |
| 720P | 0.78125元/秒 |
| 1080P | 0.9375元/秒 |
| vidu/viduq2\\_text2video | 无声视频 | 540P | 0.1125元/秒 |
| 720P | 0.21875元/秒 |
| 1080P | 0.375元/秒 |

**Vidu-图生视频-基于首帧**

Vidu-图生视频模型输入视频首帧，再根据提示词生成视频。[API参考](https://help.aliyun.com/zh/model-studio/vidu-image-to-video-api-reference) ｜ [在线体验](https://bailian.console.aliyun.com/?spm=5176.30275541.J_ZGek9Blx07Hclc3Ddt9dg.4.51f82f3dFlj82T&scm=20140722.S_card%40%40%E4%BA%A7%E5%93%81%40%402983180.S_new%7EUND%7Ecard.ID_card%40%40%E4%BA%A7%E5%93%81%40%402983180-RL_%E7%99%BE%E7%82%BC%E5%B9%B3%E5%8F%B0-LOC_2024SPSearchCard-OR_ser-PAR1_215043cb17587857714454653ea60a-V_4-RE_new7-P0_0-P1_0&tab=demohouse#/experience/t2v)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **支持的能力** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| vidu/viduq3-pro\\_img2video `**推荐**` | 有声视频、无声视频 > 支持智能分镜，生成效果较好 | 540P | 0.3125元/秒 | 无免费额度 |
| 720P | 0.78125元/秒 |
| 1080P | 0.9375元/秒 |
| vidu/viduq3-turbo\\_img2video | 有声视频、无声视频 > 支持智能分镜，生成速度较快 | 540P | 0.25元/秒 |
| 720P | 0.375元/秒 |
| 1080P | 0.4375元/秒 |
| vidu/viduq2-pro\\_img2video | 无声视频 | 540P | 0.15625元/秒 |
| 720P | 0.34375元/秒 |
| 1080P | 0.71875元/秒 |
| vidu/viduq2-turbo\\_img2video | 无声视频 | 540P | 0.0875元/秒 |
| 720P | 0.25元/秒 |
| 1080P | 0.46875元/秒 |

**Vidu-图生视频-基于首尾帧**

Vidu-首尾帧生视频模型，只需提供首帧和尾帧图片，便能根据提示词生成一段丝滑流畅的动态视频。[API参考](https://help.aliyun.com/zh/model-studio/vidu-keyframe-to-video-api-reference)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **支持的能力** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| vidu/viduq3-pro\\_start-end2video `**推荐**` | 有声视频、无声视频 > 支持智能分镜，生成效果较好 | 540P | 0.3125元/秒 | 无免费额度 |
| 720P | 0.78125元/秒 |
| 1080P | 0.9375元/秒 |
| vidu/viduq3-turbo\\_start-end2video | 有声视频、无声视频 > 支持智能分镜，生成速度较快 | 540P | 0.25元/秒 |
| 720P | 0.375元/秒 |
| 1080P | 0.4375元/秒 |
| vidu/viduq2-pro\\_start-end2video | 无声视频 | 540P | 0.15625元/秒 |
| 720P | 0.34375元/秒 |
| 1080P | 0.71875元/秒 |
| vidu/viduq2-turbo\\_start-end2video | 无声视频 | 540P | 0.0875元/秒 |
| 720P | 0.25元/秒 |
| 1080P | 0.46875元/秒 |

**Vidu-参考生视频**

Vidu-参考生视频模型支持参考图像和视频，搭配提示词生成视频。[API参考](https://help.aliyun.com/zh/model-studio/vidu-reference-to-video-api-reference)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **支持的能力** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| vidu/viduq2-pro\\_reference2video`**推荐**` | 无声视频 > 支持参考图像和视频 | 540P | 0.25元/秒 | 无免费额度 |
| 720P | 0.3125元/秒 |
| 1080P | 0.78125元/秒 |
| vidu/viduq2\\_reference2video | 无声视频 > 仅支持参考图像 | 540P | 0.21875元/秒 |
| 720P | 0.28125元/秒 |
| 1080P | 0.71875元/秒 |

## **文本向量**

文本向量模型用于将文本转换成一组可以代表文字的数字，适用于搜索、聚类、推荐、分类任务。模型根据输入Token数计费。[同步接口API详情](https://help.aliyun.com/zh/model-studio/text-embedding-synchronous-api)| [批处理接口API详情](https://help.aliyun.com/zh/model-studio/text-embedding-batch-api)

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **向量维度** | **批次大小** | **单批次最大Token数** | **支持语种** | **单价** **（每百万输入Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| text-embedding-v4 > 属于[Qwen3-Embedding](https://qwenlm.github.io/zh/blog/qwen3-embedding/)系列 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 2,048、1,536、1,024（默认）、768、512、256、128、64 | 10  | 8,192 | 中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等100+主流语种及多种编程语言 | 0.5元 | 100万Token 有效期：百炼开通后90天内 |
| text-embedding-v3 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 1,024（默认）、768、512、256、128或64 | 中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等50+主流语种 | 0.5元 | 各50万Token 有效期：百炼开通后90天内 |

**更多模型**

| **模型名称** | **向量维度** | **批次大小** | **单批次最大处理Token数** | **支持语种** | **单价** **（每百万输入Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| text-embedding-v2 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 1,536 | 25  | 2,048 | 中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语 | 0.7元 | 50万Token 有效期：百炼开通后90天内 |
| text-embedding-v1 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 中文、英语、西班牙语、法语、葡萄牙语、印尼语 |
| text-embedding-async-v2 | 100,000 | 中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语 | 0.7元 | 各2000万Token 有效期：百炼开通后90天内 |
| text-embedding-async-v1 | 中文、英语、西班牙语、法语、葡萄牙语、印尼语 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **向量维度** | **批次大小** | **单批次最大Token数** | **支持语种** | **单价（每百万输入Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| text-embedding-v4 > 属于[Qwen3-Embedding](https://qwenlm.github.io/zh/blog/qwen3-embedding/)系列 | 2,048、1,536、1,024（默认）、768、512、256、128、64 | 10  | 8,192 | 中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等100+主流语种 | 0.514元 | 无免费额度 |
| text-embedding-v3 | 1,024（默认）、768、512 | 中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等50+主流语种 |

**说明**

批次大小指单次API调用中能处理的文本数量上限。例如，text-embedding-v4的批次大小为10，意味着一次请求最多可传入10个文本进行向量化，且每个文本不得超过 8192 个Token。这个限制适用于：

-   字符串数组输入：数组最多包含10个元素。
    
-   文件输入：文本文件最多包含10行文本。
    

**模型升级概述**

1.  **text-embedding-v2**
    
    -   **语种扩充**：新增对日语、韩语、德语、俄罗斯语的文本向量化能力。
        
    -   **效果提升**：优化了预训练模型和SFT策略，提升了整体效果，公开数据评测结果显示有显著改进。
        
2.  **text-embedding-v3**
    
    -   **语种扩充**：支持意大利语、波兰语、越南语、泰语等语种，语种数量增加至50余种。
        
    -   **输入长度扩展**：最大输入长度从2048 Token扩展至8192 Token。
        
    -   **连续向量维度自定义**：允许用户选择1024、768、512、256、128或64维度，默认维度为1024。
        
    -   **不再区分Query/Document类型**：简化输入，text\_type参数不再需要指定文本类型。
        
    -   **Sparse向量支持**：支持在接口中指定输出稠密向量和离散向量。
        
    -   **效果提升**：进一步优化预训练模型和SFT策略，提升整体效果，公开数据评测结果显示效果更佳。
        
3.  **text-embedding-v4**
    
    -   **语种扩充**：涵盖主流自然语言及多种编程语言，语种数量增加至100余种。
        
    -   **向量维度弹性扩展**：新增2,048及1,536向量维度选项，向量维度选项扩展至8个。
        
    -   **效果提升**：文本检索、聚类、分类性能大幅提升，相较于text-embedding-v3在MTEB多语言、中英、Code检索等评测任务中效果提升15%~40%。
        

**v1、v2、v3模型的效果数据**

| **模型** | **MTEB** | **MTEB（Retrieval task）** | **CMTEB** | **CMTEB (Retrieval task)** |
| --- | --- | --- | --- | --- |
| text-embedding-v1 | 58.30 | 45.47 | 59.84 | 56.59 |
| text-embedding-v2 | 60.13 | 49.49 | 62.17 | 62.78 |
| text-embedding-v3（64维度） | 57.40 | 46.52 | 59.19 | 62.03 |
| text-embedding-v3（128维度） | 60.19 | 52.51 | 63.81 | 68.22 |
| text-embedding-v3（256维度） | 61.13 | 54.41 | 65.92 | 71.07 |
| text-embedding-v3（512维度） | 62.11 | 54.30 | 66.81 | 71.88 |
| text-embedding-v3（768维度） | 62.43 | 54.74 | 67.90 | 72.29 |
| text-embedding-v3（1024维度） | 63.39 | 55.41 | 68.92 | 73.23 |
| text-embedding-v4（512维度） | 64.73 | 56.34 | 68.79 | 73.33 |
| text-embedding-v4（1024维度） | 68.36 | 59.30 | 70.14 | 73.98 |
| text-embedding-v4（2048维度） | 71.58 | 61.97 | 71.99 | 75.01 |

MTEB（大规模文本嵌入评测基准）和CMTEB（中文大规模文本嵌入评测基准）采用0-100分制评估模型性能，数值越高代表效果越优。总分通过综合分类、聚类、检索等任务反映模型通用性，Retrieval Task分数用于衡量检索任务（如文档搜索）的精度，分数越高检索效果越强。

## **多模态向量**

多模态向量模型将文本、图像或视频转换成一组由浮点数组成的向量，适用于视频分类、图像分类、图文检索等。[API参考](https://help.aliyun.com/zh/model-studio/multimodal-embedding-api-reference)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **数据类型** | **向量维度** | **单价（每百万输入Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| qwen3-vl-embedding | float(32) | 2560, 2048, 1536, 1024, 768, 512, 256 | 图片/视频：1.8元 文本：0.7元 | 100万Token 有效期：百炼开通后90天内 |
| qwen2.5-vl-embedding | 1024(默认)、512、768、2048 |
| tongyi-embedding-vision-plus-2026-03-06 | 1152（默认）, 1024, 512, 256, 128, 64 | 图片/视频：0.5元 文本：0.5元 |
| tongyi-embedding-vision-flash-2026-03-06 | 768（默认）, 512, 256, 128, 64 | 图片/视频：0.15元 文本：0.15元 |
| tongyi-embedding-vision-plus | 1152（默认）, 1024, 512, 256, 128, 64 | 图片/视频：0.5元 文本：0.5元 |
| tongyi-embedding-vision-flash | 768（默认）, 512, 256, 128, 64 | 图片/视频：0.15元 文本：0.15元 |
| multimodal-embedding-v1 | 1,024 | 图片/视频：0.9元 文本：0.7元 |

## **文本分类、抽取、排序**

### **OpenNLU**

针对给定的文本（中文或英文）进行信息抽取或文本分类。模型根据输出Token数计费。[API参考](https://help.aliyun.com/zh/model-studio/opennlu-api)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **最大输入Token数** | **单价（每百万 Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| opennlu-v1 | 1,024 | 4.65元 | 100万Token 有效期：百炼开通后90天内 |

### **排序模型**

通常用于语义检索，即给定查询 (Query) 和一系列候选文本 (Documents)，会根据与查询的语义相关性从高到低对候选文本进行排序。[API参考](https://help.aliyun.com/zh/model-studio/text-rerank-api)

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **最大Document数量** | **单行最大输入Token** | **最大输入Token** | **支持语言** | **单价（每百万输入Token）** | **免费额度** |
| --- | --- | --- | --- | --- | --- | --- |
| qwen3-vl-rerank | 100 | 8,000 | 120,000 | 中、英、日、韩、法、德等33种主流语言 | 图片：1.8元 文字：0.7元 | 各100万Token 有效期：百炼开通后90天内 |
| qwen3-rerank | 500 | 4,000 | 30,000 | 中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等100+主流语种 | 0.5元 |
| gte-rerank-v2 | 中、英、日、韩、泰语、西、法、葡、德、印尼语、阿拉伯语等50+语种 | 0.8元 |

-   **单行最大输入Token**：每个Query或Document的最大Token数量为4,000。如果输入内容超过此长度，将会被截断。
    
-   **最大Document数量**：每次请求中Document的最大数量为500。
    
-   **最大输入Token**：每次请求中所有Query和Document的Token总数不得超过30,000。
    

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **最大Document数量** | **单行最大输入Token** | **最大输入Token** | **支持语言** | **单价（每百万输入Token）** | **免费额度** |
| --- | --- | --- | --- | --- | --- | --- |
| qwen3-rerank | 500 | 4,000 | 30,000 | 中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等100+主流语种 | 0.5元 | 各100万Token 有效期：百炼开通后90天内 |

-   **单行最大输入Token**：每个Query或Document的最大Token数量为4,000。如果输入内容超过此长度，将会被截断。
    
-   **最大Document数量**：每次请求中Document的最大数量为500。
    
-   **最大输入Token**：每次请求中所有Query和Document的Token总数不得超过30,000。
    

## **行业**

### **通义法睿**

适用于回答法律问题、推荐裁判类案、辅助案情分析、生成法律文书、检索法律知识、审查合同条款等。[API参考](https://help.aliyun.com/zh/model-studio/tongyi-farui-api) | [在线体验](https://bailian.console.aliyun.com/#/model-market/detail/farui-plus)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** |
| --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |     | **（每百万 Token）** |   |
| farui-plus | 12k | 12k | 2k  | 20元 |   |

### **意图理解**

千问意图理解模型，能够在百毫秒级时间内快速、准确地解析用户意图，并选择合适工具来解决用户问题。[API参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/) | [使用方法](https://help.aliyun.com/zh/model-studio/intent-detect-capability)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度** [（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万Token）** |   |
| tongyi-intent-detect-v3 | 8,192 | 8,192 | 1,024 | 0.4元 | 1元  | 100万Token 有效期：百炼开通后90天内 |

### **角色扮演**

千问的角色扮演模型，适合拟人化的对话场景（如虚拟社交、游戏NPC、IP复刻、硬件/玩具/车机等）。相比于其它千问模型，提升了人设还原、话题推进、倾听共情等能力。[使用方法](https://help.aliyun.com/zh/model-studio/role-play)

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万 Token）** |   |
| qwen-plus-character | 32,768 | 32,000 | 4,096 | 0.8元 | 2元  | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen-flash-character | 8,192 | 8,000 | 0.25元 | 1.5元 |
| qwen-flash-character-2026-02-26 | 8,192 | 8,192 | 0.18元 | 1.5元 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万 Token）** |   |
| qwen-plus-character-ja | 8,192 | 7,680 | 512 | 3.67元 | 10.275元 | 无免费额度 |

### 界面交互

GUI-Plus 可基于屏幕截图和自然语言指令来解析用户意图，并转换为标准化的图像用户界面（GUI）操作（如点击、输入、滚动等），供外部系统决策或执行。相较于千问VL系列模型，提升了GUI操作的准确性。[使用方法](https://help.aliyun.com/zh/model-studio/gui-automation) | [API参考](https://help.aliyun.com/zh/model-studio/gui-plus-interface-interaction-model)

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **模式** | **上下文长度** | **最大输入** | **最大思维链长度** | **最大回复长度** | **输入成本** | **输出成本** | **免费额度** [查看剩余额度](https://help.aliyun.com/zh/model-studio/new-free-quota#view-quota) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | **（Token数）** |   |   |   | **（每百万Token）** |   |
| **gui-plus** | 非思考模式 | 256,000 | 254,976 > 单图最大16384 | \\- | 32,768 | 1.5元 | 4.5元 | 各100万Token 有效期：百炼开通后90天内 |
| gui-plus-2026-02-26 | 思考模式 | 262,144 | 258,048 > 单图最大16384 | 81,920 | 32,768 |
| 非思考模式 | 260,096 > 单图最大16384 | \\- | 32,768 |

## **已下线模型**

## 2026年1月30日下线

| **类别** | **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本（每百万Token）** | **输出成本（每百万Token）** | **替代模型** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   |
| 千问Max | qwen-max-2024-04-03 | 8,000 | 6,000 | 2,000 | 40元 | 120元 | qwen-max-2025-01-25 |
| 千问Plus | qwen-plus-2024-11-27 | 131,072 | 129,024 | 8,192 | 0.8元 | 2元  | qwen-plus-2025-12-01 |
| qwen-plus-2024-11-25 |
| qwen-plus-2024-09-19 |
| qwen-plus-2024-08-06 | 128,000 | 4元  | 12元 |
| qwen-plus-2024-07-23 | 32,000 | 30,000 |
| 千问Turbo | qwen-turbo-2024-09-19 | 131,072 | 129,023 | 8,192 | 0.3元 | 0.6元 | qwen-flash-2025-07-28 |
| qwen-turbo-2024-06-24 | 8,000 | 6,000 | 2,000 | 2元  | 6元  |
| 千问VL | qwen-vl-max-2024-10-30 | 32,768 | 30,720 > 单图最大16384 | 2,048 | 20元 | 20元 | qwen3-vl-plus-2025-12-19 |
| qwen-vl-max-2024-08-09 |
| qwen-vl-plus-2024-08-09 | 1.5元 | 4.5元 | qwen3-vl-flash-2025-10-15 |
| 千问Audio | qwen-audio-turbo-2024-12-04 | 8,192 | 6,144 | 2,048 | 仅供免费体验，免费额度用完后不可调用。 |   | qwen3-omni-flash |
| qwen-audio-turbo-2024-08-07 | 8,000 | 6,000 | 1,500 |
| qwen-audio-asr-2024-12-04 | 8,192 | 6,144 | 2,048 | qwen3-asr-flash |

## 2025年7月30日下线

| **类别** | **模型名称** | **上下文长度** | **最大输入** | **输入成本** | **输出成本（每百万Token）** | **替代模型** |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |
| 千问VL快照版 | qwen-vl-plus-2023-12-01 | 8,000 | 6,000 | 2,000 | 8元  | qwen-vl-plus |
| 零一万物 | yi-large | 32,000 | 32,000 | 仅供免费体验，免费额度用完后不可调用。 |   | Qwen3、DeepSeek、Kimi等 |
| yi-medium |
| yi-large-rag | 16,000 | 16,000 |
| yi-large-turbo |
| Dolly | dolly-12b-v2 | 限时免费 |   |   |   |

## 2025年7月2日下线

| **类别** | **模型名称** | **上下文长度** | **最大输入** | **输入成本（每百万Token）** | **输出成本（每百万Token）** | **替代模型** |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |
| Llama-仅文本输入 | llama3.3-70b-instruct | 32,000 | 30,000 | 仅供免费体验，免费额度用完后不可调用。 |   | Qwen3、DeepSeek、Kimi等 |
| llama3.2-3b-instruct |
| llama3.2-1b-instruct |
| llama3.1-405b-instruct |
| llama3.1-70b-instruct |
| llama3.1-8b-instruct |
| llama3-70b-instruct | 8,000 | 8,000 |
| llama3-8b-instruct |
| llama2-13b-chat-v2 | 4,000 | 4,000 |
| llama2-7b-chat-v2 |
| Llama-文本和图像输入 | llama3.2-90b-vision-instruct | 8,192 | 8,192 |
| llama3.2-11b-vision |
| 百川开源版 | baichuan2-13b-chat-v1 | 4,096 | 4,096 | 8元  | 8元  |
| baichuan2-7b-chat-v1 | 6元  | 6元  |
| baichuan-7b-v1 | 仅供免费体验，免费额度用完后不可调用。 |   |
| ChatGLM | chatglm3-6b | 7,500 | 7,500 | 仅供免费体验，免费额度用完后不可调用。 |   |
| chatglm-6b-v2 | 6,500 | 6,500 | 6元  | 6元  |
| 姜子牙 | ziya-llama-13b-v1 | \\- |   | 限时免费（需申请） |   |
| BELLE | belle-llama-13b-2m-v1 |
| 元语  | chatyuan-large-v2 |
| BiLLa | billa-7b-sft-v1 |
| 动漫人物生成 | wanx-style-cosplay-v1 | 仅供免费体验，免费额度用完后不可调用。 |   | 无直接替代模型 |
| 图配文 | wanx-ast |
| 创意文字生成-WordArt锦书 | wordart-surnames |

## 2025年5月8日下线

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **替代模型** |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** |   |   | **（每百万 Token）** |   |
| qwen-max-2024-01-07 > 又称qwen-max-0107 | 8,000 | 6,000 | 2,000 | 40元 | 120元 | qwen-max |
| qwen-plus-2024-06-24 > 又称qwen-plus-0624 | 32,000 | 30,000 | 8,000 | 4元  | 12元 | qwen-plus |
| qwen-plus-2024-02-06 > 又称qwen-plus-0206 |
| qwen-turbo-2024-02-06 > 又称qwen-turbo-0206 | 8,000 | 6,000 | 2,000 | 2元  | 6元  | qwen-turbo |
| qwen-vl-max-2024-02-01 > 又称qwen-vl-max-0201 | 8,000 | 6,000 > 单图最大1280 | 2,000 | 20元 |   | qwen-vl-max |
| qwen-72b-chat | 32,000 | 30,000 | 2,000 | 20元 |   | qwen2.5-72b-instruct |
| qwen-14b-chat | 8,000 | 6,000 | 8元  |   | qwen2.5-14b-instruct |
| qwen-7b-chat | 7,500 | 1,500 | 6元  |   | qwen2.5-7b-instruct |
| qwen-1.8b-chat | 8,000 | 2,000 | 限时免费 |   | qwen2.5-1.5b-instruct |
| qwen-1.8b-longcontext-chat | 32,000 | 30,000 | qwen2.5-1.5b-instruct |
| qwen2-math-72b-instruct | 4,096 | 3,072 | 3,072 | 4元  | 12元 | qwen2.5-math-72b-instruct |
| qwen2-math-7b-instruct | 1元  | 2元  | qwen2.5-math-7b-instruct |
| qwen2-math-1.5b-instruct | 限时免费 |   | qwen2.5-math-1.5b-instruct |

| **模型名称** | **单价** | **替代模型** |
| --- | --- | --- |
| motionshop-video-detect | 0.04元/次 | 使用animate-anyone-gen2的“按视频背景生成”功能，可达到近似效果 |
| motionshop-gen3d | 1元/次 |
| motionshop-synthesis | 0.2元/秒 |

为了保证用户调用模型的公平性，阿里云百炼设置了基础限流。限流基于模型维度且与用户的阿里云主账号相关联，按照该账号下所有API-KEY调用该模型的总和计算限流。若超出限制，API请求将会失败，需等到解除限流条件时再次调用。

## **限流规则**

-   **主账号维度**：按**主账号**下，所有RAM子账号、所有业务空间、所有API-KEY的调用总和计算。
    
-   **不同模型独立限流**：具体参见下方表格。
    

## **限流FAQ**

### **为什么触发限流？**

根据错误信息判断：

-   Requests rate limit exceeded或You exceeded your current requests list：表示**调用频率**触发限流。
    
-   Allocated quota exceeded或You exceeded your current quota：表示**Token消耗**触发限流。
    
-   Request rate increased too quickly：表示在未达到RPM或TPM限流条件时，因**调用频率在短时间内激增**，触发了系统稳定性保护机制。
    
-   其他报错请参考[错误信息](https://help.aliyun.com/zh/model-studio/error-code)确认原因。
    

**注意**：除了RPM（Requests Per Minute，每分钟请求数）和TPM，限流策略可能按秒级 **RPS**（RPM/60）与 **TPS**（TPM/60）限制，即使总调用量未达到每分钟上限，短时间内的请求爆发也可能触发限流。

### **如何查看模型调用量？**

模型调用完**一小时后**，在模型监控（[北京](https://bailian.console.aliyun.com/?tab=model#/model-telemetry)或[新加坡](https://modelstudio.console.aliyun.com/?tab=model#/model-telemetry)）页面设置查询条件（例如，选择时间范围、业务空间等），再在**模型列表**区域找到目标模型并单击**操作**列的**监控**，即可查看该模型的调用统计结果。具体请参见[模型监控](https://help.aliyun.com/zh/model-studio/model-telemetry/)文档。

> 数据按小时更新，高峰期可能有小时级延迟，请您耐心等待。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6923304571/p992753.png)

### **遇到限流后多久恢复？**

**通常在一分钟内恢复**。若出现其他报错，请根据[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

### **如何避免限流？**

1.  **选用高限流模型**
    
    -   优先使用 [qwen-plus](https://help.aliyun.com/zh/model-studio/models#6c45e49509gtr) 等限流宽松的模型。
        
    -   稳定版或最新版比带日期的快照版本限流更宽松。
        
2.  **优化调用策略**
    
    -   **调整调用频率**：触发Requests rate limit exceeded或You exceeded your current requests list时，降低调用频率。
        
    -   **减少Token消耗：**触发Allocated quota exceeded或You exceeded your current quota时，缩短输入或输出长度。
        
    -   **平滑请求速率**：当调用频率骤增并触发系统稳定性保护（收到 Request rate increased too quickly 报错）时，建议优化客户端调用逻辑，采用平滑请求策略（如匀速调度、指数退避或请求队列缓冲），将请求均匀分散在时间窗口内，避免瞬时高峰。
        
3.  **添加备选模型**
    
    建议您在遇到限流报错后切换到备用模型继续生成，提升并发并降低失败概率。以下代码展示了调用 `qwen-plus-2025-07-28` 触发限流，改用 `qwen-plus-2025-07-14` 重发请求的示例。
    
    **示例代码**
    
    ```
    import os
    import asyncio
    from openai import AsyncOpenAI, APIStatusError
    
    # 配置
    API_KEY = os.getenv("DASHSCOPE_API_KEY")
    # 主用模型
    MODEL = "qwen-plus-2025-07-28"
    # 备选模型
    BACKUP_MODEL = "qwen-plus-2025-07-14"
    # 测试问题
    QUESTION = "你是谁？"
    # 并发设置
    NUM_REQUESTS = 10
    
    client = AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    
    async def send_request(model):
        """发送单个请求"""
        try:
            await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": QUESTION}]
            )
            return True
        except APIStatusError as e:
            if e.status_code == 429:
                print(f"[限流触发] 模型 {model}")
                return False
            raise
        except Exception as e:
            print(f"[请求失败] 模型 {model}，错误：{e}")
            return False
    
    async def task(i):
        # 尝试主模型
        if await send_request(MODEL):
            return True
        # 限流时尝试备用模型
        return await send_request(BACKUP_MODEL)
    
    async def main():
        results = await asyncio.gather(*(task(i) for i in range(NUM_REQUESTS)))
        print(f"成功请求: {sum(results)}, 失败请求: {len(results) - sum(results)}")
    
    if __name__ == "__main__":
        asyncio.run(main())
    ```
    
4.  **任务拆分**：处理长对话或大型文档会快速消耗大量Token。可以将大批量任务拆分为小批次，在不同时间段提交。
    
5.  **批量推理**：如果无需实时返回结果，可使用[批量推理](https://help.aliyun.com/zh/model-studio/batch-inference)（Batch API），不受实时限流约束，但需考虑排队和处理时间。
    

## **文本生成-千问**

### **千问语言模型**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-max | 30,000 | 5,000,000 |
| qwen3-max-2026-01-23 | 600 | 1,000,000 |
| qwen3-max-2025-09-23 | 60  | 100,000 |
| qwen3-max-preview | 600 | 1,000,000 |
| qwen-max > 用[Batch API](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)调用服务时，不受限流限制。 | 1,200 |
| qwen-max-latest |
| qwen-max-2025-01-25 （qwen-max-0125） | 60  | 100,000 |
| qwen-max-2024-09-19 （qwen-max-0919） |
| qwen-max-2024-04-28 （qwen-max-0428） |
| qwen3.5-plus | 30,000 | 5,000,000 |
| qwen3.5-plus-2026-02-15 | 600 | 1,000,000 |
| qwen-plus > 用[Batch API](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)调用服务时，不受限流限制。 | 30,000 | 5,000,000 |
| qwen-plus-latest | 15,000 | 1,200,000 |
| qwen-plus-2025-12-01 | 120 | 1,000,000 |
| qwen-plus-2025-09-11 | 60  |
| qwen-plus-2025-07-28 （qwen-plus-0728） |
| qwen-plus-2025-07-14 （qwen-plus-0714） | 100,000 |
| qwen-plus-2025-04-28 （qwen-plus-0428） | 1,000,000 |
| qwen-plus-2025-01-25 （qwen-plus-0125） | 150,000 |
| qwen-plus-2025-01-12 （qwen-plus-0112） |
| qwen-plus-2024-12-20 （qwen-plus-1220） |
| qwen3.5-flash | 30,000 | 10,000,000 |
| qwen3.5-flash-2026-02-23 | 600 | 1,000,000 |
| qwen-flash | 30,000 | 10,000,000 |
| qwen-flash-2025-07-28 | 60  | 1,000,000 |
| qwen-turbo > 用[Batch API](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)调用服务时，不受限流限制。 | 1,200 | 5,000,000 |
| qwen-turbo-latest |
| qwen-turbo-2025-07-15 (qwen-turbo-0715) | 60  | 100,000 |
| qwen-turbo-2025-04-28 (qwen-turbo-0428) | 1,000,000 |
| qwen-turbo-2025-02-11 (qwen-turbo-0211) | 5,000,000 |
| qwen-turbo-2024-11-01 (qwen-turbo-1101) |
| qwq-plus | 600 | 1,000,000 |
| qwq-plus-latest |
| qwq-plus-2025-03-05 | 60  | 100,000 |
| qwen-long | 1,200 | 3,000,000 |
| qwen-long-latest | 60,000 |
| qwen-long-2025-01-25 (qwen-long-0125) | 3   | 7,500 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-max | 600 | 1,000,000 |
| qwen3-max-2025-09-23 | 60  | 100,000 |
| qwen3-max-preview | 600 | 1,000,000 |
| qwen3.5-plus | 30,000 | 5,000,000 |
| qwen3.5-plus-2026-02-15 | 600 | 1,000,000 |
| qwen-plus | 15,000 | 5,000,000 |
| qwen-plus-2025-12-01 | 60  | 1,000,000 |
| qwen-plus-2025-09-11 |
| qwen-plus-2025-07-28 |
| qwen3.5-flash | 30,000 | 10,000,000 |
| qwen3.5-flash-2026-02-23 | 600 | 1,000,000 |
| qwen-flash | 15,000 | 10,000,000 |
| qwen-flash-2025-07-28 | 60  | 1,000,000 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-max | 600 | 1,000,000 |
| qwen3-max-2026-01-23 |
| qwen3-max-2025-09-23 | 60  | 100,000 |
| qwen3-max-preview | 600 | 1,000,000 |
| qwen-max | 600 | 1,000,000 |
| qwen-max-latest | 600 | 1,000,000 |
| qwen-max-2025-01-25 (qwen-max-0125) | 60  | 100,000 |
| qwen3.5-plus | 15,000 | 5,000,000 |
| qwen3.5-plus-2026-02-15 | 60  | 1,000,000 |
| qwen-plus-latest | 600 | 1,000,000 |
| qwen-plus-2025-12-01 | 120 |
| qwen-plus-2025-09-11 | 120 |
| qwen-plus-2025-07-28 | 60  | 100,000 |
| qwen-plus-2025-07-14 (qwen-plus-0714) |
| qwen-plus-2025-04-28 (qwen-plus-0428) | 1,000,000 |
| qwen-plus-2025-01-25 (qwen-plus-0125) | 100,000 |
| qwen3.5-flash | 15,000 | 5,000,000 |
| qwen3.5-flash-2026-02-23 | 60  | 1,000,000 |
| qwen-flash | 600 | 5,000,000 |
| qwen-flash-2025-07-28 | 600 | 5,000,000 |
| qwq-plus | 60  | 100,000 |
| qwen-turbo | 600 | 5,000,000 |
| qwen-turbo-latest | 600 | 5,000,000 |
| qwen-turbo-2025-04-28 (qwen-turbo-0428) | 60  | 1,000,000 |
| qwen-turbo-2024-11-01 (qwen-turbo-1101) | 5,000,000 |

## 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen-plus-us | 600 | 1,000,000 |
| qwen-plus-2025-12-01-us | 60  |
| qwen-flash-us | 600 | 5,000,000 |
| qwen-flash-2025-07-28-us |

### **千问VL（视觉理解/图生文）**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-vl-plus | 3,000 | 5,000,000 |
| qwen3-vl-plus-2025-12-19 | 60  | 100,000 |
| qwen3-vl-plus-2025-09-23 |
| qwen3-vl-flash | 3,000 | 5,000,000 |
| qwen3-vl-flash-2026-01-22 | 60  | 100,000 |
| qwen3-vl-flash-2025-10-15 |
| qwen-vl-max | 1,200 | 1,000,000 |
| qwen-vl-max-latest |
| qwen-vl-max-2025-08-13 （qwen-vl-max-0813） | 60  | 100,000 |
| qwen-vl-max-2025-04-08 （qwen-vl-max-0408） |
| qwen-vl-max-2025-04-02 （qwen-vl-max-0402） |
| qwen-vl-max-2025-01-25 （qwen-vl-max-0125） |
| qwen-vl-max-2024-12-30 （qwen-vl-max-1230） |
| qwen-vl-max-2024-11-19 （qwen-vl-max-1119） |
| qwen-vl-plus | 1,200 | 1,000,000 |
| qwen-vl-plus-latest |
| qwen-vl-plus-2025-08-15 （qwen-vl-plus-0815） | 60  | 100,000 |
| qwen-vl-plus-2025-07-10 （qwen-vl-plus-0710） |
| qwen-vl-plus-2025-05-07 （qwen-vl-plus-0507） |
| qwen-vl-plus-2025-01-25 （qwen-vl-plus-0125） |
| qwen-vl-plus-2025-01-02 （qwen-vl-plus-0102） |
| qvq-max |
| qvq-max-latest |
| qvq-max-2025-05-15 （qvq-max-0515） |
| qvq-max-2025-03-25 （qvq-max-0325） |
| qvq-plus |
| qvq-plus-latest |
| qvq-plus-2025-05-15 （qvq-plus-0515） |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-vl-plus | 1,200 | 1,000,000 |
| qwen3-vl-plus-2025-09-23 | 60  | 100,000 |
| qwen3-vl-flash | 1,200 | 1,000,000 |
| qwen3-vl-flash-2025-10-15 | 60  | 100,000 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-vl-plus | 1,200 | 1,000,000 |
| qwen3-vl-plus-2025-12-19 | 60  | 100,000 |
| qwen3-vl-plus-2025-09-23 | 120 | 1,000,000 |
| qwen3-vl-flash | 1,200 | 1,000,000 |
| qwen3-vl-flash-2026-01-22 | 60  | 100,000 |
| qwen3-vl-flash-2025-10-15 | 120 | 1,000,000 |
| qwen-vl-max | 1,200 | 1,000,000 |
| qwen-vl-max-latest |
| qwen-vl-max-2025-08-13 (qwen-vl-max-0813) | 60  | 100,000 |
| qwen-vl-max-2025-04-08 (qwen-vl-max-0408) | 1,200 | 1,000,000 |
| qwen-vl-plus |
| qwen-vl-plus-latest |
| qwen-vl-plus-2025-08-15 (qwen-vl-plus-0815) | 120 | 1,000,000 |
| qwen-vl-plus-2025-05-07 (qwen-vl-plus-0507) |
| qwen-vl-plus-2025-01-25 (qwen-vl-plus-0125) | 1,200 |
| qvq-max | 60  | 100,000 |
| qvq-max-latest |
| qvq-max-2025-03-25 (qvq-max-0325) |

## 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-vl-flash-us | 1,200 | 1,000,000 |
| qwen3-vl-flash-2025-10-15-us | 1,000,000 | 120 |

### **千问Omni**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3.5-omni-plus | 60  | 100,000 |
| qwen3.5-omni-plus-2026-03-15 |
| qwen3.5-omni-flash |
| qwen3.5-omni-flash-2026-03-15 |
| qwen3-omni-flash |
| qwen3-omni-flash-2025-12-01 |
| qwen3-omni-flash-2025-09-15 |
| qwen-omni-turbo |
| qwen-omni-turbo-latest |
| qwen-omni-turbo-2025-03-26 （qwen-omni-turbo-0326） |
| qwen-omni-turbo-2025-01-19 （qwen-omni-turbo-0119） |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3.5-omni-plus | 60  | 100,000 |
| qwen3.5-omni-plus-2026-03-15 |
| qwen3.5-omni-flash |
| qwen3.5-omni-flash-2026-03-15 |
| qwen3-omni-flash |
| qwen3-omni-flash-2025-12-01 |
| qwen3-omni-flash-2025-09-15 |
| qwen-omni-turbo |
| qwen-omni-turbo-latest |
| qwen-omni-turbo-2025-03-26 |

### **千问Omni-Realtime**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3.5-omni-plus-realtime | 60  | 100,000 |
| qwen3.5-omni-plus-realtime-2026-03-15 |
| qwen3.5-omni-flash-realtime |
| qwen3.5-omni-flash-realtime-2026-03-15 |
| qwen3-omni-flash-realtime |
| qwen3-omni-flash-realtime-2025-12-01 |
| qwen3-omni-flash-realtime-2025-09-15 |
| qwen-omni-turbo-realtime-latest |
| qwen-omni-turbo-realtime-2025-05-08 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3.5-omni-plus-realtime | 60  | 100,000 |
| qwen3.5-omni-plus-realtime-2026-03-15 |
| qwen3.5-omni-flash-realtime |
| qwen3.5-omni-flash-realtime-2026-03-15 |
| qwen3-omni-flash-realtime |
| qwen3-omni-flash-realtime-2025-12-01 |
| qwen3-omni-flash-realtime-2025-09-15 |
| qwen-omni-turbo-realtime | 10,000 |
| qwen-omni-turbo-realtime-latest |
| qwen-omni-turbo-realtime**\\-**2025-05-08 |

### **千问OCR（文字提取）**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen-vl-ocr | 600 | 6,000,000 |
| qwen-vl-ocr-latest | 1,200 |
| qwen-vl-ocr-2025-11-20 |
| qwen-vl-ocr-2025-08-28 | 600 |
| qwen-vl-ocr-2025-04-13 |
| qwen-vl-ocr-2024-10-28 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen-vl-ocr | 600 | 6,000,000 |
| qwen-vl-ocr-2025-11-20 | 1,200 |

## 国际

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen-vl-ocr | 600 | 6,000,000 |
| qwen-vl-ocr-2025-11-20 | 1,200 |

### **千问Audio（音频理解）**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen-audio-turbo | 120 | 100,000 |
| qwen-audio-turbo-latest | 60  |

### **千问数学模型**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen-math-plus | 1,200 | 1,000,000 |
| qwen-math-plus-latest |
| qwen-math-plus-2024-09-19 （qwen-math-plus-0919） | 60  | 100,000 |
| qwen-math-plus-2024-08-16 （qwen-math-plus-0816） | 10  | 20,000 |
| qwen-math-turbo | 1200 | 1,000,000 |
| qwen-math-turbo-latest |
| qwen-math-turbo-2024-09-19 （qwen-math-turbo-0919） | 60  | 100,000 |

### **千问Coder**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-coder-plus | 5,000 | 5,000,000 |
| qwen3-coder-plus-2025-09-23 | 60  | 1,000,000 |
| qwen3-coder-plus-2025-07-22 |
| qwen3-coder-flash | 5,000 | 5,000,000 |
| qwen3-coder-flash-2025-07-28 | 60  | 1,000,000 |
| qwen-coder-plus | 1,200 |
| qwen-coder-plus-latest |
| qwen-coder-plus-2024-11-06 （qwen-coder-plus-1106） | 120 | 200,000 |
| qwen-coder-turbo | 1,200 | 1,000,000 |
| qwen-coder-turbo-latest |
| qwen-coder-turbo-2024-09-19 （qwen-coder-turbo-0919） | 60  | 100,000 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-coder-plus | 2,400 | 2,000,000 |
| qwen3-coder-plus-2025-09-23 | 60  | 1,000,000 |
| qwen3-coder-plus-2025-07-22 |
| qwen3-coder-flash | 1,200 |
| qwen3-coder-flash-2025-07-28 | 60  |

## 国际

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-coder-plus | 2,400 | 2,000,000 |
| qwen3-coder-plus-2025-09-23 | 600 | 1,000,000 |
| qwen3-coder-plus-2025-07-22 | 60  | 1,000,000 |
| qwen3-coder-flash | 600 | 5,000,000 |
| qwen3-coder-flash-2025-07-28 | 600 | 5,000,000 |

### **千问翻译模型**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen-mt-plus | 60  | 25,000 |
| qwen-mt-flash | 35,000 |
| qwen-mt-lite | 100,000 |
| qwen-mt-turbo | 35,000 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen-mt-plus | 60  | 25,000 |
| qwen-mt-flash | 35,000 |
| qwen-mt-lite | 100,000 |

## 国际

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen-mt-plus | 60  | 100,000 |
| qwen-mt-flash |
| qwen-mt-lite |
| qwen-mt-turbo |

### **千问数据挖掘模型**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen-doc-turbo | 600 | 3,000,000 |

### **千问深入研究模型**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen-deep-research | 120 | 1,200,000 |

### **通义晓蜜对话分析模型**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| tongyi-xiaomi-analysis-flash | 600 | 1,000,000 |
| tongyi-xiaomi-analysis-pro |

## **文本生成-千问-开源版**

### **千问语言模型开源版**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3.5-397b-a17b | 600 | 1,000,000 |
| qwen3.5-122b-a10b |
| qwen3.5-27b |
| qwen3.5-35b-a3b |
| qwen3-next-80b-a3b-thinking |
| qwen3-next-80b-a3b-instruct |
| qwen3-235b-a22b-thinking-2507 |
| qwen3-235b-a22b-instruct-2507 |
| qwen3-30b-a3b-thinking-2507 |
| qwen3-30b-a3b-instruct-2507 |
| qwen3-235b-a22b |
| qwen3-30b-a3b |
| qwen3-32b | 2400 |
| qwen3-14b | 600 |
| qwen3-8b |
| qwen3-4b |
| qwen3-1.7b |
| qwen3-0.6b |
| qwq-32b |
| qwq-32b-preview | 1,200 |
| qwen2.5-72b-instruct |
| qwen2.5-32b-instruct |
| qwen2.5-14b-instruct |
| qwen2.5-14b-instruct-1m | 5,000,000 |
| qwen2.5-7b-instruct | 1,000,000 |
| qwen2.5-7b-instruct-1m | 5,000,000 |
| qwen2.5-3b-instruct | 2,000,000 |
| qwen2.5-1.5b-instruct |
| qwen2.5-0.5b-instruct |
| qwen2-72b-instruct | 60  | 150,000 |
| qwen2-57b-a14b-instruct |
| qwen2-7b-instruct |
| qwen2-1.5b-instruct | 2,000,000 |
| qwen2-0.5b-instruct |
| qwen1.5-110b-chat | 10  | 20,000 |
| qwen1.5-72b-chat | 120 | 200,000 |
| qwen1.5-32b-chat | 10  | 20,000 |
| qwen1.5-14b-chat | 120 | 200,000 |
| qwen1.5-7b-chat |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3.5-397b-a17b | 600 | 1,000,000 |
| qwen3.5-122b-a10b |
| qwen3.5-27b |
| qwen3.5-35b-a3b |
| qwen3-next-80b-a3b-thinking |
| qwen3-next-80b-a3b-instruct |
| qwen3-235b-a22b-thinking-2507 |
| qwen3-235b-a22b-instruct-2507 |
| qwen3-30b-a3b-thinking-2507 |
| qwen3-30b-a3b-instruct-2507 |
| qwen3-235b-a22b |
| qwen3-32b |
| qwen3-30b-a3b |
| qwen3-14b |
| qwen3-8b |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3.5-397b-a17b | 600 | 1,000,000 |
| qwen3.5-122b-a10b | 1,000,000 |
| qwen3.5-27b | 1,000,000 |
| qwen3.5-35b-a3b | 5,000,000 |
| qwen3-next-80b-a3b-thinking | 1,000,000 |
| qwen3-next-80b-a3b-instruct |
| qwen3-235b-a22b-thinking-2507 |
| qwen3-235b-a22b-instruct-2507 |
| qwen3-30b-a3b-thinking-2507 | 5,000,000 |
| qwen3-30b-a3b-instruct-2507 |
| qwen3-235b-a22b | 1,000,000 |
| qwen3-32b |
| qwen3-30b-a3b |
| qwen3-14b |
| qwen3-8b |
| qwen3-4b |
| qwen3-1.7b |
| qwen3-0.6b |
| qwen2.5-14b-instruct-1m | 1,200 | 5,000,000 |
| qwen2.5-7b-instruct-1m |
| qwen2.5-72b-instruct | 60  | 150,000 |
| qwen2.5-32b-instruct |
| qwen2.5-14b-instruct |
| qwen2.5-7b-instruct |

### **Qwen-VL**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-vl-32b-thinking | 600 | 1,000,000 |
| qwen3-vl-32b-instruct |
| qwen3-vl-30b-a3b-thinking |
| qwen3-vl-30b-a3b-instruct |
| qwen3-vl-8b-thinking |
| qwen3-vl-8b-instruct |
| qwen3-vl-235b-a22b-thinking | 60  | 100,000 |
| qwen3-vl-235b-a22b-instruct |
| qwen2.5-vl-72b-instruct |
| qwen2.5-vl-32b-instruct |
| qwen2.5-vl-7b-instruct | 1,200 | 1,000,000 |
| qwen2.5-vl-3b-instruct |
| qwen2-vl-72b-instruct |
| qwen2-vl-7b-instruct |
| qwen2-vl-2b-instruct |
| qwen-vl-v1 | 60  | 10,000 |
| qwen-vl-chat-v1 |
| qvq-72b-preview | 60  | 100,000 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-vl-235b-a22b-thinking | 60  | 100,000 |
| qwen3-vl-235b-a22b-instruct |
| qwen3-vl-32b-thinking | 600 | 1,000,000 |
| qwen3-vl-32b-instruct |
| qwen3-vl-30b-a3b-thinking |
| qwen3-vl-30b-a3b-instruct |
| qwen3-vl-8b-thinking |
| qwen3-vl-8b-instruct |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-vl-32b-thinking | 60  | 100,000 |
| qwen3-vl-32b-instruct |
| qwen3-vl-30b-a3b-thinking |
| qwen3-vl-30b-a3b-instruct |
| qwen3-vl-8b-thinking |
| qwen3-vl-8b-instruct |
| qwen3-vl-235b-a22b-thinking |
| qwen3-vl-235b-a22b-instruct |
| qwen2.5-vl-72b-instruct |
| qwen2.5-vl-32b-instruct |
| qwen2.5-vl-7b-instruct | 1,200 | 1,000,000 |
| qwen2.5-vl-3b-instruct |

### **Qwen-Omni**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen2.5-omni-7b | 60  | 100,000 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen2.5-omni-7b | 60  | 100,000 |

### **Qwen3-Omni-Captioner**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-omni-30b-a3b-captioner | 60  | 100,000 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-omni-30b-a3b-captioner | 60  | 100,000 |

### Qwen-Audio

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen-audio-chat | 120 | 100,000 |

### **Qwen-Math**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen2.5-math-72b-instruct | 1,200 | 1,000,000 |
| qwen2.5-math-7b-instruct |
| qwen2.5-math-1.5b-instruct |

### **Qwen-Coder**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-coder-next | 600 | 1,000,000 |
| qwen3-coder-480b-a35b-instruct |
| qwen3-coder-30b-a3b-instruct |
| qwen2.5-coder-32b-instruct | 1,200 |
| qwen2.5-coder-14b-instruct |
| qwen2.5-coder-7b-instruct |
| qwen2.5-coder-3b-instruct | 2,000,000 |
| qwen2.5-coder-1.5b-instruct |
| qwen2.5-coder-0.5b-instruct |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-coder-480b-a35b-instruct | 600 | 1,000,000 |
| qwen3-coder-30b-a3b-instruct | 600 | 1,000,000 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-coder-next | 600 | 1,000,000 |
| qwen3-coder-480b-a35b-instruct |
| qwen3-coder-30b-a3b-instruct |

## **文本生成-第三方模型**

### **DeepSeek**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| deepseek-v3.2 | 15,000 | 1,200,000 |
| deepseek-v3.2-exp | 15,000 | 1,200,000 |
| deepseek-v3.1 |
| deepseek-r1-0528 | 60  | 100,000 |
| deepseek-r1 | 15,000 | 1,200,000 |
| deepseek-v3 |
| deepseek-r1-distill-qwen-7b |
| deepseek-r1-distill-qwen-14b |
| deepseek-r1-distill-qwen-32b |
| deepseek-r1-distill-qwen-1.5b | 60  | 100,000 |
| deepseek-r1-distill-llama-8b |
| deepseek-r1-distill-llama-70b |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| deepseek-v3.2 | 10,000 | 1,200,000 |

### **DeepSeek-硅基流动直供**

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| siliconflow/deepseek-v3.2 | 500 | 500,000 |
| siliconflow/deepseek-v3.1-terminus |
| siliconflow/deepseek-r1-0528 |
| siliconflow/deepseek-v3-0324 |

### **Kimi**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| kimi-k2.5 | 500 | 1,000,000 |
| kimi-k2-thinking | 500 | 1,000,000 |
| Moonshot-Kimi-K2-Instruct | 500 | 1,000,000 |

### **Kimi-月之暗面直供**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| kimi/kimi-k2.5 | 500 | 3,000,000 |

### **GLM**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| glm-5 | 500 | 1,000,000 |
| glm-4.7 |
| glm-4.6 | 60  |
| glm-4.5 |
| glm-4.5-air |

### **GLM-智谱直供**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| ZHIPU/GLM-5 | 500 | 10,000,000 |

### **MiniMax**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| MiniMax-M2.5 | 500 | 1,000,000 |
| MiniMax-M2.1 | 500 | 1,000,000 |
| abab6.5s-chat | 60  | 100,000 |
| abab6.5t-chat | 1,060 |
| abab6.5g-chat | 60  |

### **MiniMax-稀宇科技直供**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| MiniMax/MiniMax-M2.7 | 500 | 20,000,000 |
| MiniMax/MiniMax-M2.5 |
| MiniMax/MiniMax-M2.1 |

### **Llama**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| llama-4-maverick-17b-128e-instruct | 10  | 20,000 |
| llama-4-scout-17b-16e-instruct |

### **百川**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| baichuan2-turbo-192k | 10  | 20,000 |
| baichuan2-turbo |

## **图像生成**

### **千问（Qwen-Image）**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- | --- |
| **任务下发接口调用限制** | **同时处理中任务数量（并发数）** |
| 文生图与图像编辑 | qwen-image-2.0-pro | 2 次/分钟 | 同步接口无限制 |
| qwen-image-2.0-pro-2026-03-03 | 2 次/分钟 | 同步接口无限制 |
| qwen-image-2.0 | 2 次/秒 | 同步接口无限制 |
| qwen-image-2.0-2026-03-03 | 2 次/秒 | 同步接口无限制 |
| 文生图 | qwen-image-max | 2 次/分钟 | 同步接口无限制 |
| qwen-image-max-2025-12-30 | 2 次/分钟 | 同步接口无限制 |
| qwen-image-plus | 2 次/秒 | 同步接口无限制 / 异步接口 2 |
| qwen-image-plus-2026-01-09 | 2 次/秒 | 同步接口无限制 |
| qwen-image | 2 次/秒 | 同步接口无限制 / 异步接口 2 |
| 图像编辑 | qwen-image-edit-max | 2 次/分钟 | 同步接口无限制 |
| qwen-image-edit-max-2026-01-16 | 2 次/分钟 | 同步接口无限制 |
| qwen-image-edit-plus | 2 次/秒 | 同步接口无限制 |
| qwen-image-edit-plus-2025-12-15 | 2 次/秒 | 同步接口无限制 |
| qwen-image-edit-plus-2025-10-30 | 2 次/秒 | 同步接口无限制 |
| qwen-image-edit | 2 次/秒 | 同步接口无限制 |
| 图像翻译 | qwen-mt-image | 1 次/秒 | 2   |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型服务** | **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- | --- |
| **任务下发接口调用限制** | **同时处理中任务数量（并发数）** |
| 文生图与图像编辑 | qwen-image-2.0-pro | 2 次/分钟 | 同步接口无限制 |
| qwen-image-2.0-pro-2026-03-03 | 2 次/分钟 | 同步接口无限制 |
| qwen-image-2.0 | 2 次/秒 | 同步接口无限制 |
| qwen-image-2.0-2026-03-03 | 2 次/秒 | 同步接口无限制 |
| 文生图 | qwen-image-max | 2 次/分钟 | 同步接口无限制 |
| qwen-image-max-2025-12-30 | 2 次/分钟 | 同步接口无限制 |
| qwen-image-plus | 2 次/秒 | 同步接口无限制 / 异步接口 2 |
| qwen-image-plus-2026-01-09 | 2 次/秒 | 同步接口无限制 |
| qwen-image | 2 次/秒 | 同步接口无限制 / 异步接口 2 |
| 图像编辑 | qwen-image-edit-max | 2 次/分钟 | 同步接口无限制 |
| qwen-image-edit-max-2026-01-16 | 2 次/分钟 | 同步接口无限制 |
| qwen-image-edit-plus | 2 次/秒 | 同步接口无限制 |
| qwen-image-edit-plus-2025-12-15 | 2 次/秒 | 同步接口无限制 |
| qwen-image-edit-plus-2025-10-30 | 2 次/秒 | 同步接口无限制 |
| qwen-image-edit | 2 次/秒 | 同步接口无限制 |

### **文生图-Z-Image**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- |
| **每秒钟任务下发接口RPS限制** | **同时处理中任务数量（并发数）** |
| z-image-turbo | 2   | 同步接口无限制 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- |
| **每秒钟任务下发接口RPS限制** | **同时处理中任务数量（并发数）** |
| z-image-turbo | 2   | 同步接口无限制 |

### **万相**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型服务** | **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- | --- |
| **每秒钟任务下发接口RPS限制** | **同时处理中任务数量（并发数）** |
| 文生图 | wan2.6-t2i | 1   | 5   |
| wan2.5-t2i-preview | 5   |
| wan2.2-t2i-plus | 2   | 2   |
| wan2.2-t2i-flash |
| wanx2.1-t2i-plus |
| wanx2.1-t2i-turbo |
| wanx2.0-t2i-turbo |
| 图像生成 | wan2.6-image | 5   | 5   |
| 通用图像编辑 | wan2.5-i2i-preview | 5   | 5   |
| wanx2.1-imageedit | 2   | 2   |
| 文生图 | wanx-v1 | 2   | 1   |
| 图像局部重绘 | wanx-x-painting |
| 涂鸦作画 | wanx-sketch-to-image-lite |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型服务** | **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- | --- |
| **每秒钟任务下发接口RPS限制** | **同时处理中任务数量（并发数）** |
| 文生图 | wan2.6-t2i | 5   | 5   |
| 图像生成 | wan2.6-image | 5   | 5   |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型服务** | **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- | --- |
| **每秒钟任务下发接口RPS限制** | **同时处理中任务数量（并发数）** |
| 文生图 | wan2.6-t2i | 5   | 5   |
| wan2.5-t2i-preview |
| wan2.2-t2i-flash | 2   | 2   |
| wan2.2-t2i-plus |
| wan2.1-t2i-turbo |
| wan2.1-t2i-plus |
| 图像生成 | wan2.6-image | 5   | 5   |
| 通用图像编辑 | wan2.5-i2i-preview | 5   | 5   |

### **图像编辑与生成**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- |
| **每秒钟任务下发接口RPS限制** | **同时处理中任务数量（并发数）** |
| shoemodel-v1 | 2   | 1   |
| wanx-virtualmodel |
| wanx-style-repaint-v1 | 2   |
| wanx-poster-generation-v1 | 1   |
| virtualmodel-v2 |
| wanx-background-generation-v2 |
| image-instance-segmentation |
| image-erase-completion |
| image-out-painting | 2   | 10  |

### **人物写真生成-FaceChain**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- |
| **作业提交接口RPS限制** | **同时处理中任务数量** |
| facechain-facedetect | 5   | 同步接口无限制 |
| facechain-finetune | 1   | 1   |
| facechain-generation | 2   |

### **创意文字生成-WordArt锦书**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- |
| **作业提交接口RPS限制** | **同时处理中任务数量** |
| wordart-texture | 2   | 1   |
| wordart-semantic |

### **AI试衣-OutfitAnyone**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- |
| **作业提交接口RPS限制** | **同时处理中任务数量** |
| aitryon | 10  | 5   |
| aitryon-plus | 10  | 5   |
| aitryon-parsing-v1 | 10  | 同步接口无限制 |
| aitryon-refiner | 10  | 5   |

## **图像生成-第三方模型**

### **StableDiffusion文生图模型**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- |
| **作业提交接口RPS限制** | **同时处理中任务数量** |
| stable-diffusion-3.5-large | 2   | 1 在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态。 |
| stable-diffusion-3.5-large-turbo |
| stable-diffusion-xl |
| stable-diffusion-v1.5 |

### **FLUX文生图模型**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- |
| **作业提交接口RPS限制** | **同时处理中任务数量** |
| flux-merged | 2   | 1 在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态。 |
| flux-dev |
| flux-schnell |

## **语音合成（文本转语音）**

### **千问语音合成**

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

##### **千问3-TTS-Instruct-Flash**

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-tts-instruct-flash | 180 |
| qwen3-tts-instruct-flash-2026-01-26 | 180 |

##### **千问3-TTS-VD**

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-tts-vd-2026-01-26 | 180 |

##### **千问3-TTS-VC**

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-tts-vc-2026-01-22 | 180 |

##### 千问3-TTS-Flash

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-tts-flash | 180 |
| qwen3-tts-flash-2025-11-27 | 180 |
| qwen3-tts-flash-2025-09-18 | 10  |

##### 千问-TTS

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen-tts | 10  | 100,000 |
| qwen-tts-latest |
| qwen-tts-2025-05-22 |
| qwen-tts-2025-04-10 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

##### **千问3-TTS-Instruct-Flash**

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-tts-instruct-flash | 180 |
| qwen3-tts-instruct-flash-2026-01-26 | 180 |

##### **千问3-TTS-VD**

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-tts-vd-2026-01-26 | 180 |

##### **千问3-TTS-VC**

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-tts-vc-2026-01-22 | 180 |

##### 千问3-TTS-Flash

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-tts-flash | 180 |
| qwen3-tts-flash-2025-11-27 | 180 |
| qwen3-tts-flash-2025-09-18 | 10  |

### **千问实时语音合成**

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

##### **千问3-TTS-Instruct-Flash-Realtime**

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-tts-instruct-flash-realtime | 180 |
| qwen3-tts-instruct-flash-realtime-2026-01-22 | 180 |

##### 千问3-TTS-VD-Realtime

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-tts-vd-realtime-2026-01-15 | 180 |
| qwen3-tts-vd-realtime-2025-12-16 |

##### 千问3-TTS-VC-Realtime

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-tts-vc-realtime-2026-01-15 | 180 |
| qwen3-tts-vc-realtime-2025-11-27 |

##### 千问3-TTS-Flash-Realtime

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-tts-flash-realtime | 180 |
| qwen3-tts-flash-realtime-2025-11-27 | 180 |
| qwen3-tts-flash-realtime-2025-09-18 | 10  |

##### 千问-TTS-Realtime

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen-tts-realtime | 10  | 100,000 |
| qwen-tts-realtime-latest |
| qwen-tts-realtime-2025-07-15 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

##### **千问3-TTS-Instruct-Flash-Realtime**

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-tts-instruct-flash-realtime | 180 |
| qwen3-tts-instruct-flash-realtime-2026-01-22 | 180 |

##### 千问3-TTS-VD-Realtime

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-tts-vd-realtime-2026-01-15 | 180 |
| qwen3-tts-vd-realtime-2025-12-16 |

##### 千问3-TTS-VC-Realtime

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-tts-vc-realtime-2026-01-15 | 180 |
| qwen3-tts-vc-realtime-2025-11-27 |

##### 千问3-TTS-Flash-Realtime

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-tts-flash-realtime | 180 |
| qwen3-tts-flash-realtime-2025-11-27 | 180 |
| qwen3-tts-flash-realtime-2025-09-18 | 10  |

### **千问声音复刻**

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen-voice-enrollment | 180 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen-voice-enrollment | 180 |

### **千问声音设计**

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen-voice-design | 180 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen-voice-design | 180 |

### **CosyVoice语音合成**

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **提交作业接口RPS限制** |
| --- | --- |
| cosyvoice-v3.5-plus | 3   |
| cosyvoice-v3.5-flash |
| cosyvoice-v3-plus |
| cosyvoice-v3-flash |
| cosyvoice-v2 |
| cosyvoice-v1 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **提交作业接口RPS限制** |
| --- | --- |
| cosyvoice-v3-plus | 3   |
| cosyvoice-v3-flash |

### **CosyVoice声音复刻/设计**

CosyVoice声音复刻共用一个模型，共用限流额度。

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **提交作业接口RPS限制** |
| --- | --- |
| voice-enrollment | 10  |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **提交作业接口RPS限制** |
| --- | --- |
| voice-enrollment | 10  |

### **Sambert语音合成**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型服务** | **提交作业接口RPS限制** |
| --- | --- |
| Sambert系列模型 | 20  |

## **语音识别（语音转文本）与翻译（语音转成指定语种的文本）**

### **千问3-LiveTranslate-Flash**

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-livetranslate-flash | 100 | 100,000 |
| qwen3-livetranslate-flash-2025-12-01 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-livetranslate-flash | 100 | 100,000 |
| qwen3-livetranslate-flash-2025-12-01 |

### **千问3-LiveTranslate-Flash-Realtime**

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-livetranslate-flash-realtime | 10  | 100,000 |
| qwen3-livetranslate-flash-realtime-2025-09-22 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-livetranslate-flash-realtime | 10  | 100,000 |
| qwen3-livetranslate-flash-realtime-2025-09-22 |

### **千问录音文件识别**

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

##### 千问3-ASR-Flash-Filetrans

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-asr-flash-filetrans | 100 |
| qwen3-asr-flash-filetrans-2025-11-17 |

##### **千问3-ASR-Flash**

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-asr-flash | 100 |
| qwen3-asr-flash-2026-02-10 |
| qwen3-asr-flash-2025-09-08 |

##### 千问ASR

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen-audio-asr | 60  | 100,000 |
| qwen-audio-asr-latest |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

##### 千问3-ASR-Flash-Filetrans

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-asr-flash-filetrans | 100 |
| qwen3-asr-flash-filetrans-2025-11-17 |

##### **千问3-ASR-Flash**

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-asr-flash | 100 |
| qwen3-asr-flash-2026-02-10 |
| qwen3-asr-flash-2025-09-08 |

#### 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| qwen3-asr-flash-us | 100 |
| qwen3-asr-flash-2025-09-08-us |

### **千问实时语音识别**

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **每秒钟调用次数（RPS）** |
| --- | --- |
| qwen3-asr-flash-realtime | 20  |
| qwen3-asr-flash-realtime-2026-02-10 |
| qwen3-asr-flash-realtime-2025-10-27 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **每秒钟调用次数（RPS）** |
| --- | --- |
| qwen3-asr-flash-realtime | 20  |
| qwen3-asr-flash-realtime-2026-02-10 |
| qwen3-asr-flash-realtime-2025-10-27 |

### **Gummy语音识别/翻译**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **提交作业接口RPS限制** |
| --- | --- |
| gummy-realtime-v1 | 10  |
| gummy-chat-v1 |

### **Fun-ASR录音文件识别**

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| fun-asr | 600 |
| fun-asr-2025-11-07 |
| fun-asr-2025-08-25 |
| fun-asr-mtl |
| fun-asr-mtl-2025-08-25 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| fun-asr | 600 |
| fun-asr-2025-11-07 |
| fun-asr-2025-08-25 |
| fun-asr-mtl |
| fun-asr-mtl-2025-08-25 |

### **Fun-ASR实时语音识别**

#### 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **提交作业接口RPS限制** |
| --- | --- |
| fun-asr-realtime | 20  |
| fun-asr-realtime-2026-02-28 |
| fun-asr-realtime-2025-11-07 |
| fun-asr-realtime-2025-09-15 |
| fun-asr-flash-8k-realtime |
| fun-asr-flash-8k-realtime-2026-01-28 |

#### 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **提交作业接口RPS限制** |
| --- | --- |
| fun-asr-realtime | 20  |
| fun-asr-realtime-2025-11-07 |

### **Paraformer语音识别**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **提交作业接口RPS限制** |
| --- | --- |
| paraformer-realtime-v2 | 20  |
| paraformer-realtime-v1 |
| paraformer-realtime-8k-v2 |
| paraformer-realtime-8k-v1 |

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| paraformer-v2 | 1,200 |

| **模型名称** | **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| --- | --- | --- |
| paraformer-v1 | 600 | 6,000,000 |
| paraformer-mtl-v1 | 600 | 6,000,000 |

| **模型名称** | **提交作业接口RPS限制** | **同时处理中任务数量（并发数）** |
| --- | --- | --- |
| paraformer-8k-v2 | 20  | 100 |
| paraformer-8k-v1 | 10  | 500 |

### **SenseVoice语音识别**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **每分钟调用次数（RPM）** |
| --- | --- |
| sensevoice-v1 | 1,200 |

## **视频生成**

### **万相系列**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型服务** | **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- | --- |
| **每秒钟任务下发接口RPS限制** | **同时处理中任务数量（并发数）** |
| 文生视频 | wan2.6-t2v | 5   | 5   |
| wan2.5-t2v-preview | 5   | 5   |
| wan2.2-t2v-plus | 2   | 2   |
| wanx2.1-t2v-turbo |
| wanx2.1-t2v-plus |
| 图生视频-基于首帧 | wan2.6-i2v-flash | 5   | 5   |
| wan2.6-i2v |
| wan2.5-i2v-preview |
| wan2.2-i2v-flash | 2   | 2   |
| wan2.2-i2v-plus |
| wanx2.1-i2v-turbo |
| wanx2.1-i2v-plus |
| 图生视频-基于首尾帧 | wan2.2-kf2v-flash |
| wanx2.1-kf2v-plus |
| 通用视频编辑 | wanx2.1-vace-plus |
| 参考生视频 | wan2.6-r2v-flash | 5   | 5   |
| wan2.6-r2v | 5   | 5   |
| 数字人s2v | wan2.2-s2v-detect | 5   | 同步接口无限制 |
| wan2.2-s2v | 1   |
| 图生动作 | wan2.2-animate-move | 5   | 1   |
| 视频换人 | wan2.2-animate-mix | 5   | 1   |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型服务** | **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- | --- |
| **每秒钟任务下发接口RPS限制** | **同时处理中任务数量（并发数）** |
| 文生视频 | wan2.6-t2v | 5   | 5   |
| 图生视频-基于首帧 | wan2.6-i2v |
| 参考生视频 | wan2.6-r2v |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型服务** | **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- | --- |
| **每秒钟任务下发接口RPS限制** | **同时处理中任务数量（并发数）** |
| 文生视频 | wan2.6-t2v | 5   | 5   |
| wan2.5-t2v-preview |
| wan2.2-t2v-plus | 2   | 2   |
| wan2.1-t2v-turbo |
| wan2.1-t2v-plus |
| 图生视频-基于首帧 | wan2.6-i2v-flash | 5   | 5   |
| wan2.6-i2v |
| wan2.5-i2v-preview |
| wan2.2-i2v-plus | 2   | 2   |
| wan2.1-i2v-turbo |
| wan2.1-i2v-plus |
| 图生视频-基于首尾帧 | wan2.1-kf2v-plus | 1   |
| 通用视频编辑 | wan2.1-vace-plus | 2   |
| 参考生视频 | wan2.6-r2v-flash | 5   | 5   |
| wan2.6-r2v | 5   | 5   |
| 图生动作 | wan2.2-animate-move | 5   | 1   |
| 视频换人 | wan2.2-animate-mix | 5   | 1   |

## 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

| **模型服务** | **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- | --- |
| **每秒钟任务下发接口RPS限制** | **同时处理中任务数量（并发数）** |
| 文生视频 | wan2.6-t2v-us | 5   | 5   |
| 图生视频-基于首帧 | wan2.6-i2v-us |

### **舞动人像AnimateAnyone**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **任务下发接口RPS限制** | **同时处理中任务数量** |
| --- | --- | --- |
| animate-anyone-detect-gen2 | 5   | 同步接口无限制 |
| animate-anyone-template-gen2 | 1 在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态。 |
| animate-anyone-gen2 |
| animate-anyone-detect | 1算力单元支持2并发 |
| animate-anyone | 1算力单元支持1并发 |

### **悦动人像EMO**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **任务下发接口RPS限制** | **同时处理中任务数量** |
| --- | --- | --- |
| emo-detect-v1 | 5   | 同步接口无限制 |
| emo-v1 | 1 在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态。 |

### **灵动人像LivePortrait**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **任务下发接口RPS限制** | **同时处理中任务数量** |
| --- | --- | --- |
| liveportrait-detect | 5   | 同步接口无限制 |
| liveportrait | 1 在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态。 |

### **声动人像VideoRetalk**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **任务下发接口RPS限制** | **同时处理中任务数量** |
| --- | --- | --- |
| videoretalk | 1   | 1 在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态。 |

### **表情包Emoji**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **任务下发接口RPS限制** | **同时处理中任务数量** |
| --- | --- | --- |
| emoji-detect-v1 | 1   | 同步接口无限制 |
| emoji-v1 | 1 在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态。 |

### **视频风格重绘**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **任务下发接口RPS限制** | **同时处理中任务数量** |
| --- | --- | --- |
| video-style-transform | 20  | 2 在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态。 |

## **视频生成-第三方模型**

### **爱诗系列**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型服务** | **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- | --- |
| **每秒钟任务下发接口RPS限制** | **同时处理中任务数量（并发数）** |
| 文生视频 | pixverse/pixverse-v5.6-t2v | 5   | 5 > 同一个阿里云百炼API Key 在 4 个模型间共享额度。 |
| 图生视频-基于首帧 | pixverse/pixverse-v5.6-it2v | 5   |
| 图生视频-基于首尾帧 | pixverse/pixverse-v5.6-kf2v | 5   |
| 参考生视频 | pixverse/pixverse-v5.6-r2v | 5   |

### **可灵系列**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- |
| **每秒钟任务下发接口RPS限制** | **同时处理中任务数量（并发数）** |
| kling/kling-v3-video-generation | 5   | 10 > 同一个阿里云百炼API Key 在 4 个模型间共享并发额度。 |
| kling/kling-v3-omni-video-generation | 5   |
| kling/kling-v3-image-generation | 5   |
| kling/kling-v3-omni-image-generation | 5   |

### **Vidu系列**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型服务** | **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- | --- |
| **每秒钟任务下发接口RPS限制** | **同时处理中任务数量（并发数）** |
| 文生视频 | vidu/viduq3-turbo\\_text2video | 5   | 5 > 同一个阿里云百炼API Key 在 13 个模型间共享并发额度。 |
| vidu/viduq3-pro\\_text2video | 5   |
| vidu/viduq2\\_text2video | 5   |
| 图生视频-基于首帧 | vidu/viduq3-turbo\\_img2video | 5   |
| vidu/viduq3-pro\\_img2video | 5   |
| vidu/viduq2-turbo\\_img2video | 5   |
| vidu/viduq2-pro\\_img2video | 5   |
| 图生视频-基于首尾帧 | vidu/viduq3-turbo\\_start-end2video | 5   |
| vidu/viduq3-pro\\_start-end2video | 5   |
| vidu/viduq2-turbo\\_start-end2video | 5   |
| vidu/viduq2-pro\\_start-end2video | 5   |
| 参考生视频 | vidu/viduq2-pro\\_reference2video | 5   |
| vidu/viduq2\\_reference2video | 5   |

## **向量模型**

### **文本向量**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- |
| **每秒钟调用次数（RPS）** | **每分钟消耗Token数（TPM）/作业数** > **仅输入Token** |
| text-embedding-v1 | 30  | 1,200,000 |
| text-embedding-v2 |
| text-embedding-v3 |
| text-embedding-v4 |
| text-embedding-async-v1 | 1   | 当前用户在系统通用文本向量异步作业排队中和运行中的作业数量不超过50个。 另外，为了避免大量突发的作业占据太多资源，限制并发的作业数为3个，即任意时间，单个用户最多只有3个通用文本向量的异步作业在并发运行，其他的作业只能在队列中等待。 |
| text-embedding-async-v2 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）/作业数** > **含输入与输出Token** |
| text-embedding-v3 | 6,000 | 24,000,000 |

### **多模态向量**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **仅输入Token** |
| qwen3-vl-embedding | 2,400 | 1,200,000 |
| qwen2.5-vl-embedding | 1,200 | 600,000 |
| tongyi-embedding-vision-plus | 600 | 200,000 |
| tongyi-embedding-vision-flash |
| tongyi-embedding-vision-flash-2026-03-06 | 1,200 | 9,600,000 |
| tongyi-embedding-vision-plus-2026-03-06 |
| multimodal-embedding-v1 | 120 | 1,000,000 |

## **文本分类、抽取、排序**

### **OpenNLU**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| opennlu-v1 | 60  | 10,000 |

### **文本排序模型**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-rerank | 5,400 | 5,000,000,000 |
| gte-rerank-v2 | 5,040 | 4,980,000,000 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen3-rerank | 5,400 | 5,000,000,000 |
| gte-rerank-v2 | 5,040 | 4,980,000,000 |

## **行业**

### **通义法睿（法律模型）**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| farui-plus | 240 | 1,000,000 |

### **意图理解**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| tongyi-intent-detect-v3 | 1,200 | 1,000,000 |

### **角色扮演**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen-plus-character | 120 | 500,000 |
| qwen-flash-character |
| qwen-flash-character-2026-02-26 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| qwen-plus-character-ja | 120 | 500,000 |

### 界面交互

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **限流条件（超出任一数值时触发限流）** > **以下为每分钟限流条件，服务可能按 RPS（RPM/60）与 TPS（TPM/60）限制** |   |
| --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| gui-plus | 80  | 540,000 |
| gui-plus-2026-02-26 | 100 | 540,000 |

## **已下线模型**

> 详细信息，请参见[模型下线机制说明](https://help.aliyun.com/zh/model-studio/model-depreciation)。

## 2026年1月30日下线

| **类别** | **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| 千问Max | qwen-max-2024-04-03 | 0   | 0   |
| 千问Plus | qwen-plus-2024-11-27 |
| qwen-plus-2024-11-25 |
| qwen-plus-2024-09-19 |
| qwen-plus-2024-08-06 |
| qwen-plus-2024-07-23 |
| 千问Turbo | qwen-turbo-2024-09-19 |
| qwen-turbo-2024-06-24 |
| 千问VL | qwen-vl-max-2024-10-30 |
| qwen-vl-max-2024-08-09 |
| qwen-vl-plus-2024-08-09 |
| 千问Audio | qwen-audio-turbo-2024-12-04 |
| qwen-audio-turbo-2024-08-07 |
| qwen-audio-asr-2024-12-04 |

## 2025年7月30日下线

| **类别** | **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| 千问VL | qwen-vl-plus-2023-12-01 | 0   | 0   |
| 零一万物 | yi-large |
| yi-medium |
| yi-large-rag |
| yi-large-turbo |
| Dolly | dolly-12b-v2 |

## 2025年7月2日下线

| **类别** | **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| Llama-仅文本输入 | llama3.3-70b-instruct | 0   | 0   |
| llama3.2-3b-instruct |
| llama3.2-1b-instruct |
| llama3.1-405b-instruct |
| llama3.1-70b-instruct |
| llama3.1-8b-instruct |
| llama3-70b-instruct |
| llama3-8b-instruct |
| llama2-13b-chat-v2 |
| llama2-7b-chat-v2 |
| Llama-文本和图像输入 | llama3.2-90b-vision-instruct |
| llama3.2-11b-vision |
| 百川-开源版 | baichuan2-13b-chat-v1 |
| baichuan2-7b-chat-v1 |
| baichuan-7b-v1 |
| ChatGLM | chatglm3-6b |
| chatglm-6b-v2 |
| 姜子牙 | ziya-llama-13b-v1 |
| BELLE | belle-llama-13b-2m-v1 |
| 元语  | chatyuan-large-v2 |
| BiLLa | billa-7b-sft-v1 |

| **类别** | **模型名称** | **限流条件（超出任一数值时触发限流）** |   |
| --- | --- | --- | --- |
| **每秒钟任务下发接口RPS限制** | **同时处理中任务数量** |
| 动漫人物生成 | wanx-style-cosplay-v1 | 0   | 0   |
| 图配文 | wanx-ast |
| 创意文字生成-WordArt锦书 | wordart-surnames |
| AnyText图文融合 | wanx-anytext-v1 |

## 2025年5月8日下线

| **类别** | **模型名称** | **限流条件（超出任一数值时触发限流）** |   | **替代模型** |
| --- | --- | --- | --- | --- |
| **每分钟调用次数（RPM）** | **每分钟消耗Token数（TPM）** > **含输入与输出Token** |
| 文本生成-千问 | qwen-max-2024-01-07 （qwen-max-0107） | 0   | 0   | qwen-max |
| qwen-plus-2024-06-24 （qwen-plus-0624） | qwen-plus |
| qwen-plus-2024-02-06 （qwen-plus-0206） |
| qwen-turbo-2024-02-06 （qwen-turbo-0206） | qwen-turbo |
| qwen-vl-max-2024-02-01 （qwen-vl-max-0201） | qwen-vl-max |
| 文本生成-千问-开源版 | qwen-72b-chat | qwen2.5-72b-instruct |
| qwen-14b-chat | qwen2.5-14b-instruct |
| qwen-7b-chat | qwen2.5-7b-instruct |
| qwen-1.8b-chat | qwen2.5-1.5b-instruct |
| qwen-1.8b-longcontext-chat | qwen2.5-1.5b-instruct |
| qwen2-math-72b-instruct | qwen2.5-math-72b-instruct |
| qwen2-math-7b-instruct | qwen2.5-math-7b-instruct |
| qwen2-math-1.5b-instruct | qwen2.5-math-1.5b-instruct |

| **类别** | **模型名称** | **限流条件（超出任一数值时触发限流）** |   | **替代模型** |
| --- | --- | --- | --- | --- |
| **任务下发接口RPS限制** | **同时处理中任务数量** |
| 幻影人像Motionshop视频生成模型 | motionshop-video-detect | 0   | 0   | 使用animate-anyone-gen2的“按视频背景生成”功能，可达到近似效果 |
| motionshop-gen3d |
| motionshop-synthesis |
在使用百炼模型服务时，您需要选择两个关键配置项：

-   **地域**：决定模型服务的接入位置和用户静态数据的存储位置。
    
-   **部署模式**：决定推理计算可以在哪些区域执行。
    

这两个配置相互独立，但**必须按预定义组合使用**。它们共同影响服务的**延时、成本、可用模型及默认限流**。无论选择哪种部署模式，**您的静态数据**（包括输入、输出）始终存储在所选地域内。

> **提示**：地域控制“数据存储在哪”，部署模式控制“推理计算在哪”。两者结合，帮助您平衡性能、成本与合规需求。

## **如何选择地域**

模型服务的地域是指您接入百炼模型服务的物理节点位置。选择地域时，请考量以下维度：

-   **访问延迟：**物理距离直接影响响应速度。建议选择靠近您或您的终端用户的地域，以最小化网络延迟。
    
-   **合规准入：**业务部署须符合当地法律法规，请根据您的合规诉求选择合适您的静态数据存储位置。
    
-   **可用功能：**不同地域支持的功能或模型可能不同，详情请参考[各地域支持的功能](#798c325740yek)和[模型列表](https://help.aliyun.com/zh/model-studio/models)文档。
    

当前支持的地域：华北2（北京）、美国（弗吉尼亚）、新加坡

> 所有用户静态数据均存储在所选地域，符合本地数据驻留要求。

## 部署模式对比

部署模式决定了模型推理的计算区域，地域和部署模式二者为预设绑定关系，不支持自由组合。

为了降低网络延迟、提升模型响应速度，建议根据您主要用户或业务应用的地理位置选择就近地域对应的部署模式：

| **部署模式** | **绑定地域（数据存储）** | **模型推理计算范围** |
| --- | --- | --- |
| **中国内地** | 华北2（北京） | 仅限中国内地 |
| **全球** | 美国（弗吉尼亚） | 全球动态调度 |
| **国际** | 新加坡 | 全球动态调度（不含中国内地） |
| **美国** | 美国（弗吉尼亚） | 仅限美国境内 |

-   **全球模式**：适用于用户遍布全球且追求模型高可用性的业务。该模式利用全球分布的计算资源，模型可用性有保障。
    
-   **国际模式**：适用于服务海外用户（如亚太，美国等），但由于业务策略或合规需求，需明确排除使用中国内地大陆境内计算资源的场景。
    
-   **中国内地模式**：适用于主要服务中国境内用户，且必须严格满足中国等境内监管要求的场景。
    
-   **美国模式** ：适用于业务主体在美国，或受美国法规限制，需确保所有数据处理与推理行为均严格限于美国境内的场景。
    

**重要**

在**全球**部署模式和**国际**部署模式下，由于**涉及跨境计算**，您需自行确保用户业务数据跨境处理的合法性。跨区推理请求由所选地域的前端接入点接收。模型调用过程中产生的静态数据（如提示词输入、模型输出等）仅在推理过程中进行瞬时处理，不会在计算节点所在地域进行持久化存储；数据在传输过程中全程加密。

## **如何使用**

### **使用****中国内地****部署模式的模型**

使用前，请先配置请求地址、API Key和模型名称：

-   **请求地址（Base URL）**：中国内地部署模式绑定华北2（北京）地域，请使用`dashscope.aliyuncs.com`域名。以下为部分请求地址示例，其他 API 请参考对应文档：
    
    -   OpenAI Chat Completions API ：`https://dashscope.aliyuncs.com/compatible-mode/v1`
        
    -   DashScope：`https://dashscope.aliyuncs.com/api/v1`
        
-   **API Key**：请前往[密钥管理（北京）](https://bailian.console.aliyun.com/?tab=model#/api-key)页面获取。
    
-   **模型名称**：请参考[模型列表](https://help.aliyun.com/zh/model-studio/models)，选择中国内地部署模式的模型。
    

### **使用****全球****部署模式的模型**

使用前，请先配置请求地址、API Key和模型名称：

-   **请求地址（Base URL）**：全球部署模式绑定美国（弗吉尼亚）地域，请使用`dashscope-us.aliyuncs.com`域名。以下为部分请求地址示例，其他 API 请参考对应文档：
    
    -   OpenAI Chat Completions API ：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
        
    -   DashScope：`https://dashscope-us.aliyuncs.com/api/v1`
        
-   **API Key**：请前往[密钥管理（弗吉尼亚）](https://modelstudio.console.aliyun.com/us-east-1?tab=model#/api-key)页面获取。
    
-   **模型名称**：请参考[模型列表](https://help.aliyun.com/zh/model-studio/models)，选择全球部署模式的模型。
    

### **使用****国际****部署模式的模型**

使用前，请先配置请求地址、API Key和模型名称：

-   **请求地址（Base URL）**：国际部署模式绑定新加坡地域，请使用`dashscope-intl.aliyuncs.com`域名。以下为部分请求地址示例，其他 API 请参考对应文档：
    
    -   OpenAI Chat Completions API ：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
        
    -   DashScope：`https://dashscope-intl.aliyuncs.com/api/v1`
        
-   **API Key**：请前往[密钥管理（新加坡）](https://modelstudio.console.aliyun.com/?tab=model#/api-key)页面获取。
    
-   **模型名称**：请参考[模型列表](https://help.aliyun.com/zh/model-studio/models)，选择国际部署模式的模型。
    

### **使用****美国****部署模式的模型**

使用前，请先配置请求地址、API Key和模型名称：

-   **请求地址（Base URL）**：美国部署模式绑定美国（弗吉尼亚）地域，请使用`dashscope-us.aliyuncs.com`域名。以下为部分请求地址示例，其他 API 请参考对应文档：
    
    -   OpenAI Chat Completions API ：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
        
    -   DashScope：`https://dashscope-us.aliyuncs.com/api/v1`
        
-   **API Key**：请前往[密钥管理（弗吉尼亚）](https://modelstudio.console.aliyun.com/us-east-1?tab=model#/api-key)页面获取。
    
-   **模型名称**：请参考[模型列表](https://help.aliyun.com/zh/model-studio/models)，选择美国部署模式的模型（带`-us`后缀）。
    

### **异步任务**

对于异步任务（如图像生成、视频生成），所有后续操作必须使用创建任务时所用的服务域名和 API Key，否则会导致报错。

以下是在全球部署模式（美国地域）下创建图像生成任务并查询结果的示例。如使用德国地域，请将服务域名替换为`{WorkspaceId}.eu-central-1.maas.aliyuncs.com`：

```
# 创建任务（全球部署模式-美国地域，服务域名dashscope-us.aliyuncs.com）
curl --location 'https://dashscope-us.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'X-DashScope-Async: enable' \
--data '{
    "model": "wan2.6-t2i",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵"
                    }
                ]
            }
        ]
    },
    "parameters": {
        "n": 1
    }
}'

# 响应示例：{"output":{"task_id":"abc123..."},"request_id":"..."}

# 查询任务（必须使用相同服务域名）
curl -X GET https://dashscope-us.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"

# [错误] 使用其他服务域名查询将导致报错
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## **各地域支持的功能**

百炼在各地域提供的平台能力略有差异，但均适用于该地域下所有可用的部署模式：

| **板块** | **功能** | **华北2（北京）** | **新加坡** | **美国（弗吉尼亚）** |
| --- | --- | --- | --- | --- |
| **使用** | **实时推理** | 支持  | 支持  | 支持  |
| **批量推理** | 支持  | 支持  | 不支持 |
| **模型体验** | 支持  | 支持  | 支持  |
| **管理** | **模型监控** | 支持  | 支持  | 支持  |
| **模型告警** | 支持  | 支持  | 不支持 |
| **传输安全** | 支持  | 支持  | 支持  |
| **权限管理** | 支持  | 支持  | 支持  |
| **优化** | **模型调优** | 支持  | 支持  | 支持  |

## **相关文档**

-   [通义千问API参考](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)
    
-   [模型列表](https://help.aliyun.com/zh/model-studio/models)：查看各部署模式支持的模型以及上下文等信息。
    
-   [模型调用计费](https://help.aliyun.com/zh/model-studio/model-pricing)：查看各部署模式的价格差异。
    
-   [限流](https://help.aliyun.com/zh/model-studio/rate-limit)：查看各部署模式的RPM、TPM限制。
    
-   [获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)：为各部署模式创建和管理 API Key。
    
## **文本生成-千问**

### **千问Max**

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费；若模型支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)，仅输入Token享有折扣。两者不能同时生效。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **模式** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链+回答** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| qwen3-max > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 非思考和思考模式 | 0<Token≤32K | 2.5元 | 10元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| 32K<Token≤128K | 4元  | 16元 |
| 128K<Token≤252K | 7元  | 28元 |
| qwen3-max-2026-01-23 | 非思考和思考模式 | 0<Token≤32K | 2.5元 | 10元 |
| 32K<Token≤128K | 4元  | 16元 |
| 128K<Token≤252K | 7元  | 28元 |
| qwen3-max-2025-09-23 | 仅非思考模式 | 0<Token≤32K | 6元  | 24元 |
| 32K<Token≤128K | 10元 | 40元 |
| 128K<Token≤252K | 15元 | 60元 |
| qwen3-max-preview > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 非思考和思考模式 | 0<Token≤32K | 6元  | 24元 |
| 32K<Token≤128K | 10元 | 40元 |
| 128K<Token≤252K | 15元 | 60元 |

##### **更多模型**

| **模型名称** | **模式** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| qwen-max > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 仅非思考模式 | 无阶梯计价 | 2.4元 | 9.6元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen-max-latest > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 仅非思考模式 | 无阶梯计价 | 2.4元 | 9.6元 |
| qwen-max-2025-01-25 | 仅非思考模式 | 无阶梯计价 | 2.4元 | 9.6元 |
| qwen-max-2024-09-19 | 仅非思考模式 | 无阶梯计价 | 20元 | 60元 |
| qwen-max-2024-04-28 | 仅非思考模式 | 无阶梯计价 | 40元 | 120元 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

**说明**

全球部署模式的模型无免费额度。

| **模型名称** | **模式** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链+回答** |
| --- | --- | --- | --- | --- |
| qwen3-max > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 仅非思考模式 | 0<Token≤32K | 2.5元 | 10元 |
| 32K<Token≤128K | 4元  | 16元 |
| 128K<Token≤252K | 7元  | 28元 |
| qwen3-max-2025-09-23 | 仅非思考模式 | 0<Token≤32K | 6元  | 24元 |
| 32K<Token≤128K | 10元 | 40元 |
| 128K<Token≤252K | 15元 | 60元 |
| qwen3-max-preview > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 非思考和思考模式 | 0<Token≤32K | 6元  | 24元 |
| 32K<Token≤128K | 10元 | 40元 |
| 128K<Token≤252K | 15元 | 60元 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **模式** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链+回答** |
| --- | --- | --- | --- | --- |
| qwen3-max > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 非思考和思考模式 | 0<Token≤32K | 8.807元 | 44.035元 |
| 32K<Token≤128K | 17.614元 | 88.071元 |
| 128K<Token≤252K | 22.018元 | 110.089元 |
| qwen3-max-2026-01-23 | 非思考和思考模式 | 0<Token≤32K | 8.807元 | 44.035元 |
| 32K<Token≤128K | 17.614元 | 88.071元 |
| 128K<Token≤252K | 22.018元 | 110.089元 |
| qwen3-max-2025-09-23 | 仅非思考模式 | 0<Token≤32K | 8.807元 | 44.035元 |
| 32K<Token≤128K | 17.614元 | 88.071元 |
| 128K<Token≤252K | 22.018元 | 110.089元 |
| qwen3-max-preview > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 非思考和思考模式 | 0<Token≤32K | 8.807元 | 44.035元 |
| 32K<Token≤128K | 17.614元 | 88.071元 |
| 128K<Token≤252K | 22.018元 | 110.089元 |

##### **更多模型**

| **模型名称** | **模式** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** |
| --- | --- | --- | --- | --- |
| qwen-max > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 仅非思考模式 | 无阶梯计价 | 11.743元 | 46.971元 |
| qwen-max-latest | 仅非思考模式 | 无阶梯计价 | 11.743元 | 46.971元 |
| qwen-max-2025-01-25 | 仅非思考模式 | 无阶梯计价 | 11.743元 | 46.971元 |

### **千问Plus**

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单次请求的输入Token范围** | **输入单价（每百万Token）** | **输出单价（每百万Token）** |   | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **非思考模式** | **思考模式（思维链+回答）** |
| qwen3.5-plus | 0<Token≤128K | 0.8元 | 4.8元 | 4.8元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| 128K<Token≤256K | 2元  | 12元 | 12元 |
| 256K<Token≤1M | 4元  | 24元 | 24元 |
| qwen3.5-plus-2026-02-15 | 0<Token≤128K | 0.8元 | 4.8元 | 4.8元 |
| 128K<Token≤256K | 2元  | 12元 | 12元 |
| 256K<Token≤1M | 4元  | 24元 | 24元 |
| qwen-plus > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 0<Token≤128K | 0.8元 | 2元  | 8元  |
| 128K<Token≤256K | 2.4元 | 20元 | 24元 |
| 256K<Token≤1M | 4.8元 | 48元 | 64元 |
| qwen-plus-latest > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 0<Token≤128K | 0.8元 | 2元  | 8元  |
| 128K<Token≤256K | 2.4元 | 20元 | 24元 |
| 256K<Token≤1M | 4.8元 | 48元 | 64元 |
| qwen-plus-2025-12-01 | 0<Token≤128K | 0.8元 | 2元  | 8元  |
| 128K<Token≤256K | 2.4元 | 20元 | 24元 |
| 256K<Token≤1M | 4.8元 | 48元 | 64元 |
| qwen-plus-2025-09-11 | 0<Token≤128K | 0.8元 | 2元  | 8元  |
| 128K<Token≤256K | 2.4元 | 20元 | 24元 |
| 256K<Token≤1M | 4.8元 | 48元 | 64元 |
| qwen-plus-2025-07-28 | 0<Token≤128K | 0.8元 | 2元  | 8元  |
| 128K<Token≤256K | 2.4元 | 20元 | 24元 |
| 256K<Token≤1M | 4.8元 | 48元 | 64元 |
| qwen-plus-2025-07-14 | 无阶梯计价 | 0.8元 | 2元  | 8元  |
| qwen-plus-2025-04-28 | 无阶梯计价 | 0.8元 | 2元  | 8元  |

##### **更多模型**

| **模型名称** | **单次请求的输入Token范围** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| qwen-plus-2025-01-25 | 无阶梯计价 | 0.8元 | 2元  | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen-plus-2025-01-12 | 无阶梯计价 | 0.8元 | 2元  |
| qwen-plus-2024-12-20 | 无阶梯计价 | 0.8元 | 2元  |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

**说明**

全球部署模式的模型无免费额度。

| **模型名称** | **单次请求的输入Token范围** | **输入单价 （每百万Token）** | **输出单价 （每百万Token）** |   |
| --- | --- | --- | --- | --- |
| **非思考模式** | **思考模式（思维链+回答）** |
| qwen3.5-plus | 0<Token≤128K | 0.8元 | 4.8元 | 4.8元 |
| 128K<Token≤256K | 2元  | 12元 | 12元 |
| 256K<Token≤1M | 4元  | 24元 | 24元 |
| qwen3.5-plus-2026-02-15 | 0<Token≤128K | 0.8元 | 4.8元 | 4.8元 |
| 128K<Token≤256K | 2元  | 12元 | 12元 |
| 256K<Token≤1M | 4元  | 24元 | 24元 |
| qwen-plus | 0<Token≤128K | 0.8元 | 2元  | 8元  |
| 128K<Token≤256K | 2.4元 | 20元 | 24元 |
| 256K<Token≤1M | 4.8元 | 48元 | 64元 |
| qwen-plus-2025-12-01 | 0<Token≤128K | 0.8元 | 2元  | 8元  |
| 128K<Token≤256K | 2.4元 | 20元 | 24元 |
| 256K<Token≤1M | 4.8元 | 48元 | 64元 |
| qwen-plus-2025-09-11 | 0<Token≤128K | 0.8元 | 2元  | 8元  |
| 128K<Token≤256K | 2.4元 | 20元 | 24元 |
| 256K<Token≤1M | 4.8元 | 48元 | 64元 |
| qwen-plus-2025-07-28 | 0<Token≤128K | 0.8元 | 2元  | 8元  |
| 128K<Token≤256K | 2.4元 | 20元 | 24元 |
| 256K<Token≤1M | 4.8元 | 48元 | 64元 |

## **国际**

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **单次请求的输入Token范围** | **输入单价 （每百万Token）** | **输出单价 （每百万Token）** |   |
| --- | --- | --- | --- | --- |
| **非思考模式** | **思考模式（思维链+回答）** |
| qwen3.5-plus | 0<Token≤256K | 2.936元 | 17.614元 | 17.614元 |
| 256K<Token≤1M | 3.67元 | 22.018元 | 22.018元 |
| qwen3.5-plus-2026-02-15 | 0<Token≤256K | 2.936元 | 17.614元 | 17.614元 |
| 256K<Token≤1M | 3.67元 | 22.018元 | 22.018元 |
| qwen-plus | 0<Token≤256K | 2.936元 | 8.807元 | 29.357元 |
| 256K<Token≤1M | 8.807元 | 26.421元 | 88.071元 |
| qwen-plus-latest | 0<Token≤256K | 2.936元 | 8.807元 | 29.357元 |
| 256K<Token≤1M | 8.807元 | 26.421元 | 88.071元 |
| qwen-plus-2025-12-01 | 0<Token≤256K | 2.936元 | 8.807元 | 29.357元 |
| 256K<Token≤1M | 8.807元 | 26.421元 | 88.071元 |
| qwen-plus-2025-09-11 | 0<Token≤256K | 2.936元 | 8.807元 | 29.357元 |
| 256K<Token≤1M | 8.807元 | 26.421元 | 88.071元 |
| qwen-plus-2025-07-28 | 0<Token≤256K | 2.936元 | 8.807元 | 29.357元 |
| 256K<Token≤1M | 8.807元 | 26.421元 | 88.071元 |
| qwen-plus-2025-07-14 | 无阶梯计价 | 2.936元 | 8.807元 | 29.357元 |
| qwen-plus-2025-04-28 | 无阶梯计价 | 2.936元 | 8.807元 | 29.357元 |

##### **更多模型**

| **模型名称** | **单次请求的输入Token范围** | **输入单价 （每百万Token）** | **输出单价 （每百万Token）** |
| --- | --- | --- | --- |
| qwen-plus-2025-01-25 | 无阶梯计价 | 2.936元 | 8.807元 |

## 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

**说明**

美国部署模式的模型无免费额度。

| **模型名称** | **单次请求的输入Token范围** | **输入单价 （每百万Token）** | **输出单价 （每百万Token）** |   |
| --- | --- | --- | --- | --- |
| **非思考模式** | **思考模式（思维链+回答）** |
| qwen-plus-us > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 0<Token≤256K | 2.936元 | 8.807元 | 29.357元 |
| 256K<Token≤1M | 8.807元 | 26.421元 | 88.071元 |
| qwen-plus-2025-12-01-us | 0<Token≤256K | 2.936元 | 8.807元 | 29.357元 |
| 256K<Token≤1M | 8.807元 | 26.421元 | 88.071元 |

### **千问Flash**

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费；若模型支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)，仅输入Token享有折扣。两者不能同时生效。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **模式** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链+回答** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| qwen3.5-flash > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 非思考和思考模式 | 0<Token≤128K | 0.2元 | 2元  | 各100万Token 有效期：阿里云百炼开通后90天内 |
| 128K<Token≤256K | 0.8元 | 8元  |
| 256K<Token≤1M | 1.2元 | 12元 |
| qwen3.5-flash-2026-02-23 | 非思考和思考模式 | 0<Token≤128K | 0.2元 | 2元  |
| 128K<Token≤256K | 0.8元 | 8元  |
| 256K<Token≤1M | 1.2元 | 12元 |
| qwen-flash > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 非思考和思考模式 | 0<Token≤128K | 0.15元 | 1.5元 |
| 128K<Token≤256K | 0.6元 | 6元  |
| 256K<Token≤1M | 1.2元 | 12元 |
| qwen-flash-2025-07-28 | 非思考和思考模式 | 0<Token≤128K | 0.15元 | 1.5元 |
| 128K<Token≤256K | 0.6元 | 6元  |
| 256K<Token≤1M | 1.2元 | 12元 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

**说明**

全球部署模式的模型无免费额度。

| **模型名称** | **模式** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链+回答** |
| --- | --- | --- | --- | --- |
| qwen3.5-flash > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 非思考和思考模式 | 0<Token≤128K | 0.2元 | 2元  |
| 128K<Token≤256K | 0.8元 | 8元  |
| 256K<Token≤1M | 1.2元 | 12元 |
| qwen3.5-flash-2026-02-23 | 非思考和思考模式 | 0<Token≤128K | 0.2元 | 2元  |
| 128K<Token≤256K | 0.8元 | 8元  |
| 256K<Token≤1M | 1.2元 | 12元 |
| qwen-flash > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 非思考和思考模式 | 0<Token≤128K | 0.15元 | 1.5元 |
| 128K<Token≤256K | 0.6元 | 6元  |
| 256K<Token≤1M | 1.2元 | 12元 |
| qwen-flash-2025-07-28 | 非思考和思考模式 | 0<Token≤128K | 0.15元 | 1.5元 |
| 128K<Token≤256K | 0.6元 | 6元  |
| 256K<Token≤1M | 1.2元 | 12元 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **模式** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链+回答** |
| --- | --- | --- | --- | --- |
| qwen3.5-flash > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 非思考和思考模式 | 0<Token≤1M | 0.734元 | 2.936元 |
| qwen3.5-flash-2026-02-23 | 非思考和思考模式 | 0<Token≤1M | 0.734元 | 2.936元 |
| qwen-flash > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 非思考和思考模式 | 0<Token≤256K | 0.367元 | 2.936元 |
| 256K<Token≤1M | 1.835元 | 14.678元 |
| qwen-flash-2025-07-28 | 非思考和思考模式 | 0<Token≤256K | 0.367元 | 2.936元 |
| 256K<Token≤1M | 1.835元 | 14.678元 |

## 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

**说明**

美国部署模式的模型无免费额度。

| **模型名称** | **单次请求的输入Token范围** | **输入单价 （每百万Token）** | **输出单价 （每百万Token）** |
| --- | --- | --- | --- |
| qwen-flash-us > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 0<Token≤256K | 0.367元 | 2.936元 |
| 256K<Token≤1M | 1.835元 | 14.678元 |
| qwen-flash-2025-07-28-us | 0<Token≤256K | 0.367元 | 2.936元 |
| 256K<Token≤1M | 1.835元 | 14.678元 |

### **千问Turbo**

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **模式** | **输入单价（每百万Token）** | **输出单价（每百万Token）** |   | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **非思考模式** | **思考模式（思维链+回答）** |
| qwen-turbo > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 非思考和思考模式 | 0.3元 | 0.6元 | 3元  | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen-turbo-latest > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 非思考和思考模式 | 0.3元 | 0.6元 | 3元  |
| qwen-turbo-2025-07-15 | 非思考和思考模式 | 0.3元 | 0.6元 | 3元  |
| qwen-turbo-2025-04-28 | 非思考和思考模式 | 0.3元 | 0.6元 | 3元  |

##### **更多模型**

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：百炼开通后90天内 |
| --- | --- | --- | --- |
| qwen-turbo-2025-02-11 | 0.3元 | 0.6元 | 100万Token |
| qwen-turbo-2024-11-01 | 0.3元 | 0.6元 | 1000万Token |

## **国际**

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **模式** | **输入单价 （每百万Token）** | **输出单价 （每百万Token）** |   |
| --- | --- | --- | --- | --- |
| **非思考模式** | **思考模式（思维链+回答）** |
| qwen-turbo > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 非思考和思考 | 0.367元 | 1.468元 | 3.67元 |
| qwen-turbo-latest | 非思考和思考 | 0.367元 | 1.468元 | 3.67元 |
| qwen-turbo-2025-04-28 | 非思考和思考 | 0.367元 | 1.468元 | 3.67元 |

##### 更多模型

| **模型名称** | **输入单价 （每百万Token）** | **输出单价 （每百万Token）** |
| --- | --- | --- |
| qwen-turbo-2024-11-01 | 0.367元 | 1.468元 |

### **QwQ**

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **模式** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| qwq-plus > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 仅思考模式 | 1.6元 | 4元  | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwq-plus-latest | 仅思考模式 | 1.6元 | 4元  |
| qwq-plus-2025-03-05 | 仅思考模式 | 1.6元 | 4元  |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **模式** | **输入单价 （每百万Token）** | **输出单价 （每百万Token）** |
| --- | --- | --- | --- |
| qwq-plus | 仅思考模式 | 5.871元 | 17.614元 |

### 千问Long

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen-long > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 0.5元 | 2元  | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen-long-latest | 0.5元 | 2元  |
| qwen-long-2025-01-25 | 0.5元 | 2元  |

### **千问Omni**

计费规则：按输入Token和输出Token计费。不同模态的Token计算规则请参见[计费与限流](https://help.aliyun.com/zh/model-studio/qwen-omni#12db7427b94qt)。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

## Qwen3.5-Omni

| **模型名称** | **单次请求的输入Token数** | **输入单价（每百万Token）** |   | **输出单价（每百万Token）** |   | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **文本/图片/视频** | **音频** | **文本** > 多模态输入 | **文本+音频** > 仅音频计费 |
| **qwen3.5-omni-plus** | 0<Token≤128K | 0.8元 | 4.96元 | 9.6元 | 61.322元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| 128K<Token≤256K | 2元  | 24元 |
| qwen3.5-omni-plus-2026-03-15 | 0<Token≤128K | 0.8元 | 4.96元 | 9.6元 | 61.322元 |
| 128K<Token≤256K | 2元  | 24元 |
| **qwen3.5-omni-flash** | 0<Token≤128K | 0.2元 | 1.24元 | 4元  | 25.551元 |
| 128K<Token≤256K | 0.8元 | 16元 |
| qwen3.5-omni-flash-2026-03-15 | 0<Token≤128K | 0.2元 | 1.24元 | 4元  | 25.551元 |
| 128K<Token≤256K | 0.8元 | 16元 |

## Qwen3-Omni-Flash

| **模型名称** | **模式** | **输入单价（每百万Token）** |   |   | **输出单价（每百万Token）** |   |   | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **文本** | **音频** | **图片/视频** | **文本** > 仅纯文本输入 | **文本** > 多模态输入 | **文本+音频** > 仅音频计费 |
| qwen3-omni-flash | 非思考和思考模式 | 1.8元 | 15.8元 | 3.3元 | 6.9元 | 12.7元 | 62.6元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen3-omni-flash-2025-12-01 | 非思考和思考模式 | 1.8元 | 15.8元 | 3.3元 | 6.9元 | 12.7元 | 62.6元 |
| qwen3-omni-flash-2025-09-15 | 非思考和思考模式 | 1.8元 | 15.8元 | 3.3元 | 6.9元 | 12.7元 | 62.6元 |

##### 更多模型

| **模型名称** | **输入单价（每百万Token）** |   |   | **输出单价（每百万Token）** |   |   | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **文本** | **音频** | **图片/视频** | **文本** > 仅纯文本输入 | **文本** > 多模态输入 | **文本+音频** > 仅音频计费 |
| qwen-omni-turbo | 0.4元 | 25元 | 1.5元 | 1.6元 | 4.5元 | 50元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen-omni-turbo-latest | 0.4元 | 25元 | 1.5元 | 1.6元 | 4.5元 | 50元 |
| qwen-omni-turbo-2025-03-26 | 0.4元 | 25元 | 1.5元 | 1.6元 | 4.5元 | 50元 |
| qwen-omni-turbo-2025-01-19 | 0.4元 | 25元 | 1.5元 | 1.6元 | 4.5元 | 50元 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

## Qwen3.5-Omni

| **模型名称** | **输入单价（每百万Token）** |   | **输出单价（每百万Token）** |   |
| --- | --- | --- | --- | --- |
| **文本/图片/视频** | **音频** | **文本** > 多模态输入 | **文本+音频** > 仅音频计费 |
| **qwen3.5-omni-plus** | 2.998元 | 18.878元 | 35.972元 | 230.313元 |
| qwen3.5-omni-plus-2026-03-15 | 2.998元 | 18.878元 | 35.972元 | 230.313元 |
| **qwen3.5-omni-flash** | 0.749元 | 4.719元 | 5.995元 | 38.386元 |
| qwen3.5-omni-flash-2026-03-15 | 0.749元 | 4.719元 | 5.995元 | 38.386元 |

## Qwen3-Omni-Flash

| **模型名称** | **模式** | **输入单价（每百万Token）** |   |   | **输出单价（每百万Token）** |   |   |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **文本** | **音频** | **图片/视频** | **文本** > 仅纯文本输入 | **文本** > 多模态输入 | **文本+音频** > 仅音频计费 |
| qwen3-omni-flash | 非思考和思考模式 | 3.156元 | 27.962元 | 5.725元 | 12.183元 | 22.458元 | 110.896元 |
| qwen3-omni-flash-2025-12-01 | 非思考和思考模式 | 3.156元 | 27.962元 | 5.725元 | 12.183元 | 22.458元 | 110.896元 |
| qwen3-omni-flash-2025-09-15 | 非思考和思考模式 | 3.156元 | 27.962元 | 5.725元 | 12.183元 | 22.458元 | 110.896元 |

##### 更多模型

| **模型名称** | **输入单价（每百万Token）** |   |   | **输出单价（每百万Token）** |   |   | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **文本** | **音频** | **图片/视频** | **文本** > 仅纯文本输入 | **文本** > 多模态输入 | **文本+音频** > 仅音频计费 |
| qwen-omni-turbo | 0.514元 | 32.586元 | 1.541元 | 1.982元 | 4.624元 | 65.246元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen-omni-turbo-latest | 0.514元 | 32.586元 | 1.541元 | 1.982元 | 4.624元 | 65.246元 |
| qwen-omni-turbo-2025-03-26 | 0.514元 | 32.586元 | 1.541元 | 1.982元 | 4.624元 | 65.246元 |

### **千问Omni-Realtime**

计费规则：按输入Token和输出Token计费。不同模态的Token计算规则请参见[计费与限流](https://help.aliyun.com/zh/model-studio/realtime#dc0370c95d3ja)。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

## Qwen3.5-Omni-Realtime

| **模型名称** | **单次会话的输入Token数** | **输入单价（每百万Token）** |   | **输出单价（每百万Token）** |   | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **文本/图片** | **音频** | **文本** > 多模态输入 | **文本+音频** > 仅音频计费 |
| qwen3.5-omni-plus-realtime | 0<Token≤128K | 0.96元 | 5.95元 | 11.52元 | 73.587元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| \\>128K | 2.4元 | 28.8元 |
| qwen3.5-omni-plus-realtime-2026-03-15 | 0<Token≤128K | 0.96元 | 5.95元 | 11.52元 | 73.587元 |
| \\>128K | 2.4元 | 28.8元 |
| qwen3.5-omni-flash-realtime | 0<Token≤128K | 0.24元 | 1.49元 | 4.8元 | 30.661元 |
| \\>128K | 0.96元 | 19.2元 |
| qwen3.5-omni-flash-realtime-2026-03-15 | 0<Token≤128K | 0.24元 | 1.49元 | 4.8元 | 30.661元 |
| \\>128K | 0.96元 | 19.2元 |

## Qwen3-Omni-Flash-Realtime

| **模型名称** | **模式** | **输入单价（每百万Token）** |   |   | **输出单价（每百万Token）** |   |   | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **文本** | **音频** | **图片** | **文本** > 仅纯文本输入 | **文本** > 多模态输入 | **文本+音频** > 仅音频计费 |
| qwen3-omni-flash-realtime | 非思考和思考模式 | 2.2元 | 18.9元 | 3.9元 | 8.3元 | 15.2元 | 75.1元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen3-omni-flash-realtime-2025-12-01 | 非思考和思考模式 | 2.2元 | 18.9元 | 3.9元 | 8.3元 | 15.2元 | 75.1元 |
| qwen3-omni-flash-realtime-2025-09-15 | 非思考和思考模式 | 2.2元 | 18.9元 | 3.9元 | 8.3元 | 15.2元 | 75.1元 |

##### 更多模型

| **模型名称** | **输入单价（每百万Token）** |   |   | **输出单价（每百万Token）** |   |   | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **文本** | **音频** | **图片** | **文本** > 仅纯文本输入 | **文本** > 多模态输入 | **文本+音频** > 仅音频计费 |
| qwen-omni-turbo-realtime | 1.6元 | 25元 | 6元  | 6.4元 | 18元 | 50元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen-omni-turbo-realtime-latest | 1.6元 | 25元 | 6元  | 6.4元 | 18元 | 50元 |
| qwen-omni-turbo-realtime-2025-05-08 | 1.6元 | 25元 | 6元  | 6.4元 | 18元 | 50元 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

## Qwen3.5-Omni-Realtime

| **模型名称** | **输入单价（每百万Token）** |   | **输出单价（每百万Token）** |   | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **文本/图片** | **音频** | **文本** > 多模态输入 | **文本+音频** > 仅音频计费 |
| **qwen3.5-omni-plus-realtime** | 3.597元 | 22.654元 | 43.167元 | 276.376元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen3.5-omni-plus-realtime-2026-03-15 | 3.597元 | 22.654元 | 43.167元 | 276.376元 |
| qwen3.5-omni-flash-realtime | 0.899元 | 5.663元 | 7.194元 | 46.063元 |
| qwen3.5-omni-flash-realtime-2026-03-15 | 0.899元 | 5.663元 | 7.194元 | 46.063元 |

## Qwen3-Omni-Flash-Realtime

| **模型名称** | **模式** | **输入单价（每百万Token）** |   |   | **输出单价（每百万Token）** |   |   | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **文本** | **音频** | **图片** | **文本** > 仅纯文本输入 | **文本** > 多模态输入 | **文本+音频** > 仅音频计费 |
| qwen3-omni-flash-realtime | 非思考和思考模式 | 3.816元 | 33.54元 | 6.899元 | 14.605元 | 26.935元 | 133.06元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen3-omni-flash-realtime-2025-12-01 | 非思考和思考模式 | 3.816元 | 33.54元 | 6.899元 | 14.605元 | 26.935元 | 133.06元 |
| qwen3-omni-flash-realtime-2025-09-15 | 非思考和思考模式 | 3.816元 | 33.54元 | 6.899元 | 14.605元 | 26.935元 | 133.06元 |

##### 更多模型

| **模型名称** | **输入单价（每百万Token）** |   |   | **输出单价（每百万Token）** |   |   | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **文本** | **音频** | **图片/视频** | **文本** > 仅纯文本输入 | **文本** > 多模态输入 | **文本+音频** > 仅音频计费 |
| qwen-omni-turbo-realtime | 1.982元 | 32.586元 | 6.165元 | 7.853元 | 18.495元 | 65.246元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen-omni-turbo-realtime-latest | 1.982元 | 32.586元 | 6.165元 | 7.853元 | 18.495元 | 65.246元 |
| qwen-omni-turbo-realtime-2025-05-08 | 1.982元 | 32.586元 | 6.165元 | 7.853元 | 18.495元 | 65.246元 |

### **QVQ**

计费规则：按输入Token和输出Token计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qvq-max | 8元  | 32元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qvq-max-latest | 8元  | 32元 |
| qvq-max-2025-05-15 | 8元  | 32元 |
| qvq-max-2025-03-25 | 8元  | 32元 |
| qvq-plus | 2元  | 5元  |
| qvq-plus-latest | 2元  | 5元  |
| qvq-plus-2025-05-15 | 2元  | 5元  |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输入单价 （每百万Token）** | **输出单价 （每百万Token）** |
| --- | --- | --- |
| qvq-max | 8.807元 | 35.228元 |
| qvq-max-latest | 8.807元 | 35.228元 |
| qvq-max-2025-03-25 | 8.807元 | 35.228元 |

### 千问VL

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **模式** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链+回答** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| qwen3-vl-plus > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 非思考和思考模式 | 0<Token≤32K | 1元  | 10元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| 32K<Token≤128K | 1.5元 | 15元 |
| 128K<Token≤256K | 3元  | 30元 |
| qwen3-vl-plus-2025-12-19 | 非思考和思考模式 | 0<Token≤32K | 1元  | 10元 |
| 32K<Token≤128K | 1.5元 | 15元 |
| 128K<Token≤256K | 3元  | 30元 |
| qwen3-vl-plus-2025-09-23 | 非思考和思考模式 | 0<Token≤32K | 1元  | 10元 |
| 32K<Token≤128K | 1.5元 | 15元 |
| 128K<Token≤256K | 3元  | 30元 |
| qwen3-vl-flash > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 非思考和思考模式 | 0<Token≤32K | 0.15元 | 1.5元 |
| 32K<Token≤128K | 0.3元 | 3元  |
| 128K<Token≤256K | 0.6元 | 6元  |
| qwen3-vl-flash-2026-01-22 | 非思考和思考模式 | 0<Token≤32K | 0.15元 | 1.5元 |
| 32K<Token≤128K | 0.3元 | 3元  |
| 128K<Token≤256K | 0.6元 | 6元  |
| qwen3-vl-flash-2025-10-15 | 非思考和思考模式 | 0<Token≤32K | 0.15元 | 1.5元 |
| 32K<Token≤128K | 0.3元 | 3元  |
| 128K<Token≤256K | 0.6元 | 6元  |

##### **更多模型**

| **模型名称** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| qwen-vl-max > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 无阶梯计价 | 1.6元 | 4元  | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen-vl-max-latest > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 无阶梯计价 | 1.6元 | 4元  |
| qwen-vl-max-2025-08-13 | 无阶梯计价 | 1.6元 | 4元  |
| qwen-vl-max-2025-04-08 | 无阶梯计价 | 3元  | 9元  |
| qwen-vl-max-2025-04-02 | 无阶梯计价 | 3元  | 9元  |
| qwen-vl-max-2025-01-25 | 无阶梯计价 | 3元  | 9元  |
| qwen-vl-max-2024-12-30 | 无阶梯计价 | 3元  | 9元  |
| qwen-vl-max-2024-11-19 | 无阶梯计价 | 3元  | 9元  |
| qwen-vl-plus > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 无阶梯计价 | 0.8元 | 2元  |
| qwen-vl-plus-latest > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 无阶梯计价 | 0.8元 | 2元  |
| qwen-vl-plus-2025-08-15 | 无阶梯计价 | 0.8元 | 2元  |
| qwen-vl-plus-2025-07-10 | 无阶梯计价 | 0.15元 | 1.5元 |
| qwen-vl-plus-2025-05-07 | 无阶梯计价 | 1.5元 | 4.5元 |
| qwen-vl-plus-2025-01-25 | 无阶梯计价 | 1.5元 | 4.5元 |
| qwen-vl-plus-2025-01-02 | 无阶梯计价 | 1.5元 | 4.5元 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

**说明**

全球部署模式的模型无免费额度。

| **模型名称** | **模式** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链+回答** |
| --- | --- | --- | --- | --- |
| qwen3-vl-plus > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 非思考和思考模式 | 0<Token≤32K | 1元  | 10元 |
| 32K<Token≤128K | 1.5元 | 15元 |
| 128K<Token≤256K | 3元  | 30元 |
| qwen3-vl-plus-2025-09-23 | 非思考和思考模式 | 0<Token≤32K | 1元  | 10元 |
| 32K<Token≤128K | 1.5元 | 15元 |
| 128K<Token≤256K | 3元  | 30元 |
| qwen3-vl-flash > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 非思考和思考模式 | 0<Token≤32K | 0.15元 | 1.5元 |
| 32K<Token≤128K | 0.3元 | 3元  |
| 128K<Token≤256K | 0.6元 | 6元  |
| qwen3-vl-flash-2025-10-15 | 非思考和思考模式 | 0<Token≤32K | 0.15元 | 1.5元 |
| 32K<Token≤128K | 0.3元 | 3元  |
| 128K<Token≤256K | 0.6元 | 6元  |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **模式** | **单次请求的输入Token数** | **输入单价 （每百万Token）** | **输出单价 （每百万Token）** |
| --- | --- | --- | --- | --- |
| qwen3-vl-plus > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 非思考和思考模式 | 0<Token≤32K | 1.468元 | 11.743元 |
| 32K<Token≤128K | 2.202元 | 17.614元 |
| 128K<Token≤256K | 4.404元 | 35.228元 |
| qwen3-vl-plus-2025-12-19 | 非思考和思考模式 | 0<Token≤32K | 1.468元 | 11.743元 |
| 32K<Token≤128K | 2.202元 | 17.614元 |
| 128K<Token≤256K | 4.404元 | 35.228元 |
| qwen3-vl-plus-2025-09-23 | 非思考和思考模式 | 0<Token≤32K | 1.468元 | 11.743元 |
| 32K<Token≤128K | 2.202元 | 17.614元 |
| 128K<Token≤256K | 4.404元 | 35.228元 |
| qwen3-vl-flash > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 非思考和思考模式 | 0<Token≤32K | 0.367元 | 2.936元 |
| 32K<Token≤128K | 0.55元 | 4.404元 |
| 128K<Token≤256K | 0.881元 | 7.046元 |
| qwen3-vl-flash-2026-01-22 | 非思考和思考模式 | 0<Token≤32K | 0.367元 | 2.936元 |
| 32K<Token≤128K | 0.55元 | 4.404元 |
| 128K<Token≤256K | 0.881元 | 7.046元 |
| qwen3-vl-flash-2025-10-15 | 非思考和思考模式 | 0<Token≤32K | 0.367元 | 2.936元 |
| 32K<Token≤128K | 0.55元 | 4.404元 |
| 128K<Token≤256K | 0.881元 | 7.046元 |

##### **更多模型**

| **模型名称** | **单次请求的输入Token数** | **输入单价 （每百万Token）** | **输出单价 （每百万Token）** |
| --- | --- | --- | --- |
| qwen-vl-max > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 无阶梯计价 | 5.871元 | 23.486元 |
| qwen-vl-max-latest | 无阶梯计价 | 5.871元 | 23.486元 |
| qwen-vl-max-2025-08-13 | 无阶梯计价 | 5.871元 | 23.486元 |
| qwen-vl-max-2025-04-08 | 无阶梯计价 | 5.871元 | 23.486元 |
| qwen-vl-plus > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 无阶梯计价 | 1.541元 | 4.624元 |
| qwen-vl-plus-latest | 无阶梯计价 | 1.541元 | 4.624元 |
| qwen-vl-plus-2025-08-15 | 无阶梯计价 | 1.541元 | 4.624元 |
| qwen-vl-plus-2025-05-07 | 无阶梯计价 | 1.541元 | 4.624元 |
| qwen-vl-plus-2025-01-25 | 无阶梯计价 | 1.541元 | 4.624元 |

## 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

**说明**

美国部署模式的模型无免费额度。

| **模型名称** | **模式** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链+回答** |
| --- | --- | --- | --- | --- |
| qwen3-vl-flash-us > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 非思考和思考模式 | 0<Token≤32K | 0.367元 | 2.936元 |
| 32K<Token≤128K | 0.55元 | 4.404元 |
| 128K<Token≤256K | 0.881元 | 7.046元 |
| qwen3-vl-flash-2025-10-15-us | 非思考和思考模式 | 0<Token≤32K | 0.367元 | 2.936元 |
| 32K<Token≤128K | 0.55元 | 4.404元 |
| 128K<Token≤256K | 0.881元 | 7.046元 |

### 千问OCR

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen-vl-ocr > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 0.3元 | 0.5元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen-vl-ocr-latest > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 0.3元 | 0.5元 |
| qwen-vl-ocr-2025-11-20 | 0.3元 | 0.5元 |
| qwen-vl-ocr-2025-08-28 | 5元  | 5元  |
| qwen-vl-ocr-2025-04-13 | 5元  | 5元  |
| qwen-vl-ocr-2024-10-28 | 5元  | 5元  |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

**说明**

全球部署模式的模型无免费额度。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** |
| --- | --- | --- |
| qwen-vl-ocr | 0.3元 | 0.5元 |
| qwen-vl-ocr-2025-11-20 | 0.3元 | 0.5元 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** |
| --- | --- | --- |
| qwen-vl-ocr | 0.514元 | 1.174元 |
| qwen-vl-ocr-2025-11-20 | 0.514元 | 1.174元 |

### 千问Audio

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

计费规则：按输入和输出的总Token数进行计费。

音频Token计算规则：每一秒钟的音频对应25个Token。若音频时长不足1秒，则按25个Token计算。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen-audio-turbo | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐使用[全模态（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni)作为替代模型 |   | 各10万Token 有效期：阿里云百炼开通后90天内 |
| qwen-audio-turbo-latest |

### 千问数学模型

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen-math-plus | 4元  | 12元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen-math-turbo | 2元  | 6元  |

### 千问Coder

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)，仅输入Token享有折扣。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| qwen3-coder-plus > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 0<Token≤32K | 4元  | 16元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| 32K<Token≤128K | 6元  | 24元 |
| 128K<Token≤256K | 10元 | 40元 |
| 256K<Token≤1M | 20元 | 200元 |
| qwen3-coder-plus-2025-09-23 | 0<Token≤32K | 4元  | 16元 |
| 32K<Token≤128K | 6元  | 24元 |
| 128K<Token≤256K | 10元 | 40元 |
| 256K<Token≤1M | 20元 | 200元 |
| qwen3-coder-plus-2025-07-22 | 0<Token≤32K | 4元  | 16元 |
| 32K<Token≤128K | 6元  | 24元 |
| 128K<Token≤256K | 10元 | 40元 |
| 256K<Token≤1M | 20元 | 200元 |
| qwen3-coder-flash | 0<Token≤32K | 1元  | 4元  |
| 32K<Token≤128K | 1.5元 | 6元  |
| 128K<Token≤256K | 2.5元 | 10元 |
| 256K<Token≤1M | 5元  | 25元 |
| qwen3-coder-flash-2025-07-28 | 0<Token≤32K | 1元  | 4元  |
| 32K<Token≤128K | 1.5元 | 6元  |
| 128K<Token≤256K | 2.5元 | 10元 |
| 256K<Token≤1M | 5元  | 25元 |

##### **更多模型**

| **模型名称** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| qwen-coder-plus | 无阶梯计价 | 3.5元 | 7元  | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen-coder-plus-latest | 无阶梯计价 | 3.5元 | 7元  |
| qwen-coder-plus-2024-11-06 | 无阶梯计价 | 3.5元 | 7元  |
| qwen-coder-turbo | 无阶梯计价 | 2元  | 6元  |
| qwen-coder-turbo-latest | 无阶梯计价 | 2元  | 6元  |
| qwen-coder-turbo-2024-09-19 | 无阶梯计价 | 2元  | 6元  |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

**说明**

全球部署模式的模型无免费额度。

| **模型名称** | **单次请求的输入Token数** | **输入单价 （每百万Token）** | **输出单价 （每百万Token）** |
| --- | --- | --- | --- |
| qwen3-coder-plus | 0<Token≤32K | 4元  | 16元 |
| 32K<Token≤128K | 6元  | 24元 |
| 128K<Token≤256K | 10元 | 40元 |
| 256K<Token≤1M | 20元 | 200元 |
| qwen3-coder-plus-2025-09-23 | 0<Token≤32K | 4元  | 16元 |
| 32K<Token≤128K | 6元  | 24元 |
| 128K<Token≤256K | 10元 | 40元 |
| 256K<Token≤1M | 20元 | 200元 |
| qwen3-coder-plus-2025-07-22 | 0<Token≤32K | 4元  | 16元 |
| 32K<Token≤128K | 6元  | 24元 |
| 128K<Token≤256K | 10元 | 40元 |
| 256K<Token≤1M | 20元 | 200元 |
| qwen3-coder-flash | 0<Token≤32K | 1元  | 4元  |
| 32K<Token≤128K | 1.5元 | 6元  |
| 128K<Token≤256K | 2.5元 | 10元 |
| 256K<Token≤1M | 5元  | 25元 |
| qwen3-coder-flash-2025-07-28 | 0<Token≤32K | 1元  | 4元  |
| 32K<Token≤128K | 1.5元 | 6元  |
| 128K<Token≤256K | 2.5元 | 10元 |
| 256K<Token≤1M | 5元  | 25元 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际（新加坡）模型无免费额度。

| **模型名称** | **单次请求的输入Token数** | **输入单价 （每百万Token）** | **输出单价 （每百万Token）** |
| --- | --- | --- | --- |
| qwen3-coder-plus | 0<Token≤32K | 7.339元 | 36.696元 |
| 32K<Token≤128K | 13.211元 | 66.053元 |
| 128K<Token≤256K | 22.018元 | 110.089元 |
| 256K<Token≤1M | 44.035元 | 440.354元 |
| qwen3-coder-plus-2025-09-23 | 0<Token≤32K | 7.339元 | 36.696元 |
| 32K<Token≤128K | 13.211元 | 66.053元 |
| 128K<Token≤256K | 22.018元 | 110.089元 |
| 256K<Token≤1M | 44.035元 | 440.354元 |
| qwen3-coder-plus-2025-07-22 | 0<Token≤32K | 7.339元 | 36.696元 |
| 32K<Token≤128K | 13.211元 | 66.053元 |
| 128K<Token≤256K | 22.018元 | 110.089元 |
| 256K<Token≤1M | 44.035元 | 440.354元 |
| qwen3-coder-flash | 0<Token≤32K | 2.202元 | 11.009元 |
| 32K<Token≤128K | 3.67元 | 18.348元 |
| 128K<Token≤256K | 5.871元 | 29.357元 |
| 256K<Token≤1M | 11.743元 | 70.457元 |
| qwen3-coder-flash-2025-07-28 | 0<Token≤32K | 2.202元 | 11.009元 |
| 32K<Token≤128K | 3.67元 | 18.348元 |
| 128K<Token≤256K | 5.871元 | 29.357元 |
| 256K<Token≤1M | 11.743元 | 70.457元 |

### **千问翻译模型**

计费规则：按输入Token和输出Token计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen-mt-plus | 1.8元 | 5.4元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen-mt-flash | 0.7元 | 1.95元 |
| qwen-mt-lite | 0.6元 | 1.6元 |
| qwen-mt-turbo | 0.7元 | 1.95元 |

## **全球**

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

**说明**

全球部署模式的模型无免费额度。

| **模型名称** | **输入单价 （每百万Token）** | **输出单价 （每百万Token）** |
| --- | --- | --- |
| qwen-mt-plus | 1.8元 | 5.4元 |
| qwen-mt-flash | 0.7元 | 1.95元 |
| qwen-mt-lite | 0.6元 | 1.6元 |

## **国际**

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际（新加坡）模型无免费额度。

| **模型名称** | **输入单价 （每百万Token）** | **输出单价 （每百万Token）** |
| --- | --- | --- |
| qwen-mt-plus | 18.055元 | 54.09元 |
| qwen-mt-flash | 1.174元 | 3.596元 |
| qwen-mt-lite | 0.881元 | 2.642元 |
| qwen-mt-turbo | 1.174元 | 3.596元 |

### 千问数据挖掘模型

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen-doc-turbo | 0.6元 | 1元  | 无免费额度 |

### **千问深入研究模型**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen-deep-research | 54元 | 163元 | 无免费额度 |

### **通义晓蜜对话分析模型**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| tongyi-xiaomi-analysis-flash | 0.2元 | 0.4元 | 各100万Token 有效期：百炼开通后90天内 |
| tongyi-xiaomi-analysis-pro | 1.0元 | 2.7元 |

## **文本生成-千问-开源版**

### **Qwen3.5**

计费规则：按输入Token和输出Token计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单次请求的输入Token范围** | **输入单价（每百万Token）** | **输出单价（每百万Token）** |   | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **非思考模式** | **思考模式（思维链+回答）** |
| qwen3.5-397b-a17b | 0<Token≤128K | 1.2元 | 7.2元 | 7.2元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| 128K<Token≤256K | 3元  | 18元 | 18元 |
| qwen3.5-122b-a10b | 0<Token≤128K | 0.8元 | 6.4元 | 6.4元 |
| 128K<Token≤256K | 2元  | 16元 | 16元 |
| qwen3.5-27b | 0<Token≤128K | 0.6元 | 4.8元 | 4.8元 |
| 128K<Token≤256K | 1.8元 | 14.4元 | 14.4元 |
| qwen3.5-35b-a3b | 0<Token≤128K | 0.4元 | 3.2元 | 3.2元 |
| 128K<Token≤256K | 1.6元 | 12.8元 | 12.8元 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **单次请求的输入Token范围** | **输入单价（每百万Token）** | **输出单价（每百万Token）** |   |
| --- | --- | --- | --- | --- |
| **非思考模式** | **思考模式（思维链+回答）** |
| qwen3.5-397b-a17b | 0<Token≤128K | 1.2元 | 7.2元 | 7.2元 |
| 128K<Token≤256K | 3元  | 18元 | 18元 |
| qwen3.5-122b-a10b | 0<Token≤128K | 0.8元 | 6.4元 | 6.4元 |
| 128K<Token≤256K | 2元  | 16元 | 16元 |
| qwen3.5-27b | 0<Token≤128K | 0.6元 | 4.8元 | 4.8元 |
| 128K<Token≤256K | 1.8元 | 14.4元 | 14.4元 |
| qwen3.5-35b-a3b | 0<Token≤128K | 0.4元 | 3.2元 | 3.2元 |
| 128K<Token≤256K | 1.6元 | 12.8元 | 12.8元 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **单次请求的输入Token范围** | **输入单价（每百万Token）** | **输出单价（每百万Token）** |   |
| --- | --- | --- | --- | --- |
| **非思考模式** | **思考模式（思维链+回答）** |
| qwen3.5-397b-a17b | 0<Token≤256K | 4.404元 | 26.421元 | 26.421元 |
| qwen3.5-122b-a10b | 0<Token≤256K | 2.936元 | 23.486元 | 23.486元 |
| qwen3.5-27b | 0<Token≤256K | 2.202元 | 17.614元 | 17.614元 |
| qwen3.5-35b-a3b | 0<Token≤256K | 1.835元 | 14.678元 | 14.678元 |

### **Qwen3**

计费规则：按输入Token和输出Token计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **模式** | **输入单价（每百万Token）** | **输出单价（每百万Token）** |   | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **非思考模式** | **思考模式（思维链+回答）** |
| qwen3-next-80b-a3b-thinking | 仅思考模式 | 1元  | \\- | 10元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen3-next-80b-a3b-instruct | 仅非思考模式 | 1元  | 4元  | \\- |
| qwen3-235b-a22b-thinking-2507 | 仅思考模式 | 2元  | \\- | 20元 |
| qwen3-235b-a22b-instruct-2507 | 仅非思考模式 | 2元  | 8元  | \\- |
| qwen3-30b-a3b-thinking-2507 | 仅思考模式 | 0.75元 | \\- | 7.5元 |
| qwen3-30b-a3b-instruct-2507 | 仅非思考模式 | 0.75元 | 3元  | \\- |
| qwen3-235b-a22b | 非思考和思考模式 | 2元  | 8元  | 20元 |
| qwen3-32b | 非思考和思考模式 | 2元  | 8元  | 20元 |
| qwen3-30b-a3b | 非思考和思考模式 | 0.75元 | 3元  | 7.5元 |
| qwen3-14b | 非思考和思考模式 | 1元  | 4元  | 10元 |
| qwen3-8b | 非思考和思考模式 | 0.5元 | 2元  | 5元  |
| qwen3-4b | 非思考和思考模式 | 0.3元 | 1.2元 | 3元  |
| qwen3-1.7b | 非思考和思考模式 | 0.3元 | 1.2元 | 3元  |
| qwen3-0.6b | 非思考和思考模式 | 0.3元 | 1.2元 | 3元  |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

| **模型名称** | **模式** | **输入单价（每百万Token）** | **输出单价（每百万Token）** |   | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **非思考模式** | **思考模式（思维链+回答）** |
| qwen3-next-80b-a3b-thinking | 仅思考模式 | 1元  | \\- | 10元 | 无免费额度 |
| qwen3-next-80b-a3b-instruct | 仅非思考模式 | 1元  | 4元  | \\- |
| qwen3-235b-a22b-thinking-2507 | 仅思考模式 | 1.688元 | \\- | 16.88元 |
| qwen3-235b-a22b-instruct-2507 | 仅非思考模式 | 1.688元 | 6.752元 | \\- |
| qwen3-30b-a3b-thinking-2507 | 仅思考模式 | 0.75元 | \\- | 7.5元 |
| qwen3-30b-a3b-instruct-2507 | 仅非思考模式 | 0.75元 | 3元  | \\- |
| qwen3-235b-a22b | 非思考和思考模式 | 2元  | 8元  | 20元 |
| qwen3-32b | 非思考和思考模式 | 1.174元 | 4.697元 | 4.697元 |
| qwen3-30b-a3b | 非思考和思考模式 | 0.75元 | 3元  | 7.5元 |
| qwen3-14b | 非思考和思考模式 | 1元  | 4元  | 10元 |
| qwen3-8b | 非思考和思考模式 | 0.5元 | 2元  | 5元  |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **模式** | **输入单价（每百万Token）** | **输出单价（每百万Token）** |   | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **非思考模式** | **思考模式（思维链+回答）** |
| qwen3-next-80b-a3b-thinking | 仅思考模式 | 1.101元 | \\- | 8.807元 | 无免费额度 |
| qwen3-next-80b-a3b-instruct | 仅非思考模式 | 1.101元 | 8.807元 | \\- |
| qwen3-235b-a22b-thinking-2507 | 仅思考模式 | 1.688元 | \\- | 16.88元 |
| qwen3-235b-a22b-instruct-2507 | 仅非思考模式 | 1.688元 | 6.752元 | \\- |
| qwen3-30b-a3b-thinking-2507 | 仅思考模式 | 1.468元 | \\- | 17.614元 |
| qwen3-30b-a3b-instruct-2507 | 仅非思考模式 | 1.468元 | 5.871元 | \\- |
| qwen3-235b-a22b | 非思考和思考模式 | 5.137元 | 20.55元 | 61.65元 |
| qwen3-32b | 非思考和思考模式 | 1.174元 | 4.697元 | 4.697元 |
| qwen3-30b-a3b | 非思考和思考模式 | 1.468元 | 5.871元 | 17.614元 |
| qwen3-14b | 非思考和思考模式 | 2.569元 | 10.275元 | 30.825元 |
| qwen3-8b | 非思考和思考模式 | 1.321元 | 5.137元 | 15.412元 |
| qwen3-4b | 非思考和思考模式 | 0.807元 | 3.082元 | 9.247元 |
| qwen3-1.7b | 非思考和思考模式 | 0.807元 | 3.082元 | 9.247元 |
| qwen3-0.6b | 非思考和思考模式 | 0.807元 | 3.082元 | 9.247元 |

### **QwQ-开源版**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwq-32b | 2元  | 6元  | 100万Token 有效期：阿里云百炼开通后90天内 |

### **QwQ-Preview**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwq-32b-preview > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 2元  | 6元  | 各100万Token 有效期：阿里云百炼开通后90天内 |

### **Qwen2.5**

计费规则：按输入Token和输出Token计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen2.5-14b-instruct-1m | 1元  | 3元  | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen2.5-7b-instruct-1m | 0.5元 | 1元  |
| qwen2.5-72b-instruct | 4元  | 12元 |
| qwen2.5-32b-instruct | 2元  | 6元  |
| qwen2.5-14b-instruct | 1元  | 3元  |
| qwen2.5-7b-instruct | 0.5元 | 1元  |
| qwen2.5-3b-instruct | 0.3元 | 0.9元 |
| qwen2.5-1.5b-instruct | 目前仅供免费体验 > 免费额度用完后不可调用，推荐使用[Qwen3](https://help.aliyun.com/zh/model-studio/deep-thinking)、[DeepSeek-阿里云](https://help.aliyun.com/zh/model-studio/deepseek-api)、[Kimi-阿里云](https://help.aliyun.com/zh/model-studio/kimi-api)作为替代模型 |   |
| qwen2.5-0.5b-instruct |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际（新加坡）模型无免费额度。

| **模型名称** | **输入单价 （每百万Token）** | **输出单价 （每百万Token）** |
| --- | --- | --- |
| qwen2.5-14b-instruct-1m | 5.908元 | 23.632元 |
| qwen2.5-7b-instruct-1m | 2.701元 | 10.789元 |
| qwen2.5-72b-instruct | 10.275元 | 41.1元 |
| qwen2.5-32b-instruct | 5.137元 | 20.55元 |
| qwen2.5-14b-instruct | 2.569元 | 10.275元 |
| qwen2.5-7b-instruct | 1.284元 | 5.137元 |

### **Qwen2**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen2-72b-instruct | 4元  | 12元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen2-57b-a14b-instruct | 3.5元 | 7元  |
| qwen2-7b-instruct | 1元  | 2元  |
| qwen2-1.5b-instruct | 限时免费 |   |   |
| qwen2-0.5b-instruct |

### **Qwen1.5**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen1.5-110b-chat | 7元  | 14元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen1.5-72b-chat | 5元  | 10元 |
| qwen1.5-32b-chat | 3.5元 | 7元  |
| qwen1.5-14b-chat | 2元  | 4元  |
| qwen1.5-7b-chat | 1元  | 2元  |
| qwen1.5-1.8b-chat | 限时免费 |   |   |
| qwen1.5-0.5b-chat |

### **QVQ**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qvq-72b-preview | 12元 | 36元 | 10万Token 有效期：阿里云百炼开通后90天内 |

### **Qwen-Omni**

计费规则：按输入Token和输出Token计费。不同模态的Token计算规则请参见[计费与限流](https://help.aliyun.com/zh/model-studio/qwen-omni#12db7427b94qt)。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输入单价（每百万Token）** |   |   | **输出单价（每百万Token）** |   |   | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **文本** | **音频** | **图片/视频** | **文本** > 仅纯文本输入 | **文本** > 多模态输入 | **文本+音频** > 仅音频计费 |
| qwen2.5-omni-7b | 0.6元 | 38元 | 2元  | 2.4元 | 6元  | 76元 | 100万Token（不区分模态） 有效期：阿里云百炼开通后90天 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际（新加坡）模型无免费额度。

| **模型名称** | **输入单价（每百万Token）** |   |   | **输出单价（每百万Token）** |   |   |
| --- | --- | --- | --- | --- | --- | --- |
| **文本** | **音频** | **图片/视频** | **文本** > 仅纯文本输入 | **文本** > 多模态输入 | **文本+音频** > 仅音频计费 |
| qwen2.5-omni-7b | 0.734元 | 49.613元 | 2.055元 | 2.936元 | 6.165元 | 99.153元 |

### **Qwen3-Omni-Captioner**

计费规则：按输入Token和输出Token计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-omni-30b-a3b-captioner | 15.8元 | 12.7元 | 100万Token 有效期：阿里云百炼开通后90天内 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际（新加坡）模型无免费额度。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** |
| --- | --- | --- |
| qwen3-omni-30b-a3b-captioner | 27.962元 | 22.458元 |

### **Qwen-VL**

计费规则：按输入Token和输出Token计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **模式** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链+回答** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| qwen3-vl-235b-a22b-thinking | 仅思考模式 | 2元  | 20元 | 各100万 Token 有效期：阿里云百炼开通后90天内 |
| qwen3-vl-235b-a22b-instruct | 仅非思考模式 | 2元  | 8元  |
| qwen3-vl-32b-thinking | 仅思考模式 | 2元  | 20元 |
| qwen3-vl-32b-instruct | 仅非思考模式 | 2元  | 8元  |
| qwen3-vl-30b-a3b-thinking | 仅思考模式 | 0.75元 | 7.5元 |
| qwen3-vl-30b-a3b-instruct | 仅非思考模式 | 0.75元 | 3元  |
| qwen3-vl-8b-thinking | 仅思考模式 | 0.5元 | 5元  |
| qwen3-vl-8b-instruct | 仅非思考模式 | 0.5元 | 2元  |

##### **更多模型**

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen2.5-vl-72b-instruct | 16元 | 48元 | 各100万 Token 有效期：阿里云百炼开通后90天内 |
| qwen2.5-vl-32b-instruct | 8元  | 24元 |
| qwen2.5-vl-7b-instruct | 2元  | 5元  |
| qwen2.5-vl-3b-instruct | 1.2元 | 3.6元 |
| qwen2-vl-72b-instruct | 16元 | 48元 |
| qwen2-vl-7b-instruct | 目前仅供免费体验。 > 免费额度用完后不可调用，建议改用qwen-vl-max、qwen-vl-plus模型。 |   | 各10万Token 有效期：阿里云百炼开通后90天内 |
| qwen2-vl-2b-instruct | 限时免费 |   |
| qwen-vl-v1 | 目前仅供免费体验。 > 免费额度用完后不可调用，建议改用qwen-vl-max、qwen-vl-plus模型。 |   |
| qwen-vl-chat-v1 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

**说明**

全球部署模式的模型无免费额度。

| **模型名称** | **模式** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链+回答** |
| --- | --- | --- | --- |
| qwen3-vl-235b-a22b-thinking | 仅思考模式 | 2元  | 20元 |
| qwen3-vl-235b-a22b-instruct | 仅非思考模式 | 2元  | 8元  |
| qwen3-vl-32b-thinking | 仅思考模式 | 1.174元 | 4.697元 |
| qwen3-vl-32b-instruct | 仅非思考模式 | 1.174元 | 4.697元 |
| qwen3-vl-30b-a3b-thinking | 仅思考模式 | 0.75元 | 7.5元 |
| qwen3-vl-30b-a3b-instruct | 仅非思考模式 | 0.75元 | 3元  |
| qwen3-vl-8b-thinking | 仅思考模式 | 0.5元 | 5元  |
| qwen3-vl-8b-instruct | 仅非思考模式 | 0.5元 | 2元  |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **模式** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链+回答** |
| --- | --- | --- | --- |
| qwen3-vl-235b-a22b-thinking | 仅思考模式 | 2.936元 | 29.357元 |
| qwen3-vl-235b-a22b-instruct | 仅非思考模式 | 2.936元 | 11.743元 |
| qwen3-vl-32b-thinking | 仅思考模式 | 1.174元 | 4.697元 |
| qwen3-vl-32b-instruct | 仅非思考模式 | 1.174元 | 4.697元 |
| qwen3-vl-30b-a3b-thinking | 仅思考模式 | 1.468元 | 17.614元 |
| qwen3-vl-30b-a3b-instruct | 仅非思考模式 | 1.468元 | 5.871元 |
| qwen3-vl-8b-thinking | 仅思考模式 | 1.321元 | 15.412元 |
| qwen3-vl-8b-instruct | 仅非思考模式 | 1.321元 | 5.137元 |

##### **更多模型**

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen2.5-vl-72b-instruct | 20.55元 | 61.65元 | 各100万 Token 有效期：阿里云百炼开通后90天内 |
| qwen2.5-vl-32b-instruct | 10.275元 | 30.825元 |
| qwen2.5-vl-7b-instruct | 2.569元 | 7.706元 |
| qwen2.5-vl-3b-instruct | 1.541元 | 4.624元 |

### **Qwen-Audio**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen2-audio-instruct | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐使用[全模态（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni)作为替代模型。 |   | 各10万Token 有效期：阿里云百炼开通后90天内 |
| qwen-audio-chat |

### **Qwen-Math**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen2.5-math-72b-instruct | 4元  | 12元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen2.5-math-7b-instruct | 1元  | 2元  |
| qwen2.5-math-1.5b-instruct | 限时免费 |   |   |

### **Qwen-Coder**

计费规则：按输入Token和输出Token计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| qwen3-coder-next | 0<Token≤32K | 1元  | 4元  | 各100万Token 有效期：阿里云百炼开通后90天内 |
| 32K<Token≤128K | 1.5元 | 6元  |
| 128K<Token≤256K | 2.5元 | 10元 |
| qwen3-coder-480b-a35b-instruct | 0<Token≤32K | 6元  | 24元 |
| 32K<Token≤128K | 9元  | 36元 |
| 128K<Token≤200K | 15元 | 60元 |
| qwen3-coder-30b-a3b-instruct | 0<Token≤32K | 1.5元 | 6元  |
| 32K<Token≤128K | 2.25元 | 9元  |
| 128K<Token≤200K | 3.75元 | 15元 |
| qwen2.5-coder-32b-instruct | 无阶梯计价 | 2元  | 6元  |
| qwen2.5-coder-14b-instruct | 无阶梯计价 | 2元  | 6元  |
| qwen2.5-coder-7b-instruct | 无阶梯计价 | 1元  | 2元  |
| qwen2.5-coder-3b-instruct | 无阶梯计价 | 限时免费 |   |   |
| qwen2.5-coder-1.5b-instruct | 无阶梯计价 |
| qwen2.5-coder-0.5b-instruct | 无阶梯计价 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

**说明**

全球部署模式的模型无免费额度。

| **模型名称** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** |
| --- | --- | --- | --- |
| qwen3-coder-480b-a35b-instruct | 0<Token≤32K | 6元  | 24元 |
| 32K<Token≤128K | 9元  | 36元 |
| 128K<Token≤200K | 15元 | 60元 |
| qwen3-coder-30b-a3b-instruct | 0<Token≤32K | 1.5元 | 6元  |
| 32K<Token≤128K | 2.25元 | 9元  |
| 128K<Token≤200K | 3.75元 | 15元 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际（新加坡）模型无免费额度。

| **模型名称** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** |
| --- | --- | --- | --- |
| qwen3-coder-next | 0<Token≤32K | 2.202元 | 11.009元 |
| 32K<Token≤128K | 3.67元 | 18.348元 |
| 128K<Token≤256K | 5.871元 | 29.357元 |
| qwen3-coder-480b-a35b-instruct | 0<Token≤32K | 11.009元 | 55.044元 |
| 32K<Token≤128K | 19.816元 | 99.08元 |
| 128K<Token≤200K | 33.027元 | 165.133元 |
| qwen3-coder-30b-a3b-instruct | 0<Token≤32K | 3.303元 | 16.513元 |
| 32K<Token≤128K | 5.504元 | 27.522元 |
| 128K<Token≤200K | 8.807元 | 44.035元 |

## **文本生成-第三方模型**

### **DeepSeek**

计费规则：按输入Token和输出Token计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链+回答** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| deepseek-v3.2 > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 2元  | 3元  | 各100万Token 有效期：阿里云百炼开通后90天内 |
| deepseek-v3.2-exp | 2元  | 3元  |
| deepseek-v3.1 | 4元  | 12元 |
| deepseek-r1 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 4元  | 16元 |
| deepseek-r1-0528 | 4元  | 16元 |
| deepseek-v3 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 2元  | 8元  |
| deepseek-r1-distill-qwen-1.5b | 限时免费 |   |   |
| deepseek-r1-distill-qwen-7b | 0.5元 | 1元  | 各100万Token 有效期：阿里云百炼开通后90天内 |
| deepseek-r1-distill-qwen-14b | 1元  | 3元  |
| deepseek-r1-distill-qwen-32b | 2元  | 6元  |
| deepseek-r1-distill-llama-8b | 限时免费 |   |   |
| deepseek-r1-distill-llama-70b | 目前仅供免费体验 > 免费额度用完后不可调用，推荐使用[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)、[DeepSeek-阿里云](https://help.aliyun.com/zh/model-studio/deepseek-api)、[Kimi-阿里云](https://help.aliyun.com/zh/model-studio/kimi-api)作为替代模型 |   | 各100万Token 有效期：阿里云百炼开通后90天内 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际（新加坡）模型无免费额度。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链+回答** |
| --- | --- | --- |
| deepseek-v3.2 > [上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)享有折扣 | 4.272元 | 12.815元 |

### **DeepSeek-硅基流动**

**说明**

仅支持中国内地部署模式。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链+回答** | **免费额度** |
| --- | --- | --- | --- |
| siliconflow/deepseek-v3.2 | 2元  | 3元  | 无   |
| siliconflow/deepseek-v3.1-terminus | 4元  | 12元 |
| siliconflow/deepseek-r1-0528 | 4元  | 16元 |
| siliconflow/deepseek-v3-0324 | 2元  | 8元  |

### **Kimi**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| kimi-k2.5 | 4元  | 21元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| kimi-k2-thinking | 4元  | 16元 |
| Moonshot-Kimi-K2-Instruct | 4元  | 16元 |

### **Kimi-月之暗面**

**说明**

仅支持中国内地部署模式。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链和回答** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| kimi/kimi-k2.5 | 4元  | 21元 | 无   |

### **GLM**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **模式** | **单次请求的输入Token数** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链和回答** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| glm-5 | 非思考和思考模式 | 0<Token≤32K | 4元  | 18元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| 32K<Token≤198K | 6元  | 22元 |
| glm-4.7 | 非思考和思考模式 | 0<Token≤32K | 3元  | 14元 |
| 32K<Token≤166K | 4元  | 16元 |
| glm-4.6 | 非思考和思考模式 | 0<Token≤32K | 3元  | 14元 |
| 32K<Token≤166K | 4元  | 16元 |
| glm-4.5 | 非思考和思考模式 | 0<Token≤32K | 3元  | 14元 |
| 32K<Token≤96K | 4元  | 16元 |
| glm-4.5-air | 非思考和思考模式 | 0<Token≤32K | 0.8元 | 6元  |
| 32K<Token≤96K | 1.2元 | 8元  |

### **GLM-智谱**

**说明**

仅支持中国内地部署模式。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **模式** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链和回答** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| ZHIPU/GLM-5 | 非思考和思考模式 | 6元  | 22元 | 无   |

### MiniMax

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **模式** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链和回答** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| MiniMax-M2.5 | 仅思考模式 | 2.1元 | 8.4元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| MiniMax-M2.1 | 仅思考模式 | 2.1元 | 8.4元 |

### **MiniMax-稀宇科技**

**说明**

仅支持中国内地部署模式。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **模式** | **输入单价（每百万Token）** | **输出单价（每百万Token）** > **思维链和回答** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| MiniMax/MiniMax-M2.7 | 仅思考模式 | 2.1元 | 8.4元 | 无   |
| MiniMax/MiniMax-M2.5 | 仅思考模型 | 2.1元 | 8.4元 |
| MiniMax/MiniMax-M2.1 | 仅思考模式 | 2.1元 | 8.4元 |

### **MiniMax-abab**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| abab6.5g-chat | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐使用 [Qwen3](https://help.aliyun.com/zh/model-studio/deep-thinking)、[DeepSeek-阿里云](https://help.aliyun.com/zh/model-studio/deepseek-api)、[Kimi-阿里云](https://help.aliyun.com/zh/model-studio/kimi-api)等作为替代模型 |   | 各100万Token（需申请） 有效期：申请通过后90天内 |
| abab6.5t-chat |
| abab6.5s-chat |

## **图像生成**

计费规则：输入不计费，输出计费。输出按成功生成的 **图像张数** 计费。

计费公式：`费用 = 图像单价 × 输出的图像张数`。

计费说明：

-   费用与输出图像的分辨率、宽高比无关。
    
-   请求失败不产生任何费用，也不消耗免费额度。
    

计费示例：部分图像生成失败

假设图像单价为 0.10元/张。若您调用接口请求生成 4 张图像，但实际仅成功返回 3 张图像的 URL，另 1 张生成失败，系统将仅对成功生成的图像进行计费。

-   计费数量：3 张。
    
-   费用计算：0.1 × 3 = 0.3元。
    

### **千问文生图**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| qwen-image-2.0-pro | 0.5元/张 | 各100张 有效期：阿里云百炼开通后90天内 |
| qwen-image-2.0-pro-2026-03-03 | 0.5元/张 |
| qwen-image-2.0 | 0.2元/张 |
| qwen-image-2.0-2026-03-03 | 0.2元/张 |
| qwen-image-max | 0.5元/张 |
| qwen-image-max-2025-12-30 | 0.5元/张 |
| qwen-image-plus | 0.2元/张 |
| qwen-image-plus-2026-01-09 | 0.2元/张 |
| qwen-image | 0.25元/张 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输出单价** |
| --- | --- |
| qwen-image-2.0-pro | 0.550443元/张 |
| qwen-image-2.0-pro-2026-03-03 | 0.550443元/张 |
| qwen-image-2.0 | 0.256873元/张 |
| qwen-image-2.0-2026-03-03 | 0.256873元/张 |
| qwen-image-max | 0.550443元/张 |
| qwen-image-max-2025-12-30 | 0.550443元/张 |
| qwen-image-plus | 0.220177元/张 |
| qwen-image-plus-2026-01-09 | 0.220177元/张 |
| qwen-image | 0.256873元/张 |

### **千问图像编辑**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| qwen-image-2.0-pro | 0.5元/张 | 各100张 有效期：阿里云百炼开通后90天内 |
| qwen-image-2.0-pro-2026-03-03 | 0.5元/张 |
| qwen-image-2.0 | 0.2元/张 |
| qwen-image-2.0-2026-03-03 | 0.2元/张 |
| qwen-image-edit-max | 0.5元/张 |
| qwen-image-edit-max-2026-01-16 | 0.5元/张 |
| qwen-image-edit-plus | 0.2元/张 |
| qwen-image-edit-plus-2025-12-15 | 0.2元/张 |
| qwen-image-edit-plus-2025-10-30 | 0.2元/张 |
| qwen-image-edit | 0.3元/张 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输出单价** |
| --- | --- |
| qwen-image-2.0-pro | 0.550443元/张 |
| qwen-image-2.0-pro-2026-03-03 | 0.550443元/张 |
| qwen-image-2.0 | 0.256873元/张 |
| qwen-image-2.0-2026-03-03 | 0.256873元/张 |
| qwen-image-edit-max | 0.550443元/张 |
| qwen-image-edit-max-2026-01-16 | 0.550443元/张 |
| qwen-image-edit-plus | 0.220177元/张 |
| qwen-image-edit-plus-2025-12-15 | 0.220177元/张 |
| qwen-image-edit-plus-2025-10-30 | 0.220177元/张 |
| qwen-image-edit | 0.330266元/张 |

### **千问图像翻译**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| qwen-mt-image | 0.003元/张 | 100张 有效期：阿里云百炼开通后90天内 |

### **Z-Image**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| z-image-turbo | 关闭提示词改写（`prompt_extend=false`）：0.1元/张 开启提示词改写（`prompt_extend=true`）：0.2元/张 | 100张 有效期：阿里云百炼开通后90天内 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输出单价** |
| --- | --- |
| z-image-turbo | 关闭提示词改写（`prompt_extend=false`）：0.110089元/张 开启提示词改写（`prompt_extend=true`）：0.220177元/张 |

### **万相文生图**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- |
| wan2.6-t2i | 0.20元/张 | 50张 |
| wan2.5-t2i-preview | 0.20元/张 | 50张 |
| wan2.2-t2i-plus | 0.20元/张 | 100张 |
| wan2.2-t2i-flash | 0.14元/张 | 100张 |
| wanx2.1-t2i-plus | 0.20元/张 | 500张 |
| wanx2.1-t2i-turbo | 0.14元/张 | 500张 |
| wanx2.0-t2i-turbo | 0.04元/张 | 500张 |
| wanx-v1 | 0.16元/张 | 500张 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

**说明**

全球部署模式的模型无免费额度。

| **模型名称** | **输出单价** |
| --- | --- |
| wan2.6-t2i | 0.20元/张 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输出单价** |
| --- | --- |
| wan2.6-t2i | 0.220177元/张 |
| wan2.5-t2i-preview | 0.220177元/张 |
| wan2.2-t2i-plus | 0.366962元/张 |
| wan2.2-t2i-flash | 0.183481元/张 |
| wan2.1-t2i-plus | 0.366962元/张 |
| wan2.1-t2i-turbo | 0.183481元/张 |

### **万相图像生成与编辑**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- |
| wan2.6-image | 0.20元/张 | 50张 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

**说明**

全球部署模式的模型无免费额度。

| **模型名称** | **输出单价** |
| --- | --- |
| wan2.6-image | 0.20元/张 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输出单价** |
| --- | --- |
| wan2.6-image | 0.220177元/张 |

### **万相通用图像编辑**

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- |
| wan2.5-i2i-preview | 0.20元/张 | 50张 |
| wanx2.1-imageedit | 0.14元/张 | 500张 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输出单价** |
| --- | --- |
| wan2.5-i2i-preview | 0.220177元/张 |

### **万相涂鸦作画**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| wanx-sketch-to-image-lite | 0.06元/张 | 500张 有效期：阿里云百炼开通后90天内 |

### **万相图像局部重绘**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| wanx-x-painting | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)或[图像编辑-万相2.1](https://help.aliyun.com/zh/model-studio/wanx-image-edit)获取替代方案。 | 500张 有效期：阿里云百炼开通后90天内 |

### 人像风格重绘

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| wanx-style-repaint-v1 | 0.12元/张 | 500张 有效期：阿里云百炼开通后90天内 |

### **图像背景生成**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| wanx-background-generation-v2 | 0.08元/张 | 500张 有效期：阿里云百炼开通后90天内 |

### **图像画面扩展**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| image-out-painting | 0.18元/张 | 500张 有效期：阿里云百炼开通后90天内 |

### **人物实例分割**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| image-instance-segmentation | 目前仅供免费体验。 > 免费额度用完后不可调用。 | 500张 有效期：阿里云百炼开通后90天内 |

### **图像擦除补全**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| image-erase-completion | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)或[图像编辑-万相2.1](https://help.aliyun.com/zh/model-studio/wanx-image-edit)获取替代方案。 | 500张 有效期：阿里云百炼开通后90天内 |

### **虚拟模特**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| wanx-virtualmodel | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)或[图像编辑-万相2.1](https://help.aliyun.com/zh/model-studio/wanx-image-edit)获取替代方案。 | 各500张 有效期：阿里云百炼开通后90天内 |
| virtualmodel-v2 |

### **鞋靴模特**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| shoemodel-v1 | 目前仅供免费体验。 > 免费额度用完后不可调用。 | 500张 有效期：阿里云百炼开通后90天内 |

### **创意海报生成**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| wanx-poster-generation-v1 | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐参考[图像编辑-千问](https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide)或[图像编辑-万相2.1](https://help.aliyun.com/zh/model-studio/wanx-image-edit)获取替代方案。 | 500张 有效期：阿里云百炼开通后90天内 |

### **人物写真生成-FaceChain**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

-   facechain-facedetect：限时免费。
    
-   facechain-finetune：按训练次数计费，请求失败不计费。
    
-   facechain-generation：输入不计费，输出计费。输出按成功生成的图片张数计费，计费规则请参见[图像生成](#26310bc5cf4do)。
    

| **模型服务** | **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| 人物图像检测 | facechain-facedetect | 限时免费 | 限时免费 |
| 人物形象训练 | facechain-finetune | 2.5元/次 | 50次 有效期：申请通过后90天内 |
| 人物写真生成 | facechain-generation | 0.18元/张 | 500张 有效期：申请通过后90天内 |

### **创意文字生成-WordArt锦书**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

| **模型服务** | **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| 文字纹理生成 | wordart-texture | 0.08元/张 | 500张 有效期：阿里云百炼开通后90天内 |
| 文字变形 | wordart-semantic | 0.24元/张 |

### **AI试衣-OutfitAnyone**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

-   aitryon：输入不计费，输出计费。计费规则请参见[图像生成](#26310bc5cf4do)。
    
-   aitryon-plus：输入不计费，输出计费。计费规则请参见[图像生成](#26310bc5cf4do)。
    
-   aitryon-parsing-v1：输入计费，输出不计费。按输入的图像张数计费，请求失败不计费。
    
-   aitryon-refiner：输入不计费，输出计费。计费规则请参见[图像生成](#26310bc5cf4do)。
    

| **模型服务** | **模型名称** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- |
| AI试衣-基础版 | aitryon | 400张 |
| AI试衣-Plus版 | aitryon-plus | 400张 |
| AI试衣-图片分割 | aitryon-parsing-v1 | 400张 |
| AI试衣-图片精修 | aitryon-refiner | 100张 |

| **模型服务** | **模型名称** | **单价** | **折扣** | **阶梯层级** |
| --- | --- | --- | --- | --- |
| AI试衣-基础版 | aitryon | 0.20元/张 | 无   | 无   |
| AI试衣-Plus版 | aitryon-plus | 0.50元/张 | 无   | 无   |
| AI试衣-图片分割 | aitryon-parsing-v1 | 0.004元/张 | 无   | 无   |
| AI试衣-图片精修 | aitryon-refiner | 0.30元/张 | 无   | 生成数量 ≤ 25张 |
| 0.275元/张 | 9.2折 | 25张 ＜ 生成数量 ≤ 125张 |
| 0.25元/张 | 8.4折 | 125张 ＜ 生成数量 ≤ 250张 |
| 0.225元/张 | 7.5折 | 250张 ＜ 生成数量 ≤ 1250张 |
| 0.20元/张 | 6.7折 | 1250张 ＜ 生成数量 ≤ 2500张 |
| 0.175元/张 | 5.8折 | 2500张 ＜ 生成数量 ≤ 2.5万张 |
| 0.15元/张 | 5折  | 生成数量 ＞ 2.5万张 |

## **图像生成-第三方模型**

### **可灵-图像生成**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

| **模型名称** | **输出图像分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| kling/kling-v3-image-generation | 1K  | 0.2元/张 | 无免费额度 |
| 2K  | 0.2元/张 |
| kling/kling-v3-omni-image-generation | 1K  | 0.2元/张 |
| 2K  | 0.2元/张 |
| 4K  | 0.4元/张 |

### **StableDiffusion文生图模型**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| stable-diffusion-3.5-large | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐参考[文本生成图像](https://help.aliyun.com/zh/model-studio/text-to-image)获取替代方案 | 各500张 有效期：申请通过后90天内 |
| stable-diffusion-3.5-large-turbo |
| stable-diffusion-xl |
| stable-diffusion-v1.5 |

### **FLUX文生图模型**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[图像生成](#26310bc5cf4do)。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| flux-merged | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐参考[文本生成图像](https://help.aliyun.com/zh/model-studio/text-to-image)获取替代方案 | 各100张 有效期：阿里云百炼开通后90天内 |
| flux-dev |
| flux-schnell |

## **语音合成（文本转语音）**

### **Qwen-TTS**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

## **千问3-TTS-Instruct-Flash**

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-tts-instruct-flash | 0.8元 | 不计费 | 1万字符 有效期：阿里云百炼开通后90天内 |
| qwen3-tts-instruct-flash-2026-01-26 | 0.8元 | 不计费 |

## **千问3-TTS-VD**

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-tts-vd-2026-01-26 | 0.8元 | 不计费 | 1万字符 有效期：阿里云百炼开通后90天内 |

## **千问3-TTS-VC**

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-tts-vc-2026-01-22 | 0.8元 | 不计费 | 1万字符 有效期：阿里云百炼开通后90天内 |

## 千问3-TTS-Flash

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-tts-flash | 0.8元 | 不计费 | 1万字符 有效期：阿里云百炼开通后90天内 |
| qwen3-tts-flash-2025-11-27 | 0.8元 | 不计费 |
| qwen3-tts-flash-2025-09-18 | 0.8元 | 不计费 | 2025年11月13日0点前开通阿里云百炼：2000字符 2025年11月13日0点后开通阿里云百炼：1万字符 有效期：阿里云百炼开通后90天内 |

## 千问-TTS

计费规则：按输入Token和输出Token计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen-tts-flash | 1.6元 | 10元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen-tts-latest | 1.6元 | 10元 |
| qwen-tts-2025-05-22 | 1.6元 | 10元 |
| qwen-tts-2025-04-10 | 1.6元 | 10元 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

## **千问3-TTS-Instruct-Flash**

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** |
| --- | --- |
| qwen3-tts-instruct-flash | 0.8元 |
| qwen3-tts-instruct-flash-2026-01-26 | 0.8元 |

## **千问3-TTS-VD**

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** |
| --- | --- |
| qwen3-tts-vd-2026-01-26 | 0.8元 |

## **千问3-TTS-VC**

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** |
| --- | --- |
| qwen3-tts-vc-2026-01-22 | 0.8元 |

## 千问3-TTS-Flash

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** |
| --- | --- |
| qwen3-tts-flash | 0.733924元 |
| qwen3-tts-flash-2025-11-27 | 0.733924元 |
| qwen3-tts-flash-2025-09-18 | 0.733924元 |

### **Qwen-TTS-Realtime**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

## **千问3-TTS-Instruct-Flash-Realtime**

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-tts-instruct-flash-realtime | 1元  | 不计费 | 1万字符 有效期：阿里云百炼开通后90天内 |
| qwen3-tts-instruct-flash-realtime-2026-01-22 | 1元  | 不计费 | 1万字符 有效期：阿里云百炼开通后90天内 |

## 千问3-TTS-VD-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-tts-vd-realtime-2026-01-15 | 1元  | 不计费 | 1万字符 有效期：阿里云百炼开通后90天内 |
| qwen3-tts-vd-realtime-2025-12-16 | 1元  | 不计费 | 1万字符 有效期：阿里云百炼开通后90天内 |

## 千问3-TTS-VC-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-tts-vc-realtime-2026-01-15 | 1元  | 不计费 | 1万字符 有效期：阿里云百炼开通后90天内 |
| qwen3-tts-vc-realtime-2025-11-27 |

## 千问3-TTS-Flash-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-tts-flash-realtime | 1元  | 不计费 | 2025年11月13日0点前开通阿里云百炼：2000字符 2025年11月13日0点后开通阿里云百炼：1万字符 有效期：阿里云百炼开通后90天内 |
| qwen3-tts-flash-realtime-2025-11-27 | 1元  | 不计费 | 1万字符 有效期：阿里云百炼开通后90天内 |
| qwen3-tts-flash-realtime-2025-09-18 | 1元  | 不计费 | 2025年11月13日0点前开通阿里云百炼：2000字符 2025年11月13日0点后开通阿里云百炼：1万字符 有效期：阿里云百炼开通后90天内 |

## 千问-TTS-Realtime

计费规则：按输入Token和输出Token计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen-tts-realtime | 2.4元 | 12元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen-tts-realtime-latest | 2.4元 | 12元 |
| qwen-tts-realtime-2025-07-15 | 2.4元 | 12元 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

## **千问3-TTS-Instruct-Flash-Realtime**

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** |
| --- | --- |
| qwen3-tts-instruct-flash-realtime | 1元  |
| qwen3-tts-instruct-flash-realtime-2026-01-22 | 1元  |

## 千问3-TTS-VD-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** |
| --- | --- |
| qwen3-tts-vd-realtime-2026-01-15 | 0.954101元 |
| qwen3-tts-vd-realtime-2025-12-16 | 0.954101元 |

## 千问3-TTS-VC-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** |
| --- | --- |
| qwen3-tts-vc-realtime-2026-01-15 | 0.954101元 |
| qwen3-tts-vc-realtime-2025-11-27 |

## 千问3-TTS-Flash-Realtime

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** |
| --- | --- |
| qwen3-tts-flash-realtime | 0.954101元 |
| qwen3-tts-flash-realtime-2025-11-27 | 0.954101元 |
| qwen3-tts-flash-realtime-2025-09-18 | 0.954101元 |

### **Qwen-TTS声音复刻**

计费规则：按新建音色个数计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单价（每个音色）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| qwen-voice-enrollment | 0.01元 | 1000个音色/账号 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **单价（每个音色）** |
| --- | --- |
| qwen-voice-enrollment | 0.01元 |

### **Qwen-TTS声音设计**

计费规则：按新建音色个数计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **单价（每个音色）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| qwen-voice-design | 0.2元 | 10个音色/账号 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **单价（每个音色）** |
| --- | --- |
| qwen-voice-design | 0.2元 |

### **CosyVoice**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| cosyvoice-v3.5-plus | 1.5元 | 1万字符 有效期：阿里云百炼开通后90天内 |
| cosyvoice-v3.5-flash | 0.8元 |
| cosyvoice-v3-plus | 2元  |
| cosyvoice-v3-flash | 1元  |
| cosyvoice-v2 | 2元  |
| cosyvoice-v1 | 2元  |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| cosyvoice-v3-plus | 1.9082元 | 无免费额度 |
| cosyvoice-v3-flash | 0.9541元 |

### **Sambert**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入文本的字符数计费，输出不计费。

| **模型名称** | **输入单价（每万字符）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| 参见[模型列表](https://help.aliyun.com/zh/model-studio/sambert-java-sdk#57d33631f7doi) | 1元  | 每主账号每模型每月3万字符。 |

### MiniMax

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入文本的字符数计费，输出不计费。

复刻音色收取一次性费用，费用在首次使用该音色进行语音合成的时候，与语音合成的费用一同出账。

| **模型名称** | **语音合成单价（每万字符）** | [复刻一个音色](https://help.aliyun.com/zh/model-studio/mini-clone-api) | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| MiniMax/speech-2.8-hd | 3.5元 | 9.9元 （在首次使用复刻出来的音色进行语音合成的时候收取） | 无   |
| MiniMax/speech-02-hd | 3.5元 |
| MiniMax/speech-2.8-turbo | 2元  |
| MiniMax/speech-02-turbo | 2元  |

## **语音识别（语音转文本）与翻译（语音转成指定语种的文本）**

### **千问3-LiveTranslate-Flash-Realtime**

计费规则：按输入Token和输出Token计费。不同模态的Token计算规则请参见[计费说明](https://help.aliyun.com/zh/model-studio/qwen3-livetranslate-flash-realtime#6a95f2fc38za0)。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输入单价（每百万Token）** |   | **输出单价（每百万Token）** |   | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- |
| **输入：音频** | **输入：图片** | **输出：文本** | **输出：音频** |
| qwen3-livetranslate-flash-realtime | 64元 | 8元  | 64元 | 240元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen3-livetranslate-flash-realtime-2025-09-22 | 64元 | 8元  | 64元 | 240元 |

## **国际**

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输入单价 (每百万 Token)** |   | **输出单价 (每百万 Token)** |   |
| --- | --- | --- | --- | --- |
| **输入：音频** | **输入：图片** | **输出：文本** | **输出：音频** |
| qwen3-livetranslate-flash-realtime | 73.392元 | 9.541元 | 73.392元 | 278.891元 |
| qwen3-livetranslate-flash-realtime-2025-09-22 | 73.392元 | 9.541元 | 73.392元 | 278.891元 |

### **千问ASR**

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入音频的秒数计费，输出不计费。

| **模型名称** | **输入单价** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen3-asr-flash-filetrans | 0.00022元/秒 | 不计费 | 36,000秒（10小时） 有效期：阿里云百炼开通后90天内 |
| qwen3-asr-flash-filetrans-2025-11-17 |
| qwen3-asr-flash |
| qwen3-asr-flash-2026-02-10 |
| qwen3-asr-flash-2025-09-08 |

##### **更多模型**

计费规则：按输入和输出的总Token计费。

音频Token计算规则：每秒音频转换为25个Token，不足1秒按1秒计算。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen-audio-asr | 目前仅供免费体验。 > 免费额度用完后不可调用，推荐使用 Qwen3 ASR。 |   | 各10万Token 有效期：阿里云百炼开通后90天内 |
| qwen-audio-asr-latest |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

计费规则：按输入音频的秒数计费，输出不计费。

| **模型名称** | **输入单价** | **输出单价** |
| --- | --- | --- |
| qwen3-asr-flash-filetrans | 0.00026元/秒 | 不计费 |
| qwen3-asr-flash-filetrans-2025-11-17 |
| qwen3-asr-flash |
| qwen3-asr-flash-2026-02-10 |
| qwen3-asr-flash-2025-09-08 |

## 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

**说明**

美国部署模式的模型无免费额度。

计费规则：按输入音频的秒数计费，输出不计费。

| **模型名称** | **输入单价** | **输出单价** |
| --- | --- | --- |
| qwen3-asr-flash-us | 0.000035元/秒 | 不计费 |
| qwen3-asr-flash-2025-09-08-us |

### **千问ASR-Realtime**

计费规则：按输入音频的秒数计费，输出不计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输入单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| qwen3-asr-flash-realtime | 0.00033元/秒 | 36,000秒（10小时） 有效期：阿里云百炼开通后90天内 |
| qwen3-asr-flash-realtime-2026-02-10 |
| qwen3-asr-flash-realtime-2025-10-27 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输入单价** |
| --- | --- |
| qwen3-asr-flash-realtime | 0.00066元/秒 |
| qwen3-asr-flash-realtime-2026-02-10 |
| qwen3-asr-flash-realtime-2025-10-27 |

### **Gummy语音识别/翻译**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入音频的秒数计费，输出不计费。

| **模型名称** | **输入单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| gummy-realtime-v1 | 0.00015元/秒 | 36,000秒（10小时） 2025年1月17日0点前开通百炼：有效期至2025年7月15日 2025年1月17日0点起至9月8日11点前开通百炼：自开通日起90天有效 2025年9月8日11点后开通百炼：自开通日起90天有效 |
| gummy-chat-v1 |

### **Fun-ASR**

#### **录音文件识别**

计费规则：按输入音频的秒数计费，输出不计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输入单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| fun-asr | 0.00022元/秒 | 36,000秒（10小时） 有效期：阿里云百炼开通后90天 |
| fun-asr-2025-11-07 |
| fun-asr-2025-08-25 |
| fun-asr-mtl |
| fun-asr-mtl-2025-08-25 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输入单价** |
| --- | --- |
| fun-asr | 0.00026元/秒 |
| fun-asr-2025-11-07 |
| fun-asr-2025-08-25 |
| fun-asr-mtl |
| fun-asr-mtl-2025-08-25 |

#### **实时语音识别**

计费规则：按输入音频的秒数计费，输出不计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输入单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| fun-asr-realtime | 0.00033元/秒 | 36,000秒（10小时） 有效期：阿里云百炼开通后90天 |
| fun-asr-realtime-2026-02-28 |
| fun-asr-realtime-2025-11-07 |
| fun-asr-realtime-2025-09-15 |
| fun-asr-flash-8k-realtime | 0.00022元/秒 |
| fun-asr-flash-8k-realtime-2026-01-28 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输入单价** |
| --- | --- |
| fun-asr-realtime | 0.00066元/秒 |
| fun-asr-realtime-2025-11-07 |

### **Paraformer**

#### **录音文件识别**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入音频的秒数计费，输出不计费。

| **模型名称** | **输入单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| paraformer-v2 | 0.00008元/秒 | 36,000秒（10小时） 每月1日0点自动发放 有效期1个月 |
| paraformer-8k-v2 |
| paraformer-v1 |
| paraformer-8k-v1 |
| paraformer-mtl-v1 |

#### **实时语音识别**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入音频的秒数计费，输出不计费。

| **模型名称** | **输入单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| paraformer-realtime-v2 | 0.00024元/秒 | 36,000秒（10小时） 每月1日0点自动发放 有效期1个月 |
| paraformer-realtime-v1 |
| paraformer-realtime-8k-v2 |
| paraformer-realtime-8k-v1 |

### **SenseVoice**

#### **录音文件识别**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入音频的秒数计费，输出不计费。

| **模型名称** | **输入单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| sensevoice-v1 | 0.0007元/秒 | 36,000秒（10小时） 每月1日0点自动发放 有效期1个月 |

## **视频生成**

计费规则：输入不计费，输出计费。输出按成功生成的 **视频秒数** 计费。

计费公式：`费用 = 视频单价 × 输出的视频时长（单位：秒）`。

计费说明：

-   部分模型按**输出视频分辨率定价**。不同分辨率（480P/720P/1080P）的计费价格有差异。
    
-   部分模型按**输出视频模式定价**。不同视频模式（标准版/专业版）的计费价格有差异。
    
-   部分模型按**输出视频画幅定价**。不同视频画幅（1:1/3:4）的计费价格有差异。
    
-   部分模型采用**统一定价**，与分辨率、模式或画幅无关。
    
-   请求失败不产生任何费用，也不会消耗免费额度。
    

### **万相-文生视频**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- | --- |
| wan2.6-t2v | 720P | 0.6元/秒 | 50秒 |
| 1080P | 1元/秒 |
| wan2.5-t2v-preview | 480P | 0.3元/秒 | 50秒 |
| 720P | 0.6元/秒 |
| 1080P | 1元/秒 |
| wan2.2-t2v-plus | 480P | 0.14元/秒 | 50秒 |
| 1080P | 0.70元/秒 |
| wanx2.1-t2v-turbo | 480P | 0.24元/秒 | 200秒 |
| 720P | 0.24元/秒 |
| wanx2.1-t2v-plus | 720P | 0.70元/秒 | 200秒 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

**说明**

全球部署模式的模型无免费额度。

| **模型名称** | **输出视频分辨率** | **输出单价** |
| --- | --- | --- |
| wan2.6-t2v | 720P | 0.6元/秒 |
| 1080P | 1元/秒 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输出视频分辨率** | **输出单价** |
| --- | --- | --- |
| wan2.6-t2v | 720P | 0.733924元/秒 |
| 1080P | 1.100886元/秒 |
| wan2.5-t2v-preview | 480P | 0.366961元/秒 |
| 720P | 0.733923元/秒 |
| 1080P | 1.100885元/秒 |
| wan2.2-t2v-plus | 480P | 0.146785元/秒 |
| 1080P | 0.733924元/秒 |
| wan2.1-t2v-turbo | 480P | 0.264213元/秒 |
| 720P | 0.264213元/秒 |
| wan2.1-t2v-plus | 720P | 0.733924元/秒 |

## 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

**说明**

美国部署模式的模型无免费额度。

| **模型名称** | **输出视频分辨率** | **输出单价** |
| --- | --- | --- |
| wan2.6-t2v-us | 720P | 0.733924元/秒 |
| 1080P | 1.100886元/秒 |

### **万相-图生视频-基于首帧**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输出视频类型** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- | --- | --- |
| wan2.6-i2v-flash | 有声视频 `audio=true` | 720P | 0.3元/秒 | 50秒 |
| 1080P | 0.5元/秒 |
| 无声视频 `audio=false` | 720P | 0.15元/秒 |
| 1080P | 0.25元/秒 |
| wan2.6-i2v | 有声视频 | 720P | 0.6元/秒 | 50秒 |
| 1080P | 1元/秒 |
| wan2.5-i2v-preview | 有声视频 | 480P | 0.3元/秒 | 50秒 |
| 720P | 0.6元/秒 |
| 1080P | 1元/秒 |
| wan2.2-i2v-flash | 无声视频 | 480P | 0.10元/秒 | 50秒 |
| 720P | 0.20元/秒 |
| 1080P | 0.48元/秒 |
| wan2.2-i2v-plus | 无声视频 | 480P | 0.14元/秒 | 50秒 |
| 1080P | 0.70元/秒 |
| wanx2.1-i2v-turbo | 无声视频 | 480P | 0.24元/秒 | 200秒 |
| 720P | 0.24元/秒 |
| wanx2.1-i2v-plus | 无声视频 | 720P | 0.70元/秒 | 200秒 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

**说明**

全球部署模式的模型无免费额度。

| **模型名称** | **输出视频类型** | **输出视频分辨率** | **输出单价** |
| --- | --- | --- | --- |
| wan2.6-i2v | 有声视频 | 720P | 0.6元/秒 |
| 1080P | 1元/秒 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输出视频类型** | **输出视频分辨率** | **输出单价** |
| --- | --- | --- | --- |
| wan2.6-i2v-flash | 有声视频 `audio=true` | 720P | 0.366962元/秒 |
| 1080P | 0.550443元/秒 |
| 无声视频 `audio=false` | 720P | 0.183481元/秒 |
| 1080P | 0.275221元/秒 |
| wan2.6-i2v | 有声视频 | 720P | 0.733924元/秒 |
| 1080P | 1.100886元/秒 |
| wan2.5-i2v-preview | 有声视频 | 480P | 0.366961元/秒 |
| 720P | 0.733923元/秒 |
| 1080P | 1.100885元/秒 |
| wan2.2-i2v-flash | 无声视频 | 480P | 0.110089元/秒 |
| 720P | 0.264213元/秒 |
| wan2.2-i2v-plus | 无声视频 | 480P | 0.146785元/秒 |
| 1080P | 0.733924元/秒 |
| wan2.1-i2v-turbo | 无声视频 | 480P | 0.264213元/秒 |
| 720P | 0.264213元/秒 |
| wan2.1-i2v-plus | 无声视频 | 720P | 0.733924元/秒 |

## 美国

在[美国部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）地域**，模型推理计算资源仅限于美国境内。

**说明**

美国部署模式的模型无免费额度。

| **模型名称** | **输出视频类型** | **输出视频分辨率** | **输出单价** |
| --- | --- | --- | --- |
| wan2.6-i2v-us | 有声视频 | 720P | 0.733924元/秒 |
| 1080P | 1.100886元/秒 |

### **万相-图生视频-基于首尾帧**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- | --- |
| wan2.2-kf2v-flash | 480P | 0.10元/秒 | 50秒 |
| 720P | 0.20元/秒 |
| 1080P | 0.48元/秒 |
| wanx2.1-kf2v-plus | 720P | 0.70元/秒 | 200秒 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输出视频分辨率** | **输出单价** |
| --- | --- | --- |
| wan2.1-kf2v-plus | 720P | 0.733924元/秒 |

### **万相-参考生视频**

计费规则：输入视频和输出视频均计费，按**视频秒数**计费，失败不计费也不占用免费额度。

-   计费公式：计费时长 = 输入视频时长（上限 5 秒）+ 输出视频时长。
    
    -   输入视频的计费时长不超过 **5 秒**，计算规则参见[万相-参考生视频](https://help.aliyun.com/zh/model-studio/wan-video-to-video-api-reference#f79461ca408qn)。
        
    -   输出视频的计费时长为**成功生成的视频秒数**。
        
-   定价说明：计费单价由分辨率档位和 audio（是否输出有声视频）决定，与输入视频的实际分辨率或音频状态无关。
    

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输出视频类型** | **输出视频分辨率** | **输入和输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- | --- | --- |
| wan2.6-r2v-flash | 有声视频 `audio=true` | 720P | 0.3元/秒 | 50秒 |
| 1080P | 0.5元/秒 |
| 无声视频 `audio=false` | 720P | 0.15元/秒 |
| 1080P | 0.25元/秒 |
| wan2.6-r2v | 有声视频 | 720P | 0.6元/秒 | 50秒 |
| 1080P | 1元/秒 |

## 全球

在[全球部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**美国（弗吉尼亚）****地域**，模型推理计算资源在全球范围内动态调度。

**说明**

全球部署模式的模型无免费额度。

| **模型名称** | **输出视频类型** | **输出视频分辨率** | **输入和输出单价** |
| --- | --- | --- | --- |
| wan2.6-r2v | 有声视频 | 720P | 0.6元/秒 |
| 1080P | 1元/秒 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输出视频类型** | **输出视频分辨率** | **输入和输出单价** |
| --- | --- | --- | --- |
| wan2.6-r2v-flash | 有声视频 `audio=true` | 720P | 0.366962元/秒 |
| 1080P | 0.550443元/秒 |
| 无声视频 `audio=false` | 720P | 0.183481元/秒 |
| 1080P | 0.275221元/秒 |
| wan2.6-r2v | 有声视频 | 720P | 0.733924元/秒 |
| 1080P | 1.100886元/秒 |

### **万相-通用视频编辑**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| wanx2.1-vace-plus | 720P | 0.70元/秒 | 50秒 有效期：阿里云百炼开通后90天内 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输出视频分辨率** | **输出单价** |
| --- | --- | --- |
| wan2.1-vace-plus | 720P | 0.733924元/秒 |

### **万相-数字人**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

-   wan2.2-s2v-detect：输入计费，输出不计费。输入按检测的图像张数计费，只要请求成功（无论检测结果通过与否），每张输入图像均计费一次。
    
-   wan2.2-s2v：输入不计费，输出计费。输出按成功生成的视频秒数计费，计费规则请参见[视频生成](#d809366847gza)。
    

| **模型服务** | **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- | --- |
| 图像检测 | wan2.2-s2v-detect | 输入图像：0.004元/张 | 200张 |
| 视频生成 | wan2.2-s2v | 输出视频： - 480P：0.5元/秒 - 720P：0.9元/秒 | 100秒 |

### **万相-图生动作**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输出视频模式** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| wan2.2-animate-move | 标准模式`wan-std` | 0.4元/秒 | 50秒 有效期：阿里云百炼开通后90天内 |
| 专业模式`wan-pro` | 0.6元/秒 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输出视频模式** | **输出单价** |
| --- | --- | --- |
| wan2.2-animate-move | 标准模式`wan-std` | 0.880709元/秒 |
| 专业模式`wan-pro` | 1.321063元/秒 |

### **万相-视频换人**

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输出视频模式** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| wan2.2-animate-mix | 标准模式`wan-std` | 0.6元/秒 | 50秒 有效期：阿里云百炼开通后90天内 |
| 专业模式`wan-pro` | 0.9元/秒 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输出视频模式** | **输出单价** |
| --- | --- | --- |
| wan2.2-animate-mix | 标准模式`wan-std` | 1.321063元/秒 |
| 专业模式`wan-pro` | 1.908202元/秒 |

### **舞动人像AnimateAnyone**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

-   animate-anyone-detect-gen2：输入计费，输出不计费。输入按检测的图像张数计费，只要请求成功（无论检测结果通过与否），每张输入图像均计费一次。
    
-   animate-anyone-template-gen2：输入不计费，输出计费。输出按成功生成的视频秒数计费，计费规则请参见[视频生成](#d809366847gza)。
    
-   animate-anyone-gen2：输入不计费，输出计费。输出按成功生成的视频秒数计费，计费规则请参见[视频生成](#d809366847gza)。
    

| **模型服务** | **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- | --- |
| 图像检测 | animate-anyone-detect-gen2 | 输入图像：0.004元/张 | 200张 |
| 动作模板生成 | animate-anyone-template-gen2 | 输出视频：0.08元/秒 | 1800秒（30分钟） |
| 视频生成 | animate-anyone-gen2 | 输出视频：0.08元/秒 | 1800秒（30分钟） |

### **悦动人像EMO**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

-   emo-detect-v1：输入计费，输出不计费。输入按检测的图像张数计费，只要请求成功（无论检测结果通过与否），每张输入图像均计费一次。
    
-   emo-v1：输入不计费，输出计费。输出按成功生成的视频秒数计费，计费规则请参见[视频生成](#d809366847gza)。
    

| **模型服务** | **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- | --- |
| 图像检测 | emo-detect-v1 | 输入图像：0.004元/张 | 200张 |
| 视频生成 | emo-v1 | 输出视频： - 1:1画幅视频：0.08元/秒 - 3:4画幅视频：0.16元/秒 | 1800秒（30分钟） |

### **灵动人像LivePortrait**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

-   liveportrait-detect：输入计费，输出不计费。输入按检测的图像张数计费，只要请求成功（无论检测结果通过与否），每张输入图像均计费一次。
    
-   liveportrait：输入不计费，输出计费。输出按成功生成的视频秒数计费，计费规则请参见[视频生成](#d809366847gza)。
    

| **模型服务** | **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- | --- |
| 图像检测 | liveportrait-detect | 输入图像：0.004元/张 | 200张 |
| 视频生成 | liveportrait | 输出视频：0.02元/秒 | 1800秒（30分钟） |

### **表情包Emoji**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

-   emoji-detect-v1：输入计费，输出不计费。输入按检测的图像张数计费，只要请求成功（无论检测结果通过与否），每张输入图像均计费一次。
    
-   emoji-v1：输入不计费，输出计费。输出按成功生成的视频秒数计费，计费规则请参见[视频生成](#d809366847gza)。
    

| **模型服务** | **模型名称** | **单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- | --- |
| 图像检测 | emoji-detect-v1 | 输入图像：0.004元/张 | 200张 |
| 视频生成 | emoji-v1 | 输出视频：0.08元/秒 | 1800秒（30分钟） |

### **声动人像VideoRetalk**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

| **模型名称** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- |
| videoretalk | 0.08元/秒 | 1800秒（30分钟） |

### **视频风格重绘**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

| **模型名称** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| video-style-transform | 540P | 0.2元/秒 | 600秒 有效期：阿里云百炼开通后90天内 |
| 720P | 0.5元/秒 |

## **视频生成-第三方模型**

**爱诗-文生视频**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

| **模型名称** | **输出视频类型** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| pixverse/pixverse-v5.6-t2v | 有声视频 `audio=true` | 360P | 0.47元/秒 | 无免费额度 |
| 540P | 0.47元/秒 |
| 720P | 0.53元/秒 |
| 1080P | 0.7元/秒 |
| 无声视频 `audio=false` | 360P | 0.21元/秒 |
| 540P | 0.21元/秒 |
| 720P | 0.27元/秒 |
| 1080P | 0.44元/秒 |

**爱诗-图生视频-基于首帧**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

| **模型名称** | **输出视频类型** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| pixverse/pixverse-v5.6-it2v | 有声视频 `audio=true` | 360P | 0.47元/秒 | 无免费额度 |
| 540P | 0.47元/秒 |
| 720P | 0.53元/秒 |
| 1080P | 0.7元/秒 |
| 无声视频 `audio=false` | 360P | 0.21元/秒 |
| 540P | 0.21元/秒 |
| 720P | 0.27元/秒 |
| 1080P | 0.44元/秒 |

爱诗-图生视频-基于首尾帧

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

| **模型名称** | **输出视频类型** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| pixverse/pixverse-v5.6-kf2v | 有声视频 `audio=true` | 360P | 0.47元/秒 | 无免费额度 |
| 540P | 0.47元/秒 |
| 720P | 0.53元/秒 |
| 1080P | 0.7元/秒 |
| 无声视频 `audio=false` | 360P | 0.21元/秒 |
| 540P | 0.21元/秒 |
| 720P | 0.27元/秒 |
| 1080P | 0.44元/秒 |

**爱诗-参考生视频**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

| **模型名称** | **输出视频类型** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| pixverse/pixverse-v5.6-r2v | 有声视频 `audio=true` | 360P | 0.47元/秒 | 无免费额度 |
| 540P | 0.47元/秒 |
| 720P | 0.53元/秒 |
| 1080P | 0.7元/秒 |
| 无声视频 `audio=false` | 360P | 0.21元/秒 |
| 540P | 0.21元/秒 |
| 720P | 0.27元/秒 |
| 1080P | 0.44元/秒 |

**可灵-视频生成**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

| **模型名称** | **输出视频类型** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- |
| kling/kling-v3-video-generation | 无声视频 | 720P | 0.6元/秒 | 无免费额度 |
| 1080P | 0.8元/秒 |
| 有声视频 | 720P | 0.9元/秒 |
| 1080P | 1.2元/秒 |
| kling/kling-v3-omni-video-generation | 无声视频（无参考视频） | 720P | 0.6元/秒 |
| 1080P | 0.8元/秒 |
| 无声视频（有参考视频） | 720P | 0.9元/秒 |
| 1080P | 1.2元/秒 |
| 有声视频（无参考视频） | 720P | 0.9元/秒 |
| 1080P | 1.2元/秒 |

**Vidu-文生视频**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

| **模型名称** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| vidu/viduq3-pro\\_text2video | 540P | 0.3125元/秒 | 无免费额度 |
| 720P | 0.78125元/秒 |
| 1080P | 0.9375元/秒 |
| vidu/viduq3-turbo\\_text2video | 540P | 0.25元/秒 |
| 720P | 0.375元/秒 |
| 1080P | 0.4375元/秒 |
| vidu/viduq2\\_text2video | 540P | 0.1125元/秒 |
| 720P | 0.21875元/秒 |
| 1080P | 0.375元/秒 |

**Vidu-图生视频-基于首帧**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

| **模型名称** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| vidu/viduq3-pro\\_img2video | 540P | 0.3125元/秒 | 无免费额度 |
| 720P | 0.78125元/秒 |
| 1080P | 0.9375元/秒 |
| vidu/viduq3-turbo\\_img2video | 540P | 0.25元/秒 |
| 720P | 0.375元/秒 |
| 1080P | 0.4375元/秒 |
| vidu/viduq2-pro\\_img2video | 540P | 0.15625元/秒 |
| 720P | 0.34375元/秒 |
| 1080P | 0.71875元/秒 |
| vidu/viduq2-turbo\\_img2video | 540P | 0.0875元/秒 |
| 720P | 0.25元/秒 |
| 1080P | 0.46875元/秒 |

**Vidu-图生视频-基于首尾帧**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

| **模型名称** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| vidu/viduq3-pro\\_start-end2video | 540P | 0.3125元/秒 | 无免费额度 |
| 720P | 0.78125元/秒 |
| 1080P | 0.9375元/秒 |
| vidu/viduq3-turbo\\_start-end2video | 540P | 0.25元/秒 |
| 720P | 0.375元/秒 |
| 1080P | 0.4375元/秒 |
| vidu/viduq2-pro\\_start-end2video | 540P | 0.15625元/秒 |
| 720P | 0.34375元/秒 |
| 1080P | 0.71875元/秒 |
| vidu/viduq2-turbo\\_start-end2video | 540P | 0.0875元/秒 |
| 720P | 0.25元/秒 |
| 1080P | 0.46875元/秒 |

**Vidu-参考生视频**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

> 仅输出计费，计费规则请参见[视频生成](#d809366847gza)。

| **模型名称** | **输出视频分辨率** | **输出单价** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| vidu/viduq2-pro\\_reference2video | 540P | 0.25元/秒 | 无免费额度 |
| 720P | 0.3125元/秒 |
| 1080P | 0.78125元/秒 |
| vidu/viduq2\\_reference2video | 540P | 0.21875元/秒 |
| 720P | 0.28125元/秒 |
| 1080P | 0.71875元/秒 |

## **文本向量**

计费规则：按输入Token计费，输出不计费。

影响计费的因素：若模型支持[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)，其输入和输出Token单价均按实时推理价格的50%计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输入单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) 有效期：阿里云百炼开通后90天内 |
| --- | --- | --- |
| text-embedding-v4 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 0.5元 | 100万Token |
| text-embedding-v3 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 0.5元 | 50万Token |
| text-embedding-v2 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 0.7元 | 50万Token |
| text-embedding-v1 > [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)半价 | 0.7元 | 50万Token |
| text-embedding-async-v2 | 0.7元 | 2000万Token |
| text-embedding-async-v1 | 0.7元 | 2000万Token |

## **国际**

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输入单价（每百万Token）** |
| --- | --- |
| text-embedding-v4 | 0.514元 |
| text-embedding-v3 | 0.514元 |

## **多模态向量**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token计费，输出不计费。

| **模型名称** | **输入单价（每百万Token）** |   | **免费额度**[**（注）**](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| **文本** | **图片/视频** |
| qwen3-vl-embedding | 0.7元 | 1.8元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| qwen2.5-vl-embedding |
| tongyi-embedding-vision-plus | 0.5元 | 0.5元 |
| tongyi-embedding-vision-flash | 0.15元 | 0.15元 |
| multimodal-embedding-v1 | 0.7元 | 0.9元 |

## **文本分类、抽取、排序**

### **OpenNLU**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token计费，输出不计费。

| **模型名称** | **输入单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| opennlu-v1 | 4.65元 | 100万Token 有效期：阿里云百炼开通后90天内 |

### **文本排序模型**

计费规则：按输入Token计费，输出不计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输入单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| qwen3-rerank | 0.5元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| gte-rerank-v2 | 0.8元 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

| **模型名称** | **输入单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- |
| qwen3-rerank | 0.5元 | 各100万Token 有效期：阿里云百炼开通后90天内 |
| gte-rerank-v2 | 0.8元 |

## **行业模型**

### **通义法睿**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| farui-plus | 20元 | 20元 | 无免费额度 |

### **意图理解**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| tongyi-intent-detect-v3 | 0.4元 | 1元  | 100万Token 有效期：阿里云百炼开通后90天内 |

### **角色扮演**

计费规则：按输入Token和输出Token计费。

## 中国内地

在[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| qwen-plus-character | 0.8元 | 2元  | 100万Token 有效期：阿里云百炼开通后90天内 |

## 国际

在[国际部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下，接入点与数据存储均位于**新加坡地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

**说明**

国际部署模式的模型无免费额度。

| **模型名称** | **输入单价 （每百万Token）** | **输出单价 （每百万Token）** |
| --- | --- | --- |
| qwen-plus-character-ja | 3.67元 | 10.275元 |

### **界面交互**

**说明**

仅支持[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)。接入点与数据存储均位于**北京地域**，模型推理计算资源仅限于中国内地。

计费规则：按输入Token和输出Token计费。

| **模型名称** | **输入单价（每百万Token）** | **输出单价（每百万Token）** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- |
| gui-plus | 1.5元 | 4.5元 | 100万Token 有效期：阿里云百炼开通后90天内 |
| gui-plus-2026-02-26 |

为有效管理和优化在阿里云百炼平台上使用大模型的成本，阿里云百炼提供了节省计划、资源包等多种计费优惠方案。

## 选型指南

为帮助您快速选择，可参考以下选型指南：

-   [AI 通用型节省计划](#universal-savings-plan)**（推荐）**：通过承诺每月消费金额来换取阶梯式折扣，最高可享 5.3 折优惠。该方案可抵扣由阿里云百炼提供推理服务的**所有模型**，灵活性最高，**是绝大多数场景下的首选**。
    
-   [其他模型节省计划](#cb5e825e04esu)：一次性购买固定金额，用于抵扣特定模型系列的调用费用。仅适用于部分模型系列（如万相系列、语音模型系列等），且折扣通常不如通用型节省计划，可按需使用。
    
-   [资源包](#0a9293f0f8tuj)：一次性购买具体资源量（如Tokens、生成图片数量等）。仅适用于抵扣单个特定模型（例如 qwen-plus），且折扣通常不如通用型节省计划，可按需使用。
    

为最大化成本效益，建议优先了解并选择 [AI 通用型节省计划](#universal-savings-plan)。

## **AI 通用型节省计划**

### **核心优势**

AI 通用型节省计划是针对大模型按量付费使用场景设计的折扣方案。您只需承诺在一定期限内（3 个月、6 个月、12 个月或 24 个月）的月消费金额，即可在保留按量付费灵活性的基础上，享受阶梯式折扣，优化模型调用成本。其核心优势如下：

-   **覆盖全面**：可抵扣由阿里云百炼提供推理服务的全量模型，一次购买即可跨模型使用。
    
-   **成本优化显著**：承诺消费金额越高、周期越长，折扣力度越大，最高可享 5.3 折优惠。
    
-   **管理流程便捷**：购买后可立即或按指定时间生效，无需手动激活或绑定，自动抵扣，支持自动续费。
    

### **使用说明**

**生效时间**：可按需选择“开通后立即生效”或“指定时间（按小时）生效”。

**承诺周期说明**：**以月为单位**（从生效日到下个月的对应日），月承诺周期结束时，剩余额度自动过期，不可累积到下一周期。举例：如果一次性订阅了 3 个月的节省计划（月承诺额度 1000 元），**并非在 3 个月内获得 3000 元总额度，而是每月独立获得 1000 元额度**，当月未使用完的部分自动清零，不可累积到下个订阅月。

**抵扣范围**：

-   **支持抵扣**：模型调用（输入和输出 Tokens）、工具调用产生的额外 Token、上下文缓存、批量推理等产生的费用。
    
-   **不支持抵扣**：工具调用的服务费用（如联网搜索策略费用等），模型调优、模型部署产生的费用。
    

**抵扣逻辑**：

-   抵扣顺序：**新人免费额度 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费**。
    
-   多个同类型的节省计划：优先抵扣先到期的节省计划。若到期时间相同，则优先抵扣先购买的节省计划。
    
-   超出部分处理：如果同类节省计划全部到期或额度全部抵扣完后，仍有超出部分，自动转为按量付费。
    

**查询账单**：请参见[如何查询节省计划账单](https://help.aliyun.com/zh/user-center/how-to-check-the-savings-plan-bill)。

### **购买指引**

| **购买方式** | [点击购买 AI 通用型节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_GenAI_spn_cn) |
| --- | --- |
| **支持的抵扣范围** | 不同档位享受不同的折扣。 - A 类：[文本生成-千问](https://help.aliyun.com/zh/model-studio/models#785eb398acxz7)、[文本生成-千问-开源版](https://help.aliyun.com/zh/model-studio/models#461c63471cf8d)、[文本向量](https://help.aliyun.com/zh/model-studio/models#d2e1e5c9648hj)、[多模态向量](https://help.aliyun.com/zh/model-studio/models#f24b38c1fa2t7)、[排序模型](https://help.aliyun.com/zh/model-studio/models#2965731b907rk)、[行业模型](https://help.aliyun.com/zh/model-studio/models#815d8e6b3a226)、工具调用（[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)、[联网搜索](https://help.aliyun.com/zh/model-studio/web-search)、[网页抓取](https://help.aliyun.com/zh/model-studio/web-extractor)等）产生的额外 Token 用量 - B 类：[图像生成](https://help.aliyun.com/zh/model-studio/models#4611ffaa38hnp)、[语音合成（文本转语音）](https://help.aliyun.com/zh/model-studio/models#b9e5744149hd6)、[语音识别（语音转文本）与翻译（语音转成指定语种的文本）](https://help.aliyun.com/zh/model-studio/models#696c1bf328gf9)、[视频生成-万相与视频编辑](https://help.aliyun.com/zh/model-studio/models#43aa6e41fd25m) - C 类：[DeepSeek](https://help.aliyun.com/zh/model-studio/models#935bd5ba5cg5d)、[Kimi](https://help.aliyun.com/zh/model-studio/models#2363cbf60fe6m)、[GLM](https://help.aliyun.com/zh/model-studio/models#059d6a5d1chfp)、[MiniMax](https://help.aliyun.com/zh/model-studio/models#7b36766b81de6) > 三方直供模型不支持抵扣，详情参见[Q：三方直供模型支持抵扣 AI 通用节省计划吗？](#85a29cab67489) |
| **每月承诺消费金额** | 用于抵扣模型服务按量计费的每月承诺消费额。可自定义金额，1000 元起，以 10 元为单位调整，不设上限。 |
| **承诺周期** | 可选择以下四个档位的承诺周期：3个月、6个月、12个月、24个月 |
| **付费方式** | - 全预付：一次性支付整个**承诺周期**内的全部承诺消费金额，可享最大折扣。 - 零预付：购买时无需支付，之后按月支付承诺消费金额。**零预付需联系商务经理开通白名单后使用。** |
| **折扣** | 请参考[折扣信息](#85335bf156qcf)。 |
| **开通时间选择** | 可按需选择“开通后立即生效”或“指定时间（按小时）生效”。 |

### 折扣信息

不同模型、不同档位、承诺周期和付款方式享受不同的折扣。

例如：您选择了为期 12 个月、每月承诺消费 10,000 元的节省计划，采用全预付的方式支付，此时调用千问文本生成模型（A 类）时，享受 8 折优惠，即一次原价 1 元的模型调用，实际从您的节省计划额度中抵扣 0.8 元。

| **付款方式** | **月承诺金额（元）** | **A类模型** |   |   |   | **B类模型** |   |   |   | **C类** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3个月 | 6个月 | 12个月 | 24个月 | 3个月 | 6个月 | 12个月 | 24个月 | 全周期 |
| **全预付** | \\[1,000, 5,000) | 8.8折 | 8.6折 | 8.4折 | 8.2折 | 8.3折 | 8折  | 7.7折 | 7.4折 | 无折扣 |
| \\[5,000, 10,000) | 8.6折 | 8.4折 | 8.2折 | 8折  | 8折  | 7.7折 | 7.4折 | 7.1折 | 无折扣 |
| \\[10,000, 30,000) | 8.4折 | 8.2折 | 8折  | 7.8折 | 7.7折 | 7.4折 | 7.1折 | 6.8折 | 无折扣 |
| \\[30,000, 50,000) | 8.2折 | 8折  | 7.8折 | 7.6折 | 7.4折 | 7.1折 | 6.8折 | 6.5折 | 无折扣 |
| \\[50,000, 100,000) | 8折  | 7.8折 | 7.6折 | 7.4折 | 7.1折 | 6.8折 | 6.5折 | 6.2折 | 无折扣 |
| \\[100,000, 300,000) | 7.8折 | 7.6折 | 7.4折 | 7.2折 | 6.8折 | 6.5折 | 6.2折 | 5.9折 | 无折扣 |
| \\[300,000, 1,000,000) | 7.6折 | 7.4折 | 7.2折 | 7折  | 6.5折 | 6.2折 | 5.9折 | 5.6折 | 无折扣 |
| \\[1,000,000, ~) | 7.4折 | 7.2折 | 7折  | 6.8折 | 6.2折 | 5.9折 | 5.6折 | 5.3折 | 无折扣 |
| **零预付** > 需联系商务经理开通 | \\[1,000, 5,000) | 9折  | 8.8折 | 8.6折 | 8.4折 | 8.5折 | 8.2折 | 7.9折 | 7.6折 | 无折扣 |
| \\[5,000, 10,000) | 8.8折 | 8.6折 | 8.4折 | 8.2折 | 8.2折 | 7.9折 | 7.6折 | 7.3折 | 无折扣 |
| \\[10,000, 30,000) | 8.6折 | 8.4折 | 8.2折 | 8折  | 7.9折 | 7.6折 | 7.3折 | 7折  | 无折扣 |
| \\[30,000, 50,000) | 8.4折 | 8.2折 | 8折  | 7.8折 | 7.6折 | 7.3折 | 7折  | 6.7折 | 无折扣 |
| \\[50,000, 100,000) | 8.2折 | 8折  | 7.8折 | 7.6折 | 7.3折 | 7折  | 6.7折 | 6.4折 | 无折扣 |
| \\[100,000, 300,000) | 8折  | 7.8折 | 7.6折 | 7.4折 | 7折  | 6.7折 | 6.4折 | 6.1折 | 无折扣 |
| \\[300,000, 1,000,000) | 7.8折 | 7.6折 | 7.4折 | 7.2折 | 6.7折 | 6.4折 | 6.1折 | 5.8折 | 无折扣 |
| 1,000,000 及以上 | 7.6折 | 7.4折 | 7.2折 | 7折  | 6.4折 | 6.1折 | 5.8折 | 5.5折 | 无折扣 |

### 生命周期管理

您可以访问[节省计划总览页面](https://usercenter2.aliyun.com/resource/spn/overview)管理您的节省计划。

#### 节省计划续订

您可以登录[费用与成本](https://usercenter2.aliyun.com/home)控制台，左侧菜单选择**费用** > **我的订阅**，查看并管理节省计划的订阅状态、生效时间、自动续费状态等。节省计划不支持退订。

#### **查询折扣**

在 AI 通用型节省计划中，不同模型、不同档位、承诺周期和付款方式享受不同的折扣。您可以访问[节省计划价格折扣详情页面](https://usercenter2.aliyun.com/resource/spn/price)进行查询，**适用商品**选择**百炼大模型推理**或**百炼大模型-垂类模型**，以查看对应的按量折扣。

#### 查询账单

进入[费用与成本](https://usercenter2.aliyun.com/home)控制台，左侧菜单选择**账单** > **账单详情**，**产品名称**选择**大模型服务平台百炼**，**商品名称**选择 **AI 通用型节省计划**。页面默认展示当月明细账单。详情请参考[如何查询节省计划账单](https://help.aliyun.com/zh/user-center/how-to-check-the-savings-plan-bill)。

## **其他模型节省计划**

其他模型节省计划

与 AI 通用型节省计划相比，其他模型节省计划更适合用量较小或需求高度集中于某一特定模型的场景。

### 使用说明

**生效时间**：节省计划购买后立即生效。

**有效期说明**：有效期根据购买套餐而定。超出有效期后，节省计划中剩余的金额，将无法使用，不支持退款。

**抵扣范围**：支持抵扣模型调用费用（输入和输出 Tokens）。不支持抵扣工具调用、上下文缓存、批量推理等产生的费用。不支持抵扣模型调优、模型部署产生的费用。

**抵扣逻辑**：

-   抵扣顺序：**新人免费额度 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费**。
    
-   多个同类型的节省计划：优先抵扣先到期的节省计划。若到期时间相同，则优先抵扣先购买的节省计划。
    
-   超出部分处理：如果同类节省计划全部到期或额度全部抵扣完后，仍有超出部分，自动转为按量付费。
    

**查询账单**：请参见[如何查询节省计划账单](https://help.aliyun.com/zh/user-center/how-to-check-the-savings-plan-bill)。

### **支持的节省计划**

## **大语言模型**

| **购买方式** | [单击此处购买大语言模型推理节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_llminference_spn_public_cn) |
| --- | --- |
| **档位** | 阿里云百炼提供购买的档位包括：20元、100元、1,000元、5,000元、10,000元、20,000元、50,000元、100,000元、200,000元、300,000元、500,000元。 |
| **折扣** | 上述档位均无折扣，按[模型调用价格](https://help.aliyun.com/zh/model-studio/model-pricing)进行扣费。 |
| **有效期** | - 对于20元档，有效期1个月。 - 对于100元档，有效期3个月。 - 对于1,000元档，有效期6个月。 - 对于5,000元、10,000元、20,000元、50,000元、100,000元、200,000元、300,000元、500,000元八档，有效期1年。 |
| **适用地域** | 北京地域 |
| **适用模型** | 适用于已上架阿里云百炼平台并以 Token 计费的文本生成模型，模型范围包括： - 通用大语言模型： - 商业版：[千问Max](https://help.aliyun.com/zh/model-studio/models#qwen-max-cn-bj)、[千问Plus](https://help.aliyun.com/zh/model-studio/models#03a05ab98953u)、[千问Flash](https://help.aliyun.com/zh/model-studio/models#9b418d9a481yp)、[千问Turbo](https://help.aliyun.com/zh/model-studio/models#218847c4b35vb)、[QwQ](https://help.aliyun.com/zh/model-studio/models#5b345b2e75d35)、[千问Long](https://help.aliyun.com/zh/model-studio/models#2a9527533ei3o) - 开源版：[Qwen3](https://help.aliyun.com/zh/model-studio/models#2c9c4628c9yyd)、[QwQ-开源版](https://help.aliyun.com/zh/model-studio/models#690e39465dvqv)、[QwQ-Preview](https://help.aliyun.com/zh/model-studio/models#18e88cc886ll3)、[Qwen2.5](https://help.aliyun.com/zh/model-studio/models#15f2bdc5dd3zd)、[Qwen2](https://help.aliyun.com/zh/model-studio/models#4969f9cd9170b)、[Qwen1.5](https://help.aliyun.com/zh/model-studio/models#759b2e1092vt2)、[Qwen-Math](https://help.aliyun.com/zh/model-studio/models#be175f0a9ftkr)、[Qwen-Coder](https://help.aliyun.com/zh/model-studio/models#8fa09f2273rf2) - 第三方模型：[DeepSeek](https://help.aliyun.com/zh/model-studio/models#21ab4c25c7lml)、[Kimi](https://help.aliyun.com/zh/model-studio/models#0ca6cec0252yp)、[GLM](https://help.aliyun.com/zh/model-studio/models#glm4.5)、[MiniMax-abab](https://help.aliyun.com/zh/model-studio/models#6be76657ccfhm) - 多模态模型： - 商业版：[千问Omni](https://help.aliyun.com/zh/model-studio/models#90e80b9e42ged)、[千问Omni-Realtime](https://help.aliyun.com/zh/model-studio/models#6deec483126rk)、[QVQ](https://help.aliyun.com/zh/model-studio/models#c49b76da1axvk)、[千问VL](https://help.aliyun.com/zh/model-studio/models#94b18818a6ywy)、[千问OCR](https://help.aliyun.com/zh/model-studio/models#55c81ba3ccgct)、[千问Audio](https://help.aliyun.com/zh/model-studio/models#d54c2c9409nml) - 开源版：[Qwen-Omni](https://help.aliyun.com/zh/model-studio/models#94586edea0msj)、[Qwen3-Omni-Captioner](https://help.aliyun.com/zh/model-studio/models#239a84452a1tf)、[Qwen-VL](https://help.aliyun.com/zh/model-studio/models#ad306c856cmar)、[Qwen-Audio](https://help.aliyun.com/zh/model-studio/models#7d1dec0b7ffg1)、[QvQ](https://help.aliyun.com/zh/model-studio/models#7e201f80afdtg) - 领域模型：[千问数学模型](https://help.aliyun.com/zh/model-studio/models#81e8bfd40bb9n)、[千问Coder](https://help.aliyun.com/zh/model-studio/models#5d7f137a6467d)、[千问翻译模型](https://help.aliyun.com/zh/model-studio/models#5d7f137a6467d)、[千问数据挖掘模型](https://help.aliyun.com/zh/model-studio/models#7f14efe21dy5i)、[千问深入研究模型](https://help.aliyun.com/zh/model-studio/models#89f969cf130us)、[通义晓蜜对话分析模型](https://help.aliyun.com/zh/model-studio/models#067fbf0cceu7d) |

## **万相模型**

| **购买方式** | [单击此处购买万相模型节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_VideoAndImage_spn_cn)。 |
| --- | --- |
| **购买说明** | 阿里云百炼提供五个购买档位，分别为： - 20元：无折扣 - 100元：无折扣 - 1,000元：享9.8折优惠 - 10,000元：享9.5折优惠 - 30,000元：享9折优惠 优惠示例：以 1,000元 档位为例，假设生成某个视频消费1元，实际将从节省计划中抵扣1\\*0.98=0.98元。 |
| **有效期** | - 对于20元、100元两档，有效期3个月。 - 对于1,000元、10,000元、30,000元三档，有效期6个月。 |
| **适用模型** | **图像生成**：wan2.6-image、wan2.6-t2i、wan2.5-t2i-preview、wan2.5-i2i-preview、wan2.2-t2i-plus、wan2.2-t2i-flash、wanx2.0-t2i-turbo、wanx2.1-t2i-plus、wanx2.1-imageedit、wanx2.1-t2i-turbo、wanx-sketch-to-image-lite、wanx-v1 **视频生成**：wan2.6-t2v、wan2.6-i2v、wan2.6-r2v、wan2.5-t2v-preview、wan2.5-i2v-preview、wan2.2-t2v-plus、wan2.2-i2v-flash、wan2.2-t2v-flash、wan2.2-i2v-plus、wanx2.1-vace-plus、wanx2.1-kf2v-plus、wanx2.1-t2v-turbo、wanx2.1-t2v-plus、wanx2.1-i2v-turbo、wanx2.1-i2v-plus 请前往[模型列表](https://help.aliyun.com/zh/model-studio/models)查看所有模型及其调用价格。 |

## **千问语音模型**

| **购买方式** | [单击此处购买千问语音模型节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_VoiceModel_spn_cn)。 |
| --- | --- |
| **购买说明** | 阿里云百炼提供五个购买档位，分别为： - 20元：享9.8折优惠 - 100元：享9.6折优惠 - 500元：享9折优惠 - 1,000元：享8.5折优惠 - 5,000元：享8折优惠 优惠示例：以 1,000元 档位为例，假设消费1元，实际将从节省计划中抵扣1\\*0.85=0.85元。 ASR模型按秒计费，TTS模型按字符计费，请前往[模型列表](https://help.aliyun.com/zh/model-studio/models)查看模型调用价格。 |
| **有效期** | - 对于20元、100元两档，有效期为6个月。 - 对于500元、1,000元、5,000元三档，有效期可选 6 个月或 12 个月。 |
| **适用模型** | 因地域而异： - **北京：** - **语音合成**：[千问实时语音合成（Qwen-TTS-Realtime系列）](https://help.aliyun.com/zh/model-studio/models#05782f7968r7g)、[千问语音合成（Qwen-TTS 系列）](https://help.aliyun.com/zh/model-studio/models#e62b64f642k63)、[CosyVoice语音合成](https://help.aliyun.com/zh/model-studio/models#7a960cc042zwt) - **语音识别/翻译**：[千问实时语音识别（Qwen-ASR-Realtime系列）](https://help.aliyun.com/zh/model-studio/models#04625778f9jd5)、[千问录音文件识别（Qwen-ASR系列）](https://help.aliyun.com/zh/model-studio/models#8017a37ad5a66)、[Fun-ASR语音识别](https://help.aliyun.com/zh/model-studio/models#140159cc9b5iz)、[Gummy语音识别/翻译](https://help.aliyun.com/zh/model-studio/models#9e21336740rk2)、[Paraformer语音识别](https://help.aliyun.com/zh/model-studio/models#c018769cd7y88)、[SenseVoice语音识别](https://help.aliyun.com/zh/model-studio/models#511fe328d19af) - **新加坡：** 1. **语音合成**：[千问实时语音合成（Qwen-TTS-Realtime系列）](https://help.aliyun.com/zh/model-studio/models#05782f7968r7g)、[千问语音合成（Qwen-TTS 系列）](https://help.aliyun.com/zh/model-studio/models#e62b64f642k63) 2. **语音识别**：[千问实时语音识别（Qwen-ASR-Realtime系列）](https://help.aliyun.com/zh/model-studio/models#04625778f9jd5)、[Fun-ASR语音识别](https://help.aliyun.com/zh/model-studio/models#140159cc9b5iz)、[千问录音文件识别（Qwen-ASR系列）](https://help.aliyun.com/zh/model-studio/models#8017a37ad5a66) 请前往[模型列表](https://help.aliyun.com/zh/model-studio/models)查看所有模型。 |

## 向量及排序模型

| **购买方式** | [单击此处购买向量及排序模型服务节省计划。](https://common-buy.aliyun.com/?commodityCode=sfm_embeddingrerank_spn_cn) |
| --- | --- |
| **购买说明** | 阿里云百炼提供五个购买档位，分别为： - 100元：无折扣 - 500元：享 9 折优惠 - 2,000元：享 8 折优惠 - 5,000元：享 7.5 折优惠 - 10,000元：享 7 折优惠 优惠示例：以 1,000元 档位为例，假设消费 1 元，实际将从节省计划中抵扣 1 \\* 0.75 = 0.75（元）。 |
| **有效期** | - 对于100元、500元档位，有效期3个月。 - 对于2,000元档位，有效期6个月。 - 对于5,000元、10,000元档位，有效期12个月。 |
| **适用地域** | 北京地域 |
| **适用模型** | **文本向量**：text-embedding-v4、text-embedding-v3、text-embedding-v2、text-embedding-v1、text-embedding-async-v2、text-embedding-async-v1 **多模态向量**：qwen2.5-vl-embedding、tongyi-embedding-vision-plus、tongyi-embedding-vision-flash、multimodal-embedding-v1 **文本排序**：qwen3-rerank、gte-rerank-v2 请前往[模型列表](https://help.aliyun.com/zh/model-studio/models)查看所有模型及其调用价格。 |

## **资源包**

资源包

您预先购买的是具体的 Token 数量，用于抵扣特定模型**超出免费额度后**产生的实时推理用量。

### 使用说明

**生效时间**：资源包购买后立即生效，无需手动“激活”或“绑定”。

**有效期说明**：有效期根据购买套餐而定。超出有效期后，资源包中剩余的Tokens，自动作废。

**抵扣逻辑**：

-   抵扣顺序：**新人免费额度 > 资源包 > 按量付费**。
    
-   多个同类型的资源包：优先抵扣先到期的资源包。若到期时间相同，则优先抵扣先购买的资源包。
    
-   超出部分处理：如果同类资源包全部到期或额度全部抵扣完后，若仍有超出部分，自动转为按量付费。
    

**余量监控与预警：**

-   **查看余量**：点击[资源包](https://billing-cost.console.aliyun.com/ri/summary?commodityCode=fr)查看剩余量情况，点击**统计**查看使用信息。具体请参见[资源包介绍与选购](https://help.aliyun.com/zh/user-center/resource-package-instance-management)。
    
-   **设置预警**：建议[设置资源包余量预警](https://help.aliyun.com/zh/user-center/configure-balance-alerts)。当资源包使用量低于预设阈值时，系统将通过短信、邮件及站内信自动触发通知。
    

**退订说明**：

-   根据[退订规则](https://help.aliyun.com/zh/user-center/cancel-subscription/)，预付费商品未发生使用的部分，可按未使用额度费用[申请退款](https://billing-cost.console.aliyun.com/refund/refund?commodityType=RESOURCE_PLANS&refundType=NOREASON_REFUND)；已使用的部分则无法退款。
    

### **大语言模型推理资源包**

| **订购地址** | [大语言模型推理资源包qwen-plus](https://common-buy.aliyun.com/?commodityCode=sfm_llminference_dp_cn#/buy) | [大语言模型推理资源包qwen-max](https://common-buy.aliyun.com/?commodityCode=sfm_llminference2_dp_cn#/buy) | [大语言模型推理资源包qwen-turbo](https://common-buy.aliyun.com/?commodityCode=sfm_llminference3_dp_cn#/buy) |
| --- | --- | --- | --- |
| **适用地域** | 北京地域 | 北京地域 | 北京地域 |
| **适用模型** | qwen-plus及qwen-plus-latest 的实时推理服务（[非思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)） | qwen-max及qwen-max-latest 的实时推理服务（[非思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)） | qwen-turbo及qwen-turbo-latest 的实时推理服务（[非思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)） |
| **包含输入和输出总Tokens** | 1,200万/1.1亿 | 1,800万/3,900万/3.9亿/11.7亿/19.5亿 | 3,500万/3.5亿/17.5亿/35亿 |
| **价格（元）** | 11.66/114.4 | 57.6/125/1250/3750/6250 | 11.45/114.45/572.25/1144.5 |
| **有效期** | 自购买日起生效，有效期可选 3 个月、6 个月或 1 年。 | 自购买之日起有效期为 1 年。 | 自购买之日起有效期为 1 年。 |
| **使用限制** | - **qwen-plus**、**qwen-plus-latest** - 仅支持抵扣单次请求输入在`0<Token≤128K`阶梯范围内的实时推理费用（[非思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)，包含输入和输出）。 - 不支持抵扣的费用包括： - 单次请求输入在`Token>128K`阶梯范围产生的费用。 - [Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)、[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)、[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)、[模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)产生的费用。 - **qwen-max**、**qwen-max-latest、qwen-turbo**、**qwen-turbo-latest** - 仅支持抵扣实时推理产生的费用（[非思考模式](https://help.aliyun.com/zh/model-studio/deep-thinking)，包含输入和输出），不支持抵扣[Batch调用](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)、[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)、[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)、[模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)产生的费用。 |   |   |

### 图像生成模型资源包

| **订购地址** | [千问图像生成模型资源包qwen-image](https://common-buy.aliyun.com/?commodityCode=sfm_qwenimage_dp_cn) | [千问图像生成模型资源包qwen-image-plus](https://common-buy.aliyun.com/?commodityCode=sfm_qwenimageplus_dp_cn) |
| --- | --- | --- |
| **适用地域** | 北京地域 | 北京地域 |
| **适用模型** | **文生图**：qwen-image **图像编辑**：qwen-image-edit | **文生图**：qwen-image-plus **图像编辑**：qwen-image-edit-plus |
| **资源包容量 (生成图片张数)** | 80/400 | 100/1,000/10,000/100,000/500,000 |
| **价格（元）** | 20/100 | 享阶梯折扣： 20/196（9.8折）/1,900（9.5折）/18,000（9折）/85,000（8.5折） |
| **有效期** | 自购买之日起有效期为 3 个月。 | 对于100、1,000张档位，自购买之日起有效期为3个月。 对于10,000、100,000张档位，自购买之日起有效期为6个月。 对于500,000张档位，自购买之日起有效期为12个月。 |
| **说明** | 使用文生图模型生成一张图片消耗 1 张额度，使用图片编辑模型编辑一张图片消耗 1.2 张额度。 资源包容量耗尽后，将自动转为按量付费模式，超出部分按各模型对应的价格进行计费，详见[模型调用计费](https://help.aliyun.com/zh/model-studio/model-pricing)。 | 生成或编辑一张图片消耗 1 张额度。 资源包容量耗尽后，将自动转为按量付费模式，超出部分按各模型对应的价格进行计费，详见[模型调用计费](https://help.aliyun.com/zh/model-studio/model-pricing)。 |

## **常见问题**

#### **Q：节省计划和资源包是否支持退订？**

A：所有节省计划均不支持退订，请按需购买。资源包未发生使用的部分，可按未使用额度费用[申请退款](https://billing-cost.console.aliyun.com/refund/refund?commodityType=RESOURCE_PLANS&refundType=NOREASON_REFUND)，已使用的部分则无法退款。

#### **Q：资源包和节省计划如果同时存在，怎么扣费？**

A：系统的抵扣优先级为：**免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费**。即：先用免费额度；用完后扣资源包；资源包不够或不适用时，扣节省计划；最后才使用账户余额。

#### **Q：为什么购买了节省计划，但没有抵扣？**

A：常见原因如下：

1.  **模型不匹配**：您购买了其他节省计划，但调用的模型不在适用范围内。例如：购买了大语言模型节省计划，却调用了万相系列模型。您可以选择购买 [AI 通用型节省计划](#universal-savings-plan)以实现跨模型调用。
    
2.  **使用了不支持的功能**：所有节省计划均不支持抵扣[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)、[模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)费用以及工具调用的服务费用（如联网搜索策略费用等）。只有 AI 通用型节省计划支持抵扣上下文缓存、批量推理等产生的费用，以及工具调用产生的额外 Token 消耗，而其他节省计划不支持。
    
3.  **免费额度未用完**：系统抵扣顺序为：**免费额度 > 节省计划**。节省计划仅抵扣免费额度用尽后产生的账单。
    

#### **Q：三方直供模型支持抵扣 AI 通用节省计划吗？**

A：不支持。[C类模型](#standard-sp-row3)中，由阿里云百炼提供推理服务的版本支持抵扣，第三方直供版本不支持抵扣。可以在[百炼模型广场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)中通过模型卡片右上角标识判断。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9433444771/p1062187.png)

#### **Q：为什么购买了资源包，但没有抵扣？**

A：资源包的抵扣需要满足特定条件，常见原因如下：

1.  模型不匹配：您调用的模型与购买的资源包不一致。例如，购买 qwen-max 资源包却调用了 qwen-plus模型。
    
2.  使用了不支持的功能：资源包**不支持抵扣**这些功能产生的费用：[批量推理（Batch）](https://help.aliyun.com/zh/model-studio/batch-inference)、[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)、[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)、[模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)。
    
3.  Token 长度超限：对于 qwen-plus 资源包，单次请求输入超过 128K Token 的部分无法抵扣。
    
4.  免费额度未用完：系统抵扣顺序为：**免费额度 > 资源包**。资源包仅抵扣免费额度用尽后产生的账单。
    

#### **Q：如果先购买了资源包但未开通阿里云百炼服务，应该如何使用？**

A：请先[开通阿里云百炼的模型服务](https://help.aliyun.com/zh/model-studio/get-api-key#02dae3d7d6nip)。服务开通后，优先会抵扣免费额度，待免费额度消耗完后，才会开始抵扣资源包。